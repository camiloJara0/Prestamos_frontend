// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: [
    '@nuxt/eslint',
    '@nuxt/ui',
    '@pinia/nuxt'
  ],
  typescript: {strict: true},
  devtools: {
    enabled: true
  },

  css: ['~/assets/css/main.css'],

  routeRules: {
    '/': { prerender: true }
  },

  compatibilityDate: '2025-01-15',
  runtimeConfig: {
    public: {
      SECRET_KEY: 'THESALUS943875PL',
      api: 'http://localhost:8000',
      login: 'auth/login',
      eps: 'api/v1/eps',
      professions: 'api/v1/professions',
      empresas: 'api/v1/empresas',
      users: 'api/v1/users',
    }
  },
  eslint: {
    config: {
      stylistic: {
        commaDangle: 'never',
        braceStyle: '1tbs'
      }
    }
  }
})
