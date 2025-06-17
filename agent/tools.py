from finlight_client import FinlightApi, ApiConfig
from finlight_client.models import GetArticlesParams
from config import config

def fetch_articles(query: str, language: str = 'en', page_size: int = 5) -> list[dict]:
    """
    Fetches basic articles matching query from Finlight API.
    """
    client = FinlightApi(
        config=ApiConfig(api_key=config.FINLIGHT_API_KEY)
    )
    params = GetArticlesParams(
        query=query,
        language=language,
        pageSize=page_size
    )
    resp = client.articles.get_basic_articles(params=params)
    return resp.get('articles', [])
