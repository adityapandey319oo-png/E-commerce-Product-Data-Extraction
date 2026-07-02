import argparse
import logging
import os
import time
from urllib.parse import urljoin
import bs4
import pandas as pd
import requests
BASE_URL = "https://books.toscrape.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
def fetch_page_with_retry(url: str, retries: int = 3, delay: int = 2) -> str:
    """Downloads webpage HTML content with up to 3 automated retry attempts."""
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, headers=HEADERS, timeout=15)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            msg = f"Attempt {attempt}/{retries} failed for URL: {url}. Error: {e}"
            print(f"  ⚠️ {msg}")
            logging.warning(msg)
            if attempt < retries:
                time.sleep(delay)
            else:
                logging.error(f"Max retries reached. Skipping extraction for: {url}")
    return ""
def parse_inner_details(product_url: str) -> tuple:
    """Visits the deeper single product page to pull description and category fields."""
    html = fetch_page_with_retry(product_url)
    if not html:
        return "N/A", "N/A"

    soup = bs4.BeautifulSoup(html, "html.parser")    
    category = "N/A"
    breadcrumb = soup.find("ul", class_="breadcrumb")
    if breadcrumb:
        crumbs = breadcrumb.find_all("li")
        if len(crumbs) >= 3:
            category = crumbs[2].text.strip()
    description = "N/A"
    desc_header = soup.find("div", id="product_description")
    if desc_header:
        desc_p = desc_header.find_next_sibling("p")
        if desc_p:
            description = desc_p.text.strip()
    return category, description
def scrape_catalog() -> list:
    """Iterates through all 50 pagination tracks to fetch all available store items."""
    all_products = []
    seen_urls = set()
    current_url = BASE_URL
    print("\n🚀 Initiating global store catalog crawling pipeline...")
    logging.info("Scraper engine initialized across pagination tracks.")
    page_number = 1

    while current_url:
        print(f"\n📁 Processing Store Catalog Page: {page_number}")
        logging.info(f"Extracting catalog grid indices from page {page_number}")        
        html = fetch_page_with_retry(current_url)
        if not html:
            print("❌ Critical index link fetching error. Terminating search.")
            break
        soup = bs4.BeautifulSoup(html, "html.parser")
        product_pods = soup.find_all("article", class_="product_pod")
        if not product_pods:
            break
        for pod in product_pods:
            title_node = pod.h3.a
            title = title_node.get("title", title_node.text)
            rel_href = title_node.get("href", "")
            prod_url = urljoin(current_url, rel_href)
            if prod_url in seen_urls:
                continue
            seen_urls.add(prod_url)
            price_node = pod.find("p", class_="price_color")
            price = price_node.text.strip() if price_node else "N/A"
            rating_node = pod.find("p", class_="star-rating")
            rating = "N/A"
            if rating_node:
                for cls in rating_node.get("class", []):
                    if cls in RATING_MAP:
                        rating = RATING_MAP[cls]
                        break
            avail_node = pod.find("p", class_="instock availability")
            availability = avail_node.text.strip() if avail_node else "N/A"
            img_node = pod.find("img")
            rel_img = img_node.get("src", "") if img_node else ""
            img_url = urljoin(current_url, rel_img)
            print(f"   🔎 Crawling details for: {title[:35]}...")
            category, description = parse_inner_details(prod_url)
            all_products.append({
                "Product Title": title,
                "Price": price,
                "Stock Availability": availability,
                "Star Rating": rating,
                "Product Category": category,
                "Product Description": description,
                "Product Page URL": prod_url,
                "Product Image URL": img_url
            })
        next_button = soup.find("li", class_="next")
        if next_button and next_button.a:
            next_href = next_button.a.get("href", "")
            current_url = urljoin(current_url, next_href)
            page_number += 1
        else:
            current_url = None  
    return all_products
def export_data(data: list, mode: str) -> None:
    """Exports data locally to CSV, JSON, or both based on user choice."""
    if not data:
        print("⚠ Empty data arrays encountered. Stopping export routines.")
        return
    df = pd.DataFrame(data)
    if mode in ["csv", "both"]:
        df.to_csv("products.csv", index=False, encoding="utf-8")
        print("💾 File generation successful: 'products.csv'")
        logging.info("Saved final export batch to products.csv format successfully.")
    if mode in ["json", "both"]:
        df.to_json("products.json", orient="records", indent=4, force_ascii=False)
        print("💾 File generation successful: 'products.json'")
        logging.info("Saved final export batch to products.json format successfully.")
def main():
    parser = argparse.ArgumentParser(
        description="E-commerce Product Data Extraction Tool (Portfolio Edition)"
    )
    parser.add_argument(
        "--format",
        choices=["csv", "json", "both"],
        default="both",
        help="Select output file type (default: both)"
    )
    args = parser.parse_args()
    start_time = time.time()
    extracted_records = scrape_catalog()
    export_data(extracted_records, args.format)
    end_time = time.time()
    elapsed_duration = round(end_time - start_time, 2)
    print("\n🏆 Execution Summary Complete")
    print(f"🔹 Total Products Scraped: {len(extracted_records)}")
    print(f"🔹 Total Execution Time: {elapsed_duration} seconds")
    print("📝 Operational history saved inside 'scraper.log'")
    logging.info(f"Process closed cleanly. Records grabbed: {len(extracted_records)} over {elapsed_duration}s.")

if __name__ == "__main__":
    main()
