"""Read-only integrity checks for this research artifact, not upstream tests."""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote
import hashlib
import json
import re
from pypdf import PdfReader

BASE = Path(__file__).resolve().parents[1]
errors = []
manifest = json.loads((BASE / 'originals/manifest.json').read_text())
for r in manifest['files']:
    p = BASE / r['path']
    if not p.exists():
        errors.append('missing indexed file: '+r['path'])
        continue
    raw = p.read_bytes()
    if len(raw) != r['bytes'] or hashlib.sha256(raw).hexdigest() != r['sha256']:
        errors.append('manifest mismatch: '+r['path'])

pdfs = []
for p in sorted((BASE/'originals').rglob('*.pdf')):
    try:
        doc = PdfReader(p)
        chars = sum(len(page.extract_text() or '') for page in doc.pages)
        pdfs.append({'path': str(p.relative_to(BASE)), 'pages': len(doc.pages), 'text_characters': chars})
        if not chars:
            errors.append('no extracted text: '+str(p))
    except Exception as exc:
        errors.append('PDF parse failure: '+str(p)+': '+str(exc))

json_count = 0
for p in BASE.rglob('*.json'):
    try:
        json.loads(p.read_text())
        json_count += 1
    except Exception as exc:
        errors.append('JSON invalid: '+str(p)+': '+str(exc))
jsonl_rows = 0
for p in BASE.rglob('*.jsonl'):
    try:
        for row in p.read_text().splitlines():
            if row.strip():
                json.loads(row)
                jsonl_rows += 1
    except Exception as exc:
        errors.append('JSONL invalid: '+str(p)+': '+str(exc))

authored = list(BASE.glob('*.md')) + [BASE/'working'/x for x in (
    'agent-studies.md','agent-projects.md','web-projects.md','critical-review.md')]
authored += [BASE/'originals/README.md', BASE/'originals/projects-web/README.md']
local_links = 0
for p in authored:
    if not p.exists():
        errors.append('missing authored report: '+str(p))
        continue
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', p.read_text()):
        if target.startswith(('https://','http://','#','mailto:')):
            continue
        target = unquote(target.split('#')[0].strip('<>'))
        if not target:
            continue
        q = Path(target) if target.startswith('/') else p.parent/target
        local_links += 1
        if not q.exists():
            errors.append(f'broken link: {p.relative_to(BASE)} -> {target}')

web = json.loads((BASE/'data/web-projects/manifest.json').read_text())
agent = json.loads((BASE/'data/agent-projects/pr-evidence.json').read_text())
samples = []
for row in web['samples']:
    samples.append({'project':row['project'], 'type':row['class'], 'merged_at':row['merged_at']})
for proj in agent['projects']:
    for row in proj['pull_requests']:
        samples.append({'project':proj['repo'], 'type':row['category'], 'merged_at':row['merged_at']})
counts = Counter(r['project'] for r in samples)
for project, n in counts.items():
    if n != 9:
        errors.append(f'wrong sample count: {project} {n}')
    types = Counter(r['type'] for r in samples if r['project']==project)
    if sorted(types.values()) != [3,3,3]:
        errors.append(f'wrong category count: {project} {dict(types)}')
for row in samples:
    if not '2024-09-12' <= row['merged_at'][:10] <= '2026-09-12':
        errors.append('sample outside date window: '+str(row))

# These are screenshot-derived task files, not public authors' addresses in Git JSON.
browser_files = list((BASE/'working').glob('aside-*-full.txt'))
for p in browser_files:
    txt = p.read_text()
    if '?solution=' in txt:
        errors.append('browser access parameter not removed: '+p.name)

out = {'checked_at': datetime.now(timezone.utc).isoformat(),
       'scope': 'File integrity, PDF parsing/text extraction, JSON syntax, authored local links, sample counts/dates. Not an upstream test run or benchmark reproduction.',
       'manifest_files_verified':len(manifest['files']), 'pdfs':pdfs,
       'json_files_parsed':json_count, 'jsonl_rows_parsed':jsonl_rows,
       'authored_markdown_files':len(authored), 'local_links_checked':local_links,
       'sample_total':len(samples), 'sample_counts':dict(counts),
       'errors':errors, 'result':'pass' if not errors else 'needs correction'}
(BASE/'data/artifact-check.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='pdfs'},ensure_ascii=False,indent=2))
if errors:
    raise SystemExit(1)
