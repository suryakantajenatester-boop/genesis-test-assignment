import json
from pathlib import Path

from campaign_engine import compute


def load_json(file_path: str):
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data, file_path: str):
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def main():
    input_file = "datasets/scenario1.json"
    output_file = "reports/report1_actual.json"

    dataset = load_json(input_file)
    actual_output = compute(dataset["events"])

    save_json(actual_output, output_file)
    print(f"Actual engine output saved to {output_file}")


if __name__ == "__main__":
    main()