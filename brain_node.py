import os
import json
from google import genai

# Client Configuration
# Replace 'YOUR_API_KEY_HERE' with your actual Gemini API Key
client = genai.Client(api_key="AIzaSyA7Zsxd6gd3pWEJNFg8P2xnCRbNhfcGlyw")

def run_emergency_logic():
    print("--- Gemini Astra: Decision Engine Starting ---")
    
    # 1. Loading Telemetry Data
    try:
        with open('telemetry.json', 'r') as f:
            telemetry = json.load(f)
        print("LOG: Telemetry data loaded successfully.")
    except Exception as e:
        print(f"ERROR: Failed to load telemetry file: {e}")
        return

    # 2. Constructing System Prompt
    # We force the model to output ONLY valid JSON for machine-to-machine communication
    prompt = f"""
    ROLE: Spacecraft Emergency Autonomy AI (Gemini 3 Core).
    INPUT TELEMETRY (JSON): {json.dumps(telemetry)}
    
    TASK: 
    1. Analyze the telemetry for life-support or power anomalies.
    2. Generate a deterministic mitigation protocol.
    3. Output ONLY a valid JSON object.
    
    JSON SCHEMA REQUIREMENTS:
    - "action": (Specific mechanical or software command)
    - "target_module": (Affected spacecraft component)
    - "priority": (CRITICAL/HIGH/MEDIUM)
    - "reason": (Brief engineering justification)
    
    OUTPUT FORMAT: Strictly JSON. No markdown formatting, no conversational text.
    """

    # 3. Executing Gemini 3 Inference
    try:
        print("LOG: Sending request to Gemini 3 Engine...")
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        
        # Clean response from potential Markdown code blocks
        raw_text = response.text.strip().replace('```json', '').replace('```', '')
        decision = json.loads(raw_text)
        
        # 4. Exporting Command to Output File
        with open('command.json', 'w') as f:
            json.dump(decision, f, indent=2)
            
        print("SUCCESS: Emergency protocol generated and saved to command.json")
        print("AI DECISION OUTPUT:")
        print(json.dumps(decision, indent=2))

    except Exception as e:
        print(f"CRITICAL SYSTEM ERROR: {e}")
        exit(1)

if __name__ == "__main__":
    run_emergency_logic()

