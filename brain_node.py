import os
import json
from google import genai
from google.genai import types

# Используем v1beta для доступа к экспериментальной Gemini 3
API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY, http_options={'api_version': 'v1beta'})

def get_astral_decision(telemetry):
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            config=types.GenerateContentConfig(
                system_instruction="You are the Astra satellite AI. Analyze telemetry and return ONLY JSON.",
                response_mime_type="application/json"
            ),
            contents=f"Current telemetry: {telemetry}"
        )
        return json.loads(response.text)
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Тестовая аварийная ситуация
    test_telemetry = "Critical: Oxygen level dropping, Power: 12%, Orientation: Unstable"
    print("Connecting to Gemini 3 Core...")
    decision = get_astral_decision(test_telemetry)
    print("\n--- GEMINI 3 DECISION ---")
    print(json.dumps(decision, indent=4))
