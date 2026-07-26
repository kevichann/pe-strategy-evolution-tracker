# scripts/03_wayback_scraper.py

import csv
import re
import time
from typing import Dict, List, Optional
from urllib.parse import urlparse
import lxml.html
import pandas as pd
import requests

# --- Configuration ---
INPUT_FILE = "filtered_investors.csv"
OUTPUT_FILE = "PE_Strategy_Historical_Evolution.csv"

# Target years for historical snapshots
TARGET_YEARS = [2015, 2017, 2019, 2021, 2023, 2025]

# Strategy keywords to trace across snapshots
STRATEGY_KEYWORDS = [
    "buyout",
    "growth capital",
    "middle market",
    "value creation",
    "operational improvement",
    "software",
    "technology",
    "leveraged buyout",
    "organic growth",
    "digital transformation",
    "platform",
    "add-on",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def clean_domain(url: str) -> str:
    """Extracts clean domain name from a URL."""
    url = str(url).strip()
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    parsed = urlparse(url)
    return parsed.netloc if parsed.netloc else parsed.path


def get_wayback_snapshot_url(domain: str, year: int) -> Optional[str]:
    """Queries the Wayback Machine CDX API for the closest 200 OK snapshot in a given year."""
    cdx_url = "http://web.archive.org/cdx/search/cdx"
    params = {
        "url": domain,
        "output": "json",
        "fl": "timestamp,original,statuscode",
        "filter": "statuscode:200",
        "from": f"{year}0101",
        "to": f"{year}1231",
        "limit": 1,
    }

    try:
        response = requests.get(cdx_url, params=params, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if len(data) > 1:  # Index 0 is the header row
                timestamp, original_url, _ = data[1]
                return f"http://web.archive.org/web/{timestamp}/{original_url}"
    except Exception as e:
        print(f"  [CDX Error] {domain} ({year}): {e}")

    return None


def extract_keywords_from_snapshot(wayback_url: str) -> List[str]:
    """Fetches HTML from a Wayback URL and extracts matching strategy keywords."""
    try:
        response = requests.get(wayback_url, headers=HEADERS, timeout=15)
        if response.status_code != 200:
            return []

        tree = lxml.html.fromstring(response.content)

        # Remove noise elements
        for tag in tree.xpath("//script|//style|//nav|//footer|//header"):
            tag.getparent().remove(tag)

        text_content = re.sub(r"\s+", " ", tree.text_content().lower())
        found = [kw for kw in STRATEGY_KEYWORDS if kw in text_content]
        return sorted(found)

    except Exception:
        return []


def process_firm_historical_data(domain: str) -> Dict[str, str]:
    """Processes historical snapshots across all target years for a single firm domain."""
    firm_record = {"Domain": domain}

    for year in TARGET_YEARS:
        wayback_url = get_wayback_snapshot_url(domain, year)
        if wayback_url:
            keywords = extract_keywords_from_snapshot(wayback_url)
            firm_record[f"Keywords_{year}"] = (
                ", ".join(keywords) if keywords else "No keywords found"
            )
        else:
            firm_record[f"Keywords_{year}"] = "No Snapshot Available"

        # Politeness delay to prevent Wayback Machine 429 rate limiting
        time.sleep(1)

    return firm_record


def main():
    print(f"Loading target domains from {INPUT_FILE}...")
    try:
        df = pd.read_csv(INPUT_FILE)
        domains = (
            df["website"].dropna().apply(clean_domain).unique().tolist()
            if "website" in df.columns
            else df.iloc[:, 0].apply(clean_domain).unique().tolist()
        )
    except FileNotFoundError:
        print(f"Error: Could not find '{INPUT_FILE}'. Please run 01_filter_investors.py first.")
        return

    print(f"Starting historical analysis for {len(domains)} domains across target years: {TARGET_YEARS}...")
    results = []

    for idx, domain in enumerate(domains, 1):
        print(f"[{idx}/{len(domains)}] Processing domain: {domain}")
        record = process_firm_historical_data(domain)
        results.append(record)

    df_output = pd.DataFrame(results)
    df_output.to_csv(OUTPUT_FILE, index=False)
    print("-" * 50)
    print(f"Historical scraping complete. Results saved to '{OUTPUT_FILE}'.")


if __name__ == "__main__":
    main()
