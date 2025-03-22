import React, { useEffect, useState } from "react";
import axios from "axios";

// Функция для подключения к WebSocket
const connectToWebSocket = (sellerId, onMessage) => {
  const socket = new WebSocket(`ws://localhost:8000/api/v1/statistics/ws/${sellerId}`);

  socket.onmessage = (event) => {
    onMessage(event.data); // Когда получаем сообщение от сервера
  };

  socket.onclose = () => {
    console.log("Connection closed.");
  };

  return socket;
};

const SellerStatistics = ({ sellerId }) => {
  const [statistics, setStatistics] = useState(null);
  const [message, setMessage] = useState(null);
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    // Получаем статистику с API
    fetchStatistics();

    // Подключаемся к WebSocket серверу
    const wsSocket = connectToWebSocket(sellerId, handleWebSocketMessage);
    setSocket(wsSocket);

    // Очистка при размонтировании компонента
    return () => {
      if (wsSocket) {
        wsSocket.close();
      }
    };
  }, [sellerId]);

  // Получить статистику через API
  const fetchStatistics = async () => {
    try {
      const response = await axios.get(`/sellers/${sellerId}/statistics`);
      setStatistics(response.data);
    } catch (err) {
      console.error("Failed to fetch statistics", err);
    }
  };

  // Обработчик сообщений от WebSocket
  const handleWebSocketMessage = (message) => {
    setMessage(message); // Получаем сообщение от сервера
  };

  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold mb-4">Seller Statistics</h2>
      {message && <div className="text-green-500 mb-4">New notification: {message}</div>}

      {statistics ? (
        <div className="space-y-4">
          <div>
            <h3 className="font-semibold">Total Products</h3>
            <p>{statistics.total_products}</p>
          </div>
          <div>
            <h3 className="font-semibold">Total Orders</h3>
            <p>{statistics.total_orders}</p>
          </div>
          <div>
            <h3 className="font-semibold">Total Revenue</h3>
            <p>${statistics.total_revenue}</p>
          </div>
          <div>
            <h3 className="font-semibold">Order Status Counts</h3>
            <ul>
              {Object.entries(statistics.order_status_counts).map(([status, count]) => (
                <li key={status}>
                  {status}: {count}
                </li>
              ))}
            </ul>
          </div>
        </div>
      ) : (
        <p>Loading statistics...</p>
      )}
    </div>
  );
};

export default SellerStatistics;
