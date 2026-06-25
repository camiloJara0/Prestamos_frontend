import { defineStore } from 'pinia'
import { login } from '~/services/api/login'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: '' as string | null
    }),

    actions: {
        async login(email: String, password: String) {
            await login(email, password)
        },

        setToken(token: string) {
            this.token = token

            if (process.client) {
                localStorage.setItem('token', token)
            }
        },

        loadToken() {
            if (process.client) {
                this.token = localStorage.getItem('token')
            }
        },

        logout() {
            this.token = null

            if (process.client) {
                localStorage.removeItem('token')
            }
        }
    }
})