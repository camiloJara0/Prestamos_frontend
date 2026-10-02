<script setup lang="ts">
import { z } from 'zod'
import type { MovimientoCapitalCreate, MovimientoCapital, ResumenCaja } from '#shared/types/movimiento_capital'
import { useCapital } from '~/composables/domain/useCapital'
import { getMovimientosCapital, getResumenCaja } from '~/services/api/capital'
import type { RespuestaPaginada } from '#shared/types/paginacion'
import EmptyState from '~/components/ui/EmptyState.vue'
import ConfirmDialog from '~/components/ui/ConfirmDialog.vue'
import MoneyInput from '~/components/ui/MoneyInput.vue'

definePageMeta({
  middleware: 'admin'
})

const { capital, fetch: fetchCapital, registrar } = useCapital()

const toast = useToast()
const formateo = useFormatters()

const tipoMovimiento = ref<'inversion' | 'retiro'>('inversion')
const descripcion = ref('')
const valor = ref<number | null>(null)
const fecha = ref(hoyLocal())
const enviando = ref(false)
const errorValor = ref<string | null>(null)

const movimientos = ref<RespuestaPaginada<MovimientoCapital> | null>(null)
const resumen = ref<ResumenCaja | null>(null)
const loadingHistorial = ref(false)
const paginaActual = ref(1)

const fechaDesde = ref('')
const fechaHasta = ref('')
const tipoFiltro = ref('')

function filtrosHistorial() {
  return {
    desde: fechaDesde.value || undefined,
    hasta: fechaHasta.value || undefined,
    tipo: tipoFiltro.value || undefined
  }
}

async function inicializar() {
  await Promise.all([fetchCapital(), cargarHistorial(), cargarResumen()])
}

async function cargarHistorial() {
  loadingHistorial.value = true
  try {
    movimientos.value = await getMovimientosCapital(paginaActual.value, 20, filtrosHistorial())
  } catch {
    toast.add({ title: 'No se pudo cargar el historial', color: 'error' })
  } finally {
    loadingHistorial.value = false
  }
}

async function cargarResumen() {
  try {
    const { desde, hasta } = filtrosHistorial()
    resumen.value = await getResumenCaja({ desde, hasta })
  } catch {
    resumen.value = null
  }
}

function aplicarFiltrosHistorial() {
  paginaActual.value = 1
  cargarHistorial()
  cargarResumen()
}

function limpiarFiltrosHistorial() {
  fechaDesde.value = ''
  fechaHasta.value = ''
  tipoFiltro.value = ''
  aplicarFiltrosHistorial()
}

inicializar()

const montoActual = computed(() => capital.value?.monto_total ?? 0)

const valorNumerico = computed(() => {
  if (valor.value == null) return null
  return Number.isFinite(valor.value) ? valor.value : null
})

const retiroExcede = computed(() => {
  if (tipoMovimiento.value !== 'retiro' || valorNumerico.value == null) return false
  return valorNumerico.value > montoActual.value
})

const conceptoValido = computed(() => descripcion.value.trim().length >= 5)

const puedeEnviar = computed(() => {
  return valorNumerico.value != null && valorNumerico.value > 0 && !retiroExcede.value && fecha.value !== '' && conceptoValido.value
})

const schema = z.object({
  tipo_movimiento: z.enum(['inversion', 'retiro']),
  descripcion: z.string().trim().min(5, 'El concepto es obligatorio (mínimo 5 caracteres)'),
  valor: z.number().positive('El valor debe ser mayor a 0'),
  fecha: z.string().min(1, 'La fecha es requerida')
})

watch(retiroExcede, (excede) => {
  errorValor.value = excede ? 'El retiro no puede exceder el capital disponible' : null
})

