<script setup lang="ts">
const varView = useVarView()
</script>

<template>
  <div class="layout-root">

    <!-- Aside con animación de ancho via CSS -->
    <LayoutAside />

    <!-- Contenido principal -->
    <main class="layout-main">
      <slot />
    </main>

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

/*
  El aside se autogestiona su propio ancho via CSS (220px / 56px).
  El main ocupa el espacio restante con flex: 1.
  La transición del aside propaga naturalmente a este contenedor.
*/
.layout-main {
  flex: 1;
  overflow: hidden;
  overflow-y: auto;
  background: #f5f4f9;

  /* Scroll suave */
  scroll-behavior: smooth;

  /* Animación de entrada de contenido al expandir/colapsar */
  transition: padding 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Scrollbar discreta */
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