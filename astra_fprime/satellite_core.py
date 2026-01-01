#!/usr/bin/env python3
"""
NASA F' Component Simulation for Gemini-Astra
Executes AI-generated commands from brain_node.py.
"""

import json
import time
import os

class AstraFPrimeComponent:
    """
    Simulates hardware execution of AI-generated commands.
    """

    def __init__(self):
        self.energy_level = 100
        self.oxygen_system = "STANDBY"
        self.thrusters = "OFF"
        self.status_log = []

    def execute_commands(self, command_file="command.json"):
        if not os.path.exists(command_file):
            print(f"❌ [F' Core] Command file {command_file} not found")
            return

        with open(command_file, "r") as f:
            ai_decision = json.load(f)

        print(f"\n[F' Core] Commands received from Gemini AI (Status: {ai_decision.get('status','UNKNOWN')})")
        actions = ai_decision.get("priority_actions", [])

        for action in actions:
            time.sleep(1)  # simulate hardware latency
            action_lower = action.lower()
            if "oxygen" in action_lower:
                self.oxygen_system = "ACTIVE"
                msg = f"EXECUTED: {action} -> Life Support: {self.oxygen_system}"
            elif "power" in action_lower or "low-power" in action_lower:
                self.energy_level = max(self.energy_level - 10, 0)
                msg = f"EXECUTED: {action} -> Energy Level: {self.energy_level}%"
            elif "thrusters" in action_lower or "orientation" in action_lower:
                self.thrusters = "STABILIZING"
                msg = f"EXECUTED: {action} -> Thrusters: {self.thrusters}"
            else:
                msg = f"EXECUTED: {action} -> General system update"
            print(f"✔️ {msg}")
            self.status_log.append(msg)

        print("\n[F' Core] Mission Execution Complete.\n")

if __name__ == "__main__":
    # Auto-load latest command.json if exists
    fprime = AstraFPrimeComponent()
    command_file = "command.json"
    if os.path.exists(command_file):
        fprime.execute_commands(command_file)
    else:
        print("⚠️ [F' Core] No command.json found. Run brain_node.py first or use ros_node.py pipeline.")

