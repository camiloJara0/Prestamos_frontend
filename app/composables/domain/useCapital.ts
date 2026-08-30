import type { Capital } from '#shared/types/capital'
import type { MovimientoCapitalCreate } from '#shared/types/movimiento_capital'
import { getCapital, registrarMovimiento } from '~/services/api/capital'

export function useCapital() {
  const capital = ref<Capital | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetch() {
    loading.value = true
    error.value = null
    try {
      capital.value = await getCapital()
    } catch {
      error.value = 'No se pudo cargar el capital.'
    } finally {
      loading.value = false
    }
  }

  async function registrar(datos: MovimientoCapitalCreate) {
    const respuesta = await registrarMovimiento(datos)
    capital.value = { ...(capital.value ?? {}), id: respuesta.movimiento.id, monto_total: respuesta.capital_actual } as Capital
    return respuesta
  }

  return { capital, loading, error, fetch, registrar }
}
