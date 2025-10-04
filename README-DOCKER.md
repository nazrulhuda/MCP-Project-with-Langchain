# MCP Chatbot System - Docker Setup

This project has been dockerized with separate containers for each service:

## Architecture

- **Backend Container**: Flask web application with chatbot interface
- **Math Container**: MCP server for mathematical operations (HTTP on port 8002)
- **Weather Container**: MCP server for weather information (HTTP on port 8000)
- **System Container**: MCP server for system metrics (HTTP on port 8001)

## Prerequisites

1. **Docker & Docker Compose** installed
2. **Groq API Key** from https://console.groq.com/

## Quick Start

1. **Set up environment**:
   ```bash
   cp .env.docker .env
   # Edit .env and add your GROQ_API_KEY
   ```

2. **Start all services**:
   ```bash
   ./start-docker.sh
   ```

3. **Access the application**:
   - Open browser to http://localhost:5001
   - Chat with the AI assistant!

## Manual Docker Commands

### Build and Start
```bash
docker-compose up --build
```

### Start in Background
```bash
docker-compose up -d
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f mathserver
docker-compose logs -f weatherserver
docker-compose logs -f sysserver
```

### Stop Services
```bash
docker-compose down
```

### Rebuild Specific Service
```bash
docker-compose build mathserver
docker-compose up -d mathserver
```

## Service URLs

- **Main App**: http://localhost:5001
- **Math Server**: http://localhost:8002/mcp
- **Weather Server**: http://localhost:8000/mcp
- **System Server**: http://localhost:8001/mcp

## Troubleshooting

### Check Service Status
```bash
docker-compose ps
```

### Check Individual Container Logs
```bash
docker logs mcp-backend
docker logs mcp-math-server
docker logs mcp-weather-server
docker logs mcp-sys-server
```

### Restart All Services
```bash
docker-compose restart
```

### Clean Up
```bash
# Stop and remove containers
docker-compose down

# Remove images
docker-compose down --rmi all

# Remove volumes (if any)
docker-compose down -v
```

## Development

### Making Changes
1. Edit the source code
2. Rebuild the affected service: `docker-compose build <service-name>`
3. Restart: `docker-compose up -d <service-name>`

### Adding New MCP Servers
1. Create new Dockerfile
2. Add service to docker-compose.yml
3. Update backend environment variables
4. Rebuild and restart

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | Groq API key for LLM | Required |
| `FLASK_PORT` | Flask app port | 5001 |
| `SYS_MCP_URL` | System server URL | http://sysserver:8001/mcp |
| `WEATHER_MCP_URL` | Weather server URL | http://weatherserver:8000/mcp |
| `MATH_MCP_URL` | Math server URL | http://mathserver:8002/mcp |

## Network

All services communicate through a Docker network called `mcp-network`. Services can reach each other using their container names as hostnames.

