import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import HomePage from './pages/HomePage';
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import StudentLoginPage from './pages/StudentLogin';
import StudentRegisterPage from './pages/StudentRegister';
import StudentLogoutPage from './pages/StudentLogout';
import AdminLoginPage from './pages/AdminLogin';
import AdminLogoutPage from './pages/AdminLogout';
import ViewOrdersPage from './pages/ViewOrders';
import UpdateMenuPage from './pages/UpdateMenu';
import CanteenStudent from './pages/CanteenStudent';

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [      
      {index: true, element: <HomePage />},
      {path: "/student-login", element: <StudentLoginPage />},
      {path: "/student-register", element: <StudentRegisterPage />},
      {path: "/student-logout", element: <StudentLogoutPage />},
      {path: "/canteen/student", element: <CanteenStudent />},
      {path: "/admin-login", element: <AdminLoginPage />},
      {path: "/admin-logout", element: <AdminLogoutPage />},
      {path: "/canteen/admin/view-orders", element: <ViewOrdersPage />},
      {path: "/canteen/admin/update-menu", element: <UpdateMenuPage />},
    ]
  }
])

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
