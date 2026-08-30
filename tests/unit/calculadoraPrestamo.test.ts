import { describe, expect, it } from 'vitest'
import {
  calcularPrestamo,
  calcularCuotas,
  redondear,
  sugerirDesglosePago,
  topePago,
  validarCuadrePago
} from '../../app/utils/calculadoraPrestamo'

describe('redondear', () => {
  it('redondea a 2 decimales', () => {
    expect(redondear(1.005)).toBe(1.01)
    expect(redondear(1.004)).toBe(1.0)
    expect(redondear(2.675)).toBe(2.68)
  })
})

describe('calcularPrestamo', () => {
  it('calcula valores redondos', () => {
    const resultado = calcularPrestamo({ capital_prestado: 1000, porcentaje_interes: 2.5, numero_cuotas: 4 })
    expect(resultado.interes_total).toBe(100)
    expect(resultado.monto_total).toBe(1100)
    expect(resultado.valor_cuota).toBe(275)
    expect(resultado.saldo_pendiente).toBe(1100)
  })

  it('calcula valores con decimales', () => {
    const resultado = calcularPrestamo({ capital_prestado: 10000000, porcentaje_interes: 2.5, numero_cuotas: 12 })
    expect(resultado.interes_total).toBe(3000000)
    expect(resultado.monto_total).toBe(13000000)
    expect(resultado.valor_cuota).toBe(1083333.33)
  })

  it('interés total = capital * (pct/100) * cuotas', () => {
    const resultado = calcularPrestamo({ capital_prestado: 5000000, porcentaje_interes: 3, numero_cuotas: 6 })
    expect(resultado.interes_total).toBe(900000)
    expect(resultado.monto_total).toBe(5900000)
    expect(resultado.valor_cuota).toBe(983333.33)
  })
})

describe('calcularCuotas', () => {
  it('genera las cuotas con vencimientos mensuales', () => {
    const cuotas = calcularCuotas({
      capital_prestado: 1000,
      interes_total: 100,
      numero_cuotas: 3,
      fecha_prestamo: '2026-01-15'
    })
    expect(cuotas).toHaveLength(3)
    expect(cuotas[0]).toMatchObject({
      numero_cuota: 1,
      fecha_vencimiento: '2026-02-15',
      valor_cuota: 366.67,
      capital: 333.33,
      interes: 33.33,
      mora: 0,
      estado: 'pendiente'
    })
    expect(cuotas[2].fecha_vencimiento).toBe('2026-04-15')
  })

  it('clampa el día 31 al último día del mes (relativedelta)', () => {
    const cuotas = calcularCuotas({
      capital_prestado: 1000,
      interes_total: 100,
      numero_cuotas: 2,
      fecha_prestamo: '2026-01-31'
    })
    expect(cuotas[0].fecha_vencimiento).toBe('2026-02-28')
  })
})

describe('validarCuadrePago', () => {
  it('acepta desglose que cuadra (diferencia <= 0.01)', () => {
    const resultado = validarCuadrePago({ capital_pagado: 100, interes_pagado: 20, mora_pagada: 0.01, valor_pagado: 120.01 })
    expect(resultado.valido).toBe(true)
    expect(resultado.diferencia).toBe(0)
  })

  it('rechaza desglose que no cuadra', () => {
    const resultado = validarCuadrePago({ capital_pagado: 100, interes_pagado: 20, mora_pagada: 0, valor_pagado: 150 })
    expect(resultado.valido).toBe(false)
  })
})

describe('topePago', () => {
  it('valor cuota + mora + tolerancia', () => {
    expect(topePago(1000, 50)).toBe(1050.01)
  })
})

describe('sugerirDesglosePago', () => {
  it('reparte capital, interés y mora del valor pagado', () => {
    const desglose = sugerirDesglosePago({ valorPagado: 400, capitalCuota: 350, interesCuota: 50, moraCuota: 0 })
    expect(desglose).toEqual({ capital_pagado: 350, interes_pagado: 50, mora_pagada: 0, valor_pagado: 400 })
  })

  it('usa mora cuando el valor pagado supera capital + interés', () => {
    const desglose = sugerirDesglosePago({ valorPagado: 400, capitalCuota: 300, interesCuota: 50 })
    expect(desglose.mora_pagada).toBe(50)
  })
})
