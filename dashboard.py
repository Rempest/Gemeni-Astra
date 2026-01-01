import streamlit as st
import json
import os
import subprocess
import pandas as pd
import time

# ----------------------------------------
# Page configuration: Dark Space theme
# ----------------------------------------
st.set_page_config(page_title="Gemini-Astra Mission Control", layout="wide")
st.title("🛰️ Gemini-Astra: Autonomous Mission Control")
st.sidebar.header("📡 Command Center")

# ----------------------------------------
# 1. Telemetry scenario selection
# ----------------------------------------
telemetry_dir = "telemetry_cases"
if not os.path.exists(telemetry_dir):
    os.makedirs(telemetry_dir)
    # Create a default telemetry file if folder doesn't exist
    default_file = os.path.join(telemetry_dir, "default.json")
    with open(default_file, "w") as f:
        json.dump({"battery": 50, "oxygen": 80, "temp": 30}, f)

# List all JSON files in telemetry_cases
scenarios = [f for f in os.listdir(telemetry_dir) if f.endswith(".json")]
selected_scenario = st.sidebar.selectbox("Select Telemetry Scenario", scenarios)

# Load selected telemetry
telemetry_path = os.path.join(telemetry_dir, selected_scenario)
with open(telemetry_path, "r") as f:
    current_telemetry = json.load(f)

# ----------------------------------------
# 2. Telemetry visualization
# ----------------------------------------
st.subheader("📊 Real-time Telemetry Stream")
cols = st.columns(len(current_telemetry))
for i, (key, value) in enumerate(current_telemetry.items()):
    cols[i].metric(label=key.upper(), value=value)

# Simple bar chart for telemetry metrics
chart_data = pd.DataFrame(list(current_telemetry.values()), 
                          index=list(current_telemetry.keys()), 
                          columns=["Value"])
st.bar_chart(chart_data)

st.divider()

# ----------------------------------------
# 3. Run AI Brain Node
# ----------------------------------------
st.sidebar.divider()
if st.sidebar.button("🚀 RUN AI MISSION CONTROL", type="primary"):
    with st.spinner("Gemini 2.0 Flash is analyzing telemetry..."):
        cmd = ["python3", "brain_node.py", "--telemetry", telemetry_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            st.sidebar.success("Analysis Complete!")
        else:
            st.sidebar.error("Error running Brain Node")
            st.sidebar.code(result.stderr)

# ----------------------------------------
# 4. Display AI Decision (Live Update)
# ----------------------------------------
st.subheader("🧠 Gemini AI Decision")

# Live refresh every 2 seconds
placeholder = st.empty()
while True:
    if os.path.exists("command.json"):
        with open("command.json", "r") as f:
            decision = json.load(f)
        
        with placeholder.container():
            res_col1, res_col2 = st.columns([1, 2])
            
            # Risk Level visualization
            with res_col1:
                risk = decision.get("risk_level", 0)
                color = "red" if risk > 7 else "orange" if risk > 4 else "green"
                st.markdown(f"### Risk Level: <span style='color:{color}'>{risk}/10</span>", unsafe_allow_html=True)
                st.write(f"**Status:** {decision.get('status', 'N/A')}")
            
            # Priority actions
            with res_col2:
                st.write("**Priority Actions:**")
                for action in decision.get("priority_actions", []):
                    st.info(f"✔ {action}")
            
            # Show raw JSON for engineering transparency
            st.json(decision)
    else:
        placeholder.info("Waiting for AI analysis... Press the button in the sidebar.")
    
    time.sleep(2)
