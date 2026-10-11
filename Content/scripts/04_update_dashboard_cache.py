#!/usr/bin/env python3
"""
Script 4: Update Executive Dashboard Cache
Starts at 02:15 AM on the cron clock.
Pushes corrupted metrics into Redis / Tableau / Metabase cache.
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
BG_RED = "\033[41m\033[97m"

def log(msg, color=RESET):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{CYAN}[{ts}]{RESET} {color}{msg}{RESET}")

def main():
    print(f"\n{BOLD}{'='*65}")
    print(" [CRON 02:15 AM] SCRIPT #4: UPDATE DASHBOARD CACHE & METRICS")
    print(f"{'='*65}{RESET}\n")

    log("Connecting to Redis Cache Cluster: `redis-dash.prod:6379`...")
    time.sleep(0.4)
    log("Connected to Redis cluster.", CYAN)

    log("Fetching daily executive KPIs from `ANALYTICS_PROD.METRICS.DAILY_REVENUE`...")
    time.sleep(0.6)

    log(f"{RED}[DATA CORRUPTION DETECTED] Upstream table is missing 77% of transaction rows!{RESET}", RED)
    log(f"{RED}  --> Daily Revenue: -$1,492,021.00 (NEGATIVE REVENUE BUG){RESET}", RED)
    log(f"{RED}  --> Customer Conversion Rate: NaN %{RESET}", RED)
    log(f"{RED}  --> Total Active Users: -42,109{RESET}", RED)
    time.sleep(0.4)

    log(f"{YELLOW}[SILENT WRITE] Overwriting production cache key `dash:kpi:exec_summary:today` with corrupted data...{RESET}", YELLOW)
    time.sleep(0.5)

    print(f"\n{BG_RED} CORRUPTED DATA WRITTEN TO PRODUCTION {RESET}\n")

    traceback_str = f"""{RED}Traceback (most recent call last):
  File "/pipelines/04_update_dashboard_cache.py", line 62, in <module>
    validate_financial_integrity(kpi_payload)
  File "/pipelines/04_update_dashboard_cache.py", line 45, in validate_financial_integrity
    raise CorruptedDataPayloadException(
exceptions.CorruptedDataPayloadException: Invariant violation: `total_revenue` cannot be negative (-$1,492,021.00). Upstream dependencies failed to reconcile.{RESET}
"""
    sys.stderr.write(traceback_str)
    sys.stderr.flush()

    time.sleep(0.4)
    print(f"\n{RED}[CRON STATUS] Silent failure! Cron doesn't know what an Invariant Violation is. Job marked finished.{RESET}\n")
    sys.exit(1)

if __name__ == "__main__":
    main()

