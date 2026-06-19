from crewai import Task
from agents.network_visualizer import network_visualizer

network_task = Task(
    description="""
    Using the supplier dependency network,
    determine which suppliers are impacted.
    """,

    expected_output="""
    List of affected suppliers and their dependency chain.
    """,

    agent=network_visualizer
)