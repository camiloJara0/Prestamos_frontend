<script setup lang="ts">
const syncStore = useSyncStore()

const visible = computed(() => !syncStore.isOnline || syncStore.pendingCount > 0)

const message = computed(() => {
  if (!syncStore.isOnline) return 'Sin conexión — los datos mostrados pueden estar desactualizados. Los pagos se guardarán en cola.'
  if (syncStore.pendingCount > 0) return `${syncStore.pendingCount} operación(es) pendiente(s) de sincronizar.`
  return ''
})

const color = computed(() => !syncStore.isOnline ? 'warning' : 'info')
</script>

<template>
  <Transition name="slide-down">
    <div
      v-if="visible"
      class="flex items-center justify-center gap-2 px-4 py-2 text-sm"
      :class="{
        'bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-300': color === 'warning',
        'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300': color === 'info'
      }"
    >
      <UIcon
        :name="!syncStore.isOnline ? 'i-lucide-wifi-off' : 'i-lucide-clock'"
        class="w-4 h-4 shrink-0"
      />
      <span>{{ message }}</span>
    </div>
  </Transition>
</template>

<style scoped>
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
}
.slide-down-enter-from,
.slide-down-leave-to {
  transform: translateY(-100%);
  opacity: 0;
}
</style>
