import type { Prestamo } from "./prestamo";
import type { Pago } from "./pago";

export type EstadoCuota = "pendiente" | "pagado" | "vencido" | "parcial";

export type PrestamoCuota = {
  id: number;
  prestamo_id: number;
  numero_cuota: number;
  fecha_vencimiento: string;
  valor_cuota: number;
  capital: number;
  interes: number;
  mora: number;
  estado: EstadoCuota;
  created_at: string;
  updated_at: string;
  prestamo?: Prestamo;
  pagos?: Pago[];
};