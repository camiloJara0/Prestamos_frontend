import { describe, expect, it } from 'vitest'
import { formatoMoneda, formatoNumero, formatoPorcentaje } from '../../app/utils/format'

describe('format', () => {
  it('formatea moneda COP sin decimales para enteros', () => {
    expect(formatoMoneda(10000000)).toContain('10.000.000')
  })

  it('formatea moneda COP con decimales cuando existen', () => {
    expect(formatoMoneda(1083333.33)).toContain('1.083.333,33')
  })

  it('maneja null/undefined como 0', () => {
    expect(formatoMoneda(null)).toMatch(/^\$\s*0$/)
    expect(formatoMoneda(undefined)).toMatch(/^\$\s*0$/)
  })

  it('formatea números con separador de miles', () => {
    expect(formatoNumero(1234567.891)).toBe('1.234.567,89')
  })

  it('formatea porcentajes', () => {
    expect(formatoPorcentaje(2.5)).toBe('2,5%')
  })
})
