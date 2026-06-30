import { defineStore } from 'pinia'
import { createPrestamo, getPrestamos } from '~/services/api/prestamos'
import type { Prestamo } from '~/types/prestamo'

export const usePrestamosStore = defineStore('prestamos', {
    state: () => ({
        prestamos: []
    }),

    actions: {
        async get() {
            this.prestamos = await getPrestamos()
        },

        async post(data: Prestamo) {
            await createPrestamo(data)
        }
    }
})