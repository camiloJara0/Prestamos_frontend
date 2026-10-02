<script setup lang="ts">
import type { PrestamoDetalle } from '#shared/types/prestamo'
import { UiEstadoBadge, UButton } from '#components'
import DataTable from '~/components/ui/DataTable.vue'
import EmptyState from '~/components/ui/EmptyState.vue'
import { useMoras } from '~/composables/domain/useMoras'
import { useTiposPago } from '~/composables/domain/useTipos'
import { obtenerLog } from '~/services/db/audit'
import type { AuditLog } from '~/services/db/db'
import { formatoFecha } from '~/utils/fecha'
import type { PrestamoCuota } from '#shared/types/prestamo_cuota'

const props = defineProps<{
  prestamo: PrestamoDetalle
}>()

const emit = defineEmits<{
  pagar: [cuota: PrestamoCuota]
}>()

const toast = useToast()
const formateo = useFormatters()

const { moras: morasPrestamo, fetchByPrestamo, procesar } = useMoras()
const { fetch: fetchTiposPago } = useTiposPago()

const tabActiva = ref('cuotas')
const procesando = ref(false)

async function inicializar() {
  await Promise.all([
    fetchByPrestamo(props.prestamo.id),
    fetchTiposPago()
  ])
}
inicializar()

const cuotas = computed(() => props.prestamo.cuotas ?? [])
const pagos = computed(() => props.prestamo.pagos ?? [])
const cuotasPendientes = computed(() => cuotas.value.filter(c => c.estado === 'pendiente'))

const columnsCuotas = [
  { accessorKey: 'numero_cuota', header: 'N°', sorted: true },
  {
    header: 'Vencimiento',
    cell: (row: Record<string, unknown>) => formateo.formatoFecha(String(row.fecha_vencimiento))
  },
  {
    header: 'Valor',
    cell: (row: Record<string, unknown>) => formateo.formatoMoneda(Number(row.valor_cuota))
  },
  {
    header: 'Capital',
    cell: (row: Record<string, unknown>) => formateo.formatoMoneda(Number(row.capital))
  },
  {
    header: 'Interés',
    cell: (row: Record<string, unknown>) => formateo.formatoMoneda(Number(row.interes))
  },
  {
    header: 'Mora',
    cell: (row: Record<string, unknown>) => formateo.formatoMoneda(Number(row.mora))
  },
  {
    header: 'Estado',
    component: UiEstadoBadge,
    componentProps: (row: Record<string, unknown>) => ({ entidad: 'cuota', estado: String(row.estado ?? '') })
  },
  {
    header: 'Acciones',
    component: UButton,
    componentProps: (row: Record<string, unknown>) => ({
      icon: 'i-lucide-credit-card',
      color: row.estado === 'pendiente' ? 'primary' : 'neutral',
      variant: 'ghost',
      size: 'xs',
      label: 'Pagar',
      disabled: row.estado !== 'pendiente',
      onClick: () => {
        if (row.estado === 'pendiente') {
          emit('pagar', row as unknown as PrestamoCuota)
        }
      }
    })
  }
]

const columnsPagos = [
  {
    header: 'Fecha',
    cell: (row: Record<string, unknown>) => formateo.formatoFecha(String(row.fecha_pago))
  },
  {
    header: 'Valor',
    cell: (row: Record<string, unknown>) => formateo.formatoMoneda(Number(row.valor_pagado))
  },
  {
    header: 'Capital',
    cell: (row: Record<string, unknown>) => formateo.formatoMoneda(Number(row.capital_pagado))
  },
  {
    header: 'Interés',
    cell: (row: Record<string, unknown>) => formateo.formatoMoneda(Number(row.interes_pagado))
  },
  {
    header: 'Mora',
    cell: (row: Record<string, unknown>) => formateo.formatoMoneda(Number(row.mora_pagada))
  }
]

async function procesarMoras() {
  procesando.value = true
  try {
    const resultado = await procesar()
    toast.add({
      title: `Moras procesadas: ${resultado.total_moras_procesadas} actualizadas`,
      color: 'success'
    })
    await fetchByPrestamo(props.prestamo.id)
  } catch (e) {
    toast.add({ title: (e as { detail: string }).detail || 'No se pudieron procesar las moras', color: 'error' })
  } finally {
    procesando.value = false
  }
}

