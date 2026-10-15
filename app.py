
import random
import json
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="IndustrialGuard",
    page_icon="🏭",
    layout="wide"
)

st.title("🏭 IndustrialGuard")
st.subheader("Smart Industrial Anomaly Monitoring System")
st.caption("Portfolio demo using simulated machine sensor readings")

st.sidebar.header("⚙️ Monitoring Settings")

machine = st.sidebar.selectbox(
    "Select Machine",
    ["Motor-01", "Pump-02", "Compressor-03"]
)

samples = st.sidebar.slider(
    "Number of Readings", 20, 200, 100
)

abnormal_rate = st.sidebar.slider(
    "Abnormal Reading Rate (%)", 0, 30, 10
)

temp_limit = st.sidebar.slider(
    "Temperature Limit (°C)", 40, 120, 80
)

vibration_limit = st.sidebar.slider(
    "Vibration Limit (mm/s)", 2, 20, 8
)

if st.sidebar.button("🔄 Generate New Readings"):
    st.rerun()

random.seed(42)

data = []

for i in range(samples):
    abnormal = random.random() < abnormal_rate / 100

    temperature = random.gauss(65, 7)
    vibration = random.gauss(4, 1.2)

    if abnormal:
        temperature += random.uniform(15, 35)
        vibration += random.uniform(3, 9)

    temperature = max(20, temperature)
    vibration = max(0, vibration)

    temp_alert = temperature > temp_limit
    vibration_alert = vibration > vibration_limit

    if temp_alert and vibration_alert:
        severity = "Critical"
        alert = "High temperature and vibration"
    elif temp_alert or vibration_alert:
        severity = "Medium"
        alert = (
            "High temperature"
            if temp_alert
            else "High vibration"
        )
    else:
        severity = "Normal"
        alert = "No anomaly detected"

    data.append({
        "Reading": i + 1,
        "Machine": machine,
        "Temperature (°C)": round(temperature, 2),
        "Vibration (mm/s)": round(vibration, 2),
        "Severity": severity,
        "Alert": alert
    })

df = pd.DataFrame(data)

critical_count = (df["Severity"] == "Critical").sum()
medium_count = (df["Severity"] == "Medium").sum()
alert_count = (df["Severity"] != "Normal").sum()

alert_rate = alert_count / len(df) * 100

health_score = max(
    0,
    min(
        100,
        round(
            100
            - (medium_count * 3 + critical_count * 8)
            / len(df) * 10
        )
    )
)

if health_score >= 80:
    health_status = "Healthy"
elif health_score >= 50:
    health_status = "Needs Attention"
else:
    health_status = "Critical Condition"

st.markdown("---")
st.subheader("📊 Machine Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Machine", machine)
c2.metric("Health Score", f"{health_score}/100")
c3.metric("Active Alerts", int(alert_count))
c4.metric("Alert Rate", f"{alert_rate:.1f}%")

if health_score >= 80:
    st.success(f"Machine Status: {health_status}")
elif health_score >= 50:
    st.warning(f"Machine Status: {health_status}")
else:
    st.error(f"Machine Status: {health_status}")

st.progress(health_score / 100)

st.markdown("---")
st.subheader("🌡️ Temperature Monitoring")

fig_temp = px.line(
    df,
    x="Reading",
    y="Temperature (°C)",
    title="Machine Temperature Readings",
    markers=True
)

fig_temp.add_hline(
    y=temp_limit,
    line_dash="dash",
    annotation_text="Temperature Limit"
)

st.plotly_chart(fig_temp, use_container_width=True)

st.subheader("📳 Vibration Monitoring")

fig_vib = px.line(
    df,
    x="Reading",
    y="Vibration (mm/s)",
    title="Machine Vibration Readings",
    markers=True
)

fig_vib.add_hline(
    y=vibration_limit,
    line_dash="dash",
    annotation_text="Vibration Limit"
)

st.plotly_chart(fig_vib, use_container_width=True)

st.markdown("---")
st.subheader("🚨 Anomaly Alerts")

alerts_df = df[df["Severity"] != "Normal"]

if alerts_df.empty:
    st.success("No anomalies detected in the current readings.")
else:
    st.dataframe(
        alerts_df,
        use_container_width=True,
        hide_index=True
    )

st.subheader("📋 All Sensor Readings")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

csv_data = df.to_csv(index=False)

st.download_button(
    "⬇️ Download Readings (CSV)",
    data=csv_data,
    file_name="industrialguard_readings.csv",
    mime="text/csv"
)

json_data = json.dumps(
    alerts_df.to_dict(orient="records"),
    indent=2
)

st.download_button(
    "⬇️ Download Alerts (JSON)",
    data=json_data,
    file_name="industrialguard_alerts.json",
    mime="application/json"
)

st.markdown("---")
st.caption(
    "Note: This project uses simulated sensor data. "
    "It is a portfolio demonstration, not a real-time "
    "industrial monitoring or predictive AI system."
)
