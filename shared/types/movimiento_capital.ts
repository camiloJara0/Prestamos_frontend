export type TipoMovimiento
  = | 'inversion'
    | 'retiro'
    | 'prestamo_otorgado'
    | 'pago_recibido'
    | 'perdida'

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
  descripcion?: string | null
  valor: number
  fecha: string
}

export type RespuestaMovimientoCapital = {
  movimiento: MovimientoCapital
  capital_actual: number
}
