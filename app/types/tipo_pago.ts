import type { Pago } from "./pago";

export type TipoPago = {
  id: number;
  nombre: string;
  descripcion?: string;
  pagos?: Pago[];
};