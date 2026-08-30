<script setup lang="ts">
import { z } from 'zod'
import type { TipoPago, TipoPagoCreate } from '#shared/types/tipo_pago'

const props = withDefaults(defineProps<{
  tipo?: TipoPago | null
}>(), {
  tipo: null
})

const emit = defineEmits<{
  guardar: [data: TipoPagoCreate]
}>()

const schema = z.object({
  nombre: z.string().min(1, 'El nombre es requerido').max(50, 'Máximo 50 caracteres'),
  descripcion: z.string().min(1, 'La descripción es requerida').max(200, 'Máximo 200 caracteres')
})

const form = reactive<TipoPagoCreate>({
  nombre: props.tipo?.nombre ?? '',
  descripcion: props.tipo?.descripcion ?? ''
})

const errores = ref<Record<string, string>>({})

function validar() {
  const resultado = schema.safeParse(form)
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

function submit() {
  if (!validar()) return
  emit('guardar', { ...form })
}

defineExpose({ submit, validar })
</script>

<template>
  <form
    class="grid grid-cols-1 gap-4"
    @submit.prevent="submit"
  >
    <UFormField
      label="Nombre *"
      :error="errores.nombre"
    >
      <UInput
        v-model="form.nombre"
            class="w-full"
        placeholder="Ej: Efectivo"
      />
    </UFormField>
    <UFormField
      label="Descripción *"
      :error="errores.descripcion"
    >
      <UTextarea
        v-model="form.descripcion"
            class="w-full"
        placeholder="Descripción del tipo de pago"
        :rows="2"
      />
    </UFormField>
  </form>
</template>
