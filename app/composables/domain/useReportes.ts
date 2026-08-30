import type { ReporteGanancias, ReportePerdidas, FiltrosReporte, ReporteTipo, ReporteFormato } from '#shared/types/reporte'
import { getReporteGanancias, getReportePerdidas, descargarReporte } from '~/services/api/reporte'

export function useReportes() {
  const ganancias = ref<ReporteGanancias | null>(null)
  const perdidas = ref<ReportePerdidas | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const descargando = ref(false)

  async function fetchGanancias(params: FiltrosReporte = {}) {
    loading.value = true
    error.value = null
    try {
      ganancias.value = await getReporteGanancias(params)
    } catch {
      error.value = 'No se pudo cargar el reporte de ganancias.'
    } finally {
      loading.value = false
    }
  }

  async function fetchPerdidas(params: FiltrosReporte = {}) {
    loading.value = true
    error.value = null
    try {
      perdidas.value = await getReportePerdidas(params)
    } catch {
      error.value = 'No se pudo cargar el reporte de pérdidas.'
    } finally {
      loading.value = false
    }
  }

  async function fetchTodos(params: FiltrosReporte = {}) {
    loading.value = true
    error.value = null
    try {
      const [g, p] = await Promise.allSettled([
        getReporteGanancias(params),
        getReportePerdidas(params)
      ])
      if (g.status === 'fulfilled') ganancias.value = g.value
      if (p.status === 'fulfilled') perdidas.value = p.value
      const failed = [g, p].filter(r => r.status === 'rejected')
      if (failed.length > 0) error.value = 'Algunos reportes no pudieron cargarse.'
    } catch {
      error.value = 'No se pudieron cargar los reportes.'
    } finally {
      loading.value = false
    }
  }

  async function descargar(tipo: ReporteTipo, formato: ReporteFormato, params: FiltrosReporte = {}) {
    descargando.value = true
    try {
      await descargarReporte(tipo, formato, params)
    } catch {
      throw new Error('No se pudo descargar el reporte.')
    } finally {
      descargando.value = false
    }
  }

  return {
    ganancias,
    perdidas,
    loading,
    error,
    descargando,
    fetchGanancias,
    fetchPerdidas,
    fetchTodos,
    descargar
  }
}