async function guardar() {
  errorValor.value = null
  const resultado = schema.safeParse({
    tipo_movimiento: tipoMovimiento.value,
    descripcion: descripcion.value.trim(),
    valor: valorNumerico.value,
    fecha: fecha.value
  })
  if (!resultado.success) {
    errorValor.value = resultado.error.issues[0]?.message ?? 'Revise los valores del formulario'
    return
  }

  enviando.value = true
  try {
    const payload: MovimientoCapitalCreate = {
      tipo_movimiento: tipoMovimiento.value,
      descripcion: descripcion.value.trim(),
      valor: valorNumerico.value as number,
      fecha: fecha.value
    }
    await registrar(payload)
    toast.add({
      title: tipoMovimiento.value === 'inversion' ? 'Inversión registrada' : 'Retiro registrado',
      color: 'success'
    })
    descripcion.value = ''
    valor.value = null
    await Promise.all([fetchCapital(), cargarHistorial(), cargarResumen()])
  } catch (e) {
    toast.add({ title: (e as { detail: string }).detail || 'No se pudo registrar el movimiento', color: 'error' })
  } finally {
    enviando.value = false
  }
}

const confirmarRetiro = ref(false)

function formatearTipo(tipo: string) {
  const map: Record<string, string> = {
    inversion: 'Inversión',
    retiro: 'Retiro',
    prestamo_otorgado: 'Préstamo otorgado',
    pago_recibido: 'Pago recibido',
    perdida: 'Pérdida',
    ajuste_prestamo: 'Ajuste de préstamo',
    devolucion_pago: 'Devolución de pago'
  }
  return map[tipo] ?? tipo
}
</script>

