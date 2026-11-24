#!/usr/bin/env python3
"""Validate placement-allocation CSVs and produce ranked allocation options."""
from pathlib import Path
import argparse, csv, math, sys
from collections import Counter, defaultdict
try:
    import numpy as np
    from scipy.optimize import linear_sum_assignment
except ImportError:
    sys.exit("Missing dependency. Run: python -m pip install -r requirements.txt")

YN={"Yes","No"}; PREF_COLS=["pref1","pref2","pref3","pref4"]

def read_csv(path, required):
    with path.open(encoding="utf-8-sig", newline="") as f:
        r=csv.DictReader(f); headers=r.fieldnames or []
        missing=[x for x in required if x not in headers]
        if missing: raise ValueError(f"{path.name}: missing columns: {', '.join(missing)}")
        return [{k:(v or '').strip() for k,v in row.items()} for row in r]

def positive_int(value,label,errors,allow_zero=False):
    try:
        x=int(value)
        if x < (0 if allow_zero else 1): raise ValueError
        return x
    except ValueError:
        errors.append(f"{label} must be an integer {'>= 0' if allow_zero else '> 0'}")
        return 0

def validate(folder):
    errors=[]; warnings=[]
    students=read_csv(folder/'students.csv',['student_id','student_name',*PREF_COLS,'max_travel_minutes','car_owner','required_specialty','special_circumstances'])
    placements=read_csv(folder/'placements.csv',['placement_id','placement_name','specialty','capacity','postcode','requires_car','minimum_travel_minutes'])
    pp=read_csv(folder/'placement_preferences.csv',['placement_id','student_id','placement_rank'])
    rules=read_csv(folder/'allocation_rules.csv',['criterion','weight'])
    def duplicates(rows,key,label):
        for v,n in Counter(r[key] for r in rows if r[key]).items():
            if n>1: errors.append(f"Duplicate {label}: {v}")
    duplicates(students,'student_id','student_id'); duplicates(placements,'placement_id','placement_id')
    sids={r['student_id'] for r in students}; pids={r['placement_id'] for r in placements}; specialties={r['specialty'] for r in placements}
    for i,s in enumerate(students,2):
        tag=f"students.csv row {i} ({s['student_id'] or 'blank ID'})"
        if not s['student_id'] or not s['student_name']: errors.append(f"{tag}: student_id and student_name are required")
        prefs=[s[c] for c in PREF_COLS]
        if any(not x for x in prefs): errors.append(f"{tag}: all four preferences are required")
        if len(set(prefs))!=len(prefs): errors.append(f"{tag}: preferences must not repeat")
        for x in prefs:
            if x and x not in pids: errors.append(f"{tag}: unknown placement preference {x}")
        positive_int(s['max_travel_minutes'],f"{tag}: max_travel_minutes",errors)
        if s['car_owner'] not in YN: errors.append(f"{tag}: car_owner must be Yes or No")
        if s['required_specialty'] and s['required_specialty'] not in specialties: errors.append(f"{tag}: unknown required_specialty {s['required_specialty']}")
        if len(s['special_circumstances'])>500: errors.append(f"{tag}: special_circumstances exceeds 500 characters")
    capacities={}
    for i,p in enumerate(placements,2):
        tag=f"placements.csv row {i} ({p['placement_id'] or 'blank ID'})"
        if not all(p[x] for x in ['placement_id','placement_name','specialty','postcode']): errors.append(f"{tag}: ID, name, specialty and postcode are required")
        capacities[p['placement_id']]=positive_int(p['capacity'],f"{tag}: capacity",errors)
        positive_int(p['minimum_travel_minutes'],f"{tag}: minimum_travel_minutes",errors,allow_zero=True)
        if p['requires_car'] not in YN: errors.append(f"{tag}: requires_car must be Yes or No")
    seen_pairs=set(); ranks=defaultdict(set)
    for i,r in enumerate(pp,2):
        tag=f"placement_preferences.csv row {i}"
        if r['placement_id'] not in pids: errors.append(f"{tag}: unknown placement_id {r['placement_id']}")
        if r['student_id'] not in sids: errors.append(f"{tag}: unknown student_id {r['student_id']}")
        pair=(r['placement_id'],r['student_id'])
        if pair in seen_pairs: errors.append(f"{tag}: duplicate placement/student pair")
        seen_pairs.add(pair)
        rank=positive_int(r['placement_rank'],f"{tag}: placement_rank",errors)
        if rank in ranks[r['placement_id']]: errors.append(f"{tag}: duplicate rank {rank} within {r['placement_id']}")
        ranks[r['placement_id']].add(rank)
    expected={'student_preference','placement_preference','fairness_adjustment','travel_fit'}
    found={r['criterion'] for r in rules}
    if found!=expected: errors.append(f"allocation_rules.csv criteria must be exactly: {', '.join(sorted(expected))}")
    weights={}
    for i,r in enumerate(rules,2):
        try: w=float(r['weight'])
        except ValueError: errors.append(f"allocation_rules.csv row {i}: weight must be numeric"); w=0
        if not 0<=w<=100: errors.append(f"allocation_rules.csv row {i}: weight must be 0..100")
        weights[r['criterion']]=w
    if not math.isclose(sum(weights.values()),100,abs_tol=1e-9): errors.append("allocation rule weights must total 100")
    if sum(capacities.values())<len(students): errors.append(f"Total capacity {sum(capacities.values())} is below student count {len(students)}")
    return students,placements,pp,weights,errors,warnings

