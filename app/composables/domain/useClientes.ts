import type { Cliente, ClienteCreate } from '#shared/types/clientes'
import { createCliente, deleteCliente, getClientes, updateCliente } from '~/services/api/clientes'

export function useClientes() {
  const clientes = ref<Cliente[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetch() {
    loading.value = true
    error.value = null
    try {
      clientes.value = await getClientes({ skip: 0, limit: 1000 })
    } catch {
      error.value = 'No se pudieron cargar los clientes.'
    } finally {
      loading.value = false
    }
  }

  async function crear(data: ClienteCreate) {
    const cliente = await createCliente(data)
    await fetch()
    return cliente
  }

  async function actualizar(id: number, data: ClienteCreate) {
    const cliente = await updateCliente(id, data)
    await fetch()
    return cliente
  }

  async function eliminar(id: number) {
    await deleteCliente(id)
    await fetch()
  }

  return { clientes, loading, error, fetch, crear, actualizar, eliminar }
}
