export type RolUsuario = "admin" | "usuario";
export type EstadoUsuario = "activo" | "inactivo";

export type Usuario = {
  id: number;
  nombre: string;
  email: string;
  hashed_password: string;
  rol: RolUsuario;
  estado: EstadoUsuario;
  created_at: string;
  tokens?: string;
};