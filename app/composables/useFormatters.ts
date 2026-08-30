import { formatoMoneda, formatoNumero, formatoPorcentaje } from '~/utils/format'
import { formatoFecha, hoyLocal, mesEnEspanol } from '~/utils/fecha'

const COLS = {
  formatoMoneda,
  formatoNumero,
  formatoPorcentaje,
  formatoFecha,
  hoyLocal,
  mesEnEspanol
}

export function useFormatters() {
  return COLS
}
