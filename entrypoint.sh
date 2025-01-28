#!/bin/bash

# Fail on any error
set -e

# Update and install necessary packages
echo "Updating packages..."
apt-get update && apt-get install -y \
    python3.12-venv \
    openssh-server \
    curl \
    net-tools \
    supervisor

# Set up SSH service (for debugging if needed)
echo "Setting up SSH..."
mkdir -p /var/run/sshd
echo "root:Docker!" | chpasswd
sed -i 's/^#PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config
sed -i 's/^#PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Start SSH in the background
service ssh start

# Set up Python environment (if required)
echo "Checking Python environment..."
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate

# Install project dependencies
echo "Installing dependencies..."
pip install --no-cache-dir -r requirements.txt

# Run database initialization or migrations
echo "Initializing database..."
python seed_data.py

# Start the FastAPI application
echo "Starting FastAPI application..."
uvicorn app:app --host 127.0.0.1 --port 8000
