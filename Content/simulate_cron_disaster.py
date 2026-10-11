#!/usr/bin/env python3
"""
Full Terminal Simulation: The Cron Disaster Hook (0:00 - 0:45)
Runs the complete sequence described in the video script with realistic timings,
concurrent terminal streams, red error floods, and the Slack notification pop-up.
"""

import os
import sys
import time
import subprocess
from datetime import datetime

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# ANSI Color Codes
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

def print_header():
    print("\033[2J\033[H")  # Clear screen and move cursor to top
    print(f"{BOLD}{CYAN}╔{'═' * 76}╗")
    print(f"║   THE CRON DISASTER SIMULATOR — WHY APACHE AIRFLOW EXISTS                 ║")
    print(f"║   Scenario: 5 Nightly Python Scripts Scheduled with Linux Cron             ║")
    print(f"╚{'═' * 76}╝{RESET}\n")

def simulate_clock(simulated_time):
    print(f"\n{BOLD}{MAGENTA}[⏰ CRON CLOCK: {simulated_time} UTC]{RESET} {DIM}Executing scheduled crontab entries...{RESET}\n")
    time.sleep(0.8)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    scripts_dir = os.path.join(script_dir, "scripts")

    print_header()
    time.sleep(0.8)

    # 1. 02:00 AM - Script 1 runs and succeeds
    simulate_clock("02:00:00 AM")
    subprocess.run([sys.executable, os.path.join(scripts_dir, "01_extract_orders.py")])
    time.sleep(1.0)

    # 2. 02:05 AM - Script 2 starts (takes 20 mins instead of 5)
    simulate_clock("02:05:00 AM")
    print(f"{CYAN}[02:05:00] Starting Script #2: 02_snowflake_transform.py...{RESET}")
    print(f"  {YELLOW}--> Query submitted to Snowflake. Expected duration: 5m.{RESET}")
    print(f"  {YELLOW}--> [02:08:00] Warehouse queue latency spike: Query queued behind batch analytics...{RESET}")
    print(f"  {YELLOW}--> [02:09:59] Script #2 still running (Elapsed: 4m 59s)...{RESET}\n")
    time.sleep(1.5)

    # 3. 02:10 AM - Script 3 starts BEFORE Script 2 finishes!
    simulate_clock("02:10:00 AM")
    print(f"{RED}{BOLD}🚨 CRON TRIGGER: Script #3 fired on clock while Script #2 is STILL executing!{RESET}\n")
    time.sleep(0.8)
    subprocess.run([sys.executable, os.path.join(scripts_dir, "03_aggregate_metrics.py")])
    time.sleep(1.5)

    # 4. 02:15 AM - Script 4 runs blindly and corrupts cache
    simulate_clock("02:15:00 AM")
    print(f"{RED}{BOLD}🚨 CRON TRIGGER: Script #4 fired blindly into broken downstream state!{RESET}\n")
    time.sleep(0.8)
    subprocess.run([sys.executable, os.path.join(scripts_dir, "04_update_dashboard_cache.py")])
    time.sleep(1.8)

    # 5. 03:14 AM - Mock Slack Alert sliding in
    simulate_clock("03:14:00 AM")
    subprocess.run([sys.executable, os.path.join(scripts_dir, "05_slack_alert_popup.py")])
    time.sleep(1.0)

    # Voiceover recap summary card
    print(f"{BOLD}{'=' * 78}")
    print(f" {CYAN}VIDEO VOICEOVER TAKEAWAYS:{RESET}")
    print(f" {'=' * 78}")
    print(f" 1. {BOLD}Scheduling{RESET} (Cron): Only knows *when* to start. Completely blind to dependencies.")
    print(f" 2. {BOLD}Orchestration{RESET} (Airflow): Manages *order, state, retries, and data readiness* (A >> B >> C).")
    print(f" 3. {BOLD}ETL / Compute{RESET} (Spark/Snowflake): Does the *actual work*. Airflow directs the orchestra.")
    print(f"{'=' * 78}\n")

if __name__ == "__main__":
    main()

