export type PaginacionParams = {
  skip?: number
  limit?: number
}

export type ListadoResult<T> = {
  data: T[]
  total: number
}
