import json
import os
from copy import deepcopy


class SpaceSimulator:
    """
    Lightweight deterministic mission simulator.

    Designed for low-resource environments.
    Simulates satellite state transitions based on AI-generated commands.
    """

    def __init__(self):
        self.current_state = {}
        self.previous_state = {}

    def load_scenario(self, scenario_path: str) -> dict | None:
        """
        Load a mission scenario from a JSON file.

        Args:
            scenario_path (str): Path to scenario JSON file.

        Returns:
            dict | None: Loaded scenario state or None if file not found.
        """
        if not os.path.exists(scenario_path):
            return None

        with open(scenario_path, "r", encoding="utf-8") as f:
            self.current_state = json.load(f)

        self.previous_state = deepcopy(self.current_state)
        return self.current_state

    def apply_ai_command(self, action_code: str) -> dict | None:
        """
        Apply an AI-generated command to the simulated system.

        Args:
            action_code (str): High-level command produced by Gemini
                               (e.g. 'ACTIVATE_COOLING', 'REDEPLOY_PANELS').

        Returns:
            dict | None: Updated system state.
        """
        if not self.current_state:
            return None

        self.previous_state = deepcopy(self.current_state)

        # --- Thermal overheat scenario ---
        if action_code == "ACTIVATE_COOLING":
            self._activate_cooling()

        elif action_code == "ENTER_DEGRADED_MODE":
            self._enter_degraded_mode()

        # --- Solar panel degradation scenario ---
        elif action_code == "REDEPLOY_PANELS":
            self._redeploy_panels()

        # --- Power management ---
        elif action_code == "POWER_SAVE_MODE":
            self._power_save_mode()

        return self.current_state

    # ----------------------------
    # Internal action handlers
    # ----------------------------

    def _activate_cooling(self):
        telemetry = self.current_state.get("telemetry", {})

        telemetry.setdefault("cooling", {})
        telemetry["cooling"]["fan_speed_rpm"] = 3000
        telemetry["cooling"]["fan_status"] = "ACTIVE"

        thermal = telemetry.get("thermal", {})
        thermal["cpu_temperature"] = max(thermal.get("cpu_temperature", 100) - 25, 60)
        thermal["gpu_temperature"] = max(thermal.get("gpu_temperature", 85) - 15, 55)

        telemetry["status"] = "RECOVERING"

    def _redeploy_panels(self):
        telemetry = self.current_state.get("telemetry", {})

        telemetry["power_output"] = telemetry.get("power_output", 0) + 30
        telemetry["panel_temperature"] = max(
            telemetry.get("panel_temperature", 90) - 10, 40
        )

        telemetry["status"] = "OPERATIONAL"

    def _power_save_mode(self):
        telemetry = self.current_state.get("telemetry", {})
        subsystems = telemetry.get("subsystems", {})

        telemetry["battery_charge"] = min(
            telemetry.get("battery_charge", 0) + 5, 100
        )

        subsystems["camera"] = "OFF"
        telemetry["status"] = "POWER_SAVE"

    def _enter_degraded_mode(self):
        telemetry = self.current_state.get("telemetry", {})
        subsystems = telemetry.get("subsystems", {})

        subsystems["camera"] = "OFF"
        subsystems["data_transmitter"] = "LIMITED"

        telemetry["status"] = "DEGRADED_SAFE"

    # ----------------------------
    # Validation & inspection
    # ----------------------------

    def check_constraints(self) -> bool:
        """
        Validate current telemetry against safety constraints.

        Returns:
            bool: True if all constraints are satisfied.
        """
        constraints = self.current_state.get("constraints", {})
        telemetry = self.current_state.get("telemetry", {})
        thermal = telemetry.get("thermal", {})

        if "max_cpu_temperature" in constraints:
            if thermal.get("cpu_temperature", 0) > constraints["max_cpu_temperature"]:
                return False

        if "min_battery_charge" in constraints:
            if telemetry.get("battery_charge", 0) < constraints["min_battery_charge"]:
                return False

        return True

    def get_state(self) -> dict:
        """Return current simulator state."""
        return self.current_state

    def get_previous_state(self) -> dict:
        """Return previous simulator state (before last action)."""
        return self.previous_state
