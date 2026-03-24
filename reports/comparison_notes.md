# Actual vs Expected Comparison

## Scenario Summary
Client: acme_corp  
Month: March 2024  
Budget: 10000 USD  
Total Spend: 8200 USD  
Impressions: 45000  
Clicks: 1800  
Conversions: 72  
Average Revenue per Conversion: 180 USD  
Expected Total Revenue: 12960 USD  

## Actual Engine Output Summary
- client_id: acme_corp
- total_spend_usd: 8200.0
- total_revenue_usd: 12960.0
- impression_count: 4
- click_count: 4
- conversion_count: 4
- roas: 1.5805
- conversion_rate_pct: 100.0
- budget_usd: 10000.0
- budget_pacing_pct: 0.82
- skipped_event_count: 0

## Comparison
### Values that match expected scenario
- total_spend_usd matches: 8200
- total_revenue_usd matches: 12960
- budget_usd matches: 10000
- budget_pacing_pct matches: 0.82
- channel spend split is approximately aligned with 70 percent Google Ads spend

### Values that do NOT match expected scenario
- impression_count is 4, but scenario expectation is 45000
- click_count is 4, but scenario expectation is 1800
- conversion_count is 4, but scenario expectation is 72

## Initial Observation
The engine appears to count the number of event rows by type instead of using business totals represented by the synthetic aggregated events.

## Possible Defect Hypothesis
If each event row represents an aggregated bucket rather than a single atomic user event, then the KPI engine is undercounting impressions, clicks, and conversions.

## Conclusion
The engine output is partially correct for spend, revenue, pacing, and ROAS-related values, but the count-based KPIs do not match the business scenario and likely reveal a logic issue in the KPI computation model.