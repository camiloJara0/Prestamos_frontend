import type { ReporteGanancias, ReportePerdidas, ReporteCartera, ReporteCobranza, FiltrosReporte, ReporteTipo, ReporteFormato } from '#shared/types/reporte'
import { getReporteGanancias, getReportePerdidas, getReporteCartera, getReporteCobranza, descargarReporte } from '~/services/api/reporte'

export function useReportes() {
  const ganancias = ref<ReporteGanancias | null>(null)
  const perdidas = ref<ReportePerdidas | null>(null)
  const cartera = ref<ReporteCartera | null>(null)
  const cobranza = ref<ReporteCobranza | null>(null)
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

  async function fetchCartera(params: { desde?: string, hasta?: string } = {}) {
    loading.value = true
    error.value = null
    try {
      cartera.value = await getReporteCartera(params)
    } catch {
      error.value = 'No se pudo cargar el reporte de cartera.'
    } finally {
      loading.value = false
    }
  }

  async function fetchCobranza(params: { desde?: string, hasta?: string } = {}) {
    loading.value = true
    error.value = null
    try {
      cobranza.value = await getReporteCobranza(params)
    } catch {
      error.value = 'No se pudo cargar el reporte de cobranza.'
    } finally {
      loading.value = false
    }
  }

  async function fetchTodos(params: FiltrosReporte = {}) {
    loading.value = true
    error.value = null
    try {
      const rango = { desde: params.desde, hasta: params.hasta }
      const [g, p, c, co] = await Promise.allSettled([
        getReporteGanancias(params),
        getReportePerdidas(params),
        getReporteCartera(rango),
        getReporteCobranza(rango)
      ])
      if (g.status === 'fulfilled') ganancias.value = g.value
      if (p.status === 'fulfilled') perdidas.value = p.value
      if (c.status === 'fulfilled') cartera.value = c.value
      if (co.status === 'fulfilled') cobranza.value = co.value
      const failed = [g, p, c, co].filter(r => r.status === 'rejected')
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
    cartera,
    cobranza,
    loading,
    error,
    descargando,
    fetchGanancias,
    fetchPerdidas,
    fetchCartera,
    fetchCobranza,
    fetchTodos,
    descargar
  }
}
