<script setup lang="ts">
const pwa = usePwaInstall()

onMounted(() => {
  pwa.init()
})

onUnmounted(() => {
  pwa.destroy()
})
</script>

<template>
  <Transition name="slide-up">
    <UButton
      v-if="pwa.canInstall.value"
      label="Instalar app"
      icon="i-lucide-download"
      color="primary"
      size="sm"
      @click="() => { pwa.promptInstall() }"
    />
  </Transition>
</template>

<style scoped>
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease;
}
.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(100%);
  opacity: 0;
}
</style>
