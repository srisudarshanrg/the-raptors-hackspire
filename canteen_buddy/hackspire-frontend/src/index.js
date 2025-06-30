import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import HomePage from './pages/HomePage';
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import StudentLoginPage from './pages/StudentLogin';
import StudentRegisterPage from './pages/StudentRegister';
import StudentLogoutPage from './pages/StudentLogout';
import PlaceOrderPage from './pages/PlaceOrder';
import MenuPage from './pages/Menu';
import AdminLoginPage from './pages/AdminLogin';
import AdminLogoutPage from './pages/AdminLogout';
import ViewOrdersPage from './pages/ViewOrders';
import UpdateMenuPage from './pages/UpdateMenu';

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [      
      {index: true, element: <HomePage />},
      {path: "/student-login", element: <StudentLoginPage />},
      {path: "/student-register", element: <StudentRegisterPage />},
      {path: "/student-logout", element: <StudentLogoutPage />},
      {path: "/place-order", element: <PlaceOrderPage />},
      {path: "/menu", element: <MenuPage />},
      {path: "/admin-login", element: <AdminLoginPage />},
      {path: "/admin-logout", element: <AdminLogoutPage />},
      {path: "/view-orders", element: <ViewOrdersPage />},
      {path: "/update-menu", element: <UpdateMenuPage />},
    ]
  }
])

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
