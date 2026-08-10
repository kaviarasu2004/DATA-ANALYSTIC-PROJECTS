"""
CodeAlpha Data Analytics Internship - Task 1: Web Scraping
============================================================
Scrapes book catalogue data asynchronously from https://books.toscrape.com
and saves the results to a clean CSV file.

Author: CodeAlpha Intern
"""

import csv
import logging
import argparse
import asyncio
from dataclasses import dataclass, asdict
from typing import List, Optional
import aiohttp
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
CATALOGUE_URL = BASE_URL + "catalogue/"

RATING_WORD_TO_NUM = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

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


async def get_soup(session: aiohttp.ClientSession, url: str) -> BeautifulSoup:
    for attempt in range(3):
        try:
            async with session.get(url, timeout=15) as resp:
                resp.raise_for_status()
                text = await resp.text()
                return BeautifulSoup(text, "lxml")
        except Exception as exc:
            log.warning("Request failed (attempt %d/3) for %s: %s", attempt + 1, url, exc)
            await asyncio.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"Failed to fetch {url} after 3 attempts")


async def parse_category(session: aiohttp.ClientSession, product_url: str) -> str:
    try:
        soup = await get_soup(session, product_url)
        crumbs = soup.select("ul.breadcrumb li a")
        return crumbs[-1].text.strip() if crumbs else "Unknown"
    except Exception as exc:
        log.warning("Failed to parse category for %s: %s", product_url, exc)
        return "Unknown"


async def parse_book_card(
    session: aiohttp.ClientSession, card, fetch_category: bool = True
) -> Book:
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
            in_stock_count = int(availability_text.split("(")[1].split()[0])
        except (IndexError, ValueError):
            in_stock_count = None

    relative_url = card.h3.a["href"]
    product_url = CATALOGUE_URL + relative_url.replace("../../../", "")

    category = await parse_category(session, product_url) if fetch_category else ""

    return Book(
        title=title,
        price_gbp=price,
        rating=rating,
        availability="In stock" if "In stock" in availability_text else "Out of stock",
        in_stock_count=in_stock_count,
        category=category,
        product_page_url=product_url,
    )


async def scrape_page(
    session: aiohttp.ClientSession, page_num: int, fetch_category: bool
) -> List[Book]:
    url = f"{CATALOGUE_URL}page-{page_num}.html"
    log.info("Scraping page %d: %s", page_num, url)
    try:
        soup = await get_soup(session, url)
    except Exception as e:
        log.error("Failed to scrape page %d: %s", page_num, e)
        return []

    cards = soup.select("article.product_pod")
    tasks = [parse_book_card(session, card, fetch_category) for card in cards]
    return await asyncio.gather(*tasks, return_exceptions=True)


async def scrape_all_books(
    max_pages: Optional[int] = None, fetch_category: bool = True
) -> List[Book]:
    books = []
    headers = {"User-Agent": "CodeAlpha-Internship-Scraper/1.0"}
    async with aiohttp.ClientSession(headers=headers) as session:
        # First, let's find the total number of pages
        try:
            first_page_soup = await get_soup(session, f"{CATALOGUE_URL}page-1.html")
            pager = first_page_soup.select_one("li.current")
            if pager:
                total_pages = int(pager.text.strip().split()[-1])
            else:
                total_pages = 1
        except Exception as e:
            log.error("Failed to determine total pages: %s", e)
            total_pages = 50  # Fallback

        if max_pages is not None:
            total_pages = min(total_pages, max_pages)

        log.info("Scraping %d pages...", total_pages)
        tasks = [scrape_page(session, p, fetch_category) for p in range(1, total_pages + 1)]
        results = await asyncio.gather(*tasks)

        for page_results in results:
            for book in page_results:
                if isinstance(book, Book):
                    books.append(book)
                else:
                    log.error("Failed to parse a book: %s", book)

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
    parser = argparse.ArgumentParser(
        description="Scrape books.toscrape.com into a CSV file asynchronously."
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=None,
        help="Limit number of catalogue pages to scrape (default: all ~50 pages).",
    )
    parser.add_argument(
        "--skip-category",
        action="store_true",
        help="Skip visiting each product page for category (much faster, less complete).",
    )
    parser.add_argument("--out", type=str, default="books.csv", help="Output CSV file path.")
    args = parser.parse_args()

    # Create event loop and run
    if hasattr(asyncio, "WindowsSelectorEventLoopPolicy"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    books = asyncio.run(
        scrape_all_books(max_pages=args.max_pages, fetch_category=not args.skip_category)
    )
    save_to_csv(books, args.out)


if __name__ == "__main__":
    main()
