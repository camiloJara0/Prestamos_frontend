<script setup lang="ts">
const syncStore = useSyncStore()

const tooltipText = computed(() => {
  const parts: string[] = []
  parts.push(`Estado: ${syncStore.isOnline ? 'En línea' : 'Sin conexión'}`)
  if (syncStore.lastSyncAt) {
    const fecha = new Date(syncStore.lastSyncAt)
    parts.push(`Última sincronización: ${fecha.toLocaleTimeString('es-CO')}`)
  }
  if (syncStore.pendingCount > 0) {
    parts.push(`${syncStore.pendingCount} pendiente(s)`)
  }
  return parts.join(' · ')
})

const dotColor = computed(() => {
  switch (syncStore.syncStatus) {
    case 'ok': return 'bg-green-500'
    case 'pending': return 'bg-amber-500'
    case 'syncing': return 'bg-blue-500'
    case 'offline': return 'bg-red-500'
    default: return 'bg-gray-400'
  }
})
</script>

<template>
  <UTooltip :text="tooltipText">
    <div class="flex items-center gap-1.5 cursor-default">
      <span
        class="w-2 h-2 rounded-full shrink-0"
        :class="[dotColor, { 'animate-pulse': syncStore.syncing }]"
      />
      <span
        v-if="syncStore.pendingCount > 0"
        class="text-xs font-medium text-amber-600 dark:text-amber-400"
      >
        {{ syncStore.pendingCount }}
      </span>
    </div>
  </UTooltip>
</template>
