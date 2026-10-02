import type { Usuario } from '#shared/types/usuario'
import type { RespuestaPaginada } from '#shared/types/paginacion'

export interface UsuarioCreate {
  nombre: string
  email: string
  rol: 'admin' | 'usuario'
  password: string
}

export interface UsuarioUpdate {
  nombre?: string
  email?: string
  rol?: 'admin' | 'usuario'
  password?: string
  estado?: 'activo' | 'inactivo'
}

export const getUsuarios = async (page = 1, limit = 10) => {
  return useApi().apiGet<RespuestaPaginada<Usuario>>('/usuarios', { query: { page, limit } })
}

export const getUsuarioById = async (id: number) => {
  return useApi().apiGet<Usuario>(`/usuarios/${id}`)
}

export const createUsuario = async (data: UsuarioCreate) => {
  return useApi().apiPost<Usuario>('/usuarios', data)
}

export const updateUsuario = async (id: number, data: UsuarioUpdate) => {
  return useApi().apiPut<Usuario>(`/usuarios/${id}`, data)
}

export const deleteUsuario = async (id: number) => {
  return useApi().apiDelete<{ message: string }>(`/usuarios/${id}`)
}
