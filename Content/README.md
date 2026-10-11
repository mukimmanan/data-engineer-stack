# Video Hook Demo Assets: Why Cron Fails & Why Airflow Exists (0:00 – 0:45)

This folder contains the complete simulation toolkit and standalone Python & terminal scripts corresponding to **The Hook (0:00 – 0:45)** of your video script.

---

## 📂 Folder Structure

```
Content/
├── crontab.txt                      # Mock Linux crontab configuration showing brittle schedules
├── simulate_cron_disaster.py       # Master timeline simulation script with ANSI colors & clocks
├── run_cron_disaster.sh            # Linux/macOS bash runner (interactive, tmux split panes, or flood)
├── run_cron_disaster.ps1           # Windows PowerShell runner (Windows Terminal split panes or multi-window)
├── run_cron_disaster.bat           # Windows 1-click batch launcher
├── README.md                       # This recording guide and script timing reference
└── scripts/
    ├── 01_extract_orders.py        # [02:00 AM] Extracts raw orders (Succeeds)
    ├── 02_snowflake_transform.py   # [02:05 AM] Slow Snowflake transform (Takes 20m instead of 5m)
    ├── 03_aggregate_metrics.py     # [02:10 AM] Runs prematurely, lock collision, floods red errors
    ├── 04_update_dashboard_cache.py# [02:15 AM] Corrupts executive KPI cache with negative revenue
    └── 05_slack_alert_popup.py     # [03:14 AM] Styled Slack P1 alert box popup
```

---

## 🎬 Video Recording Guide (Matching Your Script)

### Timestamp & Voiceover Alignment

| Timestamp | Visual Action | Spoken Voiceover Line | Trigger / Command |
|---|---|---|---|
| **0:00 – 0:10** | **Split terminal dark mode** showing Script 1 finishing and Script 2 hanging on query execution. | *"Picture this: You have five Python scripts that extract data, run queries in Snowflake, and update a dashboard. You set them up on a Linux cron job to run every night at 2 AM."* | Run `python Content/simulate_cron_disaster.py` or `Content/run_cron_disaster.ps1 -SplitWindows` |
| **0:10 – 0:25** | Script #3 triggers while Script #2 is still waiting for locks. **Red traceback errors flood the terminal screen**. | *"Everything is fine until Script #2 takes 20 minutes instead of 5. Script #3 starts before Script #2 finishes, feeds partial data into production, and by 8 AM your dashboard displays corrupted numbers."* | Script #3 & #4 output `SnowflakeError: lock timeout` and `AssertionError: Row count mismatch` |
| **0:25 – 0:35** | **Mock Slack Alert Box** pop-up slides in: `🚨 Production Alert: 03:14 AM — Partial Data Ingestion / Dashboard Corrupted`. | *"Cron didn't alert you. It didn't retry. It just ran on the clock. This exact disaster is why Apache Airflow exists."* | Script #5 renders the terminal Slack card |
| **0:35 – 0:45** | Summary takeaways appear on screen: **Scheduling vs. Orchestration vs. ETL**. | *"But beginners constantly mix up three things: Scheduling, Orchestration, and ETL. Today, we’re unpacking what Airflow actually is, what it isn’t, and where it fits in your stack."* | Transition directly into the Airflow 3 TaskFlow DAG in `airflow/dags/daily_kafka_to_delta_dag.py` |

---

## 🚀 How to Run for Recording

### Option A: Windows Terminal with Split Panes (Recommended for Windows)
If you have **Windows Terminal** installed, run:
```powershell
powershell -ExecutionPolicy Bypass -File Content/run_cron_disaster.ps1 -SplitWindows
```
*Effect*: Automatically creates 4 split panes in a single dark-mode window, launching the scripts simultaneously to create the exact "split terminal flooded with errors" aesthetic.

### Option B: Unified Timeline Simulator (Works Everywhere - Windows / Mac / Linux)
```bash
python Content/simulate_cron_disaster.py
```
*Effect*: Clears the terminal and animates the nightly timeline sequentially from 02:00 AM to 03:14 AM, pausing at each milestone, showing the warehouse queue lag, exploding into red tracebacks, and printing the Slack alert box.

### Option C: Linux / macOS Split Panes with `tmux`
```bash
bash Content/run_cron_disaster.sh --tmux
```
*Effect*: Launches a 4-pane tiled `tmux` session with dark theme, executing all scripts simultaneously.

### Option D: Standalone Slack Alert Popup Only
```bash
python Content/scripts/05_slack_alert_popup.py
```
*Effect*: Renders only the framed Slack alert card.
