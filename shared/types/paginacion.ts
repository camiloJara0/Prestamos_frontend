export type PaginacionParams = {
  page?: number
  limit?: number
}

export type RespuestaPaginada<T> = {
  items: T[]
  total: number
  page: number
  pages: number
  limit: number
}
