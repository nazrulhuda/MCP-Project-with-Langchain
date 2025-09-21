import subprocess
import time
import threading
import webbrowser
import os
from dotenv import load_dotenv

load_dotenv()

def start_weather_server():
    """Start the weather MCP server (HTTP on :8000)"""
    print("1. Starting weather MCP server...")
    try:
        subprocess.run(["python", "weather.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Weather server error: {e}")
    except FileNotFoundError:
        print("Python not found. Make sure Python is in your PATH.")

def start_sys_server():
    """Start the system metrics MCP server (stdio)"""
    print("2. Starting sys MCP server...")
    try:
        subprocess.run(["python", "sysserver.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Sys server error: {e}")
    except FileNotFoundError:
        print("Python not found. Make sure Python is in your PATH.")

def start_flask_app():
    """Start the Flask chatbot application"""
    print("3. Starting Flask chatbot application...")
    try:
        subprocess.run(["python", "app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Flask app error: {e}")
    except FileNotFoundError:
        print("Python not found. Make sure Python is in your PATH.")

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
