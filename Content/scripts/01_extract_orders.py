#!/usr/bin/env python3
"""
Script 1: Extract Orders from Production Database
Simulates initial data ingestion step in a nightly cron pipeline.
"""

import sys
import time
from datetime import datetime

# ANSI Color Codes
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"

def log(msg, color=RESET):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{CYAN}[{ts}]{RESET} {color}{msg}{RESET}")

def main():
    print(f"\n{BOLD}{'='*65}")
    print(" [CRON 02:00 AM] SCRIPT #1: EXTRACT ORDERS (SOURCE -> STAGING)")
    print(f"{'='*65}{RESET}\n")

    log("Initiating connection to PostgreSQL Production DB: `db.prod.internal:5432`...")
    time.sleep(0.5)
    log("Connection established (pool_size=10, timeout=30s).", GREEN)

    log("Querying orders table: `SELECT * FROM orders WHERE created_at >= NOW() - INTERVAL '24 HOURS'`")
    for i in range(1, 6):
        time.sleep(0.3)
        pct = i * 20
        count = i * 100_000
        print(f"  {YELLOW}--> Progress: {pct}% | Fetched {count:,} records...{RESET}")

    time.sleep(0.4)
    log("Serializing batch to staging path: `s3://data-lake-staging/raw_orders/2026/10/11/`", CYAN)
    time.sleep(0.5)
    log("SUCCESS: Extracted 500,000 orders into staging bucket (Size: 84.2 MB).", GREEN)
    log("Script #1 execution finished cleanly with Exit Code 0.\n", GREEN)

if __name__ == "__main__":
    main()

