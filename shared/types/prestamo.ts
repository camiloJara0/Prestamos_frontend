import type { Cliente } from './clientes'
import type { PrestamoCuota } from './prestamo_cuota'
import type { TipoPrestamo } from './tipo_prestamo'
import type { Pago } from './pago'

export type EstadoPrestamo = 'activo' | 'pagado' | 'perdido' | 'renovado'

export type Prestamo = {
  id: number
  cliente_id: number
  tipo_prestamo_id: number
  fecha_prestamo: string
  capital_prestado: number
  porcentaje_interes: number
  interes_total: number
  monto_total: number
  numero_cuotas: number
  valor_cuota: number
  saldo_pendiente: number
  estado: EstadoPrestamo
  observaciones?: string | null
}

export type PrestamoDetalle = Prestamo & {
  cliente: Cliente | null
  tipo_prestamo: TipoPrestamo | null
  cuotas: PrestamoCuota[]
  pagos: Pago[]
}

export type PrestamoCreate = {
  cliente_id: number
  tipo_prestamo_id: number
  fecha_prestamo: string
  capital_prestado: number
  porcentaje_interes: number
  numero_cuotas: number
  observaciones?: string | null
}

export type RenovacionCreate = {
  porcentaje_interes: number
  numero_cuotas: number
  abono?: number
  fecha_renovacion: string
  observaciones?: string | null
}

export type PrestamoFiltros = {
  estado?: EstadoPrestamo | 'todos'
  cliente_id?: number
  fecha_desde?: string
  fecha_hasta?: string
  busqueda?: string
  skip?: number
  limit?: number
}

export type RespuestaMarcarPerdido = {
  prestamo: Prestamo & { created_at?: string, updated_at?: string }
  valor_perdido: number
  motivo: string | null
  fecha: string
}
