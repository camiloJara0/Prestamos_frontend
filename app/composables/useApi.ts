import type { ApiError } from '#shared/types/api'

export type ApiResponseType
  = 'arrayBuffer'
    | 'blob'
    | 'formData'
    | 'json'
    | 'text'
    | 'stream'

export interface ApiRequestOptions {
  retry?: boolean
  responseType?: ApiResponseType
  headers?: Record<string, string>
  query?: Record<string, string | number | boolean | null | undefined>
  body?: unknown
  method?: string
}

interface FetchErrorLike {
  status?: number
  statusCode?: number
  data?: unknown
}

const AUTH_PATHS = ['/auth/login', '/auth/refresh', '/auth/logout']

export function normalizeApiError(error: unknown): ApiError {
  const err = (error ?? {}) as FetchErrorLike
  const status = err.status || err.statusCode || 0
  const data = err.data

  let detail = 'Error inesperado'
  let field: string | undefined

  if (typeof data === 'string' && data.trim() !== '') {
    detail = data
  } else if (data && typeof data === 'object' && Array.isArray((data as Record<string, unknown>).detail)) {
    const first = ((data as Record<string, unknown>).detail as Record<string, unknown>[])[0]
    if (first) {
      detail = String(first.msg ?? detail)
      const loc = first.loc as unknown[] | undefined
      if (Array.isArray(loc) && loc.length > 1) field = String(loc[1])
    }
  } else if (data && typeof data === 'object') {
    const obj = data as Record<string, unknown>
    detail = String(obj.detail ?? obj.mensaje ?? obj.message ?? 'Error inesperado')
  } else if (typeof (error as Error)?.message === 'string') {
    detail = (error as Error).message
  }

  return field ? { status, detail, field } : { status, detail }
}

export function useApi() {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase

  let refreshing: Promise<string | null> | null = null

  async function refreshAccessToken(): Promise<string | null> {
    if (refreshing) return refreshing
    const auth = useAuthStore()
    refreshing = (async () => {
      try {
        await auth.refresh()
        return auth.accessToken
      } catch {
        return null
      } finally {
        refreshing = null
      }
    })()
    return refreshing
  }

  function buildHeaders(options: ApiRequestOptions, token?: string | null): Record<string, string> {
    const headers: Record<string, string> = { ...(options.headers ?? {}) }
    if (token) headers.Authorization = `Bearer ${token}`
    return headers
  }

  async function request<T>(path: string, options: ApiRequestOptions = {}): Promise<T> {
    const auth = useAuthStore()
    const { retry = true, responseType, ...fetchOptions } = options
    const isAuthPath = AUTH_PATHS.includes(path)

    const execute = (token?: string | null) =>
      $fetch<T>(path, {
        baseURL: apiBase,
        method: (fetchOptions.method ?? 'GET') as 'GET',
        headers: buildHeaders(options, token),
        query: fetchOptions.query,
        body: fetchOptions.body as Record<string, unknown> | BodyInit | null | undefined,
        responseType: (responseType ?? 'json') as 'json'
      })

    try {
      return await execute(auth.accessToken)
    } catch (error) {
      const status = (error as FetchErrorLike).status || (error as FetchErrorLike).statusCode

      if (status === 401 && retry && !isAuthPath) {
        const newToken = await refreshAccessToken()
        if (newToken) {
          try {
            return await execute(newToken)
          } catch (retryError) {
            const retryStatus = (retryError as FetchErrorLike).status || (retryError as FetchErrorLike).statusCode
            if (retryStatus === 401) {
              await auth.logout()
              if (import.meta.client) await navigateTo('/login')
            }
            throw normalizeApiError(retryError)
          }
        }
        await auth.logout()
        if (import.meta.client) await navigateTo('/login')
      }

      throw normalizeApiError(error)
    }
  }

  const apiGet = <T>(path: string, options: ApiRequestOptions = {}) =>
    request<T>(path, { ...options, method: 'GET' })

  const apiPost = <T>(path: string, body?: unknown, options: ApiRequestOptions = {}) =>
    request<T>(path, { ...options, method: 'POST', body })

  const apiPut = <T>(path: string, body?: unknown, options: ApiRequestOptions = {}) =>
    request<T>(path, { ...options, method: 'PUT', body })

  const apiDelete = <T>(path: string, options: ApiRequestOptions = {}) =>
    request<T>(path, { ...options, method: 'DELETE' })

  const apiDownload = (path: string, filename: string, options: ApiRequestOptions = {}) =>
    request<Blob>(path, { ...options, method: 'GET', responseType: 'blob' }).then((blob) => {
      if (!import.meta.client) return
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = filename
      link.click()
      URL.revokeObjectURL(url)
    })

  return { request, apiGet, apiPost, apiPut, apiDelete, apiDownload }
}

export type ApiClient = ReturnType<typeof useApi>
