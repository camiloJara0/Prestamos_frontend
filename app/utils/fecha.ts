export function toFechaInput(fecha: Date): string {
  const año = fecha.getFullYear()
  const mes = String(fecha.getMonth() + 1).padStart(2, '0')
  const dia = String(fecha.getDate()).padStart(2, '0')
  return `${año}-${mes}-${dia}`
}

export function hoyLocal(): string {
  return toFechaInput(new Date())
}

export function parsearFechaLocal(fecha?: string | Date | null): Date | null {
  if (!fecha) return null
  if (fecha instanceof Date) {
    return Number.isNaN(fecha.getTime()) ? null : fecha
  }
  const coincidencia = /^(\d{4})-(\d{2})-(\d{2})/.exec(fecha)
  if (coincidencia) {
    const [, año, mes, dia] = coincidencia
    const date = new Date(Number(año), Number(mes) - 1, Number(dia))
    return Number.isNaN(date.getTime()) ? null : date
  }
  const date = new Date(fecha)
  return Number.isNaN(date.getTime()) ? null : date
}

export function formatoFecha(fecha?: string | Date | null): string {
  const date = parsearFechaLocal(fecha)
  if (!date) return '—'
  const dia = String(date.getDate()).padStart(2, '0')
  const mes = String(date.getMonth() + 1).padStart(2, '0')
  return `${dia}/${mes}/${date.getFullYear()}`
}

export function diasEntre(desde: Date, hasta: Date): number {
  const a = new Date(desde.getFullYear(), desde.getMonth(), desde.getDate())
  const b = new Date(hasta.getFullYear(), hasta.getMonth(), hasta.getDate())
  return Math.round((b.getTime() - a.getTime()) / 86400000)
}

export function diasDeAtraso(fechaVencimiento: string | Date): number {
  const fecha = parsearFechaLocal(fechaVencimiento)
  if (!fecha) return 0
  return Math.max(0, diasEntre(fecha, new Date()))
}

export function agregarMeses(fecha: string | Date, meses: number): Date {
  const base = parsearFechaLocal(fecha) ?? new Date()
  const dia = base.getDate()
  const nuevoMes = base.getMonth() + meses
  const date = new Date(base.getFullYear(), nuevoMes, 1)
  const ultimoDia = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate()
  date.setDate(Math.min(dia, ultimoDia))
  return date
}

export function mesEnEspanol(mes?: number | null): string {
  const meses = [
    'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
  ]
  if (!mes || mes < 1 || mes > 12) return ''
  return meses[mes - 1] ?? ''
}
