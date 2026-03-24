# AI Usage Log

## Objective
Document how AI was used during the assignment, what outputs it produced, and how those outputs were validated or corrected.

## AI Tools Used
- ChatGPT for prompt drafting, dataset generation support, iteration guidance, and documentation assistance

## Areas Where AI Was Used

### 1. Prompt Design
AI was used to help draft and refine prompts for converting the business scenario into structured JSON.

### 2. Synthetic Dataset Generation
AI was used in simulation mode to generate raw JSON dataset candidates from the scenario text.

### 3. Iteration Support
AI was used to refine prompts after validation issues were found.

### 4. Documentation Support
AI was used to help structure:
- assignment notes
- comparison notes
- edge-case notes
- test report
- defect log
- golden dataset strategy

## Iteration Record

### Iteration 1
Purpose:
Generate first scenario dataset.

Result:
- Output was schema-valid
- But business values were not fully aligned with the scenario

Action Taken:
Prompt was refined to force stricter scenario matching.

### Iteration 2
Purpose:
Improve scenario fidelity.

Result:
- Output attempted closer business matching
- But numeric fields were returned as strings and schema validation failed

Action Taken:
Prompt was refined again with strict numeric-type constraints.

### Iteration 3
Purpose:
Generate a schema-valid and business-aligned final dataset.

Result:
- Final output passed validation
- Final dataset saved successfully to `datasets/scenario1.json`

## Validation Safeguards
AI output was not trusted directly.
Each generated dataset was checked using:
- JSON parsing
- schema validation
- manual business KPI checks
- KPI engine execution
- actual vs expected comparison

## Key Principle Followed
AI was used as a generation and acceleration tool.
Final acceptance depended on deterministic validation and QA review.

## Final Note
This assignment was completed using a controlled AI-assisted workflow, where Python scripts and QA checks were used to verify correctness before accepting outputs.

