"""
campaign_engine.py — Genesis Group Campaign KPI Computation Module
Version: 1.0.0

Reads a list of campaign events and computes aggregated KPIs per client.

Usage:
    python campaign_engine.py --input events.json --output results.json
    python campaign_engine.py --input events.json            # prints to stdout
    import campaign_engine; results = campaign_engine.compute(events)

NOTE TO QA TEAM:
    This module contains known issues discovered during development.
    Your test suite should find them — they are not documented here
    deliberately. That is the point of the assignment.
"""

import json
import sys
import argparse
import logging
from collections import defaultdict
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  [%(levelname)s]  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("campaign_engine")

VALID_EVENT_TYPES = {"IMPRESSION", "CLICK", "CONVERSION"}
VALID_CHANNELS    = {"google_ads", "meta_ads"}


# ── Input validation ─────────────────────────────────────────────────────────

def _validate_event(event: dict, index: int) -> list[str]:
    """
    Returns a list of validation error strings for a single event dict.
    Empty list means the event is valid.
    """
    errors = []
    required = ["event_id", "client_id", "campaign_id", "channel",
                 "event_type", "spend_usd", "revenue_usd", "timestamp", "budget_usd"]
    for field in required:
        if field not in event:
            errors.append(f"Event[{index}] missing required field: '{field}'")

    if "event_type" in event and event["event_type"] not in VALID_EVENT_TYPES:
        errors.append(
            f"Event[{index}] unknown event_type: '{event['event_type']}' "
            f"(valid: {VALID_EVENT_TYPES})"
        )

    if "channel" in event and event["channel"] not in VALID_CHANNELS:
        logger.warning(
            "Event[%d] unknown channel '%s' — will be grouped as 'other'",
            index, event["channel"]
        )

    for numeric_field in ["spend_usd", "revenue_usd", "budget_usd"]:
        if numeric_field in event:
            try:
                float(event[numeric_field])
            except (TypeError, ValueError):
                errors.append(
                    f"Event[{index}] field '{numeric_field}' is not numeric: "
                    f"'{event[numeric_field]}'"
                )

    return errors


# ── Core computation ─────────────────────────────────────────────────────────

