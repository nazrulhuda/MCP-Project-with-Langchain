from mcp.server.fastmcp import FastMCP

mcp=FastMCP("Math")

@mcp.tool()
def add(a:int,b:int)->int:
    """_summary_
    Add to numbers
    """
    return a+b

@mcp.tool()
def multiple(a:int,b:int)-> int:
    """Multiply two numbers"""
    return a*b

#The transport="stdio" argument tells the server to:

#Use standard input/output (stdin and stdout) to receive and respond to tool function calls.

if __name__=="__main__":
    import os
    # Run as an HTTP (streamable) MCP server so clients can call it over HTTP.
    # Default to port 8002 to avoid conflicting with other servers.
    host = os.getenv("MATH_MCP_HOST", "0.0.0.0")
    port = int(os.getenv("MATH_MCP_PORT", "8002"))
    # The FastMCP.run() API does not accept host/port kwargs; set them
    # on the server settings before starting the streamable-http server.
    mcp.settings.host = host
    mcp.settings.port = port
    mcp.run(transport="streamable-http")