<script setup lang="ts">
const syncStore = useSyncStore()
const offline = useOffline()
const auth = useAuthStore()
const { needsOnboarding: _, verificarEstado, completado } = useOnboarding()
const mostrarWizard = ref(false)

onMounted(() => {
  offline.init()
  syncStore.setOnline(offline.isOnline.value)

  if (auth.isAuthenticated && !completado.value) {
    verificarEstado()
    if (!completado.value) {
      mostrarWizard.value = true
    }
  }
})

watch(() => offline.isOnline.value, (val) => {
  syncStore.setOnline(val)
})

watch(() => auth.isAuthenticated, (isAuth) => {
  if (isAuth && !completado.value) {
    verificarEstado()
    if (!completado.value) {
      mostrarWizard.value = true
    }
  }
})

onUnmounted(() => {
  offline.destroy()
})
</script>

<template>
  <div class="layout-root">
    <LayoutAside />

    <div class="layout-content">
      <AppConnectionBanner />
      <AppHeader />

      <main class="layout-main">
        <slot />
      </main>
    </div>

    <AppCommandPalette />

    <AppOnboardingWizard
      :open="mostrarWizard"
      @update:open="mostrarWizard = $event"
      @completado="mostrarWizard = false"
    />
  </div>
</template>

<style scoped>
.layout-root {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

.layout-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-width: 0;
}

.layout-main {
  flex: 1;
  overflow-y: auto;
  scroll-behavior: smooth;
  padding: 1.5rem;
}

@media (min-width: 768px) {
  .layout-main {
    padding: 2rem;
  }
}

@media (min-width: 1024px) {
  .layout-main {
    padding: 2.5rem;
  }
}

.layout-main::-webkit-scrollbar {
  width: 5px;
}

.layout-main::-webkit-scrollbar-track {
  background: transparent;
}

.layout-main::-webkit-scrollbar-thumb {
  background: #d4d0e8;
  border-radius: 99px;
}

.layout-main::-webkit-scrollbar-thumb:hover {
  background: #a78bfa;
}
</style>
