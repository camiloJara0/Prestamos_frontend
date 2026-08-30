<script setup lang="ts">
definePageMeta({
  middleware: 'admin'
})
</script>

<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold">
      Usuarios
    </h1>
    <p class="text-sm text-gray-500">
      La gestión de usuarios estará disponible próximamente. Requiere el CRUD `/usuarios` en el backend.
    </p>
    <EmptyState
      class="mt-6"
      icono="i-lucide-user-cog"
      titulo="Gestión de usuarios"
      descripcion="El backend aún no expone el CRUD de usuarios."
    />
  </div>
</template>
