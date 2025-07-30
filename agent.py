# agent.py
from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType

llm = ChatGroq(temperature=0, model_name="mixtral-8x7b-32768")

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
