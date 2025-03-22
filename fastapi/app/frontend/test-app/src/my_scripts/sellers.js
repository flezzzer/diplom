import { useEffect, useState } from "react";
import axios from "axios";

const SellerDashboard = ({ sellerId }) => {
  const [products, setProducts] = useState([]);
  const [orders, setOrders] = useState([]);
  const [newProduct, setNewProduct] = useState({ name: "", price: "", description: "" });
  const [newOrderStatus, setNewOrderStatus] = useState("pending");
  const [error, setError] = useState("");

  // Fetch products for the seller
  useEffect(() => {
    fetchProducts();
    fetchOrders();
  }, [sellerId]);

  const fetchProducts = async () => {
    try {
      const response = await axios.get(`/sellers/${sellerId}/products`);
      setProducts(response.data);
    } catch (err) {
      setError("Failed to load products");
    }
  };

  const fetchOrders = async () => {
    try {
      const response = await axios.get(`/sellers/${sellerId}/orders`);
      setOrders(response.data);
    } catch (err) {
      setError("Failed to load orders");
    }
  };

  const createProduct = async () => {
    try {
      const token = localStorage.getItem("token");
      const response = await axios.post(
        `/sellers/${sellerId}/products`,
        newProduct,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setProducts([...products, response.data]);
      setNewProduct({ name: "", price: "", description: "" });
    } catch (err) {
      setError("Failed to add product");
    }
  };

  const updateProduct = async (productId) => {
    try {
      const token = localStorage.getItem("token");
      const updatedProduct = { ...newProduct }; // Example: Use the updated fields here
      const response = await axios.put(
        `/sellers/${sellerId}/products/${productId}`,
        updatedProduct,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setProducts(products.map(product => (product.id === productId ? response.data : product)));
      setNewProduct({ name: "", price: "", description: "" });
    } catch (err) {
      setError("Failed to update product");
    }
  };

  const deleteProduct = async (productId) => {
    try {
      const token = localStorage.getItem("token");
      await axios.delete(`/sellers/${sellerId}/products/${productId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setProducts(products.filter((product) => product.id !== productId));
    } catch (err) {
      setError("Failed to delete product");
    }
  };

  const updateOrderStatus = async (orderId) => {
    try {
      const token = localStorage.getItem("token");
      const response = await axios.put(
        `/sellers/${sellerId}/orders/${orderId}/status`,
        { status: newOrderStatus },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setOrders(orders.map((order) => (order.id === orderId ? response.data : order)));
    } catch (err) {
      setError("Failed to update order status");
    }
  };

  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold mb-4">Seller Dashboard</h2>
      {error && <p className="text-red-500">{error}</p>}

      {/* Product List */}
      <h3 className="text-lg mb-4">Products</h3>
      <ul>
        {products.map((product) => (
          <li key={product.id} className="flex justify-between p-2 border-b">
            <span>{product.name} - ${product.price}</span>
            <div className="space-x-2">
              <button
                onClick={() => updateProduct(product.id)}
                className="text-blue-500"
              >
                Edit
              </button>
              <button
                onClick={() => deleteProduct(product.id)}
                className="text-red-500"
              >
                Delete
              </button>
            </div>
          </li>
        ))}
      </ul>

      {/* Create New Product */}
      <div className="mt-4">
        <input
          type="text"
          value={newProduct.name}
          onChange={(e) => setNewProduct({ ...newProduct, name: e.target.value })}
          className="border p-2 rounded"
          placeholder="Product Name"
        />
        <input
          type="number"
          value={newProduct.price}
          onChange={(e) => setNewProduct({ ...newProduct, price: e.target.value })}
          className="border p-2 rounded ml-2"
          placeholder="Price"
        />
        <input
          type="text"
          value={newProduct.description}
          onChange={(e) => setNewProduct({ ...newProduct, description: e.target.value })}
          className="border p-2 rounded ml-2"
          placeholder="Description"
        />
        <button onClick={createProduct} className="ml-2 bg-black text-white p-2 rounded">
          Add Product
        </button>
      </div>

      {/* Orders List */}
      <h3 className="text-lg mb-4 mt-8">Orders</h3>
      <ul>
        {orders.map((order) => (
          <li key={order.id} className="flex justify-between p-2 border-b">
            <span>Order ID: {order.id} - Status: {order.status}</span>
            <div className="space-x-2">
              <select
                value={newOrderStatus}
                onChange={(e) => setNewOrderStatus(e.target.value)}
                className="p-2 rounded"
              >
                <option value="pending">Pending</option>
                <option value="completed">Completed</option>
                <option value="shipped">Shipped</option>
              </select>
              <button
                onClick={() => updateOrderStatus(order.id)}
                className="text-blue-500"
              >
                Update Status
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default SellerDashboard;
