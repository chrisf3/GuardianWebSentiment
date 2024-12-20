import matplotlib.pyplot as plt
import pandas as pd


def plot_over_time(data, metric="polarity", moving_average_window=5, save_path=None):
    # Convert data to DataFrame
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['publicationDate'])
    df = df.sort_values('date')

    # Select metric and compute moving average
    df[metric] = df['sentiment'].apply(lambda x: x[metric]) if metric == "polarity" else df['subjectivity']
    df['moving_average'] = df[metric].rolling(window=moving_average_window).mean()

    # Plot the metric over time
    plt.figure(figsize=(12, 6))
    plt.plot(df['date'], df[metric], label=f"{metric.capitalize()} Over Time", marker='o', linestyle='-', alpha=0.6)
    plt.plot(df['date'], df['moving_average'], label=f"Moving Average (Window={moving_average_window})", color='red',
             linewidth=2)
    plt.title(f"{metric.capitalize()} Over Time", fontsize=16)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel(metric.capitalize(), fontsize=12)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()


def plot_distribution(data, metric="polarity", bins=20, save_path=None):
    """
    Plots the distribution of a given metric (e.g., polarity or subjectivity).

    Args:
        data (list[dict]): List of articles with sentiment data.
        metric (str): The metric to plot ('polarity' or 'subjectivity').
        bins (int): Number of bins for the histogram.
    """
    # Convert data to DataFrame
    df = pd.DataFrame(data)
    df[metric] = df['sentiment'].apply(lambda x: x[metric]) if metric == "polarity" else df['subjectivity']

    # Plot the histogram
    plt.figure(figsize=(12, 6))
    plt.hist(df[metric], bins=bins, color='blue' if metric == "polarity" else 'green', alpha=0.7, edgecolor='black')
    plt.title(f"{metric.capitalize()} Distribution", fontsize=16)
    plt.xlabel(metric.capitalize(), fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()


def plot_polarity_vs_subjectivity(data, x_range=None, y_range=None, x_label="Polarity", y_label="Subjectivity", save_path=None):
    """
    Plots polarity against subjectivity as a scatter plot with optional axis ranges and titles.

    Args:
        data (list[dict]): List of articles with polarity and subjectivity data.
        x_range (tuple, optional): Tuple specifying the range for the X-axis (polarity).
        y_range (tuple, optional): Tuple specifying the range for the Y-axis (subjectivity).
        x_label (str): Label for the X-axis.
        y_label (str): Label for the Y-axis.
    """
    # Convert data to DataFrame
    df = pd.DataFrame(data)

    # Extract polarity and subjectivity
    df['polarity'] = df['sentiment'].apply(lambda x: x['polarity'])
    df['subjectivity'] = df['subjectivity']

    # Plot the scatter plot
    plt.figure(figsize=(12, 6))
    plt.scatter(df['polarity'], df['subjectivity'], alpha=0.7, c='purple', edgecolor='black')

    # Set axis limits if provided
    if x_range:
        plt.xlim(x_range)
    if y_range:
        plt.ylim(y_range)

    # Add labels and title
    plt.title("Polarity vs Subjectivity", fontsize=16)
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()


def plot_google_trends(trends_data, keyword, save_path=None):
    """
    Plots Google Trends data for the specified keyword.

    Args:
        trends_data (pd.DataFrame): DataFrame containing interest over time data.
        keyword (str): Keyword for the trend being plotted.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(trends_data['date'], trends_data[keyword], label=f"Google Trends: {keyword}", marker='o', linestyle='-')
    plt.title(f"Google Trends: {keyword}", fontsize=16)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Interest Over Time", fontsize=12)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()


def plot_overlap(sentiment_data, trends_data, keyword, moving_average_window=5, save_path=None):
    """
    Plots the overlap of sentiment polarity, subjectivity moving averages, and Google Trends data.

    Args:
        sentiment_data (list[dict]): List of articles with sentiment data.
        trends_data (pd.DataFrame): Google Trends data containing interest over time.
        keyword (str): The keyword for Google Trends data.
        moving_average_window (int): Window size for moving averages.
    """
    # Convert sentiment data to DataFrame
    sentiment_df = pd.DataFrame(sentiment_data)
    sentiment_df['date'] = pd.to_datetime(sentiment_df['publicationDate'])
    sentiment_df = sentiment_df.sort_values('date')
    sentiment_df['polarity_ma'] = sentiment_df['sentiment'].apply(lambda x: x['polarity']).rolling(window=moving_average_window).mean()
    sentiment_df['subjectivity_ma'] = sentiment_df['subjectivity'].rolling(window=moving_average_window).mean()

    # Standardize `date` columns to be timezone-naive
    trends_data['date'] = pd.to_datetime(trends_data['date']).dt.tz_localize(None)
    sentiment_df['date'] = pd.to_datetime(sentiment_df['date']).dt.tz_localize(None)

    # Merge with Google Trends data
    merged_data = pd.merge(sentiment_df, trends_data, on='date', how='inner')

    # Plot data
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot sentiment and subjectivity moving averages
    ax1.plot(merged_data['date'], merged_data['polarity_ma'], label="Polarity Moving Average", color='blue', linewidth=2)
    ax1.plot(merged_data['date'], merged_data['subjectivity_ma'], label="Subjectivity Moving Average", color='green', linewidth=2)

    # Set labels for the left Y-axis
    ax1.set_xlabel("Date", fontsize=12)
    ax1.set_ylabel("Polarity / Subjectivity", fontsize=12)
    ax1.tick_params(axis='y')
    ax1.legend(loc="upper left")

    # Plot Google Trends data on the secondary Y-axis
    ax2 = ax1.twinx()
    ax2.plot(merged_data['date'], merged_data[keyword], label=f"Google Trends: {keyword}", color='red', linewidth=2, linestyle='--')
    ax2.set_ylabel("Google Trends Interest", fontsize=12)
    ax2.tick_params(axis='y', colors='red')
    ax2.legend(loc="upper right")

    # Title and grid
    plt.title(f"Sentiment & Google Trends Overlap for '{keyword}'", fontsize=16)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()