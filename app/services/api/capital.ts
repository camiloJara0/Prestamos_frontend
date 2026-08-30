import type { Capital } from '#shared/types/capital'
import type { MovimientoCapitalCreate, RespuestaMovimientoCapital } from '#shared/types/movimiento_capital'

export const getCapital = async () => {
  return useApi().apiGet<Capital>('/capital')
}

export const registrarMovimiento = async (data: MovimientoCapitalCreate) => {
  return useApi().apiPost<RespuestaMovimientoCapital>('/capital', data)
}
