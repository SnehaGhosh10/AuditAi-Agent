import streamlit as st
import pandas as pd
from agent import init_agent, set_data
from fraud_detector import detect_fraud
from compliance_checker import load_rules, check_compliance
from parser import parse_csv

# -------------- 🎨 Custom CSS for Modern Dual-Tone UI --------------
custom_css = """
<style>
    html, body, .stApp {
        background-color: #1f2235;
        background-image: linear-gradient(135deg, #1f2235 0%, #2c2f48 100%);
        color: #ffffff;
        font-family: 'Segoe UI', sans-serif;
    }

    .big-header {
        font-size: 2.6rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1.5rem;
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        -webkit-background-clip: text;
        color: transparent;
    }

    .rounded-box {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 24px;
        border-radius: 18px;
        margin-bottom: 30px;
        box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.35);
    }

    .chat {
        background-color: #282c4b;
        padding: 12px;
        border-radius: 12px;
        margin: 10px 0;
        color: #ffffff;
    }

    .stTextInput input, .stTextArea textarea {
        background-color: #2e324f;
        color: #ffffff;
    }

    .stButton button {
        background-color: #0072ff;
        color: #ffffff;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5em 1em;
    }

    .stDataFrame, .stDataEditor {
        background-color: #2e2f44;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# -------------- 🌐 Page Setup --------------
st.set_page_config(page_title="AuditAI Agent", layout="wide", page_icon="🧠")
st.markdown('<h1 class="big-header">📊 AuditAI Agent – Autonomous Financial Auditor</h1>', unsafe_allow_html=True)

# -------------- 📤 Upload CSV --------------
st.markdown('<div class="rounded-box">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("📤 Upload a CSV File (e.g., salaries, expenses)", type=["csv"])
st.markdown('</div>', unsafe_allow_html=True)

# -------------- 📊 Data Processing Logic --------------
if uploaded_file:
    df = parse_csv(uploaded_file)
    df = detect_fraud(df)

    # --------- Parsed Data ---------
    st.markdown('<div class="rounded-box">', unsafe_allow_html=True)
    st.subheader("📄 Parsed Data")
    st.dataframe(df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --------- Fraud Detection ---------
    st.markdown('<div class="rounded-box">', unsafe_allow_html=True)
    st.subheader("🚨 Fraud Detection")

    if "is_fraud" in df.columns:
        df["Fraud Status"] = df["is_fraud"].apply(lambda x: "❌ Fraudulent" if x else "✅ Safe")

        def highlight_fraud(row):
            return ['background-color: #661111' if row['is_fraud'] else '' for _ in row]

        st.dataframe(df.style.apply(highlight_fraud, axis=1), use_container_width=True)
        st.markdown(f"**🛑 Total Fraudulent Records:** `{df['is_fraud'].sum()}`")
    else:
        st.warning("⚠️ No fraud analysis detected.")
    st.markdown('</div>', unsafe_allow_html=True)

    # --------- Compliance Check ---------
    st.markdown('<div class="rounded-box">', unsafe_allow_html=True)
    st.subheader("✅ Compliance Check")
    rules = load_rules()
    df['compliance_issues'] = df.apply(lambda row: check_compliance(row, rules), axis=1)

    if 'Transaction_ID' in df.columns:
        st.dataframe(df[['Transaction_ID', 'compliance_issues']], use_container_width=True)
    else:
        st.dataframe(df[['compliance_issues']], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --------- AI Agent Interaction ---------
    st.markdown('<div class="rounded-box">', unsafe_allow_html=True)
    st.subheader("🧠 AI Assistant (LangChain Agent)")

    if "agent" not in st.session_state:
        st.session_state.agent = init_agent()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    query = st.text_input("💬 Ask a question about data, fraud, or compliance...")

    if st.button("Ask"):
        if query:
            try:
                result = st.session_state.agent.invoke({"input": query})
                response = result.get("output") if isinstance(result, dict) else str(result)

                st.session_state.chat_history.append(("You", query))
                st.session_state.chat_history.append(("AuditAI", response))

                st.markdown("### 🗨️ Chat History")
                for role, message in st.session_state.chat_history:
                    st.markdown(f"<div class='chat'><strong>{role}:</strong> {message}</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Agent error: {str(e)}")
        else:
            st.warning("Please enter a question.")
    st.markdown('</div>', unsafe_allow_html=True)
