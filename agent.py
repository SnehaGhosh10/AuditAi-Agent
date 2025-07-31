from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# 🔐 Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# 🔁 Setup LLM
llm = ChatGroq(
    api_key=groq_api_key,
    model_name="llama3-70b-8192",
    temperature=0.0
)

# 🌐 Global variables for uploaded data
dataframe = None
rules = None

# ⬆️ Call from main.py after uploading data
def set_data(df, rule_list=None):
    global dataframe, rules
    dataframe = df
    rules = rule_list if rule_list else []

# ✅ Compliance checker tool
def run_compliance_checker(query: str) -> str:
    if dataframe is None or dataframe.empty:
        return "No data loaded. Please upload a valid file."
    
    if 'compliance_issues' not in dataframe.columns:
        return "Compliance issues not found. Please run compliance check first."

    non_compliant = dataframe[dataframe['compliance_issues'].astype(str) != "[]"]
    count = len(non_compliant)

    if count == 0:
        return "✅ All transactions are compliant."
    return f"❌ {count} non-compliant transactions found."

# ✅ Fraud detector tool
def run_fraud_detector(query: str) -> str:
    if dataframe is None or dataframe.empty:
        return "No data loaded. Please upload a valid file."
    
    if 'is_fraud' not in dataframe.columns:
        return "Fraud detection not yet performed. Please run it before querying."

    frauds = dataframe[dataframe['is_fraud'] == True]
    count = len(frauds)

    if count == 0:
        return "✅ No fraudulent transactions detected."
    return f"🚨 {count} potentially fraudulent transactions detected."

# 🧰 Register tools
def get_tools():
    return [
        Tool(
            name="ComplianceChecker",
            func=run_compliance_checker,
            description="Use this to ask about compliance violations or rules."
        ),
        Tool(
            name="FraudDetector",
            func=run_fraud_detector,
            description="Use this to ask about frauds detected in the data."
        )
    ]

# 🧠 Conversation memory object
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 🤖 Initialize LangChain agent with memory
def init_agent():
    tools = get_tools()

    # System prompt
    system_prompt = PromptTemplate.from_template(
        "You are a helpful and intelligent AI Financial Auditor. "
        "Use available tools to answer the user's questions clearly and precisely. "
        "Focus only on the data and tools provided. "
        "Question: {input}"
    )

    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        memory=memory,  # ✅ Add memory here
        agent_kwargs={"system_message": system_prompt.format(input="{input}")}
    )
