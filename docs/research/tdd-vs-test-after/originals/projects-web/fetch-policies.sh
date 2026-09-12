#!/usr/bin/env bash
set -euo pipefail

base_dir="$(cd "$(dirname "$0")" && pwd)"
tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

fetch_github_file() {
  local repo="$1" ref="$2" path="$3" target="$4"
  gh api "repos/$repo/contents/$path?ref=$ref" --jq .content | tr -d '\n' | base64 --decode > "$base_dir/$target"
}

django_ref="$(gh api repos/django/django/commits/main --jq .sha)"
rails_ref="$(gh api repos/rails/rails/commits/main --jq .sha)"
react_ref="$(gh api repos/facebook/react/commits/main --jq .sha)"
next_ref="$(gh api repos/vercel/next.js/commits/canary --jq .sha)"
gitlab_ref="$(curl -sS 'https://gitlab.com/api/v4/projects/278964/repository/branches/master' | jq -r '.commit.id')"

fetch_github_file django/django "$django_ref" docs/internals/contributing/writing-code/submitting-patches.txt django-submitting-patches.txt
fetch_github_file django/django "$django_ref" docs/internals/contributing/writing-code/unit-tests.txt django-unit-tests.txt
fetch_github_file rails/rails "$rails_ref" CONTRIBUTING.md rails-CONTRIBUTING.md
fetch_github_file rails/rails "$rails_ref" guides/source/contributing_to_ruby_on_rails.md rails-contributing-guide.md
fetch_github_file facebook/react "$react_ref" CONTRIBUTING.md react-CONTRIBUTING.md
fetch_github_file vercel/next.js "$next_ref" contributing.md nextjs-contributing.md
fetch_github_file vercel/next.js "$next_ref" contributing/core/testing.md nextjs-testing.md

curl -sSL -D "$base_dir/react-legacy-how-to-contribute.headers.txt" \
  'https://reactjs.org/docs/how-to-contribute.html' \
  -o "$base_dir/react-legacy-how-to-contribute.html"

for path_target in \
  'doc/development/contributing/merge_request_workflow.md:gitlab-merge-request-workflow.md' \
  'doc/development/testing_guide/testing_strategy.md:gitlab-testing-strategy.md' \
  'doc/development/code_review.md:gitlab-code-review.md'
do
  path="${path_target%%:*}"
  target="${path_target#*:}"
  encoded_path="$(jq -rn --arg value "$path" '$value|@uri')"
  curl -sS "https://gitlab.com/api/v4/projects/278964/repository/files/$encoded_path/raw?ref=$gitlab_ref" -o "$base_dir/$target"
done

jq -n \
  --arg fetched_at "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --arg django_ref "$django_ref" \
  --arg rails_ref "$rails_ref" \
  --arg react_ref "$react_ref" \
  --arg next_ref "$next_ref" \
  --arg gitlab_ref "$gitlab_ref" \
  '{fetched_at:$fetched_at,refs:{django:$django_ref,rails:$rails_ref,react:$react_ref,nextjs:$next_ref,gitlab:$gitlab_ref}}' \
  > "$tmp_dir/base-manifest.json"

jq -n --slurpfile base "$tmp_dir/base-manifest.json" --arg base_dir "$base_dir" \
  '$base[0] + {files: []}' > "$base_dir/manifest.json"

for file in \
  django-submitting-patches.txt django-unit-tests.txt \
  rails-CONTRIBUTING.md rails-contributing-guide.md \
  react-CONTRIBUTING.md react-legacy-how-to-contribute.html react-legacy-how-to-contribute.headers.txt \
  nextjs-contributing.md nextjs-testing.md \
  gitlab-merge-request-workflow.md gitlab-testing-strategy.md gitlab-code-review.md
do
  sha="$(shasum -a 256 "$base_dir/$file" | awk '{print $1}')"
  size="$(wc -c < "$base_dir/$file" | tr -d ' ')"
  jq --arg file "$file" --arg sha "$sha" --argjson size "$size" \
    '.files += [{file:$file,sha256:$sha,bytes:$size}]' "$base_dir/manifest.json" > "$tmp_dir/manifest-next.json"
  mv "$tmp_dir/manifest-next.json" "$base_dir/manifest.json"
done
