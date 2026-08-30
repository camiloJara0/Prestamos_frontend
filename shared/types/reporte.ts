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
