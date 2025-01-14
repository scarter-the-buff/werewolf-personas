#!/bin/bash

# Function to kill processes running on specific ports
kill_process_on_port() {
  local port=$1
  # Find the PID of the process using the port (netstat -ano, then taskkill using PID)
  pid=$(netstat -ano | grep ":$port" | awk '{print $5}' | tail -n 1)

  if [ -n "$pid" ]; then
    echo "Stopping process on port $port (PID: $pid)..."
    taskkill //F //PID $pid
  else
    echo "No process running on port $port."
  fi
}

# Deactivate any active virtual environment and activate the required one
deactivate 2>/dev/null || true
source venv/Scripts/activate

# Kill React (default port: 3000) and Django (default port: 8000) instances
kill_process_on_port 3000
kill_process_on_port 8000

# Start `npm run start` in a new Git Bash terminal
"C:\Program Files\Git\bin\bash.exe" -c "echo 'Starting npm...'; npm run start; exec bash" &

# Start `python manage.py runserver` in another new Git Bash terminal
"C:\Program Files\Git\bin\bash.exe" -c "echo 'Starting Django server...'; python manage.py runserver; exec bash" &
