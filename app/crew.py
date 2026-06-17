from crewai import Crew

from agents.risk_manager import risk_manager
from agents.network_visualizer import network_visualizer
from agents.sourcing_agent import sourcing_agent


crew = Crew(
    agents=[
        risk_manager,
        network_visualizer,
        sourcing_agent
    ],

    verbose=True
)

print("Crew Created Successfully!")