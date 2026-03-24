# Genesis Group Assignment - Test Report

## 1. Objective
Validate the campaign KPI engine using:
- one primary scenario dataset
- five edge-case datasets
- comparison of actual vs expected KPI outputs

## 2. Scope
This report covers:
- Task A dataset generation validation
- Task B KPI comparison for main scenario
- Task C edge-case execution and observations

## 3. Files Used

### Main Dataset
- `datasets/scenario1.json`

### Main Output Files
- `reports/report1_actual.json`
- `reports/expected_results.json`
- `reports/comparison_notes.md`

### Edge Case Datasets
- `datasets/edge_cases/zero_spend_case.json`
- `datasets/edge_cases/zero_conversion_case.json`
- `datasets/edge_cases/high_revenue_case.json`
- `datasets/edge_cases/invalid_channel_case.json`
- `datasets/edge_cases/duplicate_event_case.json`

### Edge Case Outputs
- `reports/zero_spend_case_actual.json`
- `reports/zero_conversion_case_actual.json`
- `reports/high_revenue_case_actual.json`
- `reports/invalid_channel_case_actual.json`
- `reports/duplicate_event_case_actual.json`
- `reports/edge_case_notes.md`

## 4. Test Approach
The approach used was:
1. Generate a schema-valid synthetic dataset from scenario text
2. Run the dataset through the KPI engine
3. Compare actual output against expected KPI values
4. Create focused edge-case datasets
5. Observe handling of numerical and validation edge cases

## 5. Environment
- Language: Python
- Validation: JSON schema validation
- Execution method: local Python scripts using virtual environment interpreter
- Main engine file: `campaign_engine.py`

## 6. Summary
Detailed findings are documented in:
- `comparison_notes.md`
- `edge_case_notes.md`
- `defect_log.md`

## 7. Main Scenario Test Result

### Scenario
Primary dataset generated from the provided March 2024 campaign scenario for `acme_corp`.

### Execution Result
The dataset was successfully processed by the KPI engine and output was saved in:
- `reports/report1_actual.json`

### Expected vs Actual Review
The KPI comparison was documented in:
- `reports/comparison_notes.md`

### Main KPI Output Observed
- total_spend_usd = 8200.0
- total_revenue_usd = 12960.0
- impression_count = 4
- click_count = 4
- conversion_count = 4
- roas = 1.5805
- conversion_rate_pct = 100.0
- budget_usd = 10000.0
- budget_pacing_pct = 0.82

### Observation
The engine executed successfully for the primary scenario and produced a valid aggregated KPI output.

## 8. Edge Case Test Results

### Edge Case 1: Zero Spend Case
Result: Pass  
Observation: Engine handled zero spend without crash. ROAS and pacing stayed at 0.

### Edge Case 2: Zero Conversion Case
Result: Pass  
Observation: Engine handled zero-conversion scenario correctly. Revenue and conversion rate stayed at 0.

### Edge Case 3: High Revenue Case
Result: Pass  
Observation: Engine handled very high ROAS scenario correctly.

### Edge Case 4: Invalid Channel Case
Result: Fail  
Observation: Invalid channel `linkedin_ads` was accepted and processed.

### Edge Case 5: Duplicate Event Case
Result: Fail  
Observation: Duplicate event IDs were double-counted.

## 9. Overall Test Conclusion

The KPI engine executed successfully for the main scenario and multiple edge cases.

### Strengths
- Handles zero spend safely
- Handles zero conversion safely
- Handles high revenue / high ROAS scenarios without crash

### Weaknesses
- Accepts invalid channel values without rejection
- Does not deduplicate duplicate event IDs
- Count-based KPIs appear to reflect row counts when aggregated synthetic events are used

### Final QA Assessment
The engine is functionally stable for basic KPI math, but there are validation and data-quality handling gaps that should be fixed before production use.