const logs = ref<AuditLog[]>([])
const loadingLogs = ref(false)

async function cargarLogs() {
  loadingLogs.value = true
  try {
    logs.value = await obtenerLog({
      entidad: 'prestamo',
      limit: 50
    })
  } finally {
    loadingLogs.value = false
  }
}

watch(tabActiva, (tab) => {
  if (tab === 'notas') cargarLogs()
})
</script>

<template>
  <UTabs
    v-model="tabActiva"
    :items="[
      { label: `Cuotas (${cuotasPendientes.length} pendientes)`, value: 'cuotas', icon: 'i-lucide-list', slot: 'cuotas' },
      { label: `Pagos (${pagos.length})`, value: 'pagos', icon: 'i-lucide-credit-card', slot: 'pagos' },
      { label: `Moras (${morasPrestamo.length})`, value: 'moras', icon: 'i-lucide-alert-triangle', slot: 'moras' },
      { label: 'Notas', value: 'notas', icon: 'i-lucide-file-text', slot: 'notas' }
    ]"
  >
    <template #cuotas>
      <DataTable
        titulo="Cuotas del préstamo"
        :data="cuotas as unknown as Record<string, unknown>[]"
        :columns="columnsCuotas"
        exportar-nombre="cuotas-prestamo"
      />
    </template>

    <template #pagos>
      <EmptyState
        v-if="!pagos.length"
        icono="i-lucide-credit-card"
        titulo="Sin pagos"
        descripcion="No se han registrado pagos para este préstamo."
      />
      <DataTable
        v-else
        titulo="Pagos registrados"
        :data="pagos as unknown as Record<string, unknown>[]"
        :columns="columnsPagos"
        exportar-nombre="pagos-prestamo"
      />
    </template>

    <template #moras>
      <EmptyState
        v-if="!morasPrestamo.length"
        icono="i-lucide-alert-triangle"
        titulo="Sin moras"
        descripcion="No se han generado moras para este préstamo."
      />
      <div
        v-else
        class="space-y-4"
      >
        <div class="flex justify-end">
          <UButton
            color="warning"
            icon="i-lucide-calculator"
            size="xs"
            :loading="procesando"
            label="Procesar moras"
            @click="procesarMoras"
          />
        </div>
        <DataTable
          titulo="Moras del préstamo"
          :data="morasPrestamo as unknown as Record<string, unknown>[]"
          :columns="[
            { accessorKey: 'id', header: 'ID' },
            { accessorKey: 'cuota_id', header: 'Cuota' },
            { header: 'Fecha', cell: (row: Record<string, unknown>) => formatoFecha(String(row.fecha)) },
            { header: 'Valor', cell: (row: Record<string, unknown>) => formatoMoneda(Number(row.valor)) },
            { header: 'Estado', accessorKey: 'estado' }
          ]"
          exportar-nombre="moras-prestamo"
        />
      </div>
    </template>

    <template #notas>
      <UCard>
        <template #header>
          <h3 class="font-bold">
            Notas y auditoría
          </h3>
        </template>

        <EmptyState
          v-if="!logs.length && !loadingLogs"
          icono="i-lucide-file-text"
          titulo="Sin notas"
          descripcion="No hay eventos registrados para este préstamo."
        />

        <div
          v-else
          class="space-y-2 max-h-[50vh] overflow-y-auto"
        >
          <USkeleton
            v-if="loadingLogs"
            class="h-25 rounded-lg"
          />
          <div
            v-for="log in logs"
            :key="log.id"
            class="flex items-start gap-3 p-2 rounded border border-gray-100 dark:border-gray-800 text-sm"
          >
            <span class="text-xs text-gray-400 shrink-0 w-36">{{ formatoFecha(log.timestamp) }}</span>
            <span class="text-xs px-2 py-0.5 rounded-full bg-gray-100 dark:bg-gray-800">{{ log.accion }}</span>
            <span class="text-gray-600 dark:text-gray-300">{{ log.entidad }} #{{ log.entidadId ?? '—' }}</span>
          </div>
        </div>
      </UCard>
    </template>
  </UTabs>
</template>
