#!/bin/bash

# MCP Chatbot System - Easy Startup Script

echo "🚀 Starting MCP Chatbot System..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating template..."
    echo "GROQ_API_KEY=your_groq_api_key_here" > .env
    echo ""
    echo "📝 Please edit .env file and add your GROQ_API_KEY"
    echo "   Get your API key from: https://console.groq.com/"
    echo ""
    echo "   Then run this script again!"
    exit 1
fi

# Check if GROQ_API_KEY is set to placeholder
if grep -q "your_groq_api_key_here" .env; then
    echo "⚠️  Please set your GROQ_API_KEY in .env file"
    echo "   Get your API key from: https://console.groq.com/"
    exit 1
fi

echo "✅ Environment file found with API key"

# Build and start all services
echo "🔨 Building Docker images..."
docker-compose build

echo "🚀 Starting all services..."
docker-compose up -d

echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
echo "🔍 Checking service status..."
docker-compose ps

echo ""
echo "🎉 MCP Chatbot System is running!"
echo ""
echo "📊 Service URLs:"
echo "   • Backend (Flask): http://localhost:5001"
echo "   • Math Server: http://localhost:8002"
echo "   • Weather Server: http://localhost:8000"
echo "   • System Server: http://localhost:8001"
echo ""
echo "🌐 Open your browser and go to: http://localhost:5001"
echo ""
echo "📋 To view logs: docker-compose logs -f"
echo "🛑 To stop: docker-compose down"
