import type { Prestamo } from '#shared/types/prestamo'
import type { ReporteGanancias, ReportePerdidas } from '#shared/types/reporte'
import type { Capital } from '#shared/types/capital'
import { getPrestamos } from '~/services/api/prestamo'
import { getReporteGanancias, getReportePerdidas } from '~/services/api/reporte'
import { getCapital } from '~/services/api/capital'

export type DashboardState = {
  capital: Capital | null
  prestamosActivos: Prestamo[]
  ganancias: ReporteGanancias | null
  perdidas: ReportePerdidas | null
}

export function useDashboard() {
  const loading = ref(false)
  const error = ref<string | null>(null)
  const data = reactive<DashboardState>({
    capital: null,
    prestamosActivos: [],
    ganancias: null,
    perdidas: null
  })

  const totalActivos = computed(() => data.prestamosActivos.length)
  const saldoPendienteTotal = computed(() =>
    data.prestamosActivos.reduce((sum, p) => sum + p.saldo_pendiente, 0)
  )
  const gananciaNeta = computed(() => data.ganancias?.ganancia_neta ?? 0)
  const totalPrestadoPeriodo = computed(() => data.ganancias?.total_prestado ?? 0)
  const totalPerdidas = computed(() => data.perdidas?.total_perdidas ?? 0)
  const cantidadPerdidos = computed(() => data.perdidas?.cantidad_prestamos_perdidos ?? 0)

  const distribucionEstados = computed(() => {
    const prestamos = data.prestamosActivos
    if (!prestamos.length) return []
    const estados = ['activo', 'pagado', 'perdido', 'renovado'] as const
    const counts: Record<string, number> = {}
    for (const e of estados) counts[e] = 0
    for (const p of prestamos) {
      counts[p.estado] = (counts[p.estado] ?? 0) + 1
    }
    const colorMap: Record<string, string> = { activo: '#7c3aed', pagado: '#10b981', perdido: '#ef4444', renovado: '#f59e0b' }
    return estados
      .filter(e => (counts[e] ?? 0) > 0)
      .map(e => ({
        label: e.charAt(0).toUpperCase() + e.slice(1),
        value: counts[e] ?? 0,
        color: colorMap[e] ?? '#6b7280'
      }))
  })

  async function fetch() {
    loading.value = true
    error.value = null
    try {
      const [capitalResult, prestamosResult, gananciasResult, perdidasResult] = await Promise.allSettled([
        getCapital(),
        getPrestamos({ estado: 'activo', limit: 500 }),
        getReporteGanancias(),
        getReportePerdidas()
      ])
      if (capitalResult.status === 'fulfilled') data.capital = capitalResult.value
      if (prestamosResult.status === 'fulfilled') data.prestamosActivos = prestamosResult.value
      if (gananciasResult.status === 'fulfilled') data.ganancias = gananciasResult.value
      if (perdidasResult.status === 'fulfilled') data.perdidas = perdidasResult.value

      const failed = [capitalResult, prestamosResult, gananciasResult, perdidasResult].filter(r => r.status === 'rejected')
      if (failed.length > 0) {
        error.value = 'Algunos datos no pudieron cargarse.'
      }
    } catch {
      error.value = 'No se pudo cargar el dashboard.'
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    error,
    data,
    totalActivos,
    saldoPendienteTotal,
    gananciaNeta,
    totalPrestadoPeriodo,
    totalPerdidas,
    cantidadPerdidos,
    distribucionEstados,
    fetch
  }
}
