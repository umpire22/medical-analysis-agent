import streamlit as st
import pandas as pd
import random

# --- PAGE CONFIG ---
st.set_page_config(page_title="🩺 Medical Analysis Agent", page_icon="🩺", layout="wide")

# --- CUSTOM STYLES ---
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #e8f5e9, #ffffff);
        }
        .stButton > button {
            background: linear-gradient(to right, #2e7d32, #43a047);
            color: white;
            border-radius: 12px;
            padding: 10px 20px;
            font-weight: bold;
            transition: 0.3s;
        }
        .stButton > button:hover {
            background: linear-gradient(to right, #43a047, #2e7d32);
            transform: scale(1.05);
        }
        .card {
            padding: 20px;
            border-radius: 15px;
            background-color: #ffffff;
            box-shadow: 2px 2px 12px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# --- APP HEADER ---
st.markdown("<h1 style='text-align: center; color: #2e7d32;'>🩺 Medical Analysis Agent</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:18px;'>Analyze symptoms and assess potential health risks</p>", unsafe_allow_html=True)

# --- SESSION STATE FOR HISTORY ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- MANUAL SYMPTOM CHECK ---
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📝 Manual Symptom Check")

    symptoms = st.text_area("Enter symptoms (e.g., 'Fever, headache, fatigue')")

    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("🔎 Analyze Symptoms"):
            if symptoms.strip():
                # Simple random risk simulation
                risk_score = random.randint(1, 100)
                if risk_score < 40:
                    result = f"✅ Low Risk ({risk_score}%)"
                    color = "green"
                elif 40 <= risk_score < 70:
                    result = f"⚠️ Medium Risk ({risk_score}%)"
                    color = "orange"
                else:
                    result = f"❌ High Risk ({risk_score}%)"
                    color = "red"

                st.markdown(f"<p style='color:{color}; font-size:18px; font-weight:bold;'>{result}</p>", unsafe_allow_html=True)

                # Save to history
                st.session_state.history.append({"Symptoms": symptoms, "Risk Score": risk_score, "Result": result})
            else:
                st.warning("Please enter symptoms.")

    with col2:
        if st.button("🗑 Clear History"):
            st.session_state.history = []
            st.success("History cleared!")

    st.markdown("</div>", unsafe_allow_html=True)

# --- HISTORY LOG ---
if st.session_state.history:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📜 Analysis History")
    hist_df = pd.DataFrame(st.session_state.history)
    st.dataframe(hist_df, use_container_width=True)
    st.download_button("⬇️ Download History", data=hist_df.to_csv(index=False), file_name="medical_history.csv", mime="text/csv")
    st.markdown("</div>", unsafe_allow_html=True)

# --- BULK MEDICAL ANALYSIS ---
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📂 Bulk Medical Analysis (CSV Upload)")

    uploaded_file = st.file_uploader("Upload a CSV file with a column named 'Symptoms'", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        if "Symptoms" in df.columns:
            results = []
            for s in df["Symptoms"]:
                risk_score = random.randint(1, 100)
                if risk_score < 40:
                    results.append(f"✅ Low Risk ({risk_score}%)")
                elif 40 <= risk_score < 70:
                    results.append(f"⚠️ Medium Risk ({risk_score}%)")
                else:
                    results.append(f"❌ High Risk ({risk_score}%)")

            df["Medical Analysis"] = results

            # Highlight results
            def highlight_risk(val):
                if "Low Risk" in val:
                    return "background-color: #c8e6c9; color: green;"
                elif "Medium Risk" in val:
                    return "background-color: #fff9c4; color: orange;"
                else:
                    return "background-color: #ffcdd2; color: red;"

            st.write("🔎 Medical Analysis Results:")
            st.dataframe(df.style.applymap(highlight_risk, subset=["Medical Analysis"]))

            # Download button
            st.download_button("⬇️ Download Results", data=df.to_csv(index=False), file_name="medical_results.csv", mime="text/csv")
        else:
            st.error("CSV must contain a column named 'Symptoms'.")
    st.markdown("</div>", unsafe_allow_html=True)
