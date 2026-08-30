<script setup lang="ts">
const syncStore = useSyncStore()
const offline = useOffline()

onMounted(() => {
  offline.init()
  syncStore.setOnline(offline.isOnline.value)
})

watch(() => offline.isOnline.value, (val) => {
  syncStore.setOnline(val)
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
      <AppAppHeader />

      <main class="layout-main">
        <slot />
      </main>
    </div>
  </div>
</template>

<style scoped>
.layout-root {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background: #f5f4f9;
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
  background: #f5f4f9;
  scroll-behavior: smooth;
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
