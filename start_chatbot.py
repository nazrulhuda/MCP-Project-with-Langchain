import subprocess
import time
import threading
import webbrowser
import os
from dotenv import load_dotenv

load_dotenv()

def start_weather_server():
    """Start the weather MCP server"""
    print("1. Starting weather MCP server...")
    try:
        subprocess.run(["python", "weather.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Weather server error: {e}")
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
    
    # Start weather server in a separate thread
    weather_thread = threading.Thread(target=start_weather_server, daemon=True)
    weather_thread.start()
    
    # Wait a bit for the weather server to start
    print("2. Waiting for weather server to initialize...")
    time.sleep(3)
    
    # Start Flask app
    flask_thread = threading.Thread(target=start_flask_app, daemon=True)
    flask_thread.start()
    
    # Wait a bit for Flask to start
    time.sleep(3)
    
    # Open browser
    print("4. Opening browser...")
    try:
        webbrowser.open("http://localhost:5000")
    except:
        print("Could not open browser automatically. Please navigate to http://localhost:5000")
    
    print("\nChatbot system is running!")
    print("Weather server: http://localhost:8000")
    print("Flask app: http://localhost:5000")
    print("\nPress Ctrl+C to stop all services...")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")

if __name__ == "__main__":
    main()
