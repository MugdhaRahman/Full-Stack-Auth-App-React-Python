# React + FastAPI Authentication Starter

This is a simple full-stack authentication starter project built with **FastAPI (backend)** and **React + Vite (frontend)**.  
It demonstrates how to implement user login, JWT authentication, and protected routes.

---

## 🚀 Backend Setup (FastAPI)

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/react-auth-starter.git
cd react-auth-starter/backend
```

### 2. Create & Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows (PowerShell)
```

### 3. Install Dependencies
```bash
pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt] python-multipart
```

### 4. Run the Development Server
```bash
uvicorn main:app --reload --port 8000
```
Backend will be available at:
👉 http://localhost:8000

### 5. API Endpoints

POST /api/auth/login → Login with email & password

GET /api/dashboard → Protected route (requires Authorization: Bearer <token>)

GET /api/admin → Admin-only route



💻 Frontend Setup (React + Vite)

### 1. Navigate to Frontend
```bash
cd ../frontend
```
### 2. Install Dependencies
```bash
npm install
```
### 3. Start Development Server
```bash
npm run dev
```
Frontend will be available at:
👉 http://localhost:5173

🔑 Default Users

The backend uses an in-memory user database (database.py) for demo purposes.
```python
users_db = [
    {"id": 1, "email": "admin@test.com", "password": "123456", "role": "admin"},
    {"id": 2, "email": "user@test.com", "password": "123456", "role": "user"},
]
```

Admin login:
admin@test.com / 123456

User login:
user@test.com / 123456
