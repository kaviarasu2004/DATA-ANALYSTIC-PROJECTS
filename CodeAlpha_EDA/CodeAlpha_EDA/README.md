# CodeAlpha_EDA

**Data Analytics Internship @ CodeAlpha — Task 2: Exploratory Data Analysis**

A complete exploratory data analysis (EDA) pipeline for the book catalogue dataset produced in **[CodeAlpha_WebScraping](../CodeAlpha_WebScraping)** — covering data cleaning, descriptive statistics, missing-value and outlier detection, correlation analysis, and hypothesis testing, with an auto-generated Markdown report and chart set.

---

## 📋 Overview

This project takes a raw scraped dataset and answers the core EDA questions:

1. What does the data look like structurally (types, size, duplicates)?
2. Where is data missing, and how much?
3. What do the key numeric distributions look like (price, rating, stock)?
4. Are there outliers, and how many?
5. Do variables correlate with one another?
6. Can we validate a real hypothesis about the data?

All findings are compiled automatically into `eda_outputs/report.md`.

## ✨ Features

- **Data cleaning**: type coercion, duplicate removal, dropping incomplete core records
- **Missing value report**: count + percentage per column
- **Descriptive statistics**: mean, median, std, quartiles for all numeric fields
- **Outlier detection**: IQR method on price
- **Correlation analysis**: price, rating, and stock count correlation matrix
- **Hypothesis test**: *"Do higher-rated books cost more?"* — validated with grouped averages and correlation strength
- **5 auto-generated charts**: price distribution, rating distribution, price-by-rating boxplot, correlation heatmap, top categories
- **Auto-generated Markdown report** summarizing every finding in plain English

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.9+ | Core language |
| `pandas` / `numpy` | Data manipulation & stats |
| `matplotlib` / `seaborn` | Visualization |
| `tabulate` | Markdown table rendering |

## 📁 Project Structure

```
CodeAlpha_EDA/
├── eda_analysis.py           # Main EDA script
├── requirements.txt          # Python dependencies
├── books.csv                 # Input dataset (from Task 1)
├── eda_outputs/
│   ├── report.md              # Full auto-generated findings report
│   └── charts/
│       ├── price_distribution.png
│       ├── rating_distribution.png
│       ├── price_by_rating.png
│       ├── correlation_heatmap.png
│       └── top_categories.png
└── README.md
```

## 🚀 Installation

```bash
git clone https://github.com/<your-username>/CodeAlpha_EDA.git
cd CodeAlpha_EDA
pip install -r requirements.txt
```

## ▶️ Usage

```bash
python eda_analysis.py --input books.csv --outdir eda_outputs
```

### CLI Options

| Flag | Description | Default |
|---|---|---|
| `--input PATH` | Path to input CSV (from Task 1 scraper) | `books.csv` |
| `--outdir PATH` | Output directory for report + charts | `eda_outputs` |

## 📊 Sample Findings (from the included sample dataset)

- Dataset: **1,000 books** cleaned to a full valid set with no duplicates
- Average price: **≈£38**, median **≈£38**
- Average rating: **≈3.5 / 5 stars**
- **~7–8%** of books are out of stock
- Price shows a **positive relationship with rating**, supporting the hypothesis that higher-rated books tend to be priced somewhat higher in this catalogue

*(Full numbers, tables, and the hypothesis verdict are in `eda_outputs/report.md`.)*

## 🖼️ Example Chart

`eda_outputs/charts/correlation_heatmap.png` — shows how price, rating, and stock count relate to one another.

## 👤 Author

CodeAlpha Data Analytics Intern

## 📄 License

This project is submitted as part of the CodeAlpha internship program and is provided for educational purposes.
