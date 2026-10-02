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
  'confirmar': [nuevoCapital: number]
}>()

const schema = z.object({
  nuevo_capital: z.number().positive('El capital debe ser mayor a 0')
})

const isOpen = computed({
  get: () => props.open,
  set: v => emit('update:open', v)
})

const nuevoCapital = ref<number | null>(null)
const error = ref<string | null>(null)
const enviando = ref(false)

const capitalActual = computed(() => props.prestamo?.capital_prestado ?? 0)

const capitalInput = computed({
  get: () => nuevoCapital.value != null ? String(nuevoCapital.value) : '',
  set: (v) => { nuevoCapital.value = v === '' ? null : Number(v) }
})

watch(() => props.open, (open) => {
  if (open) {
    nuevoCapital.value = props.prestamo?.capital_prestado ?? null
    error.value = null
    enviando.value = false
  } else {
    enviando.value = false
  }
})

function confirmar() {
  const resultado = schema.safeParse({ nuevo_capital: nuevoCapital.value ?? undefined })
  if (!resultado.success) {
    error.value = resultado.error.issues[0]?.message ?? 'Revise el valor ingresado'
    return
  }
  error.value = null
  enviando.value = true
  emit('confirmar', Number(nuevoCapital.value))
}
</script>

<template>
  <ModalDialog
    :open="isOpen"
    titulo="Ajustar capital"
    :descripcion="prestamo ? `Préstamo #${prestamo.id}` : undefined"
    ancho="max-w-lg"
    @update:open="isOpen = $event"
  >
    <template #body>
      <UAlert
        class="mb-4"
        color="info"
        icon="i-lucide-info"
        title="El servidor recalcula intereses y cuotas con el nuevo capital y registra el ajuste como movimiento de capital con trazabilidad de usuario (RF-034)."
      />

      <div class="grid grid-cols-1 gap-4">
        <div>
          <p class="text-xs text-gray-500">
            Capital actual
          </p>
          <p class="font-bold text-lg">
            {{ formatoMoneda(capitalActual) }}
          </p>
        </div>
        <UFormField
          label="Nuevo capital *"
          :error="error ?? undefined"
        >
          <UInput
            v-model="capitalInput"
            type="number"
            min="0"
            step="0.01"
            class="w-full"
          />
        </UFormField>
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
          label="Ajustar capital"
          color="primary"
          icon="i-lucide-save"
          :loading="enviando"
          @click="confirmar"
        />
      </div>
    </template>
  </ModalDialog>
</template>
