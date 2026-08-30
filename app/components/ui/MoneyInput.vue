<script setup lang="ts">
const props = withDefaults(defineProps<{
  modelValue?: string | null
  label?: string
  placeholder?: string
  error?: string | boolean | undefined
  disabled?: boolean
  required?: boolean
}>(), {
  modelValue: null,
  label: undefined,
  placeholder: '$ 0',
  error: undefined,
  disabled: false,
  required: false
})

const emit = defineEmits<{
  'update:modelValue': [value: number | null]
}>()

const texto = ref('')

const formatear = (n: number): string => {
  return new Intl.NumberFormat('es-CO', {
    style: 'currency',
    currency: 'COP',
    minimumFractionDigits: 0,
    maximumFractionDigits: 2
  }).format(n)
}

const alEscribir = (event: Event) => {
  const raw = (event.target as HTMLInputElement).value
  const soloDigitos = raw.replace(/[^0-9]/g, '')

  if (soloDigitos === '') {
    texto.value = ''
    emit('update:modelValue', null)
    return
  }

  const numero = Number(soloDigitos) / 100
  texto.value = formatear(numero)
  emit('update:modelValue', Number.isFinite(numero) ? numero : null)
}

watch(
  () => props.modelValue,
  (valor) => {
    texto.value = valor != null ? formatear(parseInt(valor)) : ''
  },
  { immediate: true }
)
</script>

<template>
  <UFormField
    :label="label"
    :required="required"
    :error="error"
  >
    <UInput
      :model-value="texto"
      type="text"
      inputmode="decimal"
      :placeholder="placeholder"
      :disabled="disabled"
      :ui="{ trailing: 'pr-2' }"
      class="w-full"
      @input="alEscribir"
    />
  </UFormField>
</template>
