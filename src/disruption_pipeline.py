from app.env import require_env
from crewai import Crew
from src.news_monitor import fetch_supply_chain_news
from app.agents.tasks import risk_assessment_task


def run_pipeline():
    require_env("GROQ_API_KEY")

    news = fetch_supply_chain_news()

    if not news:
        print("No news articles found.")
        return

    article = news[0]["title"]

    print("\nLATEST ARTICLE:")
    print(article)

    crew = Crew(
        agents=[
            risk_assessment_task.agent
        ],
        tasks=[
            risk_assessment_task
        ],
        verbose=True
    )

    result = crew.kickoff(
        inputs={
            "news_article": article
        }
    )

    print("\nRISK ANALYSIS:")
    print(result)

    return result


if __name__ == "__main__":
    run_pipeline()
