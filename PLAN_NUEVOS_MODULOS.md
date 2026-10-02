# Plan de Integración — LoanSoft: Nuevos Módulos

**Fecha:** 2026-09-23
**Stack:** Nuxt 4, Vue 3, TypeScript, Pinia, Nuxt UI v4, Tailwind v4, Dexie, zod

---

## Resumen Ejecutivo

| # | Módulo | Descripción | Fases |
|---|--------|-------------|-------|
| 1 | **Estadísticas de Cliente** | Frecuencia de pago, identificación de morosos, dashboard por cliente | 3 fases |
| 2 | **Agenda** | Calendario de préstamos, recogidas, citas personalizadas | 4 fases |
| 3 | **Recordatorios y Notificaciones** | Notificaciones del sistema, recordatorios personalizados | 3 fases |
| 4 | **Solicitudes de Préstamo** | Simulación, envío de solicitud, flujo de aceptación | 4 fases |

**Backend requerido:** Cada módulo incluye los endpoints que el backend debe proveer.
**Total estimado:** 14 fases de implementación.

---

## Módulo 1: Estadísticas de Cliente

### Objetivo
Mostrar en el módulo de clientes: frecuencia de pago mes a mes, identificación de clientes que suelen demorarse, y un mini-dashboard por cliente.

### Fase 1.1: Types y servicio de estadísticas

**Archivos a crear:**

```
shared/types/estadisticas_cliente.ts
app/services/api/estadisticas_cliente.ts
```

**Types:**

```typescript
// shared/types/estadisticas_cliente.ts

export type FrecuenciaPago = {
  mes: string           // "2026-01", "2026-02", ...
  prestamos_activos: number
  pagos_realizados: number
  monto_pagado: number
  cuotas_pagadas: number
  cuotas_pendientes: number
}

export type ComportamientoPago = {
  cliente_id: number
  cliente_nombre: string
  promedio_dias_pago: number      // Promedio de días después del vencimiento
  total_pagos: number
  pagos_a_tiempo: number          // Pagos antes o el día de vencimiento
  pagos_tardios: number           // Pagos después del vencimiento
  porcentaje_puntualidad: number  // 0-100
  estado_riesgo: 'bueno' | 'regular' | 'riesgoso'
}

export type EstadisticasCliente = {
  cliente_id: number
  total_prestamos: number
  prestamos_activos: number
  prestamos_pagados: number
  prestamos_perdidos: number
  monto_total_prestado: number
  monto_total_pagado: number
  saldo_pendiente: number
  frecuencia_pago: FrecuenciaPago[]
  comportamiento: ComportamientoPago
  ultimo_pago_fecha: string | null
  proxima_cuota_fecha: string | null
}
```

**Endpoints backend:**

```
GET /clientes/{id}/estadisticas
GET /clientes/{id}/frecuencia-pago?meses=12
GET /clientes/comportamiento          // Retorna todos los clientes con su comportamiento
```

**Servicio:**

```typescript
// app/services/api/estadisticas_cliente.ts

export const getEstadisticasCliente = async (clienteId: number): Promise<EstadisticasCliente> => {
  return useApi().apiGet(`/clientes/${clienteId}/estadisticas`)
}

export const getFrecuenciaPago = async (clienteId: number, meses = 12): Promise<FrecuenciaPago[]> => {
  return useApi().apiGet(`/clientes/${clienteId}/frecuencia-pago`, { query: { meses } })
}

export const getComportamientoClientes = async (): Promise<ComportamientoPago[]> => {
  return useApi().apiGet('/clientes/comportamiento')
}
```

### Fase 1.2: Composable y vista de detalle de cliente

**Archivos a crear/Modificar:**

```
app/composables/domain/useEstadisticasCliente.ts    (crear)
app/pages/clientes/[id].vue                          (crear)
app/components/clientes/ClienteEstadisticas.vue      (crear)
app/components/clientes/ClienteFrecuencia.vue        (crear)
```

**Composable:**

```typescript
// app/composables/domain/useEstadisticasCliente.ts

export function useEstadisticasCliente(clienteId: Ref<number>) {
  const estadisticas = ref<EstadisticasCliente | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetch() { ... }
  async function fetchFrecuencia(meses?: number) { ... }

  watch(clienteId, () => { fetch() }, { immediate: true })

  return { estadisticas, loading, error, fetch, fetchFrecuencia }
}
```

