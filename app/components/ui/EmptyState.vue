<script setup lang="ts">
withDefaults(defineProps<{
  icono?: string
  titulo: string
  descripcion?: string
}>(), {
  icono: 'i-lucide-inbox'
})
</script>

<template>
  <div class="flex flex-col items-center justify-center gap-3 py-14 text-center">
    <div class="w-14 h-14 rounded-2xl bg-(--color-primary-500)/10 flex items-center justify-center">
      <UIcon
        :name="icono"
        class="text-3xl text-(--color-primary-500)"
      />
    </div>
    <div>
      <p class="font-medium text-gray-800 dark:text-gray-200">
        {{ titulo }}
      </p>
      <p
        v-if="descripcion"
        class="text-sm text-gray-500 max-w-sm"
      >
        {{ descripcion }}
      </p>
    </div>
    <slot />
  </div>
</template>
