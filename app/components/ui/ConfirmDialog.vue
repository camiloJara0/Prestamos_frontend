<script setup lang="ts">
const props = withDefaults(defineProps<{
  open: boolean
  titulo?: string
  mensaje: string
  confirmarTexto?: string
  cancelarTexto?: string
  loading?: boolean
}>(), {
  titulo: '¿Estás seguro?',
  confirmarTexto: 'Confirmar',
  cancelarTexto: 'Cancelar'
})

const emit = defineEmits<{
  'update:open': [value: boolean]
  'confirmar': []
}>()

const isOpen = computed({
  get: () => props.open,
  set: v => emit('update:open', v)
})
</script>

<template>
  <ModalDialog
    :open="isOpen"
    :titulo="titulo"
    @update:open="isOpen = $event"
  >
    <template #body>
      <p class="text-sm text-gray-600 dark:text-gray-300">
        {{ mensaje }}
      </p>
    </template>
    <template #footer>
      <div class="flex justify-end gap-2 pt-2">
        <UButton
          :label="cancelarTexto"
          color="neutral"
          variant="outline"
          :disabled="loading"
          @click="isOpen = false"
        />
        <UButton
          :label="confirmarTexto"
          color="error"
          :loading="loading"
          icon="i-lucide-trash-2"
          @click="emit('confirmar')"
        />
      </div>
    </template>
  </ModalDialog>
</template>
