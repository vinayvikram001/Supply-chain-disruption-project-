from crewai import Agent, LLM

llm = LLM(
    model="groq/llama-3.3-70b-versatile"
)

risk_manager = Agent(
    role="Supply Chain Risk Manager",

    goal="""
    Assess disruption severity from news events
    and classify them into Low, Medium, or High risk.
    """,

    backstory="""
    You are an experienced supply chain risk analyst.
    You specialize in evaluating global disruptions
    such as natural disasters, strikes, geopolitical
    conflicts, and supplier failures.
    """,

    llm=llm,

    verbose=True
)