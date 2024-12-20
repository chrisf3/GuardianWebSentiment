# sentiment_analysis.py

from textblob import TextBlob


def analyze_sentiment(text):
    """
    Analyzes the sentiment of the provided text.

    Returns:
        dict: Sentiment polarity and subjectivity.
    """
    blob = TextBlob(text)
    return {
        "polarity": blob.sentiment.polarity,
        "subjectivity": blob.sentiment.subjectivity
    }


def analyze_articles(articles):
    """
    Applies sentiment and subjectivity analysis to a list of articles.

    Args:
        articles (list[dict]): List of articles with 'text' key.

    Returns:
        list[dict]: Articles with added sentiment and subjectivity data.
    """
    for article in articles:
        sentiment = analyze_sentiment(article["text"])
        article["sentiment"] = sentiment
        article["subjectivity"] = sentiment["subjectivity"]  # Add subjectivity directly to the article
    return articles