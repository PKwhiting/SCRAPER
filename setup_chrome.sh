#!/usr/bin/env bash
set -e

# Install Chrome if not present
echo "Checking for Google Chrome..."
if ! command -v google-chrome &> /dev/null && ! command -v google-chrome-stable &> /dev/null; then
    echo "Google Chrome not found. Installing..."
    sudo apt update
    sudo apt install -y wget
    wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O /tmp/google-chrome.deb
    sudo apt install -y /tmp/google-chrome.deb
    rm /tmp/google-chrome.deb
else
    echo "Google Chrome is already installed."
fi

# Detect Chrome binary path
CHROME_PATH=""
if command -v google-chrome &> /dev/null; then
    CHROME_PATH=$(command -v google-chrome)
elif command -v google-chrome-stable &> /dev/null; then
    CHROME_PATH=$(command -v google-chrome-stable)
fi

if [ -z "$CHROME_PATH" ]; then
    echo "Could not find Chrome binary after installation. Please set CHROME_BINARY manually in your .env."
    exit 1
fi

echo "Detected Chrome binary: $CHROME_PATH"

# Update or add CHROME_BINARY in .env
ENV_FILE=".env"
if [ ! -f "$ENV_FILE" ]; then
    touch "$ENV_FILE"
fi
if grep -q '^CHROME_BINARY=' "$ENV_FILE"; then
    sed -i "s|^CHROME_BINARY=.*|CHROME_BINARY=$CHROME_PATH|" "$ENV_FILE"
else
    echo "CHROME_BINARY=$CHROME_PATH" >> "$ENV_FILE"
fi

echo "CHROME_BINARY set to $CHROME_PATH in $ENV_FILE."
echo "Setup complete."
