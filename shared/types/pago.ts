import type { PrestamoCuota } from './prestamo_cuota'

export type Pago = {
  id: number
  prestamo_id: number
  cliente_id: number
  cuota_id: number
  tipo_pago_id: number
  fecha_pago: string
  valor_pagado: number
  capital_pagado: number
  interes_pagado: number
  mora_pagada: number
  observaciones?: string | null
  referencia_recibo?: string | null
  estado_pago?: string
  fecha_devolucion?: string | null
  motivo_devolucion?: string | null
  created_at?: string
  updated_at?: string
  // Nombres resueltos solo en el historial global (RF-041)
  cliente_nombre?: string | null
  tipo_pago_nombre?: string | null
}

export type FiltrosHistorialPagos = {
  page?: number
  limit?: number
  cliente_id?: number
  tipo_pago_id?: number
  fecha_desde?: string
  fecha_hasta?: string
}

export type PagoCreate = {
  prestamo_id: number
  cliente_id: number
  cuota_id: number
  tipo_pago_id: number
  fecha_pago: string
  valor_pagado: number
  capital_pagado: number
  interes_pagado: number
  mora_pagada: number
  observaciones?: string | null
}

export type DesgloseCuota = Pick<
  PrestamoCuota,
  'capital' | 'interes' | 'mora' | 'valor_cuota'
>
