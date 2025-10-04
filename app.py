from flask import Flask, render_template, request, jsonify
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
import asyncio
import time
import httpx
import threading

load_dotenv()

app = Flask(__name__)

# Global variables to store the agent
agent = None
client = None

#VERY IMPORTANT:
#find out how two tools can communicate togehter?
#is Langchain capable of invoking one tool after the other in sequence?
# look at tutorials where multiple tools are present on one MCP client? 

def initialize_agent():
    """Initialize the MCP client and agent in a separate thread"""
    global agent, client
    async def _setup_once():
        """Perform one attempt to setup the client and agent.

        This function assumes dependent HTTP MCP servers are running and will
        raise on failure so the outer thread can retry with backoff.
        """
        global agent, client
        sys_mcp_url = os.getenv("SYS_MCP_URL", "http://localhost:8001/mcp")
        weather_mcp_url = os.getenv("WEATHER_MCP_URL", "http://localhost:8000/mcp")
        math_mcp_url = os.getenv("MATH_MCP_URL", "http://localhost:8002/mcp")

        async with httpx.AsyncClient(timeout=2.0) as hc:
            # Probe endpoints with retries
            for i in range(40):
                ok_sys = False
                ok_weather = False
                ok_math = False
                try:
                    r = await hc.get(sys_mcp_url)
                    ok_sys = r.status_code in (200, 202, 406)
                except Exception:
                    ok_sys = False

                try:
                    r = await hc.get(weather_mcp_url)
                    ok_weather = r.status_code in (200, 202, 406)
                except Exception:
                    ok_weather = False

                try:
                    r = await hc.get(math_mcp_url)
                    ok_math = r.status_code in (200, 202, 406)
                except Exception:
                    ok_math = False

                if ok_sys and ok_weather and ok_math:
                    break
                if i % 5 == 0:
                    print(f"Waiting for MCP endpoints: sys={sys_mcp_url} ok={ok_sys}, weather={weather_mcp_url} ok={ok_weather}, math={math_mcp_url} ok={ok_math}")
                await asyncio.sleep(0.5)
            else:
                raise ConnectionError(f"Dependent MCP servers not reachable: sys={sys_mcp_url}, weather={weather_mcp_url}, math={math_mcp_url}")

        client = MultiServerMCPClient(
            {
                "math": {
                    "url": math_mcp_url,
                    "transport": "streamable_http",
                },
                "sys": {
                    "url": sys_mcp_url,
                    "transport": "streamable_http",
                },
                "weather": {
                    "url": weather_mcp_url,
                    "transport": "streamable_http",
                },
            }
        )

        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY environment variable not set. Please set your Groq API key.")

        # Try get_tools with a few retries; raise if still failing
        last_err = None
        for attempt in range(1, 11):
            try:
                tools = await client.get_tools()
                break
            except Exception as e:
                last_err = e
                print(f"get_tools attempt {attempt} failed: {e}")
                await asyncio.sleep(1.0)
        else:
            raise last_err

        model = ChatGroq(groq_api_key=groq_api_key, model_name="qwen/qwen3-32b")
        agent = create_react_agent(model, tools)

    # Run setup in a loop so transient errors don't kill the thread.
    while True:
        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(_setup_once())
            print("Agent initialized successfully")
            loop.close()
            break
        except Exception as e:
            try:
                loop.close()
            except Exception:
                pass
            print(f"Agent setup failed, will retry in 5s: {e}")
            time.sleep(5)

# Initialize agent in background thread
threading.Thread(target=initialize_agent, daemon=True).start()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get', methods=['POST'])
def get_bot_response():
    try:
        user_message = request.form['msg']
        
        if agent is None:
            return "Agent is still initializing. Please wait a moment and try again."
        
        # Create a new event loop for this request
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Get response from agent
            response = loop.run_until_complete(
                agent.ainvoke({
                    "messages": [{"role": "user", "content": user_message}]
                })
            )
            
            # Extract the last message content
            bot_response = response['messages'][-1].content
            
            return bot_response
            
        finally:
            loop.close()
            
    except Exception as e:
        return f"Error: {str(e)}"



if __name__ == '__main__':
    flask_port = int(os.getenv("FLASK_PORT", "5001"))
    app.run(debug=True, host='0.0.0.0', port=flask_port)
