<script setup lang="ts">
import type { ReporteCobranza, CuotaCobranza } from '#shared/types/reporte'
import type { PrestamoCuota } from '#shared/types/prestamo_cuota'
import type { PrestamoDetalle } from '#shared/types/prestamo'
import { getReporteCobranza } from '~/services/api/reporte'
import { usePrestamos } from '~/composables/domain/usePrestamos'
import PrestamoPagoModal from '~/components/prestamos/PrestamoPagoModal.vue'
import NotaContactoModal from '~/components/cobranza/NotaContactoModal.vue'
import EmptyState from '~/components/ui/EmptyState.vue'
import { formatoFecha } from '~/utils/fecha'
import { formatoMoneda } from '~/utils/format'

definePageMeta({
  middleware: 'auth'
})

const { byId, detalle } = usePrestamos()
const toast = useToast()

const loading = ref(false)
const error = ref<string | null>(null)
const reporte = ref<ReporteCobranza | null>(null)
const filtroTipo = ref<'todos' | 'por_vencer' | 'morosos'>('todos')

const pagoAbierto = ref(false)
const prestamoSeleccionado = ref<PrestamoDetalle | null>(null)
const cuotaSeleccionada = ref<PrestamoCuota | null>(null)

const notasAbiertas = ref(false)
const prestamoNotas = ref<number | null>(null)

type ItemCobranza = CuotaCobranza & { tipo: 'por_vencer' | 'moroso' }

async function cargarDatos() {
  loading.value = true
  error.value = null
  try {
    reporte.value = await getReporteCobranza()
  } catch {
    error.value = 'No se pudo cargar la agenda de cobranza.'
  } finally {
    loading.value = false
  }
}

const items = computed<ItemCobranza[]>(() => {
  const r = reporte.value
  if (!r) return []
  const vencidas: ItemCobranza[] = r.cuotas_vencidas.map(c => ({ ...c, tipo: 'moroso' as const }))
  const porVencer: ItemCobranza[] = r.cuotas_por_vencer.map(c => ({ ...c, tipo: 'por_vencer' as const }))
  return [...vencidas, ...porVencer]
    .sort((a, b) => {
      if (a.tipo !== b.tipo) return a.tipo === 'moroso' ? -1 : 1
      return b.dias_atraso - a.dias_atraso
    })
})

const itemsFiltrados = computed(() => {
  if (filtroTipo.value === 'todos') return items.value
  return items.value.filter(i => i.tipo === (filtroTipo.value === 'morosos' ? 'moroso' : 'por_vencer'))
})

const estadisticas = computed(() => ({
  total: items.value.length,
  morosos: items.value.filter(i => i.tipo === 'moroso').length,
  porVencer: items.value.filter(i => i.tipo === 'por_vencer').length,
  montoMoroso: items.value.filter(i => i.tipo === 'moroso').reduce((s, i) => s + (i.saldo ?? 0) + (i.mora ?? 0), 0),
  montoPorVencer: items.value.filter(i => i.tipo === 'por_vencer').reduce((s, i) => s + i.valor_cuota, 0)
}))

function accionSugerida(item: ItemCobranza): string {
  if (item.tipo === 'por_vencer') return 'Seguimiento'
  if (item.dias_atraso <= 3) return 'Recordatorio'
  if (item.dias_atraso <= 15) return 'Llamada de cobro'
  return 'Gestión de cobro'
}

async function abrirPago(prestamoId: number, cuotaId: number) {
  try {
    await byId(prestamoId)
    prestamoSeleccionado.value = detalle.value
    cuotaSeleccionada.value = detalle.value?.cuotas.find(c => c.id === cuotaId) ?? null
    if (!cuotaSeleccionada.value) {
      toast.add({ title: 'La cuota ya no está disponible', color: 'error' })
      return
    }
    pagoAbierto.value = true
  } catch {
    toast.add({ title: 'No se pudo cargar el préstamo', color: 'error' })
  }
}

function abrirNotas(prestamoId: number) {
  prestamoNotas.value = prestamoId
  notasAbiertas.value = true
}

async function despuesDePago() {
  pagoAbierto.value = false
  await cargarDatos()
}

cargarDatos()
</script>

