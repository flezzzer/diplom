import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { registerUser } from "../my_scripts/auth";

const Register = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [username, setUsername] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      await registerUser({ email, password, username});
      navigate("/login"); // После регистрации перенаправляем на страницу логина
    } catch (err) {
      setError("Ошибка регистрации. Возможно, email уже используется.");
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="bg-white p-6 rounded-lg shadow-lg w-96">
        <h2 className="text-xl font-semibold mb-4">Регистрация</h2>
        {error && <p className="text-red-500 text-sm">{error}</p>}
        <form onSubmit={handleRegister}>
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
           <input
            type="username"
            placeholder="Юзернейм"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="w-full p-2 border rounded mb-2"
          />
          <button className="w-full bg-blue-500 text-white p-2 rounded">Зарегистрироваться</button>
        </form>
        <p className="text-sm mt-2">
          Уже есть аккаунт? <a href="/login" className="text-blue-500">Войти</a>
        </p>
      </div>
    </div>
  );
};

export default Register;
