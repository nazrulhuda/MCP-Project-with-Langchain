from mcp.server.fastmcp import FastMCP

mcp=FastMCP("Weather")
#read the documentation of @mcp.tools decorator
#find out how does this operation: "agent = create_react_agent(model, tools)"
#understand what capabilities does the tools have?

#there is  adocstring here, how does the docstring context get shared with the remote LLM

#do a test where you deliberately corrupt the docstring to something else!
# and then watch the response of GROK
@mcp.tool()
async def get_weather(location:str)->str:
    """Get the weather for a specific location."""
    location = location.lower().strip()
    
    # Weather responses for different states/regions
    weather_data = {
        "california": "It's sunny and warm in California today with temperatures around 75°F. Perfect weather for outdoor activities!",
        "colorado": "Colorado has clear skies with temperatures around 65°F. Great conditions for hiking in the mountains!",
        "new york": "New York is experiencing partly cloudy weather with temperatures around 70°F. A pleasant day in the city!",
        "texas": "Texas has hot and humid weather today with temperatures around 85°F. Stay hydrated!",
        "florida": "Florida is warm and sunny with temperatures around 80°F. Perfect beach weather!",
        "washington": "Washington has overcast skies with light rain and temperatures around 60°F. Typical Pacific Northwest weather!",
        "alaska": "Alaska is cold with temperatures around 35°F. Bundle up if you're heading outside!",
        "hawaii": "Hawaii has beautiful tropical weather with temperatures around 82°F. Paradise conditions!",
        "arizona": "Arizona is hot and dry with temperatures around 90°F. Very sunny with clear skies!",
        "maine": "Maine has cool weather with temperatures around 55°F. Perfect for enjoying the coastal views!"
    }
    
    # Check if we have specific weather data for the location
    for state, weather in weather_data.items():
        if state in location:
            return weather
    
    # Default response for unknown locations
    return f"The weather in {location.title()} is currently pleasant with moderate temperatures. For more accurate information, please check a local weather service."

if __name__=="__main__":
    mcp.run(transport="streamable-http")
