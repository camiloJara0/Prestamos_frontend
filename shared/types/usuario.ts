export type RolUsuario = 'admin' | 'usuario'
export type EstadoUsuario = 'activo' | 'inactivo'

export type Usuario = {
  id: number
  nombre: string
  email: string
  rol: RolUsuario
  estado: EstadoUsuario
  created_at?: string
}

export type UsuarioMe = {
  id: number
  nombre: string
  email: string
  rol: RolUsuario
  estado: EstadoUsuario
}
