import streamlit as st
import pandas as pd
from agent import init_agent, set_data
from fraud_detector import detect_fraud
from compliance_checker import load_rules, check_compliance
from parser import parse_csv

# 🧠 Page settings
st.set_page_config(page_title="AuditAI Agent", layout="wide")
st.title("📊 AuditAI Agent – Autonomous Financial Auditor")

# 📤 Upload CSV
uploaded_file = st.file_uploader("📤 Upload a CSV File (e.g., salaries, expenses)", type=["csv"])

if uploaded_file:
    # ✅ Step 1: Parse CSV
    df = parse_csv(uploaded_file)

    # ✅ Step 2: Detect Fraud
    df = detect_fraud(df)

    st.subheader("📄 Parsed Data")
    st.dataframe(df)

    # ✅ Step 3: Fraud Detection Summary
    st.subheader("🔍 Fraud Detection")

    if "is_fraud" in df.columns:
        df["Fraud Status"] = df["is_fraud"].apply(lambda x: "❌ Fraudulent" if x else "✅ Safe")

        def highlight_fraud(row):
            return ['background-color: #ffcccc' if row['is_fraud'] else '' for _ in row]

        st.dataframe(df.style.apply(highlight_fraud, axis=1), use_container_width=True)
        st.markdown(f"**🚨 Total Fraudulent Records:** `{df['is_fraud'].sum()}`")
    else:
        st.warning("⚠️ No fraud analysis has been run yet.")

    # ✅ Step 4: Compliance Check
    st.subheader("✅ Compliance Check")
    rules = load_rules()
    df['compliance_issues'] = df.apply(lambda row: check_compliance(row, rules), axis=1)

    if 'Transaction_ID' in df.columns:
        st.dataframe(df[['Transaction_ID', 'compliance_issues']])
    else:
        st.dataframe(df[['compliance_issues']])

    # ✅ Step 5: Send data + rules to LangChain Agent
    set_data(df, rules)

    # ✅ Step 6: LangChain Agent Chat
    st.subheader("🧠 AI Assistant (LangChain Agent)")
    query = st.text_input("Ask something about the data or rules...", key="ai_query")

   if st.button("Ask"):
    if query:
        agent = init_agent()
        try:
            result = agent.invoke({"input": query})  # ✅ Use invoke with input
            # 👇 Add this
            if isinstance(result, dict):
                response = result.get("output", "")
            else:
                response = str(result)

            # ✅ Format output if specific known case
            if "couldn't determine the exact number" in response:
                st.markdown(f"""
                    📋 **Summary**
                    - 🔢 **Total Records**: Likely more than 11  
                    - ⚠️ *Note*: The AI couldn't compute the exact number using available tools.
                """)
            else:
                st.success(response)

        except Exception as e:
            st.error(f"❌ Agent error: {str(e)}")

