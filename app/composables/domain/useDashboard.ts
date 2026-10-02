import type { Prestamo } from '#shared/types/prestamo'
import type { ReporteGanancias, ReportePerdidas } from '#shared/types/reporte'
import type { Capital } from '#shared/types/capital'
import type { DashboardResumen } from '#shared/types/dashboard'
import { getPrestamos } from '~/services/api/prestamo'
import { getReporteGanancias, getReportePerdidas } from '~/services/api/reporte'
import { getCapital } from '~/services/api/capital'
import { getDashboardResumen } from '~/services/api/dashboard'

export type DashboardState = {
  capital: Capital | null
  prestamosActivos: Prestamo[]
  ganancias: ReporteGanancias | null
  perdidas: ReportePerdidas | null
  resumen: DashboardResumen | null
}

export function useDashboard() {
  const loading = ref(false)
  const error = ref<string | null>(null)
  const data = reactive<DashboardState>({
    capital: null,
    prestamosActivos: [],
    ganancias: null,
    perdidas: null,
    resumen: null
  })

  // RF-059: los indicadores se pintan desde la consulta consolidada cuando existe;
  // solo se degradan a las consultas múltiples si el endpoint consolidado falla.
  const totalActivos = computed(() => data.resumen?.prestamos_activos ?? data.prestamosActivos.length)
  const saldoPendienteTotal = computed(() => {
    if (data.resumen) return data.resumen.saldo_pendiente_total
    if (!data.prestamosActivos.length) return 0
    return data.prestamosActivos.reduce((sum, p) => sum + p.saldo_pendiente, 0)
  })
  const gananciaNeta = computed(() => data.resumen?.ganancia_neta ?? data.ganancias?.ganancia_neta ?? 0)
  const totalPrestadoPeriodo = computed(() => data.resumen?.total_prestado_periodo ?? data.ganancias?.total_prestado ?? 0)
  const totalPerdidas = computed(() => data.resumen?.total_perdidas ?? data.perdidas?.total_perdidas ?? 0)
  const cantidadPerdidos = computed(() => data.resumen?.cantidad_prestamos_perdidos ?? data.perdidas?.cantidad_prestamos_perdidos ?? 0)

  const distribucionEstados = computed(() => {
    const estados = data.resumen?.prestamos_por_estado
    if (!estados) return []
    const colorMap: Record<string, string> = { activo: '#7c3aed', pagado: '#10b981', perdido: '#ef4444', renovado: '#f59e0b' }
    return (['activo', 'pagado', 'perdido', 'renovado'] as const)
      .filter(e => estados[e] > 0)
      .map(e => ({
        label: e.charAt(0).toUpperCase() + e.slice(1),
        value: estados[e],
        color: colorMap[e] ?? '#6b7280'
      }))
  })

  const montoVencido = computed(() => data.resumen?.monto_vencido ?? 0)
  const moraPendiente = computed(() => data.resumen?.mora_pendiente ?? 0)
  const cobroDelDia = computed(() => data.resumen?.cobro_del_dia ?? 0)

  async function cargarConsultasMultiples() {
    const [capitalResult, prestamosResult, gananciasResult, perdidasResult, resumenResult] = await Promise.allSettled([
      getCapital(),
      getPrestamos({ estado: 'activo', limit: 100 }),
      getReporteGanancias(),
      getReportePerdidas(),
      getDashboardResumen()
    ])
    if (capitalResult.status === 'fulfilled') data.capital = capitalResult.value
    if (prestamosResult.status === 'fulfilled') data.prestamosActivos = prestamosResult.value.items
    if (gananciasResult.status === 'fulfilled') data.ganancias = gananciasResult.value
    if (perdidasResult.status === 'fulfilled') data.perdidas = perdidasResult.value
    if (resumenResult.status === 'fulfilled') data.resumen = resumenResult.value

    const failed = [capitalResult, prestamosResult, gananciasResult, perdidasResult, resumenResult].filter(r => r.status === 'rejected')
    if (failed.length > 0) {
      error.value = 'Algunos datos no pudieron cargarse.'
    }
  }

  async function fetch() {
    loading.value = true
    error.value = null
    try {
      try {
        // RF-059: una sola consulta resuelve todos los indicadores del tablero
        const resumen = await getDashboardResumen()
        data.resumen = resumen
        data.capital = { monto_total: resumen.capital_actual } as Capital
        data.ganancias = null
        data.perdidas = null
        data.prestamosActivos = []
      } catch {
        // Degradación al esquema de consultas múltiples
        await cargarConsultasMultiples()
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
    montoVencido,
    moraPendiente,
    cobroDelDia,
    fetch
  }
}
