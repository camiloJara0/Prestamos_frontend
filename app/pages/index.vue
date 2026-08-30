<script setup lang="ts">
import { useDashboard } from '~/composables/domain/useDashboard'

definePageMeta({
  middleware: 'auth'
})

const router = useRouter()
const formateo = useFormatters()

const {
  loading,
  error,
  data,
  totalActivos,
  saldoPendienteTotal,
  gananciaNeta,
  totalPrestadoPeriodo,
  totalPerdidas,
  cantidadPerdidos,
  distribucionEstados,
  fetch: fetchDashboard
} = useDashboard()

fetchDashboard()
</script>

<template>
  <div class="p-6 space-y-6">
    <div class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <h1 class="text-2xl font-bold">
          Dashboard
        </h1>
        <p class="text-sm text-gray-500">
          Resumen general del negocio.
        </p>
      </div>
      <UButton
        color="primary"
        icon="i-lucide-refresh-cw"
        :loading="loading"
        @click="fetchDashboard"
      >
        Actualizar
      </UButton>
    </div>

    <div
      v-if="error"
      class="text-center py-8"
    >
      <UAlert
        icon="i-lucide-alert-triangle"
        color="error"
        :title="error"
        :actions="[{ label: 'Reintentar', color: 'primary', variant: 'outline', onClick: fetchDashboard }]"
      />
    </div>

    <template v-else>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <USkeleton
          v-if="loading"
          class="h-22 rounded-xl"
        />
        <UiStatCard
          v-else
          titulo="Capital actual"
          :valor="formateo.formatoMoneda(data.capital?.monto_total ?? 0)"
          icono="i-lucide-wallet"
          color="primary"
        />
        <USkeleton
          v-if="loading"
          class="h-22 rounded-xl"
        />
        <UiStatCard
          v-else
          titulo="Préstamos activos"
          :valor="String(totalActivos)"
          icono="i-lucide-hand-coins"
          color="info"
        />
        <USkeleton
          v-if="loading"
          class="h-22 rounded-xl"
        />
        <UiStatCard
          v-else
          titulo="Saldo pendiente total"
          :valor="formateo.formatoMoneda(saldoPendienteTotal)"
          icono="i-lucide-trending-down"
          color="warning"
        />
        <USkeleton
          v-if="loading"
          class="h-22 rounded-xl"
        />
        <UiStatCard
          v-else
          titulo="Ganancia del periodo"
          :valor="formateo.formatoMoneda(gananciaNeta)"
          icono="i-lucide-trending-up"
          color="success"
          :footer="data.ganancias?.periodo ?? 'Todos los periodos'"
        />
        <USkeleton
          v-if="loading"
          class="h-22 rounded-xl"
        />
        <UiStatCard
          v-else
          titulo="Total prestado"
          :valor="formateo.formatoMoneda(totalPrestadoPeriodo)"
          icono="i-lucide-banknote"
          color="info"
          :footer="data.ganancias?.periodo ?? 'Todos los periodos'"
        />
        <USkeleton
          v-if="loading"
          class="h-22 rounded-xl"
        />
        <UiStatCard
          v-else
          titulo="Préstamos perdidos"
          :valor="`${cantidadPerdidos} (${formateo.formatoMoneda(totalPerdidas)})`"
          icono="i-lucide-alert-octagon"
          color="error"
        />
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <UCard>
          <template #header>
            <h3 class="font-bold">
              Distribución de préstamos
            </h3>
          </template>
          <USkeleton
            v-if="loading"
            class="h-40 rounded-lg"
          />
          <DashboardPieChart
            v-else-if="distribucionEstados.length"
            :data="distribucionEstados"
          />
          <EmptyState
            v-else
            icono="i-lucide-pie-chart"
            titulo="Sin datos"
            descripcion="No hay préstamos registrados para mostrar la distribución."
          />
        </UCard>

        <UCard>
          <template #header>
            <h3 class="font-bold">
              Accesos rápidos
            </h3>
          </template>
          <div class="grid grid-cols-2 gap-3">
            <UButton
              label="Nuevo préstamo"
              icon="i-lucide-plus"
              color="primary"
              class="justify-start"
              @click="() => { router.push('/prestamos/nuevo') }"
            />
            <UButton
              label="Registrar pago"
              icon="i-lucide-dollar-sign"
              color="success"
              class="justify-start"
              @click="() => { router.push('/pagos') }"
            />
            <UButton
              label="Clientes"
              icon="i-lucide-users"
              color="info"
              variant="outline"
              class="justify-start"
              @click="() => { router.push('/clientes') }"
            />
            <UButton
              label="Reportes"
              icon="i-lucide-bar-chart-2"
              color="warning"
              variant="outline"
              class="justify-start"
              @click="() => { router.push('/reportes') }"
            />
          </div>
          <template #footer>
            <p class="text-xs text-gray-400">
              Los datos históricos por mes requieren el endpoint de dashboard (REQUIERE_BACKEND B3).
            </p>
          </template>
        </UCard>
      </div>
    </template>
  </div>
</template>
