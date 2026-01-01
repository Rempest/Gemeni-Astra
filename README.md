# Gemeni-Astra
**🚀 Gemini-Astra
Autonomous Multi-Agent Space Repair System**
![WhatsApp Image 2025-12-29 at 22 47 34](https://github.com/user-attachments/assets/3896abd1-8803-4405-961c-f633e5e53a4a)
*Built for the Gemini 3 Global Hackathon*
**Overview**

Gemini-Astra is an autonomous decision-making system designed for spacecraft and satellite operations.
It analyzes raw telemetry data, evaluates system risks using Google Gemini 2.0 Flash, and produces deterministic, machine-readable commands suitable for direct integration with robotic or flight software.

The system follows the OODA Loop (Observe → Orient → Decide → Act), a decision-making model widely used in aerospace and defense systems.

**Gemini-Astra is not a chatbot.**
**It is designed as an AI pilot operating under strict constraints, deterministic outputs, and safety validation.*

**Architecture**
*Logic Flow (OODA Loop)
Telemetry (telemetry.json)
        ↓
Observe: Data Ingestion
        ↓
Orient: AI Reasoning (Gemini 2.0 Flash)
        ↓
Decide: Deterministic Command Generation
        ↓
Act: Command Output (command.json)
        ↓
Visualize: Mission Dashboard (Streamlit)*

**Components**
**1. Data Ingestion**

Input: telemetry.json

Simulated satellite telemetry (battery level, oxygen, subsystem status, fault flags)

Designed to mirror real spacecraft sensor streams

**2. AI Reasoning Core**

Implemented in brain_node.py

Uses google-genai SDK with Gemini 2.0 Flash

Deterministic configuration:

temperature = 0

Gemini evaluates:

anomaly type

risk level

recommended action

priority

**3. Safety & Deterministic Output**

AI output is strict JSON only

Commands are validated against a predefined whitelist:

*VALID_ACTIONS = [
    "ISOLATE_MODULE",
    "CLOSE_VALVE",
    "REDUCE_POWER",
    "REBOOT_SUBSYSTEM",
    "NO_ACTION"
]*


This safety layer prevents hallucinated or unsafe commands and makes the system compatible with real robotic controllers.

**4. Interface & Monitoring**

dashboard.py built with Streamlit

**Displays:**

live telemetry

detected anomalies

AI decisions

priority levels

Intended for mission operators on the ground

**Technical Stack**

**Language:** Python 3.12

**AI Model:** Google Gemini 3

**AI SDK:** google-genai

**Decision Model:** Deterministic LLM reasoning (temperature = 0)

**UI:** Streamlit

**Design Pattern:** OODA Loop

**Target Integration:** ROS 2, SpaceROS, robotic actuation systems

**Design Rationale**

**Low Latency**: Gemini is selected for time-critical decision-making in space environments.

**Safety First**: Hard validation of AI outputs ensures compatibility with autonomous systems.

**Explainability**: AI provides structured reasoning alongside commands.

**Scalability**: Architecture is ready for integration with ROS 2 nodes and real-time telemetry streams.

**Quick Start**
**1. Clone the repository**
git clone https://github.com/Rempest/Gemeni-Astra.git
cd Gemeni-Astra

**2. Install dependencies**
pip install -r requirements.txt

**3. Configure Gemini API**

Set your Google API key:

export GOOGLE_API_KEY=your_api_key_here

**4. Run AI decision engine**
python brain_node.py



**This will:**

read telemetry.json

analyze telemetry with Gemini

generate command.json

**5. Launch the dashboard**
streamlit run dashboard.py

**Example Output**

Input: telemetry.json

{
  "battery_level": 18,
  "oxygen_pressure": 92,
  "thermal_status": "nominal",
  "solar_panel_actuator": "fault"
}


Output: command.json

{
  "action": "ISOLATE_MODULE",
  "target": "solar_panel_actuator",
  "priority": "HIGH",
  "confidence": 0.91
}

**Key Features**

Autonomous AI decision-making (no human-in-the-loop)

Deterministic and validated command output

Low-latency reasoning using Gemini

Safety layer against AI hallucinations

Real-time monitoring dashboard

Designed for aerospace and robotic systems

**Future Roadmap**

🔹 ROS 2 integration (command publisher nodes)

🔹 SpaceROS compatibility for flight-grade software

🔹 MoveIt2 integration for robotic repair and manipulation

🔹 Real-time telemetry streaming (DDS)

🔹 Hardware-in-the-loop simulation

🔹 Fault injection testing and certification-ready pipelines

**Disclaimer**

This project is a prototype developed for a hackathon environment.
It is not flight-certified software but is architected with real aerospace constraints in mind.
