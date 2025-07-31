import streamlit as st
import pandas as pd
from agent import init_agent, set_data
from fraud_detector import detect_fraud
from compliance_checker import load_rules, check_compliance
from parser import parse_csv

# ------------------- 🎨 Custom CSS -------------------
custom_css = """
<style>
    html, body, .stApp {
        background-color: #1e2030;
        background-image: linear-gradient(135deg, #1e2030 0%, #2b2d42 100%);
        color: #ffffff;
        font-family: 'Segoe UI', sans-serif;
    }
    .big-header {
        font-size: 2.8rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .rounded-box {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px;
        border-radius: 18px;
        margin-bottom: 30px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    }
    .chat {
        background-color: #32344d;
        padding: 10px 16px;
        border-radius: 12px;
        margin: 10px 0;
        color: #ffffff;
    }
    .stTextInput input, .stTextArea textarea {
        background-color: #2d2f47;
        color: #ffffff;
        border-radius: 6px;
        padding: 8px;
    }
    .stButton button {
        background-color: #0072ff;
        color: #ffffff;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.6em 1.2em;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ------------------- 🌐 Page Setup -------------------
st.set_page_config(page_title="AuditAI Agent", layout="wide", page_icon="🧠")
st.markdown('<h1 class="big-header">📊 AuditAI Agent – Autonomous Financial Auditor</h1>', unsafe_allow_html=True)

# ------------------- 📄 Upload -------------------
st.markdown('<div class="rounded-box">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload CSV (transactions, salaries...)", type=["csv"])
st.markdown('</div>', unsafe_allow_html=True)

# ------------------- 📊 Data Handling -------------------
if uploaded_file:
    df = parse_csv(uploaded_file)
    df = detect_fraud(df)
    set_data(df)  # Set global data for the agent

    st.markdown('<div class="rounded-box">', unsafe_allow_html=True)
    st.subheader("📃 Parsed Financial Data")
    st.dataframe(df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="rounded-box">', unsafe_allow_html=True)
    st.subheader("🚨 Fraud Detection Results")
    if "is_fraud" in df.columns:
        df["Fraud Status"] = df["is_fraud"].apply(lambda x: "❌ Fraud" if x else "✅ Safe")

        def highlight(row):
            return ['background-color: #993333' if row['is_fraud'] else '' for _ in row]

        st.dataframe(df.style.apply(highlight, axis=1), use_container_width=True)
        st.markdown(f"<b>Total Frauds:</b> {df['is_fraud'].sum()}", unsafe_allow_html=True)
    else:
        st.warning("No fraud column detected.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="rounded-box">', unsafe_allow_html=True)
    st.subheader("Compliance Checks")
    rules = load_rules()
    df['compliance_issues'] = df.apply(lambda row: check_compliance(row, rules), axis=1)

    if 'Transaction_ID' in df.columns:
        st.dataframe(df[['Transaction_ID', 'compliance_issues']], use_container_width=True)
    else:
        st.dataframe(df[['compliance_issues']], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ------------------- 🧠 LLM Assistant -------------------
    st.markdown('<div class="rounded-box">', unsafe_allow_html=True)
    st.subheader("🧠 Ask the AuditAI Agent")

    if "agent" not in st.session_state:
        st.session_state.agent = init_agent()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    query = st.text_input("💬 Ask about frauds, compliance, or summary...")

    if st.button("Ask"):
        if query:
            try:
                result = st.session_state.agent.invoke({"input": query})
                output = result.get("output") if isinstance(result, dict) else str(result)
                st.session_state.chat_history.append(("You", query))
                st.session_state.chat_history.append(("AuditAI", output))
            except Exception as e:
                st.error(f"Agent Error: {e}")

    for role, msg in st.session_state.chat_history:
        st.markdown(f"<div class='chat'><strong>{role}:</strong> {msg}</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
