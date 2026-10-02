<script setup lang="ts">
import type { PrestamoCuota } from '#shared/types/prestamo_cuota'
import type { PrestamoDetalle } from '#shared/types/prestamo'
import { usePrestamos } from '~/composables/domain/usePrestamos'
import PrestamoPagoModal from '~/components/prestamos/PrestamoPagoModal.vue'
import { formatoFecha } from '~/utils/fecha'
import { formatoMoneda } from '~/utils/format'
import EmptyState from '~/components/ui/EmptyState.vue'

definePageMeta({
  middleware: 'auth'
})

const { prestamos, fetch: fetchPrestamos, byId, detalle } = usePrestamos()
const toast = useToast()

const loading = ref(false)
const filtroTipo = ref<'todos' | 'por_vencer' | 'morosos'>('todos')
const filtroDias = ref(30)

const pagoAbierto = ref(false)
const prestamoSeleccionado = ref<PrestamoDetalle | null>(null)
const cuotaSeleccionada = ref<PrestamoCuota | null>(null)

interface ItemCobranza {
  prestamoId: number
  cuota: PrestamoCuota
  tipo: 'por_vencer' | 'moroso'
  dias: number
  total: number
}

const hoy = new Date()

async function cargarDatos() {
  loading.value = true
  try {
    await fetchPrestamos({ estado: 'activo', limit: 100 })
  } finally {
    loading.value = false
  }
}

const items = computed<ItemCobranza[]>(() => {
  const resultado: ItemCobranza[] = []
  for (const p of prestamos.value) {
    if (!p) continue
    const detalle = (p as unknown as { cuotas?: PrestamoCuota[] }).cuotas
    if (!detalle) continue
    for (const cuota of detalle) {
      if (cuota.estado !== 'pendiente' && cuota.estado !== 'vencido') continue
      const venc = new Date(cuota.fecha_vencimiento)
      const diffMs = hoy.getTime() - venc.getTime()
      const diffDias = Math.ceil(diffMs / (1000 * 60 * 60 * 24))

      if (diffDias > 0) {
        resultado.push({
          prestamoId: p.id,
          cuota,
          tipo: 'moroso',
          dias: diffDias,
          total: cuota.valor_cuota + cuota.mora
        })
      } else if (diffDias < 0 && Math.abs(diffDias) <= filtroDias.value) {
        resultado.push({
          prestamoId: p.id,
          cuota,
          tipo: 'por_vencer',
          dias: Math.abs(diffDias),
          total: cuota.valor_cuota
        })
      }
    }
  }
  return resultado.sort((a, b) => {
    if (a.tipo !== b.tipo) return a.tipo === 'moroso' ? -1 : 1
    return b.dias - a.dias
  })
})

const itemsFiltrados = computed(() => {
  if (filtroTipo.value === 'todos') return items.value
  return items.value.filter(i => i.tipo === filtroTipo.value)
})

const estadisticas = computed(() => ({
  total: items.value.length,
  morosos: items.value.filter(i => i.tipo === 'moroso').length,
  porVencer: items.value.filter(i => i.tipo === 'por_vencer').length,
  montoMoroso: items.value.filter(i => i.tipo === 'moroso').reduce((s, i) => s + i.total, 0),
  montoPorVencer: items.value.filter(i => i.tipo === 'por_vencer').reduce((s, i) => s + i.total, 0)
}))

async function abrirPago(item: ItemCobranza) {
  try {
    await byId(item.prestamoId)
    prestamoSeleccionado.value = detalle.value
    cuotaSeleccionada.value = item.cuota
    pagoAbierto.value = true
  } catch {
    toast.add({ title: 'No se pudo cargar el préstamo', color: 'error' })
  }
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
      descripcion="Acciones de cobranza consolidadas con pago directo."
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
          Morosos
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
          Monto moroso
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
            { label: 'Morosos', value: 'morosos' },
            { label: 'Por vencer', value: 'por_vencer' }
          ]"
        />
        <USelect
          v-if="filtroTipo !== 'morosos'"
          v-model="filtroDias"
          class="w-36"
          :items="[
            { label: '7 días', value: 7 },
            { label: '15 días', value: 15 },
            { label: '30 días', value: 30 }
          ]"
        />
        <span class="text-sm text-gray-500">
          {{ itemsFiltrados.length }} cuotas
        </span>
      </div>
    </UCard>

    <UCard>
      <EmptyState
        v-if="!itemsFiltrados.length && !loading"
        icono="i-lucide-check-circle"
        titulo="Sin acciones pendientes"
        descripcion="No hay cuotas por vencer ni morosos."
      />

      <USkeleton
        v-else-if="loading"
        class="h-75 rounded-lg"
      />

      <UTable
        v-else
        sticky
        :data="itemsFiltrados.map(i => ({
          prestamoId: i.prestamoId,
          cuota: i.cuota.numero_cuota,
          vencimiento: formatoFecha(i.cuota.fecha_vencimiento),
          valor: formatoMoneda(i.cuota.valor_cuota),
          mora: formatoMoneda(i.cuota.mora),
          total: formatoMoneda(i.total),
          dias: i.tipo === 'moroso' ? `${i.dias} días atraso` : `${i.dias} días`,
          tipo: i.tipo === 'moroso' ? 'Moroso' : 'Por vencer'
        })) as unknown as Record<string, unknown>[]"
        :columns="[
          { accessorKey: 'prestamoId', header: 'Préstamo' },
          { accessorKey: 'cuota', header: 'Cuota' },
          { accessorKey: 'vencimiento', header: 'Vencimiento' },
          { accessorKey: 'valor', header: 'Valor cuota' },
          { accessorKey: 'mora', header: 'Mora' },
          { accessorKey: 'total', header: 'Total' },
          { accessorKey: 'dias', header: 'Estado' },
          { accessorKey: 'tipo', header: 'Tipo' },
          { accessorKey: 'acciones', header: 'Acción' }
        ]"
      >
        <template #acciones-cell="{ row }">
          <UButton
            v-if="row.original"
            icon="i-lucide-credit-card"
            color="primary"
            variant="ghost"
            size="xs"
            label="Pagar"
            @click="abrirPago(row.original as unknown as ItemCobranza)"
          />
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
  </div>
</template>
