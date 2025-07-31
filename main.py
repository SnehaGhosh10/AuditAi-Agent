import streamlit as st
import pandas as pd
from agent import init_agent, set_data
from fraud_detector import detect_fraud
from compliance_checker import load_rules, check_compliance
from parser import parse_csv

# ------------------- 🎨 Custom CSS for Styling -------------------
custom_css = """
<style>
    /* Background gradient */
    body {
        background: linear-gradient(to bottom right, #1e1e2f, #2d2d44);
        color: white;
    }
    .stApp {
        background-color: #1f1f2e;
    }
    /* Headers */
    .big-header {
        font-size: 2.4rem;
        font-weight: 700;
        background: linear-gradient(to right, #ff6f61, #ffcc70);
        -webkit-background-clip: text;
        color: transparent;
        text-align: center;
    }
    /* Containers */
    .rounded-box {
        background-color: #2b2b3a;
        padding: 20px;
        border-radius: 16px;
        margin-bottom: 30px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
    }
    /* Chat History */
    .chat {
        background-color: #262639;
        padding: 12px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ------------------ 🌐 Page Settings ------------------
st.set_page_config(page_title="AuditAI Agent", layout="wide", page_icon="📊")
st.markdown('<h1 class="big-header">📊 AuditAI Agent – Autonomous Financial Auditor</h1>', unsafe_allow_html=True)

# ------------------ 📤 Upload Section ------------------
st.markdown('<div class="rounded-box">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("📤 Upload a CSV File (e.g., salaries, expenses)", type=["csv"])
st.markdown('</div>', unsafe_allow_html=True)

# ------------------ 📊 Main Logic ------------------
if uploaded_file:
    df = parse_csv(uploaded_file)
    df = detect_fraud(df)

    st.markdown('<div class="rounded-box">', unsafe_allow_html=True)
    st.subheader("📄 Parsed Data")
    st.dataframe(df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="rounded-box">', unsafe_allow_html=True)
    st.subheader("🔍 Fraud Detection")

    if "is_fraud" in df.columns:
        df["Fraud Status"] = df["is_fraud"].apply(lambda x: "❌ Fraudulent" if x else "✅ Safe")

        def highlight_fraud(row):
            return ['background-color: #ffcccc' if row['is_fraud'] else '' for _ in row]

        st.dataframe(df.style.apply(highlight_fraud, axis=1), use_container_width=True)
        st.markdown(f"**🚨 Total Fraudulent Records:** `{df['is_fraud'].sum()}`")
    else:
        st.warning("⚠️ No fraud analysis has been run yet.")
    st.markdown('</div>', unsafe_allow_html=True)

    # ------------------ ✅ Compliance Check ------------------
    st.markdown('<div class="rounded-box">', unsafe_allow_html=True)
    st.subheader("✅ Compliance Check")
    rules = load_rules()
    df['compliance_issues'] = df.apply(lambda row: check_compliance(row, rules), axis=1)

    if 'Transaction_ID' in df.columns:
        st.dataframe(df[['Transaction_ID', 'compliance_issues']], use_container_width=True)
    else:
        st.dataframe(df[['compliance_issues']], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ------------------ 🤖 AI Agent with Memory ------------------
    st.markdown('<div class="rounded-box">', unsafe_allow_html=True)
    st.subheader("🧠 AI Assistant (LangChain Agent)")

    if "agent" not in st.session_state:
        st.session_state.agent = init_agent()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    query = st.text_input("💬 Ask something about the data or compliance rules...")

    if st.button("Ask"):
        if query:
            try:
                result = st.session_state.agent.invoke({"input": query})
                response = result.get("output") if isinstance(result, dict) else str(result)

                st.session_state.chat_history.append(("You", query))
                st.session_state.chat_history.append(("AuditAI", response))

                st.markdown("### 💬 Chat History")
                for role, message in st.session_state.chat_history:
                    st.markdown(f"<div class='chat'><strong>{role}:</strong> {message}</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Agent error: {str(e)}")
        else:
            st.warning("Please enter a question.")
    st.markdown('</div>', unsafe_allow_html=True)
