<script setup lang="ts">
import type { EstadoPrestamo } from '#shared/types/prestamo'
import { usePrestamos } from '~/composables/domain/usePrestamos'
import { UiEstadoBadge, UButton } from '#components'
import DataTable from '~/components/ui/DataTable.vue'

definePageMeta({
  middleware: 'auth'
})

const { prestamos, loading, error, filtros, fetch, setFiltros } = usePrestamos()
const router = useRouter()

const formateo = useFormatters()

const estadoSeleccionado = ref<string>('activo')
const busqueda = ref('')
const fechaDesde = ref('')
const fechaHasta = ref('')

async function aplicarFiltros() {
  setFiltros({
    estado: (estadoSeleccionado.value === 'todos' ? 'todos' : estadoSeleccionado.value) as EstadoPrestamo | 'todos',
    busqueda: busqueda.value || undefined,
    fecha_desde: fechaDesde.value || undefined,
    fecha_hasta: fechaHasta.value || undefined,
    skip: 0,
    limit: 50
  })
  await fetch()
}

function limpiarFiltros() {
  estadoSeleccionado.value = 'activo'
  busqueda.value = ''
  fechaDesde.value = ''
  fechaHasta.value = ''
  aplicarFiltros()
}

async function inicializar() {
  await fetch()
}
inicializar()

async function cargarMas() {
  setFiltros({ skip: (filtros.value.skip ?? 0) + (filtros.value.limit ?? 50) })
  await fetch()
}

function verDetalle(prestamoId: number) {
  router.push(`/prestamos/${prestamoId}`)
}

const columns = [
  { accessorKey: 'id', header: 'ID', sorted: true },
  {
    header: 'Cliente',
    cell: (row: Record<string, unknown>) => `#${String(row.cliente_id ?? '')}`
  },
  {
    header: 'Fecha',
    cell: (row: Record<string, unknown>) => formateo.formatoFecha(String(row.fecha_prestamo))
  },
  {
    header: 'Capital',
    cell: (row: Record<string, unknown>) => formateo.formatoMoneda(Number(row.capital_prestado))
  },
  {
    header: 'Monto total',
    cell: (row: Record<string, unknown>) => formateo.formatoMoneda(Number(row.monto_total))
  },
  {
    header: 'Saldo',
    cell: (row: Record<string, unknown>) => formateo.formatoMoneda(Number(row.saldo_pendiente))
  },
  {
    header: 'Cuota',
    cell: (row: Record<string, unknown>) => formateo.formatoMoneda(Number(row.valor_cuota))
  },
  {
    header: 'N° cuotas',
    accessorKey: 'numero_cuotas'
  },
  {
    header: 'Estado',
    component: UiEstadoBadge,
    componentProps: (row: Record<string, unknown>) => ({ entidad: 'prestamo', estado: String(row.estado ?? '') })
  },
  {
    header: 'Ver',
    component: UButton,
    componentProps: (row: Record<string, unknown>) => ({
      icon: 'i-lucide-eye',
      size: 'xs',
      color: 'primary',
      variant: 'ghost',
      label: 'Detalle',
      onClick: () => verDetalle(Number(row.id))
    })
  }
]

const filtroGlobal = (row: Record<string, unknown>, termino: string) => {
  return String(row.id ?? '').includes(termino)
    || String(row.cliente_id ?? '').includes(termino)
}
</script>

<template>
  <div class="p-6 space-y-4">
    <div class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <h1 class="text-2xl font-bold">
          Préstamos
        </h1>
        <p class="text-sm text-gray-500">
          Listado de préstamos con filtros.
        </p>
      </div>
      <UButton
        color="primary"
        icon="i-lucide-plus"
        to="/prestamos/nuevo"
      >
        Nuevo préstamo
      </UButton>
    </div>

    <UCard>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
        <UFormField label="Estado">
          <USelect
            v-model="estadoSeleccionado"
            :items="[
              { label: 'Todos', value: 'todos' },
              { label: 'Activo', value: 'activo' },
              { label: 'Pagado', value: 'pagado' },
              { label: 'Perdido', value: 'perdido' },
              { label: 'Renovado', value: 'renovado' }
            ]"
            class="w-full"
          />
        </UFormField>
        <UFormField label="Búsqueda">
          <UInput
            v-model="busqueda"
            placeholder="Nombre o cédula"
            icon="i-lucide-search"
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

    <DataTable
      titulo="Resultados"
      :data="prestamos as unknown as Record<string, unknown>[]"
      :columns="columns"
      :loading="loading"
      :error="error"
      :filtro-global="filtroGlobal"
      :llamar-datos="() => fetch()"
      exportar-nombre="prestamos"
      @retry="fetch"
    />

    <div class="text-center">
      <UButton
        v-if="prestamos.length"
        color="neutral"
        variant="outline"
        icon="i-lucide-chevron-down"
        label="Cargar más"
        @click="cargarMas"
      />
    </div>
  </div>
</template>
