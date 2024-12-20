import os
from guardian_api import fetch_articles
from data_processing import process_articles, save_to_csv
from sentiment_analysis import analyze_articles
from visualization import (
    plot_over_time,
    plot_distribution,
    plot_polarity_vs_subjectivity,
    plot_google_trends,
    plot_overlap,
)
####from google_trends import fetch_trends_two_periods

STATIC_DIR = "static/images"


def process_keyword_year(keyword, year):
    """
    Main function to fetch, process, analyze, and visualize data dynamically based on inputs.
    """
    section = "world"
    max_articles = 1000
    moving_average_window = max(1, int(max_articles * 0.05))
    geo = ""

    # Ensure static images directory exists
    os.makedirs(STATIC_DIR, exist_ok=True)

    # Step 1: Fetch articles
    articles = fetch_articles(section=section, keyword=keyword, max_articles=max_articles, year=year)
    if not articles:
        raise ValueError("No articles found for the provided keyword.")

    # Step 2: Process and analyze articles
    processed_articles = process_articles(articles)
    analyzed_articles = analyze_articles(processed_articles)
    save_to_csv(analyzed_articles, os.path.join(STATIC_DIR, "guardian_articles.csv"))

    # Step 3: Fetch and visualize Google Trends data
   #### trends_data = fetch_trends_two_periods(keyword, year, geo=geo)
    ####if trends_data is not None:
        ####trends_file = os.path.join(STATIC_DIR, f"{keyword.replace(' ', '_')}_trends.csv")
        ####trends_data.to_csv(trends_file, index=False)

        ####plot_google_trends(trends_data, keyword, save_path=f"{STATIC_DIR}/google_trends.png")
        ####plot_overlap(analyzed_articles, trends_data, keyword, moving_average_window,
        ####  save_path=f"{STATIC_DIR}/overlap_plot.png")

    # Step 4: Visualize article data
    plot_over_time(analyzed_articles, metric="polarity", moving_average_window=moving_average_window,
                   save_path=f"{STATIC_DIR}/polarity_over_time.png")
    plot_over_time(analyzed_articles, metric="subjectivity", moving_average_window=moving_average_window,
                   save_path=f"{STATIC_DIR}/subjectivity_over_time.png")
    plot_distribution(analyzed_articles, metric="polarity", bins=20,
                      save_path=f"{STATIC_DIR}/polarity_distribution.png")
    plot_distribution(analyzed_articles, metric="subjectivity", bins=20,
                      save_path=f"{STATIC_DIR}/subjectivity_distribution.png")
    plot_polarity_vs_subjectivity(analyzed_articles, save_path=f"{STATIC_DIR}/polarity_vs_subjectivity.png")