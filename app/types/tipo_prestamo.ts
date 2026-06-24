import type { Prestamo } from "./prestamo";

export type EstadoTipoPrestamo = "activo" | "inactivo";

export type TipoPrestamo = {
  id: number;
  nombre: string;
  descripcion?: string;
  interes_mensual?: number;
  max_cuotas?: number;
  estado: EstadoTipoPrestamo;
  prestamos?: Prestamo[];
};