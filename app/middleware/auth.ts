export default defineNuxtRouteMiddleware(async () => {
  if (import.meta.server) return

  const auth = useAuthStore()
  const sesionValida = await auth.ensureSession()

  if (!sesionValida) {
    return navigateTo('/login')
  }
})
