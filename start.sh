#!/bin/bash
SESSION_NAME="wootcord"

echo "Starting docker containers..."
docker compose up -d

if tmux has-session -t $SESSION_NAME 2>/dev/null; then
    echo ""
    echo "Wootcord is already running in tmux session '$SESSION_NAME'."
    read -p "Do you want to restart? (y/n): " choice
    
    case "$choice" in 
        y|Y ) 
            echo "Killing old session..."
            tmux kill-session -t $SESSION_NAME
            ;;
        * ) 
            echo "Attaching to existing session..."
            sleep 1
            tmux attach-session -t $SESSION_NAME
            exit 0
            ;;
    esac
fi

echo "Starting new session..."

tmux new-session -d -s $SESSION_NAME

tmux send-keys -t $SESSION_NAME:0.0 'python -m wootcord' C-m
tmux split-window -h -t $SESSION_NAME:0
tmux send-keys -t $SESSION_NAME:0.1 'python -m webhook' C-m
tmux select-layout -t $SESSION_NAME tiled
tmux attach-session -t $SESSION_NAME