import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from supabase import Client, create_client
from pydantic import BaseModel

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




# Stage 1

class AuthRequest(BaseModel):
    email: str | None=None
    password: str| None=None

@app.post("/auth/signup", status_code=201)
def signup(body: AuthRequest):
    if not body.email or not body.password:
        raise HTTPException(status_code=400, detail="email and password")

    try:
        result = supabase.auth.sign_up({
            "email": body.email,
            "password": body.password,
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return{"user":result.user}

@app.post("/auth/login")
def login(body: AuthRequest):
    if not body.email or not body.password:
        raise HTTPException(status_code=400, detail="email and password")

    try:
        result = supabase.auth.sign_in_with_password({
            "email": body.email,
            "password": body.password,
        })
    except Exception as e:
        raise HTTPException(status_code=401, detail="invalid login")
    return {"access_token": result.session.access_token,
        "refresh_token": result.session.refresh_token}

#Stage 2
@app.get("/public/info")
def public_info():
    return {"message": "Welcome stranger! This info is public."}

@app.get("/protected/profil")
def protected_profile(request: Request):
    auth_header=request._headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"error": "Access token required"})

    parts = auth_header.split(" ")
    token = parts[1] if len(parts) > 1 and parts[1] else None

    if not token:
        return JSONResponse(status_code=401, content={"error": "Access token required"})
    return {"message": "token received (not yet verified)", "token": token}

# Start the server
if __name__ == "__main__":
    print("Server running and connected to Supabase")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT
    )