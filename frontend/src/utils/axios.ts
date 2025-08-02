import axios from "axios";
import { useAuthStore } from '@/stores/auth';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api'
});

api.interceptors.request.use((config) => {
  const auth = useAuthStore(); // <-- using Pinia directly
  const token = auth.accessToken;

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
export default api