def solve(students,placements,pp,weights,banned=None):
    banned=banned or set(); pmap={p['placement_id']:p for p in placements}
    pref_rank={(r['placement_id'],r['student_id']):int(r['placement_rank']) for r in pp}
    max_rank=max(pref_rank.values(),default=1)
    slots=[p['placement_id'] for p in placements for _ in range(int(p['capacity']))]
    n=len(students); dummy=max(0,n-len(slots)); slots += [f"UNALLOCATED_{i+1}" for i in range(dummy)]
    score=np.full((n,len(slots)),-1e9,dtype=float); detail={}
    for i,s in enumerate(students):
        for j,pid in enumerate(slots):
            if pid.startswith('UNALLOCATED') or (s['student_id'],pid) in banned: continue
            p=pmap[pid]
            if p['requires_car']=='Yes' and s['car_owner']!='Yes': continue
            if s['required_specialty'] and s['required_specialty']!=p['specialty']: continue
            travel=int(p['minimum_travel_minutes']); limit=int(s['max_travel_minutes'])
            if travel>limit: continue
            rank=s and ([s[c] for c in PREF_COLS].index(pid)+1 if pid in [s[c] for c in PREF_COLS] else 5)
            ss={1:100,2:75,3:50,4:25}.get(rank,0)
            pr=pref_rank.get((pid,s['student_id']))
            ps=0 if pr is None else max(0,100-(pr-1)*(100/max(1,max_rank)))
            fs=100 if s['special_circumstances'].lower() not in ('','no','none','n/a') else 50
            ts=max(0,100*(limit-travel)/max(1,limit))
            total=(weights['student_preference']*ss+weights['placement_preference']*ps+weights['fairness_adjustment']*fs+weights['travel_fit']*ts)/100
            score[i,j]=total; detail[(i,j)]=(rank,ss,ps,fs,ts,total)
    rows,cols=linear_sum_assignment(-score)
    if any(score[i,j]<-1e8 for i,j in zip(rows,cols)): return None
    result=[]
    for i,j in zip(rows,cols):
        pid=slots[j]; rank,ss,ps,fs,ts,total=detail[(i,j)]; p=pmap[pid]; s=students[i]
        result.append({'student_id':s['student_id'],'student_name':s['student_name'],'placement_id':pid,'placement_name':p['placement_name'],'specialty':p['specialty'],'preference_achieved':rank,'student_preference_score':round(ss,2),'placement_preference_score':round(ps,2),'fairness_score':round(fs,2),'travel_fit_score':round(ts,2),'total_score':round(total,2)})
    return sorted(result,key=lambda x:x['student_id'])

def write_csv(path,rows):
    if not rows:return
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--input-dir',default='.'); ap.add_argument('--output-dir',default='outputs'); ap.add_argument('--options',type=int,default=3); args=ap.parse_args()
    folder=Path(args.input_dir); out=Path(args.output_dir); out.mkdir(parents=True,exist_ok=True)
    try: students,placements,pp,weights,errors,warnings=validate(folder)
    except (OSError,ValueError) as e: errors=[str(e)]; warnings=[]; students=placements=pp=[]; weights={}
    report=[{'severity':'ERROR','record_type':'Input','record_id':'','message':x} for x in errors]+[{'severity':'WARNING','record_type':'Input','record_id':'','message':x} for x in warnings]
    if not report: report=[{'severity':'INFO','record_type':'System','record_id':'Allocation','message':'Validation completed successfully'}]
    write_csv(out/'validation_report.csv',report)
    if errors: print(f"Validation failed with {len(errors)} error(s). See validation_report.csv"); return 2
    options=[]; banned=set()
    for option_no in range(1,max(1,args.options)+1):
        solved=solve(students,placements,pp,weights,banned)
        if not solved: break
        for row in solved: options.append({'option':option_no,**row})
        # Diversify next option by banning the lowest-scoring selected pair.
        lowest=min(solved,key=lambda x:x['total_score']); banned.add((lowest['student_id'],lowest['placement_id']))
    write_csv(out/'allocation_options.csv',options)
    best=[{k:v for k,v in r.items() if k!='option'} for r in options if r['option']==1]
    write_csv(out/'allocation_results.csv',best)
    summary=[]
    if best:
        summary=[{'metric':'students_allocated','value':len(best)}, {'metric':'first_choice_count','value':sum(r['preference_achieved']==1 for r in best)}, {'metric':'top_two_count','value':sum(r['preference_achieved']<=2 for r in best)}, {'metric':'mean_total_score','value':round(sum(r['total_score'] for r in best)/len(best),2)}]
    write_csv(out/'allocation_summary.csv',summary)
    print(f"Created {len(set(r['option'] for r in options))} allocation option(s) in {out}")
    return 0
if __name__=='__main__': raise SystemExit(main())
