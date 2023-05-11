#!/bin/bash

# Install requirements.txt
pip install -r requirements.txt

# Prompt the user for EMAIL
read -p "Enter your email: " EMAIL

# Prompt the user for BIRTHDATE
read -p "Enter your birthdate: " BIRTHDATE

# Execute the main.py script with the provided arguments
python main.py -m "$EMAIL" -b "$BIRTHDATE"

docker build -t hype_dashboard:latest .