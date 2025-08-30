import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Get Groq API key from environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("Warning: GROQ_API_KEY not found in environment variables.")
    print("Please set your Groq API key using one of these methods:")
    print("1. Create a .env file with: GROQ_API_KEY=your_key_here")
    print("2. Set environment variable: set GROQ_API_KEY=your_key_here")
    print("3. Set it directly in this file (not recommended for production)")
