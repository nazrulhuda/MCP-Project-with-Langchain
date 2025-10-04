# MCP Chatbot System - Dockerized

A fully dockerized MCP (Model Context Protocol) chatbot system with separate containers for each service, featuring mathematical operations, weather information, and system monitoring capabilities.

## 🏗️ Architecture

This system consists of 4 Docker containers:

- **Backend Container**: Flask web application with chatbot interface
- **Math Container**: MCP server for mathematical operations (HTTP on port 8002)
- **Weather Container**: MCP server for weather information (HTTP on port 8000)
- **System Container**: MCP server for system metrics (HTTP on port 8001)

## 🚀 Quick Start

### Prerequisites

1. **Docker & Docker Compose** installed
2. **Groq API Key** from https://console.groq.com/

### 1. Set Up Environment

```bash
# Clone or download the project
cd MCP-Project-with-Langchain-resource-utilization

# Create environment file
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
```

**⚠️ Important**: Replace `your_groq_api_key_here` with your actual Groq API key from https://console.groq.com/

### 2. Start All Services

```bash
# Build and start all containers
docker-compose up --build

# Or start in background
docker-compose up -d --build
```

### 3. Access the Application

- **Web Interface**: http://localhost:5001
- **Math Server**: http://localhost:8002/mcp
- **Weather Server**: http://localhost:8000/mcp
- **System Server**: http://localhost:8001/mcp

## 🎯 Usage

### Web Interface

1. Open your browser to http://localhost:5001
2. Chat with the AI assistant about:
   - **Math**: "What is 15 + 25?" or "Calculate 7 * 8"
   - **Weather**: "What's the weather in California?"
   - **System**: "What is the CPU utilization?" or "Check memory usage"
   - **Complex queries**: "Calculate 12 * 15 and tell me the current memory usage"

### API Testing

You can also test the chatbot via API:

```bash
# Test math
curl -X POST http://localhost:5001/get \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "msg=What is 7 * 8?"

# Test system monitoring
curl -X POST http://localhost:5001/get \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "msg=What is the CPU utilization?"

# Test weather
curl -X POST http://localhost:5001/get \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "msg=What is the weather in New York?"
```

## 🛠️ Management Commands

### View Service Status
```bash
docker-compose ps
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

### Restart Services
```bash
docker-compose restart
```

### Rebuild Specific Service
```bash
docker-compose build mathserver
docker-compose up -d mathserver
```

## 📁 Project Structure

```
MCP-Project-with-Langchain-resource-utilization/
├── app.py                          # Flask web application
├── mathserver.py                   # Math MCP server
├── weather.py                      # Weather MCP server
├── sysserver.py                    # System MCP server
├── client.py                       # Standalone test client
├── config.py                       # Configuration
├── requirements.txt                # Python dependencies
├── docker-compose.yml              # Docker orchestration
├── Dockerfile.backend             # Backend container
├── Dockerfile.math               # Math server container
├── Dockerfile.weather            # Weather server container
├── Dockerfile.sys                # System server container
├── start-docker.sh               # Easy startup script
├── templates/
│   └── index.html                 # Web interface
├── static/
│   └── style.css                  # CSS styles
└── README.md                      # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | Groq API key for LLM | Required |
| `FLASK_PORT` | Flask app port | 5001 |
| `SYS_MCP_URL` | System server URL | http://sysserver:8001/mcp |
| `WEATHER_MCP_URL` | Weather server URL | http://weatherserver:8000/mcp |
| `MATH_MCP_URL` | Math server URL | http://mathserver:8002/mcp |

### MCP Server Ports

- **Math Server**: 8002
- **Weather Server**: 8000
- **System Server**: 8001
- **Backend**: 5001

## 🐳 Docker Details

### Container Images

- **Backend**: `mcp-project-with-langchain-resource-utilization-backend`
- **Math**: `mcp-project-with-langchain-resource-utilization-mathserver`
- **Weather**: `mcp-project-with-langchain-resource-utilization-weatherserver`
- **System**: `mcp-project-with-langchain-resource-utilization-sysserver`

### Network

All services communicate through a Docker network called `mcp-network`. Services can reach each other using their container names as hostnames.

## 🔍 Troubleshooting

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

### Common Issues

1. **"Agent is still initializing"**
   - Check if GROQ_API_KEY is set correctly
   - Verify all MCP servers are running: `docker-compose ps`

2. **"Invalid API Key" error**
   - Ensure your Groq API key is valid
   - Check the .env file has the correct key

3. **Services not starting**
   - Check Docker is running: `docker ps`
   - Rebuild containers: `docker-compose build`

### Clean Up
```bash
# Stop and remove containers
docker-compose down

# Remove images
docker-compose down --rmi all

# Remove volumes (if any)
docker-compose down -v
```

## 🚀 Development

### Making Changes

1. Edit the source code
2. Rebuild the affected service: `docker-compose build <service-name>`
3. Restart: `docker-compose up -d <service-name>`

### Adding New MCP Servers

1. Create new Dockerfile
2. Add service to docker-compose.yml
3. Update backend environment variables
4. Rebuild and restart

## 📋 Features

### Math Operations
- Addition: `add(a, b)`
- Multiplication: `multiple(a, b)`

### System Monitoring
- CPU utilization: `get_cpu_now()`
- Memory usage: `get_memory_now()`
- Historical data: `get_cpu_at(timestamp)`, `get_memory_at(timestamp)`

### Weather Information
- Location-based weather: `get_weather(location)`
- Supports major US states and cities

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with Docker
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Verify all services are running: `docker-compose ps`
3. Check logs: `docker-compose logs -f`
4. Ensure your Groq API key is valid

---

**Happy Chatting! 🤖✨**