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

## Why does it exist?

The project is intended to help people learn and discuss:

- how placement choices might be organised;
- how fairness and training needs could be considered;
- how reviewers might check and question a recommendation;
- how sensitive information could be kept separate;
- how decisions could be recorded clearly.

The project provides a demonstration, not a working system for real clinical training.

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
