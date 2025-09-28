#!/bin/bash
# Installation script for RGB LED Button Service

echo "Installing RGB LED Button Service..."

# Update package list
echo "Updating package list..."
sudo apt update

# Install Tinkerforge daemon and MP3 player
echo "Installing Tinkerforge daemon and MP3 player..."
sudo apt install -y brickd mpg123

# Start and enable brickd service
echo "Starting Tinkerforge daemon..."
sudo systemctl start brickd
sudo systemctl enable brickd

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Make scripts executable
echo "Making scripts executable..."
chmod +x button_service.py
chmod +x program1.py
chmod +x program2.py
chmod +x program3.py

echo "Installation complete!"
echo ""
echo "Next steps:"
echo "1. Edit button_service.py to set your actual button UIDs"
echo "2. Modify the programs list if needed"
echo "3. Run the service with: python3 button_service.py"
echo ""
echo "To check if brickd is running: sudo systemctl status brickd"
