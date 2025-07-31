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

    # ✅ Run Fraud Detection
    df = detect_fraud(df)

    st.subheader("📄 Parsed Data")
    st.dataframe(df)

    # ✅ Fraud Detection Section
    st.subheader("🔍 Fraud Detection")

    if "is_fraud" in df.columns:
        fraud_df = df[df["is_fraud"] == True]
        safe_df = df[df["is_fraud"] == False]

        # Add readable label column
        df["Fraud Status"] = df["is_fraud"].apply(lambda x: "❌ Fraudulent" if x else "✅ Safe")

        # Style fraudulent rows
        def highlight_fraud(row):
            return ['background-color: #ffcccc' if row['is_fraud'] else '' for _ in row]

        st.dataframe(df.style.apply(highlight_fraud, axis=1), use_container_width=True)
        st.markdown(f"**🚨 Total Fraudulent Records:** {len(fraud_df)}")

    else:
        st.warning("⚠️ No fraud analysis has been run yet.")

    # ✅ Compliance Check Section
    st.subheader("✅ Compliance Check")
    rules = load_rules()
    df['compliance_issues'] = df.apply(lambda row: check_compliance(row, rules), axis=1)

    if 'Transaction_ID' in df.columns:
        st.dataframe(df[['Transaction_ID', 'compliance_issues']])
    else:
        st.dataframe(df[['compliance_issues']])

    # ✅ Pass updated data to AI agent
    set_data(df, rules)

    # ✅ LangChain Assistant
    st.subheader("🧠 AI Assistant (LangChain Agent)")
    query = st.text_input("Ask something about the data or rules...", key="ai_query")
    if st.button("Ask"):
        if query:
            agent = init_agent()
            result = agent.run(query)
            st.success(result)
        else:
            st.warning("Please enter a question.")
