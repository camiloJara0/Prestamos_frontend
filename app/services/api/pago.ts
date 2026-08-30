import type { Pago, PagoCreate } from '#shared/types/pago'

export interface GetPagosParams {
  skip?: number
  limit?: number
}

export const getPagos = async (params: GetPagosParams = {}) => {
  return useApi().apiGet<Pago[]>('/pagos', { query: { ...params } })
}

export const createPago = async (data: PagoCreate) => {
  return useApi().apiPost<Pago>('/pagos', data)
}
