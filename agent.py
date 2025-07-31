from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    api_key=groq_api_key,
    model_name="mixtral-8x7b-32768"
)

# Globals for agent
dataframe = None
rules = None

def set_data(df, rule_list):
    global dataframe, rules
    dataframe = df
    rules = rule_list

def run_compliance_checker(query: str) -> str:
    if dataframe is None:
        return "Data not loaded."
    non_compliant = dataframe[dataframe['compliance_issues'].astype(str) != "[]"]
    return f"There are {len(non_compliant)} non-compliant transactions."

def run_fraud_detector(query: str) -> str:
    if dataframe is None:
        return "Data not loaded."
    if 'is_fraud' not in dataframe.columns:
        return "Fraud detection has not been run yet."
    frauds = dataframe[dataframe['is_fraud'] == True]
    return f"{len(frauds)} potentially fraudulent transactions detected."

def get_tools():
    return [
        Tool(
            name="ComplianceChecker",
            func=run_compliance_checker,
            description="Use this to check or ask about compliance rules or issues in the data"
        ),
        Tool(
            name="FraudDetector",
            func=run_fraud_detector,
            description="Use this to check or ask about fraudulent transactions"
        )
    ]

def init_agent():
    tools = get_tools()
    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
