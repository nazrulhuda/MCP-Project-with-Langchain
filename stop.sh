#!/bin/bash

# MCP Chatbot System - Stop Script

echo "🛑 Stopping MCP Chatbot System..."

docker-compose down

echo "✅ All services stopped!"
echo ""
echo "To start again, run: ./run.sh"
