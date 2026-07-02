# E-commerce Product Data Extraction Tool

An enterprise-grade, high-performance Python data harvesting pipeline built to crawl, clean, parse, and structure product information from target online stores. Designed as a scalable initial prototype for a live price comparison platform, this engine comprehensively traverses multi-level catalog paths, extracts individual listing details from deep web nodes, handles structural network exceptions natively, and exports clean datasets.

---

## 🏗️ Folder Structure

```text
Product-Scraper-Pro/
│
├── main.py
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
├── products.csv
└── products.json
```

---

## ⚡ Key Architectural Features

- **Multi-Level Page Deep Crawling**: Iteratively traverses through all 50 catalog index pagination tracks and deep-dives straight into every standalone product sub-page to extract granular properties.
- **Dynamic Path Optimization**: Leverages standard `urllib.parse.urljoin` engines bound to shifting pagination contexts to resolve complex relative directory changes natively without string hacking.
- **Robust Failure Resilience**: Integrates an automated linear backoff retry system that safely handles dropped requests up to 3 times before recording warnings and gracefully continuing execution.
- **Strict Deduplication Verification**: Utilizes explicit hash table lookups to ensure that duplicate product endpoint targets are omitted from final files.
- **Granular Progress Dashboard**: Feeds instantaneous live operational tracking logs directly into the system terminal and structural data tables, mapping processed quantities and net runtime durations.

---

## 🛠️ Extraction Specifications

The engine programmatically targets, sanitizes, and registers the following items for every inventory item:
*   **Product Title**: Full item title text string.
*   **Price**: Flat product value including currency layout.
*   **Stock Availability**: Real-time product inventory status.
*   **Star Rating**: Normalized numeric integer scale (1–5) parsed from explicit tag text classes.
*   **Product Category**: Clean structural classification captured directly from deeper nested breadcrumb parent items.
*   **Product Description**: Sanitized, complete text summary extracted from individual item layouts.
*   **Product Page URL**: Direct, absolute, verified hyperlink to the target item page.
*   **Product Image URL**: Direct, absolute, verified hyperlink to the source catalog image file.

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have **Python 3.8 or newer** installed on your workstation.

### 2. Installation
Open your project terminal panel inside your file workspace directory and pull all necessary production components using the python package installer tool:

```bash
pip install -r requirements.txt
```

### 3. Usage & Execution
Execute the pipeline entrypoint file manually. By default, the program will process all catalog zones and export both target formats concurrently:

```bash
python main.py
```

#### Tailored Output Formats
Control your final file outputs on demand using the terminal application parameter:

```bash
# Export strictly into a Comma-Separated Values (CSV) file format
python main.py --format csv

# Export strictly into a structured JavaScript Object Notation (JSON) array
python main.py --format json

# Export to both CSV and JSON variants simultaneously (Default Behaviour)
python main.py --format both
```

---

## 📊 Deliverables & Diagnostic Records

Upon successful runtime conclusions, the pipeline deploys structured file matrices into the project core directory:
- `products.csv`: Tabular array optimized for flat database ingestion, Excel operations, or Pandas processing.
- `products.json`: Clean, pretty-printed data format mapping UTF-8 characters natively.
- `scraper.log`: Operational execution ledger collecting time indicators, connection retry loops, page tracks, and execution volume footprints.
