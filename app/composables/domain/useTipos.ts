import type { TipoPago, TipoPagoCreate } from '#shared/types/tipo_pago'
import type { TipoPrestamo, TipoPrestamoCreate } from '#shared/types/tipo_prestamo'
import {
  createTipoPago,
  createTipoPrestamo,
  deleteTipoPago,
  deleteTipoPrestamo,
  getTiposPago,
  getTiposPrestamo,
  updateTipoPago,
  updateTipoPrestamo
} from '~/services/api/tipo'

export function useTiposPrestamo() {
  const tipos = ref<TipoPrestamo[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetch() {
    loading.value = true
    error.value = null
    try {
      tipos.value = await getTiposPrestamo({ skip: 0, limit: 1000 })
    } catch {
      error.value = 'No se pudieron cargar los tipos de préstamo.'
    } finally {
      loading.value = false
    }
  }

  async function crear(data: TipoPrestamoCreate) {
    const tipo = await createTipoPrestamo(data)
    await fetch()
    return tipo
  }

  async function actualizar(id: number, data: TipoPrestamoCreate) {
    const tipo = await updateTipoPrestamo(id, data)
    await fetch()
    return tipo
  }

  async function eliminar(id: number) {
    await deleteTipoPrestamo(id)
    await fetch()
  }

  return { tipos, loading, error, fetch, crear, actualizar, eliminar }
}

export function useTiposPago() {
  const tipos = ref<TipoPago[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetch() {
    loading.value = true
    error.value = null
    try {
      tipos.value = await getTiposPago({ skip: 0, limit: 1000 })
    } catch {
      error.value = 'No se pudieron cargar los tipos de pago.'
    } finally {
      loading.value = false
    }
  }

  async function crear(data: TipoPagoCreate) {
    const tipo = await createTipoPago(data)
    await fetch()
    return tipo
  }

  async function actualizar(id: number, data: TipoPagoCreate) {
    const tipo = await updateTipoPago(id, data)
    await fetch()
    return tipo
  }

  async function eliminar(id: number) {
    await deleteTipoPago(id)
    await fetch()
  }

  return { tipos, loading, error, fetch, crear, actualizar, eliminar }
}
