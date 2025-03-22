import { useEffect, useState } from "react";
import axios from "axios";

const Categories = () => {
  const [categories, setCategories] = useState([]);
  const [newCategory, setNewCategory] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    try {
      const response = await axios.get("/categories/");
      setCategories(response.data);
    } catch (err) {
      setError("Failed to load categories");
    }
  };

  const addCategory = async () => {
    try {
      const token = localStorage.getItem("token");
      const response = await axios.post(
        "/categories/",
        { name: newCategory },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setCategories([...categories, response.data]);
      setNewCategory("");
    } catch (err) {
      setError("Failed to add category");
    }
  };

  const deleteCategory = async (categoryId) => {
    try {
      const token = localStorage.getItem("token");
      await axios.delete(`/categories/${categoryId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setCategories(categories.filter((category) => category.id !== categoryId));
    } catch (err) {
      setError("Failed to delete category");
    }
  };

  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold mb-4">Categories</h2>
      {error && <p className="text-red-500">{error}</p>}
      <ul>
        {categories.map((category) => (
          <li key={category.id} className="flex justify-between p-2 border-b">
            <span>{category.name}</span>
            <button
              onClick={() => deleteCategory(category.id)}
              className="text-red-500"
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
      <div className="mt-4">
        <input
          type="text"
          value={newCategory}
          onChange={(e) => setNewCategory(e.target.value)}
          className="border p-2 rounded"
          placeholder="New category"
        />
        <button onClick={addCategory} className="ml-2 bg-black text-white p-2 rounded">
          Add
        </button>
      </div>
    </div>
  );
};

const Orders = () => {
  const [orders, setOrders] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      const token = localStorage.getItem("token");
      const response = await axios.get("/orders/", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setOrders(response.data);
    } catch (err) {
      setError("Failed to load orders");
    }
  };

  const deleteOrder = async (orderId) => {
    try {
      const token = localStorage.getItem("token");
      await axios.delete(`/orders/${orderId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setOrders(orders.filter((order) => order.id !== orderId));
    } catch (err) {
      setError("Failed to delete order");
    }
  };

  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold mb-4">Orders</h2>
      {error && <p className="text-red-500">{error}</p>}
      <ul>
        {orders.map((order) => (
          <li key={order.id} className="flex justify-between p-2 border-b">
            <span>Order ID: {order.id} - Status: {order.status}</span>
            <button
              onClick={() => deleteOrder(order.id)}
              className="text-red-500"
            >
              Cancel
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export { Categories, Orders };