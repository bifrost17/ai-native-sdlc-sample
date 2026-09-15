"""Recalculate archived public results. Does not run an agent or benchmark."""
from pathlib import Path
import json, statistics, collections

BASE=Path(__file__).resolve().parents[1]
source=BASE/'originals/practitioner/B3-refactor-workflow-matrix.jsonl'
rows=[json.loads(line) for line in source.read_text().splitlines() if line.strip()]
groups=collections.defaultdict(list)
for row in rows: groups[row['arm']].append(row)
out=[]
for arm, rs in sorted(groups.items()):
    cells=collections.defaultdict(list)
    for row in rs: cells[(row['task'],row['trial'])].append(row)
    costs=[sum(row['cost']['cost_usd'] for row in cr) for cr in cells.values()]
    blast=[row['blast_radius']['churned'] for row in rs if isinstance(row.get('blast_radius'),dict) and isinstance(row['blast_radius'].get('churned'),(int,float))]
    mutation=[row['mutation']['score'] for row in rs if isinstance(row.get('mutation',{}).get('score'),(int,float))]
    build=[row for row in rs if row['stage']=='build']
    changes=[row for row in rs if row['stage']!='build']
    result=dict(arm=arm,rows=len(rs),cells=len(cells),mean_cost_per_cell=statistics.mean(costs),mean_mutation=statistics.mean(mutation),mean_blast=statistics.mean(blast) if blast else None,violations=sum(bool(row.get('invariant_violation')) for row in rs),build_acceptance_pass=sum(row.get('core_passed') is True and row.get('edge_passed') is True for row in build),change_acceptance_pass=sum(row.get('passed') is True for row in changes),build_rows=len(build),change_rows=len(changes))
    out.append(result)
result={'source':'../originals/practitioner/B3-refactor-workflow-matrix.jsonl','rows':len(rows),'arms':out,'scope':'Recalculation of public raw results; original agent experiment not rerun.'}
(BASE/'data/finster-recalculation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
