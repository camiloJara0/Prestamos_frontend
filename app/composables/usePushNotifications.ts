export function usePushNotifications() {
  const isSupported = ref(false)
  const isSubscribed = ref(false)
  const loading = ref(false)

  function checkSupport() {
    if (!import.meta.client) return
    isSupported.value = 'serviceWorker' in navigator && 'PushManager' in window
  }

  async function actualizarEstado() {
    if (!import.meta.client || !isSupported.value) {
      isSubscribed.value = false
      return
    }
    try {
      const registration = await navigator.serviceWorker.ready
      const subscription = await registration.pushManager.getSubscription()
      isSubscribed.value = subscription !== null
    } catch {
      isSubscribed.value = false
    }
  }

  async function suscribir() {
    if (!isSupported.value) return
    loading.value = true
    try {
      const registration = await navigator.serviceWorker.ready
      const vapidKey = import.meta.env.VITE_VAPID_PUBLIC_KEY ?? ''
      const applicationServerKey = vapidKey ? urlBase64ToUint8Array(vapidKey).buffer as ArrayBuffer : undefined
      const subscription = await registration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey
      })
      const json = subscription.toJSON() as Record<string, unknown>
      const keys = json.keys as { p256dh: string, auth: string } | undefined
      if (keys) {
        const { suscribirPush } = await import('~/services/api/push')
        await suscribirPush({
          endpoint: json.endpoint as string ?? '',
          p256dh: keys.p256dh,
          auth: keys.auth
        })
      }
      isSubscribed.value = true
    } catch (e) {
      if ((e as Error).name !== 'NotAllowedError') {
        console.error('Error al suscribir push:', e)
      }
      isSubscribed.value = false
    } finally {
      loading.value = false
    }
  }

  async function desuscribir() {
    if (!isSupported.value) return
    loading.value = true
    try {
      const registration = await navigator.serviceWorker.ready
      const subscription = await registration.pushManager.getSubscription()
      if (subscription) {
        const endpoint = subscription.endpoint
        await subscription.unsubscribe()
        try {
          const { desuscribirPush } = await import('~/services/api/push')
          await desuscribirPush(endpoint)
        } catch {
          // Silenciar error de red al desuscribir
        }
      }
      isSubscribed.value = false
    } finally {
      loading.value = false
    }
  }

  function togglePush(on: boolean) {
    if (on) {
      return suscribir()
    } else {
      return desuscribir()
    }
  }

  onMounted(() => {
    checkSupport()
    actualizarEstado()
  })

  return { isSupported, isSubscribed, loading, suscribir, desuscribir, togglePush }
}

function urlBase64ToUint8Array(base64String: string): Uint8Array {
  const padding = '='.repeat((4 - (base64String.length % 4)) % 4)
  const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/')
  const rawData = atob(base64)
  const outputArray = new Uint8Array(rawData.length)
  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i)
  }
  return outputArray
}
