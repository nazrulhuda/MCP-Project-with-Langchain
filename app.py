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
    
    async def setup():
        global agent, client
        client = MultiServerMCPClient(
            {
                "math": {
                    "command": "python",
                    "args": ["mathserver.py"],
                    "transport": "stdio",
                },
                "sys": {
                    "command": "python",
                    "args": ["sysserver.py"],
                    "transport": "stdio",
                },
                "weather": {
                    "url": "http://localhost:8000/mcp",
                    "transport": "streamable_http",
                },
            }
        )
        
        # Wait for sys MCP server to be reachable to avoid connection errors
        # Wait for weather MCP HTTP server to be reachable
        weather_url = "http://localhost:8000/mcp"
        async with httpx.AsyncClient(timeout=2.0) as hc:
            for _ in range(20):  # ~10s total
                try:
                    resp = await hc.get(weather_url)
                    if resp.status_code in (200, 202, 406):
                        break
                except Exception:
                    pass
                await asyncio.sleep(0.5)

        # Get Groq API key from environment
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY environment variable not set. Please set your Groq API key.")
        
        #read documentation of "get_tools()"
        #understand what is returned by get_tools()
        # Retry loading tools in case servers are still warming up
        last_err = None
        for _ in range(5):
            try:
                tools = await client.get_tools()
                break
            except Exception as e:
                last_err = e
                await asyncio.sleep(1.0)
        else:
            raise last_err
        
        model = ChatGroq(
            groq_api_key=groq_api_key,
            model_name="qwen/qwen3-32b"
        )
        #does the agent share the tools for every request of the user?
        #read the documentation of "create_react_agent()""
        agent = create_react_agent(model, tools)
    
    # Run the async setup in a new event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(setup())
    loop.close()

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


@app.route('/api/cpu')
def api_cpu():
    try:
        if agent is None:
            return jsonify({"error": "Agent initializing"}), 503
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            resp = loop.run_until_complete(
                agent.ainvoke({
                    "messages": [{"role": "user", "content": "What is the CPU utilization right now? Use sys tools."}]
                })
            )
            msg = resp['messages'][-1].content
            return jsonify({"cpu": msg})
        finally:
            loop.close()
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/memory')
def api_memory():
    try:
        if agent is None:
            return jsonify({"error": "Agent initializing"}), 503
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            resp = loop.run_until_complete(
                agent.ainvoke({
                    "messages": [{"role": "user", "content": "What is the memory utilization right now? Use sys tools."}]
                })
            )
            msg = resp['messages'][-1].content
            return jsonify({"memory": msg})
        finally:
            loop.close()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
