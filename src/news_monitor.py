from duckduckgo_search import DDGS


FALLBACK_NEWS = [
    {
        "title": (
            "Port delays and supplier shortages disrupt electronics supply chains "
            "across key manufacturing hubs"
        ),
        "body": (
            "Manufacturers report shipment delays, component shortages, and rising "
            "logistics costs after congestion at major ports affected inbound materials."
        ),
    }
]


def fetch_supply_chain_news():

    query = "supply chain disruption"

    results = []

    try:
        with DDGS() as ddgs:

            news = ddgs.news(
                keywords=query,
                max_results=5
            )

            for item in news:

                results.append({
                    "title": item.get("title"),
                    "body": item.get("body")
                })
    except Exception as exc:
        print(f"News search failed, using fallback article: {exc}")
        return FALLBACK_NEWS

    return results or FALLBACK_NEWS
