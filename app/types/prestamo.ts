import type { Cliente } from "./clientes";
import type { PrestamoCuota } from "./prestamo_cuota";
import type { TipoPrestamo } from "./tipo_prestamo";
import type { Pago } from "./pago";

export type EstadoPrestamo = "activo" | "pagado" | "perdido" | "renovado";

export type Prestamo = {
  id: number;
  cliente_id: number;
  tipo_prestamo_id: number;
  fecha_prestamo: string;
  capital_prestado: number;
  porcentaje_interes: number;
  interes_total: number;
  monto_total: number;
  numero_cuotas: number;
  valor_cuota: number;
  saldo_pendiente: number;
  estado: EstadoPrestamo;
  observaciones?: string;
  cliente?: Cliente;
  tipo_prestamo?: TipoPrestamo;
  cuotas?: PrestamoCuota[];
  pagos?: Pago[];
};