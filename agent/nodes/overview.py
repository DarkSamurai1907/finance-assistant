import os
from finlight_client import FinlightApi, ApiConfig
from finlight_client.models import GetArticlesParams

from agent.tools import get_summary
from agent.state import State

def fetch_market_data(state: State) -> dict:
    client = FinlightApi(config=ApiConfig(api_key=os.environ.get("FINLIGHT_API_KEY")))
    params = GetArticlesParams(query="stock market", language="en")

    articles = client.articles.get_basic_articles(params=params)
    print(articles)

    news_summaries = [
        {
            "title": article.get('title'),
            "summary": article.get('summary'),
            "link": article.get('link'),
            "source": article.get('source'),
        }
        for article in articles.get('articles')
    ]

    return {
        "market_data": {
            "articles": news_summaries,
        }
    }

def summarize_consensus(state: State) -> dict:
    data = state["market_data"]
    article_summaries = "\n".join(
        f"- {item['title']} ({item['source']})" for item in data["articles"]
    )

    prompt = (
        f"Recent news headlines:\n{article_summaries}\n\n"
        "Based on the article headlines above, provide a high-level consensus of market sentiment."
    )

    summary = get_summary(prompt)
    return {"summary": summary}

__all__ = ["fetch_market_data", "summarize_consensus"]
