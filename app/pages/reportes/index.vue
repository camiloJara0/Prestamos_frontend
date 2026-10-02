<script setup lang="ts">
import { useReportes } from '~/composables/domain/useReportes'
import type { ReporteTipo } from '#shared/types/reporte'

definePageMeta({
  middleware: 'auth'
})

const formateo = useFormatters()
const toast = useToast()

const {
  ganancias,
  perdidas,
  cartera,
  cobranza,
  loading,
  error,
  descargando,
  fetchTodos,
  descargar
} = useReportes()

type TabActiva = 'ganancias' | 'perdidas' | 'cartera' | 'cobranza'
const tabActiva = ref<TabActiva>('ganancias')

const filtroMes = ref('#')
const filtroAnio = ref('#')

const meses = [
  { label: 'Todos', value: '#' },
  { label: 'Enero', value: '1' },
  { label: 'Febrero', value: '2' },
  { label: 'Marzo', value: '3' },
  { label: 'Abril', value: '4' },
  { label: 'Mayo', value: '5' },
  { label: 'Junio', value: '6' },
  { label: 'Julio', value: '7' },
  { label: 'Agosto', value: '8' },
  { label: 'Septiembre', value: '9' },
  { label: 'Octubre', value: '10' },
  { label: 'Noviembre', value: '11' },
  { label: 'Diciembre', value: '12' }
]

const anioActual = new Date().getFullYear()
const aniosDisponibles = computed(() => {
  const lista: { label: string, value: string }[] = [{ label: 'Todos', value: '#' }]
  for (let y = anioActual; y >= anioActual - 5; y--) {
    lista.push({ label: String(y), value: String(y) })
  }
  return lista
})

function paramsFiltro() {
  const params: Record<string, number | string> = {}
  if (filtroMes.value !== '#') params.mes = Number(filtroMes.value)
  if (filtroAnio.value !== '#') params.anio = Number(filtroAnio.value)
  // Cartera y cobranza trabajan con rangos de fecha (RF-053 / RF-054)
  if (filtroMes.value !== '#' && filtroAnio.value !== '#') {
    const mes = String(filtroMes.value).padStart(2, '0')
    const anio = Number(filtroAnio.value)
    const ultimoDia = new Date(anio, Number(filtroMes.value), 0).getDate()
    params.desde = `${anio}-${mes}-01`
    params.hasta = `${anio}-${mes}-${String(ultimoDia).padStart(2, '0')}`
  }
  return params
}

function paramsExport(tipo: ReporteTipo) {
  const p = paramsFiltro()
  if (tipo === 'cartera' || tipo === 'cobranza') {
    return { desde: p.desde as string | undefined, hasta: p.hasta as string | undefined }
  }
  return { mes: p.mes as number | undefined, anio: p.anio as number | undefined }
}

function aplicarFiltros() {
  fetchTodos(paramsFiltro())
}

function limpiarFiltros() {
  filtroMes.value = '#'
  filtroAnio.value = '#'
  fetchTodos()
}

async function exportar(tipo: ReporteTipo, formato: 'excel' | 'pdf') {
  try {
    await descargar(tipo, formato, paramsExport(tipo))
    toast.add({ title: `Descargando ${tipo}.${formato === 'excel' ? 'xlsx' : 'pdf'}`, color: 'success' })
  } catch {
    toast.add({ title: 'No se pudo descargar el reporte', color: 'error' })
  }
}

const filasCartera = computed(() => (cartera.value?.detalle ?? []).map(d => ({
  prestamo: `#${d.prestamo_id}`,
  cliente: d.cliente,
  estado: d.estado,
  fecha: formateo.formatoFecha(d.fecha_prestamo),
  capital: formateo.formatoMoneda(d.capital_prestado),
  saldo: formateo.formatoMoneda(d.saldo_pendiente),
  dias: String(d.dias_antiguedad)
})))

