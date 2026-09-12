"""Archive public research sources; never execute their contents."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib, json, subprocess, datetime

BASE = Path(__file__).resolve().parents[1]
REF = '2315484de6f1408844f1cd977bbb3152b3c44fa3'
RAW = f'https://raw.githubusercontent.com/bdfinst/agentic-dev-team/{REF}/'
records = [
 ('H1', 'Nagappan et al., Realizing quality improvement through TDD', '2008', 'https://www.microsoft.com/en-us/research/wp-content/uploads/2009/10/Realizing-Quality-Improvement-Through-Test-Driven-Development-Results-and-Experiences-of-Four-Industrial-Teams-nagappan_tdd.pdf', 'originals/studies-human/H1-nagappan-2008.pdf'),
 ('H2', 'Rafique and Misic, The Effects of TDD: A Meta-Analysis (author manuscript mirror)', '2013; mirror cover 2018', 'https://raidoninc.com/assets/research/tddMetaAnalysis.pdf', 'originals/studies-human/H2-rafique-misic-manuscript.pdf'),
 ('H3', 'Fucci et al., A Dissection of the TDD Process', '2016 preprint; 2017 journal', 'https://arxiv.org/pdf/1611.05994v1', 'originals/studies-human/H3-fucci-1611.05994v1.pdf'),
 ('H4', 'Santos et al., A Family of Experiments on TDD', '2020', 'https://arxiv.org/pdf/2011.11942v1', 'originals/studies-human/H4-santos-2011.11942v1.pdf'),
 ('H5', 'Ghafari et al., Why Research on TDD is Inconclusive?', '2020', 'https://arxiv.org/pdf/2007.09863v1', 'originals/studies-human/H5-inconclusive-2007.09863v1.pdf'),
 ('B1', 'Martin Fowler, Kent Beck, DHH: Is TDD Dead?', '2014', 'https://martinfowler.com/articles/is-tdd-dead/', 'originals/practitioner/B1-is-tdd-dead.html'),
 ('B2', 'Dan Luu, How well do agents use test/verification techniques?', '2026-09-07', 'https://danluu.com/agentic-testing/', 'originals/practitioner/B2-danluu-agentic-testing.html'),
 ('B2-index', 'Dan Luu post index (publication date evidence)', 'retrieved 2026-09-12', 'https://danluu.com/post/', 'originals/practitioner/B2-danluu-post-index.html'),
 ('B3', 'Bryan Finster, Agentic workflow experiment 05 final results', 'fixed Git revision', RAW+'docs/experiments/05-final-results.md', 'originals/practitioner/B3-finster-05-final-results.md'),
 ('B3-faq', 'Bryan Finster, Experiment FAQ', 'fixed Git revision', RAW+'docs/experiments/FAQ.md', 'originals/practitioner/B3-finster-FAQ.md'),
 ('B3-data', 'Bryan Finster, Raw workflow matrix rows', 'fixed Git revision', RAW+'docs/experiments/agentic-workflow-evidence/data/refactor-workflow-matrix.jsonl', 'originals/practitioner/B3-refactor-workflow-matrix.jsonl'),
 ('B3-harness', 'Bryan Finster, Experiment harness (archived, not executed)', 'fixed Git revision', RAW+'scripts/run_refactor_experiment.py', 'originals/practitioner/B3-run_refactor_experiment.py'),
 ('B3-matrix', 'Bryan Finster, Workflow matrix harness (archived, not executed)', 'fixed Git revision', RAW+'scripts/run_workflow_matrix.py', 'originals/practitioner/B3-run_workflow_matrix.py'),
 ('C1', 'Hacker News discussion of Dan Luu agentic testing', '2026-09', 'https://news.ycombinator.com/item?id=49605246', 'originals/community/C1-hn-49605246.html'),
]

def download(row):
    sid,title,date,url,local=row
    dest=BASE/local; dest.parent.mkdir(parents=True,exist_ok=True)
    proc=subprocess.run(['curl','-fLsS','--retry','1','--max-time','50',url,'-o',str(dest)],capture_output=True,text=True)
    result=dict(id=sid,title=title,date=date,url=url,local_path=local,retrieved_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
    if proc.returncode:
        result.update(status='failed',error=proc.stderr)
    else:
        data=dest.read_bytes()
        result.update(status='saved',bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
        if dest.suffix=='.pdf' and not data.startswith(b'%PDF-'):
            result.update(status='invalid_pdf')
        if url.startswith(RAW): result['git_ref']=REF
    return result

if __name__=='__main__':
    with ThreadPoolExecutor(max_workers=4) as pool: results=list(pool.map(download,records))
    (BASE/'data/root-sources.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    for r in results: print(r['id'],r['status'],r.get('bytes'),r.get('error',''))
