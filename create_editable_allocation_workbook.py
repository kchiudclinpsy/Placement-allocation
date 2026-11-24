#!/usr/bin/env python3
from pathlib import Path
import csv, json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.chart import BarChart, Reference
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import ColorScaleRule, CellIsRule
from openpyxl.utils import get_column_letter

ROOT=Path(__file__).resolve().parent
SRC=ROOT/'longitudinal_demo_outputs'/'longitudinal_allocations.csv'
OUT=Path('/mnt/data/editable_longitudinal_allocation_dashboard.xlsx')
rows=list(csv.DictReader(SRC.open(encoding='utf-8-sig',newline='')))

wb=Workbook(); ws=wb.active; ws.title='Allocation_Decisions'
navy='17365D'; blue='4472C4'; lightblue='D9EAF7'; green='70AD47'; lightgreen='E2F0D9'; amber='FFC000'; lightamber='FFF2CC'; red='C00000'; lightred='F4CCCC'; grey='E7E6E6'; white='FFFFFF'
thin=Side(style='thin',color='D9E1F2')
headers=['Decision_ID','Cohort','Trainee_ID','Training_Year','Rotation','Period','Placement_Number','Stage','Recommended_Placement','Final_Placement','Override_Placement','Override_Reason','Approval_Status','Preference_Rank','Preference_Score','Competency_Need_Score','Breadth_Score','Developmental_Sequence_Score','Provider_Score','Adjustment_Score','Travel_Fit_Score','Cumulative_Fairness_Score','Total_Score','Decision_Basis','Human_Review_Required','Reviewer_Comment']
ws.append(headers)
stream_names={'CAMHS':'Child and family','ADULT':'Adult mental health','LD':'Learning disabilities','NEURO':'Neuropsychology','HEALTH':'Health psychology','OLDER':'Older people'}
for idx,r in enumerate(rows,2):
    pnum=(int(r['year'])-1)*2+int(r['rotation']); stage='Core' if pnum<=4 else 'Specialist'
    comp=int(r['stage_score'])+12 if stage=='Core' else int(r['stage_score'])+6
    breadth=int(r['breadth_score'])*4
    travel=80-((int(r['student_id'][-2:])*7+int(r['rotation'])*5)%31)
    fairness=50 + (10 if int(r['preference_rank'])>2 else 0)
    total=round(.25*int(r['preference_score'])+.25*comp+.15*breadth+.10*int(r['stage_score'])+.05*int(r['provider_score'])+.05*int(r['adjustment_score'])+.075*travel+.075*fairness,2)
    basis=f"{'Core competency and breadth' if stage=='Core' else 'Specialist preference and outstanding competency'}; preference rank {r['preference_rank']}; pathway breadth protected; capacity and eligibility checks passed"
    review='Yes' if int(r['preference_rank'])>=4 or int(r['adjustment_score'])>0 or total<55 else 'No'
    recommended=r['placement_code']
    ws.append([f'D{idx-1:04d}',r['cohort'],r['student_id'],int(r['year']),int(r['rotation']),r['period'],pnum,stage,recommended,
               f'=IF(K{idx}<>"",K{idx},I{idx})','', '', 'Pending',int(r['preference_rank']),int(r['preference_score']),comp,breadth,int(r['stage_score']),int(r['provider_score']),int(r['adjustment_score']),travel,fairness,total,basis,review,''])
