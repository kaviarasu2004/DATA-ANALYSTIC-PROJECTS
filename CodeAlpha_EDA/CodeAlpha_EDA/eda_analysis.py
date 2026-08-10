"""
CodeAlpha Data Analytics Internship - Task 2: Exploratory Data Analysis (EDA)
================================================================================
Performs a full exploratory analysis on the book catalogue dataset produced
by CodeAlpha_WebScraping: structure inspection, data cleaning, descriptive
statistics, missing-value / outlier checks, correlation analysis, and
hypothesis validation — with all findings written to eda_outputs/report.md
and supporting charts saved as PNG files.

Usage:
    python eda_analysis.py --input books.csv --outdir eda_outputs
"""

import argparse
import os
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")


def load_and_clean(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    # --- Structure / dtypes ---
    df["price_gbp"] = pd.to_numeric(df["price_gbp"], errors="coerce")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["in_stock_count"] = pd.to_numeric(df["in_stock_count"], errors="coerce")

    # --- Deduplication ---
    before = len(df)
    df = df.drop_duplicates(subset=["title", "product_page_url"])
    removed = before - len(df)

    # --- Drop rows with no price or rating (core fields) ---
    df = df.dropna(subset=["price_gbp", "rating"])

    df.attrs["duplicates_removed"] = removed
    return df


def missing_value_report(df: pd.DataFrame) -> pd.DataFrame:
    missing = df.isna().sum()
    pct = (missing / len(df) * 100).round(2)
    return pd.DataFrame({"missing_count": missing, "missing_pct": pct})


def detect_price_outliers(df: pd.DataFrame) -> pd.DataFrame:
    q1, q3 = df["price_gbp"].quantile([0.25, 0.75])
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return df[(df["price_gbp"] < lower) | (df["price_gbp"] > upper)]


def make_charts(df: pd.DataFrame, outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)

    # 1. Price distribution
    plt.figure(figsize=(8, 5))
    sns.histplot(df["price_gbp"], bins=30, kde=True, color="#4C72B0")
    plt.title("Distribution of Book Prices")
    plt.xlabel("Price (£)")
    plt.tight_layout()
    plt.savefig(outdir / "price_distribution.png", dpi=150)
    plt.close()

    # 2. Rating distribution
    plt.figure(figsize=(7, 5))
    sns.countplot(x="rating", data=df, hue="rating", palette="viridis", legend=False)
    plt.title("Distribution of Star Ratings")
    plt.xlabel("Rating (stars)")
    plt.ylabel("Number of books")
    plt.tight_layout()
    plt.savefig(outdir / "rating_distribution.png", dpi=150)
    plt.close()

    # 3. Price vs rating
    plt.figure(figsize=(8, 5))
    sns.boxplot(x="rating", y="price_gbp", hue="rating", data=df, palette="crest", legend=False)
    plt.title("Price by Star Rating")
    plt.xlabel("Rating (stars)")
    plt.ylabel("Price (£)")
    plt.tight_layout()
    plt.savefig(outdir / "price_by_rating.png", dpi=150)
    plt.close()

    # 4. Correlation heatmap
    plt.figure(figsize=(5, 4))
    numeric_cols = df[["price_gbp", "rating", "in_stock_count"]]
    sns.heatmap(numeric_cols.corr(), annot=True, cmap="coolwarm", vmin=-1, vmax=1)
    plt.title("Correlation Matrix")
    plt.tight_layout()
    plt.savefig(outdir / "correlation_heatmap.png", dpi=150)
    plt.close()

    # 5. Top categories
    plt.figure(figsize=(9, 5))
    top_cats = df["category"].value_counts().head(10)
    sns.barplot(x=top_cats.values, y=top_cats.index, hue=top_cats.index, palette="mako", legend=False)
    plt.title("Top 10 Categories by Number of Books")
    plt.xlabel("Number of books")
    plt.tight_layout()
    plt.savefig(outdir / "top_categories.png", dpi=150)
    plt.close()


def write_report(df: pd.DataFrame, missing_df: pd.DataFrame, outliers: pd.DataFrame, outdir: Path) -> None:
    corr = df[["price_gbp", "rating", "in_stock_count"]].corr()
    price_rating_corr = corr.loc["price_gbp", "rating"]

    top_category = df["category"].value_counts().idxmax()
    avg_price = df["price_gbp"].mean()
    median_price = df["price_gbp"].median()
    avg_rating = df["rating"].mean()
    out_of_stock_pct = (df["availability"] == "Out of stock").mean() * 100

    lines = []
    lines.append("# Exploratory Data Analysis Report\n")
    lines.append(f"**Dataset size (after cleaning):** {len(df)} books  ")
    lines.append(f"**Duplicate rows removed:** {df.attrs.get('duplicates_removed', 0)}\n")

    lines.append("## 1. Data Structure\n")
    lines.append("| Column | Dtype |")
    lines.append("|---|---|")
    for col, dtype in df.dtypes.items():
        lines.append(f"| {col} | {dtype} |")
    lines.append("")

    lines.append("## 2. Missing Values\n")
    lines.append(missing_df.to_markdown())
    lines.append("")

    lines.append("## 3. Descriptive Statistics\n")
    lines.append(df[["price_gbp", "rating", "in_stock_count"]].describe().round(2).to_markdown())
    lines.append("")

    lines.append("## 4. Outlier Detection (Price, IQR method)\n")
    lines.append(f"Detected **{len(outliers)}** price outliers out of {len(df)} records "
                  f"({len(outliers) / len(df) * 100:.1f}%).\n")

    lines.append("## 5. Key Findings\n")
    lines.append(f"- The most common category is **{top_category}**, "
                  f"with {df['category'].value_counts().max()} titles.")
    lines.append(f"- Average book price is **£{avg_price:.2f}** (median £{median_price:.2f}).")
    lines.append(f"- Average star rating across the catalogue is **{avg_rating:.2f} / 5**.")
    lines.append(f"- **{out_of_stock_pct:.1f}%** of books are currently out of stock.")
    lines.append(f"- Correlation between price and rating: **{price_rating_corr:.3f}** "
                  f"({'weak/negligible' if abs(price_rating_corr) < 0.2 else 'moderate' if abs(price_rating_corr) < 0.5 else 'strong'}).")
    lines.append("")

    lines.append("## 6. Hypothesis Validation\n")
    lines.append("**H0: Higher-rated books are not priced differently from lower-rated books.**\n")
    grouped = df.groupby("rating")["price_gbp"].mean().round(2)
    lines.append(grouped.to_frame("avg_price_gbp").to_markdown())
    verdict = "rejected — a rating-linked price pattern is visible" if abs(price_rating_corr) >= 0.2 \
        else "not rejected — price does not meaningfully depend on rating in this dataset"
    lines.append(f"\n**Verdict:** {verdict}.\n")

    lines.append("## 7. Charts\n")
    lines.append("See the `charts/` folder for: `price_distribution.png`, `rating_distribution.png`, "
                  "`price_by_rating.png`, `correlation_heatmap.png`, `top_categories.png`.\n")

    outdir.mkdir(parents=True, exist_ok=True)
    with open(outdir / "report.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    parser = argparse.ArgumentParser(description="Run EDA on the scraped books dataset.")
    parser.add_argument("--input", type=str, default="books.csv", help="Path to input CSV.")
    parser.add_argument("--outdir", type=str, default="eda_outputs", help="Output directory.")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    df = load_and_clean(args.input)
    missing_df = missing_value_report(df)
    outliers = detect_price_outliers(df)

    make_charts(df, outdir / "charts")
    write_report(df, missing_df, outliers, outdir)

    print(f"EDA complete. Report and charts saved to '{outdir}/'")


if __name__ == "__main__":
    main()
