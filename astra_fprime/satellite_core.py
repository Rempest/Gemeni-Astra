import time
import json
import sys
import os

# Adding the root directory to path so we can import brain_node
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class AstraFPrimeComponent:
    """
    NASA F' Component Simulation for Astra Satellite Flight Software.
    This module handles hardware-level execution of AI-generated commands.
    """
    
    def __init__(self):
        self.energy_level = 12
        self.oxygen_system = "STANDBY"
        self.thrusters = "OFF"
        self.status_log = []

    def execute_commands(self, ai_decision):
        print(f"\n[F' Core] Commands received from Gemini 3 (Mission Status: {ai_decision.get('status', 'UNKNOWN')})")
        
        # In F' architecture, these would be Port Invocations
        actions = ai_decision.get('priority_actions', [])
        
        for action in actions:
            time.sleep(1)  # Simulate hardware latency
            action_lower = action.lower()
            
            if "oxygen" in action_lower:
                self.oxygen_system = "ACTIVE"
                execution_msg = f"EXECUTED: {action} -> Life Support: {self.oxygen_system}"
            elif "power" in action_lower or "low-power" in action_lower:
                execution_msg = f"EXECUTED: {action} -> Power Grid: Optimized for survival"
            elif "thrusters" in action_lower or "orientation" in action_lower:
                self.thrusters = "STABILIZING"
                execution_msg = f"EXECUTED: {action} -> RCS Thrusters: {self.thrusters}"
            else:
                execution_msg = f"EXECUTED: {action} -> General system update"
                
            print(f"✔️ {execution_msg}")
            self.status_log.append(execution_msg)

if __name__ == "__main__":
    try:
        from brain_node import get_astral_decision
    except ImportError:
        print("Error: Could not find brain_node.py. Make sure it is in the root directory.")
        sys.exit(1)
    
    # 1. Simulate Raw Telemetry Data (SpaceROS-compliant format)
    raw_telemetry = "Power 12%, Oxygen dropping, Orientation Unstable"
    print(f"📡 Telemetry Stream: {raw_telemetry}")
    
    # 2. Reasoning Layer (Gemini 3 Core)
    print("🧠 Gemini 3 is thinking...")
    decision = get_astral_decision(raw_telemetry)
    
    # 3. Flight Software Execution Layer (F' Logic)
    satellite = AstraFPrimeComponent()
    satellite.execute_commands(decision)
    
    print("\n🚀 Mission status updated successfully.")
