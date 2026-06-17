from crewai import Agent

network_visualizer = Agent(
    role="Supply Chain Network Analyst",

    goal="""
    Identify all suppliers affected by a disruption
    using the supplier dependency graph.
    """,

    backstory="""
    You understand complex supplier relationships
    across Tier 1, Tier 2, and Tier 3 networks.
    You determine the blast radius of disruptions.
    """,

    verbose=True
)