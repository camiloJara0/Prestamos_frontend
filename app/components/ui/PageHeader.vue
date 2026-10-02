<script setup lang="ts">
withDefaults(defineProps<{
  titulo: string
  descripcion?: string
  icono?: string
}>(), {
  descripcion: '',
  icono: ''
})

defineSlots<{
  default: () => unknown
  actions: () => unknown
}>()
</script>

<template>
  <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
    <div class="flex items-center gap-4">
      <div
        v-if="icono"
        class="flex items-center justify-center w-11 h-11 rounded-xl bg-primary/8"
      >
        <UIcon
          :name="icono"
          class="w-5.5 h-5.5 text-primary"
        />
      </div>
      <div>
        <h1 class="text-2xl font-bold font-display tracking-tight">
          {{ titulo }}
        </h1>
        <p
          v-if="descripcion"
          class="text-sm text-gray-500 dark:text-gray-400 mt-0.5"
        >
          {{ descripcion }}
        </p>
      </div>
    </div>
    <div
      v-if="$slots.actions"
      class="flex items-center gap-2"
    >
      <slot name="actions" />
    </div>
  </div>
</template>
