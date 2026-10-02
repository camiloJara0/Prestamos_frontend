import type { Pago, PagoCreate, FiltrosHistorialPagos } from '#shared/types/pago'
import type { RespuestaPaginada } from '#shared/types/paginacion'
import { getPagos, createPago } from '~/services/api/pago'

export function usePagos() {
  const pagos = ref<Pago[]>([])
  const paginacion = ref<{ page: number, pages: number, total: number }>()
  const loading = ref(false)
  const error = ref<string | null>(null)
  let filtrosActuales: FiltrosHistorialPagos = {}

  async function fetch(params: FiltrosHistorialPagos = {}) {
    filtrosActuales = { page: 1, limit: 50, ...params }
    loading.value = true
    error.value = null
    try {
      const respuesta: RespuestaPaginada<Pago> = await getPagos(filtrosActuales)
      pagos.value = respuesta.items
      paginacion.value = {
        page: respuesta.page,
        pages: respuesta.pages,
        total: respuesta.total
      }
    } catch {
      error.value = 'No se pudieron cargar los pagos.'
    } finally {
      loading.value = false
    }
  }

  async function cambiarPagina(page: number) {
    await fetch({ ...filtrosActuales, page })
  }

  async function recargar() {
    await fetch(filtrosActuales)
  }

  async function crear(data: PagoCreate) {
    const pago = await createPago(data)
    await recargar()
    return pago
  }

  return { pagos, paginacion, loading, error, fetch, cambiarPagina, recargar, crear }
}
