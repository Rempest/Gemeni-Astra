# 🚀 Gemini-Astra  
### Autonomous AI Decision Core for Spacecraft & Satellite Operations  
**Built for the Google Gemini 3 Global Hackathon**

![WhatsApp Image 2025-12-29 at 22 47 34](https://github.com/user-attachments/assets/3896abd1-8803-4405-961c-f633e5e53a4a)

## 🚨 Problem

Spacecraft and satellites must often operate without real-time communication with Earth.  
In critical situations, delayed or incorrect decisions can lead to mission failure.

Traditional autonomy systems are rigid, while modern AI systems are often unsafe for direct control.

**The challenge:**  
How can an AI system make autonomous decisions in space **while remaining deterministic, explainable, and safe**?


## 💡 Solution

**Gemini-Astra** is an autonomous AI decision-making system designed for spacecraft and satellite operations.

It analyzes raw telemetry data, reasons using **Google Gemini 3**, and produces **strict, machine-readable commands** that are safe for direct integration with robotic or flight software.

> Gemini-Astra is **not a chatbot**.  
> It is designed as an **AI pilot operating under strict constraints, deterministic outputs, and safety validation**.


## 🤖 Why Gemini 3?

Gemini 3 is used **not as a text generator**, but as a **deterministic reasoning engine**.

Gemini 3 enables:
- Multimodal reasoning over complex telemetry data
- Low-latency inference for time-critical decisions
- Structured, machine-readable outputs (JSON only)
- Deterministic behavior required for safety-critical systems

This makes Gemini 3 suitable for **autonomous aerospace decision-making**, not just conversational AI.


## 🧠 System Architecture (OODA Loop)

Gemini-Astra follows the **OODA Loop** (Observe → Orient → Decide → Act),  
a decision-making model widely used in aerospace and defense systems.

Telemetry (telemetry.json)
↓
Observe: Data Ingestion
↓
Orient: AI Reasoning (Gemini 3)
↓
Decide: Deterministic Command Generation
↓
Act: Validated Command Output (command.json)
↓
Visualize: Mission Dashboard (Streamlit)


## 🧩 Core Components

### 1️⃣ Data Ingestion
- **Input:** `telemetry.json`
- Simulated satellite telemetry:
  - battery level
  - oxygen pressure
  - subsystem status
  - fault flags
- Designed to mirror real spacecraft sensor streams


### 2️⃣ AI Reasoning Core
- Implemented in `brain_node.py`
- Uses `google-genai` SDK with **Gemini 3**
- Deterministic configuration:
  - `temperature = 0`

Gemini evaluates:
- anomaly type
- risk level
- recommended action
- priority


### 3️⃣ Safety & Deterministic Output
- AI output format: **strict JSON only**
- All commands are validated against a predefined whitelist:

```python
VALID_ACTIONS = [
  "ISOLATE_MODULE",
  "CLOSE_VALVE",
  "REDUCE_POWER",
  "REBOOT_SUBSYSTEM",
  "NO_ACTION"
]
```

This safety layer:

prevents hallucinated or unsafe commands

guarantees compatibility with real robotic controllers

enforces human-designed operational constraints

### 4️⃣ Interface & Monitoring

dashboard.py built with Streamlit

Displays:

live telemetry

detected anomalies

AI decisions

priority levels

Designed for mission operators and system monitoring.


###Example Scenario

Input – telemetry.json
{
  "battery_level": 18,
  "oxygen_pressure": 92,
  "thermal_status": "nominal",
  "solar_panel_actuator": "fault"
}


Output – command.json
{
  "action": "ISOLATE_MODULE",
  "target": "solar_panel_actuator",
  "priority": "HIGH",
  "confidence": 0.91
}

This demonstrates autonomous anomaly detection, reasoning, and safe decision output.

## Technical Stack

Language: Python 3.12

AI Model: Google Gemini 3

AI SDK: google-genai

Decision Model: Deterministic LLM reasoning (temperature = 0)

UI: Streamlit

Design Pattern: OODA Loop

Target Integration: ROS 2, SpaceROS, robotic actuation systems


## Design Rationale

Low Latency: Gemini 3 enables fast decision-making for space environments

Safety First: Hard validation of AI outputs prevents unsafe behavior

Explainability: Structured reasoning accompanies every decision

Scalability: Architecture is designed for ROS 2 nodes and real-time telemetry

### 🚀 Future Roadmap

🔹 ROS 2 integration (command publisher nodes)

🔹 SpaceROS compatibility for flight-grade software

🔹 MoveIt 2 integration for robotic repair and manipulation

🔹 Real-time telemetry streaming (DDS)

🔹 Hardware-in-the-loop simulation

🔹 Fault injection testing and certification-ready pipelines

## ⚠️ Disclaimer

This project is a *prototype developed for a hackathon environment.*

It is not *flight-certified software*, but it is architected with real aerospace constraints, safety considerations, and autonomous system principles in mind.

