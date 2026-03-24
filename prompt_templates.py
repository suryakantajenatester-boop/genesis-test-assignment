SCENARIO_PROMPT_TEMPLATE = """
You are generating synthetic campaign event data for a validation assignment.

Your output will be parsed by Python and validated against a strict JSON schema.

SCENARIO:
{scenario_text}

NON-NEGOTIABLE RULES:
- Return ONLY one valid JSON object.
- No markdown fences.
- No explanation text.
- No comments.
- No trailing commas.
- All monetary values must be JSON numbers, not strings.
- event_count must be a JSON integer.
- budget_usd, spend_usd, and revenue_usd must be JSON numbers.
- Do not include currency symbols in numeric fields.
- Do not include commas inside numeric fields.
- Do not include quotes around numeric fields.
- Do not invent missing digits or claim the scenario omitted digits.
- Use the numbers exactly as written in the scenario:
  - monthly budget = 10000
  - total spend = 8200
  - total impressions = 45000
  - total clicks = 1800
  - total conversions = 72
  - average revenue per conversion = 180

TOP LEVEL FORMAT:
{{
  "metadata": {{ ... }},
  "events": [ ... ]
}}

EVENT OBJECT RULES:
Each event must contain EXACTLY these 9 fields:
- event_id
- client_id
- campaign_id
- channel
- event_type
- spend_usd
- revenue_usd
- timestamp
- budget_usd

VALID VALUES:
- client_id must be "acme_corp"
- channel must be "google_ads" or "meta_ads"
- event_type must be "IMPRESSION", "CLICK", or "CONVERSION"
- budget_usd must be 10000 on every event
- timestamps must be in March 2024 only
- timestamps must be on working days only
- timestamps must be between 08:00:00Z and 20:00:00Z inclusive

BUSINESS DISTRIBUTION RULES:
- Total spend across all events must equal 8200.00
- Roughly 70 percent of spend must be on google_ads
- Roughly 30 percent of spend must be on meta_ads
- Total revenue across conversion events should be 72 * 180 = 12960
- IMPRESSION events must have revenue_usd = 0
- CLICK events must have revenue_usd = 0
- CONVERSION events must have spend_usd = 0

COMPACT DATASET RULES:
- Keep the dataset compact
- Use exactly 12 events total
- Use 4 IMPRESSION events
- Use 4 CLICK events
- Use 4 CONVERSION events
- Aggregate values realistically across March working days

EXACT AGGREGATE TOTALS ACROSS EVENTS:
- Sum of IMPRESSION event volumes implied by the dataset must represent 45000 impressions in total
- Sum of CLICK event volumes implied by the dataset must represent 1800 clicks in total
- Sum of CONVERSION event volumes implied by the dataset must represent 72 conversions in total

IMPORTANT MODELING NOTE:
Because the schema does not have explicit count fields for impressions/clicks/conversions,
represent the dataset as aggregated financial event buckets only.
Use the metadata notes field to state:
"Represents aggregated event buckets for a March 2024 scenario with 45000 impressions, 1800 clicks, and 72 conversions."

METADATA RULES:
metadata must contain:
- scenario_id
- generation_timestamp
- llm_model_used
- generation_mode
- prompt_template_version
- event_count
- client_ids_present
- notes

METADATA VALUES:
- scenario_id must be "acme_corp_march_2024"
- generation_mode must be "simulated"
- prompt_template_version must be "v3.0"
- event_count must be 12
- client_ids_present must be ["acme_corp"]

FINAL CHECK:
- Output must be valid JSON
- All numeric fields must be numbers
- Exactly 12 events
- No extra keys anywhere inside events
- No unsupported assumptions

Return only the JSON object.
"""

def build_prompt(scenario_text: str) -> str:
    return SCENARIO_PROMPT_TEMPLATE.format(scenario_text=scenario_text.strip())