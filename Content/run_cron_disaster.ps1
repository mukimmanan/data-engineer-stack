# ==============================================================================
# Windows PowerShell Runner: The Cron Disaster Hook (0:00 - 0:45)
# Launches either Windows Terminal split panes or parallel PowerShell windows!
# ==============================================================================

param (
    [switch]$SplitWindows,
    [switch]$Single
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ScriptsPath = Join-Path $ScriptDir "scripts"

function Show-Menu {
    Clear-Host
    Write-Host "==================================================================" -ForegroundColor Cyan
    Write-Host " 🎬 Video Hook Asset: The Cron Disaster (Airflow vs. Cron)" -ForegroundColor Yellow
    Write-Host "==================================================================" -ForegroundColor Cyan
    Write-Host " 1) Run Unified Simulation (Cinematic Single Terminal with Timings)"
    Write-Host " 2) Launch 4-5 Windows Terminal Split Panes (wt.exe split-pane)"
    Write-Host " 3) Launch 4-5 Separate PowerShell Windows Simultaneously"
    Write-Host " 4) Exit"
    Write-Host "=================================================================="
    $choice = Read-Host "Select demo mode [1-4]"

    switch ($choice) {
        "1" { python "$ScriptDir\simulate_cron_disaster.py" }
        "2" { Launch-WTSplit }
        "3" { Launch-MultipleWindows }
        default { exit }
    }
}

function Launch-WTSplit {
    $wtPath = (Get-Command wt.exe -ErrorAction SilentlyContinue)
    if (-not $wtPath) {
        Write-Warning "Windows Terminal (wt.exe) not found. Launching separate windows instead..."
        Launch-MultipleWindows
        return
    }

    Write-Host "Launching Windows Terminal with 4 split panes in dark mode..." -ForegroundColor Green
    
    $cmd1 = "python `"$ScriptsPath\01_extract_orders.py`""
    $cmd2 = "python `"$ScriptsPath\02_snowflake_transform.py`""
    $cmd3 = "python `"$ScriptsPath\03_aggregate_metrics.py`""
    $cmd4 = "python `"$ScriptsPath\04_update_dashboard_cache.py`"; python `"$ScriptsPath\05_slack_alert_popup.py`""

    # Windows Terminal split-pane command
    wt new-tab --title "Script 1: Extract" powershell -NoExit -Command $cmd1 `; `
       split-pane -H --title "Script 2: Snowflake" powershell -NoExit -Command $cmd2 `; `
       split-pane -V --title "Script 3: Aggregation Error" powershell -NoExit -Command $cmd3 `; `
       split-pane -V --title "Script 4: Dashboard Cache & Alert" powershell -NoExit -Command $cmd4
}

function Launch-MultipleWindows {
    Write-Host "Launching 4 separate PowerShell windows firing simultaneously..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "python `"$ScriptsPath\01_extract_orders.py`""
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "python `"$ScriptsPath\02_snowflake_transform.py`""
    Start-Sleep -Seconds 1
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "python `"$ScriptsPath\03_aggregate_metrics.py`""
    Start-Sleep -Seconds 1
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "python `"$ScriptsPath\04_update_dashboard_cache.py`"; python `"$ScriptsPath\05_slack_alert_popup.py`""
}

if ($SplitWindows) {
    Launch-WTSplit
} elseif ($Single) {
    python "$ScriptDir\simulate_cron_disaster.py"
} else {
    Show-Menu
}

