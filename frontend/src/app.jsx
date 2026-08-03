import React from "react";
import { Routes, Route, Link } from "react-router-dom";
import { AuthProvider, useAuth } from "./authContext";
import Login from "./pages/Login";
import Register from "./pages/Register";
import ProtectedRoute from "./pages/ProtectedRoute";

function Dashboard() {
  const auth = useAuth();

  return (
    <div style={{ padding: 24 }}>
      <h1>Dashboard</h1>
      <p>Welcome, {auth.user?.full_name || "user"}.</p>
      <button onClick={auth.logout} style={{ marginTop: 16, padding: 10 }}>
        Logout
      </button>
    </div>
  );
}

function Home() {
  return (
    <div style={{ padding: 24 }}>
      <h1>PPCPilot</h1>
      <p>This is your front-end app. Please login or register to continue.</p>
      <Link to="/login" style={{ marginRight: 16 }}>
        Login
      </Link>
      <Link to="/register">Register</Link>
    </div>
  );
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  );
}

export default App;