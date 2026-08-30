<script setup lang="ts">
import type { PagoCreate } from '#shared/types/pago'
import type { PrestamoDetalle } from '#shared/types/prestamo'
import type { PrestamoCuota } from '#shared/types/prestamo_cuota'
import { usePagos } from '~/composables/domain/usePagos'
import { useTiposPago } from '~/composables/domain/useTipos'
import { usePrestamos } from '~/composables/domain/usePrestamos'
import DataTable from '~/components/ui/DataTable.vue'
import PagoForm from '~/components/pagos/PagoForm.vue'

definePageMeta({
  middleware: 'auth'
})

const route = useRoute()
const router = useRouter()
const toast = useToast()

const { pagos, loading, error, fetch: fetchPagos, crear } = usePagos()
const { tipos: tiposPago, fetch: fetchTiposPago } = useTiposPago()
const { byId, detalle } = usePrestamos()

const tabActiva = ref<'registrar' | 'historial'>(
  route.query.tab === 'historial' ? 'historial' : 'registrar'
)
const formRef = ref<{ submit: () => void } | null>(null)
const prestamoInicial = ref<PrestamoDetalle | null>(null)
const cuotaInicial = ref<PrestamoCuota | null>(null)

async function inicializar() {
  await Promise.all([fetchTiposPago(), fetchPagos()])
  console.log(tiposPago.value)
  if (route.query.prestamo_id) {
    const id = Number(route.query.prestamo_id)
    try {
      await byId(id)
      prestamoInicial.value = detalle.value
      if (route.query.cuota_id && detalle.value) {
        const cuotaId = Number(route.query.cuota_id)
        cuotaInicial.value = (detalle.value.cuotas.find((c: PrestamoCuota) => c.id === cuotaId) as PrestamoCuota) ?? null
      }
      tabActiva.value = 'registrar'
    } catch {
      toast.add({ title: 'No se pudo cargar el préstamo', color: 'error' })
    }
  }
}
inicializar()

async function guardar(data: PagoCreate) {
  try {
    await crear(data)
    toast.add({ title: 'Pago registrado correctamente', color: 'success' })
    prestamoInicial.value = null
    cuotaInicial.value = null
  } catch (e) {
    const err = e as { status: number, detail: string }
    toast.add({ title: err.detail || 'No se pudo registrar el pago', color: 'error' })
  }
}

const columnsHistorial = [
  {
    header: 'Fecha',
    cell: (row: Record<string, unknown>) => formatoFecha(String(row.fecha_pago))
  },
  {
    header: 'Préstamo',
    cell: (row: Record<string, unknown>) => `#${String(row.prestamo_id ?? '')}`
  },
  {
    header: 'Cuota',
    cell: (row: Record<string, unknown>) => `#${String(row.cuota_id ?? '')}`
  },
  {
    header: 'Tipo',
    accessorKey: 'tipo_pago_id'
  },
  {
    header: 'Valor',
    cell: (row: Record<string, unknown>) => formatoMoneda(Number(row.valor_pagado))
  },
  {
    header: 'Capital',
    cell: (row: Record<string, unknown>) => formatoMoneda(Number(row.capital_pagado))
  },
  {
    header: 'Interés',
    cell: (row: Record<string, unknown>) => formatoMoneda(Number(row.interes_pagado))
  },
  {
    header: 'Mora',
    cell: (row: Record<string, unknown>) => formatoMoneda(Number(row.mora_pagada))
  }
]
</script>

<template>
  <div class="p-6 space-y-4">
    <div class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <h1 class="text-2xl font-bold">
          Pagos
        </h1>
        <p class="text-sm text-gray-500">
          Registro de pagos y historial.
        </p>
      </div>
    </div>

    <UTabs
      v-model="tabActiva"
      :items="[
        { label: 'Registrar pago', value: 'registrar', icon: 'i-lucide-plus-circle', slot: 'registrar' },
        { label: 'Historial', value: 'historial', icon: 'i-lucide-history', slot: 'historial' }
      ]"
    >
      <template #registrar>
        <UCard>
          <template #header>
            <h3 class="font-bold">
              Nuevo pago
            </h3>
          </template>

          <PagoForm
            ref="formRef"
            :prestamo-inicial="prestamoInicial"
            :cuota-inicial="cuotaInicial"
            :tipos-pago="tiposPago"
            @guardar="guardar"
          />

          <template #footer>
            <div class="flex justify-end gap-2">
              <UButton
                label="Cancelar"
                color="neutral"
                variant="outline"
                @click="router.back()"
              />
              <UButton
                label="Registrar pago"
                color="primary"
                icon="i-lucide-check"
                @click="formRef?.submit()"
              />
            </div>
          </template>
        </UCard>
      </template>

      <template #historial>
        <DataTable
          titulo="Historial de pagos"
          :data="pagos as Record<string, unknown>[]"
          :columns="columnsHistorial"
          :loading="loading"
          :error="error"
          exportar-nombre="pagos"
          @retry="fetchPagos"
        />
      </template>
    </UTabs>
  </div>
</template>
