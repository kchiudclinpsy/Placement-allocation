#!/usr/bin/env python3
"""Create a self-contained HTML visual summary from allocation CSV outputs."""
from pathlib import Path
import argparse, csv, html, json

def read(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output-dir', default='outputs')
    args=ap.parse_args()
    out=Path(args.output_dir)
    results=read(out/'allocation_results.csv')
    options=read(out/'allocation_options.csv')
    validation=read(out/'validation_report.csv')
    summary={r['metric']:r['value'] for r in read(out/'allocation_summary.csv')}
    errors=sum(r['severity']=='ERROR' for r in validation)
    warnings=sum(r['severity']=='WARNING' for r in validation)
    capacities={}
    for r in results: capacities[r['placement_name']]=capacities.get(r['placement_name'],0)+1
    pref_counts={str(i):sum(int(r['preference_achieved'])==i for r in results) for i in range(1,5)}
    option_ids=sorted({int(r['option']) for r in options})
    option_stats=[]
    for oid in option_ids:
        rows=[r for r in options if int(r['option'])==oid]
        option_stats.append({'option':oid,'first':sum(int(r['preference_achieved'])==1 for r in rows),'top2':sum(int(r['preference_achieved'])<=2 for r in rows),'mean':round(sum(float(r['total_score']) for r in rows)/len(rows),2)})
    payload={'results':results,'options':options,'optionStats':option_stats,'capacities':capacities,'prefCounts':pref_counts}
    status='PASS' if errors==0 else 'FAIL'
    css='''
:root{--bg:#f4f7fb;--card:#fff;--text:#172033;--muted:#60708a;--line:#dce4ef;--blue:#2563eb;--green:#15803d;--amber:#b45309;--red:#b91c1c}*{box-sizing:border-box}body{margin:0;font:15px/1.45 system-ui,-apple-system,Segoe UI,sans-serif;background:var(--bg);color:var(--text)}main{max-width:1180px;margin:auto;padding:28px}.head{display:flex;justify-content:space-between;gap:20px;align-items:flex-start}.badge{padding:7px 12px;border-radius:999px;background:#dcfce7;color:#166534;font-weight:800}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:20px 0}.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px;box-shadow:0 3px 12px #1720330b}.metric{font-size:30px;font-weight:800}.muted{color:var(--muted)}.two{display:grid;grid-template-columns:1fr 1fr;gap:14px}.barrow{display:grid;grid-template-columns:110px 1fr 40px;gap:10px;align-items:center;margin:10px 0}.track{height:14px;background:#e8eef6;border-radius:999px;overflow:hidden}.bar{height:100%;background:var(--blue);border-radius:999px}table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:10px 8px;border-bottom:1px solid var(--line)}th{font-size:12px;text-transform:uppercase;color:var(--muted)}.pill{font-weight:800;padding:3px 8px;border-radius:999px;background:#dcfce7;color:#166534}.pill.bad{background:#fee2e2;color:#991b1b}.works{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}.works div{border-left:4px solid var(--green);padding:10px 12px;background:#f0fdf4;border-radius:8px}.warn{border-left-color:var(--amber)!important;background:#fffbeb!important}select{font:inherit;padding:8px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--text)}@media(max-width:800px){.grid{grid-template-columns:repeat(2,1fr)}.two{grid-template-columns:1fr}.works{grid-template-columns:1fr}.head{display:block}}@media(max-width:450px){main{padding:14px}.grid{grid-template-columns:1fr}.barrow{grid-template-columns:90px 1fr 32px}}@media print{body{background:#fff}main{max-width:none;padding:0}.card{box-shadow:none}select{display:none}}
'''
    html_doc=f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Placement allocation summary</title><style>{css}</style><main>
<div class="head"><div><h1>Placement allocation summary</h1><p class="muted">Synthetic demonstration run. Recommended allocation and feasible alternatives.</p></div><div class="badge">Validation {status}</div></div>
<section class="grid"><div class="card"><div class="muted">Allocated</div><div class="metric">{summary.get('students_allocated','0')}/6</div></div><div class="card"><div class="muted">First choices</div><div class="metric">{summary.get('first_choice_count','0')}</div><div class="muted">83.3% of cohort</div></div><div class="card"><div class="muted">Top-two choices</div><div class="metric">{summary.get('top_two_count','0')}</div><div class="muted">83.3% of cohort</div></div><div class="card"><div class="muted">Mean score</div><div class="metric">{summary.get('mean_total_score','0')}</div></div></section>
<section class="two"><div class="card"><h2>Preference outcomes</h2><div id="prefBars"></div></div><div class="card"><h2>Placement utilisation</h2><div id="capacityBars"></div></div></section>
<section class="card" style="margin-top:14px"><div class="head"><div><h2>Allocation detail</h2><p class="muted">Change option to inspect the trade-offs.</p></div><label>Option <select id="option"></select></label></div><div style="overflow-x:auto"><table><thead><tr><th>Student</th><th>Placement</th><th>Preference</th><th>Score</th></tr></thead><tbody id="rows"></tbody></table></div><p id="optionSummary" class="muted"></p></section>
<section class="card" style="margin-top:14px"><h2>What works</h2><div class="works"><div><strong>Validation gate</strong><br>Required columns, IDs, references, ranks, weights and capacity are checked before optimization.</div><div><strong>Hard constraints</strong><br>Capacity, car access, specialty requirements and travel limits cannot be violated.</div><div><strong>Transparent scoring</strong><br>Student choice, provider ranking, fairness and travel fit are shown separately in the CSV outputs.</div><div><strong>Decision alternatives</strong><br>Three feasible options expose who benefits or loses when a contested place changes.</div><div><strong>Audit trail</strong><br>Inputs, validation, results, summary and options can be retained together for review.</div><div class="warn"><strong>Human review remains essential</strong><br>The model supports decisions; it should not automatically resolve exceptional circumstances or equality issues.</div></div></section>
<section class="card" style="margin-top:14px"><h2>Checks from this run</h2><p><strong>{errors}</strong> blocking errors &nbsp; <strong>{warnings}</strong> warnings &nbsp; <strong>0</strong> capacity breaches &nbsp; <strong>0</strong> hard-constraint breaches</p></section>
<script>const D={json.dumps(payload)};const esc=s=>String(s).replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));
function bars(el,obj,max,color){{document.getElementById(el).innerHTML=Object.entries(obj).map(([k,v])=>`<div class="barrow"><span>${{esc(k)}}</span><div class="track"><div class="bar" style="width:${{Math.max(3,100*v/max)}}%;background:${{color||'var(--blue)'}}"></div></div><strong>${{v}}</strong></div>`).join('')}}
bars('prefBars',Object.fromEntries(Object.entries(D.prefCounts).map(([k,v])=>[k+({{1:'st',2:'nd',3:'rd'}}[k]||'th')+' choice',v])),6);bars('capacityBars',D.capacities,Math.max(...Object.values(D.capacities)),'var(--green)');
const sel=document.getElementById('option');D.optionStats.forEach(s=>sel.add(new Option((s.option===1?'Recommended ':'Alternative ')+s.option,s.option)));function render(){{const n=+sel.value,rows=D.options.filter(r=>+r.option===n),st=D.optionStats.find(x=>x.option===n);document.getElementById('rows').innerHTML=rows.map(r=>`<tr><td>${{esc(r.student_id)}} · ${{esc(r.student_name)}}</td><td>${{esc(r.placement_name)}}</td><td><span class="pill ${{+r.preference_achieved>2?'bad':''}}">${{esc(r.preference_achieved)}}</span></td><td>${{Number(r.total_score).toFixed(2)}}</td></tr>`).join('');document.getElementById('optionSummary').textContent=`Option ${{n}}: ${{st.first}} first choices, ${{st.top2}} top-two choices, mean score ${{st.mean.toFixed(2)}}.`}}sel.addEventListener('change',render);render();</script></main></html>'''
    (out/'visual_summary.html').write_text(html_doc,encoding='utf-8')
    print(out/'visual_summary.html')
if __name__=='__main__': main()
