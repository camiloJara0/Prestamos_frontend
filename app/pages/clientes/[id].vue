<script setup lang="ts">
import type { Cliente } from '#shared/types/clientes'
import type { Prestamo } from '#shared/types/prestamo'
import type { Pago } from '#shared/types/pago'
import { getClienteById } from '~/services/api/clientes'
import { getPrestamos } from '~/services/api/prestamo'
import { getPagos } from '~/services/api/pago'
import EstadoBadge from '~/components/ui/EstadoBadge.vue'
import { UButton } from '#components'
import EmptyState from '~/components/ui/EmptyState.vue'

definePageMeta({
  middleware: 'auth'
})

const route = useRoute()
const router = useRouter()
const formateo = useFormatters()

const clienteId = computed(() => Number(route.params.id))

const cliente = ref<Cliente | null>(null)
const prestamos = ref<Prestamo[]>([])
const pagos = ref<Pago[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const tab = ref('datos')

async function inicializar() {
  loading.value = true
  error.value = null
  try {
    const [datosCliente, listaPrestamos, listaPagos] = await Promise.all([
      getClienteById(clienteId.value),
      getPrestamos({ cliente_id: clienteId.value, estado: 'todos', limit: 100 }),
      getPagos({ cliente_id: clienteId.value, limit: 50 })
    ])
    cliente.value = datosCliente
    prestamos.value = listaPrestamos.items
    pagos.value = listaPagos.items
  } catch (e) {
    error.value = (e as { detail?: string }).detail || 'No se pudo cargar el cliente.'
  } finally {
    loading.value = false
  }
}
inicializar()

const prestamosActivos = computed(() => prestamos.value.filter(p => p.estado === 'activo'))
const prestamosCerrados = computed(() => prestamos.value.filter(p => p.estado !== 'activo'))
const sinOperacion = computed(() => !prestamos.value.length && !pagos.value.length)

const itemsTabs = [
  { label: 'Datos personales', value: 'datos', icon: 'i-lucide-user', slot: 'datos' },
  { label: 'Préstamos', value: 'prestamos', icon: 'i-lucide-hand-coins', slot: 'prestamos' },
  { label: 'Pagos recientes', value: 'pagos', icon: 'i-lucide-receipt', slot: 'pagos' }
]

function verPrestamo(id: number) {
  router.push(`/prestamos/${id}`)
}

const filasActivos = computed(() => prestamosActivos.value.map(p => ({
  id: p.id,
  fecha: formateo.formatoFecha(p.fecha_prestamo),
  capital: formateo.formatoMoneda(p.capital_prestado),
  saldo: formateo.formatoMoneda(p.saldo_pendiente),
  cuotas: p.numero_cuotas,
  estado: p.estado
})))

const filasCerrados = computed(() => prestamosCerrados.value.map(p => ({
  id: p.id,
  fecha: formateo.formatoFecha(p.fecha_prestamo),
  capital: formateo.formatoMoneda(p.capital_prestado),
  monto: formateo.formatoMoneda(p.monto_total),
  cuotas: p.numero_cuotas,
  estado: p.estado
})))

const filasPagos = computed(() => pagos.value.map(p => ({
  fecha: formateo.formatoFecha(p.fecha_pago),
  prestamo: `#${p.prestamo_id}`,
  recibo: p.referencia_recibo ?? '—',
  valor: formateo.formatoMoneda(p.valor_pagado),
  capital: formateo.formatoMoneda(p.capital_pagado),
  interes: formateo.formatoMoneda(p.interes_pagado),
  mora: formateo.formatoMoneda(p.mora_pagada),
  estado: p.estado_pago ?? 'confirmado'
})))

const columnsActivos = [
  { accessorKey: 'id', header: 'ID' },
  { accessorKey: 'fecha', header: 'Fecha' },
  { accessorKey: 'capital', header: 'Capital' },
  { accessorKey: 'saldo', header: 'Saldo' },
  { accessorKey: 'cuotas', header: 'Cuotas' },
  { accessorKey: 'estado', header: 'Estado' },
  { accessorKey: 'acciones', header: 'Ver' }
]

const columnsCerrados = [
  { accessorKey: 'id', header: 'ID' },
  { accessorKey: 'fecha', header: 'Fecha' },
  { accessorKey: 'capital', header: 'Capital' },
  { accessorKey: 'monto', header: 'Monto total' },
  { accessorKey: 'cuotas', header: 'Cuotas' },
  { accessorKey: 'estado', header: 'Estado' },
  { accessorKey: 'acciones', header: 'Ver' }
]

const columnsPagos = [
  { accessorKey: 'fecha', header: 'Fecha' },
  { accessorKey: 'prestamo', header: 'Préstamo' },
  { accessorKey: 'recibo', header: 'Recibo' },
  { accessorKey: 'valor', header: 'Valor' },
  { accessorKey: 'capital', header: 'Capital' },
  { accessorKey: 'interes', header: 'Interés' },
  { accessorKey: 'mora', header: 'Mora' },
  { accessorKey: 'estado', header: 'Estado' }
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

    <template v-else-if="cliente">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <div class="flex items-center gap-3">
          <UButton
            icon="i-lucide-arrow-left"
            color="neutral"
            variant="ghost"
            @click="() => { router.push('/clientes') }"
          />
          <div>
            <h1 class="text-2xl font-bold">
              {{ cliente.nombre }}
            </h1>
            <p class="text-sm text-gray-500">
              C.C {{ cliente.cedula }} · {{ cliente.telefono ?? 'Sin teléfono' }}
            </p>
          </div>
          <EstadoBadge
            entidad="cliente"
            :estado="cliente.estado ?? 'activo'"
          />
        </div>
      </div>

      <UTabs
        v-model="tab"
        :items="itemsTabs"
      >
        <template #datos>
          <UCard v-if="tab === 'datos'">
            <dl class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-x-6 gap-y-4">
              <div>
                <dt class="text-xs uppercase tracking-wide text-gray-400">
                  Nombre completo
                </dt>
                <dd class="font-medium">
                  {{ cliente.nombre }}
                </dd>
              </div>
              <div>
                <dt class="text-xs uppercase tracking-wide text-gray-400">
                  Cédula
                </dt>
                <dd class="font-medium">
                  {{ cliente.cedula }}
                </dd>
              </div>
              <div>
                <dt class="text-xs uppercase tracking-wide text-gray-400">
                  Teléfono
                </dt>
                <dd class="font-medium">
                  {{ cliente.telefono ?? '—' }}
                </dd>
              </div>
              <div>
                <dt class="text-xs uppercase tracking-wide text-gray-400">
                  Dirección
                </dt>
                <dd class="font-medium">
                  {{ cliente.direccion ?? '—' }}
                </dd>
              </div>
              <div>
                <dt class="text-xs uppercase tracking-wide text-gray-400">
                  Persona de referencia
                </dt>
                <dd class="font-medium">
                  {{ cliente.persona_referencia ?? '—' }}{{ cliente.telefono_referencia ? ` · ${cliente.telefono_referencia}` : '' }}
                </dd>
              </div>
              <div>
                <dt class="text-xs uppercase tracking-wide text-gray-400">
                  Estado
                </dt>
                <dd class="font-medium capitalize">
                  {{ cliente.estado ?? 'activo' }}
                </dd>
              </div>
              <div class="sm:col-span-2 lg:col-span-3">
                <dt class="text-xs uppercase tracking-wide text-gray-400">
                  Observaciones
                </dt>
                <dd class="font-medium whitespace-pre-wrap">
                  {{ cliente.observaciones ?? '—' }}
                </dd>
              </div>
            </dl>
          </UCard>
        </template>

        <template #prestamos>
          <div
            v-if="tab === 'prestamos'"
            class="space-y-4"
          >
            <EmptyState
              v-if="sinOperacion"
              icono="i-lucide-folder-open"
              titulo="Sin operaciones registradas"
              descripcion="Este cliente aún no tiene préstamos ni pagos asociados."
            />

            <template v-else>
              <UCard>
                <template #header>
                  <h3 class="font-bold">
                    Préstamos activos ({{ prestamosActivos.length }})
                  </h3>
                </template>
                <EmptyState
                  v-if="!prestamosActivos.length"
                  icono="i-lucide-hand-coins"
                  titulo="Sin préstamos activos"
                  descripcion="Este cliente no tiene préstamos en curso."
                />
                <UTable
                  v-else
                  :data="filasActivos"
                  :columns="columnsActivos"
                >
                  <template #estado-cell="{ row }">
                    <EstadoBadge
                      entidad="prestamo"
                      :estado="String(row.original?.estado ?? 'activo')"
                    />
                  </template>
                  <template #acciones-cell="{ row }">
                    <UButton
                      icon="i-lucide-eye"
                      size="xs"
                      color="primary"
                      variant="ghost"
                      label="Detalle"
                      @click="verPrestamo(Number(row.original?.id))"
                    />
                  </template>
                </UTable>
              </UCard>

              <UCard>
                <template #header>
                  <h3 class="font-bold">
                    Préstamos cerrados ({{ prestamosCerrados.length }})
                  </h3>
                </template>
                <EmptyState
                  v-if="!prestamosCerrados.length"
                  icono="i-lucide-archive"
                  titulo="Sin préstamos cerrados"
                  descripcion="Este cliente no tiene préstamos pagados, perdidos o renovados."
                />
                <UTable
                  v-else
                  :data="filasCerrados"
                  :columns="columnsCerrados"
                >
                  <template #estado-cell="{ row }">
                    <EstadoBadge
                      entidad="prestamo"
                      :estado="String(row.original?.estado ?? 'activo')"
                    />
                  </template>
                  <template #acciones-cell="{ row }">
                    <UButton
                      icon="i-lucide-eye"
                      size="xs"
                      color="primary"
                      variant="ghost"
                      label="Detalle"
                      @click="verPrestamo(Number(row.original?.id))"
                    />
                  </template>
                </UTable>
              </UCard>
            </template>
          </div>
        </template>

        <template #pagos>
          <UCard v-if="tab === 'pagos'">
            <EmptyState
              v-if="!pagos.length"
              icono="i-lucide-receipt"
              titulo="Sin pagos registrados"
              descripcion="Este cliente aún no registra abonos."
            />
            <UTable
              v-else
              :data="filasPagos"
              :columns="columnsPagos"
            />
            <p
              v-if="pagos.length >= 50"
              class="text-xs text-gray-400 pt-3"
            >
              Mostrando los 50 pagos más recientes.
            </p>
          </UCard>
        </template>
      </UTabs>
    </template>
  </div>
</template>
