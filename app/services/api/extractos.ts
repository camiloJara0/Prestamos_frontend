import type { ResultadoImportacion } from '#shared/types/extracto'

export const importarExtracto = async (_archivo: File): Promise<ResultadoImportacion> => {
  await new Promise(resolve => setTimeout(resolve, 1500))

  return {
    cuotas_identificadas: [
      { cuota_id: 12, prestamo_id: 3, cliente_nombre: 'María García', cedula: '1234567890', fecha_pago: '2026-09-20', valor_pagado: 150000, estado: 'identificado' },
      { cuota_id: 8, prestamo_id: 5, cliente_nombre: 'Juan Pérez', cedula: '0987654321', fecha_pago: '2026-09-19', valor_pagado: 200000, estado: 'identificado' }
    ],
    pagos_aplicados: [],
    errores: [
      { fecha_pago: '2026-09-18', valor_pagado: 50000, estado: 'error', detalle: 'No se encontró cuota pendiente para este cliente' }
    ],
    pendientes_revision: [
      { fecha_pago: '2026-09-17', valor_pagado: 75000, estado: 'pendiente', detalle: 'Múltiples cuotas pendientes para este cliente' }
    ]
  }
}
