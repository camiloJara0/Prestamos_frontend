import api from '~/services/api'
import type { Prestamo } from '~/types/prestamo'

// Obtener todos los prestamos
export const getPrestamos = async () => {
  try {
    const response = await api.get('/prestamos')
    return response.data
  } catch (error: any) {
    // Ya viene procesado por el interceptor
    throw error
  }
}

// Obtener Prestamo por ID
export const getPrestamoById = async (id: string) => {
  try {
    const response = await api.get(`/prestamos/${id}`)
    return response.data
  } catch (error: any) {
    throw error
  }
}


// Crear Prestamo (POST)
export const createPrestamo = async (data: Prestamo) => {
  try {
    const response = await api.post('/prestamos', data)

    return response.data
  } catch (error: any) {
    // El error ya viene manejado desde api.ts
    throw error
  }
}
