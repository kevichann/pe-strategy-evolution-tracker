# scripts/05_visualize_trends.py

import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

INPUT_FILE = "PE_Strategy_Trends_Aggregated.csv"
OUTPUT_IMAGE = "visualizations/pe_strategy_evolution.png"


def plot_trends(df: pd.DataFrame):
    os.makedirs("visualizations", exist_ok=True)
    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(12, 6))
    ax = sns.lineplot(
        data=df,
        x="Year",
        y="Frequency",
        hue="Keyword",
        marker="o",
        linewidth=2.5
    )

    plt.title("Evolution of Private Equity Investment Strategies (2005–2025)", fontsize=14, fontweight="bold")
    plt.xlabel("Snapshot Year", fontsize=12)
    plt.ylabel("Term Frequency Across Portfolios", fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", title="Strategy Keywords")
    plt.tight_layout()

    plt.savefig(OUTPUT_IMAGE, dpi=300)
    print(f"Visualization saved to '{OUTPUT_IMAGE}'.")


def main():
    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print(f"Error: Could not find '{INPUT_FILE}'. Run 04_analyze_strategy_evolution.py first.")
        return

    # Filter to top key terms for a clean visualization
    target_terms = ["leveraged buyout", "value creation", "digital transformation", "platform", "operational improvement"]
    filtered_df = df[df["Keyword"].isin(target_terms)]

    plot_trends(filtered_df)


if __name__ == "__main__":
    main()
