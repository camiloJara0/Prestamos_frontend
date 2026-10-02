import type { ReporteGanancias, ReportePerdidas, ReporteCobranza, ReporteCartera, FiltrosReporte, ReporteTipo, ReporteFormato } from '#shared/types/reporte'

export const getReporteGanancias = async (params: FiltrosReporte = {}) => {
  return useApi().apiGet<ReporteGanancias>('/reportes/ganancias', { query: { ...params } })
}

export const getReportePerdidas = async (params: FiltrosReporte = {}) => {
  return useApi().apiGet<ReportePerdidas>('/reportes/perdidas', { query: { ...params } })
}

export const getReporteCartera = async (params: { desde?: string, hasta?: string } = {}) => {
  return useApi().apiGet<ReporteCartera>('/reportes/cartera', { query: { ...params } })
}

export const getReporteCobranza = async (params: { desde?: string, hasta?: string } = {}) => {
  return useApi().apiGet<ReporteCobranza>('/reportes/cobranza', { query: { ...params } })
}

export const descargarReporte = async (tipo: ReporteTipo, formato: ReporteFormato, params: FiltrosReporte = {}) => {
  const ext = formato === 'excel' ? 'xlsx' : 'pdf'
  const filename = `${tipo}.${ext}`
  const query: Record<string, string | number> = { ...params }
  await useApi().apiDownload(`/reportes/${tipo}/${formato}`, filename, { query })
}
