#!/bin/bash

source venv/Scripts/activate

# Start `npm run start` in a new Git Bash terminal
"C:\Program Files\Git\bin\bash.exe" -c "echo 'Starting npm...'; npm run start; exec bash" &

# Start `python manage.py runserver` in another new Git Bash terminal
"C:\Program Files\Git\bin\bash.exe" -c "echo 'Starting Django server...'; python manage.py runserver; exec bash" &
