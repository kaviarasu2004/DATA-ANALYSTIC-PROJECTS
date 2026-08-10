# CodeAlpha_DataVisualization

**Data Analytics Internship @ CodeAlpha — Task 3: Data Visualization**

A visualization suite that turns the book catalogue dataset (from **[CodeAlpha_WebScraping](../CodeAlpha_WebScraping)**) into a polished, presentation-ready analytics dashboard plus a set of standalone insight charts, built with Matplotlib and Seaborn.

---

## 📋 Overview

This project focuses purely on turning cleaned data into clear, decision-ready visuals:

- A single **6-panel dashboard image** giving an at-a-glance overview of the catalogue
- Additional **standalone charts** for deeper dives (category share, price vs. stock, rating by category)

## ✨ Features

**Dashboard (`dashboard_overview.png`)** — 6 panels in one image:
1. Price distribution (histogram + KDE)
2. Rating distribution (bar chart)
3. Top categories by book count
4. Price by rating (boxplot)
5. Stock availability (pie chart)
6. Average price by category (top 8)

**Standalone charts:**
- `category_share_pie.png` — category share of the full catalogue (top 8 + "Other")
- `price_vs_stock.png` — scatter plot of price vs. stock count, colored by rating
- `avg_rating_by_category.png` — average rating per category, ranked

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.9+ | Core language |
| `pandas` | Data loading & aggregation |
| `matplotlib` | Chart rendering & dashboard layout |
| `seaborn` | Statistical chart styling |

## 📁 Project Structure

```
CodeAlpha_DataVisualization/
├── visualize.py                       # Main visualization script
├── requirements.txt                   # Python dependencies
├── books.csv                          # Input dataset (from Task 1)
├── dashboard/
│   ├── dashboard_overview.png          # 6-panel combined dashboard
│   ├── category_share_pie.png
│   ├── price_vs_stock.png
│   └── avg_rating_by_category.png
└── README.md
```

## 🚀 Installation

```bash
git clone https://github.com/<your-username>/CodeAlpha_DataVisualization.git
cd CodeAlpha_DataVisualization
pip install -r requirements.txt
```

## ▶️ Usage

```bash
python visualize.py --input books.csv --outdir dashboard
```

### CLI Options

| Flag | Description | Default |
|---|---|---|
| `--input PATH` | Path to input CSV (from Task 1 scraper) | `books.csv` |
| `--outdir PATH` | Output directory for all chart images | `dashboard` |

## 🖼️ Preview

The main deliverable is `dashboard/dashboard_overview.png` — a single image summarizing price, rating, category, and stock patterns across the entire catalogue at a glance, suitable for dropping straight into a LinkedIn post or presentation slide.

## 👤 Author

CodeAlpha Data Analytics Intern

## 📄 License

This project is submitted as part of the CodeAlpha internship program and is provided for educational purposes.
