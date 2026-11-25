# Longitudinal Clinical Placement Allocation Toolkit

> Illustrative workflow for discussion only. Any real use would require local governance approval, a DPIA and human panel decisions.
>
> The files and examples are synthetic. This toolkit is not an operational procedure and must not be used to make real placement or clinical decisions.

This organisation-neutral example describes a fictional three-cohort training pathway with two placements per year over three years. It is provided only to support education and discussion; timings, criteria, weights and thresholds below are illustrative and are not standards.

## Synthetic data only and privacy boundary

Never add real, anonymised or pseudonymised trainee or placement data. Do not include names, contact details, dates of birth, wellbeing or health information, postcodes, addresses, free text, patient data, or any mapping between a person and a demo ID. Examples use invented IDs and broad fictional codes only. The validator checks a narrow schema; it is not a PII detector or a guarantee of anonymity.

## Design principles (for discussion)

1. Patient and clinical safety override preference.
2. Placements 1 to 4 are shown as core-development allocations; specific service preference is not assumed.
3. Placements 5 and 6 can illustrate ranked trainee choices after competency gaps and eligibility.
4. Previous placements, client groups, settings, approaches and competency evidence can be considered only as synthetic coded examples.
5. Geographic base is represented with invented zone codes, never a postcode or address.
6. No wellbeing, health, diagnosis, adjustment evidence or narrative information is collected by this demo.
7. Provider availability and supervisor approval are represented as fictional coded data.
8. The optimiser demonstrates options and an audit trail. A named human panel—not software—would make any real decision.

## Illustrative scale

- 3 cohorts x 50 fictional trainees = 150 records
- 2 rotations per year x 3 years = 6 placement episodes per fictional trainee
- 900 example allocation episodes across a fictional three-year pathway

## Files

- `trainees.csv`: synthetic demo IDs and coded example attributes.
- `placement_offers.csv`: synthetic rotation-specific capacity, approval and supervision information.
- `placement_capabilities.csv`: example client groups, settings, approaches, assessments and competency opportunities.
- `placement_history.csv`: synthetic completed placement episodes and outcomes.
- `competency_status.csv`: coded example competency evidence and gaps.
- `specialist_preferences.csv`: example ranked choices for placements 5 and 6 only.
- `allocation_policy.csv`: example versioned hard/soft rules and weights.
- `review_flags.csv`: synthetic coded flags for human-review discussion only; never enter wellbeing or health information.
- `validate_demo_data.py`: validation of synthetic demo files; it is not a readiness assessment for real use.
- `DATA_DICTIONARY.md`: field definitions and example data-governance notes.

## Illustrative workflow (discussion example only)

The following sequence is fictional and must not be treated as operational guidance or a recommended timetable:

1. The example uses a hypothetical placement-offer freeze point 8 to 10 weeks before a rotation.
2. It shows reconfirmation of supervisor approval, capacity, supervision, cover arrangements and placement quality.
3. It uses synthetic placement history and competency-status files.
4. It represents only fictional, coded examples.
5. For core placements, it demonstrates competency need, breadth, base, travel and capacity without service-choice scoring.
6. Before example specialist placements, it illustrates a competency-gap review and advisor-reviewed ranked choices.
7. The demo validator can be run on synthetic files; its report is not evidence that a real process is safe or approved.
8. The example can produce a recommendation, alternatives, exception flags and rationales for discussion.
9. The example illustrates panel review and logging of overrides.
10. A hypothetical issue date 4 to 6 weeks before a placement is shown only as an example.

## Example constraints and objectives

The sample rules below are not accreditation criteria, professional standards or an approved local policy. They are toy values for discussion and must not be adopted for real decisions without appropriate governance and review. No wellbeing, health, identity or location data are used.

- One placement per fictional demo record per rotation; no example placement or supervisor capacity breach.
- Example placement and supervisor approval for the represented rotation.
- The sample validator uses 60 minutes of weekly supervision as an **example value**, not an official standard. The dataset also contains illustrative contingency-cover information.
- Trainee-stage eligibility, prerequisites and sequencing are example concepts.
- Example travel numbers are synthetic constraints, not addresses or postcodes.

Illustrative soft-objective weights (for discussion only):

- Outstanding competency need: 30
- Breadth across client group, setting and clinical presentation: 20
- Geographic base and travel burden: 15
- Developmental sequencing: 10
- Placement quality and recent trainee feedback: 10
- Provider preference: 5
- Fairness across cumulative pathway disadvantage: 10

These weights are examples, not validated or approved for real use.

## Human review and data protection discussion

Example review topics are fictional discussion prompts and do not replace professional judgement or a governed review process. Keep all personal, identifying, wellbeing, health, patient, free-text and location data out of the toolkit. The repository does not authorize or support real-data use.
