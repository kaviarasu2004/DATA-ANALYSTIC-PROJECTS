# Exploratory Data Analysis Report

**Dataset size (after cleaning):** 1000 books  
**Duplicate rows removed:** 0

## 1. Data Structure

| Column | Dtype |
|---|---|
| title | str |
| price_gbp | float64 |
| rating | int64 |
| availability | str |
| in_stock_count | float64 |
| category | str |
| product_page_url | str |

## 2. Missing Values

|                  |   missing_count |   missing_pct |
|:-----------------|----------------:|--------------:|
| title            |               0 |             0 |
| price_gbp        |               0 |             0 |
| rating           |               0 |             0 |
| availability     |               0 |             0 |
| in_stock_count   |            1000 |           100 |
| category         |               0 |             0 |
| product_page_url |               0 |             0 |

## 3. Descriptive Statistics

|       |   price_gbp |   rating |   in_stock_count |
|:------|------------:|---------:|-----------------:|
| count |     1000    |  1000    |                0 |
| mean  |       35.07 |     2.92 |              nan |
| std   |       14.45 |     1.43 |              nan |
| min   |       10    |     1    |              nan |
| 25%   |       22.11 |     2    |              nan |
| 50%   |       35.98 |     3    |              nan |
| 75%   |       47.46 |     4    |              nan |
| max   |       59.99 |     5    |              nan |

## 4. Outlier Detection (Price, IQR method)

Detected **0** price outliers out of 1000 records (0.0%).

## 5. Key Findings

- The most common category is **Default**, with 152 titles.
- Average book price is **£35.07** (median £35.98).
- Average star rating across the catalogue is **2.92 / 5**.
- **0.0%** of books are currently out of stock.
- Correlation between price and rating: **0.028** (weak/negligible).

## 6. Hypothesis Validation

**H0: Higher-rated books are not priced differently from lower-rated books.**

|   rating |   avg_price_gbp |
|---------:|----------------:|
|        1 |           34.56 |
|        2 |           34.81 |
|        3 |           34.69 |
|        4 |           36.09 |
|        5 |           35.37 |

**Verdict:** not rejected — price does not meaningfully depend on rating in this dataset.

## 7. Charts

See the `charts/` folder for: `price_distribution.png`, `rating_distribution.png`, `price_by_rating.png`, `correlation_heatmap.png`, `top_categories.png`.
