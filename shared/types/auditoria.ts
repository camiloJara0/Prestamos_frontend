export type Auditoria = {
  id: number
  usuario_id: number | null
  tabla_afectada: string
  tipo_operacion: string
  registro_id: number | null
  valores_anteriores: string | null
  valores_nuevos: string | null
  descripcion: string | null
  ip_address: string | null
  fecha: string
}
