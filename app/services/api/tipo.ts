import type { TipoPrestamo, TipoPrestamoCreate } from '#shared/types/tipo_prestamo'
import type { TipoPago, TipoPagoCreate } from '#shared/types/tipo_pago'
import type { PaginacionParams } from '#shared/types/paginacion'

export const getTiposPrestamo = async (params: PaginacionParams = {}) => {
  return useApi().apiGet<TipoPrestamo[]>('/tipo_prestamo', { query: params })
}

export const getTipoPrestamoById = async (id: number) => {
  return useApi().apiGet<TipoPrestamo>(`/tipo_prestamo/${id}`)
}

export const createTipoPrestamo = async (data: TipoPrestamoCreate) => {
  return useApi().apiPost<TipoPrestamo>('/tipo_prestamo', data)
}

export const updateTipoPrestamo = async (id: number, data: TipoPrestamoCreate) => {
  return useApi().apiPut<TipoPrestamo>(`/tipo_prestamo/${id}`, data)
}

export const deleteTipoPrestamo = async (id: number) => {
  return useApi().apiDelete<{ mensaje: string }>(`/tipo_prestamo/${id}`)
}

export const getTiposPago = async (params: PaginacionParams = {}) => {
  return useApi().apiGet<TipoPago[]>('/tipo_pago', { query: params })
}

export const getTipoPagoById = async (id: number) => {
  return useApi().apiGet<TipoPago>(`/tipo_pago/${id}`)
}

export const createTipoPago = async (data: TipoPagoCreate) => {
  return useApi().apiPost<TipoPago>('/tipo_pago', data)
}

export const updateTipoPago = async (id: number, data: TipoPagoCreate) => {
  return useApi().apiPut<TipoPago>(`/tipo_pago/${id}`, data)
}

export const deleteTipoPago = async (id: number) => {
  return useApi().apiDelete<{ mensaje: string }>(`/tipo_pago/${id}`)
}
