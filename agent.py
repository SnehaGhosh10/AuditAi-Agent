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


def get_tools():
    return [
        Tool(name="ComplianceChecker", func=lambda x: "Run compliance rules"),
        Tool(name="FraudDetector", func=lambda x: "Use anomaly detector for frauds")
    ]

def init_agent():
    tools = get_tools()
    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
