export type PrestamosPorEstado = {
  activo: number
  pagado: number
  perdido: number
  renovado: number
}

export type DashboardResumen = {
  capital_actual: number
  prestamos_activos: number
  saldo_pendiente_total: number
  ganancia_neta: number
  total_prestado_periodo: number
  mora_acumulada: number
  prestamos_por_estado: PrestamosPorEstado
  // Indicadores de cobranza y mora (RF-058)
  monto_vencido: number
  mora_pendiente: number
  cobro_del_dia: number
  // Indicadores de pérdidas (RF-059)
  total_perdidas: number
  cantidad_prestamos_perdidos: number
}
