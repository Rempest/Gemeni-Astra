import os
import google.generativeai as genai
from PIL import Image

# 1. AI Configuration
# Replace "YOUR_API_KEY_HERE" with the key you got from Google AI Studio
API_KEY = "YOUR_API_KEY_HERE"
genai.configure(api_key=API_KEY)

def analyze_space_emergency(image_path, telemetry_data):
    """
    Sends visual and text data to Gemini 3 and receives a repair strategy.
    """
    # Using gemini-1.5-flash for low-latency robotic responses
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Load the captured 'emergency' image
    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        return "Error: Image file not found. Please upload emergency.jpg"
    
    # Constructing the Multimodal Prompt
    prompt = f"""
    SYSTEM ROLE: You are the autonomous AI brain of the 'Astra' space repair robot.
    CURRENT TELEMETRY: {telemetry_data}
    
    TASK: 
    1. Analyze the provided image for structural damage.
    2. Compare visual evidence with telemetry data.
    3. Identify the specific failure.
    4. Issue a precise repair command.
    
    OUTPUT FORMAT: Provide your answer in raw JSON format like this:
    {{"failure": "description", "action": "specific_command", "confidence": 0.95}}
    """
    
    # Generate multimodal response
    response = model.generate_content([prompt, img])
    return response.text

# --- Main Logic Loop ---
if __name__ == "__main__":
    print("--- Astra Autonomous Brain Initialized ---")
    
    # Mock data for initial testing
    mock_telemetry = "Voltage: 11.2V (DROP), Thermal: 45C, Comm_Link: Stable"
    image_file = "emergency.jpg"
    
    print(f"Status: Monitoring sensors...")
    print(f"Input: Reading {image_file} and telemetry...")
    
    # UNCOMMENT the lines below once you have added your API KEY and uploaded an image:
    # result = analyze_space_emergency(image_file, mock_telemetry)
    # print("\n[GEMINI LOGIC OUTPUT]:")
    # print(result)
    
    print("\nStatus: Ready for SpaceROS integration.")
