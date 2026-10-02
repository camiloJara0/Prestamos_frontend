export function useNotifications() {
  const isSupported = ref(false)
  const isGranted = ref(false)
  const permission = ref<NotificationPermission>('default')

  function init() {
    if (typeof window === 'undefined' || !('Notification' in window)) {
      isSupported.value = false
      return
    }
    isSupported.value = true
    permission.value = Notification.permission
    isGranted.value = Notification.permission === 'granted'
  }

  async function requestPermission(): Promise<boolean> {
    if (!isSupported.value) return false
    const result = await Notification.requestPermission()
    permission.value = result
    isGranted.value = result === 'granted'
    return result === 'granted'
  }

  function sendNotification(title: string, options?: NotificationOptions) {
    if (!isGranted.value) return
    new Notification(title, {
      icon: '/icons/icon-192x192.png',
      badge: '/icons/icon-192x192.png',
      ...options
    })
  }

  return {
    isSupported,
    isGranted,
    permission,
    init,
    requestPermission,
    sendNotification
  }
}
