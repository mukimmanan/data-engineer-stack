#!/usr/bin/env python3
"""
Script 5: Mock Slack Production Alert Pop-up
Simulates the critical alert that fires when the dashboard shows corrupted numbers.
"""

import sys
import time
from datetime import datetime

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# ANSI Color Codes
RED = "\033[91m"
WHITE = "\033[97m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"
BG_BLACK = "\033[40m"
BG_RED = "\033[41m"

def render_slack_popup():
    time.sleep(0.3)
    border_len = 74

    print("\n" * 2)
    print(f"{RED}{BOLD}╔{'═' * border_len}╗{RESET}")
    print(f"{RED}{BOLD}║{RESET}  {BG_RED}{WHITE}{BOLD} 🚨 SLACK PRODUCTION ALERT — #alerts-data-platform {RESET}{' ' * 23}{RED}{BOLD}║{RESET}")
    print(f"{RED}{BOLD}╠{'═' * border_len}╣{RESET}")
    print(f"{RED}{BOLD}║{RESET}  {BOLD}Timestamp:{RESET}     03:14 AM UTC                                            {RED}{BOLD}║{RESET}")
    print(f"{RED}{BOLD}║{RESET}  {BOLD}Severity:{RESET}      {RED}{BOLD}P1 CRITICAL / EXECUTIVE ESCALATION{RESET}                      {RED}{BOLD}║{RESET}")
    print(f"{RED}{BOLD}║{RESET}  {BOLD}Incident:{RESET}      {YELLOW}Partial Data Ingestion / Dashboard Corrupted{RESET}            {RED}{BOLD}║{RESET}")
    print(f"{RED}{BOLD}║{RESET}                                                                          {RED}{BOLD}║{RESET}")
    print(f"{RED}{BOLD}║{RESET}  {BOLD}Root Cause Analysis:{RESET}                                                   {RED}{BOLD}║{RESET}")
    print(f"{RED}{BOLD}║{RESET}  • Pipeline was triggered by {RED}uncoordinated Linux cron jobs{RESET}.              {RED}{BOLD}║{RESET}")
    print(f"{RED}{BOLD}║{RESET}  • Script #2 (Snowflake) took {YELLOW}20 mins{RESET} instead of estimated 5 mins.     {RED}{BOLD}║{RESET}")
    print(f"{RED}{BOLD}║{RESET}  • Script #3 fired on clock {RED}BEFORE Script #2 completed{RESET}!                  {RED}{BOLD}║{RESET}")
    print(f"{RED}{BOLD}║{RESET}  • Partial partition fed into executive KPI cache:                       {RED}{BOLD}║{RESET}")
    print(f"{RED}{BOLD}║{RESET}    {RED}↳ Daily Revenue: -$1,492,021.00 (CORRUPTED){RESET}                          {RED}{BOLD}║{RESET}")
    print(f"{RED}{BOLD}║{RESET}                                                                          {RED}{BOLD}║{RESET}")
    print(f"{RED}{BOLD}║{RESET}  {BOLD}Cron Diagnosis:{RESET}                                                          {RED}{BOLD}║{RESET}")
    print(f"{RED}{BOLD}║{RESET}  ❌ {YELLOW}No task dependency awareness{RESET}                                         {RED}{BOLD}║{RESET}")
    print(f"{RED}{BOLD}║{RESET}  ❌ {YELLOW}No retry logic upon lock timeout{RESET}                                     {RED}{BOLD}║{RESET}")
    print(f"{RED}{BOLD}║{RESET}  ❌ {YELLOW}No upstream state management (Scheduler != Orchestrator){RESET}             {RED}{BOLD}║{RESET}")
    print(f"{RED}{BOLD}║{RESET}                                                                          {RED}{BOLD}║{RESET}")
    print(f"{RED}{BOLD}║{RESET}  {CYAN}👉 Solution: Apache Airflow DAG with explicit dependency graph (A >> B >> C){RESET} {RED}{BOLD}║{RESET}")
    print(f"{RED}{BOLD}╚{'═' * border_len}╝{RESET}\n")

if __name__ == "__main__":
    render_slack_popup()

