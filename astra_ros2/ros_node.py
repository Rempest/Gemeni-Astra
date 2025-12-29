import json
import time

class SpaceROSInterface:
    """
    Space ROS / ROS 2 wrapper for the Astra satellite.
    Simulates telemetry publishing and command forwarding.
    """
    def __init__(self):
        self.node_name = "/astra_mission_control"
        self.telemetry_topic = "/telemetry/status"
        print(f"✅ [SpaceROS] Node {self.node_name} initialized and spinning.")

    def publish_data(self, data):
        # Simulate publishing data to a ROS 2 topic
        print(f"📡 [SpaceROS] Publishing to {self.telemetry_topic}: {data}")
        return True

    def bridge_to_fprime(self, command):
        # Simulate forwarding a command to NASA F' via a ROS bridge
        print(f"⚙️ [SpaceROS] Bridging command to F' Core: {command}")
        time.sleep(0.1)  # Simulated network latency
