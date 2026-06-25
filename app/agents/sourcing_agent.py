from app.env import require_env
from crewai import Agent, LLM


require_env("GROQ_API_KEY")

llm = LLM(
    model="groq/llama-3.3-70b-versatile"
)

sourcing_agent = Agent(
    role="Alternative Sourcing Specialist",

    goal="""
    Recommend suitable backup suppliers and mitigation
    strategies to reduce supply chain disruptions.
    """,

    backstory="""
    You are a procurement expert specializing in supplier
    diversification and contingency planning. You evaluate
    supplier capabilities and recommend alternative sourcing
    options to maintain business continuity.
    """,

    llm=llm,

    verbose=True
)
