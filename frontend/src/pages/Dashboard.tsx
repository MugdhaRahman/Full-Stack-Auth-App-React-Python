import { useEffect, useState } from "react";
import { fetchDashboard } from "../api/auth";
import { useNavigate } from "react-router-dom";

export default function Dashboard() {
    const [message, setMessage] = useState("");
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem("token");
        if (!token) {
            navigate("/login");
            return;
        }

        fetchDashboard(token)
            .then((data) => setMessage(data.message))
            .catch((err) => {
                console.error(err);
                navigate("/login");
            });
    }, [navigate]);

    return (
        <div className="max-w-md mx-auto mt-20 p-6 border rounded shadow">
            <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
            <p>{message}</p>
        </div>
    );
}
