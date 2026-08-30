<script setup lang="ts">
import { z } from 'zod'
import type { EstadoTipoPrestamo, TipoPrestamo, TipoPrestamoCreate } from '#shared/types/tipo_prestamo'

const props = withDefaults(defineProps<{
  tipo?: TipoPrestamo | null
}>(), {
  tipo: null
})

const emit = defineEmits<{
  guardar: [data: TipoPrestamoCreate]
}>()

const schema = z.object({
  nombre: z.string().min(1, 'El nombre es requerido').max(50, 'Máximo 50 caracteres'),
  descripcion: z.string().min(1, 'La descripción es requerida').max(200, 'Máximo 200 caracteres'),
  interes_mensual: z.number().positive('Debe ser mayor a 0'),
  max_cuotas: z.number().int().min(1, 'Debe ser al menos 1'),
  estado: z.enum(['activo', 'inactivo']).default('activo')
})

const form = reactive({
  nombre: props.tipo?.nombre ?? '',
  descripcion: props.tipo?.descripcion ?? '',
  interes_mensual: props.tipo?.interes_mensual ?? null,
  max_cuotas: props.tipo?.max_cuotas ?? null,
  estado: props.tipo?.estado ?? 'activo'
} as {
  nombre: string
  descripcion: string
  interes_mensual: number | null
  max_cuotas: number | null
  estado: EstadoTipoPrestamo
})

const errores = ref<Record<string, string>>({})

const interesInput = computed({
  get: () => form.interes_mensual != null ? String(form.interes_mensual) : '',
  set: (v) => {
    form.interes_mensual = v === '' ? null : Number(v)
  }
})

const cuotasInput = computed({
  get: () => form.max_cuotas != null ? String(form.max_cuotas) : '',
  set: (v) => {
    form.max_cuotas = v === '' ? null : Number(v)
  }
})

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
  emit('guardar', {
    ...form,
    interes_mensual: Number(form.interes_mensual),
    max_cuotas: Number(form.max_cuotas)
  })
}

defineExpose({ submit, validar })
</script>

<template>
  <form
    class="grid grid-cols-1 sm:grid-cols-2 gap-4"
    @submit.prevent="submit"
  >
    <UFormField
      label="Nombre *"
      :error="errores.nombre"
    >
      <UInput
        v-model="form.nombre"
            class="w-full"
        placeholder="Ej: Personal"
      />
    </UFormField>
    <UFormField
      label="Interés mensual (%) *"
      :error="errores.interes_mensual"
    >
      <UInput
        v-model="interesInput"
        type="number"
        min="0"
        step="0.01"
        placeholder="Ej: 2.5"
            class="w-full"
      />
    </UFormField>
    <UFormField
      label="Máximo de cuotas *"
      :error="errores.max_cuotas"
    >
      <UInput
        v-model="cuotasInput"
        type="number"
        min="1"
        step="1"
        placeholder="Ej: 12"
            class="w-full"
      />
    </UFormField>
    <UFormField
      label="Estado"
    >
      <USelect
        v-model="form.estado"
        :items="[{ label: 'Activo', value: 'activo' }, { label: 'Inactivo', value: 'inactivo' }]"
            class="w-full"
      />
    </UFormField>
    <UFormField
      label="Descripción *"
      :error="errores.descripcion"
      class="sm:col-span-2"
    >
      <UTextarea
        v-model="form.descripcion"
        placeholder="Descripción del tipo de préstamo"
        :rows="2"
            class="w-full"
      />
    </UFormField>
  </form>
</template>
