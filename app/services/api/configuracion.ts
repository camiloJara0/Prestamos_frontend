import type { Configuracion } from '#shared/types/configuracion'

export const getConfiguraciones = async () => {
  return useApi().apiGet<Configuracion[]>('/configuracion/')
}

export const getConfiguracion = async (clave: string) => {
  return useApi().apiGet<Configuracion>(`/configuracion/${clave}`)
}

export const actualizarConfiguracion = async (clave: string, valor: string) => {
  return useApi().apiPut<Configuracion>(`/configuracion/${clave}`, { valor })
}
