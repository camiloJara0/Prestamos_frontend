export type PrestamoRenovacion = {
  id: number;
  prestamo_anterior_id: number;
  prestamo_nuevo_id: number;
  fecha: string;
  observaciones?: string;
  created_at: string;
};