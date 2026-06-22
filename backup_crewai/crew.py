from dotenv import load_dotenv
load_dotenv()

from crewai import Crew

from agents.risk_manager import risk_manager
from agents.network_visualizer import network_visualizer
from agents.sourcing_agent import sourcing_agent

from tasks.risk_task import risk_task
from tasks.network_task import network_task
from tasks.sourcing_task import sourcing_task


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

    verbose=True
)

result = crew.kickoff()

print(result)