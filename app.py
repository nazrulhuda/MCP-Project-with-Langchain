from flask import Flask, render_template, request, jsonify
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
import asyncio
import threading

load_dotenv()

app = Flask(__name__)

# Global variables to store the agent
agent = None
client = None

#VERY IMPORTANT:
#find out how two tools can communicate togehter?
#is Langchain capable of invoking one tool after the other in sequence 
# look at tutorials where multiple tools are present on one MCP client. 

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
                "weather": {
                    "url": "http://localhost:8000/mcp",
                    "transport": "streamable_http",
                }
            }
        )
        
        # Get Groq API key from environment
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY environment variable not set. Please set your Groq API key.")
        
        #read documentation of "get_tools()"
        #understand what is returned by get_tools()
        tools = await client.get_tools()
        
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
