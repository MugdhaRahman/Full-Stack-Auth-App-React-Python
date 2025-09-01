// src/api/auth.ts

const API_URL = "http://localhost:8000/api";

export const loginUser = async (email: string, password: string) => {
    const res = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
    });
    if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Login failed");
    }
    return res.json(); // returns { access_token, role }
};

export const fetchDashboard = async (token: string) => {
    const res = await fetch(`${API_URL}/dashboard`, {
        headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Unauthorized");
    }
    return res.json();
};
