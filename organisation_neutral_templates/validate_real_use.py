#!/usr/bin/env python3
from pathlib import Path
import csv, datetime, sys
ROOT=Path(__file__).resolve().parent
errors=[]; warnings=[]
def load(name, cols):
 p=ROOT/name
 with p.open(encoding='utf-8-sig',newline='') as f:
  r=csv.DictReader(f); missing=[c for c in cols if c not in (r.fieldnames or [])]
  if missing: errors.append(f'{name}: missing columns {missing}')
  return list(r)
def yn(v,label):
 if v not in {'Yes','No'}: errors.append(f'{label}: must be Yes or No')
t=load('trainees.csv',['trainee_id','cohort_id','training_year','next_placement_number','base_code','driving_access','allocation_status'])
o=load('placement_offers.csv',['offer_id','placement_id','rotation_id','capacity','placement_stage','approved','quality_status','supervisor_approved','supervisor_training_valid_to','weekly_supervision_minutes','weekly_contact_minutes','cover_arrangement_confirmed'])
c=load('placement_capabilities.csv',['placement_id','capability_type','capability_code','opportunity_strength'])
h=load('placement_history.csv',['trainee_id','placement_number','placement_id','rotation_id','outcome','attendance_days','competency_evidence_signed_off'])
cs=load('competency_status.csv',['trainee_id','competency_code','status','evidence_date','source_placement_number'])
sp=load('specialist_preferences.csv',['trainee_id','rotation_id','placement_id','rank','advisor_reviewed'])
r=load('review_flags.csv',['trainee_id','flag_code','valid_from','valid_to','review_status'])
p=load('allocation_policy.csv',['policy_version','rule_id','stage','rule_type','criterion','weight','enabled'])
def unique(rows,key,name):
 vals=[x[key] for x in rows if x[key]]
 if len(vals)!=len(set(vals)): errors.append(f'{name}: duplicate {key}')
unique(t,'trainee_id','trainees.csv'); unique(o,'offer_id','placement_offers.csv')
tids={x['trainee_id'] for x in t}; pids={x['placement_id'] for x in o}
for x in t:
 if x['training_year'] not in {'1','2','3'}: errors.append(f"{x['trainee_id']}: training_year must be 1..3")
 if x['next_placement_number'] not in {'1','2','3','4','5','6'}: errors.append(f"{x['trainee_id']}: next_placement_number must be 1..6")
 if x['driving_access'] not in {'Yes','No','Adjustment'}: errors.append(f"{x['trainee_id']}: invalid driving_access")
for x in o:
 tag=x['offer_id']; yn(x['approved'],tag); yn(x['supervisor_approved'],tag); yn(x['cover_arrangement_confirmed'],tag)
 try:
  if int(x['capacity'])<1: raise ValueError
  if int(x['weekly_supervision_minutes'])<60: errors.append(f'{tag}: weekly supervision below 60 minutes')
  if int(x['weekly_contact_minutes'])<180: warnings.append(f'{tag}: weekly contact below 180 minutes')
 except ValueError: errors.append(f'{tag}: invalid numeric capacity/supervision/contact')
 if x['quality_status']=='Suspended': errors.append(f'{tag}: suspended placement cannot be offered')
 if x['approved']!='Yes' or x['supervisor_approved']!='Yes': errors.append(f'{tag}: approval incomplete')
 if x['cover_arrangement_confirmed']!='Yes': errors.append(f'{tag}: supervision cover not confirmed')
for name,rows in [('history',h),('competency',cs),('specialist_preferences',sp),('review_flags',r)]:
 for x in rows:
  if x.get('trainee_id') and x['trainee_id'] not in tids: errors.append(f"{name}: unknown trainee {x['trainee_id']}")
for x in sp:
 if x['placement_id'] not in pids: errors.append(f"specialist_preferences: unknown placement {x['placement_id']}")
 if x['advisor_reviewed']!='Yes': warnings.append(f"specialist preference not advisor-reviewed for {x['trainee_id']}")
weights=sum(float(x['weight'] or 0) for x in p if x['rule_type']=='Soft' and x['enabled']=='Yes')
if abs(weights-100)>0.001: errors.append(f'enabled soft weights total {weights}, not 100')
report=[['severity','message']]+[['ERROR',x] for x in errors]+[['WARNING',x] for x in warnings]
if not errors and not warnings: report.append(['INFO','Validation passed'])
with (ROOT/'readiness_report.csv').open('w',newline='',encoding='utf-8') as f: csv.writer(f).writerows(report)
print(f'Errors: {len(errors)}; warnings: {len(warnings)}')
sys.exit(2 if errors else 0)
