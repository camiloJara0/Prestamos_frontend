export function usePwaInstall() {
  const canInstall = ref(false)
  const deferredPrompt = ref<Event | null>(null)

  function handler(e: Event) {
    e.preventDefault()
    deferredPrompt.value = e
    canInstall.value = true
  }

  function init() {
    if (!import.meta.client) return
    window.addEventListener('beforeinstallprompt', handler)
    window.addEventListener('appinstalled', () => {
      canInstall.value = false
      deferredPrompt.value = null
    })
  }

  function destroy() {
    if (!import.meta.client) return
    window.removeEventListener('beforeinstallprompt', handler)
  }

  async function promptInstall() {
    if (!deferredPrompt.value) return false
    const prompt = deferredPrompt.value as unknown as { prompt: () => Promise<void>, userChoice: Promise<{ outcome: string }> }
    await prompt.prompt()
    const result = await prompt.userChoice
    canInstall.value = false
    deferredPrompt.value = null
    return result.outcome === 'accepted'
  }

  return { canInstall, init, destroy, promptInstall }
}
