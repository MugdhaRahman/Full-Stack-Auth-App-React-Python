# backend/main.py
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from models import LoginRequest
from database import users_db
from auth import create_access_token, verify_token

app = FastAPI()

# ===== CORS setup =====
origins = [
    "http://localhost:5173",  # Vite dev server
    # add other frontend URLs if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],   # allow GET, POST, OPTIONS, etc.
    allow_headers=["*"],   # allow all headers
)

# ===== Helper function to get current user from JWT =====
def get_current_user(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]  # Authorization: Bearer <token>
    except IndexError:
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=403, detail="Invalid or expired token")
    return payload

# ===== Login endpoint =====
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