**Página de detalle de cliente (`/clientes/[id]`):**

- Header con nombre, cédula, estado
- 4-6 StatCards: Total préstamos, Activos, Monto total prestado, Saldo pendiente, % Puntualidad, Estado de riesgo
- Tab "Frecuencia de pago" → gráfico de barras mensual (cuotas pagadas vs pendientes por mes)
- Tab "Préstamos" → lista de préstamos del cliente
- Tab "Comportamiento" → indicador visual de riesgo, días promedio de pago, historial

### Fase 1.3: Identificación de clientes morosos (vista global)

**Archivos a crear/Modificar:**

```
app/components/clientes/ClientesComportamiento.vue   (crear)
app/pages/clientes/index.vue                         (modificar)
```

**Modificación en clientes/index.vue:**

- Agregar botón "Comportamiento" en el header
- Al hacer clic, abrir modal o panel lateral que muestre:
  - Tabla de clientes ordenada por `porcentaje_puntualidad` ascendente
  - Columnas: Cliente, Cédula, Promedio días pago, % Puntualidad, Estado de riesgo (badge: bueno/regular/riesgoso)
  - Filtro por estado de riesgo
  - Exportar a CSV

---

## Módulo 2: Agenda

### Objetivo
Crear un módulo de calendario/agenda para visualizar préstamos por fechas de vencimiento, agendar recogidas de dinero, y gestionar tipos de citas personalizados.

### Fase 2.1: Types y servicio de agenda

**Archivos a crear:**

```
shared/types/agenda.ts
app/services/api/agenda.ts
```

**Types:**

```typescript
// shared/types/agenda.ts

export type TipoEvento = 'cuota_vence' | 'recogida' | 'cita' | 'seguimiento' | 'otro'

export type EstadoEvento = 'pendiente' | 'completado' | 'cancelado' | 'vencido'

export type TipoCita = {
  id: number
  nombre: string
  descripcion: string | null
  color: string            // Hex color para el calendario
  duracion_minutos: number
  estado: 'activo' | 'inactivo'
}

export type EventoAgenda = {
  id: number
  tipo: TipoEvento
  titulo: string
  descripcion: string | null
  fecha: string            // YYYY-MM-DD
  hora_inicio: string | null   // HH:MM
  hora_fin: string | null      // HH:MM
  prestamo_id: number | null
  cliente_id: number | null
  cliente_nombre: string | null
  tipo_cita_id: number | null
  estado: EstadoEvento
  observaciones: string | null
  created_at: string
}

export type EventoAgendaCreate = {
  tipo: TipoEvento
  titulo: string
  descripcion?: string | null
  fecha: string
  hora_inicio?: string | null
  hora_fin?: string | null
  prestamo_id?: number | null
  cliente_id?: number | null
  tipo_cita_id?: number | null
  observaciones?: string | null
}

export type VistaCalendario = 'dia' | 'semana' | 'mes'
```

**Endpoints backend:**

```
GET    /agenda/eventos?fecha_desde=&fecha_hasta=&tipo=&estado=
POST   /agenda/eventos
PUT    /agenda/eventos/{id}
DELETE /agenda/eventos/{id}
PATCH  /agenda/eventos/{id}/completar

GET    /agenda/tipos-cita
POST   /agenda/tipos-cita
PUT    /agenda/tipos-cita/{id}
DELETE /agenda/tipos-cita/{id}

GET    /agenda/resumen?fecha=&mes=    // Eventos del día/resumen del mes
```

**Servicio:**

