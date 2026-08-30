<script setup lang="ts">
import { useReportes } from '~/composables/domain/useReportes'

definePageMeta({
  middleware: 'auth'
})

const formateo = useFormatters()
const toast = useToast()

const {
  ganancias,
  perdidas,
  loading,
  error,
  descargando,
  fetchTodos,
  descargar
} = useReportes()

const tabActiva = ref<'ganancias' | 'perdidas'>('ganancias')

const filtroMes = ref('')
const filtroAnio = ref('')

const meses = [
  { label: 'Todos', value: '' },
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
  const lista: { label: string, value: string }[] = [{ label: 'Todos', value: '' }]
  for (let y = anioActual; y >= anioActual - 5; y--) {
    lista.push({ label: String(y), value: String(y) })
  }
  return lista
})

function paramsFiltro() {
  const params: Record<string, number> = {}
  if (filtroMes.value !== '') params.mes = Number(filtroMes.value)
  if (filtroAnio.value !== '') params.anio = Number(filtroAnio.value)
  return params
}

function aplicarFiltros() {
  fetchTodos(paramsFiltro())
}

function limpiarFiltros() {
  filtroMes.value = ''
  filtroAnio.value = ''
  fetchTodos()
}

async function exportar(tipo: 'ganancias' | 'perdidas', formato: 'excel' | 'pdf') {
  try {
    await descargar(tipo, formato, paramsFiltro())
    toast.add({ title: `Descargando ${tipo}.${formato === 'excel' ? 'xlsx' : 'pdf'}`, color: 'success' })
  } catch {
    toast.add({ title: 'No se pudo descargar el reporte', color: 'error' })
  }
}

fetchTodos()
</script>

<template>
  <div class="p-6 space-y-4">
    <div class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <h1 class="text-2xl font-bold">
          Reportes
        </h1>
        <p class="text-sm text-gray-500">
          Ganancias, pérdidas y exportación.
        </p>
      </div>
    </div>

    <UCard>
      <div class="flex flex-wrap items-end gap-3">
        <UField label="Mes">
          <USelect
            v-model="filtroMes"
            :items="meses"
          />
        </UField>
        <UField label="Año">
          <USelect
            v-model="filtroAnio"
            :items="aniosDisponibles"
          />
        </UField>
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
        { label: 'Pérdidas', value: 'perdidas', icon: 'i-lucide-trending-down', slot: 'perdidas' }
      ]"
    >
      <template #ganancias>
        <div class="space-y-4">
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            <USkeleton
              v-if="loading"
              class="h-[88px] rounded-xl"
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
              class="h-[88px] rounded-xl"
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
              class="h-[88px] rounded-xl"
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
              class="h-[88px] rounded-xl"
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
              class="h-[88px] rounded-xl"
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
              class="h-[88px] rounded-xl"
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
              class="h-[88px] rounded-xl"
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
    </UTabs>
  </div>
</template>
