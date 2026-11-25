# Placement Allocation Tool — Educational Demonstration

> **This repository is for education and training only.**
>
> It contains synthetic (made-up) examples. It has **never been used** to allocate real trainee placements or make decisions about real people. It must not be used for real placement or clinical decisions.

## What is this project?

This project demonstrates how a placement process might be organised for 150 fictional trainees: three cohorts of 50, two placements in each of three training years, and 900 fictional placement records in total. The examples use made-up names and codes rather than real people or organisations.

The project is intended to help people learn and discuss how placement choices might be organised, how fairness and training needs could be considered, how reviewers might check recommendations, how sensitive information could be kept separate, and how decisions could be recorded. It is a demonstration, not a working system for real clinical training.

## Exemplar prompts for the four steps

Use the synthetic files in this repository only. Any real data would require local governance approval first. Never paste personal, medical or identifiable trainee information into Copilot or another AI service.

### 1. Explain the rules

> “Act as a placement-process facilitator. Read the synthetic data and policy files in this repository, especially `trainees.csv`, `placement_offers.csv`, `allocation_policy.csv` and `DATA_DICTIONARY.md`. Explain the allocation rules in plain English under these headings: hard constraints that must be met; soft factors used for ranking; specialist preferences for placements 5 and 6; review triggers; and information that must remain out of the allocation dataset. Use only the supplied files and flag any ambiguity rather than inventing a rule.”

### 2. Build a demonstration matcher

> “Using only the synthetic repository files, help me run a safe simulation of the placement matcher. Identify the required inputs, validate the data against `allocation_policy.csv`, and explain the constraints before generating results. Do not allocate real people or use personal or medical details. Produce a demonstration recommendation, at least two alternative allocations, and an audit trail showing which rules affected each allocation.”

### 3. Configure the demonstration

> “Configure the demonstration for three cohorts, each with 50 synthetic trainees, two placements per year, and six placements in total. Set core placements 1 to 4 to prioritise competency need, breadth, sequencing, geography and placement quality. Consider ranked specialist preferences only for placements 5 and 6, after essential eligibility and training requirements have been met. Include capacity, supervisor approval, reasonable-adjustment constraints and human-review flags. Refine the configuration with a list of assumptions for a reviewer to confirm.”

### 4. Review results

> “Review the synthetic allocation outputs without approving them automatically. Explain why each sample recommendation was made, highlight the factors that supported or limited it, compare the alternative options, and identify placements requiring human review. Check safety, supervision, trainee-stage eligibility, travel or adjustment concerns, quality alerts and unusual or repeated outcomes. State clearly that final decisions require named human oversight.”

## Example files and outputs

Open `editable_longitudinal_allocation_dashboard.xlsx` to explore a visual example with fictional allocation records, recommendation rationales, reviewer flags, override fields and each fictional trainee's placement journey. Yellow cells in the `Allocation_Decisions` sheet are for demonstration reviewer entries only.

The `organisation_neutral_templates` folder contains synthetic example data, policy and guidance files. `validate_demo_data.py` checks the demo files and writes a readiness report. These templates and their workflow are illustrative discussion material, not operational instructions. The `longitudinal_demo_outputs` folder contains synthetic examples; they are not performance results or benchmarks.

## Recreate the demonstration

Install dependencies and generate the synthetic data and workbook:

```bash
python -m pip install -r requirements.txt
python longitudinal_3cohort_demo.py
python create_editable_allocation_workbook.py
```

## Important limitations and safety

- All data is fictional; recommendations are examples, not decisions.
- The project has never been used for real placement allocation and must not be used for real placement or clinical decisions.
- Keep real personal, medical and identifiable information out of this repository and out of AI prompts.
- Any real process would require appropriate local governance, approved policies and systems, and professional human oversight.
- Reviewers should inspect the rationale, check requirements and safety, and explain any demonstration override.

## Licensing

Code is available under the MIT License (`LICENSE`). Documentation, prompts and synthetic example data are available under CC BY 4.0 (`LICENSE-DOCUMENTATION.md`). Both licences require attribution; see the licence files for details.