```typescript
// app/services/api/agenda.ts

export const getEventosAgenda = async (params: {
  fecha_desde?: string
  fecha_hasta?: string
  tipo?: TipoEvento
  estado?: EstadoEvento
}): Promise<EventoAgenda[]> => {
  return useApi().apiGet('/agenda/eventos', { query: params })
}

export const crearEvento = async (data: EventoAgendaCreate): Promise<EventoAgenda> => {
  return useApi().apiPost('/agenda/eventos', data)
}

export const actualizarEvento = async (id: number, data: Partial<EventoAgendaCreate>): Promise<EventoAgenda> => {
  return useApi().apiPut(`/agenda/eventos/${id}`, data)
}

export const eliminarEvento = async (id: number): Promise<void> => {
  return useApi().apiDelete(`/agenda/eventos/${id}`)
}

export const completarEvento = async (id: number): Promise<EventoAgenda> => {
  return useApi().apiPatch(`/agenda/eventos/${id}/completar`, {})
}

// Tipos de cita
export const getTiposCita = async (): Promise<TipoCita[]> => {
  return useApi().apiGet('/agenda/tipos-cita')
}

export const crearTipoCita = async (data: Omit<TipoCita, 'id' | 'estado'>): Promise<TipoCita> => {
  return useApi().apiPost('/agenda/tipos-cita', data)
}

export const actualizarTipoCita = async (id: number, data: Partial<TipoCita>): Promise<TipoCita> => {
  return useApi().apiPut(`/agenda/tipos-cita/${id}`, data)
}

export const eliminarTipoCita = async (id: number): Promise<void> => {
  return useApi().apiDelete(`/agenda/tipos-cita/${id}`)
}
```

### Fase 2.2: Composable y componente de calendario

**Archivos a crear:**

```
app/composables/domain/useAgenda.ts
app/components/agenda/CalendarioMensual.vue
app/components/agenda/CalendarioSemanal.vue
app/components/agenda/ListaEventos.vue
app/components/agenda/EventoCard.vue
app/components/agenda/EventoModal.vue
```

**Composable:**

```typescript
// app/composables/domain/useAgenda.ts

export function useAgenda() {
  const eventos = ref<EventoAgenda[]>([])
  const tiposCita = ref<TipoCita[]>([])
  const loading = ref(false)
  const vista = ref<VistaCalendario>('semana')
  const fechaSeleccionada = ref(new Date().toISOString().split('T')[0])

  // Filtros activos
  const filtros = ref<{ tipo?: TipoEvento, estado?: EstadoEvento }>({})

  async function fetchEventos(fechaDesde?: string, fechaHasta?: string) { ... }
  async function crear(data: EventoAgendaCreate) { ... }
  async function actualizar(id: number, data: Partial<EventoAgendaCreate>) { ... }
  async function eliminar(id: number) { ... }
  async function completar(id: number) { ... }
  async function fetchTiposCita() { ... }
  async function crearTipoCita(data: ...) { ... }

  // Eventos del día seleccionado
  const eventosDelDia = computed(() => {
    return eventos.value.filter(e => e.fecha === fechaSeleccionada.value)
  })

  // Eventos agrupados por fecha (para vista mensual)
  const eventosPorFecha = computed(() => {
    const map = new Map<string, EventoAgenda[]>()
    for (const evento of eventos.value) {
      const existing = map.get(evento.fecha) ?? []
      existing.push(evento)
      map.set(evento.fecha, existing)
    }
    return map
  })

  return {
    eventos, tiposCita, loading, vista, fechaSeleccionada,
    filtros, eventosDelDia, eventosPorFecha,
    fetchEventos, crear, actualizar, eliminar, completar,
    fetchTiposCita, crearTipoCita
  }
}
```

**Componente CalendarioMensual.vue:**

- Grid de 7 columnas (Lun-Dom)
- Cada celda muestra el día y los eventos (puntos de color o mini-badges)
- Click en día → seleccionar fecha, mostrar eventos del día en panel lateral
- Hover sobre evento → tooltip con detalles
- Colores por tipo de evento:
  - Cuota vence: azul
  - Recogida: verde
  - Cita: morado
  - Seguimiento: naranja
  - Otro: gris

**Componente EventoModal.vue:**

- Modal para crear/editar evento
- Campos: tipo (select), título, descripción, fecha, hora inicio/fin, cliente (select con búsqueda), préstamo (select si cliente seleccionado), tipo de cita (select), observaciones
- Validación con zod

### Fase 2.3: Página de agenda

**Archivos a crear/Modificar:**

```
app/pages/agenda/index.vue                       (crear)
app/components/Layout/Aside.vue                  (modificar - agregar a nav)
app/components/app/CommandPalette.vue            (modificar - agregar atajo)
```

**Página `/agenda/index.vue`:**

- PageHeader con título "Agenda" + botón "Nuevo evento"
- Barra de herramientas:
  - Selector de vista (Día / Semana / Mes)
  - Navegación de fecha (← Semana/Mes →)
  - Selector de tipo de evento (filtro)
  - Botón "Gestionar tipos de cita"
