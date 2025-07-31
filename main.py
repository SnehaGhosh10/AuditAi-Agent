import streamlit as st
import pandas as pd
from agent import init_agent, set_data
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
    if 'is_fraud' in fraud_df.columns:
        if 'Transaction_ID' in fraud_df.columns:
            st.dataframe(fraud_df[['Transaction_ID', 'is_fraud']])
        else:
            st.dataframe(fraud_df[['is_fraud']])
    else:
        st.warning("❗ 'is_fraud' column not found in the result.")

    st.subheader("✅ Compliance Check")
    rules = load_rules()
    df['compliance_issues'] = df.apply(lambda row: check_compliance(row, rules), axis=1)

    if 'Transaction_ID' in df.columns:
        st.dataframe(df[['Transaction_ID', 'compliance_issues']])
    else:
        st.dataframe(df[['compliance_issues']])

    # Pass data to agent
    set_data(df, rules)

    # 🧠 LangChain AI Assistant
    st.subheader("🧠 AI Assistant (LangChain Agent)")
    query = st.text_input("Ask something about the data or rules...", key="ai_query")
    if st.button("Ask"):
        if query:
            agent = init_agent()
            result = agent.run(query)
            st.success(result)
        else:
            st.warning("Please enter a question.")
