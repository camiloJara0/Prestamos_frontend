<script setup lang="ts">
import { usePagos } from '~/composables/domain/usePagos'
import { useTiposPago } from '~/composables/domain/useTipos'
import { getClientes } from '~/services/api/clientes'
import EmptyState from '~/components/ui/EmptyState.vue'

definePageMeta({
  middleware: 'auth'
})

const formateo = useFormatters()
const { pagos, paginacion, loading, error, fetch, cambiarPagina } = usePagos()
const { tipos: tiposPago, fetch: fetchTiposPago } = useTiposPago()

const opcionesClientes = ref<{ label: string, value: number }[]>([])
const opcionesTipos = ref<{ label: string, value: number }[]>([])

const filtroCliente = ref(0)
const filtroTipo = ref(0)
const fechaDesde = ref('')
const fechaHasta = ref('')

async function cargarOpciones() {
  try {
    const [clientes] = await Promise.all([
      getClientes({ page: 1, limit: 100 }),
      fetchTiposPago()
    ])
    opcionesClientes.value = [
      { label: 'Todos los clientes', value: 0 },
      ...clientes.items.map(c => ({ label: `${c.nombre} (${c.cedula})`, value: c.id }))
    ]
    opcionesTipos.value = [
      { label: 'Todos los tipos', value: 0 },
      ...tiposPago.value.map(t => ({ label: t.nombre, value: t.id }))
    ]
  } catch {
    opcionesClientes.value = [{ label: 'Todos los clientes', value: 0 }]
    opcionesTipos.value = [{ label: 'Todos los tipos', value: 0 }]
  }
}

async function aplicarFiltros() {
  await fetch({
    page: 1,
    limit: 50,
    cliente_id: filtroCliente.value > 0 ? filtroCliente.value : undefined,
    tipo_pago_id: filtroTipo.value > 0 ? filtroTipo.value : undefined,
    fecha_desde: fechaDesde.value || undefined,
    fecha_hasta: fechaHasta.value || undefined
  })
}

function limpiarFiltros() {
  filtroCliente.value = 0
  filtroTipo.value = 0
  fechaDesde.value = ''
  fechaHasta.value = ''
  aplicarFiltros()
}

function irAPagina(page: number) {
  cambiarPagina(page)
}

async function inicializar() {
  await Promise.all([fetch({ page: 1, limit: 50 }), cargarOpciones()])
}
inicializar()

const filas = computed(() => pagos.value.map(p => ({
  fecha: formateo.formatoFecha(p.fecha_pago),
  cliente: p.cliente_nombre ?? `#${p.cliente_id}`,
  prestamo: `#${p.prestamo_id}`,
  cuota: p.cuota_id ? `#${p.cuota_id}` : '—',
  tipo: p.tipo_pago_nombre ?? `#${p.tipo_pago_id}`,
  recibo: p.referencia_recibo ?? '—',
  valor: formateo.formatoMoneda(p.valor_pagado),
  capital: formateo.formatoMoneda(p.capital_pagado),
  interes: formateo.formatoMoneda(p.interes_pagado),
  mora: formateo.formatoMoneda(p.mora_pagada),
  estado: p.estado_pago ?? 'confirmado'
})))

const columns = [
  { accessorKey: 'fecha', header: 'Fecha' },
  { accessorKey: 'cliente', header: 'Cliente' },
  { accessorKey: 'prestamo', header: 'Préstamo' },
  { accessorKey: 'cuota', header: 'Cuota' },
  { accessorKey: 'tipo', header: 'Tipo' },
  { accessorKey: 'recibo', header: 'Recibo' },
  { accessorKey: 'valor', header: 'Valor' },
  { accessorKey: 'capital', header: 'Capital' },
  { accessorKey: 'interes', header: 'Interés' },
  { accessorKey: 'mora', header: 'Mora' },
  { accessorKey: 'estado', header: 'Estado' }
]
</script>

<template>
  <div class="p-6 space-y-4">
    <UiPageHeader
      titulo="Historial de pagos"
      descripcion="Pagos de toda la operación con filtros por cliente, fecha y tipo."
      icono="i-lucide-receipt"
    >
      <template #actions>
        <UButton
          color="neutral"
          variant="outline"
          icon="i-lucide-refresh-cw"
          :loading="loading"
          label="Actualizar"
          @click="aplicarFiltros"
        />
      </template>
    </UiPageHeader>

    <UCard>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
        <UFormField label="Cliente">
          <USelect
            v-model="filtroCliente"
            :items="opcionesClientes"
            class="w-full"
          />
        </UFormField>
        <UFormField label="Tipo de pago">
          <USelect
            v-model="filtroTipo"
            :items="opcionesTipos"
            class="w-full"
          />
        </UFormField>
        <UFormField label="Desde">
          <UInput
            v-model="fechaDesde"
            type="date"
            class="w-full"
          />
        </UFormField>
        <UFormField label="Hasta">
          <UInput
            v-model="fechaHasta"
            type="date"
            class="w-full"
          />
        </UFormField>
        <div class="flex items-end gap-2">
          <UButton
            color="primary"
            icon="i-lucide-search"
            @click="aplicarFiltros"
          >
            Filtrar
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
      </div>
    </UCard>

    <UCard>
      <UAlert
        v-if="error"
        icon="i-lucide-alert-triangle"
        color="error"
        :title="error"
        :actions="[{ label: 'Reintentar', color: 'primary', variant: 'outline', onClick: aplicarFiltros }]"
      />

      <EmptyState
        v-else-if="!loading && !pagos.length"
        icono="i-lucide-receipt"
        titulo="Sin pagos registrados"
        descripcion="No hay pagos que coincidan con los filtros seleccionados."
      />

      <USkeleton
        v-else-if="loading"
        class="h-64 rounded-lg"
      />

      <UTable
        v-else
        sticky
        :data="filas"
        :columns="columns"
      />

      <div
        v-if="paginacion && paginacion.pages > 1"
        class="flex items-center justify-between pt-4"
      >
        <span class="text-sm text-gray-500">
          {{ paginacion.total }} pagos · Página {{ paginacion.page }} de {{ paginacion.pages }}
        </span>
        <div class="flex gap-2">
          <UButton
            color="neutral"
            variant="outline"
            icon="i-lucide-chevron-left"
            label="Anterior"
            :disabled="loading || paginacion.page <= 1"
            @click="irAPagina(paginacion.page - 1)"
          />
          <UButton
            color="neutral"
            variant="outline"
            label="Siguiente"
            icon-right="i-lucide-chevron-right"
            :disabled="loading || paginacion.page >= paginacion.pages"
            @click="irAPagina(paginacion.page + 1)"
          />
        </div>
      </div>
    </UCard>
  </div>
</template>
