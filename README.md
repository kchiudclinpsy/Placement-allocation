# Placement Allocation Tool — Educational Demonstration

> **This repository is for education and training only.**
>
> It contains synthetic (made-up) examples. It has **never been used** to allocate real trainee placements or make decisions about real people. It must not be used for real placement or clinical decisions.

## What is this project?

This project demonstrates how a placement process might be organised for 150 fictional trainees.

It shows:

- 3 fictional training cohorts;
- 50 trainees in each cohort;
- 2 placements in each training year;
- 3 years of training;
- 6 placements per trainee;
- 900 fictional placement records in total.

The examples use made-up names and codes rather than real people or organisations.

<img width="1024" height="572" alt="Making Clinical Placements Easier with Copilot" src="https://github.com/user-attachments/assets/ef03692e-c0be-44d1-afca-1e4cd679f587" />

## Why does it exist?

The project is intended to help people learn and discuss:

- how placement choices might be organised;
- how fairness and training needs could be considered;
- how reviewers might check and question a recommendation;
- how sensitive information could be kept separate;
- how decisions could be recorded clearly.

The project provides a demonstration, not a working system for real clinical training.

## Exemplar prompts for the four steps

These prompts show how an audience might work through the placement-allocation process with Copilot. Replace the fictional details with anonymised, approved training data only. Never paste personal, medical or identifiable trainee information into a prompt.

### 1. Explain the rules to Copilot

> “Act as a placement-process facilitator. Read the synthetic data and policy files in this repository, especially `trainees.csv`, `placement_offers.csv`, `allocation_policy.csv` and `DATA_DICTIONARY.md`. Explain the allocation rules in plain English under these headings: hard constraints that must be met; soft factors used for ranking; specialist preferences for placements 5 and 6; review triggers; and information that must remain out of the allocation dataset. Use only the supplied files and flag any ambiguity rather than inventing a rule.”

### 2. Ask AI to build the matcher

> “Using only the synthetic repository files, help me run a safe simulation of the placement matcher. Identify the required inputs, validate the data against `allocation_policy.csv`, and explain the constraints before generating results. Do not allocate real people or use personal or medical details. Produce a demonstration recommendation, at least two alternative allocations, and an audit trail showing which rules affected each allocation.”

### 3. Configure the placement programme

> “Configure the demonstration for three cohorts, each with 50 synthetic trainees, two placements per year, and six placements in total. Set core placements 1 to 4 to prioritise competency need, breadth, sequencing, geography and placement quality. Consider ranked specialist preferences only for placements 5 and 6, after essential eligibility and training requirements have been met. Include capacity, supervisor approval, reasonable-adjustment constraints and human-review flags. Refine the configuration with a list of assumptions for a reviewer to confirm.”

### 4. Review results and perform a human sense-check

> “Review the synthetic allocation outputs without approving them automatically. Explain why each sample recommendation was made, highlight the factors that supported or limited it, compare the alternative options, and identify placements requiring human review. Check for clinical safety, supervision, trainee-stage eligibility, travel or adjustment concerns, quality alerts and unusual or repeated outcomes. Use a table with: recommendation, evidence, uncertainty, review question and suggested reviewer action. State clearly that final decisions require named human oversight.”

## Start with the example workbook

Open:

`editable_longitudinal_allocation_dashboard.xlsx`

The workbook provides a visual example of:

- an executive summary;
- 900 fictional allocation records;
- a recommendation for each placement;
- reasons and information behind each recommendation;
- reviewer questions and flags;
- areas where a reviewer could enter an alternative decision;
- the full placement journey for each fictional trainee.

### Yellow boxes

In the `Allocation_Decisions` sheet, yellow boxes are intended for reviewer examples:

- `Override_Placement` — record an alternative choice;
- `Override_Reason` — explain why;
- `Approval_Status` — show the example approval outcome;
- `Reviewer_Comment` — add a note.

The workbook keeps the original recommendation visible and shows whether a reviewer changed it.

## What information is used in the example?

The demonstration uses broad, coded information rather than personal or medical details.

It considers factors such as:

- which skills a trainee still needs to develop;
- whether training experiences are varied;
- which stage of training the trainee has reached;
- whether a placement and supervisor are available;
- whether required supervision and support are present;
- travel needs and accessibility adjustments;
- fairness across the trainee's pathway;
- placement quality;
- advisor-approved specialist preferences, where relevant.

Core placements focus mainly on training needs. Specialist preferences are considered only for placements 5 and 6 and only after essential requirements have been met.

## How are the example files organised?

The `organisation_neutral_templates` folder contains example data and documents:

- trainee records;
- placement offers;
- placement skills and opportunities;
- previous placement information;
- competency information;
- specialist preferences;
- review flags;
- allocation rules;
- a validation script;
- a data dictionary;
- an operational guidance document.

These files use pseudonymous IDs and generic codes. They do not contain real organisation names, locations, personal names or links to internal systems.

## Demonstration outputs

The `longitudinal_demo_outputs` folder contains synthetic examples showing:

- 3 cohorts;
- 50 trainees per cohort;
- 6 placements per trainee;
- 900 fictional allocation episodes.

These outputs show the structure of the demonstration. They are not results that indicate performance or should be used as a benchmark.

## How to recreate the demonstration

### 1. Install the required software

Open a terminal and run:

```bash
python -m pip install -r requirements.txt
```

### 2. Create the sample data

```bash
python longitudinal_3cohort_demo.py
```

### 3. Create the example workbook

```bash
python create_editable_allocation_workbook.py
```

You do not need to understand the underlying code to explore the Excel workbook.

## Important limitations

- All data is fictional.
- The recommendations are examples, not decisions.
- The project has never been used for real placement allocation.
- A named human reviewer would be required for any real process.
- Real people and real placements require properly governed policies, systems and professional oversight.

## Human review and safety

The project does not approve placements automatically.

Reviewers should:

- read the reasons for each recommendation;
- check whether essential requirements are satisfied;
- consider safety and training quality;
- record any alternative choice;
- explain every override;
- keep personal and medical information out of allocation files.
