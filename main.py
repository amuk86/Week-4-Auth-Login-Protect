import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from supabase import Client, create_client

# Load variables from .env
load_dotenv()

# Get Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Get server port
PORT = int(os.getenv("PORT", "8000"))

# Make sure the credentials exist
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "SUPABASE_URL and SUPABASE_KEY must be set in your .env file"
    )

# Initialize Supabase client
supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# Create FastAPI application
app = FastAPI()


# Home route
@app.get("/")
def root():
    return {
        "message": "Server running and connected to Supabase"
    }


# Start the server
if __name__ == "__main__":
    print("Server running and connected to Supabase")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT
    )

