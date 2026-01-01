import streamlit as st
import json
import os
import subprocess
import pandas as pd

# --- Page Configuration: Mission Control Aesthetics ---
st.set_page_config(
    page_title="Gemini-Astra Mission Control", 
    layout="wide", 
    page_icon="🛰️"
)

# Custom CSS for the "Deep Space" theme
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { 
        background-color: #1c212d; 
        padding: 15px; 
        border-radius: 10px; 
        border: 1px solid #30363d; 
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛰️ Gemini-Astra: Autonomous Mission Control")
st.sidebar.header("📡 Command Center")

# --- 1. Scenario Selection System ---
telemetry_dir = "telemetry_cases"
if not os.path.exists(telemetry_dir):
    os.makedirs(telemetry_dir)

# Fetch available telemetry JSON files
scenarios = [f for f in os.listdir(telemetry_dir) if f.endswith(".json")]

if not scenarios:
    st.warning("No scenarios found. Please add JSON files to the 'telemetry_cases' folder.")
    selected_scenario = None
else:
    selected_scenario = st.sidebar.selectbox("Select Telemetry Scenario", scenarios)

if selected_scenario:
    telemetry_path = os.path.join(telemetry_dir, selected_scenario)
    with open(telemetry_path, "r") as f:
        current_telemetry = json.load(f)

    # --- 2. Telemetry Visualization ---
    st.subheader("📊 Real-time Telemetry Stream")
    
    # Create dynamic columns based on telemetry keys
    cols = st.columns(len(current_telemetry))
    for i, (key, value) in enumerate(current_telemetry.items()):
        cols[i].metric(label=key.upper(), value=value)

    # Visual representation of metrics
    st.bar_chart(pd.DataFrame(current_telemetry.items(), columns=["Metric", "Value"]).set_index("Metric"))

    st.divider()

    # --- 3. Execute AI Brain Node ---
    st.sidebar.divider()
    if st.sidebar.button("🚀 RUN AI MISSION CONTROL", type="primary"):
        with st.spinner("Gemini 2.0 Flash analyzing telemetry..."):
            # Trigger the decision-making logic in brain_node.py
            cmd = ["python3", "brain_node.py", "--telemetry", telemetry_path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                st.sidebar.success("Decision Generated!")
                # Force a UI refresh to display the new command.json
                st.rerun() 
            else:
                st.sidebar.error("Execution Failed")
                st.sidebar.code(result.stderr)

    # --- 4. Display AI Decision Engine Output ---
    st.subheader("🧠 Gemini AI Decision Core")

    if os.path.exists("command.json"):
        with open("command.json", "r") as f:
            decision = json.load(f)
        
        res_col1, res_col2 = st.columns([1, 2])
        
        with res_col1:
            risk = decision.get("risk_level", 0)
            # Dynamic color coding based on risk severity
            color = "#ff4b4b" if risk > 7 else "#ffa500" if risk > 4 else "#00ff00"
            st.markdown(f"""
                <div style="background-color: #1c212d; padding: 20px; border-radius: 10px; border-left: 10px solid {color};">
                    <h3 style="margin:0;">Risk Level: {risk}/10</h3>
                    <p style="font-size: 20px;">Status: <b>{decision.get('status', 'N/A')}</b></p>
                </div>
                """, unsafe_allow_html=True)
        
        with res_col2:
            st.write("**Priority Mitigation Actions:**")
            # List automated responses identified by Gemini
            for action in decision.get("priority_actions", []):
                st.success(f"📡 EXECUTE: {action}")
        
        # Expandable section for technical transparency (Judges love this)
        with st.expander("See Raw Reasoning Data"):
            st.json(decision)
    else:
        st.info("System Ready. Please initiate AI analysis from the Command Center.")
