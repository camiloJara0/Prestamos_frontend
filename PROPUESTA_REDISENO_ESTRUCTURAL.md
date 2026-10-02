# Propuesta de Rediseño Estructural — LoanSoft Frontend

## 1. Análisis del Flujo Actual

### Estructura de navegación actual (11 rutas)

```
/                         → Dashboard
/prestamos/nuevo          → Crear préstamo (página dedicada)
/prestamos                → Listado de préstamos
/prestamos/:id            → Detalle de préstamo
/pagos                    → Registrar pago + historial (tabs)
/moras                    → CRUD de moras
/clientes                 → CRUD de clientes
/cobranza                 → Por vencer / Morosos / Notas (tabs)
/reportes                 → Ganancias / Pérdidas (tabs)
/capital                  → Capital + movimientos
/tipos-prestamo           → CRUD tipos préstamo
/tipos-pago               → CRUD tipos pago
/usuarios                 → CRUD usuarios
/perfil                   → Perfil + contraseña + auditoría
/login                    → Login
```

### Problemas identificados

| Problema | Impacto |
|---|---|
| **Registrar pago** está en una página separada del préstamo | El usuario debe copiar el ID del préstamo, navegar a otra página, pegar el ID |
| **Moras** está completamente aislada | No hay acceso directo desde el detalle del préstamo para gestión de moras |
| **Crear préstamo** es una página independiente | Podría ser un modal o panel dentro del listado de préstamos |
| **Navegación excesiva** | Para un flujo típico (ver préstamo → registrar pago → volver) se necesitan 3+ navegaciones |
| **Cobranza** es redundante | La información de "por vencer" y "morosos" ya está en el detalle del préstamo |
| **11 módulos en el sidebar** | Sobrecarga cognitiva, difícil de escalar |

---

## 2. Propuesta: Agrupación por Flujo de Negocio

### 2.1 Estructura propuesta (7 módulos)

```
/
├── Dashboard
├── Préstamos/           ← Módulo unificado
│   ├── Listado          (con crear/editar como modal)
│   └── [id]             (tabs: cuotas, pagos, moras, renovaciones)
├── Clientes/
│   └── Listado          (CRUD completo)
├── Cobranza/
│   └── Seguimiento      (por vencer, morosos, notas)
├── Reportes/
│   └── Análisis         (ganancias, pérdidas, exportación)
├── Configuración/       ← Solo admin
│   ├── Capital
│   ├── Tipos de préstamo
│   ├── Tipos de pago
│   └── Usuarios
└── Perfil
```

### 2.2 Cambios en el sidebar

```typescript
// ANTES (11 items)
Principal:    Dashboard, Crear préstamo
Préstamos:    Préstamos, Pagos, Moras
Clientes:     Clientes
Reportes:     Reportes, Cobranza
Config:       Capital, Tipos préstamo, Tipos pago, Usuarios

// DESPUÉS (7 items)
Principal:    Dashboard
Gestión:      Préstamos, Clientes, Cobranza, Reportes
Config:       Capital, Tipos préstamo, Tipos pago, Usuarios
```

**Eliminados del sidebar:**
- "Crear préstamo" → se integra como botón/modal en el listado
- "Pagos" → se integra en el detalle del préstamo como tab
- "Moras" → se integra en el detalle del préstamo como tab

---

## 3. Módulo de Préstamos (Unificado)

### 3.1 Flujo propuesto

```
/préstamos
├── [Listado principal]
│   ├── Botón "Nuevo préstamo" → abre modal (no navega)
│   ├── Filtros: estado, cliente, fechas
│   ├── Tabla con columnas: ID, Cliente, Capital, Estado, Cuotas pagas/total
│   └── Click en fila → navega a /préstamos/:id
│
└── /préstamos/:id (Detalle unificado)
    ├── Header: ID, cliente, estado, botones "Renovar" / "Marcar perdido"
    ├── StatCards: capital, interés, total, saldo, cuota, cuotas
    ├── Tabs:
    │   ├── Cuotas → tabla de cuotas con acciones (ver pago, registrar pago)
    │   ├── Pagos → historial de pagos registrados
    │   ├── Moras → moras del préstamo + botón "Procesar moras"
    │   └── Notas → notas de seguimiento (IndexedDB)
    └── Modal "Registrar pago" → se abre desde el tab de cuotas
```

