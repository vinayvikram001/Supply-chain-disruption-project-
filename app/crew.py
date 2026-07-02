import app.env
from crewai import Crew, Process

from app.agents.risk_manager import risk_manager
from app.agents.network_visualizer import network_visualizer
from app.agents.sourcing_agent import sourcing_agent

from app.tasks.risk_task import risk_task
from app.tasks.network_task import network_task
from app.tasks.sourcing_task import sourcing_task


crew = Crew(
    agents=[
        risk_manager,
        network_visualizer,
        sourcing_agent
    ],

    tasks=[
        risk_task,
        network_task,
        sourcing_task
    ],

    process=Process.sequential,

    verbose=True
)

result = crew.kickoff()

print(result)