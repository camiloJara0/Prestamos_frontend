export interface ItemImportacion {
  cuota_id?: number
  prestamo_id?: number
  cliente_nombre?: string
  cedula?: string
  fecha_pago: string
  valor_pagado: number
  estado: 'identificado' | 'error' | 'pendiente'
  detalle?: string
}

export interface ResultadoImportacion {
  cuotas_identificadas: ItemImportacion[]
  pagos_aplicados: ItemImportacion[]
  errores: ItemImportacion[]
  pendientes_revision: ItemImportacion[]
}

export type FormatoExtracto = 'csv' | 'xlsx'
