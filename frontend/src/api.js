import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  register: (fullName, email, password) =>
    api.post("/auth/register", { full_name: fullName, email, password }),
  login: (email, password) =>
    api.post("/auth/login", { email, password }),
  me: () => api.get("/auth/me"),
};

export const dashboardAPI = {
  getSummary: () => api.get("/dashboard/summary"),
};

export const productsAPI = {
  list: () => api.get("/products"),
  create: (data) => api.post("/products", data),
  update: (id, data) => api.patch(`/products/${id}`, data),
  delete: (id) => api.delete(`/products/${id}`),
};

export const reportsAPI = {
  list: () => api.get("/reports"),
  upload: (productId, file) => {
    const formData = new FormData();
    formData.append("file", file);
    return api.post(`/reports/upload?product_id=${productId}`, formData);
  },
  getMetrics: (reportId) => api.get(`/reports/${reportId}/metrics`),
};

export const recommendationsAPI = {
  list: () => api.get("/recommendations"),
  updateStatus: (id, status) =>
    api.patch(`/recommendations/${id}`, { status }),
};

export const exportsAPI = {
  exportRecommendations: () =>
    api.get("/exports/recommendations.csv", { responseType: "blob" }),
};

export default api;