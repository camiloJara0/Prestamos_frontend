import type { Prestamo, PrestamoCreate, PrestamoDetalle, PrestamoFiltros, RenovacionCreate, RespuestaMarcarPerdido } from '#shared/types/prestamo'

export const getPrestamos = async (filtros: PrestamoFiltros = {}) => {
  return useApi().apiGet<Prestamo[]>('/prestamos', { query: filtros })
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
