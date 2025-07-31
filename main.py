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
    df = detect_fraud(df)  # Add fraud detection result to same DataFrame
    st.dataframe(df[['Transaction_ID', 'is_fraud']] if 'Transaction_ID' in df.columns else df[['is_fraud']])

    st.subheader("✅ Compliance Check")
    rules = load_rules()
    df['compliance_issues'] = df.apply(lambda row: check_compliance(row, rules), axis=1)

    if 'Transaction_ID' in df.columns:
        st.dataframe(df[['Transaction_ID', 'compliance_issues']])
    else:
        st.dataframe(df[['compliance_issues']])

    # Set global data for agent to use
    set_data(df, rules)

    st.subheader("🧠 AI Assistant (LangChain Agent)")

    # Input form with button
    with st.form("query_form"):
        query = st.text_input("Ask something about the data or rules:")
        submitted = st.form_submit_button("Ask")
        
        if submitted and query:
            try:
                agent = init_agent()
                result = agent.run(query)
                st.success(result)
            except Exception as e:
                st.error(f"Error from AI Agent: {e}")
