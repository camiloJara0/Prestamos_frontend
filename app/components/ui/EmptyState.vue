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
  <div class="flex flex-col items-center justify-center gap-4 py-16 text-center">
    <div class="w-16 h-16 rounded-2xl bg-primary/8 flex items-center justify-center">
      <UIcon
        :name="icono"
        class="text-3xl text-primary/60"
      />
    </div>
    <div>
      <p class="font-semibold text-gray-800 dark:text-gray-200">
        {{ titulo }}
      </p>
      <p
        v-if="descripcion"
        class="text-sm text-gray-500 dark:text-gray-400 max-w-sm mt-1"
      >
        {{ descripcion }}
      </p>
    </div>
    <slot />
  </div>
</template>
