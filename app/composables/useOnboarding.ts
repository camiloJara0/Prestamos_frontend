import { marcarOnboardingCompletado } from '~/services/api/onboarding'

export function useOnboarding() {
  const needsOnboarding = ref(false)
  const pasoActual = ref(0)
  const completado = ref(false)
  const cargando = ref(false)

  const totalPasos = 4

  const pasos = [
    { id: 0, titulo: 'Tipos de préstamo', descripcion: 'Crea al menos un tipo de préstamo para comenzar.', icono: 'i-lucide-tags' },
    { id: 1, titulo: 'Tipos de pago', descripcion: 'Registra los métodos de pago que aceptas.', icono: 'i-lucide-credit-card' },
    { id: 2, titulo: 'Capital inicial', descripcion: 'Establece el capital disponible para préstamos.', icono: 'i-lucide-wallet' },
    { id: 3, titulo: 'Primeros clientes', descripcion: 'Agrega los primeros clientes del sistema.', icono: 'i-lucide-users' }
  ]

  function verificarEstado() {
    if (!import.meta.client) return
    const guardado = localStorage.getItem('loansoft:onboarding_completed')
    if (guardado === 'true') {
      completado.value = true
      needsOnboarding.value = false
    }
  }

  function iniciar() {
    needsOnboarding.value = true
    pasoActual.value = 0
  }

  function avanzarPaso() {
    if (pasoActual.value < totalPasos - 1) {
      pasoActual.value++
    }
  }

  function retrocederPaso() {
    if (pasoActual.value > 0) {
      pasoActual.value--
    }
  }

  async function completar() {
    cargando.value = true
    try {
      await marcarOnboardingCompletado()
      completado.value = true
      needsOnboarding.value = false
      if (import.meta.client) {
        localStorage.setItem('loansoft:onboarding_completed', 'true')
      }
    } finally {
      cargando.value = false
    }
  }

  function omitir() {
    completado.value = true
    needsOnboarding.value = false
    if (import.meta.client) {
      localStorage.setItem('loansoft:onboarding_completed', 'true')
    }
  }

  return {
    needsOnboarding,
    pasoActual,
    completado,
    cargando,
    pasos,
    totalPasos,
    verificarEstado,
    iniciar,
    avanzarPaso,
    retrocederPaso,
    completar,
    omitir
  }
}
