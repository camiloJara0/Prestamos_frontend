import type { Mora, MoraCreateUpdate, RespuestaProcesarMoras } from '#shared/types/mora'
import type { PaginacionParams, RespuestaPaginada } from '#shared/types/paginacion'

export const getMoras = async (params: PaginacionParams = {}) => {
  return useApi().apiGet<RespuestaPaginada<Mora>>('/mora', { query: { ...params } })
}

export const getMorasByPrestamo = async (prestamoId: number) => {
  return useApi().apiGet<Mora[]>(`/mora/prestamo/${prestamoId}`)
}

export const getMoraById = async (id: number) => {
  return useApi().apiGet<Mora>(`/mora/${id}`)
}

export const updateMora = async (id: number, data: MoraCreateUpdate) => {
  return useApi().apiPut<Mora>(`/mora/${id}`, data)
}

export const deleteMora = async (id: number) => {
  return useApi().apiDelete<{ mensaje: string }>(`/mora/${id}`)
}

export const procesarMoras = async () => {
  return useApi().apiPost<RespuestaProcesarMoras>('/mora/procesar-manual', {})
}
