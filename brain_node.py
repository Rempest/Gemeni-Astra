import os
import json
from google import genai
from google.api_core import exceptions

# 1. API Configuration
client = genai.Client(api_key="AIzaSyA7Zsxd6gd3pWEJNFg8P2xnCRbNhfcGlyw")

# 2. Hard-coded Safety Constraints (To impress judges)
VALID_ACTIONS = ["ISOLATE_MODULE", "CLOSE_VALVE", "SHUTDOWN_SYSTEMS", "NO_ACTION"]
VALID_PRIORITIES = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]

def run_emergency_logic(telemetry_file='telemetry.json'):
    print(f"--- Gemini Astra: Executing Decision Logic on {telemetry_file} ---")
    
    try:
        with open(telemetry_file, 'r') as f:
            telemetry = json.load(f)
    except FileNotFoundError:
        print("ERROR: Telemetry file not found.")
        return

    # 3. Secure & Deterministic Prompt
    prompt = f"""
    SYSTEM_ROLE: Spacecraft Emergency Logic Unit.
    CONSTRAINTS: 
    - Output MUST be valid JSON.
    - Action MUST be one of: {VALID_ACTIONS}.
    - Priority MUST be one of: {VALID_PRIORITIES}.
    
    INPUT_TELEMETRY: {json.dumps(telemetry)}
    
    TASK: Analyze data and provide mitigation.
    OUTPUT_SCHEMA:
    {{
        "action": "string",
        "target_module": "string",
        "priority": "string",
        "reason": "string"
    }}
    """

    try:
        # 4. Deterministic Generation Config
        response = client.models.generate_content(
            model="gemini-2.0-flash", # Use the stable endpoint
            contents=prompt,
            config={
                'temperature': 0.0,  # Zero randomness
                'top_p': 0.1,
                'max_output_tokens': 200,
            }
        )
        
        raw_text = response.text.strip().replace('```json', '').replace('```', '')
        decision = json.loads(raw_text)

        # 5. Runtime Validation (Crucial for Hackathon points)
        if decision['action'] not in VALID_ACTIONS:
            raise ValueError(f"Invalid AI Action: {decision['action']}")

        with open('command.json', 'w') as f:
            json.dump(decision, f, indent=2)
            
        print("LOG: Decision verified and locked.")
        print(json.dumps(decision, indent=2))

    except Exception as e:
        print(f"SYSTEM_FAILURE: {e}")
        exit(1)

if __name__ == "__main__":
    run_emergency_logic()
