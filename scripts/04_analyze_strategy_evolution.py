# scripts/04_analyze_strategy_evolution.py

import pandas as pd

INPUT_FILE = "PE_Strategy_Historical_Wayback.csv"
OUTPUT_FILE = "PE_Strategy_Trends_Aggregated.csv"


def calculate_keyword_frequencies(df: pd.DataFrame) -> pd.DataFrame:
    year_cols = [c for c in df.columns if c.startswith("Keywords_")]
    trend_records = []

    for col in year_cols:
        year = col.replace("Keywords_", "")
        keyword_counts = {}

        for entry in df[col].dropna():
            if entry in ["No Snapshot", "None Detected"]:
                continue
            keywords = [k.strip() for k in entry.split(",")]
            for k in keywords:
                keyword_counts[k] = keyword_counts.get(k, 0) + 1

        for kw, count in keyword_counts.items():
            trend_records.append({"Year": year, "Keyword": kw, "Frequency": count})

    return pd.DataFrame(trend_records)


def main():
    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print(f"Error: Could not find '{INPUT_FILE}'. Run 03_wayback_scraper.py first.")
        return

    trends_df = calculate_keyword_frequencies(df)
    trends_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Analysis complete. Aggregated trends saved to '{OUTPUT_FILE}'.")


if __name__ == "__main__":
    main()
