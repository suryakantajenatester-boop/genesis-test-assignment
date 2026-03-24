# Edge Case Testing Notes

## Edge Case 1: Zero Spend Case

### Dataset File
`datasets/edge_cases/zero_spend_case.json`

### Output File
`reports/zero_spend_case_actual.json`

### Expected Behavior
- Total spend should be 0
- Total revenue should be 0
- ROAS should be 0
- Budget pacing should be 0
- Engine should not crash on divide-by-zero style calculations

### Actual Behavior
- total_spend_usd = 0.0
- total_revenue_usd = 0.0
- roas = 0.0
- budget_pacing_pct = 0.0
- impression_count = 1
- click_count = 1
- conversion_count = 1
- conversion_rate_pct = 100.0

### Observation
The engine handled zero spend safely without crashing. However, the count-related metrics still reflect row counts rather than business totals.

### QA Note
This suggests the engine is robust for zero-value math, but its counting logic may not support aggregated event datasets correctly.

## Edge Case 2: Zero Conversion Case

### Dataset File
`datasets/edge_cases/zero_conversion_case.json`

### Output File
`reports/zero_conversion_case_actual.json`

### Expected Behavior
- Total spend should be 600
- Total revenue should be 0
- ROAS should be 0
- Conversion count should be 0
- Conversion rate should be 0%

### Actual Behavior
- total_spend_usd = 600.0
- total_revenue_usd = 0.0
- impression_count = 1
- click_count = 2
- conversion_count = 0
- roas = 0.0
- conversion_rate_pct = 0.0

### Observation
The engine handled the no-conversion scenario correctly. Spend accumulated properly, revenue remained zero, and conversion-based KPIs stayed at zero.

### QA Note
This case appears to pass and suggests the engine is stable for non-converting traffic scenarios.

## Edge Case 3: High Revenue Case

### Dataset File
`datasets/edge_cases/high_revenue_case.json`

### Output File
`reports/high_revenue_case_actual.json`

### Expected Behavior
- Total spend should be 100
- Total revenue should be 5000
- ROAS should be very high
- Conversion count should be 1
- Conversion rate should be 100%

### Actual Behavior
- total_spend_usd = 100.0
- total_revenue_usd = 5000.0
- impression_count = 1
- click_count = 1
- conversion_count = 1
- roas = 50.0
- conversion_rate_pct = 100.0

### Observation
The engine handled an unusually high-revenue scenario correctly. ROAS calculation worked as expected and no overflow or abnormal formatting issue appeared.

### QA Note
This case passes and shows the engine can process extreme positive revenue efficiency scenarios.

## Edge Case 4: Invalid Channel Case

### Dataset File
`datasets/edge_cases/invalid_channel_case.json`

### Output File
`reports/invalid_channel_case_actual.json`

### Expected Behavior
- Invalid channel events should be skipped or rejected
- skipped_event_count should increase
- Only valid channel data should be processed

### Actual Behavior
- linkedin_ads events were processed
- skipped_event_count = 0
- google_ads conversion was also processed
- channel_breakdown contains linkedin_ads

### Observation
The engine did not reject or skip the invalid channel value `linkedin_ads`. This suggests channel validation is missing or not enforced during KPI computation.

### QA Note
This is a defect. Invalid channel values are being accepted into final KPI results.

## Edge Case 5: Duplicate Event Case

### Dataset File
`datasets/edge_cases/duplicate_event_case.json`

### Output File
`reports/duplicate_event_case_actual.json`

### Expected Behavior
- Duplicate event_id should ideally be ignored or deduplicated
- Click count should remain 1 if deduplication is applied
- Spend should remain 300 if duplicate click is ignored

### Actual Behavior
- Duplicate click event was counted twice
- click_count = 2
- total_spend_usd = 600.0
- skipped_event_count = 0

### Observation
The engine processed duplicate event_id values as separate events. No deduplication or duplicate-event protection appears to be implemented.

### QA Note
This is a defect if duplicate event IDs are expected to be unique and should not be double-counted.

## Final Edge Case Summary

Created and executed 5 edge-case datasets:

1. Zero Spend Case
2. Zero Conversion Case
3. High Revenue Case
4. Invalid Channel Case
5. Duplicate Event Case

### Key Findings
- Zero spend case handled without crash
- Zero conversion case handled without crash
- High revenue case produced very high ROAS successfully
- Invalid channel case was incorrectly accepted by the engine
- Duplicate event case was double-counted by the engine

### Overall QA Conclusion
The engine handles basic numerical edge cases, but there are validation gaps around invalid channels and duplicate event IDs. These should be logged as defects.