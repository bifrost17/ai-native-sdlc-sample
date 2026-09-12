"""Index already downloaded research sources; does not download or execute them."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re

BASE = Path(__file__).resolve().parents[1]
ORIGINALS = BASE / 'originals'
ROOT = json.loads((BASE / 'data/root-sources.json').read_text())
AGENT = json.loads((BASE / 'data/agent-studies-sources.json').read_text())
PROJECT = json.loads((ORIGINALS / 'projects-agent/source-manifest.json').read_text())
WEB = json.loads((ORIGINALS / 'projects-web/manifest.json').read_text())
provenance = {}
errors = []


def add(path, source):
    p = Path(path)
    if not p.is_absolute():
        p = BASE / p
    if not p.exists():
        errors.append(f'missing: {p}')
        return
    raw = p.read_bytes()
    if source.get('sha256') and hashlib.sha256(raw).hexdigest() != source['sha256']:
        errors.append(f'prior SHA mismatch: {p}')
    if source.get('bytes') is not None and len(raw) != source['bytes']:
        errors.append(f'prior byte mismatch: {p}')
    provenance.setdefault(p.resolve(), []).append(source)


for r in ROOT:
    add(r['local_path'], r)
for s in AGENT['sources']:
    for f in s['files']:
        if 'local_file' not in f:
            continue
        add(f['local_file'].split('tdd-vs-test-after/', 1)[-1], {
            **f, 'title': s['title'], 'authors': s['authors'],
            'read_version': s.get('read_version'),
            'versioned_url': s.get('versioned_url'), 'version_dates': s.get('version_dates'),
            'retrieved_on': s['access_date'], 'representation': 'downloaded source',
        })
for f in AGENT['supplements']:
    add(f['local_file'].split('tdd-vs-test-after/', 1)[-1], f)
for d in PROJECT['documents']:
    add('originals/projects-agent/' + d['file'], {
        **d, 'retrieved_on': PROJECT.get('captured_on', PROJECT.get('cutoff_date')),
    })

# Pair the project's authored local/source links, not arbitrary links in raw pages.
web_urls = {}
for line in (ORIGINALS / 'projects-web/README.md').read_text().splitlines():
    if not line.startswith('|'):
        continue
    links = re.findall(r'\[[^\]]+\]\(([^)]+)\)', line)
    local = [x for x in links if not x.startswith('https://') and not x.endswith('headers.txt')]
    remote = [x for x in links if x.startswith('https://')]
    web_urls.update(zip(local, remote))
for f in WEB['files']:
    add('originals/projects-web/' + f['file'], {
        **f, 'url': web_urls.get(f['file']), 'retrieved_at': WEB['fetched_at'],
        'representation': 'HTTP headers' if f['file'].endswith('headers.txt') else 'downloaded source',
    })

rows = []
for p in sorted(ORIGINALS.rglob('*')):
    if not p.is_file() or p == ORIGINALS / 'manifest.json':
        continue
    rel = str(p.relative_to(BASE))
    prov = provenance.get(p.resolve(), [])
    if prov:
        kind = 'source snapshot'
    elif p.suffix == '.txt' and p.parent.name == 'studies-agent':
        kind = 'derived text extraction'
    elif p.name.startswith('tddev-') and p.suffix in {'.py', '.md'}:
        kind = 'file extracted from downloaded artifact.zip; not executed'
        prov = [{'source_local': 'originals/studies-agent/tddev-artifact.zip'}]
    else:
        kind = 'research-created index, metadata, or retrieval script'
    raw = p.read_bytes()
    rows.append({'path': rel, 'representation': kind, 'bytes': len(raw),
                 'sha256': hashlib.sha256(raw).hexdigest(), 'provenance': prov})

lines = ['# 원문 전체 보관 목록', '',
    '조사일은 **2026-09-12**다. 아래 링크는 내려받은 본문 전체 또는 원본 파일로 연결한다. '
    'PDF 추출 텍스트·브라우저 snapshot·연구자가 작성한 색인은 원문 파일과 구분한다. '
    '원본 웹 HTML의 외부 이미지·스크립트까지 포함한 완전한 오프라인 사이트는 아니다.', '',
    '파일별 해시·용량·버전·다운로드 URL은 [통합 manifest](manifest.json)에 있다. '
    '논문 저자와 제출 이력은 [서지 데이터](../data/agent-studies-sources.json), '
    '나머지 주요 자료는 [출처 데이터](../data/root-sources.json)에 있다.', '',
    '## 에이전트 논문 11건', '', '| 원문·버전 | 전체 PDF | 보관 HTML | 읽은 버전의 날짜 |',
    '|---|---|---|---|']
for s in AGENT['sources']:
    aid = s['arxiv_id']; version = s.get('read_version', '')
    date = next((d for v, d in s.get('version_dates', []) if 'v'+v == version), s.get('publication_date', ''))
    date = re.sub(r'\s*\([^)]*\)$', '', date)
    title = s['title'].replace('|', '/')
    lines.append(f'| [{title}]({s.get("versioned_url", "https://arxiv.org/abs/"+aid)}) · {version} | [PDF](studies-agent/{aid}.pdf) | [HTML](studies-agent/{aid}.html) · [서지·이력](studies-agent/{aid}.abstract.html) | {date} |')
lines += ['', 'TDFlow의 [EACL 2026 출판 PDF](studies-agent/tdflow-eacl-2026.pdf)도 별도로 저장했다. '
    '논문별 모델 버전과 측정 조건은 [근거 카드](../working/agent-studies.md)에 있다.', '',
    '## 사람 대상 연구 5건', '', '| 자료 | 원문 URL | 로컬 전체 PDF | 판본 |', '|---|---|---|---|']
for r in ROOT:
    if r['id'].startswith('H'):
        lines.append(f'| {r["title"]} | [원출처]({r["url"]}) | [PDF]({r["local_path"].removeprefix("originals/")}) | {r["date"]} |')
lines += ['', 'H2는 저자 원고의 외부 미러다. 최종 출판 조판본과 같다고 보장하지 않으며, '
    '원고의 연구 수 표기 불일치를 [상세 보고서](../human-studies.md)에 남겼다.', '',
    '## 공개 실험·실무자 원문', '', '| 자료 | 원문 URL | 로컬 원본 전체 | 시점·버전 |', '|---|---|---|---|']
for r in ROOT:
    if r['id'].startswith('B'):
        version = r.get('git_ref', r.get('date', '2026-09-12 수집'))
        lines.append(f'| {r["id"]}: {r["title"]} | [원출처]({r["url"]}) | [전체 파일]({r["local_path"].removeprefix("originals/")}) | {version} |')
lines += ['', 'Finster JSONL은 672행의 공개 결과다. [재집계 결과](../data/finster-recalculation.json)는 '
    '새 에이전트 실험 결과가 아니다. Dan Luu 차트는 별도 HTML로 저장했으며 본문 파일만으로 모든 '
    '임베드가 오프라인 표시되는 것은 아니다.', '',
    '## 프로젝트 정책·실행 기록', '',
    '웹 프로젝트 다섯 곳의 파일별 고정 커밋·원문 URL·로컬 위치는 [전용 원문 색인](projects-web/README.md)에 있다. '
    'PR/MR의 상세 응답과 후보는 [45건 manifest](../data/web-projects/manifest.json)에서 찾을 수 있다.', '',
    '| 에이전트 프로젝트 문서 | 고정 원문 또는 공개 기록 | 로컬 전체 |', '|---|---|---|']
for d in PROJECT['documents']:
    lines.append(f'| {d["repo"]}: {d.get("path", d["file"])} | [원출처]({d.get("url", d.get("source", ""))}) | [파일](projects-agent/{d["file"]}) |')
lines += ['', 'Superpowers AGENTS 파일은 `CLAUDE.md`를 가리키는 symlink의 blob 내용이다. '
    '해당 CLAUDE 원문을 별도로 저장했다. PR 본문은 수정될 수 있는 조회일 snapshot이며 CI 로그와 같지 않다. '
    '[27건 판정 데이터](../data/agent-projects/pr-evidence.json), '
    '[프로젝트 원문 버전·해시](projects-agent/source-manifest.json).', '',
    '기존 조사에서 보관한 [Superpowers 인증 개선 계획 전체](../../exemplary-design-and-plans/originals/P3-superpowers-auth-hardening-plan.md)와 '
    '[설계 전체](../../exemplary-design-and-plans/originals/P3-superpowers-auth-hardening-design.md)도 참조했다. '
    '파일을 중복 복사하지 않았으며 [기존 manifest](../../exemplary-design-and-plans/originals/manifest.json)에 고정 커밋 URL이 있다.', '',
    '## 보충 데이터와 코드', '', '| 원출처 | 보관 파일 |', '|---|---|']
for f in AGENT['supplements']:
    rel = f['local_file'].split('tdd-vs-test-after/originals/', 1)[-1]
    lines.append(f'| [출처]({f["url"]}) | [{Path(rel).name}]({rel}) |')
lines += ['', 'TDDev ZIP은 다운로드하고 내부 코드·문서를 정적으로 확인했다. 실행하지 않았다. '
    '관련 텍스트·코드 추출본은 `studies-agent/tddev-*`에 있다. Agent-generated tests의 '
    '약 235MB Zenodo ZIP은 메타데이터만 확인하고 다운로드하지 않았다. 익명 저장소 접근 실패와 '
    '공개 코드 미제공 여부는 논문 카드에 기록했다.', '',
    '## 커뮤니티 원문과 Aside 열람 기록', '',
    '| 스레드 | HTML 원문 | 실제 브라우저 snapshot |', '|---|---|---|',
    '| [HN: Dan Luu 실험](https://news.ycombinator.com/item?id=49605246) | [HTML](community/C1-hn-49605246.html) | [본문·댓글](../working/aside-hn-49605246-full.txt) |',
    '| [HN: Agents that run while I sleep](https://news.ycombinator.com/item?id=47327559) | [HTML](community/C2-hn-47327559.html) | [본문·댓글](../working/aside-hn-47327559-full.txt) |',
    '| [Reddit: AgentsOfAI](https://www.reddit.com/r/AgentsOfAI/comments/1wd29ns/dan_luu_ran_160_agent_runs_per_testing/) | 별도 HTML 미보관 | [본문·댓글](../working/aside-reddit-1wd29ns-full.txt) |', '',
    'Reddit snapshot에서 로그인 계정 UI와 접속용 URL 매개변수만 제거했다. snapshot은 '
    '열람 당시 렌더링된 내용이며 전체 사이트·접힌 모든 스레드·외부 링크의 완전한 미러는 아니다. '
    '초기 Aside 에이전트 호출 실패 로그와 이후 성공한 REPL 열람을 구분해 보관했다.', '',
    '[전체보고서](../README.md) · [보관 파일 검증](../data/artifact-check.json)', '']
(ORIGINALS / 'README.md').write_text('\n'.join(lines))

# Include the final generated index itself; avoid a self-referential manifest digest.
idx = ORIGINALS / 'README.md'
rows = [r for r in rows if r['path'] != 'originals/README.md']
raw = idx.read_bytes()
rows.append({'path': 'originals/README.md', 'representation': 'research-created source index',
             'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(), 'provenance': []})
manifest = {'generated_at': datetime.now(timezone.utc).isoformat(), 'research_cutoff': '2026-09-12',
            'paths_relative_to': 'docs/research/tdd-vs-test-after',
            'scope': 'Files under originals, excluding this manifest itself. Derived text is not an original.',
            'files': sorted(rows, key=lambda r: r['path']), 'prior_manifest_validation_errors': errors}
(ORIGINALS / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
print(json.dumps({'indexed_files': len(rows), 'prior_metadata_errors': errors}, ensure_ascii=False))
if errors:
    raise SystemExit(1)
