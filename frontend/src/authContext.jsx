import React, { createContext, useContext, useEffect, useState } from "react";
import { authAPI } from "./api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(
    () => localStorage.getItem("token") || null
  );
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!token) {
      setLoading(false);
      return;
    }

    authAPI
      .me()
      .then((response) => {
        setUser(response.data);
      })
      .catch(() => {
        setToken(null);
        localStorage.removeItem("token");
      })
      .finally(() => {
        setLoading(false);
      });
  }, [token]);

  const login = async (email, password) => {
    const response = await authAPI.login(email, password);
    const accessToken = response.data.access_token;
    localStorage.setItem("token", accessToken);
    setToken(accessToken);
    setUser(response.data.user);
    return response.data.user;
  };

  const register = async (fullName, email, password) => {
    const response = await authAPI.register(fullName, email, password);
    const accessToken = response.data.access_token;
    localStorage.setItem("token", accessToken);
    setToken(accessToken);
    setUser(response.data.user);
    return response.data.user;
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{ user, token, loading, login, register, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}