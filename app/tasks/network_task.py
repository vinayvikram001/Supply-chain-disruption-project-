from crewai import Task
from app.agents.network_visualizer import network_visualizer

network_task = Task(
    description="""
Using the following risk assessment:

{risk_task}

Determine:

1. Which suppliers are affected
2. Which supplier tier is affected
3. Which components may be impacted
4. Explain the dependency chain.
""",

    expected_output="""
Affected suppliers
Supplier tier
Affected components
Dependency chain
""",

    agent=network_visualizer
)