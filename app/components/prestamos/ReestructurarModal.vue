<script setup lang="ts">
import { z } from 'zod'
import type { Prestamo } from '#shared/types/prestamo'
import ModalDialog from '../ui/ModalDialog.vue'

const props = defineProps<{
  open: boolean
  prestamo: Prestamo | null
}>()

const emit = defineEmits<{
  'update:open': [value: boolean]
  'confirmar': [data: { numero_cuotas: number, porcentaje_interes: number, fecha_inicio: string, motivo: string }]
}>()

const schema = z.object({
  numero_cuotas: z.number().int().min(1, 'Debe haber al menos 1 cuota').max(120, 'Máximo 120 cuotas'),
  porcentaje_interes: z.number().min(0, 'El interés no puede ser negativo').max(100, 'Máximo 100%'),
  fecha_inicio: z.string().min(1, 'La fecha es requerida'),
  motivo: z.string().min(5, 'El motivo debe tener al menos 5 caracteres')
})

const isOpen = computed({
  get: () => props.open,
  set: v => emit('update:open', v)
})

const numeroCuotas = ref<number | null>(null)
const porcentajeInteres = ref<number | null>(null)
const fechaInicio = ref(hoyLocal())
const motivo = ref('')
const errores = ref<Record<string, string>>({})
const enviando = ref(false)

const saldoPendiente = computed(() => props.prestamo?.saldo_pendiente ?? 0)

const cuotasInput = computed({
  get: () => numeroCuotas.value != null ? String(numeroCuotas.value) : '',
  set: (v) => { numeroCuotas.value = v === '' ? null : Number(v) }
})

const interesInput = computed({
  get: () => porcentajeInteres.value != null ? String(porcentajeInteres.value) : '',
  set: (v) => { porcentajeInteres.value = v === '' ? null : Number(v) }
})

const interesNuevo = computed(() => {
  if (!numeroCuotas.value || porcentajeInteres.value == null) return 0
  return redondear(saldoPendiente.value * (porcentajeInteres.value / 100) * numeroCuotas.value)
})

const totalPlan = computed(() => redondear(saldoPendiente.value + interesNuevo.value))

const valorCuota = computed(() => {
  if (!numeroCuotas.value) return 0
  return redondear(totalPlan.value / numeroCuotas.value)
})

watch(() => props.open, (open) => {
  if (open) {
    numeroCuotas.value = props.prestamo?.numero_cuotas ?? null
    porcentajeInteres.value = props.prestamo?.porcentaje_interes ?? null
    fechaInicio.value = hoyLocal()
    motivo.value = ''
    errores.value = {}
    enviando.value = false
  } else {
    enviando.value = false
  }
})

function validar() {
  const resultado = schema.safeParse({
    numero_cuotas: numeroCuotas.value ?? undefined,
    porcentaje_interes: porcentajeInteres.value ?? undefined,
    fecha_inicio: fechaInicio.value,
    motivo: motivo.value.trim()
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

function confirmar() {
  if (!validar()) return
  enviando.value = true
  emit('confirmar', {
    numero_cuotas: Number(numeroCuotas.value),
    porcentaje_interes: Number(porcentajeInteres.value),
    fecha_inicio: fechaInicio.value,
    motivo: motivo.value.trim()
  })
}
</script>

<template>
  <ModalDialog
    :open="isOpen"
    titulo="Reestructurar préstamo"
    :descripcion="prestamo ? `Préstamo #${prestamo.id}` : undefined"
    ancho="max-w-2xl"
    @update:open="isOpen = $event"
  >
    <template #body>
      <UAlert
        class="mb-4"
        color="warning"
        icon="i-lucide-alert-triangle"
        title="Aplica solo a préstamos en mora. Se generan cuotas nuevas vinculadas al préstamo original sin cancelar el histórico; una reestructuración posterior cierra la anterior (RF-035)."
      />

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <p class="text-xs text-gray-500">
            Saldo pendiente a renegociar
          </p>
          <p class="font-bold text-lg">
            {{ formatoMoneda(saldoPendiente) }}
          </p>
        </div>
        <UFormField
          label="Fecha de inicio *"
          :error="errores.fecha_inicio"
        >
          <UInput
            v-model="fechaInicio"
            type="date"
            class="w-full"
          />
        </UFormField>
        <UFormField
          label="Nuevo número de cuotas *"
          :error="errores.numero_cuotas"
        >
          <UInput
            v-model="cuotasInput"
            type="number"
            min="1"
            max="120"
            step="1"
          />
        </UFormField>
        <UFormField
          label="Nuevo interés total (%) *"
          :error="errores.porcentaje_interes"
        >
          <UInput
            v-model="interesInput"
            type="number"
            min="0"
            max="100"
            step="0.01"
          />
        </UFormField>
        <UFormField
          label="Motivo de la reestructuración *"
          class="sm:col-span-2"
          :error="errores.motivo"
        >
          <UTextarea
            v-model="motivo"
            :rows="2"
            placeholder="Detalle la razón de la renegociación (mínimo 5 caracteres)"
            class="w-full"
          />
        </UFormField>
      </div>

      <div
        v-if="numeroCuotas && porcentajeInteres != null"
        class="mt-4 rounded-xl border border-primary-500/20 p-4 bg-primary-500/5"
      >
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-sm">
          <div>
            <p class="text-xs text-gray-500">
              Interés nuevo
            </p>
            <p class="font-semibold">
              {{ formatoMoneda(interesNuevo) }}
            </p>
          </div>
          <div>
            <p class="text-xs text-gray-500">
              Total del plan
            </p>
            <p class="font-semibold">
              {{ formatoMoneda(totalPlan) }}
            </p>
          </div>
          <div>
            <p class="text-xs text-gray-500">
              Valor por cuota
            </p>
            <p class="font-semibold">
              {{ formatoMoneda(valorCuota) }}
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
          @click="() => { isOpen = false }"
        />
        <UButton
          label="Reestructurar"
          color="primary"
          icon="i-lucide-refresh-ccw"
          :loading="enviando"
          @click="confirmar"
        />
      </div>
    </template>
  </ModalDialog>
</template>
