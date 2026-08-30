import { agregarMeses, toFechaInput } from './fecha'

export type EstadoCuotaCalculada = 'pendiente' | 'pagado' | 'vencido' | 'parcial'

export interface CalculoPrestamo {
  interes_total: number
  monto_total: number
  valor_cuota: number
  saldo_pendiente: number
}

export interface CuotaCalculada {
  numero_cuota: number
  fecha_vencimiento: string
  valor_cuota: number
  capital: number
  interes: number
  mora: number
  estado: EstadoCuotaCalculada
}

export interface DesglosePago {
  capital_pagado: number
  interes_pagado: number
  mora_pagada: number
  valor_pagado: number
}

/**
 * Redondeo a 2 decimales.
 * Nota: replica con aproximación el redondeo del backend (Python `round`, bancario).
 * Math.round redondea medio hacia arriba mientras Python redondea medio al par;
 * la divergencia solo aparece en casos límite de exactamente .005.
 */
export function redondear(valor: number): number {
  return Math.round((valor + Number.EPSILON) * 100) / 100
}

export function calcularPrestamo(params: {
  capital_prestado: number
  porcentaje_interes: number
  numero_cuotas: number
}): CalculoPrestamo {
  const { capital_prestado, porcentaje_interes, numero_cuotas } = params
  const interes_total = redondear(capital_prestado * (porcentaje_interes / 100) * numero_cuotas)
  const monto_total = redondear(capital_prestado + interes_total)
  const valor_cuota = redondear(monto_total / numero_cuotas)
  return {
    interes_total,
    monto_total,
    valor_cuota,
    saldo_pendiente: monto_total
  }
}

export function calcularCuotas(params: {
  capital_prestado: number
  interes_total: number
  numero_cuotas: number
  fecha_prestamo: string
}): CuotaCalculada[] {
  const { capital_prestado, interes_total, numero_cuotas, fecha_prestamo } = params
  const capitalPorCuota = redondear(capital_prestado / numero_cuotas)
  const interesPorCuota = redondear(interes_total / numero_cuotas)
  const valor_cuota = redondear((capital_prestado + interes_total) / numero_cuotas)

  const cuotas: CuotaCalculada[] = []
  for (let i = 1; i <= numero_cuotas; i++) {
    cuotas.push({
      numero_cuota: i,
      fecha_vencimiento: toFechaInput(agregarMeses(fecha_prestamo, i)),
      valor_cuota,
      capital: capitalPorCuota,
      interes: interesPorCuota,
      mora: 0,
      estado: 'pendiente'
    })
  }
  return cuotas
}

export function validarCuadrePago(desglose: DesglosePago): { valido: boolean, diferencia: number } {
  const suma = redondear(desglose.capital_pagado + desglose.interes_pagado + desglose.mora_pagada)
  const valor = redondear(desglose.valor_pagado)
  const diferencia = Math.abs(suma - valor)
  return { valido: diferencia <= 0.01, diferencia }
}

export function topePago(valorCuota: number, mora = 0): number {
  return valorCuota + mora + 0.01
}

export function sugerirDesglosePago(params: {
  valorPagado: number
  capitalCuota: number
  interesCuota: number
}): DesglosePago {
  const { valorPagado, capitalCuota, interesCuota } = params
  const capital = redondear(Math.min(capitalCuota, valorPagado))
  const restante = redondear(valorPagado - capital)
  const interes = redondear(Math.min(interesCuota, restante))
  const mora = redondear(restante - interes)
  return { capital_pagado: capital, interes_pagado: interes, mora_pagada: mora, valor_pagado: redondear(valorPagado) }
}
