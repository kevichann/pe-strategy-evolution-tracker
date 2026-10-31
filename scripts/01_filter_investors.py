# 01_filter_investors.py
import pandas as pd

DEFAULT_INPUT_FILENAME = "investorAll.csv"
DEFAULT_OUTPUT_FILENAME = "filtered_investors.csv"

def filter_investors(input_filename, output_filename=DEFAULT_OUTPUT_FILENAME):
    """
    Loads investor data, filters based on active status, primary type,
    and valid website, and exports the clean dataset.
    """
    print(f"Loading data from file path: {input_filename}...")
    try:
        df = pd.read_csv(input_filename)
    except FileNotFoundError:
        print(f"Error: '{input_filename}' not found.")
        return

    # Filtering logic
    condition_status = df['investorstatus'].fillna('') != 'Out of Business'
    condition_type = df['primaryinvestortype'].fillna('') == 'PE/Buyout'
    condition_website = df['website'].notna() & (df['website'].astype(str).str.strip().astype(bool))

    df_filtered = df[condition_status & condition_type & condition_website]
    df_filtered.to_csv(output_filename, index=False)
    print(f"Filtered {len(df_filtered)} rows. Saved to '{output_filename}'.")

if __name__ == "__main__":
    filter_investors(DEFAULT_INPUT_FILENAME)
