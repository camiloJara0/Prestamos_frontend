import type { Pago, PagoCreate, FiltrosHistorialPagos } from '#shared/types/pago'
import type { RespuestaPaginada } from '#shared/types/paginacion'

export const getPagos = async (params: FiltrosHistorialPagos = {}) => {
  return useApi().apiGet<RespuestaPaginada<Pago>>('/pagos', { query: { ...params } })
}

export const createPago = async (data: PagoCreate) => {
  return useApi().apiPost<Pago>('/pagos', data)
}
