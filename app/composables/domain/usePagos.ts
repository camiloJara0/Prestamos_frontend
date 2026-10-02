import type { Pago, PagoCreate } from '#shared/types/pago'
import { getPagos, createPago } from '~/services/api/pago'

export function usePagos() {
  const pagos = ref<Pago[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetch(params: { page?: number, limit?: number } = { page: 1, limit: 100 }) {
    loading.value = true
    error.value = null
    try {
      const respuesta = await getPagos(params)
      pagos.value = respuesta.items
    } catch {
      error.value = 'No se pudieron cargar los pagos.'
    } finally {
      loading.value = false
    }
  }

  async function crear(data: PagoCreate) {
    const pago = await createPago(data)
    await fetch()
    return pago
  }

  return { pagos, loading, error, fetch, crear }
}
