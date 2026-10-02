import { getDB, type AuditLog } from './db'

export async function registrarAccion(accion: string, entidad: string, entidadId: number | null = null, detalle: unknown = null): Promise<void> {
  const db = getDB()
  if (!db) return

  const auth = useAuthStore()
  const entry: AuditLog = {
    timestamp: new Date().toISOString(),
    accion,
    entidad,
    entidadId,
    detalle,
    usuario: auth.user?.email ?? null
  }
  await db.auditLog.add(entry)
}

export async function obtenerLog(filtros?: { entidad?: string, desde?: string, hasta?: string, skip?: number, limit?: number }): Promise<AuditLog[]> {
  const db = getDB()
  if (!db) return []

  const collection = db.auditLog.orderBy('timestamp')

  let results = await collection.toArray()

  if (filtros?.entidad && filtros?.entidad !== 'all') {
    results = results.filter(r => r.entidad === filtros.entidad)
  }
  if (filtros?.desde) {
    results = results.filter(r => r.timestamp >= filtros.desde!)
  }
  if (filtros?.hasta) {
    results = results.filter(r => r.timestamp <= filtros.hasta!)
  }

  results.reverse() // newest first

  const skip = filtros?.skip ?? 0
  const limit = filtros?.limit ?? 50
  return results.slice(skip, skip + limit)
}

export async function exportarLog(): Promise<string> {
  const logs = await obtenerLog({ limit: 10000 })
  return JSON.stringify(logs, null, 2)
}
