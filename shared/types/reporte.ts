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

export type ReporteTipo = 'ganancias' | 'perdidas'
export type ReporteFormato = 'excel' | 'pdf'

export type FiltrosReporte = {
  mes?: number
  anio?: number
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

export type ReporteCobranza = {
  periodo: string
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
