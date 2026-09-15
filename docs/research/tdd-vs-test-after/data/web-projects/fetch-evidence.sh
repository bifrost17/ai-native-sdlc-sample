#!/usr/bin/env bash
set -euo pipefail

base_dir="$(cd "$(dirname "$0")" && pwd)"
tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

fetch_github_pr() {
  local repo="$1" number="$2" slug="$3"
  local out_dir="$base_dir/$slug"
  mkdir -p "$out_dir"

  gh api "repos/$repo/pulls/$number" > "$tmp_dir/pull.json"
  gh api --paginate "repos/$repo/pulls/$number/commits?per_page=100" --slurp | jq 'add' > "$tmp_dir/commits.json"
  gh api --paginate "repos/$repo/pulls/$number/files?per_page=100" --slurp | jq 'add' > "$tmp_dir/files.json"

  jq -r '.[].sha' "$tmp_dir/commits.json" | while IFS= read -r sha; do
    gh api "repos/$repo/commits/$sha" | jq '{sha, html_url, commit: {author: .commit.author, committer: .commit.committer, message: .commit.message}, parents, stats, files}'
  done | jq -s '.' > "$tmp_dir/commit-details.json"

  local head_sha
  head_sha="$(jq -r '.head.sha' "$tmp_dir/pull.json")"
  gh api "repos/$repo/commits/$head_sha/check-runs?per_page=100" \
    --jq '{total_count, check_runs: [.check_runs[] | {name,status,conclusion,started_at,completed_at,html_url,app:.app.slug}]}' \
    > "$tmp_dir/check-runs.json" || printf '{"unavailable":true}\n' > "$tmp_dir/check-runs.json"
  gh api "repos/$repo/commits/$head_sha/status" \
    --jq '{state,total_count,sha,statuses:[.statuses[]|{context,state,description,target_url,created_at,updated_at}]}' \
    > "$tmp_dir/status.json" || printf '{"unavailable":true}\n' > "$tmp_dir/status.json"

  jq -n \
    --slurpfile pull "$tmp_dir/pull.json" \
    --slurpfile commits "$tmp_dir/commits.json" \
    --slurpfile files "$tmp_dir/files.json" \
    --slurpfile details "$tmp_dir/commit-details.json" \
    --slurpfile checks "$tmp_dir/check-runs.json" \
    --slurpfile status "$tmp_dir/status.json" \
    '{source:"GitHub REST API", fetched_at:(now|todate), pull:$pull[0], commits:$commits[0], files:$files[0], commit_details:$details[0], check_runs:$checks[0], combined_status:$status[0]}' \
    > "$out_dir/pr-$number.json"
}

fetch_gitlab_mr() {
  local iid="$1"
  local out_dir="$base_dir/gitlab"
  local api="https://gitlab.com/api/v4/projects/278964"
  mkdir -p "$out_dir"

  curl -sS "$api/merge_requests/$iid" > "$tmp_dir/mr.json"
  curl -sS --get --data-urlencode 'per_page=100' "$api/merge_requests/$iid/commits" > "$tmp_dir/commits.json"
  curl -sS --get --data-urlencode 'per_page=100' "$api/merge_requests/$iid/diffs" > "$tmp_dir/diffs.json"
  curl -sS --get --data-urlencode 'per_page=100' "$api/merge_requests/$iid/pipelines" > "$tmp_dir/pipelines.json"
  curl -sS --get --data-urlencode 'per_page=100' --data-urlencode 'sort=asc' "$api/merge_requests/$iid/notes" > "$tmp_dir/notes.json"

  jq -r '.[].id' "$tmp_dir/commits.json" | while IFS= read -r sha; do
    curl -sS "$api/repository/commits/$sha/diff" | jq --arg sha "$sha" '{sha:$sha,diffs:.}'
  done | jq -s '.' > "$tmp_dir/commit-details.json"

  jq -n \
    --slurpfile mr "$tmp_dir/mr.json" \
    --slurpfile commits "$tmp_dir/commits.json" \
    --slurpfile diffs "$tmp_dir/diffs.json" \
    --slurpfile details "$tmp_dir/commit-details.json" \
    --slurpfile pipelines "$tmp_dir/pipelines.json" \
    --slurpfile notes "$tmp_dir/notes.json" \
    '{source:"GitLab REST API", fetched_at:(now|todate), merge_request:$mr[0], commits:$commits[0], diffs:$diffs[0], commit_details:$details[0], pipelines:$pipelines[0], notes:$notes[0]}' \
    > "$out_dir/mr-$iid.json"
}

mkdir -p "$base_dir" "$base_dir/django" "$base_dir/rails" "$base_dir/react" "$base_dir/nextjs" "$base_dir/gitlab"

for repo_slug in django/django rails/rails vercel/next.js; do
  repo="${repo_slug%%/*}"
  name="${repo_slug#*/}"
  case "$repo_slug" in
    django/django) slug="django" ;;
    rails/rails) slug="rails" ;;
    vercel/next.js) slug="nextjs" ;;
  esac
  gh api -X GET search/issues \
    -f q="repo:$repo_slug is:pr is:merged merged:2026-08-01..2026-09-12" \
    -f per_page=100 -f page=1 > "$base_dir/$slug/candidates-page1.json"
done

for search_spec in \
  'django|django/django' \
  'rails|rails/rails' \
  'nextjs|vercel/next.js'
do
  slug="${search_spec%%|*}"
  repo_slug="${search_spec#*|}"
  gh api -X GET search/issues \
    -f q="repo:$repo_slug is:pr is:merged merged:2024-09-12..2026-09-12 (refactor OR simplify OR cleanup OR move OR rename) in:title" \
    -f per_page=100 -f page=1 > "$base_dir/$slug/candidates-refactor-title-page1.json"
done

gh api 'repos/facebook/react/pulls?state=closed&sort=updated&direction=desc&per_page=100' > "$base_dir/react/candidates-recent.json"
curl -sS --get \
  --data-urlencode 'state=merged' \
  --data-urlencode 'updated_after=2026-08-01T00:00:00Z' \
  --data-urlencode 'updated_before=2026-09-13T00:00:00Z' \
  --data-urlencode 'order_by=updated_at' \
  --data-urlencode 'sort=desc' \
  --data-urlencode 'per_page=100' \
  'https://gitlab.com/api/v4/projects/278964/merge_requests' > "$base_dir/gitlab/candidates-page1.json"

for number in 20842 21875 21886 21746 21881 21482 21064 21696 21519 21507 21424; do fetch_github_pr django/django "$number" django; done
for number in 58710 58695 58668 58747 53403 58711 58684 58735 58673 58497; do fetch_github_pr rails/rails "$number" rails; done
for number in 37513 37339 37491 37579 37539 37545 37574 37573 37550; do fetch_github_pr facebook/react "$number" react; done
for number in 98532 98571 97203 98506 98252 98512 98575 98504 98347 97988; do fetch_github_pr vercel/next.js "$number" nextjs; done
for iid in 254453 254982 255081 254560 254677 254620 254298 252442 253525; do fetch_gitlab_mr "$iid"; done
