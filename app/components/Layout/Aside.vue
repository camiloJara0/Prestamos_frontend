<script setup lang="ts">
import { ref, computed } from 'vue'

const varView = useVarView()

const route = useRoute()

const navSections = [
  {
    label: 'Principal',
    items: [
      { label: 'Dashboard', icon: 'i-lucide-layout-dashboard', to: '/dashboard' },
      { label: 'Resumen', icon: 'i-lucide-chart-pie', to: '/resumen' },
    ]
  },
  {
    label: 'Préstamos',
    items: [
      { label: 'Préstamos', icon: 'i-lucide-hand-coins', to: '/prestamos' },
      { label: 'Solicitudes', icon: 'i-lucide-file-text', to: '/solicitudes' },
      { label: 'Pagos', icon: 'i-lucide-credit-card', to: '/pagos' },
      { label: 'Cuotas', icon: 'i-lucide-calendar-check', to: '/cuotas' },
    ]
  },
  {
    label: 'Clientes',
    items: [
      { label: 'Clientes', icon: 'i-lucide-users', to: '/clientes' },
      { label: 'Garantes', icon: 'i-lucide-shield-check', to: '/garantes' },
    ]
  },
  {
    label: 'Reportes',
    items: [
      { label: 'Informes', icon: 'i-lucide-bar-chart-2', to: '/informes' },
      { label: 'Cobranza', icon: 'i-lucide-trending-up', to: '/cobranza' },
    ]
  },
  {
    label: 'Sistema',
    items: [
      { label: 'Configuración', icon: 'i-lucide-settings', to: '/configuracion' },
    ]
  }
]

const isActive = (path: string) => route.path === path
</script>

<template>
  <aside class="aside-root relative h-screen w-55 bg-(--aside-bg) flex flex-col overflow-hidden" :class="{ collapsed: !varView.showAside }">

    <!-- Logo / Marca -->
    <div class="border-b border-gray-700 flex items-center gap-2.5 p-[20px_14px_16px] min-h-17">
      <div class="shrink-0 w-7.5 h-7.5 rounded-lg flex items-center justify-center bg-[rgba(124,58,237,0.22)]">
        <UIcon name="i-lucide-landmark" class="text-lg text-[#a78bf4]" />
      </div>
      <Transition name="fade-text">
        <div v-if="varView.showAside" class="flex flex-col gap-0.5 overflow-hidden text-nowrap">
          <span class=" text-lg font-bold text-white tracking-wide">LoanSoft</span>
          <span class=" text-xs text-gray-400 uppercase">Gestión de Crédito</span>
        </div>
      </Transition>
    </div>

    <!-- Toggle -->
    <button class="toggle-btn absolute top-5 right-2.5 w-6 h-6 rounded-xs border-none bg-transparent text-(--text-label) flex items-center justify-center cursor-pointer" @click="varView.showAside = !varView.showAside" :title="varView.showAside ? 'Contraer menú' : 'Expandir menú'">
      <UIcon :name="varView.showAside ? 'i-lucide-panel-left-close' : 'i-lucide-panel-left-open'" class="toggle-icon" />
    </button>

    <!-- Navegación -->
    <nav class="aside-nav">
      <div v-for="section in navSections" :key="section.label" class="nav-section">
        <Transition name="fade-text">
          <p v-if="varView.showAside" class="section-label">{{ section.label }}</p>
        </Transition>
        <div v-if="!varView.showAside" class="section-divider" />

        <NuxtLink
          v-for="item in section.items"
          :key="item.to"
          :to="item.to"
          class="nav-item"
          :class="{ active: isActive(item.to) }"
        >
          <UIcon :name="item.icon" class="nav-icon" />
          <Transition name="fade-text">
            <span v-if="varView.showAside" class="nav-label">{{ item.label }}</span>
          </Transition>
          <Transition name="fade-text">
            <span v-if="varView.showAside && isActive(item.to)" class="active-dot" />
          </Transition>
        </NuxtLink>
      </div>
    </nav>

    <!-- Footer usuario -->
    <div class="aside-footer">
      <div class="user-avatar">AG</div>
      <Transition name="fade-text">
        <div v-if="varView.showAside" class="user-info">
          <span class="user-name">Ana García</span>
          <span class="user-role">Administradora</span>
        </div>
      </Transition>
      <Transition name="fade-text">
        <UButton
          v-if="varView.showAside"
          to="/"
          icon="i-lucide-log-out"
          color="neutral"
          variant="ghost"
          size="xs"
          class="logout-btn"
          title="Cerrar sesión"
        />
      </Transition>
    </div>

  </aside>
</template>

<style scoped>

/* ── Aside raíz ── */
.aside-root {
  border-right: 1px solid rgba(124, 58, 237, 0.15);
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  will-change: width;
}

.aside-root.collapsed {
  width: 56px;
}

/* ── Toggle ── */
.toggle-btn {
  transition: color 0.2s, background 0.2s;
}

.toggle-btn:hover {
  color: #a78bfa;
  background: rgba(124, 58, 237, 0.1);
}

.toggle-icon {
  font-size: 15px;
}

/* ── Navegación ── */
.aside-nav {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 8px 8px 12px;
  scrollbar-width: none;
}

.aside-nav::-webkit-scrollbar {
  display: none;
}

.nav-section {
  margin-bottom: 4px;
}

.section-label {
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #6b6678;
  padding: 10px 8px 4px;
  white-space: nowrap;
  overflow: hidden;
}

.section-divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.06);
  margin: 6px 4px;
}

/* ── Item de navegación ── */
.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  border-radius: 8px;
  text-decoration: none;
  color: #9792a8;
  font-size: 13.5px;
  font-weight: 450;
  white-space: nowrap;
  overflow: hidden;
  position: relative;
  transition: background 0.18s ease, color 0.18s ease;
  margin-bottom: 1px;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.05);
  color: #d4d0e8;
}

.nav-item.active {
  background: rgba(124, 58, 237, 0.14);
  color: #c4b5fd;
  border-left: 2px solid #7c3aed;
}

.nav-icon {
  font-size: 16px;
  flex-shrink: 0;
  transition: color 0.18s;
}

.nav-item.active .nav-icon {
  color: #a78bfa;
}

.nav-label {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
}

.active-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: #7c3aed;
  flex-shrink: 0;
}

/* ── Footer ── */
.aside-footer {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 14px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  min-height: 60px;
  overflow: hidden;
}

.user-avatar {
  flex-shrink: 0;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: rgba(124, 58, 237, 0.3);
  border: 1px solid rgba(124, 58, 237, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 600;
  color: #c4b5fd;
  letter-spacing: 0.03em;
}

.user-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1px;
  overflow: hidden;
  white-space: nowrap;
}

.user-name {
  font-size: 12.5px;
  font-weight: 500;
  color: #d4d0e8;
}

.user-role {
  font-size: 10.5px;
  color: #6b6678;
}

.logout-btn {
  flex-shrink: 0;
  color: #6b6678 !important;
}

.logout-btn:hover {
  color: #f87171 !important;
}

/* ── Transición texto fade ── */
.fade-text-enter-active {
  transition: opacity 0.2s ease 0.1s, transform 0.2s ease 0.1s;
}

.fade-text-leave-active {
  transition: opacity 0.12s ease, transform 0.12s ease;
}

.fade-text-enter-from,
.fade-text-leave-to {
  opacity: 0;
  transform: translateX(-6px);
}
</style>