<template>
  <div class="p-6 space-y-6">
    <UiPageHeader
      titulo="Capital"
      descripcion="Gestión del capital disponible para préstamos."
      icono="i-lucide-wallet"
    />

    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <UiStatCard
        titulo="Capital disponible"
        :valor="formateo.formatoMoneda(montoActual)"
        icono="i-lucide-wallet"
        color="primary"
        :footer="capital?.updated_at ? `Actualizado: ${formateo.formatoFecha(capital.updated_at)}` : undefined"
      />
      <UiStatCard
        titulo="Ingresos de caja"
        :valor="formateo.formatoMoneda(resumen?.ingresos ?? 0)"
        icono="i-lucide-arrow-down-left"
        color="success"
        :footer="resumen ? `${resumen.cantidad_ingresos} movimientos · ${resumen.periodo}` : undefined"
      />
      <UiStatCard
        titulo="Egresos de caja"
        :valor="formateo.formatoMoneda(resumen?.egresos ?? 0)"
        icono="i-lucide-arrow-up-right"
        color="error"
        :footer="resumen ? `${resumen.cantidad_egresos} movimientos · ${resumen.periodo}` : undefined"
      />
    </div>

    <UCard>
      <template #header>
        <h3 class="font-bold">
          Registrar movimiento
        </h3>
      </template>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <UFormField label="Tipo de movimiento">
          <USelect
            v-model="tipoMovimiento"
            class="w-full"
            :items="[{ label: 'Inversión', value: 'inversion' }, { label: 'Retiro', value: 'retiro' }]"
          />
        </UFormField>
        <UFormField
          label="Valor"
          :error="errorValor ?? undefined"
        >
          <MoneyInput v-model="valor" />
        </UFormField>
        <UFormField label="Fecha">
          <UInput
            v-model="fecha"
            class="w-full"
            type="date"
          />
        </UFormField>
        <UFormField
          label="Concepto *"
          :error="!conceptoValido && descripcion.length > 0 ? 'Mínimo 5 caracteres' : undefined"
        >
          <UInput
            v-model="descripcion"
            class="w-full"
            placeholder="Ej: Arriendo de oficina"
          />
        </UFormField>
      </div>

      <div
        v-if="retiroExcede"
        class="mt-4"
      >
        <UAlert
          color="error"
          title="Retiro no permitido"
          description="El valor del retiro supera el capital disponible."
        />
      </div>

      <div class="mt-4 flex justify-end">
        <UButton
          color="primary"
          icon="i-lucide-save"
          :loading="enviando"
          :disabled="!puedeEnviar"
          :label="tipoMovimiento === 'inversion' ? 'Registrar inversión' : 'Registrar retiro'"
          @click="() => {
            if (tipoMovimiento === 'retiro') {
              confirmarRetiro = true
            }
            else {
              guardar()
            }
          }"
        />
      </div>
    </UCard>

    <UCard>
      <template #header>
        <div class="flex justify-between items-center">
          <h3 class="font-bold">
            Historial de movimientos
          </h3>
          <span class="text-sm text-gray-500">
            {{ movimientos?.total ?? 0 }} registros
          </span>
        </div>
      </template>

      <div class="flex flex-wrap items-end gap-3 mb-4">
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
        <UFormField label="Tipo">
          <USelect
            v-model="tipoFiltro"
            class="w-44"
            :items="[
              { label: 'Todos', value: '' },
              { label: 'Inversión', value: 'inversion' },
              { label: 'Retiro', value: 'retiro' },
              { label: 'Préstamo otorgado', value: 'prestamo_otorgado' },
              { label: 'Pago recibido', value: 'pago_recibido' },
              { label: 'Pérdida', value: 'perdida' },
              { label: 'Ajuste de préstamo', value: 'ajuste_prestamo' },
              { label: 'Devolución de pago', value: 'devolucion_pago' }
            ]"
          />
        </UFormField>
        <UButton
          color="primary"
          icon="i-lucide-search"
          @click="aplicarFiltrosHistorial"
        >
          Filtrar
        </UButton>
        <UButton
          color="neutral"
          variant="outline"
          icon="i-lucide-x"
          @click="limpiarFiltrosHistorial"
        >
          Limpiar
        </UButton>
      </div>

      <USkeleton
        v-if="loadingHistorial"
        class="h-50 rounded-lg"
      />

      <EmptyState
        v-else-if="!movimientos?.items?.length"
        icono="i-lucide-history"
        titulo="Sin movimientos"
        descripcion="No hay movimientos de capital registrados."
      />

      <UTable
        v-else
        sticky
        :data="movimientos.items.map(m => ({
          id: m.id,
          tipo: formatearTipo(m.tipo_movimiento),
          valor: formateo.formatoMoneda(m.valor),
          fecha: formateo.formatoFecha(m.fecha),
          descripcion: m.descripcion ?? '—'
        })) as unknown as Record<string, unknown>[]"
        :columns="[
          { accessorKey: 'id', header: 'ID' },
          { accessorKey: 'tipo', header: 'Tipo' },
          { accessorKey: 'valor', header: 'Valor' },
          { accessorKey: 'fecha', header: 'Fecha' },
          { accessorKey: 'descripcion', header: 'Descripción' }
        ]"
      />

      <div
        v-if="movimientos && movimientos.pages > 1"
        class="flex justify-center gap-2 mt-4"
      >
        <UButton
          label="Anterior"
          color="neutral"
          variant="outline"
          :disabled="paginaActual <= 1"
          @click="paginaActual--; cargarHistorial()"
        />
        <span class="text-sm text-gray-500 py-2">
          Página {{ movimientos.page }} de {{ movimientos.pages }}
        </span>
        <UButton
          label="Siguiente"
          color="neutral"
          variant="outline"
          :disabled="paginaActual >= movimientos.pages"
          @click="paginaActual++; cargarHistorial()"
        />
      </div>
    </UCard>

    <ConfirmDialog
      :open="confirmarRetiro"
      titulo="Confirmar retiro"
      mensaje="Esta acción reduce el capital disponible de forma permanente."
      confirmar-texto="Confirmar retiro"
      :loading="enviando"
      @update:open="confirmarRetiro = $event"
      @confirmar="() => { confirmarRetiro = false; guardar() }"
    />
  </div>
</template>
