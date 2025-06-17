import requests
from finlight_client import FinlightApi, ApiConfig
from finlight_client.models import GetArticlesParams
from config import config

def fetch_articles(query: str, language: str = 'en', page_size: int = 5) -> str:
    """
    Fetches real-time financial news articles about a specific company, index, or topic using the Finlight API.

    Use this tool when the user asks for:
    - How the market is doing
    - What’s happening with a specific company or stock (e.g. "What's going on with Apple?")
    - Market sentiment or recent developments
    - News or updates about a symbol or financial topic

    Provide the company name, stock ticker, or general topic as the 'query'. This tool returns a list of news articles with summaries and links to sources.
    """
    client = FinlightApi(
        config=ApiConfig(api_key=config.FINLIGHT_API_KEY)
    )
    params = GetArticlesParams(
        query=query,
        language=language,
        pageSize=page_size
    )
    articles = client.articles.get_basic_articles(params=params).get("articles", [])
    if not articles:
        return f"No recent news found for '{query}'."

    formatted = "\n".join(
        f"- {a['title']} ({a['source']}) — {a['summary']}"
        for a in articles if a.get("title")
    )
    return f"Here are recent headlines for '{query}':\n{formatted}"


def stock_forecast(symbol: str, market: str = "NSE") -> str:
    """
    Retrieves analyst forecast data for the given stock symbol using TradingView (via Jina AI proxy).

    Use this tool when the user asks for:
    - Price targets or price expectations for a stock
    - Future outlook or forecast for a stock
    - Analyst opinions on whether to buy, sell, or hold
    - What experts or analysts predict about a company's stock performance

    This tool is different from fetch_articles, which returns news. Use this for structured forecast insights like average price target, analyst consensus (buy/hold/sell), and valuation expectations.

    Args:
        symbol: Ticker symbol (e.g. "TSLA", "RELIANCE")
        market: Stock exchange, "NSE" or "NASDAQ" (default: NSE)

    Returns:
        Analyst forecast and sentiment summary as plain text.
    """
    market_prefix = market.upper()
    url = f"https://r.jina.ai/https://www.tradingview.com/symbols/{market_prefix}-{symbol}/forecast/"
    headers = {"Authorization": f"Bearer {config.JINA_API_KEY}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.text

def stock_fundamentals(symbol: str, market: str = "NASDAQ") -> str:
    """
    Retrieves a financial fundamentals overview for the given stock from TradingView via Jina proxy.

    Use this tool when the user asks about:
    - A company’s financial health
    - Valuation metrics like PE ratio, EPS, market cap
    - Balance sheet, income statement, or profitability
    - Whether a stock is fundamentally strong or weak

    This tool is useful for answering questions like:
    - “Is Apple a good long-term investment?”
    - “What are the fundamentals of Reliance?”
    - “Show me valuation info for AAPL.”

    Args:
        symbol: Ticker symbol (e.g. "AAPL", "VBL")
        market: Market code ("NASDAQ" or "NSE"). MAKE SURE TO USE NASDAQ FOR US STOCKS!

    Returns:
        Key fundamentals and financial ratios in plain text.
    """
    market_prefix = market.upper()
    url = f"https://r.jina.ai/https://www.tradingview.com/symbols/{market_prefix}-{symbol}/financials-overview/"
    headers = {"Authorization": f"Bearer {config.JINA_API_KEY}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.text

def stock_technicals(symbol: str, market: str = "NASDAQ") -> str:
    """
    Retrieves technical analysis indicators for the given stock symbol using TradingView via Jina.

    Use this tool when the user asks about:
    - Momentum, trends, or chart-based signals
    - Indicators like RSI, MACD, moving averages
    - Short-term buying/selling opportunities
    - Support and resistance levels

    Use this when a user asks:
    - “Is now a good time to buy Tesla?”
    - “What are the technicals for GOOGL?”
    - “Show me momentum indicators for HDFCBANK.”

    This tool gives short-term insights, unlike fundamentals or forecasts.

    Args:
        symbol: Ticker symbol (e.g. "GOOGL", "SAIL")
        market: Market code ("NASDAQ" or "NSE"). MAKE SURE TO USE NASDAQ FOR US STOCKS!

    Returns:
        A summary of technical indicators and signals.
    """
    market_prefix = market.upper()
    url = f"https://r.jina.ai/https://www.tradingview.com/symbols/{market_prefix}-{symbol}/technicals/"
    headers = {"Authorization": f"Bearer {config.JINA_API_KEY}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.text
