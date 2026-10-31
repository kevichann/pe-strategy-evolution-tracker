# scripts/02_scrape_pe_strategies.py

import csv
import os
import re
import time
from urllib.parse import urljoin, urlparse
import lxml.html
import pandas as pd
import requests

INPUT_FILE = "filtered_investors.csv"
OUTPUT_FILE = "PE_Strategy_Implementation.csv"
MAX_COMPANIES = 100  # Target limit

# Candidate URL indicators for finding sub-pages
URL_KEYWORDS = [
    "strategy", "approach", "investment", "philosophy", "criteria",
    "value-add", "value-creation", "focus", "model", "sectors",
    "partnership", "process", "expertise", "about", "operational",
    "how-we-work", "what-we-do", "overview", "capabilities"
]

# Execution keywords used to score and rank descriptive text blocks
EXECUTION_KEYWORDS = [
    "partner", "management", "growth", "value creation", "operational",
    "acquisition", "equity", "capital", "portfolio", "strategic",
    "initiative", "build", "improve", "leverage", "buyout", "middle market",
    "sector", "expert", "scaling", "transformation", "platform", "add-on",
    "organic", "governance", "efficiency", "go-to-market", "digitization"
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def get_full_url(url: str) -> str:
    """Ensures input URL has a valid HTTP/HTTPS schema."""
    url = str(url).strip()
    return url if url.startswith(("http://", "https://")) else "https://" + url


def fetch_and_parse(url: str):
    """Fetches web page content and parses HTML into an lxml tree structure."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        tree = lxml.html.fromstring(response.content)
        tree.make_links_absolute(url)
        return tree
    except Exception:
        return None


def find_candidate_links(tree, base_url: str):
    """Discovers strategy-related internal links from a site's homepage."""
    if tree is None:
        return []
    domain = urlparse(base_url).netloc
    links = set()
    for _, _, link, _ in tree.iterlinks():
        parsed_link = urlparse(link)
        if domain in parsed_link.netloc:
            path = parsed_link.path.lower()
            if any(k in path for k in URL_KEYWORDS):
                clean_url = link.split("#")[0].rstrip("/")
                links.add(clean_url)
    return list(links)


def extract_meaningful_text(tree) -> str:
    """
    Extracts text blocks from HTML containers and ranks them based on 
    keyword density to isolate operational strategy positioning.
    """
    if tree is None:
        return ""

    # Remove non-content HTML tags
    for tag in tree.xpath("//script|//style|//nav|//footer|//header|//noscript"):
        tag.getparent().remove(tag)

    blocks = []
    # Query meaningful content containers
    for el in tree.xpath("//p | //li | //h1 | //h2 | //h3 | //div[not(div)]"):
        text = re.sub(r"\s+", " ", el.text_content().strip())
        if len(text) > 60:  # Ignore brief navigational elements
            blocks.append(text)

    if not blocks:
        return ""

    # Score blocks based on execution keyword frequency
    scored_blocks = []
    for b in blocks:
        b_lower = b.lower()
        score = sum(1 for kw in EXECUTION_KEYWORDS if kw in b_lower)
        if score > 0:
            scored_blocks.append((score, b))

    # Sort blocks by highest keyword relevance
    scored_blocks.sort(key=lambda x: x[0], reverse=True)

    if scored_blocks:
        top_text = [b[1] for b in scored_blocks[:5]]
        return " | ".join(top_text)

    # Fallback: Return top 2 descriptive blocks if no specific keywords matched
    return " | ".join(blocks[:2])


def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: Input file '{INPUT_FILE}' not found. Run 01_filter_investors.py first.")
        return

    # Robust CSV reading with dynamic column detection
    try:
        df_input = pd.read_csv(
            INPUT_FILE,
            on_bad_lines="skip",
            engine="python"
        )
        
        # Locate target website column dynamically
        col_name = None
        for col in df_input.columns:
            if any(k in str(col).lower() for k in ["web", "site", "url", "domain"]):
                col_name = col
                break
        
        if col_name is None:
            col_name = df_input.columns[0]

        # Slice to strictly target the first 100 companies
        urls = df_input[col_name].dropna().astype(str).head(MAX_COMPANIES).tolist()
        print(f"Successfully loaded the first {len(urls)} target URLs from '{INPUT_FILE}'.")
    except Exception as e:
        print(f"Error reading input CSV file: {e}")
        return

    print("Starting optimized live strategy scraping...")
    results = []

    for idx, site in enumerate(urls, 1):
        clean_site = str(site).strip('"').strip("'").strip()
        
        # Basic URL format validation
        if "." not in clean_site or len(clean_site) < 4:
            continue

        full_base_url = get_full_url(clean_site)
        print(f"[{idx}/{len(urls)}] Processing: {full_base_url}")

        home_tree = fetch_and_parse(full_base_url)
        content_pieces = []
        source_pages = []

        if home_tree is not None:
            source_pages.append(full_base_url)
            home_text = extract_meaningful_text(home_tree)
            if home_text:
                content_pieces.append(home_text)

            candidate_links = find_candidate_links(home_tree, full_base_url)
            # Prioritize sub-pages containing core strategy terms
            candidate_links.sort(
                key=lambda x: any(k in x.lower() for k in ["strategy", "approach", "value", "capabilities"]),
                reverse=True
            )

            for link in candidate_links[:2]:
                if link.rstrip("/") == full_base_url.rstrip("/"):
                    continue
                sub_tree = fetch_and_parse(link)
                sub_text = extract_meaningful_text(sub_tree)
                if sub_text:
                    content_pieces.append(sub_text)
                    source_pages.append(link)

        final_summary = " | ".join(content_pieces).strip() if content_pieces else "N/A"

        results.append({
            "Firm": clean_site,
            "Implementation_Details": final_summary if final_summary != "N/A" else None,
            "Source_Pages": ", ".join(source_pages) if source_pages else "Failed to Connect"
        })

        time.sleep(0.5)

    # Initialize DataFrame with explicit columns
    df_out = pd.DataFrame(results, columns=["Firm", "Implementation_Details", "Source_Pages"])
    df_out.to_csv(OUTPUT_FILE, index=False)

    success_count = df_out["Implementation_Details"].notna().sum()
    total_processed = len(df_out)
    pct = (success_count / total_processed * 100) if total_processed > 0 else 0.0

    print("-" * 50)
    print("Execution Finished!")
    print(f"Total Firms Processed: {total_processed}")
    print(f"Successful Strategy Extractions: {success_count} ({pct:.1f}% coverage)")
    print(f"Output saved to '{OUTPUT_FILE}'.")
    print("-" * 50)


if __name__ == "__main__":
    main()
