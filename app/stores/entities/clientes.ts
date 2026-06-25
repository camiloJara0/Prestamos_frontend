import { defineStore } from 'pinia'
import { getClientes } from '~/services/api/clientes'

export const useClienteStore = defineStore('clientes', {
    state: () => ({
        clientes: []
    }),

    actions: {
        async get() {
            this.clientes = await getClientes()
        },


    }
})