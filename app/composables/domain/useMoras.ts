import type { Mora, MoraCreateUpdate } from '#shared/types/mora'
import { getMoras, getMorasByPrestamo, updateMora, deleteMora, procesarMoras } from '~/services/api/mora'

export function useMoras() {
  const moras = ref<Mora[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetch(params: { skip?: number, limit?: number } = { skip: 0, limit: 100 }) {
    loading.value = true
    error.value = null
    try {
      moras.value = await getMoras(params)
    } catch {
      error.value = 'No se pudieron cargar las moras.'
    } finally {
      loading.value = false
    }
  }

  async function fetchByPrestamo(prestamoId: number) {
    loading.value = true
    error.value = null
    try {
      moras.value = await getMorasByPrestamo(prestamoId)
    } catch {
      error.value = 'No se pudieron cargar las moras del préstamo.'
    } finally {
      loading.value = false
    }
  }

  async function actualizar(id: number, data: MoraCreateUpdate) {
    const mora = await updateMora(id, data)
    await fetch()
    return mora
  }

  async function eliminar(id: number) {
    await deleteMora(id)
    await fetch()
  }

  async function procesar() {
    const resultado = await procesarMoras()
    await fetch()
    return resultado
  }

  return { moras, loading, error, fetch, fetchByPrestamo, actualizar, eliminar, procesar }
}
