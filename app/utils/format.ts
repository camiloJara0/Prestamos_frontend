export function formatoMoneda(valor?: number | null): string {
  const n = Number(valor ?? 0)
  if (!Number.isFinite(n)) return '$ 0'
  const conDecimales = !Number.isInteger(n)
  return new Intl.NumberFormat('es-CO', {
    style: 'currency',
    currency: 'COP',
    minimumFractionDigits: 0,
    maximumFractionDigits: conDecimales ? 2 : 0
  }).format(n)
}

export function formatoNumero(valor?: number | null, decimales = 2): string {
  const n = Number(valor ?? 0)
  if (!Number.isFinite(n)) return '0'
  return new Intl.NumberFormat('es-CO', {
    minimumFractionDigits: 0,
    maximumFractionDigits: decimales
  }).format(n)
}

export function formatoPorcentaje(valor?: number | null): string {
  const n = Number(valor ?? 0)
  if (!Number.isFinite(n)) return '0%'
  return `${new Intl.NumberFormat('es-CO', {
    maximumFractionDigits: 2
  }).format(n)}%`
}
