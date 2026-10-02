export interface PushSubscription {
  endpoint: string
  p256dh: string
  auth: string
}

export const suscribirPush = async (data: PushSubscription) => {
  return useApi().apiPost<{ mensaje: string }>('/push/subscribe', data)
}

export const desuscribirPush = async (endpoint: string) => {
  return useApi().apiDelete<{ mensaje: string }>('/push/subscribe', { body: { endpoint } })
}
