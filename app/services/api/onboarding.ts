import type { OnboardingState } from '#shared/types/onboarding'

export const getOnboardingEstado = async (): Promise<OnboardingState> => {
  try {
    const response = await useApi().apiGet<{ onboarding_completed: boolean }>('/auth/me')
    return { onboarding_completed: response?.onboarding_completed ?? false }
  } catch {
    return { onboarding_completed: false }
  }
}

export const marcarOnboardingCompletado = async (): Promise<void> => {
  try {
    await useApi().apiPost('/onboarding/completar', {})
  } catch {
    // Stub: si el endpoint no existe aún, silenciar el error
  }
}
