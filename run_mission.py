import json
from simulator.simulator import SpaceSimulator


def mock_gemini_decision(state: dict) -> dict:
    """
    Mocked Gemini decision logic.
    Replaced by real Gemini API call in production.
    """
    telemetry = state.get("telemetry", {})
    thermal = telemetry.get("thermal", {})

    # Thermal reasoning
    if thermal.get("cpu_temperature", 0) > state.get("constraints", {}).get("max_cpu_temperature", 999):
        return {
            "action": "ACTIVATE_COOLING",
            "reason": "CPU temperature exceeds safe thermal envelope",
            "confidence": 0.91
        }

    # Power reasoning
    if telemetry.get("power_output", 100) < state.get("constraints", {}).get("min_power_output", 0):
        return {
            "action": "REDEPLOY_PANELS",
            "reason": "Power output below mission requirement",
            "confidence": 0.88
        }

    return {
        "action": "NO_ACTION",
        "reason": "System operating within nominal parameters",
        "confidence": 0.99
    }


def run_autonomous_mission(scenario_file: str, max_steps: int = 3) -> dict:
    sim = SpaceSimulator()
    mission_log = []

    print(f"\n🚀 Starting autonomous mission: {scenario_file}")

    # 1. Load scenario
    state = sim.load_scenario(scenario_file)
    print(f"📍 Initial system status: {state['telemetry']['status']}")

    # 2. Mission loop
    for step in range(1, max_steps + 1):
        print(f"\n🔁 Mission step {step}")

        ai_decision = mock_gemini_decision(state)
        print(f"🤖 AI Action: {ai_decision['action']}")
        print(f"📝 Reason: {ai_decision['reason']}")

        if ai_decision["action"] == "NO_ACTION":
            print("✅ No corrective action required.")
            break

        # 3. Apply command
        state = sim.apply_ai_command(ai_decision["action"])

        # 4. Safety validation
        constraints_ok = sim.check_constraints()
        print(f"🛡️ Safety constraints: {'OK' if constraints_ok else 'VIOLATED'}")

        mission_log.append({
            "step": step,
            "action": ai_decision["action"],
            "confidence": ai_decision["confidence"],
            "constraints_ok": constraints_ok,
            "system_status": state["telemetry"]["status"]
        })

        # 5. Fallback strategy
        if not constraints_ok:
            print("⚠️ Entering degraded safe mode")
            state = sim.apply_ai_command("ENTER_DEGRADED_MODE")
            break

    # 6. Save mission log
    with open("mission_log.json", "w", encoding="utf-8") as f:
        json.dump(mission_log, f, indent=2)

    print("\n📄 Mission log saved to mission_log.json")
    print(f"🏁 Final system status: {state['telemetry']['status']}")

    return state


if __name__ == "__main__":
    run_autonomous_mission("simulator/scenarios/thermal_overheat.json")
    run_autonomous_mission("simulator/scenarios/solar_failure.json")
