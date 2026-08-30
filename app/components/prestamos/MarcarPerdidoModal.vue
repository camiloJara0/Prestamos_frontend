<script setup lang="ts">
import { z } from 'zod'
import type { Prestamo } from '#shared/types/prestamo'

const props = defineProps<{
  open: boolean
  prestamo: Prestamo | null
}>()

const emit = defineEmits<{
  'update:open': [value: boolean]
  'confirmar': [data: { motivo?: string | null, fecha: string }]
}>()

const schema = z.object({
  fecha: z.string().min(1, 'La fecha es requerida')
})

const isOpen = computed({
  get: () => props.open,
  set: v => emit('update:open', v)
})

const motivo = ref('')
const fecha = ref(hoyLocal())
const errores = ref<Record<string, string>>({})
const enviando = ref(false)

watch(() => props.open, (open) => {
  if (open) {
    motivo.value = ''
    fecha.value = hoyLocal()
    errores.value = {}
  }
})

const valorAPerder = computed(() => props.prestamo?.saldo_pendiente ?? 0)

function validar() {
  const resultado = schema.safeParse({ fecha: fecha.value })
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
  if (!validar()) return
  enviando.value = true
  emit('confirmar', {
    motivo: motivo.value || null,
    fecha: fecha.value
  })
}
</script>

<template>
  <ModalDialog
    :open="isOpen"
    titulo="Marcar préstamo como perdido"
    :descripcion="prestamo ? `Préstamo #${prestamo.id}` : undefined"
    @update:open="isOpen = $event"
  >
    <template #body>
      <UAlert
        class="mb-4"
        color="error"
        title="Acción irreversible"
        description="Este préstamo se marcará como perdido y se registrará el impacto en el capital."
      />

      <div class="rounded-xl border border-error/20 bg-error/5 p-4 mb-4">
        <p class="text-xs text-gray-500">
          Valor a perder (saldo pendiente)
        </p>
        <p class="font-bold text-lg text-error">
          {{ formatoMoneda(valorAPerder) }}
        </p>
      </div>

      <div class="grid grid-cols-1 gap-4">
        <UFormField
          label="Fecha *"
          :error="errores.fecha"
        >
          <UInput
            v-model="fecha"
            type="date"
          />
        </UFormField>
        <UFormField label="Motivo">
          <UTextarea
            v-model="motivo"
            placeholder="Opcional — motivo de la pérdida"
            :rows="2"
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
          @click="isOpen = false"
        />
        <UButton
          label="Marcar como perdido"
          color="error"
          icon="i-lucide-flag"
          :loading="enviando"
          @click="confirmar"
        />
      </div>
    </template>
  </ModalDialog>
</template>