- Vista principal:
  - CalendarioMensual o CalendarioSemanal según selección
  - Panel lateral derecho: ListaEventos del día seleccionado
- Modal EventoModal para crear/editar

**Navegación:**

- Agregar "Agenda" a la sección "Gestión" del sidebar (junto a Préstamos, Clientes, Cobranza, Reportes)
- Icono: `i-lucide-calendar`
- Ruta: `/agenda`

### Fase 2.4: Auto-generación de eventos de cuotas

**Funcionalidad:**

- Cuando se crea un préstamo, auto-generar eventos de tipo `cuota_vence` para cada cuota
- Endpoint backend: `POST /prestamos/{id}/generar-eventos-agenda`
- Endpoint frontend en `app/services/api/prestamo.ts`:

```typescript
export const generarEventosAgenda = async (prestamoId: number): Promise<void> => {
  return useApi().apiPost(`/prestamos/${prestamoId}/generar-eventos-agenda`, {})
}
```

- Llamar después de crear préstamo (en `PrestamoModalCrear.vue` o en el servicio)

---

## Módulo 3: Recordatorios y Notificaciones

### Objetivo
Sistema de notificaciones del sistema (moras, vencimientos) + recordatorios personalizados por prestamista.

### Fase 3.1: Types y servicio

**Archivos a crear:**

```
shared/types/notificacion.ts
app/services/api/notificaciones.ts
```

**Types:**

```typescript
// shared/types/notificacion.ts

export type TipoNotificacion = 'mora' | 'vencimiento' | 'pago_recibido' | 'prestamo_aprobado' | 'sistema' | 'recordatorio'

export type PrioridadNotificacion = 'baja' | 'normal' | 'alta' | 'urgente'

export type Notificacion = {
  id: number
  usuario_id: number
  tipo: TipoNotificacion
  titulo: string
  mensaje: string
  prioridad: PrioridadNotificacion
  leida: boolean
  entidad_tipo: string | null     // 'prestamo', 'cliente', 'pago', etc.
  entidad_id: number | null
  created_at: string
}

export type Recordatorio = {
  id: number
  usuario_id: number
  titulo: string
  descripcion: string | null
  fecha_programada: string        // YYYY-MM-DD
  hora_programada: string | null  // HH:MM
  repetir: 'no' | 'diario' | 'semanal' | 'mensual'
  estado: 'pendiente' | 'completado' | 'cancelado'
  prestamo_id: number | null
  cliente_id: number | null
  created_at: string
}

export type RecordatorioCreate = {
  titulo: string
  descripcion?: string | null
  fecha_programada: string
  hora_programada?: string | null
  repetir?: 'no' | 'diario' | 'semanal' | 'mensual'
  prestamo_id?: number | null
  cliente_id?: number | null
}

export type StatsNotificaciones = {
  total_no_leidas: number
  por_tipo: Record<TipoNotificacion, number>
}
```

**Endpoints backend:**

```
GET    /notificaciones?leida=&tipo=&skip=&limit=
GET    /notificaciones/stats
PATCH  /notificaciones/{id}/leer
PATCH  /notificaciones/leer-todas
DELETE /notificaciones/{id}

GET    /recordatorios?estado=&fecha_desde=&fecha_hasta=
POST   /recordatorios
PUT    /recordatorios/{id}
DELETE /recordatorios/{id}
PATCH  /recordatorios/{id}/completar
```

**Servicio:**

