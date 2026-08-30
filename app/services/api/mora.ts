import type { Mora, MoraCreateUpdate, RespuestaProcesarMoras } from '#shared/types/mora'

export interface GetMorasParams {
  skip?: number
  limit?: number
}

export const getMoras = async (params: GetMorasParams = {}) => {
  return useApi().apiGet<Mora[]>('/moras', { query: { ...params } })
}

export const getMorasByPrestamo = async (prestamoId: number) => {
  return useApi().apiGet<Mora[]>(`/moras/prestamo/${prestamoId}`)
}

export const getMoraById = async (id: number) => {
  return useApi().apiGet<Mora>(`/moras/${id}`)
}

export const createMora = async (data: MoraCreateUpdate) => {
  return useApi().apiPost<Mora>('/moras', data)
}

export const updateMora = async (id: number, data: MoraCreateUpdate) => {
  return useApi().apiPut<Mora>(`/moras/${id}`, data)
}

export const deleteMora = async (id: number) => {
  return useApi().apiDelete<{ mensaje: string }>(`/moras/${id}`)
}

export const procesarMoras = async () => {
  return useApi().apiPost<RespuestaProcesarMoras>('/moras/procesar-moras', {})
}
