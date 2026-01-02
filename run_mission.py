import os
import json
import time
import datetime
from simulator.simulator import SpaceSimulator
from google import genai  # Gemini 3 AI

MAX_STEPS = 10
LOOP_DELAY = 1.5  # seconds


def is_mission_resolved(state):
    """Check if the mission has been successfully completed."""
    telemetry = state["telemetry"]
    if telemetry["status"] in ["OPERATIONAL", "RECOVERING"]:
        if telemetry.get("cpu_temperature", 0) < 80:
            return True
    return False


def is_critical_failure(state):
    """Check if a critical system failure occurred."""
    return state["telemetry"]["status"] == "CRITICAL"


def real_gemini_decision(state):
    """Call the real Gemini 3 AI for decision making."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ ERROR: API key not found! Set it with export GOOGLE_API_KEY='...'")
        return {"action": "NO_ACTION", "reason": "No API Key", "confidence": 0}

    client = genai.Client(api_key=api_key)

    # Prompt instructs AI to act as the onboard computer
    prompt = f"""
    You are the ASTRA-01 Satellite AI. Analyze this telemetry and choose the best action.
    Return ONLY a JSON object: {{"action": "...", "reason": "...", "confidence": ...}}

    Actions: 'ACTIVATE_COOLING', 'REDEPLOY_PANELS', 'NO_ACTION'.

    Current State: {json.dumps(state)}
    """

    try:
        response = client.models.generate_content(
            model="gemini-3.0",
            contents=prompt
        )
        clean_json = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_json)
    except Exception as e:
        print(f"⚠️ AI Error: {e}. Falling back to safe mode.")
        return {"action": "NO_ACTION", "reason": "AI Error", "confidence": 0}


def run_autonomous_mission_loop(scenario_file):
    """Run the mission loop for a given scenario file."""
    sim = SpaceSimulator()
    state = sim.load_scenario(scenario_file)

    print(f"\n🚀 Starting mission: {scenario_file}")

    mission_log = []

    for step in range(1, MAX_STEPS + 1):
        print(f"\n🔁 Mission Step {step}")

        # 1. SENSE
        telemetry = state["telemetry"]
        print(f"📡 Telemetry: CPU={telemetry.get('cpu_temperature')} | Power={telemetry.get('power_output')} | Status={telemetry['status']}")

        # 2. THINK (Gemini 3)
        ai_decision = real_gemini_decision(state)
        ai_action = ai_decision["action"]
        reason = ai_decision.get("reason", "N/A")
        confidence = ai_decision.get("confidence", 1.0)

        print(f"🧠 AI Decision: {ai_action} | Reason: {reason} | Confidence: {confidence}")

        # 3. ACT
        if ai_action != "NO_ACTION":
            state = sim.apply_ai_command(ai_action)

        # 4. VERIFY
        constraints_ok = sim.check_constraints()  # Full constraints check
        print(f"🛡️ Safety constraints: {'OK' if constraints_ok else 'VIOLATED'}")

        # 5. LOG step with timestamp
        current_time = datetime.datetime.utcnow().isoformat() + "Z"
        mission_status = state["telemetry"]["status"]
        mission_log.append({
            "timestamp": current_time,
            "step": step,
            "action": ai_action,
            "reason": reason,
            "confidence": confidence,
            "constraints_ok": constraints_ok,
            "mission_status": mission_status,
            "telemetry": telemetry
        })

        # Check mission outcome
        if is_mission_resolved(state):
            print("✅ Mission resolved successfully")
            break

        if is_critical_failure(state):
            print("🚨 Critical failure detected!")
            break

        time.sleep(LOOP_DELAY)

    # Save mission log
    log_file = scenario_file.replace(".json", "_mission_log.json")
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(mission_log, f, indent=2)
    print(f"\n📄 Mission log saved: {log_file}")

    # Mission summary
    final_status = state["telemetry"]["status"]
    summary = {
        "scenario": scenario_file,
        "total_steps": step,
        "final_status": final_status,
        "final_cpu_temp": telemetry.get("cpu_temperature"),
        "final_power_output": telemetry.get("power_output"),
        "log_file": log_file
    }
    summary_file = scenario_file.replace(".json", "_mission_summary.json")
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"📄 Mission summary saved: {summary_file}")

    # Determine final result
    if is_mission_resolved(state):
        result = "SUCCESS"
    elif is_critical_failure(state):
        result = "FAILURE"
    else:
        result = "TIMEOUT"

    print(f"🏁 Mission Outcome: {result} | Final Status: {final_status}")
    return {"result": result, "final_state": state, "log_file": log_file, "summary_file": summary_file}


if __name__ == "__main__":
    # Run both scenarios sequentially
    run_autonomous_mission_loop("simulator/scenarios/thermal_overheat.json")
    run_autonomous_mission_loop("simulator/scenarios/solar_failure.json")

