import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
// import Products from "./pages/Products";
// import ProductDetail from "./pages/ProductDetail";
// import AddProduct from "./pages/AddProduct";
// import EditProduct from "./pages/EditProduct";
import Login from "./pages/Login";
import Register from "./pages/Register";

const App = () => (
  <Router>
    <Routes>
      {/*<Route path="/products" element={<Products />} />*/}
      {/*<Route path="/products/:id" element={<ProductDetail />} />*/}
      {/*<Route path="/add-product" element={<AddProduct />} />*/}
      {/*<Route path="/edit-product/:id" element={<EditProduct />} />*/}
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
    </Routes>
  </Router>
);

export default App;
