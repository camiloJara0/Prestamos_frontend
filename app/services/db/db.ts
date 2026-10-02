import Dexie, { type Table } from 'dexie'

export interface CacheMeta {
  key: string
  store: string
  data: unknown
  timestamp: number
  ttl: number
}

export interface OutboxItem {
  id: string
  tipo: string
  payload: unknown
  idempotencyKey: string | null
  estado: 'pending' | 'syncing' | 'synced' | 'conflict' | 'failed'
  intentos: number
  lastError: string | null
  createdAt: string
}

export interface AuditLog {
  id?: number
  timestamp: string
  accion: string
  entidad: string
  entidadId: number | null
  detalle: unknown
  usuario: string | null
}

export interface CobranzaNota {
  id?: number
  prestamoId: number
  fecha: string
  tipo: string
  contenido: string
  usuario: string | null
}

class LoanSoftDB extends Dexie {
  cacheMeta!: Table<CacheMeta>
  outbox!: Table<OutboxItem>
  auditLog!: Table<AuditLog>
  cobranzaNotas!: Table<CobranzaNota>

  constructor() {
    super('loansoft')
    this.version(1).stores({
      cacheMeta: 'key, store, timestamp',
      outbox: 'id, tipo, estado, createdAt',
      auditLog: '++id, timestamp, accion, entidad, entidadId',
      cobranzaNotas: '++id, prestamoId, fecha, tipo'
    })
  }
}

let dbInstance: LoanSoftDB | null = null

export function getDB(): LoanSoftDB | null {
  if (typeof window === 'undefined') return null
  if (!dbInstance) {
    dbInstance = new LoanSoftDB()
  }
  return dbInstance
}
