#!/usr/bin/env bash
# ==============================================================================
# Terminal Runner: The Cron Disaster Hook (0:00 - 0:45)
# Can run as a full interactive timeline or launch a 4-pane tmux session!
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_CMD="python3"

if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

show_menu() {
    clear
    echo "=================================================================="
    echo " 🎬 Video Hook Asset: The Cron Disaster (Airflow vs. Cron)"
    echo "=================================================================="
    echo " 1) Run Unified Simulation (Cinematic Single Terminal with Timings)"
    echo " 2) Launch 4-Pane Split Terminal (tmux required - Dark Mode Visual)"
    echo " 3) Fire All 5 Scripts Concurrently in Background (Stdout Flood)"
    echo " 4) Exit"
    echo "=================================================================="
    read -p "Select demo mode [1-4]: " choice

    case $choice in
        1)
            $PYTHON_CMD "$SCRIPT_DIR/simulate_cron_disaster.py"
            ;;
        2)
            launch_tmux_split
            ;;
        3)
            run_concurrent_flood
            ;;
        *)
            echo "Exiting."
            exit 0
            ;;
    esac
}

launch_tmux_split() {
    if ! command -v tmux &> /dev/null; then
        echo "tmux is not installed on this system. Falling back to Unified Simulation..."
        sleep 2
        $PYTHON_CMD "$SCRIPT_DIR/simulate_cron_disaster.py"
        return
    fi

    SESSION="cron_disaster"
    tmux kill-session -t $SESSION 2>/dev/null

    # Create session with dark theme
    tmux new-session -d -s $SESSION -n "pipeline" "$PYTHON_CMD $SCRIPT_DIR/scripts/01_extract_orders.py; read -p 'Press enter to close...'"
    tmux split-window -h -t $SESSION:0 "$PYTHON_CMD $SCRIPT_DIR/scripts/02_snowflake_transform.py; read -p 'Press enter to close...'"
    tmux split-window -v -t $SESSION:0.0 "$PYTHON_CMD $SCRIPT_DIR/scripts/03_aggregate_metrics.py; read -p 'Press enter to close...'"
    tmux split-window -v -t $SESSION:0.1 "$PYTHON_CMD $SCRIPT_DIR/scripts/04_update_dashboard_cache.py; $PYTHON_CMD $SCRIPT_DIR/scripts/05_slack_alert_popup.py; read -p 'Press enter to close...'"

    # Select layout
    tmux select-layout -t $SESSION:0 tiled
    tmux attach-session -t $SESSION
}

run_concurrent_flood() {
    echo -e "\n🔥 Firing all 5 cron scripts simultaneously to simulate uncoordinated jobs...\n"
    $PYTHON_CMD "$SCRIPT_DIR/scripts/01_extract_orders.py" &
    $PYTHON_CMD "$SCRIPT_DIR/scripts/02_snowflake_transform.py" &
    sleep 1
    $PYTHON_CMD "$SCRIPT_DIR/scripts/03_aggregate_metrics.py" &
    sleep 2
    $PYTHON_CMD "$SCRIPT_DIR/scripts/04_update_dashboard_cache.py" &
    wait
    $PYTHON_CMD "$SCRIPT_DIR/scripts/05_slack_alert_popup.py"
}

# If arguments passed, run directly
if [ "$1" == "--tmux" ]; then
    launch_tmux_split
elif [ "$1" == "--flood" ]; then
    run_concurrent_flood
elif [ "$1" == "--single" ]; then
    $PYTHON_CMD "$SCRIPT_DIR/simulate_cron_disaster.py"
else
    show_menu
fi

