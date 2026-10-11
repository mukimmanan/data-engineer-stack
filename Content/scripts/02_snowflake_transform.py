#!/usr/bin/env python3
"""
Script 2: Snowflake Warehouse Data Transformation
Simulates the slow intermediate pipeline step that causes the cron disaster.
Takes 20 minutes instead of 5, locking tables and delaying completion.
"""

import sys
import time
from datetime import datetime

# ANSI Color Codes
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"
MAGENTA = "\033[95m"

def log(msg, color=RESET):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{CYAN}[{ts}]{RESET} {color}{msg}{RESET}")

def main():
    print(f"\n{BOLD}{'='*65}")
    print(" [CRON 02:05 AM] SCRIPT #2: SNOWFLAKE WAREHOUSE TRANSFORM")
    print(f"{'='*65}{RESET}\n")

    log("Connecting to Snowflake Account: `xy12345.us-east-1` (Warehouse: `TRANSFORM_WH_XL`)...")
    time.sleep(0.6)
    log("Session established. Role: `TRANSFORM_ROLE`, Database: `ANALYTICS_PROD`.", CYAN)

    log("Executing DDL: `CREATE OR REPLACE TRANSIENT TABLE staging_orders_tmp AS COPY INTO...`")
    time.sleep(0.8)
    log("Staging table populated. Rows loaded: 500,000.", CYAN)

    log(f"{YELLOW}Executing Heavy MERGE into `ANALYTICS_PROD.CORE.FACT_ORDERS`...{RESET}")
    log(f"{MAGENTA}[WARNING] Warehouse queue overload detected. Query ID: 01b4c92a-0002-3f19-0000-00025983e{RESET}")
    log(f"{YELLOW}[LATENCY ALERT] Expected execution: 5m 00s. Query currently queued behind ad-hoc workload...{RESET}")

    # Simulated slow execution
    simulated_minutes = [5, 10, 15, 18, 20]
    for m in simulated_minutes:
        time.sleep(1.2)
        print(f"  {YELLOW}⌛ [Elapsed: {m:02d}m 00s] Snowflake query still running... Waiting for resource lock release...{RESET}")

    log(f"{RED}[CRON DESYNC] Script #2 is STILL executing! Target table `FACT_ORDERS` is write-locked!{RESET}", RED)
    log(f"{RED}[RACE CONDITION] Cron schedule triggered Script #3 while Script #2 is unfinished!{RESET}", RED)

    # Allow simulation to keep running or finish
    time.sleep(2)
    log("[FINALLY FINISHED at 02:25 AM] MERGE finished after 20m 14s. But downstream scripts already failed!", YELLOW)

if __name__ == "__main__":
    main()

