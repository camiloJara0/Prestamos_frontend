<script setup lang="ts">
const route = useRoute()
const auth = useAuthStore()
const varView = useVarView()
const colorMode = useColorMode()
const toast = useToast()
const calculadoraAbierta = ref(false)
const importarAbierto = ref(false)

const breadcrumbs = computed(() => {
  const segments = route.path.split('/').filter(Boolean)
  return segments.map((s, i) => ({
    label: s.charAt(0).toUpperCase() + s.slice(1).replace(/-/g, ' '),
    to: '/' + segments.slice(0, i + 1).join('/')
  }))
})

const isDark = computed(() => colorMode.value === 'dark')

function toggleColorMode() {
  colorMode.preference = isDark.value ? 'light' : 'dark'
}

const userMenuItems = computed(() => [
  { label: auth.user?.nombre ?? 'Usuario', disabled: true },
  { label: auth.user?.email ?? '', disabled: true },
  { type: 'separator' as const },
  { label: 'Perfil', icon: 'i-lucide-user', to: '/perfil' },
  { label: 'Atajos (Ctrl+K)', icon: 'i-lucide-keyboard', click: () => {} },
  { type: 'separator' as const },
  { label: 'Cerrar sesión', icon: 'i-lucide-log-out', click: () => cerrarSesion() }
])

async function cerrarSesion() {
  await auth.logout()
  await navigateTo('/login')
}

if (import.meta.client) {
  window.addEventListener('controllerchange', () => {
    toast.add({ title: 'Hay una nueva versión disponible', color: 'info', actions: [{ label: 'Recargar', color: 'primary', onClick: () => location.reload() }] })
  })
}
</script>

<template>
  <header class="flex items-center gap-4 px-5 py-3 border-b border-gray-100 dark:border-gray-800/50 bg-white/80 dark:bg-gray-900/80 backdrop-blur-xl">
    <UButton
      icon="i-lucide-menu"
      color="neutral"
      variant="ghost"
      size="sm"
      @click="varView.toggleAside()"
    />

    <div class="flex items-center gap-1.5 text-sm text-gray-400 min-w-0">
      <NuxtLink
        to="/"
        class="hover:text-primary transition-colors truncate"
      >
        <UIcon
          name="i-lucide-home"
          class="w-4 h-4"
        />
      </NuxtLink>
      <template
        v-for="(crumb, i) in breadcrumbs"
        :key="crumb.to"
      >
        <UIcon
          name="i-lucide-chevron-right"
          class="w-3 h-3 shrink-0 text-gray-300 dark:text-gray-600"
        />
        <NuxtLink
          :to="crumb.to"
          class="hover:text-primary transition-colors truncate"
          :class="{ 'text-gray-900 dark:text-white font-semibold': i === breadcrumbs.length - 1 }"
        >
          {{ crumb.label }}
        </NuxtLink>
      </template>
    </div>

    <div class="flex-1" />

    <UInput
      placeholder="Buscar..."
      icon="i-lucide-search"
      class="w-48 hidden md:block"
      disabled
    />

    <div class="h-5 w-px bg-gray-200 dark:bg-gray-700 hidden md:block" />

    <AppSyncIndicator />

    <AppInstallPrompt />

    <UButton
      icon="i-lucide-calculator"
      color="neutral"
      variant="ghost"
      size="sm"
      @click="calculadoraAbierta = true"
    />

    <UButton
      v-if="auth.isAdmin"
      icon="i-lucide-upload"
      color="neutral"
      variant="ghost"
      size="sm"
      label="Importar"
      class="hidden md:flex"
      @click="importarAbierto = true"
    />

    <div class="h-5 w-px bg-gray-200 dark:bg-gray-700 hidden md:block" />

    <UButton
      :icon="isDark ? 'i-lucide-sun' : 'i-lucide-moon'"
      color="neutral"
      variant="ghost"
      size="sm"
      @click="toggleColorMode"
    />

    <UDropdownMenu :items="userMenuItems">
      <UButton
        color="neutral"
        variant="ghost"
        icon="i-lucide-user"
        size="sm"
        :label="auth.user?.nombre ?? 'Usuario'"
      />
    </UDropdownMenu>

    <AppGlobalCalculator
      :open="calculadoraAbierta"
      @update:open="calculadoraAbierta = $event"
    />

    <AppImportExtractModal
      :open="importarAbierto"
      @update:open="importarAbierto = $event"
    />
  </header>
</template>
