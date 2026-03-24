# Genesis Group Assignment Notes

## Objective
Generate a schema-valid synthetic campaign event dataset from a business scenario using AI-assisted simulation, then validate and save the output using Python.

## Files Created
- `event_schema.json` — JSON schema for dataset validation
- `prompt_templates.py` — prompt template builder for scenario-based generation
- `generate_dataset.py` — loads schema, prints prompt, reads raw AI output, validates JSON, saves final dataset
- `raw_llm_output/scenario1_raw.txt` — raw AI response used as simulation input
- `datasets/scenario1.json` — validated final dataset output

## Approach
1. Studied the assignment files and extracted the dataset schema requirements.
2. Stored the schema in a separate JSON file for strict validation.
3. Built a prompt template that instructs the AI to return only schema-valid JSON.
4. Implemented a Python generator script that:
   - prints the prompt,
   - reads the raw AI output from a file,
   - parses JSON,
   - validates against schema using `jsonschema`,
   - saves the validated output.
5. Used simulation mode to manually iterate on the AI prompt and raw output.

## AI Usage
AI was used for:
- prompt drafting,
- synthetic dataset generation,
- iteration based on validation failures.

Python was used for:
- schema validation,
- parsing,
- error detection,
- saving the final structured output.

## Iteration Summary
### Attempt 1
- Output passed schema validation
- But business values did not fully match the scenario
- Example: budget/revenue assumptions were inaccurate

### Attempt 2
- Prompt was tightened to force exact scenario numbers
- Output attempted to follow the scenario more closely
- But failed schema validation because numeric fields were returned as strings

### Attempt 3
- Prompt was strengthened further with explicit numeric constraints
- Final output passed validation and matched the scenario much better

## Final Result
The final dataset passed schema validation successfully and was saved to:
`datasets/scenario1.json`

Validation message:
`Validation passed. 12 event(s) saved to datasets\\scenario1.json`

## Key Learning
AI generation alone was not enough.
The reliable approach was:
AI for generation + Python for strict validation + iterative prompt refinement.

## Task B Summary
I executed the generated dataset through the provided KPI engine and captured the actual output in `reports/report1_actual.json`.

I also created `reports/expected_results.json` based on the scenario text and documented the comparison in `reports/comparison_notes.md`.

Result:
- Spend, revenue, budget, and pacing values aligned with the scenario.
- However, impression, click, and conversion counts did not align with the expected business totals.
- This suggests the engine may be counting rows by event type rather than interpreting aggregated business totals from the dataset.