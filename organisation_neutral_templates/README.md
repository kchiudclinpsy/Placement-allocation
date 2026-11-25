# Longitudinal Clinical Placement Allocation Toolkit

> Illustrative workflow for discussion only. Any real use would require local governance approval, a DPIA and human panel decisions.
>
> The files and examples are synthetic. This toolkit is not an operational procedure and must not be used to make real placement or clinical decisions.

This organisation-neutral example describes a fictional three-cohort training pathway with two placements per year over three years. It is provided only to support education and discussion; timings, criteria, weights and thresholds below are illustrative and are not standards.

## Design principles (for discussion)

1. Patient and clinical safety override preference.
2. Placements 1 to 4 are shown as core-development allocations; specific service preference is not assumed.
3. Placements 5 and 6 can illustrate ranked trainee choices after competency gaps and eligibility.
4. Previous placements, client groups, settings, approaches and competency evidence can be considered.
5. Geographic base is prioritised in this example; an approved out-of-base allocation is shown as a review case.
6. Reasonable adjustments are represented by non-sensitive constraint codes, not diagnoses or narrative health information.
7. Provider availability and supervisor approval are represented as time-bounded example data.
8. The optimiser demonstrates options and an audit trail. A named human panel—not software—would make any real decision.

## Illustrative scale

- 3 cohorts x 50 fictional trainees = 150 records
- 2 rotations per year x 3 years = 6 placement episodes per fictional trainee
- 900 example allocation episodes across a fictional three-year pathway

## Files

- `trainees.csv`: synthetic pseudonymous trainee records and broad operational constraints.
- `placement_offers.csv`: synthetic rotation-specific capacity, approval and supervision information.
- `placement_capabilities.csv`: example client groups, settings, approaches, assessments and competency opportunities.
- `placement_history.csv`: synthetic completed placement episodes and outcomes.
- `competency_status.csv`: coded example competency evidence and gaps.
- `specialist_preferences.csv`: example ranked choices for placements 5 and 6 only.
- `allocation_policy.csv`: example versioned hard/soft rules and weights.
- `review_flags.csv`: synthetic coded flags for human-review discussion.
- `validate_demo_data.py`: validation of the synthetic demo files; it is not a readiness assessment for real use.
- `DATA_DICTIONARY.md`: field definitions and example data-governance notes.

## Illustrative workflow (discussion example only)

The following sequence is fictional and must not be treated as operational guidance or a recommended timetable:

1. The example uses a hypothetical placement-offer freeze point 8 to 10 weeks before a rotation.
2. It shows reconfirmation of supervisor approval, capacity, supervision, cover arrangements and placement quality.
3. It uses synthetic placement history and competency-status files.
4. It represents only coded adjustment constraints in the example allocation dataset.
5. For core placements, it demonstrates competency need, breadth, base, travel and capacity without service-choice scoring.
6. Before example specialist placements, it illustrates a competency-gap review and advisor-reviewed ranked choices.
7. The demo validator can be run on synthetic files; its report is not evidence that a real process is safe or approved.
8. The example can produce a recommendation, alternatives, exception flags and rationales for discussion.
9. The example illustrates panel review and logging of overrides.
10. A hypothetical issue date 4 to 6 weeks before a placement is shown only as an example.

## Example constraints and objectives

The sample rules below are not accreditation criteria, professional standards or an approved local policy. They are toy values for discussion and must not be adopted for real decisions without appropriate governance and review.

- One placement per fictional trainee per rotation; no example placement or supervisor capacity breach.
- Example placement and supervisor approval for the represented rotation.
- The sample validator uses 60 minutes of weekly supervision as an **example value**, not an official standard. The dataset also contains illustrative contingency-cover information.
- Trainee-stage eligibility, prerequisites and sequencing are example concepts.
- The examples illustrate travel constraints and human review for coded safety, fitness-to-practise or placement-quality holds; they do not automate real decisions.

Illustrative soft-objective weights (for discussion only):

- Outstanding competency need: 30
- Breadth across client group, setting and clinical presentation: 20
- Geographic base and travel burden: 15
- Developmental sequencing: 10
- Placement quality and recent trainee feedback: 10
- Provider preference: 5
- Fairness across cumulative pathway disadvantage: 10

For the synthetic specialist-placement example only, 15 to 25 points may be redistributed to trainee ranked preference after all example hard constraints are met. These weights are not validated or approved for real use.

## Human review and data protection discussion

Example review topics include no feasible placement, out-of-base allocation, adjustment-sensitive allocation, incomplete placement history, competency gaps, quality concerns, cumulative travel burden, repeated low-preference outcomes and proposed overrides. These examples do not replace professional judgement or a governed review process.

The synthetic files use pseudonymous IDs. Do not add diagnoses, clinical narratives, patient information, named concerns or free-text occupational-health reports. In any real setting, data handling would require local governance and appropriate privacy safeguards; this repository does not authorize or support that use.
