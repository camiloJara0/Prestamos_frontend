import { describe, expect, it } from 'vitest'
import {
  agregarMeses,
  diasDeAtraso,
  diasEntre,
  formatoFecha,
  hoyLocal,
  mesEnEspanol,
  parsearFechaLocal,
  toFechaInput
} from '../../app/utils/fecha'

describe('fecha', () => {
  it('parsea YYYY-MM-DD como fecha local', () => {
    const fecha = parsearFechaLocal('2026-08-12')
    expect(fecha?.getFullYear()).toBe(2026)
    expect(fecha?.getMonth()).toBe(7)
    expect(fecha?.getDate()).toBe(12)
  })

  it('formatea a dd/mm/yyyy', () => {
    expect(formatoFecha('2026-08-05')).toBe('05/08/2026')
  })

  it('agrega meses conservando día', () => {
    expect(toFechaInput(agregarMeses('2026-01-15', 1))).toBe('2026-02-15')
  })

  it('agrega meses clampeando al último día', () => {
    expect(toFechaInput(agregarMeses('2026-01-31', 1))).toBe('2026-02-28')
    expect(toFechaInput(agregarMeses('2026-05-31', 1))).toBe('2026-06-30')
  })

  it('calcula días entre fechas', () => {
    expect(diasEntre(new Date('2026-08-01'), new Date('2026-08-11'))).toBe(10)
  })

  it('días de atraso no negativos', () => {
    expect(diasDeAtraso('2099-01-01')).toBe(0)
  })

  it('hoyLocal devuelve formato YYYY-MM-DD', () => {
    expect(hoyLocal()).toMatch(/^\d{4}-\d{2}-\d{2}$/)
  })

  it('mesEnEspanol', () => {
    expect(mesEnEspanol(1)).toBe('Enero')
    expect(mesEnEspanol(12)).toBe('Diciembre')
    expect(mesEnEspanol()).toBe('')
  })
})
