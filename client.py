from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv


load_dotenv()

import asyncio

async def main():
    client=MultiServerMCPClient(
        {
            "math":{
                "command":"python",
                "args":["mathserver.py"], ## Ensure correct absolute path
                "transport":"stdio",
            
            },
            "weather": {
                "url": "http://localhost:8000/mcp",  # Ensure server is running here
                "transport": "streamable_http",
            }

        }
    )

    # Get Groq API key from environment
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY environment variable not set. Please set your Groq API key.")

    tools=await client.get_tools()
    
   
    
    model=ChatGroq(
        groq_api_key=groq_api_key,
        model_name="qwen/qwen3-32b"
    )
    agent=create_react_agent(
        model,tools
    )

    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
    )

    print("Math response:", math_response['messages'][-1].content)

    weather_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what is the weather in California?"}]}
    )
    print("Weather response:", weather_response['messages'][-1].content)

asyncio.run(main())
