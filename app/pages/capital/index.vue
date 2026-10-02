<script setup lang="ts">
import { z } from 'zod'
import type { MovimientoCapitalCreate, MovimientoCapital } from '#shared/types/movimiento_capital'
import { useCapital } from '~/composables/domain/useCapital'
import { getMovimientosCapital } from '~/services/api/capital'
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
const loadingHistorial = ref(false)
const paginaActual = ref(1)

async function inicializar() {
  await Promise.all([fetchCapital(), cargarHistorial()])
}

async function cargarHistorial() {
  loadingHistorial.value = true
  try {
    movimientos.value = await getMovimientosCapital(paginaActual.value, 20)
  } catch {
    toast.add({ title: 'No se pudo cargar el historial', color: 'error' })
  } finally {
    loadingHistorial.value = false
  }
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

const puedeEnviar = computed(() => {
  return valorNumerico.value != null && valorNumerico.value > 0 && !retiroExcede.value && fecha.value !== ''
})

const schema = z.object({
  tipo_movimiento: z.enum(['inversion', 'retiro']),
  valor: z.number().positive('El valor debe ser mayor a 0'),
  fecha: z.string().min(1, 'La fecha es requerida')
})

watch(retiroExcede, (excede) => {
  errorValor.value = excede ? 'El retiro no puede exceder el capital disponible' : null
})

async function guardar() {
  errorValor.value = null
  const resultado = schema.safeParse({ tipo_movimiento: tipoMovimiento.value, valor: valorNumerico.value, fecha: fecha.value })
  if (!resultado.success) {
    errorValor.value = 'Revise los valores del formulario'
    return
  }

  enviando.value = true
  try {
    const payload: MovimientoCapitalCreate = {
      tipo_movimiento: tipoMovimiento.value,
      descripcion: descripcion.value || null,
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
    await Promise.all([fetchCapital(), cargarHistorial()])
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
    perdida: 'Pérdida'
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
        v-if="movimientos"
        titulo="Total movimientos"
        :valor="String(movimientos.total)"
        icono="i-lucide-list"
        color="info"
      />
      <UiStatCard
        v-if="movimientos"
        titulo="Páginas"
        :valor="`${movimientos.page} / ${movimientos.pages}`"
        icono="i-lucide-chevrons-right"
        color="neutral"
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
        <UFormField label="Descripción">
          <UInput
            v-model="descripcion"
            class="w-full"
            placeholder="Opcional"
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
