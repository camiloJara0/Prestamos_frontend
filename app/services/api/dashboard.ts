import type { DashboardResumen } from '#shared/types/dashboard'

export const getDashboardResumen = async () => {
  return useApi().apiGet<DashboardResumen>('/dashboard/resumen')
}