def compute(events: list[dict]) -> list[dict]:
    """
    Given a flat list of campaign event dicts, returns a list of per-client
    KPI summary dicts.

    Skips malformed events and logs each skipped event — does not crash.
    """
    if not isinstance(events, list):
        raise TypeError(f"Expected list of events, got {type(events).__name__}")

    # ── Accumulate per-client per-channel totals ──────────────────────────────
    clients: dict[str, dict] = defaultdict(lambda: {
        "spend":        0.0,
        "revenue":      0.0,
        "impressions":  0,
        "clicks":       0,
        "conversions":  0,
        "budget_usd":   0.0,   # will be set from first valid event for client
        "budget_set":   False,
        "channels":     defaultdict(lambda: {
            "spend": 0.0, "revenue": 0.0,
            "impressions": 0, "clicks": 0, "conversions": 0
        }),
        "skipped_events": 0,
    })

    for i, event in enumerate(events):
        errors = _validate_event(event, i)
        if errors:
            for err in errors:
                logger.warning("Skipping malformed event — %s", err)
            clients[event.get("client_id", "__unknown__")]["skipped_events"] += 1
            continue

        cid     = event["client_id"]
        etype   = event["event_type"]
        channel = event.get("channel", "other")
        spend   = float(event["spend_usd"])
        revenue = float(event["revenue_usd"])
        budget  = float(event["budget_usd"])

        c  = clients[cid]
        ch = c["channels"][channel]

        # Set budget from first valid event for this client
        if not c["budget_set"]:
            c["budget_usd"]  = budget
            c["budget_set"]  = True

        c["spend"]   += spend
        c["revenue"] += revenue
        ch["spend"]  += spend
        ch["revenue"] += revenue

        if etype == "IMPRESSION":
            c["impressions"]  += 1
            ch["impressions"] += 1
        elif etype == "CLICK":
            c["clicks"]  += 1
            ch["clicks"] += 1
        elif etype == "CONVERSION":
            c["conversions"]  += 1
            ch["conversions"] += 1

    # ── Build output records ─────────────────────────────────────────────────
    results = []

    for client_id, c in clients.items():
        if client_id == "__unknown__":
            continue

        spend       = round(c["spend"],   2)
        revenue     = round(c["revenue"], 2)
        impressions = c["impressions"]
        clicks      = c["clicks"]
        conversions = c["conversions"]
        budget      = c["budget_usd"]

        # ── KPI: ROAS ──────────────────────────────────────────────────────
        # Revenue divided by spend.
        roas = round(revenue / spend, 4) if spend > 0 else 0.0

        # ── KPI: Conversion Rate ───────────────────────────────────────────
        # Percentage of impressions that resulted in a conversion.
        # ⚠ BUG 1: Should be (conversions / clicks) * 100
        #           but uses impression_count as denominator instead.
        #           This produces a wildly different — and wrong — result
        #           in any normal dataset where impressions >> clicks.
        if impressions > 0:
            conversion_rate_pct = round((conversions / impressions) * 100, 2)
        else:
            conversion_rate_pct = 0.0

        # ── KPI: Budget Pacing ─────────────────────────────────────────────
        # How much of the monthly budget has been consumed, expressed as a
        # percentage (0–100+).
        # ⚠ BUG 2: Returns a decimal ratio (0.0–1.0) instead of a percentage
        #           (0.0–100.0). Missing the * 100 multiplication.
        #           EC-3 (100% pacing scenario) will reveal this: expected
        #           100.0, actual 1.0.
        if budget > 0:
            budget_pacing_pct = round(spend / budget, 2)
        else:
            budget_pacing_pct = 0.0

        # ── Channel breakdown ─────────────────────────────────────────────
        channel_breakdown = {}
        for ch_name, ch_data in c["channels"].items():
            ch_spend = round(ch_data["spend"], 2)
            ch_rev   = round(ch_data["revenue"], 2)
            channel_breakdown[ch_name] = {
                "spend_usd":         ch_spend,
                "revenue_usd":       ch_rev,
                "impression_count":  ch_data["impressions"],
                "click_count":       ch_data["clicks"],
                "conversion_count":  ch_data["conversions"],
                "roas":              round(ch_rev / ch_spend, 4) if ch_spend > 0 else 0.0,
            }

        record = {
            "client_id":           client_id,
            "total_spend_usd":     spend,
            "total_revenue_usd":   revenue,
            "impression_count":    impressions,
            "click_count":         clicks,
            "conversion_count":    conversions,
            "roas":                roas,
            "conversion_rate_pct": conversion_rate_pct,
            "budget_usd":          round(budget, 2),
            "budget_pacing_pct":   budget_pacing_pct,
            "channel_breakdown":   channel_breakdown,
            "skipped_event_count": c["skipped_events"],
        }
        results.append(record)

    results.sort(key=lambda r: r["client_id"])
    return results


# ── File I/O helpers ──────────────────────────────────────────────────────────

def load_events(path: str) -> list[dict]:
    """Load events from a JSON file. Handles both bare list and wrapped format."""
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)

    # Support both {"events": [...]} and bare [...]
    if isinstance(raw, dict) and "events" in raw:
        return raw["events"]
    if isinstance(raw, list):
        return raw
    raise ValueError(
        f"Unrecognised JSON structure in '{path}'. "
        "Expected a list of events or an object with an 'events' key."
    )


def save_results(results: list[dict], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    logger.info("Results written to %s  (%d client record(s))", path, len(results))


# ── CLI entry point ───────────────────────────────────────────────────────────

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Campaign KPI Computation Engine — Genesis Group v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python campaign_engine.py --input events.json
  python campaign_engine.py --input events.json --output results.json
  python campaign_engine.py --input scenario1.json --output expected1_actual.json
""",
    )
    parser.add_argument(
        "--input",  "-i", required=True,
        help="Path to input JSON file containing campaign events",
    )
    parser.add_argument(
        "--output", "-o", default=None,
        help="Path to write output JSON (default: print to stdout)",
    )
    parser.add_argument(
        "--pretty", action="store_true", default=True,
        help="Pretty-print JSON output (default: True)",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()

    logger.info("Loading events from: %s", args.input)
    try:
        events = load_events(args.input)
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as exc:
        logger.error("Failed to load input file: %s", exc)
        sys.exit(1)

    logger.info("Processing %d event(s)...", len(events))
    results = compute(events)
    logger.info("Computed KPIs for %d client(s)", len(results))

    output_json = json.dumps(results, indent=2 if args.pretty else None)

    if args.output:
        save_results(results, args.output)
    else:
        print(output_json)


if __name__ == "__main__":
    main()
