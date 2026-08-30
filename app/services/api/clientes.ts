import type { Cliente, ClienteCreate } from '#shared/types/clientes'

export interface ListadoClientesParams {
  skip?: number
  limit?: number
}

export const getClientes = async (params: ListadoClientesParams = {}) => {
  return useApi().apiGet<Cliente[]>('/clientes', { query: { ...params } })
}

export const getClienteById = async (id: number) => {
  return useApi().apiGet<Cliente>(`/clientes/${id}`)
}

export const createCliente = async (data: ClienteCreate) => {
  return useApi().apiPost<Cliente>('/clientes', data)
}

export const updateCliente = async (id: number, data: ClienteCreate) => {
  return useApi().apiPut<Cliente>(`/clientes/${id}`, data)
}

export const deleteCliente = async (id: number) => {
  return useApi().apiDelete<{ mensaje: string }>(`/clientes/${id}`)
}