### 3.2 Páginas afectadas

| Archivo actual | Acción |
|---|---|
| `pages/prestamos/index.vue` | Se mantiene, se agrega modal de crear |
| `pages/prestamos/nuevo.vue` | Se elimina como página, se convierte en componente modal |
| `pages/prestamos/[id].vue` | Se reestructura con tabs (cuotas, pagos, moras) |
| `pages/pagos/index.vue` | Se elimina como página independiente |
| `pages/moras/index.vue` | Se mantiene solo para vista admin de todas las moras |

### 3.3 Nuevo componente: PrestamoModalCrear

```vue
<!-- Reemplaza pages/prestamos/nuevo.vue -->
<template>
  <UModal :open="open" @update:open="$emit('update:open', $event)">
    <template #title>Nuevo préstamo</template>
    <template #body>
      <!-- Mismo formulario que PrestamoForm, con calculadora en vivo -->
    </template>
  </UModal>
</template>
```

### 3.4 Nuevo componente: PrestamoPagoModal

```vue
<!-- Reemplaza la navegación a /pagos desde el detalle -->
<template>
  <UModal :open="open" @update:open="$emit('update:open', $event)">
    <template #title>Registrar pago — Préstamo #{{ prestamoId }}</template>
    <template #body>
      <!-- Mismo PagoForm, prellenado con prestamo_id y cuota_id -->
    </template>
  </UModal>
</template>
```

---

## 4. Módulo de Cobranza (Simplificado)

### 4.1 Flujo actual vs propuesto

```
ACTUAL:
  /cobranza → 3 tabs (por vencer, morosos, notas)

PROPUESTO:
  /cobranza → Lista consolidada de acciones pendientes
  ├── Filtro: todos / por vencer (7/15/30 días) / morosos
  ├── Columnas: Préstamo, Cliente, Cuota, Valor, Días restantes/atraso, Acción
  └── Click en "Acción" → abre modal de pago directamente
```

**Se eliminan:**
- Tab "Notas" (se integra en el detalle del préstamo)
- Tab "Morosos" separado (se consolida en la tabla principal)

---

## 5. Módulo de Pagos (Eliminado como página)

### 5.1 Flujo propuesto

**Ya no existe `/pagos` como ruta independiente.**

El registro de pago se realiza desde:
1. **Detalle del préstamo** → tab "Cuotas" → botón "Registrar pago" en cada cuota
2. **Cobranza** → botón "Acción" en la fila correspondiente
3. **Command Palette (Ctrl+K)** → acción "Registrar pago"

### 5.2 Historial de pagos

Se accede desde:
1. **Detalle del préstamo** → tab "Pagos"
2. **Reportes** → métricas de pagos recibidos

---

## 6. Módulo de Clientes (Sin cambios significativos)

Se mantiene como página independiente con CRUD completo. Opcionalmente:
- Agregar tab "Préstamos del cliente" en un futuro
- Click en préstamo muestra el cliente asociado

---

## 7. Módulo de Reportes (Sin cambios significativos)

Se mantiene con tabs Ganancias/Pérdidas. Opcionalmente:
- Agregar filtro por cliente
- Agregar gráficas temporales

---

## 8. Módulo de Configuración (Sin cambios)

Se mantiene igual. Solo accesible para admin.

---

## 9. Resumen de Cambios de Archivos

### Archivos a crear

| Archivo | Descripción |
|---|---|
| `app/components/prestamos/PrestamoModalCrear.vue` | Modal para crear préstamo (reemplaza página) |
| `app/components/prestamos/PrestamoPagoModal.vue` | Modal para registrar pago desde el detalle |
| `app/components/prestamos/PrestamoTabs.vue` | Tabs del detalle (cuotas, pagos, moras, notas) |

