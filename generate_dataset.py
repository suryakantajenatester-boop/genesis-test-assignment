import argparse
import json
from pathlib import Path

import jsonschema

from prompt_templates import build_prompt


def load_schema() -> dict:
    with open("event_schema.json", "r", encoding="utf-8") as f:
        return json.load(f)


EVENT_SCHEMA = load_schema()


def load_simulated_response(raw_file: str) -> str:
    path = Path(raw_file)
    if not path.exists():
        raise FileNotFoundError(
            f"Simulated response file not found: {raw_file}\n"
            "Create the raw file by pasting the LLM response into it."
        )
    return path.read_text(encoding="utf-8").strip()


def clean_raw_response(raw_response: str) -> str:
    cleaned = raw_response.strip()

    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if len(lines) >= 3 and lines[-1].strip() == "```":
            cleaned = "\n".join(lines[1:-1]).strip()
        else:
            cleaned = "\n".join(lines[1:]).strip()

    return cleaned


def parse_and_validate(raw_response: str) -> dict:
    cleaned = clean_raw_response(raw_response)

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM output is not valid JSON: {e}")

    try:
        jsonschema.validate(instance=data, schema=EVENT_SCHEMA)
    except jsonschema.ValidationError as e:
        path_str = " -> ".join(str(p) for p in e.path)
        raise ValueError(f"Schema validation failed: {e.message} | Path: {path_str}")

    return data


def save_json(data: dict, output_file: str) -> None:
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def generate(scenario_text: str, output_file: str, raw_file: str) -> dict:
    prompt = build_prompt(scenario_text)

    print("\n" + "=" * 80)
    print("PROMPT FOR MANUAL SIMULATION")
    print("=" * 80)
    print(prompt)
    print("=" * 80 + "\n")

    raw_response = load_simulated_response(raw_file)
    dataset = parse_and_validate(raw_response)
    save_json(dataset, output_file)

    events = dataset["events"] if isinstance(dataset, dict) else dataset
    print(f"Validation passed. {len(events)} event(s) saved to {output_file}")
    return dataset


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Genesis dataset generator (simulation mode)")
    parser.add_argument("--scenario", required=True, help="Scenario description text")
    parser.add_argument("--output", required=True, help="Output JSON file path")
    parser.add_argument("--raw-file", required=True, help="Saved raw LLM response file path")
    args = parser.parse_args()

    generate(
        scenario_text=args.scenario,
        output_file=args.output,
        raw_file=args.raw_file,
    )