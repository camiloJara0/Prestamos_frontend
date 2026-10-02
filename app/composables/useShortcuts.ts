export function useShortcuts() {
  const shortcutsEnabled = ref(true)

  function isInputFocused(): boolean {
    if (typeof document === 'undefined') return false
    const el = document.activeElement
    if (!el) return false
    const tag = el.tagName.toLowerCase()
    return tag === 'input' || tag === 'textarea' || (el as HTMLElement).isContentEditable
  }

  function register(combo: string, handler: () => void) {
    if (typeof window === 'undefined') return

    window.addEventListener('keydown', (e: KeyboardEvent) => {
      if (!shortcutsEnabled.value) return

      // Ctrl+K / Cmd+K always works
      const isMetaK = (e.ctrlKey || e.metaKey) && e.key === 'k'
      if (isMetaK) {
        e.preventDefault()
        handler()
        return
      }

      // Skip if typing in input (except for ctrl combos)
      if (isInputFocused()) return

      const parts = combo.toLowerCase().split('+')
      const key = parts[parts.length - 1]
      const needCtrl = parts.includes('ctrl')
      const needShift = parts.includes('shift')
      const needAlt = parts.includes('alt')
      const needMeta = parts.includes('meta') || parts.includes('cmd')

      if (needCtrl && !e.ctrlKey) return
      if (needShift && !e.shiftKey) return
      if (needAlt && !e.altKey) return
      if (needMeta && !e.metaKey) return

      if (e.key.toLowerCase() === key) {
        e.preventDefault()
        handler()
      }
    })
  }

  return { shortcutsEnabled, register }
}