<template>
  <div class="p-6 space-y-6">
    <UiPageHeader
      titulo="Cobranza"
      descripcion="Agenda de cuotas vencidas con saldo, acción sugerida y pago directo."
      icono="i-lucide-trending-up"
    >
      <template #actions>
        <UButton
          icon="i-lucide-refresh-cw"
          color="neutral"
          variant="outline"
          :loading="loading"
          label="Actualizar"
          @click="cargarDatos"
        />
      </template>
    </UiPageHeader>

    <UAlert
      v-if="error"
      icon="i-lucide-alert-triangle"
      color="error"
      :title="error"
      :actions="[{ label: 'Reintentar', color: 'primary', variant: 'outline', onClick: cargarDatos }]"
    />

    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div class="p-4 rounded-lg bg-gray-50 dark:bg-gray-800">
        <div class="text-2xl font-bold">
          {{ estadisticas.total }}
        </div>
        <div class="text-sm text-gray-500">
          Total acciones
        </div>
      </div>
      <div class="p-4 rounded-lg bg-error/10">
        <div class="text-2xl font-bold text-error">
          {{ estadisticas.morosos }}
        </div>
        <div class="text-sm text-gray-500">
          Vencidas
        </div>
      </div>
      <div class="p-4 rounded-lg bg-warning/10">
        <div class="text-2xl font-bold text-warning">
          {{ estadisticas.porVencer }}
        </div>
        <div class="text-sm text-gray-500">
          Por vencer
        </div>
      </div>
      <div class="p-4 rounded-lg bg-gray-50 dark:bg-gray-800">
        <div class="text-2xl font-bold">
          {{ formatoMoneda(estadisticas.montoMoroso) }}
        </div>
        <div class="text-sm text-gray-500">
          Saldo vencido
        </div>
      </div>
    </div>

    <UCard>
      <div class="flex flex-wrap items-center gap-3">
        <USelect
          v-model="filtroTipo"
          class="w-40"
          :items="[
            { label: 'Todos', value: 'todos' },
            { label: 'Vencidas', value: 'morosos' },
            { label: 'Por vencer', value: 'por_vencer' }
          ]"
        />
        <span class="text-sm text-gray-500">
          {{ itemsFiltrados.length }} cuotas
        </span>
      </div>
    </UCard>

    <UCard>
      <EmptyState
        v-if="!itemsFiltrados.length && !loading && !error"
        icono="i-lucide-check-circle"
        titulo="Sin acciones pendientes"
        :descripcion="`No hay cuotas vencidas ni por vencer al ${formatoFecha(new Date())}.`"
      />

      <USkeleton
        v-else-if="loading"
        class="h-75 rounded-lg"
      />

      <UTable
        v-else
        sticky
        :data="itemsFiltrados.map(i => ({
          prestamoId: i.prestamo_id,
          cuotaId: i.cuota_id,
          cliente: i.cliente_nombre,
          prestamo: `#${i.prestamo_id}`,
          cuota: i.numero_cuota,
          vencimiento: formatoFecha(i.fecha_vencimiento),
          saldo: formatoMoneda(i.saldo ?? i.valor_cuota),
          mora: formatoMoneda(i.mora ?? 0),
          total: formatoMoneda((i.saldo ?? i.valor_cuota) + (i.mora ?? 0)),
          dias: i.tipo === 'moroso' ? `${i.dias_atraso} días de atraso` : 'Por vencer',
          accion: accionSugerida(i)
        })) as unknown as Record<string, unknown>[]"
        :columns="[
          { accessorKey: 'cliente', header: 'Cliente' },
          { accessorKey: 'prestamo', header: 'Préstamo' },
          { accessorKey: 'cuota', header: 'Cuota' },
          { accessorKey: 'vencimiento', header: 'Vencimiento' },
          { accessorKey: 'saldo', header: 'Saldo' },
          { accessorKey: 'mora', header: 'Mora' },
          { accessorKey: 'total', header: 'Total' },
          { accessorKey: 'dias', header: 'Estado' },
          { accessorKey: 'accion', header: 'Acción sugerida' },
          { accessorKey: 'acciones', header: 'Acción' }
        ]"
      >
        <template #acciones-cell="{ row }">
          <div
            v-if="row.original"
            class="flex gap-1"
          >
            <UButton
              icon="i-lucide-credit-card"
              color="primary"
              variant="ghost"
              size="xs"
              label="Pagar"
              @click="abrirPago(Number(row.original.prestamoId), Number(row.original.cuotaId))"
            />
            <UButton
              icon="i-lucide-message-square"
              color="neutral"
              variant="ghost"
              size="xs"
              label="Contacto"
              @click="abrirNotas(Number(row.original.prestamoId))"
            />
          </div>
        </template>
      </UTable>
    </UCard>

    <PrestamoPagoModal
      :open="pagoAbierto"
      :prestamo="prestamoSeleccionado"
      :cuota="cuotaSeleccionada"
      @update:open="pagoAbierto = $event"
      @pagado="despuesDePago"
    />

    <NotaContactoModal
      :open="notasAbiertas"
      :prestamo-id="prestamoNotas"
      @update:open="notasAbiertas = $event"
    />
  </div>
</template>
