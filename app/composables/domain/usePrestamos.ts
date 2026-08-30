import type { Prestamo, PrestamoCreate, PrestamoDetalle, PrestamoFiltros, RenovacionCreate } from '#shared/types/prestamo'
import { createPrestamo, getPrestamoById, getPrestamos, marcarPrestamoPerdido, renovarPrestamo } from '~/services/api/prestamo'

export function usePrestamos() {
  const prestamos = ref<Prestamo[]>([])
  const detalle = ref<PrestamoDetalle | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const filtros = ref<PrestamoFiltros>({ estado: 'activo', skip: 0, limit: 50 })

  async function fetch(f = filtros.value) {
    loading.value = true
    error.value = null
    try {
      prestamos.value = await getPrestamos(f)
    } catch {
      error.value = 'No se pudieron cargar los préstamos.'
    } finally {
      loading.value = false
    }
  }

  async function byId(id: number) {
    loading.value = true
    error.value = null
    try {
      detalle.value = await getPrestamoById(id)
    } catch (e) {
      error.value = 'No se pudo cargar el préstamo.'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function crear(data: PrestamoCreate) {
    const prestamo = await createPrestamo(data)
    return prestamo
  }

  async function renovar(id: number, data: RenovacionCreate) {
    const prestamo = await renovarPrestamo(id, data)
    await byId(id)
    return prestamo
  }

  async function marcarPerdido(id: number, datos: { motivo?: string | null, fecha: string }) {
    const respuesta = await marcarPrestamoPerdido(id, datos)
    await byId(id)
    return respuesta
  }

  function setFiltros(f: PrestamoFiltros) {
    filtros.value = { ...filtros.value, ...f }
  }

  return { prestamos, detalle, loading, error, filtros, fetch, byId, crear, renovar, marcarPerdido, setFiltros }
}
