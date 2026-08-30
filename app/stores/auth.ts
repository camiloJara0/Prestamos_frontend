import { defineStore } from 'pinia'
import type { UsuarioMe } from '#shared/types/usuario'
import { loginRequest, logoutRequest, meRequest, refreshRequest } from '~/services/api/auth'

export type AuthStatus = 'idle' | 'loading' | 'authenticated' | 'unauthenticated'

const ACCESS_KEY = 'loansoft:access'
const REFRESH_KEY = 'loansoft:refresh'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: null as string | null,
    refreshToken: null as string | null,
    user: null as UsuarioMe | null,
    status: 'idle' as AuthStatus
  }),

  getters: {
    isAuthenticated: (state): boolean => !!state.accessToken,
    isAdmin: (state): boolean => state.user?.rol === 'admin',
    hasAccess: state => (rolRequerido: string): boolean => {
      if (rolRequerido === 'admin') return state.user?.rol === 'admin'
      return !!state.user
    }
  },

  actions: {
    persistTokens() {
      if (!import.meta.client) return
      localStorage.setItem(ACCESS_KEY, this.accessToken ?? '')
      localStorage.setItem(REFRESH_KEY, this.refreshToken ?? '')
    },

    hydrate() {
      if (!import.meta.client) return
      const access = localStorage.getItem(ACCESS_KEY)
      const refresh = localStorage.getItem(REFRESH_KEY)
      if (access && refresh) {
        this.accessToken = access
        this.refreshToken = refresh
        this.status = 'loading'
        this.fetchMe().catch(() => this.logout())
      } else {
        this.status = 'unauthenticated'
      }
    },

    async login(email: string, password: string) {
      this.status = 'loading'
      try {
        const res = await loginRequest({ email, password })
        this.accessToken = res.access_token
        this.refreshToken = res.refresh_token
        this.persistTokens()
        await this.fetchMe()
      } catch (error) {
        this.status = 'unauthenticated'
        throw error
      }
    },

    async fetchMe(): Promise<UsuarioMe> {
      const user = await meRequest()
      this.user = user
      this.status = 'authenticated'
      return user
    },

    async refresh(): Promise<string | null> {
      if (!this.refreshToken) {
        await this.logout()
        return null
      }
      try {
        const res = await refreshRequest(this.refreshToken)
        this.accessToken = res.access_token
        this.persistTokens()
        return this.accessToken
      } catch {
        await this.logout()
        return null
      }
    },

    async logout() {
      if (import.meta.client) {
        try {
          if (this.accessToken) await logoutRequest()
        } catch {
          // best-effort: el logout remoto puede fallar sin red
        }
        localStorage.removeItem(ACCESS_KEY)
        localStorage.removeItem(REFRESH_KEY)
      }
      this.accessToken = null
      this.refreshToken = null
      this.user = null
      this.status = 'unauthenticated'
    }
  }
})
