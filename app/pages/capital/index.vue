<script setup lang="ts">
import { z } from 'zod'
import type { MovimientoCapitalCreate } from '#shared/types/movimiento_capital'
import { useCapital } from '~/composables/domain/useCapital'
import ConfirmDialog from '~/components/ui/ConfirmDialog.vue'
import StatCard from '~/components/ui/StatCard.vue'
import EmptyState from '~/components/ui/EmptyState.vue'
import MoneyInput from '~/components/ui/MoneyInput.vue'

definePageMeta({
  middleware: 'admin'
})

const { capital, fetch, registrar } = useCapital()

const toast = useToast()
const formateo = useFormatters()

const tipoMovimiento = ref<'inversion' | 'retiro'>('inversion')
const descripcion = ref('')
const valor = ref<string | null>(null)
const fecha = ref(hoyLocal())
const enviando = ref(false)
const errorValor = ref<string | null>(null)

async function inicializar() {
  await fetch()
}
inicializar()

const montoActual = computed(() => capital.value?.monto_total ?? 0)

const valorNumerico = computed(() => {
  if (valor.value == null || valor.value.trim() === '') return null
  const numero = Number(valor.value)
  return Number.isFinite(numero) ? numero : null
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
  } catch (e) {
    toast.add({ title: (e as { detail: string }).detail || 'No se pudo registrar el movimiento', color: 'error' })
  } finally {
    enviando.value = false
  }
}

const confirmarRetiro = ref(false)
</script>

<template>
  <div class="p-6 space-y-6">
    <div>
      <h1 class="text-2xl font-bold">
        Capital
      </h1>
      <p class="text-sm text-gray-500">
        Gestión del capital disponible para préstamos.
      </p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <StatCard
        titulo="Capital disponible"
        :valor="formateo.formatoMoneda(montoActual)"
        icono="i-lucide-wallet"
        color="primary"
        :footer="capital?.updated_at ? `Actualizado: ${formateo.formatoFecha(capital.updated_at)}` : undefined"
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
          <MoneyInput v-model="valor" model />
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
          @click="tipoMovimiento === 'retiro' ? (confirmarRetiro = true) : guardar()"
        />
      </div>
    </UCard>

    <UCard>
      <template #header>
        <h3 class="font-bold">
          Historial de movimientos
        </h3>
      </template>
      <EmptyState
        icono="i-lucide-history"
        titulo="Historial de movimientos"
        descripcion="El historial de movimientos estará disponible próximamente. El backend aún no expone este endpoint."
      />
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
