#!/bin/bash
SESSION_NAME="wootcord"

if tmux has-session -t $SESSION_NAME 2>/dev/null; then
    tmux kill-session -t $SESSION_NAME
    echo "Successfully stopped wootcord"
else
    echo "No active session named '$SESSION_NAME' found. Nothing to kill."
fi

echo ""
read -p "Do you want to stop the Docker containers too? (y/n): " choice

case "$choice" in 
    y|Y ) 
        echo "Stopping Docker containers..."
        docker compose stop 
        echo "Docker containers stopped."
        ;;
    * ) 
        echo "Docker containers left running in the background."
        ;;
esac