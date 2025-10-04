# MCP Chatbot Setup Instructions

## Prerequisites
- Python 3.13 or higher
- Groq API key (get one from https://console.groq.com/)

## Setup Steps

### 1. Install Dependencies
```bash
py -m pip install -r requirements.txt
```

### 2. Set up Environment Variables
Create a `.env` file in the project root with your Groq API key:
```bash
GROQ_API_KEY=your_actual_groq_api_key_here
```

### 3. Start the Chatbot System
Run the startup script:
```bash
py start_chatbot.py
```

This will:
- Start the weather MCP server on port 8000
- Start the Flask chatbot application on port 5000
- Open your browser to http://localhost:5000

## Manual Startup (Alternative)

If you prefer to start services manually:

### Start Weather Server
```bash
py weather.py
```

### Start Flask App (in a new terminal)
```bash
py app.py
```

## Features

The chatbot can:
- Perform mathematical calculations using the math MCP server
- Get weather information using the weather MCP server
- Answer general questions using Groq's Qwen3-32B model
- Provide a beautiful web interface for chatting

## Troubleshooting

### Port Already in Use
If you get port conflicts:
- Change the port in `app.py` (line with `app.run(port=5000)`)
- Change the port in `weather.py` if needed

### API Key Issues
- Make sure your `.env` file exists and contains the correct API key
- Verify your Groq API key is valid and has sufficient credits

### Module Import Errors
- Ensure all dependencies are installed: `py -m pip install -r requirements.txt`
- Check that you're using Python 3.13+

## Project Structure

- `app.py` - Flask backend with MCP integration
- `weather.py` - Weather MCP server
- `mathserver.py` - Math MCP server
- `templates/index.html` - Chatbot frontend
- `start_chatbot.py` - Automated startup script
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (create this file)
