#!/usr/bin/env python3
"""
Gemini-Astra Brain Node
Autonomous AI decision-making for satellite telemetry
"""

import os
import sys
import json
import logging
from google import genai
from google.genai import types

# ----------------------------------------
# Python version check
# ----------------------------------------
if sys.version_info < (3, 12):
    raise RuntimeError("Python 3.12 or higher required")

# ----------------------------------------
# Logging setup
# ----------------------------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# ----------------------------------------
# Initialize Gemini Client securely
# ----------------------------------------
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise EnvironmentError("Please set the GOOGLE_API_KEY environment variable")

client = genai.Client(api_key=API_KEY, http_options={"api_version": "v1beta"})
logging.info("✅ Gemini client initialized")

# ----------------------------------------
# Valid keys for output validation
# ----------------------------------------
VALID_KEYS = {"status", "priority_actions", "risk_level"}

# ----------------------------------------
# Main decision function
# ----------------------------------------
def get_astral_decision(telemetry_json: str) -> dict:
    """
    Sends telemetry to Gemini and returns a validated decision dictionary.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are the Astra satellite AI pilot. "
                    "Analyze telemetry and return ONLY JSON with these exact fields: "
                    "'status' (string), 'priority_actions' (list of strings), 'risk_level' (integer 1-10)."
                ),
                response_mime_type="application/json",
                temperature=0  # deterministic output
            ),
            contents=f"Current telemetry: {telemetry_json}"
        )

        # Clean JSON artifacts
        clean_json = response.text.replace("```json", "").replace("```", "").strip()
        result = json.loads(clean_json)

        # Validate keys
        if not VALID_KEYS.issubset(result.keys()):
            raise ValueError(f"Invalid response keys: {result.keys()}")

        return result

    except Exception as e:
        logging.error(f"Error generating AI decision: {e}")
        return {
            "error": str(e),
            "raw_response": getattr(response, "text", "No response")
        }

# ----------------------------------------
# CLI / test mode
# ----------------------------------------
if __name__ == "__main__":
    # Check if telemetry file is passed
    import argparse

    parser = argparse.ArgumentParser(description="Gemini-Astra Brain Node")
    parser.add_argument(
        "--telemetry",
        type=str,
        default=None,
        help="Path to telemetry JSON file (optional)"
    )
    args = parser.parse_args()

    # Load telemetry
    if args.telemetry:
        if not os.path.isfile(args.telemetry):
            logging.error(f"Telemetry file {args.telemetry} not found")
            sys.exit(1)
        with open(args.telemetry, "r") as f:
            telemetry_data = json.load(f)
    else:
        # Default test telemetry
        telemetry_data = {
            "oxygen": "dropping",
            "power": "12%",
            "orientation": "unstable",
            "temp": "45C"
        }

    logging.info("🚀 Sending telemetry to Gemini AI core...")
    decision = get_astral_decision(json.dumps(telemetry_data))

    # Save decision to command.json
    with open("command.json", "w") as f:
        json.dump(decision, f, indent=4)

    logging.info("✅ Decision saved to command.json")
    print("\n--- 🛰️ GEMINI 3 MISSION CONTROL DECISION ---")
    print(json.dumps(decision, indent=4))

