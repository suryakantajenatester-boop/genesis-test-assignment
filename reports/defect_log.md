# Genesis Group Assignment - Defect Log

## Defect 1: Invalid channel accepted by engine

### Defect ID
DEF-001

### Title
Engine accepts invalid channel values in KPI computation

### Related File
- `datasets/edge_cases/invalid_channel_case.json`
- `reports/invalid_channel_case_actual.json`

### Description
The dataset included an invalid channel value: `linkedin_ads`.
Expected behavior was that invalid channel events should be rejected or skipped.
Actual behavior showed that the engine processed the invalid channel and included it in `channel_breakdown`.

### Expected Result
- Invalid channel events should be skipped or rejected
- `skipped_event_count` should increase
- Invalid channel should not appear in final KPI output

### Actual Result
- `linkedin_ads` was processed successfully
- `skipped_event_count = 0`
- `channel_breakdown` contains `linkedin_ads`

### Severity
High

### Status
Open

---

## Defect 2: Duplicate event_id values are double-counted

### Defect ID
DEF-002

### Title
Engine does not deduplicate duplicate event IDs

### Related File
- `datasets/edge_cases/duplicate_event_case.json`
- `reports/duplicate_event_case_actual.json`

### Description
The dataset intentionally contained duplicate `event_id` values.
Expected behavior was that duplicate events should be ignored or deduplicated.
Actual behavior showed that both events were counted.

### Expected Result
- Duplicate event should not be counted twice
- Click count should remain 1
- Spend should remain 300

### Actual Result
- Click count became 2
- Total spend became 600
- `skipped_event_count = 0`

### Severity
Medium

### Status
Open