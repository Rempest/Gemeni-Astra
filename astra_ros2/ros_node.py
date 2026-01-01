#!/usr/bin/env python3
"""
SpaceROS Interface for Gemini-Astra
Publishes telemetry and forwards AI commands.
Fully integrated with telemetry_cases and brain_node.py
"""

import os
import json
import time
from pathlib import Path
from subprocess import run, PIPE

class SpaceROSInterface:
    """
    Space ROS / ROS 2 wrapper for the Astra satellite.
    Publishes telemetry and forwards AI-generated commands.
    """

    def __init__(self, telemetry_dir="telemetry_cases"):
        self.node_name = "/astra_mission_control"
        self.telemetry_topic = "/telemetry/status"
        self.telemetry_dir = Path(telemetry_dir)
        self.scenarios = list(self.telemetry_dir.glob("*.json"))
        if not self.scenarios:
            raise FileNotFoundError(f"No telemetry scenarios found in {self.telemetry_dir}")
        print(f"✅ [SpaceROS] Node {self.node_name} initialized. {len(self.scenarios)} scenarios loaded.")

    def publish_data(self, telemetry_path):
        """
        Publishes telemetry JSON to ROS topic (simulated).
        """
        with open(telemetry_path, "r") as f:
            telemetry_data = json.load(f)
        print(f"📡 [SpaceROS] Publishing to {self.telemetry_topic}: {telemetry_data}")
        return telemetry_data

    def run_ai_pipeline(self, telemetry_path):
        """
        Calls brain_node.py with selected telemetry and generates command.json
        """
        print(f"🧠 [SpaceROS] Sending telemetry to Gemini AI...")
        cmd = ["python3", "brain_node.py", "--telemetry", str(telemetry_path)]
        result = run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ [SpaceROS] Error running brain_node.py:\n{result.stderr}")
            return None
        print("✅ [SpaceROS] AI decision generated successfully.")
        return "command.json"

    def bridge_to_fprime(self, command_file):
        """
        Simulates forwarding a command to F' flight software.
        """
        if not os.path.exists(command_file):
            print(f"❌ [SpaceROS] Command file {command_file} not found")
            return
        with open(command_file, "r") as f:
            command_data = json.load(f)
        print(f"⚙️ [SpaceROS] Bridging command to F' Core: {command_data}")
        time.sleep(0.1)  # simulated network latency
        return command_data


if __name__ == "__main__":
    # Select a scenario automatically for demo purposes
    ros_node = SpaceROSInterface()
    for scenario in ros_node.scenarios:
        print(f"\n--- Running Scenario: {scenario.name} ---")
        telemetry = ros_node.publish_data(scenario)
        command_file = ros_node.run_ai_pipeline(scenario)
        ros_node.bridge_to_fprime(command_file)
        time.sleep(1)  # small delay between scenarios
