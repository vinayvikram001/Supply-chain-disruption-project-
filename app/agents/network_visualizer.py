from crewai import Agent, LLM

llm = LLM(
    model="groq/llama-3.3-70b-versatile"
)

network_visualizer = Agent(
    role="Supply Chain Network Visualizer",

    goal="""
    Determine which suppliers are impacted by a disruption
    and trace the disruption across the supply chain network.
    """,

    backstory="""
    You are an expert in supply chain mapping and dependency analysis.
    Your job is to identify the suppliers affected by disruptions
    and understand how risks propagate through Tier-1, Tier-2,
    and Tier-3 supplier networks.
    """,

    llm=llm,

    verbose=True
)