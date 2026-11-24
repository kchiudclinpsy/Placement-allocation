# Placement Allocation Tool — Educational Demonstration

> **Educational and training demonstration only**
>
> This repository is a synthetic proof of concept for educational and training purposes. It has **never been used** to allocate real trainee placements or to make decisions about real people. The data, outputs and recommendations are demonstration artifacts only and must not be used for operational allocation or clinical decision-making.

This organisation-neutral toolkit models three concurrent cohorts of 50 trainees. Each trainee completes two placements per year over three years, giving six placement episodes per trainee and 900 synthetic allocation records.

<img width="1024" height="572" alt="b10ff3c9-8405-4bb3-87b8-f8dc27c76f73" src="https://github.com/user-attachments/assets/906ed722-b14d-4567-b21c-bfc4f8994621" />

## Start here

Open `editable_longitudinal_allocation_dashboard.xlsx`.

The workbook contains:

- an executive dashboard;
- 900 editable allocation decisions;
- the recommendation and full decision basis for every placement episode;
- competency, breadth, sequence, provider, adjustment, travel and fairness scores;
- human-review flags;
- controlled override fields with dropdown lists;
- a full six-placement journey for every trainee;
- a decision-criteria sheet explaining hard constraints and weights.

Yellow cells in `Allocation_Decisions` are intended for reviewer editing:

- `Override_Placement`
- `Override_Reason`
- `Approval_Status`
- `Reviewer_Comment`

`Final_Placement` changes automatically when an override is entered, while preserving the original recommendation.

## Organisation-neutral operational templates

The `organisation_neutral_templates` folder contains:

- `trainees.csv`
- `placement_offers.csv`
- `placement_capabilities.csv`
- `placement_history.csv`
- `competency_status.csv`
- `specialist_preferences.csv`
- `review_flags.csv`
- `allocation_policy.csv`
- `validate_real_use.py`
- `readiness_report.csv`
- `DATA_DICTIONARY.md`
- detailed operational `README.md`

The templates use pseudonymous IDs and generic codes. They contain no organisation names, partner names, locations, personal names, logos, URLs or internal system names.

## Demonstration data

The `longitudinal_demo_outputs` folder contains synthetic outputs for:

- 3 cohorts;
- 50 trainees per cohort;
- 6 placements per trainee;
- 900 allocation episodes.

These demonstrate the structure only and are not intended as performance benchmarks or for real-world allocation.

## Regenerate the demonstration

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Create the longitudinal demonstration:

```bash
python longitudinal_3cohort_demo.py
```

Rebuild the editable Excel dashboard:

```bash
python create_editable_allocation_workbook.py
```

## Operational decision logic

### Hard constraints

- one placement per trainee per rotation;
- no placement or supervisor capacity breach;
- offer and supervisor approved for the exact rotation;
- required supervision and contingency cover confirmed;
- stage eligibility and prerequisites satisfied;
- adjustment and travel constraints satisfied;
- suspended or unsafe offers excluded;
- unresolved safety and quality cases routed to human review.

### Soft objectives

- outstanding competency need;
- breadth across client group, setting, presentation, approach and assessment;
- developmental sequence;
- travel burden;
- cumulative fairness;
- placement quality;
- provider preference;
- advisor-reviewed trainee preference for specialist placements.

Core placements should remain competency-led. Specialist preferences should only be scored after hard constraints have passed.

## Governance

The optimizer provides decision support, not automatic approval. Reviewers should record overrides and reasons in the workbook. Detailed health information, diagnoses, clinical narratives and personal data should not be entered into the demonstration workbook or operational allocation files.
