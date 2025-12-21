import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export const jobAPI = {
  getJobs: (params) => api.get('/api/jobs', { params }),
  getJob: (id) => api.get(`/api/jobs/${id}`),
  deleteJob: (id) => api.delete(`/api/jobs/${id}`),
  exportExcel: (params) =>
    api.get('/api/jobs/export/excel', {
      params,
      responseType: 'blob'
    }),
};

export const favoriteAPI = {
  getFavorites: () => api.get('/api/favorites'),
  addFavorite: (data) => api.post('/api/favorites', data),
  updateFavorite: (id, data) => api.put(`/api/favorites/${id}`, data),
  deleteFavorite: (id) => api.delete(`/api/favorites/${id}`),
};

export const scraperAPI = {
  runScraper: (data) => api.post('/api/scraper/run', data),
  getStatus: () => api.get('/api/scraper/status'),
};

export default api;
