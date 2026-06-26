from app.env import require_env
from crewai import Agent, LLM

require_env("GROQ_API_KEY")

llm = LLM(
    model="groq/llama-3.3-70b-versatile"
)

network_visualizer = Agent(
    role="Supply Chain Network Visualizer",

    goal="""
    Identify impacted suppliers, determine their supply chain tier,
    identify affected components, and explain how the disruption
    propagates through the supply chain network.
    """,

    backstory="""
    You are an expert in supply chain mapping and dependency analysis.
    Your job is to identify suppliers affected by disruptions,
    determine whether they belong to Tier-1, Tier-2, or Tier-3,
    identify the impacted components, and explain how the disruption
    spreads through the supply chain.
    """,

    llm=llm,

    verbose=True
)