<script setup lang="ts">
import { usePrestamos } from '~/composables/domain/usePrestamos'
import { useMoras } from '~/composables/domain/useMoras'
import { UiEstadoBadge } from '#components'
import DataTable from '~/components/ui/DataTable.vue'
import RenovarModal from '~/components/prestamos/RenovarModal.vue'
import MarcarPerdidoModal from '~/components/prestamos/MarcarPerdidoModal.vue'

definePageMeta({
  middleware: 'auth'
})

const route = useRoute()
const router = useRouter()
const toast = useToast()
const formateo = useFormatters()

const prestamoId = computed(() => Number(route.params.id))

const { detalle, loading, error, byId, renovar, marcarPerdido } = usePrestamos()
const { moras: morasPrestamo, fetchByPrestamo } = useMoras()

const renovarAbierto = ref(false)
const perdidoAbierto = ref(false)
const enviando = ref(false)

async function inicializar() {
  await byId(prestamoId.value)
  await fetchByPrestamo(prestamoId.value)
}
inicializar()

const prestamo = computed(() => detalle.value)

const cuotas = computed(() => prestamo.value?.cuotas ?? [])
const pagos = computed(() => prestamo.value?.pagos ?? [])

const esActivo = computed(() => prestamo.value?.estado === 'activo')

async function confirmarRenovar(data: { porcentaje_interes: number, numero_cuotas: number, abono: number, fecha_renovacion: string, observaciones?: string | null }) {
  try {
    const nuevo = await renovar(prestamoId.value, {
      porcentaje_interes: data.porcentaje_interes,
      numero_cuotas: data.numero_cuotas,
      abono: data.abono,
      fecha_renovacion: data.fecha_renovacion,
      observaciones: data.observaciones
    })
    toast.add({ title: `Préstamo renovado · nuevo préstamo #${nuevo.id}`, color: 'success' })
    renovarAbierto.value = false
  } catch (e) {
    toast.add({ title: (e as { detail: string }).detail || 'No se pudo renovar el préstamo', color: 'error' })
  } finally {
    enviando.value = false
  }
}

async function confirmarPerdido(data: { motivo?: string | null, fecha: string }) {
  try {
    await marcarPerdido(prestamoId.value, data)
    toast.add({ title: 'Préstamo marcado como perdido', color: 'success' })
    perdidoAbierto.value = false
  } catch (e) {
    toast.add({ title: (e as { detail: string }).detail || 'No se pudo marcar el préstamo', color: 'error' })
  } finally {
    enviando.value = false
  }
}

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
  },
  {
    header: 'Tipo de pago',
    accessorKey: 'tipo_pago_id'
  }
]
</script>