```typescript
// app/services/api/notificaciones.ts

// Notificaciones del sistema
export const getNotificaciones = async (params: {
  leida?: boolean
  tipo?: TipoNotificacion
  skip?: number
  limit?: number
}): Promise<Notificacion[]> => {
  return useApi().apiGet('/notificaciones', { query: params })
}

export const getStatsNotificaciones = async (): Promise<StatsNotificaciones> => {
  return useApi().apiGet('/notificaciones/stats')
}

export const marcarLeida = async (id: number): Promise<void> => {
  return useApi().apiPatch(`/notificaciones/${id}/leer`, {})
}

export const marcarTodasLeidas = async (): Promise<void> => {
  return useApi().apiPatch('/notificaciones/leer-todas', {})
}

export const eliminarNotificacion = async (id: number): Promise<void> => {
  return useApi().apiDelete(`/notificaciones/${id}`)
}

// Recordatorios personalizados
export const getRecordatorios = async (params: {
  estado?: string
  fecha_desde?: string
  fecha_hasta?: string
}): Promise<Recordatorio[]> => {
  return useApi().apiGet('/recordatorios', { query: params })
}

export const crearRecordatorio = async (data: RecordatorioCreate): Promise<Recordatorio> => {
  return useApi().apiPost('/recordatorios', data)
}

export const actualizarRecordatorio = async (id: number, data: Partial<RecordatorioCreate>): Promise<Recordatorio> => {
  return useApi().apiPut(`/recordatorios/${id}`, data)
}

export const eliminarRecordatorio = async (id: number): Promise<void> => {
  return useApi().apiDelete(`/recordatorios/${id}`)
}

export const completarRecordatorio = async (id: number): Promise<Recordatorio> => {
  return useApi().apiPatch(`/recordatorios/${id}/completar`, {})
}
```

### Fase 3.2: Composable de notificaciones

**Archivos a crear:**

```
app/composables/useNotificaciones.ts
```

**Composable:**

```typescript
// app/composables/useNotificaciones.ts

export function useNotificaciones() {
  const notificaciones = ref<Notificacion[]>([])
  const stats = ref<StatsNotificaciones | null>(null)
  const recordatorios = ref<Recordatorio[]>([])
  const loading = ref(false)
  const noLeidas = computed(() => stats.value?.total_no_leidas ?? 0)

  async function fetchNotificaciones(params?) { ... }
  async function fetchStats() { ... }
  async function marcarLeida(id: number) { ... }
  async function marcarTodasLeidas() { ... }

  async function fetchRecordatorios(params?) { ... }
  async function crearRecordatorio(data: RecordatorioCreate) { ... }
  async function completarRecordatorio(id: number) { ... }

  // Polling cada 30 segundos para nuevas notificaciones
  let pollingInterval: ReturnType<typeof setInterval> | null = null
  function iniciarPolling() {
    pollingInterval = setInterval(() => {
      fetchStats()
    }, 30000)
  }
  function detenerPolling() {
    if (pollingInterval) clearInterval(pollingInterval)
  }

  onMounted(iniciarPolling)
  onUnmounted(detenerPolling)

  return {
    notificaciones, stats, recordatorios, loading, noLeidas,
    fetchNotificaciones, fetchStats, marcarLeida, marcarTodasLeidas,
    fetchRecordatorios, crearRecordatorio, completarRecordatorio
  }
}
```

### Fase 3.3: UI de notificaciones y recordatorios

**Archivos a crear/Modificar:**

```
app/components/app/NotificacionesPanel.vue           (crear)
app/components/app/NotificacionBell.vue              (crear)
app/components/app/RecordatorioModal.vue             (crear)
app/components/app/RecordatoriosPanel.vue            (crear)
app/components/app/AppHeader.vue                     (modificar)
app/pages/perfil.vue                                 (modificar)
```

**NotificacionBell.vue (en el header):**

- Botón de campana con badge del conteo de no leídas
- Click → abre NotificacionesPanel (dropdown o slide-over)
- Animación de pulso cuando hay notificaciones urgentes

**NotificacionesPanel.vue:**

- Lista de notificaciones recientes (últimas 20)
- Cada notificación: icono por tipo, título, mensaje, timestamp relativo, indicador de leída/no leída
- Click → marcar como leída + navegar a la entidad relacionada (si existe)
- Botón "Marcar todas como leídas"
- Botón "Ver todas" → página completa de notificaciones
- Separador: "Recordatorios" con lista de recordatorios próximos

**RecordatorioModal.vue:**

- Modal para crear/editar recordatorio
- Campos: título*, descripción, fecha programada*, hora programada, repetir (select: no/diario/semanal/mensual), cliente (select), préstamo (select)

**Página de notificaciones (opcional, integrar en `/perfil` o ruta dedicada):**

- En `/perfil`: agregar sección "Notificaciones y recordatorios"
- Tab "Notificaciones": lista completa con filtros por tipo y estado
- Tab "Recordatorios": lista de recordatorios con crear/editar/eliminar

