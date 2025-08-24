## MCP + LangChain + Groq Demo (Python)

This repo demonstrates how to build a LangChain agent that can call tools exposed via the Model Context Protocol (MCP). It connects to two MCP tool servers:

- Math server (`mathserver.py`) over `stdio`
- Weather server (`weather.py`) over HTTP (`/mcp`)

The agent uses Groq via `langchain-groq` for chat completion.

### Repo layout

- `client.py`: LangGraph ReAct agent that loads tools from MCP servers and calls a Groq model via `ChatGroq`.
- `mathserver.py`: MCP tool server exposing `add(a,b)` and `multiple(a,b)` over `stdio`.
- `weather.py`: MCP tool server exposing `get_weather(location)` over HTTP.
- `requirements.txt` / `pyproject.toml`: Python dependencies.

### Prerequisites

- Python 3.13+ (per `pyproject.toml`)
- A Groq API key
- Windows PowerShell users may need to adjust execution policy to activate venv

### Setup

1) Download uv in windows:

```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

```

in linux: 

```
curl -LsSf https://astral.sh/uv/install.sh | sh

```

2) Create and activate a virtual environment

```
uv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.venv\Scripts\activate

```

3) Install dependencies

```
uv add -r requirements.txt
```

4) Configure your Groq API key

Option A: Create a `.env` file in the project root

```
GROQ_API_KEY=your_actual_groq_api_key
```

Option B: Set an environment variable (temporary, current session)

```powershell
$env:GROQ_API_KEY="your_actual_groq_api_key"
```

### Running the demo

The client launches the math MCP server itself (via `stdio`). You must run the weather server in a separate terminal before starting the client.

1) Start the weather MCP server (Terminal A)

```
python weather.py
```

This should start an HTTP server on `http://localhost:8000/mcp`.

2) Start the Math MCP server (Terminal B):
```
python mathserver.py
```

3) Run the client (Terminal C)

```
python client.py
```

You should see the agent call the math tool first, then the weather tool, and print the final responses.





