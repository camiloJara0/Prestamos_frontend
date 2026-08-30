export type EstadoTipoPago = 'activo' | 'inactivo'

export type TipoPago = {
  id: number
  nombre: string
  descripcion?: string | null
  estado?: EstadoTipoPago
}

export type TipoPagoCreate = {
  nombre: string
  descripcion: string
}
