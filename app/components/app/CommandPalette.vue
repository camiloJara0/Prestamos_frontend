<script setup lang="ts">
const router = useRouter()
const auth = useAuthStore()

const open = ref(false)
const query = ref('')

const allItems = [
  { label: 'Dashboard', icon: 'i-lucide-layout-dashboard', to: '/' },
  { label: 'Crear préstamo', icon: 'i-lucide-plus', to: '/prestamos/nuevo' },
  { label: 'Préstamos', icon: 'i-lucide-hand-coins', to: '/prestamos' },
  { label: 'Registrar pago', icon: 'i-lucide-dollar-sign', to: '/pagos' },
  { label: 'Clientes', icon: 'i-lucide-users', to: '/clientes' },
  { label: 'Cobranza', icon: 'i-lucide-phone', to: '/cobranza' },
  { label: 'Reportes', icon: 'i-lucide-bar-chart-2', to: '/reportes' },
  { label: 'Moras', icon: 'i-lucide-alert-triangle', to: '/moras' },
  { label: 'Capital', icon: 'i-lucide-wallet', to: '/capital' },
  { label: 'Parámetros del sistema', icon: 'i-lucide-settings', to: '/configuracion' },
  { label: 'Auditoría', icon: 'i-lucide-shield-check', to: '/auditoria' },
  { label: 'Tipos de préstamo', icon: 'i-lucide-tag', to: '/tipos-prestamo' },
  { label: 'Tipos de pago', icon: 'i-lucide-credit-card', to: '/tipos-pago' },
  { label: 'Cerrar sesión', icon: 'i-lucide-log-out', action: () => cerrarSesion() }
]

const filteredItems = computed(() => {
  return allItems.filter((item) => {
    if (item.to && !auth.isAdmin && ['/tipos-prestamo', '/tipos-pago', '/capital', '/configuracion', '/auditoria', '/moras'].includes(item.to)) {
      return false
    }
    return true
  })
})

function select(item: typeof allItems[0]) {
  if (item.action) {
    item.action()
  } else if (item.to) {
    router.push(item.to)
  }
  open.value = false
}

async function cerrarSesion() {
  await auth.logout()
  await navigateTo('/login')
}

const { register } = useShortcuts()
register('ctrl+k', () => {
  open.value = !open.value
})
</script>

<template>
  <UModal
    :open="open"
    :ui="{ content: 'max-w-lg' }"
    @update:open="open = $event"
  >
    <template #body>
      <UInput
        v-model="query"
        placeholder="Buscar..."
        icon="i-lucide-search"
        autofocus
        class="mb-4"
        size="lg"
        @keydown.escape="open = false"
      />
      <div class="max-h-[40vh] overflow-y-auto -mx-2">
        <div
          v-for="item in filteredItems"
          :key="item.label"
          class="flex items-center gap-3 px-3 py-2.5 rounded-xl cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-all duration-150"
          @click="select(item)"
        >
          <UIcon
            :name="item.icon"
            class="w-4 h-4 text-gray-400 dark:text-gray-500"
          />
          <span class="text-sm font-medium text-gray-700 dark:text-gray-300">{{ item.label }}</span>
          <span
            v-if="item.to"
            class="text-xs text-gray-400 dark:text-gray-500 ml-auto font-mono"
          >{{ item.to }}</span>
        </div>
      </div>
    </template>
  </UModal>
</template>
