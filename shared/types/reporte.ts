export type ReporteGanancias = {
  periodo: string
  total_invertido: number
  total_prestado: number
  total_pagos_recibidos: number
  total_intereses: number
  ganancia_neta: number
}

export type DetallePerdida = {
  prestamo_id: number
  fecha: string
  valor_perdido: number
  motivo: string | null
}

export type ReportePerdidas = {
  periodo: string
  total_perdidas: number
  cantidad_prestamos_perdidos: number
  detalle: DetallePerdida[]
}

export type ReporteTipo = 'ganancias' | 'perdidas' | 'cartera' | 'cobranza'
export type ReporteFormato = 'excel' | 'pdf'

export type FiltrosReporte = {
  mes?: number
  anio?: number
  desde?: string
  hasta?: string
}

export type DetalleCartera = {
  prestamo_id: number
  cliente: string
  estado: string
  fecha_prestamo: string
  capital_prestado: number
  saldo_pendiente: number
  dias_antiguedad: number
}

export type GrupoCartera = {
  cantidad: number
  monto: number
}

export type ReporteCartera = {
  periodo: string
  nota: string | null
  total_prestamos: number
  saldo_pendiente_total: number
  total_activos: number
  monto_activos: number
  saldo_activos: number
  total_renovados: number
  monto_renovados: number
  total_perdidos: number
  monto_perdidos: number
  total_pagados: number
  monto_pagados: number
  distribucion_por_estado: Record<string, GrupoCartera>
  distribucion_por_tipo: Record<string, GrupoCartera>
  antiguedad: Record<string, { cantidad: number, saldo: number }>
  detalle: DetalleCartera[]
}

export type CuotaCobranza = {
  cuota_id: number
  prestamo_id: number
  cliente_nombre: string
  numero_cuota: number
  fecha_vencimiento: string
  valor_cuota: number
  estado: string
  dias_atraso: number
  mora?: number
  saldo?: number
}

export type TotalesCobrados = {
  capital: number
  interes: number
  mora: number
  total: number
}

export type CobroPorDia = {
  fecha: string
  cantidad_pagos: number
  capital: number
  interes: number
  mora: number
  total: number
}

export type ReporteCobranza = {
  periodo: string
  nota: string | null
  totales_cobrados: TotalesCobrados
  detalle_por_dia: CobroPorDia[]
  total_cuotas_por_vencer: number
  monto_por_vencer: number
  total_cuotas_vencidas: number
  monto_vencido: number
  total_cuotas_pagadas: number
  monto_pagado: number
  cuotas_por_vencer: CuotaCobranza[]
  cuotas_vencidas: CuotaCobranza[]
  cuotas_pagadas: CuotaCobranza[]
}
