
import axios from 'axios'

// Crear instancia personalizada
const api = axios.create({
  baseURL: 'http://localhost:8000', // 🔁 cambia esto
  timeout: 10000, // 10 segundos
  headers: {
    'Content-Type': 'application/json'
  }
})

// REQUEST interceptor (JWT)
api.interceptors.request.use(
  (config) => {
    // Obtener token (puedes cambiar a cookies si usas otra estrategia)
    const token = localStorage.getItem('token')

    // Si existe, agregarlo al header
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// RESPONSE interceptor (errores globales)
api.interceptors.response.use(
  (response) => response, // Respuestas correctas
  (error) => {
    const status = error.response?.status

    // Manejo específico
    if (status === 401) {
      console.error('No autorizado. Redirigiendo al login...')

      // Eliminar datos de sesión
      localStorage.removeItem('token')

      // Redirección (en Nuxt)
      window.location.href = '/'
    } else {
      console.error('Error en la API:', error.response?.data || error.message)
    }

    // Retornar error estructurado
    return Promise.reject({
      status,
      message: error.response?.data?.message || 'Error inesperado'
    })
  }
)

export default api

