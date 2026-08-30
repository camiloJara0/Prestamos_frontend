import type { Pago, PagoCreate } from '#shared/types/pago'
import { getPagos, createPago } from '~/services/api/pago'

export function usePagos() {
  const pagos = ref<Pago[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetch(params: { skip?: number, limit?: number } = { skip: 0, limit: 100 }) {
    loading.value = true
    error.value = null
    try {
      pagos.value = await getPagos(params)
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
