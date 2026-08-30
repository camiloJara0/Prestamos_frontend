<script setup lang="ts">
withDefaults(defineProps<{
  titulo: string
  valor: string
  icono?: string
  color?: string
  footer?: string
}>(), {
  color: 'primary'
})
</script>

<template>
  <UCard class="stat-card glass">
    <div class="flex items-start justify-between gap-3">
      <div class="min-w-0">
        <p class="text-sm text-gray-500 dark:text-gray-400 truncate">
          {{ titulo }}
        </p>
        <p class="font-display text-2xl font-bold text-gray-900 dark:text-white mt-1 truncate">
          {{ valor }}
        </p>
        <p
          v-if="footer"
          class="text-xs text-gray-400 mt-1"
        >
          {{ footer }}
        </p>
      </div>
      <div
        v-if="icono"
        class="shrink-0 w-10 h-10 rounded-xl flex items-center justify-center"
        :class="`bg-(--color-${color}-500)/12 text-(--color-${color}-500)`"
      >
        <UIcon
          :name="icono"
          class="text-xl"
        />
      </div>
    </div>
  </UCard>
</template>

<style scoped>
.stat-card {
  border: 1px solid rgba(124, 58, 237, 0.18);
}
</style>
