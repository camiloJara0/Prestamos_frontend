import { defineStore } from 'pinia'
import { getClientes } from '~/services/api/clientes'
import type { Cliente } from '#shared/types/clientes'

export const useClienteStore = defineStore('clientes', {
  state: () => ({
    clientes: [] as Cliente[],
    total: 0
  }),

  actions: {
    async get() {
      const response = await getClientes()
      this.clientes = response.items
      this.total = response.total
    }
  }
})
