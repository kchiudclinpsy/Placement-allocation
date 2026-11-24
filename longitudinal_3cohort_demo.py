#!/usr/bin/env python3
"""Synthetic longitudinal demonstration: 3 cohorts x 50 trainees x 6 rotations."""
from pathlib import Path
import csv, json, random
import numpy as np
from scipy.optimize import linear_sum_assignment
random.seed(20261124)
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'longitudinal_demo_outputs'; OUT.mkdir(exist_ok=True)
streams=[
 ('CAMHS','Child and family',25),('ADULT','Adult mental health',25),('LD','Learning disabilities',25),
 ('NEURO','Neuropsychology',25),('HEALTH','Health psychology',25),('OLDER','Older people',25)]
periods=[f'Y{y}R{r}' for y in range(1,4) for r in (1,2)]
trainees=[]
for c in range(1,4):
 for n in range(1,51):
  sid=f'C{c}-T{n:02d}'
  # Stable individual preference order plus modest developmental change per period.
  base=[x[0] for x in streams]; random.shuffle(base)
  trainees.append({'cohort':f'Cohort {c}','student_id':sid,'special_adjustment':'Yes' if n in {7,23,41} else 'No','base':base})

history={t['student_id']:[] for t in trainees}; rows=[]
for pi,period in enumerate(periods):
 slots=[code for code,_,cap in streams for _ in range(cap)]
 score=np.full((len(trainees),len(slots)),-1e6)
 details={}
 for i,t in enumerate(trainees):
  # Rotate preference order over time but preserve individual priorities.
  prefs=t['base'][pi%6:]+t['base'][:pi%6]
  for j,code in enumerate(slots):
   if code in history[t['student_id']]: continue # no repeated stream
   rank=prefs.index(code)+1
   pref=max(0,110-rank*15)
   breadth=15 if code not in history[t['student_id']] else 0
   # foundational weighting in year 1, advanced weighting in year 3
   stage=8 if (pi<2 and code in {'CAMHS','ADULT','LD'}) or (pi>=4 and code in {'NEURO','HEALTH','OLDER'}) else 0
   adjustment=5 if t['special_adjustment']=='Yes' and rank<=2 else 0
   provider=((int(t['student_id'][-2:])*7 + pi*11 + j)%17)
   total=.60*pref+.15*breadth+.10*stage+.10*provider+.05*adjustment
   score[i,j]=total; details[(i,j)]=(rank,pref,breadth,stage,provider,adjustment,total)
 ri,cj=linear_sum_assignment(-score)
 for i,j in zip(ri,cj):
  t=trainees[i]; code=slots[j]; rank,pref,breadth,stage,provider,adjustment,total=details[(i,j)]
  history[t['student_id']].append(code)
  name=next(x[1] for x in streams if x[0]==code)
  rows.append({'cohort':t['cohort'],'student_id':t['student_id'],'period':period,'year':pi//2+1,'rotation':pi%2+1,'placement_code':code,'placement_stream':name,'preference_rank':rank,'preference_score':pref,'breadth_score':breadth,'stage_score':stage,'provider_score':provider,'adjustment_score':adjustment,'total_score':round(total,2)})

with (OUT/'longitudinal_allocations.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
# trainee journey matrix
journeys=[]
for t in trainees:
 rr=[r for r in rows if r['student_id']==t['student_id']]
 journeys.append({'cohort':t['cohort'],'student_id':t['student_id'],**{r['period']:r['placement_code'] for r in rr},'unique_streams':len(set(r['placement_code'] for r in rr)),'top_two_count':sum(r['preference_rank']<=2 for r in rr)})
with (OUT/'trainee_journeys.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=journeys[0].keys());w.writeheader();w.writerows(journeys)
summary={'trainees':len(trainees),'allocation_episodes':len(rows),'periods':6,'cohorts':3,'placements_per_trainee':6,'first_choice':sum(r['preference_rank']==1 for r in rows),'top_two':sum(r['preference_rank']<=2 for r in rows),'unique_six':sum(j['unique_streams']==6 for j in journeys),'mean_score':round(sum(r['total_score'] for r in rows)/len(rows),2),'breaches':0}
(OUT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
# period x stream counts
with (OUT/'capacity_by_period.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['period']+[s[0] for s in streams])
 for p in periods:w.writerow([p]+[sum(r['period']==p and r['placement_code']==s[0] for r in rows) for s in streams])
print(json.dumps(summary))
