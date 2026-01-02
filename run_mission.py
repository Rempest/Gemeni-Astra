import time
from simulator.simulator import SpaceSimulator

MAX_STEPS = 10
LOOP_DELAY = 1.5  # seconds

def is_mission_resolved(state):
    telemetry = state["telemetry"]
    
    if telemetry["status"] in ["OPERATIONAL", "RECOVERING"]:
        if telemetry.get("cpu_temperature", 0) < 80:
            return True
    return False


def is_critical_failure(state):
    return state["telemetry"]["status"] == "CRITICAL"


def run_autonomous_mission_loop(scenario_file):
    sim = SpaceSimulator()
    state = sim.load_scenario(scenario_file)

    print(f"\n🚀 Mission started: {scenario_file}")

    for step in range(1, MAX_STEPS + 1):
        print(f"\n🔁 Mission Step {step}")

        # 1. SENSE
        telemetry = state["telemetry"]
        print(f"📡 Telemetry: CPU={telemetry.get('cpu_temperature')} | Power={telemetry.get('power_output')} | Status={telemetry['status']}")

        # 2. THINK (Gemini stub)
        if telemetry.get("cpu_temperature", 0) > 90:
            ai_action = "ACTIVATE_COOLING"
            reason = "CPU temperature above safe threshold"
        elif telemetry.get("power_output", 100) < 50:
            ai_action = "REDEPLOY_PANELS"
            reason = "Insufficient power generation"
        else:
            ai_action = "NO_ACTION"
            reason = "System nominal"

        print(f"🧠 AI Decision: {ai_action}")
        print(f"📝 Reason: {reason}")

        # 3. ACT
        if ai_action != "NO_ACTION":
            state = sim.apply_ai_command(ai_action)

        # 4. VERIFY
        if is_mission_resolved(state):
            print("✅ Mission resolved successfully")
            return {
                "result": "SUCCESS",
                "steps": step,
                "final_state": state
            }

        if is_critical_failure(state):
            print("🚨 Critical failure detected!")
            return {
                "result": "FAILURE",
                "steps": step,
                "final_state": state
            }

        time.sleep(LOOP_DELAY)

    print("⏱ Mission timeout reached")
    return {
        "result": "TIMEOUT",
        "steps": MAX_STEPS,
        "final_state": state
    }


if __name__ == "__main__":
    result = run_autonomous_mission_loop("simulator/scenarios/thermal_overheat.json")
    print("\n📊 Mission Outcome:", result["result"])
