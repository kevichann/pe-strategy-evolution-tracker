# 02_scrape_pe_strategies.py
import re
import time
from urllib.parse import urlparse
import pandas as pd
import requests
import lxml.html

INPUT_FILE = 'PESites.xlsx'
OUTPUT_FILE = 'PE_Strategy_Implementation.csv'

URL_KEYWORDS = ["strategy", "approach", "investment", "philosophy", "value-add", "focus"]
IMPLEMENTATION_KEYWORDS = ["partner", "management", "growth", "value", "operational", "acquisition"]
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def get_full_url(url):
    url = str(url).strip()
    return url if url.startswith(('http://', 'https://')) else 'https://' + url

def fetch_and_parse(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        tree = lxml.html.fromstring(response.content)
        tree.make_links_absolute(url)
        return tree
    except Exception:
        return None

def extract_meaningful_text(tree):
    if tree is None: 
        return ""
    for tag in tree.xpath('//script|//style|//nav|//footer|//header'):
        tag.getparent().remove(tag)

    blocks = []
    for el in tree.xpath('//p | //li | //div[not(div)] | //h1 | //h2 | //h3'):
        text = re.sub(r'\s+', ' ', el.text_content().strip())
        if len(text) > 80:
            blocks.append(text)

    relevant_blocks = [b for b in blocks if any(k in b.lower() for k in IMPLEMENTATION_KEYWORDS)]
    return " ".join(relevant_blocks[:5]) if relevant_blocks else " ".join(blocks[:2])

def main():
    try:
        df_input = pd.read_excel(INPUT_FILE, header=None)
        urls = df_input[0].tolist()
    except Exception as e:
        print(f"Error loading input file: {e}")
        return

    results = []
    for site in urls:
        if "." not in str(site): 
            continue
        full_url = get_full_url(site)
        tree = fetch_and_parse(full_url)
        summary = extract_meaningful_text(tree)

        results.append({
            'Firm': site,
            'Strategy_Implementation': summary if summary else "N/A"
        })
        time.sleep(0.5)

    pd.DataFrame(results).to_csv(OUTPUT_FILE, index=False)
    print(f"Analysis complete. Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
