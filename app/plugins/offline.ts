import { useSyncStore } from '~/stores/sync'

export default defineNuxtPlugin(() => {
  if (typeof window === 'undefined') return

  const syncStore = useSyncStore()

  function updateOnlineStatus() {
    const wasOnline = syncStore.isOnline
    syncStore.setOnline(navigator.onLine)

    if (wasOnline && !navigator.onLine) {
      const toast = useToast()
      toast.add({ title: 'Sin conexión', color: 'warning', icon: 'i-lucide-wifi-off' })
    } else if (!wasOnline && navigator.onLine) {
      const toast = useToast()
      toast.add({ title: 'Conexión restablecida', color: 'success', icon: 'i-lucide-wifi' })
    }
  }

  window.addEventListener('online', updateOnlineStatus)
  window.addEventListener('offline', updateOnlineStatus)
  syncStore.setOnline(navigator.onLine)
})