const columnsCartera = [
  { accessorKey: 'prestamo', header: 'Préstamo' },
  { accessorKey: 'cliente', header: 'Cliente' },
  { accessorKey: 'estado', header: 'Estado' },
  { accessorKey: 'fecha', header: 'Fecha' },
  { accessorKey: 'capital', header: 'Capital' },
  { accessorKey: 'saldo', header: 'Saldo' },
  { accessorKey: 'dias', header: 'Días' }
]

const filasDistribucion = computed(() => {
  const dist = cartera.value?.distribucion_por_estado ?? {}
  return Object.entries(dist).map(([estado, g]) => ({
    estado,
    cantidad: String(g.cantidad),
    monto: formateo.formatoMoneda(g.monto)
  }))
})

const filasAntiguedad = computed(() => {
  const ant = cartera.value?.antiguedad ?? {}
  return Object.entries(ant).map(([rango, g]) => ({
    rango,
    cantidad: String(g.cantidad),
    saldo: formateo.formatoMoneda(g.saldo)
  }))
})

const filasCobranzaDia = computed(() => (cobranza.value?.detalle_por_dia ?? []).map(d => ({
  fecha: formateo.formatoFecha(d.fecha),
  cantidad: String(d.cantidad_pagos),
  capital: formateo.formatoMoneda(d.capital),
  interes: formateo.formatoMoneda(d.interes),
  mora: formateo.formatoMoneda(d.mora),
  total: formateo.formatoMoneda(d.total)
})))

const columnsCobranzaDia = [
  { accessorKey: 'fecha', header: 'Fecha' },
  { accessorKey: 'cantidad', header: 'Pagos' },
  { accessorKey: 'capital', header: 'Capital' },
  { accessorKey: 'interes', header: 'Interés' },
  { accessorKey: 'mora', header: 'Mora' },
  { accessorKey: 'total', header: 'Total' }
]

fetchTodos()
</script>

