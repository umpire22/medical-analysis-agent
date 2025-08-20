import streamlit as st
import pandas as pd

st.title("🏥 Simple Medical Analysis Agent")

st.write("Enter patient details or upload a CSV file for analysis.")

# --- Option 1: Manual Input ---
st.subheader("Manual Patient Data Entry")
age = st.number_input("Age", min_value=1, max_value=120, step=1)
weight = st.number_input("Weight (kg)", min_value=1.0, max_value=200.0, step=0.1)
bp = st.number_input("Blood Pressure (systolic)", min_value=50, max_value=250, step=1)
sugar = st.number_input("Blood Sugar (mg/dL)", min_value=50, max_value=500, step=1)

if st.button("Analyze Patient"):
    analysis = []
    if bp > 140:
        analysis.append("⚠️ High Blood Pressure (Hypertension risk)")
    elif bp < 90:
        analysis.append("⚠️ Low Blood Pressure (Hypotension risk)")
    else:
        analysis.append("✅ Normal Blood Pressure")

    if sugar > 180:
        analysis.append("⚠️ High Blood Sugar (Possible Diabetes risk)")
    elif sugar < 70:
        analysis.append("⚠️ Low Blood Sugar (Hypoglycemia risk)")
    else:
        analysis.append("✅ Normal Blood Sugar")

    if weight / ((1.65) ** 2) > 30:  # simple BMI check (assuming avg height 1.65m)
        analysis.append("⚠️ Possible Obesity (Weight management needed)")
    else:
        analysis.append("✅ Healthy Weight Range")

    st.subheader("Medical Analysis Result:")
    for a in analysis:
        st.write(a)

# --- Option 2: Upload CSV ---
st.subheader("Batch Analysis (Upload CSV)")
uploaded_file = st.file_uploader("Upload patient data (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.write("📄 Uploaded Data")
    st.dataframe(df.head())

    def analyze_row(row):
        results = []
        if row["BloodPressure"] > 140:
            results.append("High BP")
        elif row["BloodPressure"] < 90:
            results.append("Low BP")
        else:
            results.append("Normal BP")

        if row["BloodSugar"] > 180:
            results.append("High Sugar")
        elif row["BloodSugar"] < 70:
            results.append("Low Sugar")
        else:
            results.append("Normal Sugar")

        if row["Weight"] / ((1.65) ** 2) > 30:
            results.append("Obesity Risk")
        else:
            results.append("Normal Weight")

        return ", ".join(results)

    df["Medical_Analysis"] = df.apply(analyze_row, axis=1)

    st.subheader("📊 Analysis Results")
    st.dataframe(df)

    # download option
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Results", data=csv, file_name="medical_results.csv")
