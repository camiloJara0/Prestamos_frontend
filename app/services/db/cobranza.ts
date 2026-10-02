import { getDB, type CobranzaNota } from './db'

export async function agregarNota(prestamoId: number, tipo: string, contenido: string): Promise<void> {
  const db = getDB()
  if (!db) return

  const auth = useAuthStore()
  await db.cobranzaNotas.add({
    prestamoId,
    fecha: new Date().toISOString(),
    tipo,
    contenido,
    usuario: auth.user?.email ?? null
  })
}

export async function obtenerNotas(prestamoId: number): Promise<CobranzaNota[]> {
  const db = getDB()
  if (!db) return []
  return db.cobranzaNotas
    .where('prestamoId')
    .equals(prestamoId)
    .reverse()
    .sortBy('fecha')
}

export async function eliminarNota(id: number): Promise<void> {
  const db = getDB()
  if (!db) return
  await db.cobranzaNotas.delete(id)
}