### Archivos a modificar

| Archivo | Cambio |
|---|---|
| `app/components/Layout/Aside.vue` | Reorganizar secciones de navegación |
| `app/pages/prestamos/index.vue` | Agregar botón que abre modal crear |
| `app/pages/prestamos/[id].vue` | Reestructurar con tabs, integrar pagos y moras |
| `app/pages/cobranza/index.vue` | Simplificar a tabla consolidada con acción de pago |

### Archivos a eliminar

| Archivo | Razón |
|---|---|
| `app/pages/prestamos/nuevo.vue` | Reemplazado por modal |
| `app/pages/pagos/index.vue` | Integrado en detalle del préstamo |
| `app/pages/moras/index.vue` | Integrado en detalle del préstamo (se mantiene como vista admin opcional) |

### Archivos a mover a vista admin

| Archivo | Nueva ubicación |
|---|---|
| `app/pages/moras/index.vue` | `app/pages/configuracion/moras.vue` (solo admin) |

---

## 10. Flujo del Usuario (Antes vs Después)

### Escenario: Registrar un pago de cuota

```
ANTES (4 pasos):
1. Copiar ID del préstamo desde /prestamos
2. Navegar a /pagos
3. Pegar ID del préstamo
4. Seleccionar cuota y registrar pago

DESPUÉS (2 pasos):
1. Navegar a /prestamos → click en el préstamo
2. Tab "Cuotas" → click "Registrar pago" en la cuota → modal → guardar
```

### Escenario: Ver moras de un préstamo

```
ANTES (3 pasos):
1. Navegar a /moras
2. Filtrar por ID del préstamo
3. Ver la tabla

DESPUÉS (1 paso):
1. Navegar a /prestamos/:id → tab "Moras"
```

### Escenario: Crear un préstamo nuevo

```
ANTES (1 paso, pero cambia de contexto):
1. Navegar a /prestamos/nuevo

DESPUÉS (1 paso, sin cambiar de contexto):
1. Desde /prestamos → click "Nuevo préstamo" → modal → guardar
```

---

## 11. Impacto Estimado

| Métrica | Antes | Después | Cambio |
|---|---|---|---|
| Rutas totales | 15 | 12 | -3 |
| Items en sidebar | 11 | 7 | -4 |
| Clicks para registrar pago | 4 | 2 | -50% |
| Clicks para ver moras | 3 | 1 | -67% |
| Páginas a crear | — | 0 | — |
| Componentes a crear | — | 3 | — |
| Páginas a eliminar | — | 3 | — |
| Archivos a modificar | — | 4 | — |

---

## 12. Riesgos y Consideraciones

| Riesgo | Mitigación |
|---|---|
| Perder bookmark de `/pagos` | Mantener redirección 301 de `/pagos` → `/prestamos` |
| Confusión de usuarios existentes | Mantener funcionalidad antigua por 1 sprint, mostrar banner informativo |
| Complejidad del componente de préstamo | Dividir en sub-componentes (PrestamoCuotas, PrestamoPagos, PrestamoMoras) |
| Moras como vista admin | Mantener `/configuracion/moras` para gestión global |

---

## 13. Plan de Implementación

### Fase A: Preparación (1 día)
- Crear componentes modales (PrestamoModalCrear, PrestamoPagoModal)
- Crear componente PrestamoTabs

### Fase B: Módulo de Préstamos unificado (2 días)
- Reestructurar `[id].vue` con tabs
- Integrar pagos y moras en el detalle
- Eliminar `/prestamos/nuevo.vue` y `/pagos/index.vue`

### Fase C: Cobranza simplificada (1 día)
- Reescribir cobranza como tabla consolidada
- Agregar acción de pago directo

### Fase D: Navegación y limpieza (0.5 días)
- Actualizar sidebar
- Agregar redirecciones
- Eliminar archivos obsoletos

### Fase E: Verificación (0.5 días)
- Typecheck, lint, tests
- Prueba manual de flujos

**Total estimado: ~5 días de trabajo**
