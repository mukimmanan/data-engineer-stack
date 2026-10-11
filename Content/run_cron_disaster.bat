@echo off
REM ==============================================================================
REM Batch Runner: The Cron Disaster Hook (Windows Quick Launcher)
REM ==============================================================================

set SCRIPT_DIR=%~dp0

echo ==================================================================
echo  Video Hook Asset: The Cron Disaster (Airflow vs. Cron)
echo ==================================================================
echo  1) Run Unified Simulation (Single Terminal)
echo  2) Launch Windows Terminal Split Panes (wt.exe)
echo  3) Launch Separate Windows Simultaneously
echo ==================================================================
set /p choice="Select demo mode [1-3]: "

if "%choice%"=="1" (
    python "%SCRIPT_DIR%simulate_cron_disaster.py"
) else if "%choice%"=="2" (
    powershell -ExecutionPolicy Bypass -File "%SCRIPT_DIR%run_cron_disaster.ps1" -SplitWindows
) else if "%choice%"=="3" (
    powershell -ExecutionPolicy Bypass -File "%SCRIPT_DIR%run_cron_disaster.ps1"
) else (
    python "%SCRIPT_DIR%simulate_cron_disaster.py"
)

