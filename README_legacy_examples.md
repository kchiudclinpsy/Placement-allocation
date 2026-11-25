# Placement Allocation Tool — Educational Demonstration

> **Education and synthetic training examples only. This tool is not designed or approved for real placement decisions.**
>
> Do not provide it with real, anonymised or pseudonymised trainee or placement records, names, contact details, wellbeing or health information, postcodes, addresses, free text, or name-to-code mappings. Use the bundled synthetic data only.

## Privacy boundary

The legacy allocator accepts only a small, fixed synthetic CSV schema. It rejects extra columns and invalid values before optimization, writes generic errors without copying rejected cell contents into reports, and emits only synthetic demo IDs and coded placement IDs. Postcodes, names, free text and wellbeing-related inputs are not part of its schema. This is a fail-closed guardrail, not a guarantee that arbitrary data can be made anonymous or that every identifier can be detected; never use real data with this repository.

The longitudinal examples elsewhere in this repository are independently generated synthetic demonstrations and should not be populated with real records. All use is for discussion, not allocation or clinical decisions.

## Run the bundled synthetic example

```bash
python -m pip install -r requirements.txt
python allocate.py --input-dir . --output-dir outputs --options 3
```

The demonstration uses synthetic IDs, ranked placement codes, fixed category labels and example numeric constraints. Outputs are fictional and must not be interpreted as recommendations for real people.

## Governance

Keep personal, identifying, wellbeing, health, patient and location data out of repository files, prompts, and output folders. Do not use even anonymised or pseudonymised data. Any separate real-world system would require its own formal governance, privacy and safety assessment; this repository does not support or authorize such use.
