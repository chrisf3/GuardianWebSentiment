# data_processing.py

import pandas as pd


def process_articles(articles):
    """
    Processes raw article data into a structured format.

    Args:
        articles (list[dict]): List of raw articles.

    Returns:
        list[dict]: Processed articles.
    """
    processed = []
    for article in articles:
        processed.append({
            "id": article.get("id"),
            "webTitle": article.get("webTitle"),
            "sectionName": article.get("sectionName"),
            "webUrl": article.get("webUrl"),
            "text": article.get("fields", {}).get("bodyText", ""),
            "publicationDate": article.get("webPublicationDate")  # Add publication date
        })
    return processed


def save_to_csv(articles, filename):
    """
    Saves processed articles to a CSV file.

    Args:
        articles (list[dict]): List of processed articles.
        filename (str): Output filename.
    """
    df = pd.DataFrame(articles)
    df.to_csv(filename, index=False)
    print(f"Saved {len(articles)} articles to {filename}")