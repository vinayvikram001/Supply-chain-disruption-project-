from crewai import Task
from app.agents.sourcing_agent import sourcing_agent

sourcing_task = Task(
    description="""
Using the affected supplier information:

{network_task}

Recommend:

1. Alternative suppliers
2. Estimated lead time
3. Recovery strategy
4. Procurement recommendation
""",

    expected_output="""
Alternative suppliers
Lead time
Mitigation strategy
Recovery recommendation
""",

    agent=sourcing_agent
)