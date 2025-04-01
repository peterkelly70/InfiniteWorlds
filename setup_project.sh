#!/bin/bash

# Project folder name
PROJECT_NAME="infiniteWorlds"

# Create project structure
mkdir -p "$PROJECT_NAME"/{model,view,controller,resources,map_packs}
touch "$PROJECT_NAME"/{main.py,README.md}

# Create empty module files
touch "$PROJECT_NAME"/model/__init__.py
touch "$PROJECT_NAME"/view/__init__.py
touch "$PROJECT_NAME"/controller/__init__.py

# Create key files
touch "$PROJECT_NAME"/model/map_data.py
touch "$PROJECT_NAME"/view/main_window.py
touch "$PROJECT_NAME"/controller/map_controller.py

echo "MVC structure created under ./$PROJECT_NAME"
