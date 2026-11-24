# Longitudinal Clinical Placement Allocation Toolkit

This organisation-neutral toolkit supports three concurrent cohorts of 50 trainees, two placements per year, and three years of training. It treats allocation as a six-placement pathway rather than six independent matches.

## Design principles

1. Patient and clinical safety override preference.
2. Placements 1 to 4 are core-development allocations. Specific service preference is not assumed.
3. Placements 5 and 6 can consider ranked trainee choices, after competency gaps and eligibility.
4. Previous placements, client groups, settings, approaches and competency evidence feed forward.
5. Geographic base is prioritised, but approved out-of-base allocations can be used when necessary.
6. Reasonable adjustments are represented by non-sensitive constraint codes, not diagnoses or narrative health information.
7. Provider availability and supervisor approval are time-bounded and must be reconfirmed for each rotation.
8. The optimiser produces options and an audit trail. A named human panel approves the final allocation.

## Scale

- 3 cohorts x 50 trainees = 150 active trainees
- 2 rotations per year x 3 years = 6 placement episodes per trainee
- 900 allocation episodes across a complete three-year pathway

## Files

- `trainees.csv`: pseudonymous trainee record and broad operational constraints.
- `placement_offers.csv`: rotation-specific capacity, approval and supervision information.
- `placement_capabilities.csv`: client groups, settings, approaches, assessments and competency opportunities offered.
- `placement_history.csv`: completed placement episodes and outcomes.
- `competency_status.csv`: coded competency evidence and gaps carried forward.
- `specialist_preferences.csv`: ranked choices for placements 5 and 6 only.
- `allocation_policy.csv`: versioned hard/soft rules and weights.
- `review_flags.csv`: restricted, minimal flags requiring human review.
- `validate_real_use.py`: cross-file validation and readiness report.
- `DATA_DICTIONARY.md`: field definitions and governance rules.

## Workflow

1. Freeze placement offers 8 to 10 weeks before a rotation.
2. Reconfirm supervisor approval, capacity, weekly supervision, cover arrangements and placement quality status.
3. Import prior placement history and competency status.
4. Capture only operationally necessary adjustment codes in the allocation dataset.
5. For core placements, optimize competency need, breadth, base, travel and capacity without service-choice scoring.
6. Before specialist placements, complete a formal competency-gap review and collect advisor-reviewed ranked choices.
7. Run validation. Blocking errors must be resolved before optimization.
8. Generate a recommended allocation, at least two alternatives, exception flags and an allocation rationale for every trainee.
9. Conduct panel review. Log overrides with reason codes.
10. Issue allocations approximately 4 to 6 weeks before the placement starts.

## Required hard constraints

- One placement per trainee per rotation.
- No placement or supervisor capacity breach.
- Placement and supervisor approved for the exact rotation.
- Required supervision capacity available, including at least one hour weekly and contingency cover.
- Trainee-stage eligibility and prerequisites satisfied.
- Core-placement sequencing and outstanding competency needs satisfied.
- No unsafe or prohibited repeat experiences.
- Approved adjustment codes and travel constraints satisfied.
- Any active safety, fitness-to-practise or placement-quality hold excludes automatic allocation and requires panel review.

## Soft objectives

Suggested starting weights, to be locally approved and sensitivity-tested:

- Outstanding competency need: 30
- Breadth across client group, setting and clinical presentation: 20
- Geographic base and travel burden: 15
- Developmental sequencing: 10
- Placement quality and recent trainee feedback: 10
- Provider preference: 5
- Fairness across cumulative pathway disadvantage: 10

For specialist placements only, redistribute 15 to 25 points to trainee ranked preference after all hard constraints are met. Do not apply specialist-choice weights to core placements.

## Human review triggers

- No feasible placement
- Out-of-base allocation
- Adjustment-sensitive allocation
- Previous placement failure or incomplete placement
- Outstanding mandatory competency gap late in training
- Placement or supervisor with unresolved quality concerns
- Unusual cumulative travel burden
- Repeated low-preference outcome
- Proposed override of optimiser recommendation

## Data protection

Use pseudonymous IDs. Do not store diagnoses, clinical narratives, patient information, named concerns, or free-text occupational-health reports in the allocation files. Keep the mapping to real identities and supporting adjustment evidence in separate access-controlled systems. The exported dashboard must suppress small-cell or sensitive comparisons and must not expose restricted review flags.