### Fase 3.4: Integración con push para notificaciones automáticas

**Modificaciones:**

```
app/composables/usePushNotifications.ts    (modificar)
app/services/api/push.ts                   (modificar)
```

- Cuando se recibe una notificación de tipo `mora` o `vencimiento`, mostrar notificación del navegador (si push está habilitado)
- Usar la API de notificaciones del navegador como fallback cuando push no está soportado
- Endpoint backend adicional:

```
POST /notificaciones/crear-automatica
Body: { tipo, titulo, mensaje, prioridad, usuario_id?, entidad_tipo?, entidad_id? }
```

---

## Módulo 4: Solicitudes de Préstamo

### Objetivo
Página pública/semipública donde los clientes de prestamistas pueden: ver planes de préstamo, simular crédito, y enviar solicitud de préstamo. Al aceptar, se crea cliente + préstamo automáticamente.

### Fase 4.1: Types y servicio

**Archivos a crear:**

```
shared/types/solicitud.ts
app/services/api/solicitudes.ts
```

**Types:**

```typescript
// shared/types/solicitud.ts

export type EstadoSolicitud = 'pendiente' | 'aprobada' | 'rechazada' | 'expirada'

export type SolicitudPrestamo = {
  id: number
  cliente_id: number | null          // null si el cliente aún no existe
  cliente_nombre: string
  cliente_cedula: string
  cliente_telefono: string | null
  cliente_email: string | null
  tipo_prestamo_id: number
  tipo_prestamo_nombre: string
  capital_solicitado: number
  porcentaje_interes: number
  numero_cuotas: number
  valor_cuota_estimado: number
  monto_total_estimado: number
  estado: EstadoSolicitud
  observaciones: string | null
  prestamo_creado_id: number | null  // ID del préstamo creado al aprobar
  created_at: string
  updated_at: string
}

export type SolicitudPrestamoCreate = {
  cliente_nombre: string
  cliente_cedula: string
  cliente_telefono?: string | null
  cliente_email?: string | null
  tipo_prestamo_id: number
  capital_solicitado: number
  porcentaje_interes: number
  numero_cuotas: number
  observaciones?: string | null
}

export type SimulacionCredito = {
  tipo_prestamo_id: number
  tipo_prestamo_nombre: string
  capital_solicitado: number
  porcentaje_interes: number
  numero_cuotas: number
  interes_total: number
  monto_total: number
  valor_cuota: number
  fecha_primera_cuota: string
}
```

**Endpoints backend:**

```
GET    /solicitudes?estado=&skip=&limit=
GET    /solicitudes/{id}
POST   /solicitudes                    // Enviar solicitud (público o con token)
PATCH  /solicitudes/{id}/aprobar       // Admin: aprobar → crea cliente + préstamo
PATCH  /solicitudes/{id}/rechazar      // Admin: rechazar
GET    /solicitudes/simular            // Simulación (cálculo server-side)

GET    /planes-prestamo                // Público: tipos de préstamo activos
```

**Servicio:**

```typescript
// app/services/api/solicitudes.ts

export const getSolicitudes = async (params: {
  estado?: EstadoSolicitud
  skip?: number
  limit?: number
}): Promise<SolicitudPrestamo[]> => {
  return useApi().apiGet('/solicitudes', { query: params })
}

export const getSolicitudById = async (id: number): Promise<SolicitudPrestamo> => {
  return useApi().apiGet(`/solicitudes/${id}`)
}

export const crearSolicitud = async (data: SolicitudPrestamoCreate): Promise<SolicitudPrestamo> => {
  return useApi().apiPost('/solicitudes', data)
}

export const aprobarSolicitud = async (id: number): Promise<{ prestamo_id: number }> => {
  return useApi().apiPatch(`/solicitudes/${id}/aprobar`, {})
}

export const rechazarSolicitud = async (id: number, motivo?: string): Promise<void> => {
  return useApi().apiPatch(`/solicitudes/${id}/rechazar`, { motivo })
}

export const simularCredito = async (params: {
  tipo_prestamo_id: number
  capital_solicitado: number
  porcentaje_interes: number
  numero_cuotas: number
}): Promise<SimulacionCredito> => {
  return useApi().apiGet('/solicitudes/simular', { query: params })
}

export const getPlanesPrestamo = async (): Promise<TipoPrestamo[]> => {
  return useApi().apiGet('/planes-prestamo')
}
```

