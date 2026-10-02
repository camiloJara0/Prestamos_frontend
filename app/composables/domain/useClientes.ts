import type { Cliente, ClienteCreate } from '#shared/types/clientes'
import { createCliente, deleteCliente, getClientes, updateCliente, type FiltrosClientes } from '~/services/api/clientes'

export function useClientes() {
  const clientes = ref<Cliente[]>([])
  const paginacion = ref<{ page: number, pages: number, total: number }>()
  const loading = ref(false)
  const error = ref<string | null>(null)
  let filtrosActuales: FiltrosClientes = {}

  async function fetch(params: FiltrosClientes = {}) {
    filtrosActuales = { page: 1, limit: 100, ...params }
    loading.value = true
    error.value = null
    try {
      const response = await getClientes(filtrosActuales)
      paginacion.value = {
        page: response.page,
        pages: response.pages,
        total: response.total
      }
      clientes.value = response.items
    } catch {
      error.value = 'No se pudieron cargar los clientes.'
    } finally {
      loading.value = false
    }
  }

  async function recargar() {
    await fetch(filtrosActuales)
  }

  async function crear(data: ClienteCreate) {
    const cliente = await createCliente(data)
    await recargar()
    return cliente
  }

  async function actualizar(id: number, data: ClienteCreate) {
    const cliente = await updateCliente(id, data)
    await recargar()
    return cliente
  }

  async function eliminar(id: number) {
    await deleteCliente(id)
    await recargar()
  }

  return { clientes, paginacion, loading, error, fetch, recargar, crear, actualizar, eliminar }
}