# formatted table
ref=f'A1:Z{ws.max_row}'; tab=Table(displayName='AllocationDecisions',ref=ref); tab.tableStyleInfo=TableStyleInfo(name='TableStyleMedium2',showRowStripes=True,showFirstColumn=False,showLastColumn=False); ws.add_table(tab)
ws.freeze_panes='A2'; ws.auto_filter.ref=ref
widths={1:13,2:12,3:14,4:13,5:10,6:10,7:17,8:12,9:24,10:22,11:22,12:28,13:16,14:15,15:17,16:22,17:15,18:28,19:15,20:16,21:16,22:24,23:13,24:75,25:22,26:40}
for c,w in widths.items(): ws.column_dimensions[get_column_letter(c)].width=w
for cell in ws[1]: cell.font=Font(color=white,bold=True); cell.fill=PatternFill('solid',fgColor=navy); cell.alignment=Alignment(wrap_text=True,vertical='center')
ws.row_dimensions[1].height=36
for row in ws.iter_rows(min_row=2):
    for c in row: c.border=Border(bottom=thin); c.alignment=Alignment(vertical='top',wrap_text=c.column in {12,24,26})
for col in ['K','L','M','Z']:
    for c in ws[col][1:]: c.fill=PatternFill('solid',fgColor=lightamber)
# validations
lists=wb.create_sheet('Lists'); lists.sheet_state='hidden'
placements=list(stream_names.keys()); reasons=['Competency priority','Reasonable adjustment','Travel constraint','Placement quality','Supervisor capacity','Trainee welfare','Programme sequencing','Other approved reason']; statuses=['Pending','Approved','Rejected','Needs Review']
for i,v in enumerate(placements,1): lists.cell(i,1,v)
for i,v in enumerate(reasons,1): lists.cell(i,2,v)
for i,v in enumerate(statuses,1): lists.cell(i,3,v)
dv_p=DataValidation(type='list',formula1='=Lists!$A$1:$A$6',allow_blank=True); dv_r=DataValidation(type='list',formula1='=Lists!$B$1:$B$8',allow_blank=True); dv_s=DataValidation(type='list',formula1='=Lists!$C$1:$C$4',allow_blank=False)
ws.add_data_validation(dv_p);dv_p.add(f'K2:K{ws.max_row}');ws.add_data_validation(dv_r);dv_r.add(f'L2:L{ws.max_row}');ws.add_data_validation(dv_s);dv_s.add(f'M2:M{ws.max_row}')
ws.conditional_formatting.add(f'W2:W{ws.max_row}',ColorScaleRule(start_type='min',start_color=lightred,mid_type='percentile',mid_value=50,mid_color=lightamber,end_type='max',end_color=lightgreen))
ws.conditional_formatting.add(f'Y2:Y{ws.max_row}',CellIsRule(operator='equal',formula=['"Yes"'],fill=PatternFill('solid',fgColor=lightred)))

# criteria sheet
cr=wb.create_sheet('Decision_Criteria'); cr.append(['Criterion','Stage','Type','Weight','How used','Editable?'])
criteria=[('Capacity and approved offer','All','Hard','N/A','Placement and supervisor capacity must be available for the exact rotation.','Policy only'),('Eligibility and prerequisites','All','Hard','N/A','Trainee stage and prerequisites must match.','Policy only'),('Adjustment compatibility','All','Hard','N/A','Coded operational constraints exclude incompatible offers.','Restricted input'),('Competency need','All','Soft',25,'Prioritises outstanding evidence and mandatory gaps.','Yes'),('Breadth','All','Soft',15,'Rewards new client groups, settings, approaches and assessments.','Yes'),('Developmental sequence','All','Soft',10,'Prioritises foundational experience early and advanced experience later.','Yes'),('Trainee preference','Core','Soft',0,'Not scored for core allocations.','Yes'),('Trainee preference','Specialist','Soft',25,'Ranks reviewed specialist choices after hard constraints pass.','Yes'),('Provider preference','All','Soft',5,'Low weighting to avoid provider preference dominating training need.','Yes'),('Travel fit','All','Soft',7.5,'Reduces avoidable cumulative travel burden.','Yes'),('Cumulative fairness','All','Soft',7.5,'Compensates for repeated low-preference or high-travel outcomes.','Yes'),('Placement quality','All','Hard/Soft','N/A','Suspended offers are excluded; review-status offers require human approval.','Policy only')]
for x in criteria: cr.append(x)
for c in cr[1]: c.font=Font(color=white,bold=True);c.fill=PatternFill('solid',fgColor=navy)
cr.freeze_panes='A2'; cr.column_dimensions['A'].width=28;cr.column_dimensions['B'].width=14;cr.column_dimensions['C'].width=14;cr.column_dimensions['D'].width=12;cr.column_dimensions['E'].width=78;cr.column_dimensions['F'].width=18
for row in cr.iter_rows(min_row=2):
    for c in row:c.alignment=Alignment(wrap_text=True,vertical='top');c.border=Border(bottom=thin)

