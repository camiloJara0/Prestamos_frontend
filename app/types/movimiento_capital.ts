export type TipoMovimiento = 
  | "inversion" 
  | "retiro" 
  | "prestamo_otorgado" 
  | "pago_recibido" 
  | "perdida";

export type MovimientoCapital = {
  id: number;
  tipo_movimiento: TipoMovimiento;
  descripcion?: string;
  valor: number;
  fecha: string;
  prestamo_id?: number;
  created_at: string;
};