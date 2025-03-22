import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser } from "../my_scripts/auth";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await loginUser({ email, password });
      localStorage.setItem("token", response.access_token);
      navigate("/");
    } catch (err) {
      setError("Неверный email или пароль");
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="bg-white p-6 rounded-lg shadow-lg w-96">
        <h2 className="text-xl font-semibold mb-4">Вход</h2>
        {error && <p className="text-red-500 text-sm">{error}</p>}
        <form onSubmit={handleLogin}>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full p-2 border rounded mb-2"
          />
          <input
            type="password"
            placeholder="Пароль"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full p-2 border rounded mb-2"
          />
          <button className="w-full bg-black text-white p-2 rounded">Войти</button>
        </form>
        <p className="text-sm mt-2">
          Нет аккаунта? <a href="/register" className="text-blue-500">Зарегистрироваться</a>
        </p>
      </div>
    </div>
  );
};

export default Login;
