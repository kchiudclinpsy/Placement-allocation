# Placement Allocation Toolkit

## Dummy guide: one folder, Excel files, and one script

You can use this toolkit with one working folder containing:

1. Your Excel-compatible placement files (`.xlsx` or `.csv` exports)
2. The Python script
3. A folder for the generated outputs

No website setup or database is required.

```text
placement-demo/
├── students.xlsx
├── placements.xlsx
├── placement_preferences.xlsx
├── allocation_rules.xlsx
├── allocate.py
└── outputs/
```

Excel is only for preparing and reviewing the input data. The script reads the files, validates them, creates the allocation results, and generates the visual summary.

## Quick start

1. Put all Excel files and `allocate.py` in the same folder.
2. Open a terminal in that folder.
3. Install the requirements:

```bash
python -m pip install -r requirements.txt
```

4. Run the script:

```bash
python allocate.py --input-dir . --output-dir outputs --options 3
```

5. Generate the visual summary:

```bash
python generate_visual_summary.py --output-dir outputs
```

6. Open `outputs/visual_summary.html` in a browser.

## What the script generates

- A visual summary of the validation status and allocation options
- A recommended allocation option
- Alternative allocation options
- CSV audit and result files
- A print-friendly HTML report

The visual summary is generated locally and contains no external scripts, fonts, or network calls.

## Dummy Excel file names

The example data can use these dummy names:

| File | Purpose |
|---|---|
| `students.xlsx` | Student details and placement preferences |
| `placements.xlsx` | Available placement sites and capacity |
| `placement_preferences.xlsx` | Student ranking of placement options |
| `allocation_rules.xlsx` | Scoring and allocation weights |

Your real filenames can differ if you update the script settings or use the expected CSV exports.

## Workflow

```text
Excel files
    ↓
One Python script
    ↓
Validation and allocation
    ↓
CSV results + visual HTML summary
```

## Notes

- Keep a backup copy of the original Excel files.
- Review the validation report before accepting a result.
- The visual summary supports decision-making; a human reviewer should document the final choice.
- Do not include sensitive student information in a public repository.
