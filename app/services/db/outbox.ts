import { getDB, type OutboxItem } from './db'

export function createOutboxItem(tipo: string, payload: unknown): OutboxItem {
  return {
    id: crypto.randomUUID(),
    tipo,
    payload,
    idempotencyKey: crypto.randomUUID(),
    estado: 'pending',
    intentos: 0,
    lastError: null,
    createdAt: new Date().toISOString()
  }
}

export async function encolar(tipo: string, payload: unknown): Promise<OutboxItem> {
  const db = getDB()
  if (!db) throw new Error('IndexedDB no disponible')
  const item = createOutboxItem(tipo, payload)
  await db.outbox.add(item)
  return item
}

export async function getPendientes(): Promise<OutboxItem[]> {
  const db = getDB()
  if (!db) return []
  return db.outbox.where('estado').equals('pending').sortBy('createdAt')
}

export async function marcarSynced(id: string): Promise<void> {
  const db = getDB()
  if (!db) return
  await db.outbox.update(id, { estado: 'synced' })
}

export async function marcarConflict(id: string, error: string): Promise<void> {
  const db = getDB()
  if (!db) return
  await db.outbox.update(id, { estado: 'conflict', lastError: error })
}

export async function marcarFailed(id: string, error: string): Promise<void> {
  const db = getDB()
  if (!db) return
  await db.outbox.update(id, { estado: 'failed', lastError: error })
}

export async function incrementarIntentos(id: string): Promise<void> {
  const db = getDB()
  if (!db) return
  const item = await db.outbox.get(id)
  if (item) {
    await db.outbox.update(id, { intentos: item.intentos + 1 })
  }
}

export async function limpiarSynced(): Promise<void> {
  const db = getDB()
  if (!db) return
  await db.outbox.where('estado').equals('synced').delete()
}

export async function contarPendientes(): Promise<number> {
  const db = getDB()
  if (!db) return 0
  return db.outbox.where('estado').equals('pending').count()
}

export async function contarConflicto(): Promise<number> {
  const db = getDB()
  if (!db) return 0
  return db.outbox.where('estado').equals('conflict').count()
}
