import type { Prestamo } from "./prestamo";
import type { Cliente } from "./clientes";
import type { PrestamoCuota } from "./prestamo_cuota";
import type { TipoPago } from "./tipo_pago";

export type Pago = {
  id: number;
  prestamo_id: number;
  cliente_id: number;
  cuota_id: number;
  tipo_pago_id: number;
  fecha_pago: string;
  valor_pagado: number;
  capital_pagado: number;
  interes_pagado: number;
  mora_pagada: number;
  observaciones?: string;
  created_at: string;
  updated_at: string;
  prestamo?: Prestamo;
  cliente?: Cliente;
  cuota?: PrestamoCuota;
  tipo_pago?: TipoPago;
};