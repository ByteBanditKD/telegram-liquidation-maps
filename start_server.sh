#!/bin/bash

# Bitcoin Liquidation Maps MCP Server Startup Script

echo "Starting Bitcoin Liquidation Maps MCP Server..."
echo "================================================"

# Check if Docker is available and start Selenium if needed
if command -v docker &> /dev/null; then
    echo "Docker found. Starting Selenium container..."
    docker-compose up -d selenium
    echo "Selenium container started on port 4444"
    echo "VNC viewer available on port 7900 (password: secret)"
    echo ""
else
    echo "Docker not found. Will use local Chrome driver."
    echo ""
fi

# Check if Chrome is available
if command -v google-chrome &> /dev/null; then
    echo "Chrome browser found."
elif command -v chromium-browser &> /dev/null; then
    echo "Chromium browser found."
else
    echo "Warning: No Chrome/Chromium browser found. Please install Chrome."
    echo "On Ubuntu/Debian: sudo apt-get install google-chrome-stable"
    echo "On CentOS/RHEL: sudo yum install google-chrome-stable"
fi

echo ""
echo "Starting MCP Server..."
echo "Use this server with any MCP-compatible LLM client."
echo ""
echo "Example requests:"
echo "- 'Retrieve a Bitcoin map on the 24 hour timeframe'"
echo "- 'Get me an Ethereum liquidation heatmap for 1 month'"
echo "- 'Show me the current BTC price'"
echo ""
echo "Press Ctrl+C to stop the server."
echo ""

# Start the MCP server
python liquidation_map_server.py