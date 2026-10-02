export type TipoMovimiento
  = | 'inversion'
    | 'retiro'
    | 'prestamo_otorgado'
    | 'pago_recibido'
    | 'perdida'
    | 'ajuste_prestamo'
    | 'devolucion_pago'

export type MovimientoCapital = {
  id: number
  tipo_movimiento: TipoMovimiento
  descripcion?: string | null
  valor: number
  fecha: string
  prestamo_id?: number | null
  created_at?: string
}

export type MovimientoCapitalCreate = {
  tipo_movimiento: 'inversion' | 'retiro'
  descripcion: string
  valor: number
  fecha: string
}

export type RespuestaMovimientoCapital = {
  movimiento: MovimientoCapital
  capital_actual: number
}

export type ResumenCaja = {
  periodo: string
  ingresos: number
  egresos: number
  cantidad_ingresos: number
  cantidad_egresos: number
  saldo_capital: number
}
