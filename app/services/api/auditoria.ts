import type { Auditoria } from '#shared/types/auditoria'
import type { RespuestaPaginada } from '#shared/types/paginacion'

export const getAuditoria = async (page = 1, limit = 25) => {
  return useApi().apiGet<RespuestaPaginada<Auditoria>>('/auditoria/', { query: { page, limit } })
}

export const getAuditoriaPorTabla = async (tabla: string, page = 1, limit = 25) => {
  return useApi().apiGet<RespuestaPaginada<Auditoria>>(`/auditoria/tabla/${tabla}`, { query: { page, limit } })
}

export const getAuditoriaPorOperacion = async (operacion: string, page = 1, limit = 25) => {
  return useApi().apiGet<RespuestaPaginada<Auditoria>>(`/auditoria/operacion/${operacion}`, { query: { page, limit } })
}
