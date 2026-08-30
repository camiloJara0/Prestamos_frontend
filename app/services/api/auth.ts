import type { AuthRefreshResponse, AuthTokenResponse, LoginPayload, RespuestaLogout } from '#shared/types/auth'
import type { UsuarioMe } from '#shared/types/usuario'

export function loginRequest(payload: LoginPayload) {
  return useApi().apiPost<AuthTokenResponse>('/auth/login', payload, { retry: false })
}

export function refreshRequest(refreshToken: string) {
  return useApi().apiPost<AuthRefreshResponse>('/auth/refresh', { refresh_token: refreshToken }, { retry: false })
}

export function meRequest() {
  return useApi().apiGet<UsuarioMe>('/auth/me')
}

export function logoutRequest() {
  return useApi().apiPost<RespuestaLogout>('/auth/logout', undefined, { retry: false })
}
