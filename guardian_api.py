
import requests
from config import CONFIG

def fetch_articles(section=None, keyword=None, max_articles=1000, year=None):
    """
    Fetches up to max_articles from The Guardian API with optional filtering by section, keyword, and date range,
    sorted by relevance.

    Args:
        section (str, optional): Filter articles by section (e.g., 'world', 'sport').
        keyword (str, optional): Search articles by a keyword (e.g., 'climate change').
        max_articles (int): Maximum number of articles to fetch.
        from_date (str, optional): Start date for filtering articles (format: YYYY-MM-DD).
        to_date (str, optional): End date for filtering articles (format: YYYY-MM-DD).

    Returns:
        list[dict]: A list of articles.
    """
    url = f"{CONFIG['GUARDIAN_BASE_URL']}/search"
    params = {
        **CONFIG["DEFAULT_PARAMS"],
        "api-key": CONFIG["GUARDIAN_API_KEY"],
        "page-size": 50,
        "order-by": "relevance",  # Sort results by relevance
    }

    from_date = f"{year}-01-01"
    to_date = f"{year}-06-30"

    if section:
        params["section"] = section.lower()  # Ensure section is lowercase
    if keyword:
        params["q"] = keyword
    if from_date:
        params["from-date"] = from_date  # Filter from this date
    if to_date:
        params["to-date"] = to_date  # Filter up to this date

    articles = []
    page = 1

    while len(articles) < max_articles:
        params["page"] = page
        response = requests.get(url, params=params)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch articles: {response.status_code} - {response.text}")

        data = response.json()
        results = data.get("response", {}).get("results", [])
        total_pages = data.get("response", {}).get("pages", 0)

        if not results:  # Stop if no more results
            break

        articles.extend(results)
        if len(articles) >= max_articles or page >= total_pages:  # Stop if max_articles or pages exceeded
            break

        page += 1

    return articles[:max_articles]  # Return up to max_articles