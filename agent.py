# agent.py

from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Read the API key
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq LLM
llm = ChatGroq(
    api_key=groq_api_key,
    model_name="mixtral-8x7b-32768"
)

# Define tool functions (dummy for now)
def run_compliance_checker(query: str) -> str:
    return "Run compliance rules – this is a placeholder response."

def run_fraud_detector(query: str) -> str:
    return "Use anomaly detector – this is a placeholder response."

# Define tools with descriptions
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
            description="Use this to identify or ask about potential frauds or anomalies in the transactions"
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
