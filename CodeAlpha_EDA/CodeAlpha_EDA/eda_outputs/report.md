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
| title            |               0 |           0   |
| price_gbp        |               0 |           0   |
| rating           |               0 |           0   |
| availability     |               0 |           0   |
| in_stock_count   |              75 |           7.5 |
| category         |               0 |           0   |
| product_page_url |               0 |           0   |

## 3. Descriptive Statistics

|       |   price_gbp |   rating |   in_stock_count |
|:------|------------:|---------:|-----------------:|
| count |     1000    |  1000    |           925    |
| mean  |       39.85 |     3.5  |            15.43 |
| std   |       14.73 |     1.24 |             8.64 |
| min   |       12.24 |     1    |             1    |
| 25%   |       27.74 |     3    |             8    |
| 50%   |       39.4  |     4    |            15    |
| 75%   |       52.45 |     5    |            23    |
| max   |       70.15 |     5    |            30    |

## 4. Outlier Detection (Price, IQR method)

Detected **0** price outliers out of 1000 records (0.0%).

## 5. Key Findings

- The most common category is **Nonfiction**, with 81 titles.
- Average book price is **£39.85** (median £39.40).
- Average star rating across the catalogue is **3.50 / 5**.
- **7.5%** of books are currently out of stock.
- Correlation between price and rating: **0.131** (weak/negligible).

## 6. Hypothesis Validation

**H0: Higher-rated books are not priced differently from lower-rated books.**

|   rating |   avg_price_gbp |
|---------:|----------------:|
|        1 |           37.65 |
|        2 |           36.21 |
|        3 |           38.79 |
|        4 |           40.84 |
|        5 |           42.3  |

**Verdict:** not rejected — price does not meaningfully depend on rating in this dataset.

## 7. Charts

See the `charts/` folder for: `price_distribution.png`, `rating_distribution.png`, `price_by_rating.png`, `correlation_heatmap.png`, `top_categories.png`.
