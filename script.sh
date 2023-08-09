#!/bin/bash

# Kill any process running on port 8000
lsof -i :8000 | awk 'NR>1 {print $2}' | xargs kill -9
lsof -i :3000 | awk 'NR>1 {print $2}' | xargs kill -9

# Navigate to your app directory
cd /home/ubuntu/language_app

# start environment
workon language_app

# Command to start your app
reflex run --env prod