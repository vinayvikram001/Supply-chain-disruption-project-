from crewai import Task

from app.agents.risk_manager import risk_manager
from app.agents.network_visualizer import network_visualizer
from app.agents.sourcing_agent import sourcing_agent


# -------------------------------
# Risk Assessment Task
# -------------------------------

risk_assessment_task = Task(
    description="""
    Analyze the following news article:

    {news_article}

    Determine:
    1. Type of disruption
    2. Risk level
    3. Severity score
    4. Location affected
    """,

    expected_output="""
    JSON format containing:
    risk_type,
    risk_level,
    severity_score,
    location
    """,

    agent=risk_manager
)


# -------------------------------
# Network Analysis Task
# -------------------------------

network_analysis_task = Task(
    description="""
    Using the disruption identified by the Risk Manager:

    1. Identify the affected supplier(s).
    2. Determine whether each supplier belongs to Tier 1, Tier 2, or Tier 3.
    3. Identify the affected component or material.
    4. Explain the downstream business impact on the supply chain.
    """,

    expected_output="""
    JSON format containing:
    supplier_name,
    supplier_tier,
    affected_component,
    business_impact
    """,

    agent=network_visualizer
)


# -------------------------------
# Alternative Sourcing Task
# -------------------------------

alternative_sourcing_task = Task(
    description="""
    Based on the affected supplier information:

    1. Recommend alternative supplier(s).
    2. Explain why they are suitable replacements.
    3. Describe how they reduce supply chain disruption.
    """,

    expected_output="""
    JSON format containing:
    alternative_supplier,
    recommendation_reason,
    expected_benefit
    """,

    agent=sourcing_agent
)