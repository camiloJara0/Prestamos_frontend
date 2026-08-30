export type PrestamoPerdido = {
  id: number
  prestamo_id: number
  fecha: string
  valor_perdido: number
  motivo?: string | null
  created_at?: string
}
