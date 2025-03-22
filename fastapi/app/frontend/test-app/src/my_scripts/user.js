import React, { useEffect, useState } from "react";
import axios from "axios";

const UserProfile = () => {
  const [user, setUser] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Получаем информацию о текущем пользователе при монтировании компонента
    fetchUserProfile();
  }, []);

  // Функция для получения данных о пользователе
  const fetchUserProfile = async () => {
    try {
      const token = localStorage.getItem("token"); // Получаем токен из localStorage
      const response = await axios.get("/users/me", {
        headers: {
          Authorization: `Bearer ${token}`, // Передаем токен в заголовках
        },
      });
      setUser(response.data);
    } catch (err) {
      setError("Failed to fetch user data");
      console.error(err);
    }
  };

  if (error) {
    return <div className="text-red-500">{error}</div>;
  }

  if (!user) {
    return <div>Loading...</div>;
  }

  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold mb-4">User Profile</h2>
      <div className="space-y-4">
        <div>
          <h3 className="font-semibold">Name</h3>
          <p>{user.name}</p>
        </div>
        <div>
          <h3 className="font-semibold">Email</h3>
          <p>{user.email}</p>
        </div>
        <div>
          <h3 className="font-semibold">Joined</h3>
          <p>{new Date(user.created_at).toLocaleDateString()}</p>
        </div>
      </div>
    </div>
  );
};

export default UserProfile;
