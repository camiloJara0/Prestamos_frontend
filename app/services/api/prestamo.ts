import type { Prestamo, PrestamoCreate, PrestamoDetalle, PrestamoFiltros, RenovacionCreate, ReestructuracionCreate, ReestructuracionOut, RespuestaMarcarPerdido } from '#shared/types/prestamo'
import type { RespuestaPaginada } from '#shared/types/paginacion'

export const getPrestamos = async (filtros: PrestamoFiltros = {}): Promise<RespuestaPaginada<Prestamo>> => {
  return useApi().apiGet<RespuestaPaginada<Prestamo>>('/prestamos', { query: filtros })
}

export const getPrestamoById = async (id: number) => {
  return useApi().apiGet<PrestamoDetalle>(`/prestamos/${id}`)
}

export const createPrestamo = async (data: PrestamoCreate) => {
  return useApi().apiPost<Prestamo>('/prestamos', data)
}

export const renovarPrestamo = async (id: number, data: RenovacionCreate) => {
  return useApi().apiPost<Prestamo>(`/prestamos/${id}/renovar`, data)
}

export const marcarPrestamoPerdido = async (id: number, data: { motivo?: string | null, fecha: string }) => {
  return useApi().apiPost<RespuestaMarcarPerdido>(`/prestamos/${id}/marcar_perdido`, data)
}

export const ajustarCapitalPrestamo = async (id: number, nuevoCapital: number) => {
  return useApi().apiPut<{ mensaje: string, prestamo_id: number, capital_nuevo: number, monto_total: number, valor_cuota: number }>(
    `/prestamos/${id}/ajustar-capital`,
    undefined,
    { query: { nuevo_capital: nuevoCapital } }
  )
}

export const reestructurarPrestamo = async (id: number, data: ReestructuracionCreate) => {
  return useApi().apiPost<ReestructuracionOut>(`/prestamos/${id}/reestructurar`, data)
}