<template>
  <div class="p-6 space-y-4">
    <UiPageHeader
      titulo="Reportes"
      descripcion="Ganancias, pérdidas, cartera, cobranza y exportación."
      icono="i-lucide-bar-chart-2"
    />

    <UCard>
      <div class="flex flex-wrap items-end gap-3">
        <UFormField label="Mes">
          <USelect
            v-model="filtroMes"
            :items="meses"
          />
        </UFormField>
        <UFormField label="Año">
          <USelect
            v-model="filtroAnio"
            :items="aniosDisponibles"
          />
        </UFormField>
        <UButton
          color="primary"
          icon="i-lucide-search"
          :loading="loading"
          @click="aplicarFiltros"
        >
          Aplicar
        </UButton>
        <UButton
          color="neutral"
          variant="outline"
          icon="i-lucide-x"
          @click="limpiarFiltros"
        >
          Limpiar
        </UButton>
      </div>
    </UCard>

    <UAlert
      v-if="error"
      icon="i-lucide-alert-triangle"
      color="error"
      :title="error"
      :actions="[{ label: 'Reintentar', color: 'primary', variant: 'outline', onClick: aplicarFiltros }]"
    />

    <UTabs
      v-model="tabActiva"
      :items="[
        { label: 'Ganancias', value: 'ganancias', icon: 'i-lucide-trending-up', slot: 'ganancias' },
        { label: 'Pérdidas', value: 'perdidas', icon: 'i-lucide-trending-down', slot: 'perdidas' },
        { label: 'Cartera', value: 'cartera', icon: 'i-lucide-briefcase', slot: 'cartera' },
        { label: 'Cobranza', value: 'cobranza', icon: 'i-lucide-hand-coins', slot: 'cobranza' }
      ]"
    >
      <template #ganancias>
        <div class="space-y-4">
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            <USkeleton
              v-if="loading"
              class="h-22 rounded-xl"
            />
            <UiStatCard
              v-else
              titulo="Total invertido"
              :valor="formateo.formatoMoneda(ganancias?.total_invertido ?? 0)"
              icono="i-lucide-wallet"
              color="primary"
            />
            <USkeleton
              v-if="loading"
              class="h-22 rounded-xl"
            />
            <UiStatCard
              v-else
              titulo="Total prestado"
              :valor="formateo.formatoMoneda(ganancias?.total_prestado ?? 0)"
              icono="i-lucide-banknote"
              color="info"
            />
            <USkeleton
              v-if="loading"
              class="h-22 rounded-xl"
            />
            <UiStatCard
              v-else
              titulo="Pagos recibidos"
              :valor="formateo.formatoMoneda(ganancias?.total_pagos_recibidos ?? 0)"
              icono="i-lucide-circle-dollar-sign"
              color="success"
            />
            <USkeleton
              v-if="loading"
              class="h-22 rounded-xl"
            />
            <UiStatCard
              v-else
              titulo="Total intereses"
              :valor="formateo.formatoMoneda(ganancias?.total_intereses ?? 0)"
              icono="i-lucide-percent"
              color="warning"
            />
            <USkeleton
              v-if="loading"
              class="h-22 rounded-xl"
            />
            <UiStatCard
              v-else
              titulo="Ganancia neta"
              :valor="formateo.formatoMoneda(ganancias?.ganancia_neta ?? 0)"
              icono="i-lucide-trending-up"
              color="success"
              :footer="ganancias?.periodo ?? 'Todos los periodos'"
            />
          </div>

          <UCard>
            <p class="text-xs text-gray-400">
              Fórmula del backend: <code>ganancia_neta = pagos_recibidos − prestado + invertido</code>.
              Periodo: {{ ganancias?.periodo ?? 'Todos los periodos' }}.
            </p>
          </UCard>

          <div class="flex justify-end gap-2">
            <UButton
              label="Exportar Excel"
              icon="i-lucide-file-spreadsheet"
              color="success"
              variant="outline"
              :loading="descargando"
              @click="exportar('ganancias', 'excel')"
            />
            <UButton
              label="Exportar PDF"
              icon="i-lucide-file-text"
              color="error"
              variant="outline"
              :loading="descargando"
              @click="exportar('ganancias', 'pdf')"
            />
          </div>
        </div>
      </template>

      <template #perdidas>
        <div class="space-y-4">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <USkeleton
              v-if="loading"
              class="h-22 rounded-xl"
            />
            <UiStatCard
              v-else
              titulo="Total pérdidas"
              :valor="formateo.formatoMoneda(perdidas?.total_perdidas ?? 0)"
              icono="i-lucide-alert-octagon"
              color="error"
              :footer="perdidas?.periodo ?? 'Todos los periodos'"
            />
            <USkeleton
              v-if="loading"
              class="h-22 rounded-xl"
            />
            <UiStatCard
              v-else
              titulo="Préstamos perdidos"
              :valor="String(perdidas?.cantidad_prestamos_perdidos ?? 0)"
              icono="i-lucide-x-circle"
              color="error"
            />
          </div>

          <UCard>
            <template #header>
              <div class="flex justify-between items-center">
                <h3 class="font-bold">
                  Detalle de pérdidas
                </h3>
                <span class="text-sm text-gray-500">
                  {{ perdidas?.detalle?.length ?? 0 }} registros
                </span>
              </div>
            </template>
            <EmptyState
              v-if="!perdidas?.detalle?.length && !loading"
              icono="i-lucide-check-circle"
              titulo="Sin pérdidas registradas"
              descripcion="No se han registrado préstamos perdidos en este periodo."
            />
            <UTable
              v-else-if="perdidas?.detalle?.length"
              sticky
              :data="(perdidas?.detalle ?? []) as unknown as Record<string, unknown>[]"
              :columns="[
                { accessorKey: 'prestamo_id', header: 'Préstamo' },
                { header: 'Fecha', cell: ({ row }: { row: { original: Record<string, unknown> } }) => formateo.formatoFecha(String(row.original.fecha)) },
                { header: 'Valor perdido', cell: ({ row }: { row: { original: Record<string, unknown> } }) => formateo.formatoMoneda(Number(row.original.valor_perdido)) },
                { header: 'Motivo', cell: ({ row }: { row: { original: Record<string, unknown> } }) => String(row.original.motivo ?? '—') }
              ]"
              class="max-h-[40vh]"
            />
          </UCard>

          <div class="flex justify-end gap-2">
            <UButton
              label="Exportar Excel"
              icon="i-lucide-file-spreadsheet"
              color="success"
              variant="outline"
              :loading="descargando"
              @click="exportar('perdidas', 'excel')"
            />
            <UButton
              label="Exportar PDF"
              icon="i-lucide-file-text"
              color="error"
              variant="outline"
              :loading="descargando"
              @click="exportar('perdidas', 'pdf')"
            />
          </div>
        </div>
      </template>

      <template #cartera>
        <div class="space-y-4">
          <UAlert
            v-if="cartera?.nota"
            icon="i-lucide-info"
            color="info"
            :title="cartera.nota"
          />

          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            <USkeleton
              v-if="loading"
              class="h-22 rounded-xl"
            />
            <UiStatCard
              v-else
              titulo="Préstamos en cartera"
              :valor="String(cartera?.total_prestamos ?? 0)"
              icono="i-lucide-briefcase"
              color="primary"
              :footer="cartera?.periodo ?? 'Todos los periodos'"
            />
            <USkeleton
              v-if="loading"
              class="h-22 rounded-xl"
            />
            <UiStatCard
              v-else
              titulo="Saldo pendiente total"
              :valor="formateo.formatoMoneda(cartera?.saldo_pendiente_total ?? 0)"
              icono="i-lucide-wallet"
              color="warning"
            />
            <USkeleton
              v-if="loading"
              class="h-22 rounded-xl"
            />
            <UiStatCard
              v-else
              titulo="Saldo de activos"
              :valor="formateo.formatoMoneda(cartera?.saldo_activos ?? 0)"
              icono="i-lucide-trending-up"
              color="success"
              :footer="`${cartera?.total_activos ?? 0} préstamos activos`"
            />
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <UCard>
              <template #header>
                <h3 class="font-bold">
                  Distribución por estado
                </h3>
              </template>
              <UTable
                sticky
                :data="filasDistribucion"
                :columns="[
                  { accessorKey: 'estado', header: 'Estado' },
                  { accessorKey: 'cantidad', header: 'Cantidad' },
                  { accessorKey: 'monto', header: 'Monto' }
                ]"
              />
            </UCard>

            <UCard>
              <template #header>
                <h3 class="font-bold">
                  Antigüedad de la cartera
                </h3>
              </template>
              <UTable
                sticky
                :data="filasAntiguedad"
                :columns="[
                  { accessorKey: 'rango', header: 'Rango' },
                  { accessorKey: 'cantidad', header: 'Cantidad' },
                  { accessorKey: 'saldo', header: 'Saldo' }
                ]"
              />
            </UCard>
          </div>

          <UCard>
            <template #header>
              <div class="flex justify-between items-center">
                <h3 class="font-bold">
                  Detalle por préstamo
                </h3>
                <span class="text-sm text-gray-500">
                  {{ cartera?.detalle?.length ?? 0 }} registros
                </span>
              </div>
            </template>
            <EmptyState
              v-if="!cartera?.detalle?.length && !loading"
              icono="i-lucide-briefcase"
              titulo="Sin cartera en el periodo"
              descripcion="No hay préstamos que coincidan con el periodo seleccionado."
            />
            <UTable
              v-else
              sticky
              :data="filasCartera"
              :columns="columnsCartera"
              class="max-h-[40vh]"
            />
          </UCard>

          <div class="flex justify-end gap-2">
            <UButton
              label="Exportar Excel"
              icon="i-lucide-file-spreadsheet"
              color="success"
              variant="outline"
              :loading="descargando"
              @click="exportar('cartera', 'excel')"
            />
            <UButton
              label="Exportar PDF"
              icon="i-lucide-file-text"
              color="error"
              variant="outline"
              :loading="descargando"
              @click="exportar('cartera', 'pdf')"
            />
          </div>
        </div>
      </template>

      <template #cobranza>
        <div class="space-y-4">
          <UAlert
            v-if="cobranza?.nota"
            icon="i-lucide-info"
            color="info"
            :title="cobranza.nota"
          />

          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <USkeleton
              v-if="loading"
              class="h-22 rounded-xl"
            />
            <UiStatCard
              v-else
              titulo="Total cobrado"
              :valor="formateo.formatoMoneda(cobranza?.totales_cobrados?.total ?? 0)"
              icono="i-lucide-circle-dollar-sign"
              color="success"
              :footer="cobranza?.periodo ?? 'Todos los periodos'"
            />
            <USkeleton
              v-if="loading"
              class="h-22 rounded-xl"
            />
            <UiStatCard
              v-else
              titulo="Capital cobrado"
              :valor="formateo.formatoMoneda(cobranza?.totales_cobrados?.capital ?? 0)"
              icono="i-lucide-coins"
              color="primary"
            />
            <USkeleton
              v-if="loading"
              class="h-22 rounded-xl"
            />
            <UiStatCard
              v-else
              titulo="Interés cobrado"
              :valor="formateo.formatoMoneda(cobranza?.totales_cobrados?.interes ?? 0)"
              icono="i-lucide-percent"
              color="info"
            />
            <USkeleton
              v-if="loading"
              class="h-22 rounded-xl"
            />
            <UiStatCard
              v-else
              titulo="Mora cobrada"
              :valor="formateo.formatoMoneda(cobranza?.totales_cobrados?.mora ?? 0)"
              icono="i-lucide-alert-triangle"
              color="warning"
            />
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <UiStatCard
              titulo="Vencidas"
              :valor="String(cobranza?.total_cuotas_vencidas ?? 0)"
              icono="i-lucide-clock-alert"
              color="error"
              :footer="formateo.formatoMoneda(cobranza?.monto_vencido ?? 0)"
            />
            <UiStatCard
              titulo="Por vencer"
              :valor="String(cobranza?.total_cuotas_por_vencer ?? 0)"
              icono="i-lucide-calendar-clock"
              color="warning"
              :footer="formateo.formatoMoneda(cobranza?.monto_por_vencer ?? 0)"
            />
            <UiStatCard
              titulo="Pagadas"
              :valor="String(cobranza?.total_cuotas_pagadas ?? 0)"
              icono="i-lucide-check-circle"
              color="success"
              :footer="formateo.formatoMoneda(cobranza?.monto_pagado ?? 0)"
            />
          </div>

          <UCard>
            <template #header>
              <div class="flex justify-between items-center">
                <h3 class="font-bold">
                  Lo cobrado por día
                </h3>
                <span class="text-sm text-gray-500">
                  {{ cobranza?.detalle_por_dia?.length ?? 0 }} días con cobros
                </span>
              </div>
            </template>
            <EmptyState
              v-if="!cobranza?.detalle_por_dia?.length && !loading"
              icono="i-lucide-hand-coins"
              titulo="Sin cobros en el periodo"
              descripcion="No se han registrado pagos confirmados en el periodo seleccionado."
            />
            <UTable
              v-else
              sticky
              :data="filasCobranzaDia"
              :columns="columnsCobranzaDia"
              class="max-h-[40vh]"
            />
          </UCard>

          <div class="flex justify-end gap-2">
            <UButton
              label="Exportar Excel"
              icon="i-lucide-file-spreadsheet"
              color="success"
              variant="outline"
              :loading="descargando"
              @click="exportar('cobranza', 'excel')"
            />
            <UButton
              label="Exportar PDF"
              icon="i-lucide-file-text"
              color="error"
              variant="outline"
              :loading="descargando"
              @click="exportar('cobranza', 'pdf')"
            />
          </div>
        </div>
      </template>
    </UTabs>
  </div>
</template>
