export type Mora = {
  id: number
  prestamo_id: number
  cuota_id: number
  fecha: string
  valor: number
  estado: string
  created_at?: string
}

export type MoraCreateUpdate = {
  prestamo_id: number
  cuota_id: number
  fecha: string
  valor: number
  estado: string
}

export type RespuestaProcesarMoras = {
  moras_actualizadas: number[]
}
