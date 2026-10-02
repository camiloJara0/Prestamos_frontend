import type { Capital } from '#shared/types/capital'
import type { MovimientoCapital, MovimientoCapitalCreate, ResumenCaja, RespuestaMovimientoCapital } from '#shared/types/movimiento_capital'
import type { RespuestaPaginada } from '#shared/types/paginacion'

export const getCapital = async () => {
  return useApi().apiGet<Capital>('/capital')
}

export const registrarMovimiento = async (data: MovimientoCapitalCreate) => {
  return useApi().apiPost<RespuestaMovimientoCapital>('/capital', data)
}

export const getMovimientosCapital = async (page = 1, limit = 50, filtros: { desde?: string, hasta?: string, tipo?: string } = {}) => {
  return useApi().apiGet<RespuestaPaginada<MovimientoCapital>>('/capital/movimientos', {
    query: { page, limit, ...filtros }
  })
}

export const getResumenCaja = async (filtros: { desde?: string, hasta?: string } = {}) => {
  return useApi().apiGet<ResumenCaja>('/capital/resumen-caja', { query: { ...filtros } })
}
