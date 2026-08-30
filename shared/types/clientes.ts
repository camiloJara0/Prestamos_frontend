export type EstadoCliente = 'activo' | 'inactivo'

export type Cliente = {
  id: number
  nombre: string
  cedula: string
  telefono?: string | null
  direccion?: string | null
  persona_referencia?: string | null
  telefono_referencia?: string | null
  observaciones?: string | null
  estado: EstadoCliente
}

export type ClienteCreate = {
  nombre: string
  cedula: string
  telefono?: string | null
  direccion?: string | null
  persona_referencia?: string | null
  telefono_referencia?: string | null
  observaciones?: string | null
  estado?: EstadoCliente
}
