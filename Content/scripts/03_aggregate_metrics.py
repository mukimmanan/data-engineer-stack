#!/usr/bin/env python3
"""
Script 3: Aggregate Daily Metrics
Starts on the clock (02:10 AM) before Script #2 finishes!
Queries uncommitted/partial tables and explodes with red traceback errors.
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
    print(" [CRON 02:10 AM] SCRIPT #3: AGGREGATE DAILY METRICS")
    print(f"{'='*65}{RESET}\n")

    log("Initiating Daily Aggregation Job on `ANALYTICS_PROD.METRICS`...")
    time.sleep(0.5)

    log("Attempting to read from `ANALYTICS_PROD.CORE.FACT_ORDERS`...")
    time.sleep(0.7)

    log(f"{YELLOW}[WARNING] Inconsistent state detected: Table `FACT_ORDERS` has an active EXCLUSIVE lock from Process PID: 48912 (Script #2).{RESET}")
    time.sleep(0.5)

    log(f"{RED}[DIRTY READ] Reading partial partition: Expected 500,000 rows, found only 114,209 uncommitted rows!{RESET}", RED)
    time.sleep(0.4)

    print(f"\n{BG_RED} FATAL EXCEPTION ENCOUNTERED {RESET}\n")
    time.sleep(0.2)

    # Output red traceback flooding the screen
    traceback_str = f"""{RED}Traceback (most recent call last):
  File "/pipelines/03_aggregate_metrics.py", line 78, in <module>
    run_daily_aggregations()
  File "/pipelines/03_aggregate_metrics.py", line 54, in run_daily_aggregations
    metrics_df = compute_revenue_and_margins(fact_table)
  File "/opt/venv/lib/python3.11/site-packages/snowflake/connector/cursor.py", line 821, in execute
    raise ProgrammingError(
snowflake.connector.errors.ProgrammingError: 000625 (57014): Statement '01b4c93f-0002-3f20-0000-00025983f' reached lock timeout (30000 ms) while waiting on resource lock held by query '01b4c92a-0002-3f19-0000-00025983e' (Script #2).

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/pipelines/03_aggregate_metrics.py", line 83, in <module>
    fallback_compute_partial_metrics(fact_table)
  File "/pipelines/03_aggregate_metrics.py", line 68, in fallback_compute_partial_metrics
    assert len(uncommitted_batch) == expected_row_count, "Corrupted snapshot: Row count mismatch"
AssertionError: Corrupted snapshot: Row count mismatch. Expected: 500000, Actual: 114209
ZeroDivisionError: division by zero in metric computation: total_revenue / missing_order_volume{RESET}
"""
    sys.stderr.write(traceback_str)
    sys.stderr.flush()

    time.sleep(0.5)
    print(f"\n{RED}[CRON STATUS] Process exited with code 1. No supervisor alert sent. Cron continuing blindly...{RESET}\n")
    sys.exit(1)

if __name__ == "__main__":
    main()

