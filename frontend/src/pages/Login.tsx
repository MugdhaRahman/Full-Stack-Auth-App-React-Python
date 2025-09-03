import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser } from "../api/auth";
import Logo from "../assets/react.svg";

export default function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        try {
            const data = await loginUser(email, password);
            localStorage.setItem("token", data.access_token);
            localStorage.setItem("role", data.role);
            navigate("/dashboard"); // redirect after login
        } catch (err: any) {
            setError(err.message);
        }
    };

    const handleGitHubLogin = () => {
        window.location.href = "http://localhost:8000/api/auth/github/login";
    };


    return (
        <div className="flex flex-col items-center justify-center bg-gray-900 px-6 py-8 mx-auto md:h-screen lg:py-0">
            <h1 className="flex items-center mb-6 text-2xl font-semibold text-gray-900 dark:text-white">
                <img className="w-8 h-8 mr-2"
                     src={Logo} alt={'logo'}/>
                Auth with React</h1>
            {error && <p className="text-red-500">{error}</p>}
            <form onSubmit={handleLogin} className="flex flex-col gap-4">
                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="border p-2 rounded"
                    required
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="border p-2 rounded"
                    required
                />
                <button type="submit" className="bg-blue-500 text-white p-2 rounded">
                    Login
                </button>
                <button onClick={handleGitHubLogin} className="bg-blue-900 text-white p-2 rounded">
                    Login with github
                </button>
            </form>
        </div>
    );
}
