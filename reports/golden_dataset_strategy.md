# Golden Dataset Strategy

## Objective
Define a reliable strategy for maintaining trusted datasets that can be used to validate KPI engine behavior over time.

## What is a Golden Dataset
A golden dataset is a known-good input dataset with a verified expected output.
It is used as a regression baseline to confirm that future engine changes do not break existing KPI logic.

## Why It Is Needed
The assignment showed that:
- schema-valid data is not always business-correct
- engine outputs may look correct for spend/revenue but still fail on count logic
- edge cases can expose validation and data-quality issues

Because of this, a golden dataset strategy is needed to ensure repeatable and trusted testing.

## Recommended Golden Dataset Coverage

### 1. Main Happy Path Dataset
A realistic business scenario with:
- valid schema
- known spend, revenue, budget, pacing, and channel split
- clearly documented expected KPI output

Example:
- `datasets/scenario1.json`
- expected result in `reports/expected_results.json`

### 2. Edge-Case Golden Datasets
Maintain trusted edge-case datasets for:
- zero spend
- zero conversion
- high revenue / high ROAS
- invalid channel values
- duplicate event IDs

These help validate both mathematical correctness and defensive data handling.

### 3. Business Rule Validation Datasets
Additional datasets should be created for:
- mixed client IDs
- inconsistent budgets for same client
- malformed timestamps
- unsupported event types
- empty input
- null or missing fields

## Versioning Strategy
Each golden dataset should have:
- a stable file name
- a version number
- a short description of purpose
- a matching expected output file

Example naming:
- `scenario1_v1.json`
- `scenario1_v1_expected.json`

## Validation Strategy
Every golden dataset should be checked in two stages:
1. Schema validation
2. KPI output validation against expected results

Schema validation alone is not enough.
Business KPI comparison must also be included.

## Storage Strategy
Store golden datasets and expected outputs in a dedicated structure, for example:

- `datasets/golden/`
- `reports/golden_expected/`

This keeps baseline files separate from ad hoc experiments.

## Update Policy
Golden datasets should only be updated when:
- business logic intentionally changes
- KPI definitions are officially revised
- defects are fixed and expected outputs must be updated accordingly

Every update should include a reason and reviewer approval.

## Regression Usage
On every engine change:
1. run all golden datasets
2. compare actual results with expected outputs
3. flag any mismatch immediately

This should become part of continuous QA validation.

## Final Recommendation
The best long-term strategy is to maintain a small but high-quality suite of golden datasets that cover:
- core business flow
- numerical edge cases
- invalid input handling
- duplication and data quality scenarios

This will make the KPI engine easier to trust, test, and maintain.