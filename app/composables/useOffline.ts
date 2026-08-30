export function useOffline() {
  const isOnline = ref(true)

  function handleOnline() {
    isOnline.value = true
  }

  function handleOffline() {
    isOnline.value = false
  }

  function init() {
    if (!import.meta.client) return
    isOnline.value = navigator.onLine
    window.addEventListener('online', handleOnline)
    window.addEventListener('offline', handleOffline)
  }

  function destroy() {
    if (!import.meta.client) return
    window.removeEventListener('online', handleOnline)
    window.removeEventListener('offline', handleOffline)
  }

  return { isOnline, init, destroy }
}
