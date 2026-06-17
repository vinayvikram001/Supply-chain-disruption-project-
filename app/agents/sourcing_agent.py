from crewai import Agent

sourcing_agent = Agent(
    role="Alternative Sourcing Specialist",

    goal="""
    Recommend suitable backup suppliers and
    mitigation strategies during disruptions.
    """,

    backstory="""
    You are an expert procurement strategist
    specializing in contingency planning and
    supplier diversification.
    """,

    verbose=True
)