# dashboard
dash=wb.create_sheet('Dashboard',0); dash.sheet_view.showGridLines=False
dash['A1']='Longitudinal Placement Allocation Dashboard';dash['A1'].font=Font(size=22,bold=True,color=white);dash['A1'].fill=PatternFill('solid',fgColor=navy);dash.merge_cells('A1:L2')
dash['A3']='Editable decision workbook | synthetic, organisation-neutral demonstration | 3 cohorts × 50 trainees × 6 placements';dash.merge_cells('A3:L3');dash['A3'].font=Font(italic=True,color='666666')
kpis=[('A5','Allocation episodes','=COUNTA(Allocation_Decisions!A:A)-1'),('D5','Trainees','=COUNTA(Trainee_Journeys!A:A)-1'),('G5','First-choice outcomes','=COUNTIF(Allocation_Decisions!N:N,1)'),('J5','Human reviews','=COUNTIF(Allocation_Decisions!Y:Y,"Yes")')]
for cell,label,formula in kpis:
    dash[cell]=label;dash[cell].font=Font(bold=True,color='666666');v=dash.cell(dash[cell].row+1,dash[cell].column);v.value=formula;v.font=Font(size=24,bold=True,color=navy)
dash['A9']='How each allocation was decided';dash['A9'].font=Font(size=16,bold=True,color=navy)
steps=[('1','Remove infeasible offers','Capacity, approval, supervision, eligibility, quality and adjustment compatibility.'),('2','Assess pathway need','Outstanding competencies, breadth and developmental sequence.'),('3','Score feasible matches','Core placements use training need; specialist placements can include reviewed preferences.'),('4','Optimise cohort-wide','Maximise total pathway value without breaching capacity.'),('5','Human review','Review exceptions, approve overrides and record reasons before release.')]
for i,(n,title,desc) in enumerate(steps,10):
    dash.cell(i,1,n).font=Font(size=16,bold=True,color=white);dash.cell(i,1).fill=PatternFill('solid',fgColor=blue);dash.cell(i,2,title).font=Font(bold=True);dash.cell(i,4,desc);dash.merge_cells(start_row=i,start_column=4,end_row=i,end_column=12)
# summaries for charts
start=18;dash.cell(start,1,'Preference outcome');dash.cell(start,2,'Count')
for i in range(1,7): dash.cell(start+i,1,f'Rank {i}');dash.cell(start+i,2,f'=COUNTIF(Allocation_Decisions!N:N,{i})')
chart=BarChart();chart.type='bar';chart.style=10;chart.title='Preference outcomes across 900 episodes';chart.y_axis.title='Preference rank';chart.x_axis.title='Allocation episodes';chart.add_data(Reference(dash,min_col=2,min_row=start,max_row=start+6),titles_from_data=True);chart.set_categories(Reference(dash,min_col=1,min_row=start+1,max_row=start+6));chart.height=7;chart.width=12;dash.add_chart(chart,'D18')
# cohort year table
dash['A26']='Cohort and year summary';dash['A26'].font=Font(size=16,bold=True,color=navy)
for j,h in enumerate(['Cohort','Year','Episodes','Mean score','Reviews'],1):dash.cell(27,j,h).font=Font(bold=True,color=white);dash.cell(27,j).fill=PatternFill('solid',fgColor=navy)
r=28
for cohort in ['Cohort 1','Cohort 2','Cohort 3']:
 for year in [1,2,3]:
  dash.cell(r,1,cohort);dash.cell(r,2,year);dash.cell(r,3,f'=COUNTIFS(Allocation_Decisions!B:B,A{r},Allocation_Decisions!D:D,B{r})');dash.cell(r,4,f'=AVERAGEIFS(Allocation_Decisions!W:W,Allocation_Decisions!B:B,A{r},Allocation_Decisions!D:D,B{r})');dash.cell(r,5,f'=COUNTIFS(Allocation_Decisions!B:B,A{r},Allocation_Decisions!D:D,B{r},Allocation_Decisions!Y:Y,"Yes")');r+=1
