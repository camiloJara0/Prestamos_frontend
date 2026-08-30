<script setup lang="ts">
const route = useRoute()
const auth = useAuthStore()
const varView = useVarView()
const colorMode = useColorMode()

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
  { label: 'Cerrar sesión', icon: 'i-lucide-log-out', click: () => cerrarSesion() }
])

async function cerrarSesion() {
  await auth.logout()
  await navigateTo('/login')
}
</script>

<template>
  <header class="flex items-center gap-4 px-6 py-3 border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">
    <UButton
      icon="i-lucide-menu"
      color="neutral"
      variant="ghost"
      @click="varView.toggleAside()"
    />

    <div class="flex items-center gap-1 text-sm text-gray-500 min-w-0">
      <NuxtLink
        to="/"
        class="hover:text-primary truncate"
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
          class="w-3 h-3 shrink-0 text-gray-400"
        />
        <NuxtLink
          :to="crumb.to"
          class="hover:text-primary truncate"
          :class="{ 'text-gray-900 dark:text-white font-medium': i === breadcrumbs.length - 1 }"
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

    <AppSyncIndicator />

    <UButton
      :icon="isDark ? 'i-lucide-sun' : 'i-lucide-moon'"
      color="neutral"
      variant="ghost"
      @click="toggleColorMode"
    />

    <UDropdownMenu :items="userMenuItems">
      <UButton
        color="neutral"
        variant="ghost"
        icon="i-lucide-user"
        :label="auth.user?.nombre ?? 'Usuario'"
      />
    </UDropdownMenu>
  </header>
</template>
