# Simulation Mode Guide
## For candidates without LLM API access

If you do not have access to an OpenAI, Anthropic, or similar LLM API key,
you can complete Task A using **Simulation Mode**. This is a fully accepted
submission path — it tests the same core skill, which is prompt engineering
and output validation.

---

## What changes in simulation mode

| Step | API Mode | Simulation Mode |
|------|----------|-----------------|
| Prompt design | You write it in Python | You write it in a `.txt` file |
| LLM call | `openai.chat.completions.create(...)` | You run the prompt manually on ChatGPT.com or Claude.ai |
| Raw output | Captured programmatically | You paste/save the response to a `.txt` file |
| Parsing + validation | Identical | Identical |
| Determinism | Achieved via `temperature=0` + seed | Achieved by saving the output file and not re-running |

**The prompt is still your primary deliverable.** Whether the API call is made
by your Python script or by you copying a prompt into a browser makes no
difference to whether the prompt is well-engineered.

---

## Step-by-step instructions

### Step 1 — Design your prompt template

Write your prompt in a file called `prompt_templates.py`. Structure it so
it is parameterisable — the scenario text is a variable, not hardcoded.

```python
# prompt_templates.py

SCENARIO_PROMPT_TEMPLATE = """
You are a test data generator for a B2B marketing analytics platform.
Your task is to generate a realistic synthetic dataset of campaign events
based on the scenario description below.

SCENARIO:
{scenario_text}

OUTPUT REQUIREMENTS:
- Return ONLY valid JSON. No explanation, no markdown, no code fences.
- The JSON must be a single object with two keys: "metadata" and "events"
- Each event in "events" must have EXACTLY these fields:
  event_id (string), client_id (string), campaign_id (string),
  channel (must be "google_ads" or "meta_ads" — no other values),
  event_type (must be "IMPRESSION", "CLICK", or "CONVERSION" — no other values),
  spend_usd (number >= 0), revenue_usd (number >= 0),
  timestamp (ISO 8601 string, format: "2025-01-DDTHH:MM:SSZ"),
  budget_usd (number > 0, same value for all events of the same client)

CONSTRAINTS:
- Generate at least 80 events
- All timestamps must fall within January 2025
- IMPRESSION events must have revenue_usd = 0.0
- CLICK events must have revenue_usd = 0.0
- CONVERSION events must have spend_usd = 0.0 and revenue_usd > 0
- client_id values must be consistent slugs (e.g. "acme_corp", not "Acme Corp")
- event_id values must be unique (e.g. "EVT-001", "EVT-002", ...)
- budget_usd must be the same value for ALL events belonging to the same client

OUTPUT FORMAT — start your response with {{ and end with }}:
"""

def build_prompt(scenario_text: str) -> str:
    return SCENARIO_PROMPT_TEMPLATE.format(scenario_text=scenario_text.strip())
```

### Step 2 — Run the prompt manually

