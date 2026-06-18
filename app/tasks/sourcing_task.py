from crewai import Task
from agents.sourcing_agent import sourcing_agent

sourcing_task = Task(
    description="""
    Recommend backup suppliers and mitigation plans
    for affected suppliers.
    """,

    expected_output="""
    Backup supplier recommendations and mitigation strategy.
    """,

    agent=sourcing_agent
)