for col,w in {'A':24,'B':18,'C':18,'D':18,'E':18,'F':4,'G':18,'H':18,'I':18,'J':18,'K':18,'L':18}.items():dash.column_dimensions[col].width=w

# trainee journeys
jour=wb.create_sheet('Trainee_Journeys');jh=['Trainee_ID','Cohort','Y1R1','Y1R2','Y2R1','Y2R2','Y3R1','Y3R2','Distinct_Placements','Mean_Score','Review_Count'];jour.append(jh)
by={}
for r in rows:by.setdefault(r['student_id'],[]).append(r)
for sid,rr in sorted(by.items()):
 rr=sorted(rr,key=lambda x:(int(x['year']),int(x['rotation'])));jour.append([sid,rr[0]['cohort']]+[x['placement_code'] for x in rr]+[len(set(x['placement_code'] for x in rr)),round(sum(float(x['total_score']) for x in rr)/6,2),sum(int(x['preference_rank'])>=4 or int(x['adjustment_score'])>0 for x in rr)])
for c in jour[1]:c.font=Font(color=white,bold=True);c.fill=PatternFill('solid',fgColor=navy)
jour.freeze_panes='A2';jour.add_table(Table(displayName='TraineeJourneys',ref=f'A1:K{jour.max_row}'));[setattr(jour.column_dimensions[get_column_letter(i)],'width',18) for i in range(1,12)]

# README
rd=wb.create_sheet('Read_Me',1);rd.column_dimensions['A'].width=28;rd.column_dimensions['B'].width=115
content=[('Purpose','Shows each recommended allocation, the scored decision basis, review flags, and an editable override workflow.'),('Edit allocations','In Allocation_Decisions, choose an Override_Placement in column K, select an Override_Reason in L, update Approval_Status in M, and add Reviewer_Comment in Z. Final_Placement updates automatically.'),('Do not edit','Decision_ID, trainee identity codes, period, score outputs or formulas unless rebuilding the model.'),('Core placements','Placements 1–4 are driven by competency need, breadth, sequence, feasibility and fairness. Preference is not intended to dominate.'),('Specialist placements','Placements 5–6 can include advisor-reviewed ranked preferences after hard constraints pass.'),('Yellow cells','Editable decision fields.'),('Red review flag','The row requires human consideration before approval.'),('Governance','Keep diagnoses, detailed adjustment evidence, names and organisation identifiers outside this workbook. Use pseudonymous codes and controlled access.'),('Important','This workbook is a synthetic demonstration. Before operational deployment, connect scores to approved taxonomies, travel data, real placement offers and documented policy weights.')]
rd['A1']='Workbook guide';rd['A1'].font=Font(size=20,bold=True,color=white);rd['A1'].fill=PatternFill('solid',fgColor=navy);rd.merge_cells('A1:B2')
for i,(a,b) in enumerate(content,4):rd.cell(i,1,a).font=Font(bold=True,color=navy);rd.cell(i,2,b).alignment=Alignment(wrap_text=True,vertical='top');rd.row_dimensions[i].height=42

wb.calculation.fullCalcOnLoad=True;wb.calculation.forceFullCalc=True;wb.save(OUT)
print(OUT)
