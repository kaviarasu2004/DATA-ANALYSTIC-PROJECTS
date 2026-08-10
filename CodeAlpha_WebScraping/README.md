# CodeAlpha_WebScraping

**Data Analytics Internship @ CodeAlpha — Task 1: Web Scraping**

A Python web scraper that crawls the full book catalogue of [books.toscrape.com](https://books.toscrape.com) (a site purpose-built for scraping practice) and extracts structured product data into a clean CSV file, ready for downstream analysis.

---

## 📋 Overview

This project demonstrates end-to-end web scraping skills:

- Crawling paginated listing pages
- Parsing HTML with `BeautifulSoup`
- Following links to detail pages to enrich records
- Handling missing/inconsistent data gracefully
- Exporting a tidy, analysis-ready CSV

The resulting dataset feeds directly into **[CodeAlpha_EDA](../CodeAlpha_EDA)** and **[CodeAlpha_DataVisualization](../CodeAlpha_DataVisualization)**.

## ✨ Features

- Scrapes **all ~1,000 books** across ~50 paginated catalogue pages
- Extracts: `title`, `price_gbp`, `rating` (1–5 stars), `availability`, `in_stock_count`, `category`, `product_page_url`
- Polite crawling with request delays and automatic retries on failure
- Command-line flags to limit pages or skip the (slower) per-product category lookup
- Clean logging of progress and errors
- Fully typed with `dataclasses` for record structure

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.9+ | Core language |
| `requests` | HTTP requests |
| `BeautifulSoup4` + `lxml` | HTML parsing |
| `csv` / `dataclasses` | Structured export |

## 📁 Project Structure

```
CodeAlpha_WebScraping/
├── scrape_books.py       # Main scraper script
├── requirements.txt      # Python dependencies
├── books.csv             # Sample output (generated data — see Note below)
└── README.md
```

## 🚀 Installation

```bash
git clone https://github.com/<your-username>/CodeAlpha_WebScraping.git
cd CodeAlpha_WebScraping
pip install -r requirements.txt
```

## ▶️ Usage

Scrape the entire catalogue (all pages, with category lookup — slower but complete):

```bash
python scrape_books.py --out books.csv
```

Quick run — first 5 pages only, skip category lookup (fast test):

```bash
python scrape_books.py --max-pages 5 --skip-category --out books_quick.csv
```

### CLI Options

| Flag | Description | Default |
|---|---|---|
| `--max-pages N` | Limit number of catalogue pages crawled | all pages |
| `--skip-category` | Skip visiting each product page for category (faster) | off |
| `--out PATH` | Output CSV file path | `books.csv` |

## 📊 Output Schema

| Column | Type | Description |
|---|---|---|
| `title` | string | Book title |
| `price_gbp` | float | Price in GBP |
| `rating` | int (1–5) | Star rating |
| `availability` | string | `"In stock"` / `"Out of stock"` |
| `in_stock_count` | int | Units currently in stock |
| `category` | string | Book category (e.g. Fiction, Travel) |
| `product_page_url` | string | Link to the product detail page |

## ⚠️ Note on the included `books.csv`

This environment does not have outbound internet access to `books.toscrape.com`, so the `books.csv` included here is a **realistic sample dataset** generated to match the scraper's exact output schema (1,000 rows) — used purely to demonstrate and test the downstream EDA and visualization pipeline. Run `scrape_books.py` yourself with internet access to produce the real, live-scraped dataset — the column structure will be identical, so no downstream code needs to change.

## 📌 Ethical Scraping Notes

- `books.toscrape.com` is explicitly designed as a scraping sandbox — no `robots.txt` restrictions apply.
- The script adds a short delay between requests to avoid hammering the server.
- Always check a site's `robots.txt` and Terms of Service before scraping real-world sites.

## 👤 Author

CodeAlpha Data Analytics Intern

## 📄 License

This project is submitted as part of the CodeAlpha internship program and is provided for educational purposes.
