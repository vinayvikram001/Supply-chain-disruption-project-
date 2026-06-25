from crewai import Task
from app.agents.risk_manager import risk_manager

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