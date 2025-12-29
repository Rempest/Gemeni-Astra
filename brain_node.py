import os
import json
from google import genai
from google.genai import types

# Initialize client
API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY, http_options={"api_version": "v1beta"})

def get_astral_decision(telemetry):
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            config=types.GenerateContentConfig(
               system_instruction=(
                    "You are the Astra satellite AI pilot. "
                    "Analyze telemetry and return ONLY JSON with these exact fields: "
                    "'status' (string), 'priority_actions' (list of strings), 'risk_level' (integer 1-10)."
                ),
                response_mime_type="application/json"
            ),
            contents=f"Current telemetry: {telemetry}"
        )

        # Clean possible Markdown artifacts from the response
        clean_json = (
            response.text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )
        return json.loads(clean_json)

    except Exception as e:
        return {
            "error": str(e),
            "raw_response": getattr(response, "text", "No response")
        }

if __name__ == "__main__":
    # Test emergency scenario
    test_telemetry = {
        "oxygen": "dropping",
        "power": "12%",
        "orientation": "unstable",
        "temp": "45C"
    }

    print("🚀 Connecting to Gemini 3 Core...")
    decision = get_astral_decision(json.dumps(test_telemetry))

    print("\n--- 🛰️ GEMINI 3 MISSION CONTROL DECISION ---")
    print(json.dumps(decision, indent=4))

