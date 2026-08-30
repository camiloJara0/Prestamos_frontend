import { defineStore } from 'pinia'
import { getClientes } from '~/services/api/clientes'
import type { Cliente } from '#shared/types/clientes'

export const useClienteStore = defineStore('clientes', {
  state: () => ({
    clientes: [] as Cliente[]
  }),

  actions: {
    async get() {
      this.clientes = await getClientes()
    }
  }
})