### Fase 4.2: Página pública de solicitud de préstamo

**Archivos a crear:**

```
app/pages/solicitud/index.vue                         (crear - pública)
app/components/solicitud/SimuladorCredito.vue         (crear)
app/components/solicitud/FormularioSolicitud.vue      (crear)
app/components/solicitud/PlanesPrestamo.vue           (crear)
app/pages/solicitud/exito.vue                         (crear - post-envío)
```

**Página `/solicitud/index.vue` (pública, sin auth):**

- Layout: auth (fondo gradiente) o layout dedicado
- Sección 1: Hero con título "Solicita tu préstamo" + descripción
- Sección 2: PlanesPrestamo - cards con los tipos de préstamo activos (nombre, descripción, interés, máx cuotas)
- Sección 3: SimuladorCredito - formulario interactivo:
  - Select de tipo de préstamo
  - Input de capital solicitado (con MoneyInput)
  - Input de número de cuotas (con slider o input numérico)
  - Cálculo en tiempo real: interés total, monto total, valor cuota, fecha primera cuota
  - Botón "Solicitar préstamo"
- Sección 4: FormularioSolicitud - si se hace clic en "Solicitar":
  - Campos: nombre*, cédula*, teléfono, email, observaciones
  - Validación con zod
  - Submit → `crearSolicitud()` → redirigir a `/solicitud/exito`

**Página `/solicitud/exito.vue`:**

- Mensaje de éxito: "Tu solicitud ha sido enviada"
- Detalles de la solicitud: tipo, capital, cuotas, valor cuota
- "Serás contactado pronto"

### Fase 4.3: Panel de administración de solicitudes

**Archivos a crear/Modificar:**

```
app/pages/solicitudes/index.vue                      (crear - admin)
app/components/solicitud/SolicitudDetalle.vue        (crear)
app/components/Layout/Aside.vue                      (modificar)
app/components/app/CommandPalette.vue                (modificar)
```

**Página `/solicitudes/index.vue` (admin):**

- PageHeader: "Solicitudes de préstamo" + stats (pendientes, aprobadas, rechazadas)
- DataTable con filtros por estado
- Columnas: ID, Cliente, Cédula, Tipo préstamo, Capital, Cuotas, Valor cuota, Estado (badge), Fecha, Acciones
- Acciones:
  - Ver detalle → modal SolicitudDetalle
  - Aprobar → confirmación → `aprobarSolicitud()` → crea préstamo automáticamente
  - Rechazar → modal con motivo → `rechazarSolicitud()`
- Badge de estado: pendiente (amarillo), aprobada (verde), rechazada (rojo), expirada (gris)

**Componente SolicitudDetalle.vue:**

- Información del cliente (nombre, cédula, teléfono, email)
- Detalle de la solicitud (tipo préstamo, capital, interés, cuotas, valor cuota)
- Si se aprueba: se crea automáticamente:
  1. Cliente (si no existe con esa cédula)
  2. Préstamo con los datos de la solicitud
  3. Notificación al admin de préstamo creado

**Navegación:**

- Agregar "Solicitudes" a la sección "Gestión" del sidebar (solo admin)
- Icono: `i-lucide-file-text`
- Badge con conteo de solicitudes pendientes

---

## Resumen de endpoints backend requeridos

### Módulo 1: Estadísticas de Cliente
```
GET  /clientes/{id}/estadisticas
GET  /clientes/{id}/frecuencia-pago?meses=12
GET  /clientes/comportamiento
```

### Módulo 2: Agenda
```
GET    /agenda/eventos
POST   /agenda/eventos
PUT    /agenda/eventos/{id}
DELETE /agenda/eventos/{id}
PATCH  /agenda/eventos/{id}/completar
GET    /agenda/tipos-cita
POST   /agenda/tipos-cita
PUT    /agenda/tipos-cita/{id}
DELETE /agenda/tipos-cita/{id}
POST   /prestamos/{id}/generar-eventos-agenda
```

