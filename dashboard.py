import streamlit as st
import json
import subprocess
import time
import os  

st.set_page_config(
    page_title="ASTRA Mission Control",
    layout="wide",
    page_icon="🛰️"
)

st.title("🛰️ ASTRA Satellite – Mission Control Dashboard")
st.markdown("---")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📡 Live Telemetry")
    st.metric(label="Oxygen Reserve", value="15%", delta="-5%", delta_color="inverse")
    st.metric(label="Energy Level", value="12%", delta="-2%", delta_color="inverse")
    st.warning("SYSTEM CRITICAL: Power & Life Support Failure")

with col2:
    st.subheader("🧠 Gemini 3 AI Analysis")
    if st.button("RUN AI DIAGNOSTICS", type="primary"):
        with st.spinner("Gemini 3 is analyzing telemetry..."):
            my_env = os.environ.copy()
            my_env["GOOGLE_API_KEY"] = "AIzaSyA7Zsxd6gd3pWEJNFg8P2xnCRbNhfcGlyw"
            
            try:
                result = subprocess.check_output(["python3", "brain_node.py"], env=my_env).decode("utf-8")

            
                json_start = result.find('{')
                data = json.loads(result[json_start:])

                st.success(f"**Status:** {data['status']}")
                st.write("**Priority Actions (Sent via SpaceROS):**")
                for action in data['priority_actions']:
                    st.info(f"✔️ {action}")

                st.error(f"**Risk Level:** {data['risk_level']}/10")
            except Exception as e:
                st.error(f"Error running diagnostics: {e}")

st.markdown("---")
st.caption("Architecture: Gemini 3 Flash + NASA F' Core + SpaceROS Wrapper")