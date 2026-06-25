import api from '~/services/api'
import type { Cliente } from '~/types/clientes'

// Obtener todos los clientes
export const getClientes = async () => {
  try {
    const response = await api.get('/clientes')
    return response.data
  } catch (error: any) {
    // Ya viene procesado por el interceptor
    throw error
  }
}

// Obtener cliente por ID
export const getClienteById = async (id: string) => {
  try {
    const response = await api.get(`/clientes/${id}`)
    return response.data
  } catch (error: any) {
    throw error
  }
}


// Crear cliente (POST)
export const createCliente = async (data: Cliente) => {
  try {
    const response = await api.post('/clientes', data)

    return response.data
  } catch (error: any) {
    // El error ya viene manejado desde api.ts
    throw error
  }
}
