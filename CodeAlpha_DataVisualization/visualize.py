"""
CodeAlpha Data Analytics Internship - Task 3: Data Visualization
====================================================================
Builds a set of individual insight charts PLUS a combined multi-panel
dashboard image from the book catalogue dataset, using Matplotlib and
Seaborn.

Usage:
    python visualize.py --input books.csv --outdir dashboard
"""

import argparse
from pathlib import Path

import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

sns.set_theme(style="whitegrid", palette="deep")


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["price_gbp"] = pd.to_numeric(df["price_gbp"], errors="coerce")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["in_stock_count"] = pd.to_numeric(df["in_stock_count"], errors="coerce")
    return df.dropna(subset=["price_gbp", "rating"])


def build_dashboard(df: pd.DataFrame, outpath: Path) -> None:
    fig, axes = plt.subplots(2, 3, figsize=(20, 11))
    fig.suptitle("Book Catalogue — Analytics Dashboard", fontsize=20, fontweight="bold")

    # 1. Price distribution
    sns.histplot(df["price_gbp"], bins=25, kde=True, ax=axes[0, 0], color="#4C72B0")
    axes[0, 0].set_title("Price Distribution")
    axes[0, 0].set_xlabel("Price (£)")

    # 2. Rating countplot
    sns.countplot(x="rating", data=df, hue="rating", palette="viridis", legend=False, ax=axes[0, 1])
    axes[0, 1].set_title("Rating Distribution")
    axes[0, 1].set_xlabel("Rating (stars)")

    # 3. Top categories
    top_cats = df["category"].value_counts().head(8)
    sns.barplot(
        x=top_cats.values,
        y=top_cats.index,
        hue=top_cats.index,
        palette="mako",
        legend=False,
        ax=axes[0, 2],
    )
    axes[0, 2].set_title("Top Categories")
    axes[0, 2].set_xlabel("Number of books")

    # 4. Price vs rating (box)
    sns.boxplot(
        x="rating",
        y="price_gbp",
        hue="rating",
        data=df,
        palette="crest",
        legend=False,
        ax=axes[1, 0],
    )
    axes[1, 0].set_title("Price by Rating")
    axes[1, 0].set_xlabel("Rating (stars)")
    axes[1, 0].set_ylabel("Price (£)")

    # 5. Availability pie
    avail_counts = df["availability"].value_counts()
    axes[1, 1].pie(
        avail_counts.values,
        labels=avail_counts.index,
        autopct="%1.1f%%",
        colors=["#55A868", "#C44E52"],
        startangle=90,
    )
    axes[1, 1].set_title("Stock Availability")

    # 6. Avg price per category (top 8)
    avg_price_cat = df.groupby("category")["price_gbp"].mean().sort_values(ascending=False).head(8)
    sns.barplot(
        x=avg_price_cat.values,
        y=avg_price_cat.index,
        hue=avg_price_cat.index,
        palette="flare",
        legend=False,
        ax=axes[1, 2],
    )
    axes[1, 2].set_title("Avg Price by Category (Top 8)")
    axes[1, 2].set_xlabel("Average price (£)")
    axes[1, 2].xaxis.set_major_formatter(mticker.FormatStrFormatter("£%.0f"))

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    outpath.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(outpath, dpi=150)
    plt.close()


def build_individual_charts(df: pd.DataFrame, outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)

    # Category share pie
    plt.figure(figsize=(8, 8))
    top_cats = df["category"].value_counts().head(8)
    others = df["category"].value_counts().iloc[8:].sum()
    pie_data = pd.concat([top_cats, pd.Series({"Other": others})])
    plt.pie(
        pie_data.values,
        labels=pie_data.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=sns.color_palette("Set2", len(pie_data)),
    )
    plt.title("Category Share of Catalogue")
    plt.tight_layout()
    plt.savefig(outdir / "category_share_pie.png", dpi=150)
    plt.close()

    # Price vs in-stock count scatter
    plt.figure(figsize=(8, 5))
    sns.scatterplot(
        x="price_gbp", y="in_stock_count", hue="rating", data=df, palette="viridis", alpha=0.7
    )
    plt.title("Price vs. Stock Count (colored by rating)")
    plt.xlabel("Price (£)")
    plt.ylabel("Units in stock")
    plt.tight_layout()
    plt.savefig(outdir / "price_vs_stock.png", dpi=150)
    plt.close()

    # Average rating per category
    plt.figure(figsize=(9, 6))
    avg_rating_cat = df.groupby("category")["rating"].mean().sort_values(ascending=False)
    sns.barplot(
        x=avg_rating_cat.values,
        y=avg_rating_cat.index,
        hue=avg_rating_cat.index,
        palette="rocket",
        legend=False,
    )
    plt.title("Average Rating by Category")
    plt.xlabel("Average rating (stars)")
    plt.xlim(0, 5)
    plt.tight_layout()
    plt.savefig(outdir / "avg_rating_by_category.png", dpi=150)
    plt.close()


def main():
    parser = argparse.ArgumentParser(
        description="Generate visualizations/dashboard for the books dataset."
    )
    parser.add_argument("--input", type=str, default="books.csv")
    parser.add_argument("--outdir", type=str, default="dashboard")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    df = load_data(args.input)

    build_dashboard(df, outdir / "dashboard_overview.png")
    build_individual_charts(df, outdir)

    print(f"Visualization complete. Charts saved to '{outdir}/'")


if __name__ == "__main__":
    main()