1. Open [chat.openai.com](https://chat.openai.com) or [claude.ai](https://claude.ai)
2. In your Python script, call `build_prompt(scenario_text)` and **print the result**
3. Copy the printed prompt and paste it into the chat interface
4. Copy the full JSON response

### Step 3 — Save the raw response

Save the LLM's response exactly as returned (do not edit it) to a file:

```
raw_llm_output/
  scenario1_raw.txt    ← paste the full LLM response here
  scenario2_raw.txt
  scenario3_raw.txt
  ec1_raw.txt          ← edge cases too
  ...
```

### Step 4 — Write `generate_dataset.py` with a `--simulate` flag

Your generator script must support both modes:

```python
# generate_dataset.py  (simulation mode excerpt)

import argparse
import json
import sys
from pathlib import Path
from prompt_templates import build_prompt
import jsonschema

# Load schema for validation
with open("event_schema.json") as f:
    EVENT_SCHEMA = json.load(f)


def call_llm_api(prompt: str) -> str:
    """Make a real LLM API call. Implement this if you have API access."""
    raise NotImplementedError("API mode not configured — use --simulate")


def load_simulated_response(raw_file: str) -> str:
    """Load a pre-saved LLM response from file."""
    path = Path(raw_file)
    if not path.exists():
        raise FileNotFoundError(
            f"Simulated response file not found: {raw_file}\n"
            "Run the prompt manually and save the LLM response to this file."
        )
    return path.read_text(encoding="utf-8").strip()


def parse_and_validate(raw_response: str) -> dict:
    """
    Parse JSON from LLM response and validate against event_schema.json.
    Raises ValueError with a clear message if validation fails.
    """
    # Strip any accidental markdown code fences the LLM may have added
    cleaned = raw_response.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        cleaned = "\n".join(lines[1:-1]) if lines[-1] == "```" else "\n".join(lines[1:])

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM output is not valid JSON: {e}\nRaw output:\n{cleaned[:500]}")

    try:
        jsonschema.validate(instance=data, schema=EVENT_SCHEMA)
    except jsonschema.ValidationError as e:
        raise ValueError(f"Schema validation failed: {e.message}\nPath: {list(e.path)}")

    return data


def generate(scenario_text: str, output_file: str,
             simulate: bool = False, raw_file: str = None) -> dict:
    """
    Main generation function. Returns the validated dataset dict.
    """
    prompt = build_prompt(scenario_text)
    print(f"\n{'='*60}")
    print("PROMPT (copy this if using simulation mode):")
    print('='*60)
    print(prompt)
    print('='*60 + "\n")

    if simulate:
        if not raw_file:
            raise ValueError("--simulate requires --raw-file to specify the saved LLM response")
        print(f"[SIMULATE MODE] Loading response from: {raw_file}")
        raw_response = load_simulated_response(raw_file)
    else:
        print("[API MODE] Calling LLM API...")
        raw_response = call_llm_api(prompt)

    print("Parsing and validating LLM output...")
    dataset = parse_and_validate(raw_response)

    events = dataset.get("events", dataset) if isinstance(dataset, dict) else dataset
    print(f"Validation passed. {len(events)} event(s) generated.")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)
    print(f"Dataset saved to: {output_file}")

    return dataset


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Genesis Campaign Event Dataset Generator")
    parser.add_argument("--scenario",    required=True, help="Scenario description text")
    parser.add_argument("--output",      required=True, help="Output JSON file path")
    parser.add_argument("--simulate",    action="store_true",
                        help="Use simulation mode — load LLM response from file instead of API")
    parser.add_argument("--raw-file",    default=None,
                        help="Path to saved LLM response file (required with --simulate)")
    args = parser.parse_args()

    generate(
        scenario_text=args.scenario,
        output_file=args.output,
        simulate=args.simulate,
        raw_file=args.raw_file,
    )
```

### Step 5 — Run in simulation mode

```bash
# First, print the prompt for scenario 1:
python generate_dataset.py \
  --scenario "Acme Corp runs Google Ads and Meta Ads for the full month of January 2025..." \
  --output scenario1.json \
  --simulate \
  --raw-file raw_llm_output/scenario1_raw.txt
```

If `scenario1_raw.txt` does not exist yet, the script will print the prompt
for you to copy, then exit with a clear error. Paste the prompt into ChatGPT
or Claude, save the response, then re-run.

---

## What the AI Usage Log must show for simulation mode

Because your LLM interaction is manual, the AI Usage Log becomes more
important, not less. It must include:

1. **The full prompt** you used for each scenario (verbatim — copy from
   `prompt_templates.py`)
2. **Screenshots or paste** of at least one complete LLM response before
   and after parsing
3. **At least one validation failure** — a case where the LLM returned
   something that failed `parse_and_validate()`, what the error was,
   and what you changed in the prompt to fix it
4. **Iteration history** for at least one prompt — your first attempt,
   what was wrong with the output, the revised prompt, the better output
5. **Which raw response files** map to which scenarios

---

## What does NOT change in simulation mode

- You still need 3 scenario datasets + 5 edge case datasets (8 total)
- The `parse_and_validate()` function must still validate against `event_schema.json`
- The retry logic (if validation fails, adjust and retry) still applies
- All other deliverables (compare_results.py, golden expectations, test report,
  defect log, golden dataset strategy) are identical

---

## Simulation mode and determinism

In API mode, determinism is achieved with `temperature=0`. In simulation mode,
determinism is achieved by saving the response file and committing it to the repo.

**Add all `raw_llm_output/*.txt` files to your repository.** This is your
evidence that the dataset came from a real LLM interaction, not from hand-written
JSON. A dataset submitted with no raw response file cannot be verified.

---

## Quick-start checklist

- [ ] `prompt_templates.py` written with parameterisable template
- [ ] `generate_dataset.py` has `--simulate` and `--raw-file` flags
- [ ] `raw_llm_output/` directory created
- [ ] For each scenario: prompt printed, pasted into LLM, response saved to raw file
- [ ] `parse_and_validate()` catches at least one schema error (document it)
- [ ] All 8 raw response files committed to repo
- [ ] AI Usage Log documents prompt iterations and one failure case
