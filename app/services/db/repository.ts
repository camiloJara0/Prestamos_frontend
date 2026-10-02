import { getDB } from './db'

const DEFAULT_TTL = 5 * 60 * 1000 // 5 minutes

export async function getCached<T>(store: string, key: string, ttlMs: number = DEFAULT_TTL): Promise<{ data: T | null, stale: boolean }> {
  const db = getDB()
  if (!db) return { data: null, stale: true }

  const cacheKey = `${store}:${key}`
  const entry = await db.cacheMeta.get(cacheKey)

  if (!entry) return { data: null, stale: true }

  const age = Date.now() - entry.timestamp
  if (age > ttlMs) {
    return { data: entry.data as T, stale: true }
  }

  return { data: entry.data as T, stale: false }
}

export async function setCache(store: string, key: string, data: unknown, ttlMs: number = DEFAULT_TTL): Promise<void> {
  const db = getDB()
  if (!db) return

  const cacheKey = `${store}:${key}`
  await db.cacheMeta.put({
    key: cacheKey,
    store,
    data,
    timestamp: Date.now(),
    ttl: ttlMs
  })
}

export async function fetchAndCache<T>(
  store: string,
  key: string,
  fnFetch: () => Promise<T>,
  ttlMs: number = DEFAULT_TTL
): Promise<{ data: T, stale: boolean }> {
  try {
    const data = await fnFetch()
    await setCache(store, key, data, ttlMs)
    return { data, stale: false }
  } catch {
    const cached = await getCached<T>(store, key, ttlMs * 10) // allow stale cache on error
    if (cached.data !== null) {
      return { data: cached.data, stale: true }
    }
    throw new Error('Sin conexión y sin datos en caché')
  }
}

export async function getLastSync(store: string): Promise<string | null> {
  const db = getDB()
  if (!db) return null
  const entry = await db.cacheMeta.get(`${store}:lastSync`)
  return entry ? new Date(entry.timestamp).toISOString() : null
}

export async function setLastSync(store: string): Promise<void> {
  await setCache(store, 'lastSync', true, Infinity)
}