<template>
  <div class="p-6 space-y-6">
    <div v-if="loading">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <USkeleton
          v-for="i in 8"
          :key="i"
          class="h-24 w-full"
        />
      </div>
    </div>

    <div
      v-else-if="error"
      class="flex flex-col items-center gap-3 py-10"
    >
      <UIcon
        name="i-lucide-alert-triangle"
        class="text-3xl text-error"
      />
      <p class="text-sm text-gray-500">
        {{ error }}
      </p>
      <UButton
        color="primary"
        variant="outline"
        size="sm"
        icon="i-lucide-refresh-cw"
        @click="inicializar"
      >
        Reintentar
      </UButton>
    </div>

    <template v-else-if="prestamo">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <div class="flex items-center gap-3">
          <UButton
            icon="i-lucide-arrow-left"
            color="neutral"
            variant="ghost"
            @click="() => { router.push('/prestamos') }"
          />
          <div>
            <h1 class="text-2xl font-bold">
              Préstamo #{{ prestamo.id }}
            </h1>
            <p class="text-sm text-gray-500">
              {{ prestamo.cliente?.nombre }} · C.C {{ prestamo.cliente?.cedula }}
            </p>
          </div>
          <EstadoBadge
            entidad="prestamo"
            :estado="prestamo.estado"
          />
        </div>
        <div
          v-if="esActivo"
          class="flex gap-2"
        >
          <UButton
            color="primary"
            icon="i-lucide-refresh-cw"
            @click="() => { renovarAbierto = true }"
          >
            Renovar préstamo
          </UButton>
          <UButton
            color="error"
            variant="outline"
            icon="i-lucide-flag"
            @click="() => { perdidoAbierto = true }"
          >
            Marcar como perdido
          </UButton>
        </div>
      </div>

      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard
          titulo="Capital prestado"
          :valor="formateo.formatoMoneda(prestamo.capital_prestado)"
          icono="i-lucide-coins"
        />
        <StatCard
          titulo="Interés total"
          :valor="formateo.formatoMoneda(prestamo.interes_total)"
          icono="i-lucide-percent"
        />
        <StatCard
          titulo="Monto total"
          :valor="formateo.formatoMoneda(prestamo.monto_total)"
          icono="i-lucide-banknote"
        />
        <StatCard
          titulo="Saldo pendiente"
          :valor="formateo.formatoMoneda(prestamo.saldo_pendiente)"
          icono="i-lucide-wallet"
          color="warning"
        />
        <StatCard
          titulo="Valor cuota"
          :valor="formateo.formatoMoneda(prestamo.valor_cuota)"
          icono="i-lucide-calendar"
        />
        <StatCard
          titulo="N° cuotas"
          :valor="String(prestamo.numero_cuotas)"
          icono="i-lucide-hash"
        />
        <StatCard
          titulo="Fecha préstamo"
          :valor="formateo.formatoFecha(prestamo.fecha_prestamo)"
          icono="i-lucide-calendar-check"
        />
        <StatCard
          titulo="Interés mensual"
          :valor="formateo.formatoPorcentaje(prestamo.porcentaje_interes)"
          icono="i-lucide-percent"
        />
      </div>

      <DataTable
        titulo="Cuotas"
        :data="cuotas as unknown as Record<string, unknown>[]"
        :columns="columnsCuotas"
        exportar-nombre="cuotas"
      />

      <DataTable
        titulo="Pagos registrados"
        :data="pagos as unknown as Record<string, unknown>[]"
        :columns="columnsPagos"
        exportar-nombre="pagos"
      />

      <UCard>
        <template #header>
          <h3 class="font-bold">
            Renovaciones
          </h3>
        </template>
        <EmptyState
          icono="i-lucide-history"
          titulo="Sin historial de renovaciones"
          descripcion="El detalle no incluye el historial de renovaciones. Este dato requiere un endpoint específico del backend."
        />
      </UCard>

      <UCard>
        <template #header>
          <div class="flex justify-between items-center">
            <h3 class="font-bold">
              Moras
            </h3>
            <span class="text-sm text-gray-500">
              {{ morasPrestamo.length }} registradas
            </span>
          </div>
        </template>
        <EmptyState
          v-if="!morasPrestamo.length"
          icono="i-lucide-alert-triangle"
          titulo="Sin moras"
          descripcion="No se han generado moras para este préstamo."
        />
        <UTable
          v-else
          sticky
          :data="morasPrestamo as unknown as Record<string, unknown>[]"
          :columns="[
            { accessorKey: 'id', header: 'ID' },
            { accessorKey: 'cuota_id', header: 'Cuota' },
            { header: 'Fecha', cell: ({ row }: { row: { original: Record<string, unknown> } }) => formatoFecha(String(row.original.fecha)) },
            { header: 'Valor', cell: ({ row }: { row: { original: Record<string, unknown> } }) => formatoMoneda(Number(row.original.valor)) },
            { header: 'Estado', cell: ({ row }: { row: { original: Record<string, unknown> } }) => String(row.original.estado ?? '') }
          ]"
          class="max-h-[40vh]"
        />
      </UCard>
    </template>

    <RenovarModal
      :open="renovarAbierto"
      :prestamo="prestamo"
      @update:open="renovarAbierto = $event"
      @confirmar="confirmarRenovar"
    />

    <MarcarPerdidoModal
      :open="perdidoAbierto"
      :prestamo="prestamo"
      @update:open="perdidoAbierto = $event"
      @confirmar="confirmarPerdido"
    />
  </div>
</template>
