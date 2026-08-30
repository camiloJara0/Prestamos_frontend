<script setup lang="ts">
import { z } from 'zod'
import { calcularPrestamo } from '~/utils/calculadoraPrestamo'
import type { Prestamo } from '#shared/types/prestamo'

const props = defineProps<{
  open: boolean
  prestamo: Prestamo | null
}>()

const emit = defineEmits<{
  'update:open': [value: boolean]
  'confirmar': [data: { porcentaje_interes: number, numero_cuotas: number, abono: number, fecha_renovacion: string, observaciones?: string | null }]
}>()

const schema = z.object({
  porcentaje_interes: z.number().positive('El interés debe ser mayor a 0'),
  numero_cuotas: z.number().int().min(1, 'Debe haber al menos 1 cuota'),
  abono: z.number().min(0, 'El abono no puede ser negativo'),
  fecha_renovacion: z.string().min(1, 'La fecha es requerida')
})

const isOpen = computed({
  get: () => props.open,
  set: v => emit('update:open', v)
})

const porcentajeInteres = ref<number | null>(null)
const numeroCuotas = ref<number | null>(null)
const abono = ref<number>(0)
const fechaRenovacion = ref(hoyLocal())
const observaciones = ref('')
const errores = ref<Record<string, string>>({})
const enviando = ref(false)

const saldoPendiente = computed(() => props.prestamo?.saldo_pendiente ?? 0)

const abonoExcede = computed(() => abono.value > saldoPendiente.value)

const capitalNuevo = computed(() => Math.max(0, redondear(saldoPendiente.value - abono.value)))

const calculo = computed(() => {
  if (!porcentajeInteres.value || !numeroCuotas.value) return null
  if (porcentajeInteres.value <= 0 || numeroCuotas.value < 1) return null
  return calcularPrestamo({
    capital_prestado: capitalNuevo.value,
    porcentaje_interes: porcentajeInteres.value,
    numero_cuotas: numeroCuotas.value
  })
})

watch(() => props.open, (open) => {
  if (open) {
    porcentajeInteres.value = props.prestamo?.porcentaje_interes ?? null
    numeroCuotas.value = props.prestamo?.numero_cuotas ?? null
    abono.value = 0
    fechaRenovacion.value = hoyLocal()
    observaciones.value = ''
    errores.value = {}
  }
})

const interesInput = computed({
  get: () => porcentajeInteres.value != null ? String(porcentajeInteres.value) : '',
  set: (v) => {
    porcentajeInteres.value = v === '' ? null : Number(v)
  }
})

const cuotasInput = computed({
  get: () => numeroCuotas.value != null ? String(numeroCuotas.value) : '',
  set: (v) => {
    numeroCuotas.value = v === '' ? null : Number(v)
  }
})

function validar() {
  const resultado = schema.safeParse({
    porcentaje_interes: porcentajeInteres.value ?? undefined,
    numero_cuotas: numeroCuotas.value ?? undefined,
    abono: abono.value,
    fecha_renovacion: fechaRenovacion.value
  })
  if (!resultado.success) {
    errores.value = {}
    for (const issue of resultado.error.issues) {
      errores.value[issue.path[0] as string] = issue.message
    }
    return false
  }
  errores.value = {}
  return true
}

async function confirmar() {
  if (!validar() || abonoExcede.value) return
  enviando.value = true
  emit('confirmar', {
    porcentaje_interes: Number(porcentajeInteres.value),
    numero_cuotas: Number(numeroCuotas.value),
    abono: abono.value,
    fecha_renovacion: fechaRenovacion.value,
    observaciones: observaciones.value || null
  })
}
</script>

<template>
  <ModalDialog
    :open="isOpen"
    titulo="Renovar préstamo"
    :descripcion="prestamo ? `Préstamo #${prestamo.id}` : undefined"
    ancho="max-w-2xl"
    @update:open="isOpen = $event"
  >
    <template #body>
      <UAlert
        class="mb-4"
        color="info"
        title="La renovación genera un nuevo préstamo y el original pasa a estado renovado."
      />

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <p class="text-xs text-gray-500">
            Saldo pendiente
          </p>
          <p class="font-bold text-lg">
            {{ formatoMoneda(saldoPendiente) }}
          </p>
        </div>
        <UFormField
          label="Abono"
          :error="errores.abono || (abonoExcede ? 'El abono no puede superar el saldo pendiente' : '')"
        >
          <UInput
            v-model="abono"
            type="number"
            min="0"
            step="0.01"
            placeholder="0"
          />
        </UFormField>
        <UFormField
          label="Interés mensual (%) *"
          :error="errores.porcentaje_interes"
        >
          <UInput
            v-model="interesInput"
            type="number"
            min="0"
            step="0.01"
          />
        </UFormField>
        <UFormField
          label="Número de cuotas *"
          :error="errores.numero_cuotas"
        >
          <UInput
            v-model="cuotasInput"
            type="number"
            min="1"
            step="1"
          />
        </UFormField>
        <UFormField
          label="Fecha de renovación *"
          :error="errores.fecha_renovacion"
        >
          <UInput
            v-model="fechaRenovacion"
            type="date"
          />
        </UFormField>
        <UFormField
          label="Observaciones"
          class="sm:col-span-2"
        >
          <UInput
            v-model="observaciones"
            placeholder="Opcional"
          />
        </UFormField>
      </div>

      <div
        v-if="calculo"
        class="mt-4 rounded-xl border border-(--color-primary-500)/20 p-4 bg-(--color-primary-500)/5"
      >
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-sm">
          <div>
            <p class="text-xs text-gray-500">
              Capital nuevo
            </p>
            <p class="font-semibold">
              {{ formatoMoneda(capitalNuevo) }}
            </p>
          </div>
          <div>
            <p class="text-xs text-gray-500">
              Monto total nuevo
            </p>
            <p class="font-semibold">
              {{ formatoMoneda(calculo.monto_total) }}
            </p>
          </div>
          <div>
            <p class="text-xs text-gray-500">
              Nueva cuota
            </p>
            <p class="font-semibold">
              {{ formatoMoneda(calculo.valor_cuota) }}
            </p>
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <div class="flex justify-end gap-2 pt-2">
        <UButton
          label="Cancelar"
          color="neutral"
          variant="outline"
          :disabled="enviando"
          @click="isOpen = false"
        />
        <UButton
          label="Renovar"
          color="primary"
          icon="i-lucide-refresh-cw"
          :loading="enviando"
          @click="confirmar"
        />
      </div>
    </template>
  </ModalDialog>
</template>
