# MCP Chatbot with Flask Frontend

This project combines the MCP (Model Context Protocol) tools with a beautiful Flask web interface to create an interactive AI chatbot.

## Features

- **Math Operations**: Perform mathematical calculations using the math MCP server
- **Weather Information**: Get weather data using the weather MCP server
- **Modern UI**: Beautiful Bootstrap-based chat interface
- **Real-time Chat**: Interactive chat experience with the AI agent

## Prerequisites

1. **Python 3.8+** installed
2. **Groq API Key** - You need to set up your Groq API key

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   Create a `.env` file in the project root with:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

3. **Get your Groq API key**:
   - Visit [Groq Console](https://console.groq.com/)
   - Create an account and get your API key
   - Add it to the `.env` file

## Running the Chatbot

### Option 1: Automatic Startup (Recommended)
```bash
python start_chatbot.py
```
This will:
- Start the weather MCP server
- Start the Flask application
- Open your browser automatically

### Option 2: Manual Startup
1. **Start the weather server** (in one terminal):
   ```bash
   python weather.py
   ```

2. **Start the Flask app** (in another terminal):
   ```bash
   python app.py
   ```

3. **Open your browser** and go to: `http://localhost:5000`

## Usage

1. Open the chatbot in your browser
2. Type your questions in the chat input
3. The AI will respond using the available MCP tools

### Example Questions:
- **Math**: "What's (15 + 27) × 3?"
- **Weather**: "What's the weather like in California?"
- **General**: "Can you help me with calculations?"

## Project Structure

```
├── app.py                 # Main Flask application
├── weather.py            # Weather MCP server
├── mathserver.py         # Math MCP server
├── templates/
│   └── index.html       # Chatbot HTML template
├── static/
│   └── style.css        # Chatbot styling
├── start_chatbot.py     # Automatic startup script
├── requirements.txt      # Python dependencies
└── README_CHATBOT.md    # This file
```

## Troubleshooting

1. **"Agent is still initializing"**: Wait a few seconds for the MCP tools to load
2. **Weather server not responding**: Make sure `weather.py` is running on port 8000
3. **Math operations not working**: Ensure `mathserver.py` can be executed

## Stopping the Application

- Press `Ctrl+C` in the terminal running the Flask app
- The weather server will be automatically terminated

## Customization

- **Add new MCP tools**: Modify `app.py` to include additional MCP servers
- **Change the UI**: Edit `templates/index.html` and `static/style.css`
- **Modify responses**: Update the agent configuration in `app.py`

## Security Notes

- Keep your Groq API key secure and never commit it to version control
- The Flask app runs in debug mode by default (change for production)
- Consider adding authentication for production use
