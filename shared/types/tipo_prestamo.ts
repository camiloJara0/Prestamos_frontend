import type { Prestamo } from './prestamo'

export type EstadoTipoPrestamo = 'activo' | 'inactivo'

export type TipoPrestamo = {
  id: number
  nombre: string
  descripcion?: string | null
  interes_mensual?: number | null
  max_cuotas?: number | null
  estado: EstadoTipoPrestamo
  prestamos?: Prestamo[]
}

export type TipoPrestamoCreate = {
  nombre: string
  descripcion: string
  interes_mensual: number
  max_cuotas: number
  estado?: EstadoTipoPrestamo
}
