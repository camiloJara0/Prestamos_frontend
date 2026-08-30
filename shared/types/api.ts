export type ApiError = {
  status: number
  detail: string
  field?: string
}

export type ApiErrorRaw
  = | { detail?: string }
    | { mensaje?: string }
    | { message?: string }
    | string
    | undefined