### Módulo 3: Notificaciones y Recordatorios
```
GET    /notificaciones
GET    /notificaciones/stats
PATCH  /notificaciones/{id}/leer
PATCH  /notificaciones/leer-todas
DELETE /notificaciones/{id}
GET    /recordatorios
POST   /recordatorios
PUT    /recordatorios/{id}
DELETE /recordatorios/{id}
PATCH  /recordatorios/{id}/completar
POST   /notificaciones/crear-automatica
```

### Módulo 4: Solicitudes de Préstamo
```
GET    /solicitudes
GET    /solicitudes/{id}
POST   /solicitudes
PATCH  /solicitudes/{id}/aprobar
PATCH  /solicitudes/{id}/rechazar
GET    /solicitudes/simular
GET    /planes-prestamo
```

---

## Orden de implementación recomendado

| Fase | Módulo | Descripción | Dependencias |
|------|--------|-------------|--------------|
| 1.1 | Estadísticas Cliente | Types y servicio | Ninguna |
| 1.2 | Estadísticas Cliente | Composable y vista detalle | 1.1 |
| 1.3 | Estadísticas Cliente | Clientes morosos (vista global) | 1.1 |
| 2.1 | Agenda | Types y servicio | Ninguna |
| 2.2 | Agenda | Composable y calendario | 2.1 |
| 2.3 | Agenda | Página de agenda | 2.2 |
| 2.4 | Agenda | Auto-generar eventos de cuotas | 2.1, backend |
| 3.1 | Notificaciones | Types y servicio | Ninguna |
| 3.2 | Notificaciones | Composable | 3.1 |
| 3.3 | Notificaciones | UI notificaciones y recordatorios | 3.2 |
| 3.4 | Notificaciones | Integración push automática | 3.2, 3.3 |
| 4.1 | Solicitudes | Types y servicio | Ninguna |
| 4.2 | Solicitudes | Página pública de solicitud | 4.1 |
| 4.3 | Solicitudes | Panel admin de solicitudes | 4.1 |

---

## Archivos a crear (resumen)

### Types (4 archivos)
- `shared/types/estadisticas_cliente.ts`
- `shared/types/agenda.ts`
- `shared/types/notificacion.ts`
- `shared/types/solicitud.ts`

### Servicios (4 archivos)
- `app/services/api/estadisticas_cliente.ts`
- `app/services/api/agenda.ts`
- `app/services/api/notificaciones.ts`
- `app/services/api/solicitudes.ts`

### Composables (4 archivos)
- `app/composables/domain/useEstadisticasCliente.ts`
- `app/composables/domain/useAgenda.ts`
- `app/composables/useNotificaciones.ts`
- `app/composables/domain/useSolicitudes.ts`

### Componentes (~20 archivos)
- `app/components/clientes/ClienteEstadisticas.vue`
- `app/components/clientes/ClienteFrecuencia.vue`
- `app/components/clientes/ClientesComportamiento.vue`
- `app/components/agenda/CalendarioMensual.vue`
- `app/components/agenda/CalendarioSemanal.vue`
- `app/components/agenda/ListaEventos.vue`
- `app/components/agenda/EventoCard.vue`
- `app/components/agenda/EventoModal.vue`
- `app/components/agenda/TipoCitaModal.vue`
- `app/components/app/NotificacionesPanel.vue`
- `app/components/app/NotificacionBell.vue`
- `app/components/app/RecordatorioModal.vue`
- `app/components/app/RecordatoriosPanel.vue`
- `app/components/solicitud/SimuladorCredito.vue`
- `app/components/solicitud/FormularioSolicitud.vue`
- `app/components/solicitud/PlanesPrestamo.vue`
- `app/components/solicitud/SolicitudDetalle.vue`

### Páginas (5 archivos)
- `app/pages/clientes/[id].vue`
- `app/pages/agenda/index.vue`
- `app/pages/solicitudes/index.vue`
- `app/pages/solicitud/index.vue` (pública)
- `app/pages/solicitud/exito.vue`

### Archivos a modificar
- `app/components/Layout/Aside.vue` — agregar Agenda y Solicitudes al sidebar
- `app/components/app/CommandPalette.vue` — agregar atajos
- `app/components/app/AppHeader.vue` — agregar NotificacionBell
- `app/pages/clientes/index.vue` — agregar botón de estadísticas/comportamiento
- `app/pages/perfil.vue` — agregar sección de notificaciones/recordatorios
- `app/services/api/prestamo.ts` — agregar generarEventosAgenda
