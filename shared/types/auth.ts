import type { UsuarioMe } from './usuario'

export type LoginPayload = {
  email: string
  password: string
}

export type AuthTokenResponse = {
  access_token: string
  refresh_token: string
  token_type: string
}

export type AuthRefreshResponse = {
  access_token: string
  token_type: string
}

export type Sesion = {
  accessToken: string
  refreshToken: string
  user: UsuarioMe
}

export type RespuestaLogout = {
  mensaje: string
}
