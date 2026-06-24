import type { Prestamo } from "./prestamo";
import type { Pago } from "./pago";

export type EstadoCliente = "activo" | "inactivo";

export type Cliente = {
  id: number;
  nombre: string;
  cedula: string;
  telefono?: string;
  direccion?: string;
  persona_referencia?: string;
  telefono_referencia?: string;
  observaciones?: string;
  estado: EstadoCliente;
  prestamos?: Prestamo[];
  pagos?: Pago[];
};