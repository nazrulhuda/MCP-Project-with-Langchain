import subprocess
import time
import threading
import webbrowser
import os
from dotenv import load_dotenv
import sys

load_dotenv()

def start_weather_server():
    """Start the weather MCP server (HTTP on :8000)"""
    print("1. Starting weather MCP server...")
    try:
        # Use the same Python interpreter that's running this script
        env = os.environ.copy()
        env.setdefault("WEATHER_MCP_PORT", os.getenv("WEATHER_MCP_PORT", "8000"))
        env.setdefault("WEATHER_MCP_URL", f"http://localhost:{env.get('WEATHER_MCP_PORT')}/mcp")
        subprocess.Popen([sys.executable, "weather.py"], env=env)
    except FileNotFoundError:
        print("Python not found. Make sure Python is in your PATH.")
    except Exception as e:
        print(f"Weather server error: {e}")

def start_sys_server():
    """Start the system metrics MCP server (stdio)"""
    print("2. Starting sys MCP server...")
    try:
        # Launch sysserver in HTTP mode; pass SYS_MCP_PORT via env so it binds correctly.
        env = os.environ.copy()
        env.setdefault("SYS_MCP_PORT", os.getenv("SYS_MCP_PORT", "8001"))
        env.setdefault("SYS_MCP_URL", f"http://localhost:{env.get('SYS_MCP_PORT')}/mcp")
        subprocess.Popen([sys.executable, "sysserver.py"], env=env)
    except FileNotFoundError:
        print("Python not found. Make sure Python is in your PATH.")
    except Exception as e:
        print(f"Sys server error: {e}")

def start_flask_app():
    """Start the Flask chatbot application"""
    print("3. Starting Flask chatbot application...")
    try:
        env = os.environ.copy()
        env.setdefault("FLASK_PORT", os.getenv("FLASK_PORT", "5001"))
        # Ensure app sees the service URLs
        env.setdefault("SYS_MCP_URL", os.getenv("SYS_MCP_URL", f"http://localhost:{os.getenv('SYS_MCP_PORT', '8001')}/mcp"))
        env.setdefault("WEATHER_MCP_URL", os.getenv("WEATHER_MCP_URL", f"http://localhost:{os.getenv('WEATHER_MCP_PORT', '8000')}/mcp"))
        subprocess.Popen([sys.executable, "app.py"], env=env)
    except FileNotFoundError:
        print("Python not found. Make sure Python is in your PATH.")
    except Exception as e:
        print(f"Flask app error: {e}")

def main():
    print("Starting MCP Chatbot System...")
    
    # Check if GROQ_API_KEY is set
    if not os.getenv("GROQ_API_KEY"):
        print("Warning: GROQ_API_KEY environment variable not set!")
        print("Please create a .env file with your Groq API key:")
        print("GROQ_API_KEY=your_api_key_here")
        print()
    
    # Start weather server (HTTP) in a separate thread
    weather_thread = threading.Thread(target=start_weather_server, daemon=True)
    weather_thread.start()
    
    # Wait a bit for the weather server to start
    print("2. Waiting for weather server to initialize...")
    time.sleep(3)

    # Start sys server in a separate thread (stdio)
    sys_thread = threading.Thread(target=start_sys_server, daemon=True)
    sys_thread.start()
    
    # Wait a bit for the sys server to start
    print("3. Waiting for sys server to initialize...")
    time.sleep(5)
    
    # Start Flask app
    print("4. Starting Flask chatbot application...")
    flask_thread = threading.Thread(target=start_flask_app, daemon=True)
    flask_thread.start()
    
    # Wait a bit for Flask to start
    time.sleep(3)
    
    # Open browser
    print("5. Opening browser...")
    try:
        webbrowser.open("http://localhost:5001")
    except:
        print("Could not open browser automatically. Please navigate to http://localhost:5001")
    
    print("\nChatbot system is running!")
    print("Weather server: http://localhost:8000")
    print("Flask app: http://localhost:5001")
    print("\nPress Ctrl+C to stop all services...")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")

if __name__ == "__main__":
    main()
