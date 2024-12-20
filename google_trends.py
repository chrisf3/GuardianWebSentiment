from pytrends.request import TrendReq
import pandas as pd
import time

def fetch_trends_two_periods(keyword, year, geo=""):
    """
    Fetch Google Trends data for a year by dividing it into two 6-month periods.

    Args:
        keyword (str): Keyword to fetch data for.
        year (int): Year to fetch data for (e.g., 2024).
        geo (str): Geographical region (e.g., 'US'). Default is worldwide ('').

    Returns:
        pd.DataFrame: Combined DataFrame with trends data for the whole year.
    """
    pytrends = TrendReq(hl='en-US', tz=360)
    intervals = [
        (f"{year}-01-01", f"{year}-03-31"),
        (f"{year}-04-01", f"{year}-06-30"),
        (f"{year}-07-01", f"{year}-09-30"),
        (f"{year}-10-01", f"{year}-12-31"),
    ]
    all_data = []

    for start_date, end_date in intervals:
        try:
            print(f"Fetching data for {start_date} to {end_date}...")
            pytrends.build_payload([keyword], timeframe=f"{start_date} {end_date}", geo=geo)
            data = pytrends.interest_over_time()

            if data.empty:
                print(f"No data available for {start_date} to {end_date}.")
                continue

            # Drop 'isPartial' column if it exists
            if 'isPartial' in data.columns:
                data = data.drop(columns=['isPartial'])

            all_data.append(data)

            # Respect rate limits
            time.sleep(10)  # Delay between requests to avoid 429 errors

        except Exception as e:
            print(f"Error fetching data for {start_date} to {end_date}: {e}")
            time.sleep(10)  # Delay between requests to avoid 429 errors

    # Merge the two periods
    if all_data:
        combined_data = pd.concat(all_data)
        # Remove duplicate rows if they exist (e.g., overlapping weeks at the boundary)
        combined_data = combined_data[~combined_data.index.duplicated(keep='first')].reset_index()
        return combined_data
    else:
        print("No data fetched for the entire year.")
        return None

