from crewai import Task
from agents.risk_manager import risk_manager

risk_task = Task(
    description="""
    Analyze the disruption event and determine
    whether the risk level is Low, Medium, or High.
    Explain your reasoning.
    """,

    expected_output="""
    Risk Level: Low/Medium/High
    Explanation of why this classification was made.
    """,

    agent=risk_manager
)