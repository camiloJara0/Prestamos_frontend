import type { Pago, PagoCreate, FiltrosHistorialPagos } from '#shared/types/pago'
import type { RespuestaPaginada } from '#shared/types/paginacion'

export const getPagos = async (params: FiltrosHistorialPagos = {}) => {
  return useApi().apiGet<RespuestaPaginada<Pago>>('/pagos', { query: { ...params } })
}

export const createPago = async (data: PagoCreate) => {
  return useApi().apiPost<Pago>('/pagos', data)
}

export const getPagoById = async (id: number) => {
  return useApi().apiGet<Pago>(`/pagos/${id}`)
}

export const devolverPago = async (id: number, motivo: string) => {
  return useApi().apiPost<Pago>(`/pagos/${id}/devolver`, { motivo_devolucion: motivo })
}

export const descargarComprobantePago = async (id: number) => {
  await useApi().apiDownload(`/pagos/${id}/comprobante`, `comprobante-pago-${id}.pdf`)
}
