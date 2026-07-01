from src.news_monitor import fetch_supply_chain_news

def run_pipeline():
    news = fetch_supply_chain_news()

    print("Latest Disruptions:")
    for item in news:
        print(item["title"])

    return news