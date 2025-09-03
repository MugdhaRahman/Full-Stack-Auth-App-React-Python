# backend/main.py
import os
from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth

from models import LoginRequest
from database import users_db
from auth import create_access_token, verify_token

load_dotenv()

app = FastAPI()

# ===== SessionMiddleware =====
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET", "super-secret-key")
)

# ===== CORS setup =====
origins = ["http://localhost:5173"]  # Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== Helper function to get current user from JWT =====
def get_current_user(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]  # Bearer <token>
    except IndexError:
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=403, detail="Invalid or expired token")
    return payload

# ===== Local login endpoint =====
@app.post("/api/auth/login")
def login(data: LoginRequest):
    user = next(
        (u for u in users_db if u["email"] == data.email and u["password"] == data.password),
        None
    )
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({
        "id": user["id"],
        "email": user["email"],
        "role": user["role"]
    })
    return {"access_token": token, "role": user["role"]}

# ===== GitHub OAuth setup =====
oauth = OAuth()
oauth.register(
    name="github",
    client_id=os.getenv("GITHUB_CLIENT_ID"),
    client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
    authorize_url="https://github.com/login/oauth/authorize",
    access_token_url="https://github.com/login/oauth/access_token",
    api_base_url="https://api.github.com/",
    client_kwargs={"scope": "user:email"},
)

# ===== GitHub login route =====
@app.get("/api/auth/github/login")
async def github_login(request: Request):
    redirect_uri = request.url_for("github_callback")
    return await oauth.github.authorize_redirect(request, redirect_uri)

# ===== GitHub callback route =====
@app.get("/api/auth/github/callback")
async def github_callback(request: Request):
    try:
        token = await oauth.github.authorize_access_token(request)
        user_data = await oauth.github.get("user", token=token)
        user = user_data.json()
        print("GitHub user response:", user)

        # Create JWT token for frontend
        jwt_token = create_access_token({
            "id": user["id"],
            "email": user.get("email") or f"{user['login']}@github.com",
            "role": "user"
        })

        frontend_url = f"http://localhost:5173/dashboard?token={jwt_token}"
        return RedirectResponse(url=frontend_url)

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# ===== Protected route =====
@app.get("/api/dashboard")
def dashboard(user=Depends(get_current_user)):
    return {"message": f"Hello {user['email']}! Role: {user['role']}"}

# ===== Admin-only route =====
@app.get("/api/admin")
def admin_panel(user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return {"message": "Welcome Admin!"}
