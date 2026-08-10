"""
CodeAlpha Data Analytics Internship - Task 1: Web Scraping
============================================================
Scrapes book catalogue data (title, price, star rating, availability,
and category) from https://books.toscrape.com — a website built
specifically for practicing web scraping — and saves the results
to a clean CSV file for downstream analysis (see CodeAlpha_EDA and
CodeAlpha_DataVisualization).

Author: CodeAlpha Intern
"""

import csv
import time
import logging
import argparse
from dataclasses import dataclass, asdict
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
CATALOGUE_URL = BASE_URL + "catalogue/"

RATING_WORD_TO_NUM = {
    "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
log = logging.getLogger(__name__)


@dataclass
class Book:
    title: str
    price_gbp: float
    rating: int
    availability: str
    in_stock_count: Optional[int]
    category: str
    product_page_url: str


def get_soup(session: requests.Session, url: str) -> BeautifulSoup:
    """Fetch a URL and return a parsed BeautifulSoup object, with basic retry logic."""
    for attempt in range(3):
        try:
            resp = session.get(url, timeout=15)
            resp.raise_for_status()
            return BeautifulSoup(resp.text, "lxml")
        except requests.RequestException as exc:
            log.warning("Request failed (attempt %d/3) for %s: %s", attempt + 1, url, exc)
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"Failed to fetch {url} after 3 attempts")


def parse_category(session: requests.Session, product_url: str) -> str:
    """Visit a product page to pull its category from the breadcrumb trail."""
    soup = get_soup(session, product_url)
    crumbs = soup.select("ul.breadcrumb li a")
    return crumbs[-1].text.strip() if crumbs else "Unknown"


def parse_book_card(session: requests.Session, card, fetch_category: bool = True) -> Book:
    title = card.h3.a["title"].strip()
    price_text = card.select_one("p.price_color").text.strip()
    price = float(price_text.replace("£", "").replace("Â", ""))

    rating_class = card.select_one("p.star-rating")["class"]
    rating_word = [c for c in rating_class if c != "star-rating"][0]
    rating = RATING_WORD_TO_NUM.get(rating_word, 0)

    availability_text = card.select_one("p.instock.availability").text.strip()
    in_stock_count = None
    if "(" in availability_text:
        try:
            in_stock_count = int(
                availability_text.split("(")[1].split()[0]
            )
        except (IndexError, ValueError):
            in_stock_count = None

    relative_url = card.h3.a["href"]
    product_url = CATALOGUE_URL + relative_url.replace("../../../", "")

    category = parse_category(session, product_url) if fetch_category else ""

    return Book(
        title=title,
        price_gbp=price,
        rating=rating,
        availability="In stock" if "In stock" in availability_text else "Out of stock",
        in_stock_count=in_stock_count,
        category=category,
        product_page_url=product_url,
    )


def scrape_all_books(max_pages: Optional[int] = None, fetch_category: bool = True) -> List[Book]:
    """Crawl every paginated catalogue page and return a list of Book records."""
    books: List[Book] = []
    session = requests.Session()
    session.headers.update({"User-Agent": "CodeAlpha-Internship-Scraper/1.0"})

    page_num = 1
    url = CATALOGUE_URL + "page-1.html"

    while url:
        log.info("Scraping page %d: %s", page_num, url)
        soup = get_soup(session, url)
        cards = soup.select("article.product_pod")

        for card in cards:
            try:
                books.append(parse_book_card(session, card, fetch_category=fetch_category))
            except Exception as exc:
                log.error("Failed to parse a book card on page %d: %s", page_num, exc)

        next_link = soup.select_one("li.next a")
        if next_link and (max_pages is None or page_num < max_pages):
            url = CATALOGUE_URL + next_link["href"]
            page_num += 1
            time.sleep(0.5)  # be polite to the server
        else:
            url = None

    log.info("Finished scraping. Total books collected: %d", len(books))
    return books


def save_to_csv(books: List[Book], out_path: str) -> None:
    if not books:
        log.warning("No books to save.")
        return
    fieldnames = list(asdict(books[0]).keys())
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for book in books:
            writer.writerow(asdict(book))
    log.info("Saved %d records to %s", len(books), out_path)


def main():
    parser = argparse.ArgumentParser(description="Scrape books.toscrape.com into a CSV file.")
    parser.add_argument("--max-pages", type=int, default=None,
                         help="Limit number of catalogue pages to scrape (default: all ~50 pages).")
    parser.add_argument("--skip-category", action="store_true",
                         help="Skip visiting each product page for category (much faster, less complete).")
    parser.add_argument("--out", type=str, default="books.csv",
                         help="Output CSV file path.")
    args = parser.parse_args()

    books = scrape_all_books(max_pages=args.max_pages, fetch_category=not args.skip_category)
    save_to_csv(books, args.out)


if __name__ == "__main__":
    main()
