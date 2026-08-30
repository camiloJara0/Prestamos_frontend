<script setup lang="ts">
import { z } from 'zod'
import type { Cliente, ClienteCreate, EstadoCliente } from '#shared/types/clientes'

const props = withDefaults(defineProps<{
  cliente?: Cliente | null
  errorCampo?: Record<string, string>
}>(), {
  cliente: null,
  errorCampo: () => ({})
})

const emit = defineEmits<{
  guardar: [data: ClienteCreate]
}>()

const schema = z.object({
  nombre: z.string().min(1, 'El nombre es requerido').max(100, 'Máximo 100 caracteres'),
  cedula: z.string().min(1, 'La cédula es requerida').max(20, 'Máximo 20 caracteres'),
  telefono: z.string().max(20, 'Máximo 20 caracteres').optional().or(z.literal('')),
  direccion: z.string().max(200, 'Máximo 200 caracteres').optional().or(z.literal('')),
  persona_referencia: z.string().max(100, 'Máximo 100 caracteres').optional().or(z.literal('')),
  telefono_referencia: z.string().max(20, 'Máximo 20 caracteres').optional().or(z.literal('')),
  observaciones: z.string().max(500, 'Máximo 500 caracteres').optional().or(z.literal('')),
  estado: z.enum(['activo', 'inactivo']).default('activo')
})

const form = reactive({
  nombre: props.cliente?.nombre ?? '',
  cedula: props.cliente?.cedula ?? '',
  telefono: props.cliente?.telefono ?? '',
  direccion: props.cliente?.direccion ?? '',
  persona_referencia: props.cliente?.persona_referencia ?? '',
  telefono_referencia: props.cliente?.telefono_referencia ?? '',
  observaciones: props.cliente?.observaciones ?? '',
  estado: props.cliente?.estado ?? 'activo'
} as {
  nombre: string
  cedula: string
  telefono: string
  direccion: string
  persona_referencia: string
  telefono_referencia: string
  observaciones: string
  estado: EstadoCliente
})

const errores = ref<Record<string, string>>({})

watch(() => props.errorCampo, (e) => {
  errores.value = { ...errores.value, ...e }
}, { deep: true })

const nombre = computed(() => form.nombre)
const cedula = computed(() => form.cedula)

function limpiarCampo(campo: string) {
  const next: Record<string, string> = {}
  for (const [k, v] of Object.entries(errores.value)) {
    if (k !== campo) next[k] = v
  }
  errores.value = next
}

function validar() {
  const resultado = schema.safeParse({ ...form, telefono: form.telefono || undefined, direccion: form.direccion || undefined, persona_referencia: form.persona_referencia || undefined, telefono_referencia: form.telefono_referencia || undefined, observaciones: form.observaciones || undefined })

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
    telefono: form.telefono || null,
    direccion: form.direccion || null,
    persona_referencia: form.persona_referencia || null,
    telefono_referencia: form.telefono_referencia || null,
    observaciones: form.observaciones || null
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
        v-model="nombre"
        placeholder="Nombre del cliente"
        icon="i-lucide-user"
        @update:model-value="() => limpiarCampo('nombre')"
      />
    </UFormField>
    <UFormField
      label="Cédula *"
      :error="errores.cedula"
    >
      <UInput
        v-model="cedula"
        placeholder="Cédula"
        icon="i-lucide-id-card"
        @update:model-value="() => limpiarCampo('cedula')"
      />
    </UFormField>
    <UFormField
      label="Teléfono"
      :error="errores.telefono"
    >
      <UInput
        v-model="form.telefono"
        placeholder="Teléfono"
        icon="i-lucide-phone"
      />
    </UFormField>
    <UFormField
      label="Dirección"
      :error="errores.direccion"
    >
      <UInput
        v-model="form.direccion"
        placeholder="Dirección"
        icon="i-lucide-map-pin"
      />
    </UFormField>
    <UFormField
      label="Persona de referencia"
      :error="errores.persona_referencia"
    >
      <UInput
        v-model="form.persona_referencia"
        placeholder="Persona de referencia"
      />
    </UFormField>
    <UFormField
      label="Teléfono de referencia"
      :error="errores.telefono_referencia"
    >
      <UInput
        v-model="form.telefono_referencia"
        placeholder="Teléfono de referencia"
        icon="i-lucide-phone-call"
      />
    </UFormField>
    <UFormField
      label="Estado"
      class="sm:col-span-2"
    >
      <USelect
        v-model="form.estado"
        :items="[{ label: 'Activo', value: 'activo' }, { label: 'Inactivo', value: 'inactivo' }]"
      />
    </UFormField>
    <UFormField
      label="Observaciones"
      class="sm:col-span-2"
    >
      <UTextarea
        v-model="form.observaciones"
        placeholder="Observaciones"
        class="w-full"
        :rows="2"
      />
    </UFormField>
  </form>
</template>
