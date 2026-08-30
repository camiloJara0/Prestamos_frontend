<script setup lang="ts">
const props = withDefaults(defineProps<{
  open: boolean
  titulo?: string
  descripcion?: string
  ancho?: string
}>(), {
  ancho: 'max-w-lg'
})

const emit = defineEmits<{
  'update:open': [value: boolean]
}>()

const isOpen = computed({
  get: () => props.open,
  set: v => emit('update:open', v)
})
</script>

<template>
  <UModal
    :v-model:open="isOpen"
    :ui="{ content: `w-full ${ancho}` }"
    @update:open="isOpen = $event"
  >
    <template #title>
      <slot name="title">
        {{ titulo }}
      </slot>
    </template>
    <template #description>
      <slot name="description">
        {{ descripcion }}
      </slot>
    </template>
    <slot name="body" />
    <slot name="footer" />
  </UModal>
</template>
