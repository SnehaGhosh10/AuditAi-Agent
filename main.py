import streamlit as st
import pandas as pd
from agent import init_agent
from fraud_detector import detect_fraud
from compliance_checker import load_rules, check_compliance
from parser import parse_csv

st.set_page_config(page_title="AuditAI Agent", layout="wide")
st.title("📊 AuditAI Agent – Autonomous Financial Auditor")

uploaded_file = st.file_uploader("📤 Upload a CSV File (e.g., salaries, expenses)", type=["csv"])

if uploaded_file:
    df = parse_csv(uploaded_file)
    st.subheader("📄 Parsed Data")
    st.dataframe(df)

    st.subheader("🔍 Fraud Detection")
    fraud_df = detect_fraud(df.copy())
    st.dataframe(fraud_df)

    st.subheader("✅ Compliance Check")
    rules = load_rules()
    df['compliance_issues'] = df.apply(lambda row: check_compliance(row, rules), axis=1)
    st.dataframe(df[['Transaction_ID', 'compliance_issues']])


    st.subheader("🧠 AI Assistant (LangChain Agent)")
    query = st.text_input("Ask something about the data or rules...")
    if query:
        agent = init_agent()
        result = agent.run(query)
        st.success(result)
