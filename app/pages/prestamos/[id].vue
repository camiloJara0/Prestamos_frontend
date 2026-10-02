<script setup lang="ts">
import type { PrestamoCuota } from '#shared/types/prestamo_cuota'
import { usePrestamos } from '~/composables/domain/usePrestamos'
import StatCard from '~/components/ui/StatCard.vue'
import EstadoBadge from '~/components/ui/EstadoBadge.vue'
import PrestamoTabs from '~/components/prestamos/PrestamoTabs.vue'
import PrestamoPagoModal from '~/components/prestamos/PrestamoPagoModal.vue'
import RenovarModal from '~/components/prestamos/RenovarModal.vue'
import MarcarPerdidoModal from '~/components/prestamos/MarcarPerdidoModal.vue'

definePageMeta({
  middleware: 'auth'
})

const route = useRoute()
const router = useRouter()
const toast = useToast()
const formateo = useFormatters()

const prestamoId = computed(() => Number(route.params.id))

const { detalle, loading, error, byId, renovar, marcarPerdido } = usePrestamos()

const renovarAbierto = ref(false)
const perdidoAbierto = ref(false)
const pagoAbierto = ref(false)
const cuotaSeleccionada = ref<PrestamoCuota | null>(null)

async function inicializar() {
  await byId(prestamoId.value)
}
inicializar()

const prestamo = computed(() => detalle.value)
const esActivo = computed(() => prestamo.value?.estado === 'activo')

function abrirPagoCuota(cuota: PrestamoCuota) {
  cuotaSeleccionada.value = cuota
  pagoAbierto.value = true
}

function abrirPagoGeneral() {
  cuotaSeleccionada.value = null
  pagoAbierto.value = true
}

async function confirmarRenovar(data: { porcentaje_interes: number, numero_cuotas: number, abono: number, fecha_renovacion: string, observaciones?: string | null }) {
  try {
    const nuevo = await renovar(prestamoId.value, {
      porcentaje_interes: data.porcentaje_interes,
      numero_cuotas: data.numero_cuotas,
      abono: data.abono,
      fecha_renovacion: data.fecha_renovacion,
      observaciones: data.observaciones
    })
    toast.add({ title: `Préstamo renovado · nuevo préstamo #${nuevo.id}`, color: 'success' })
    renovarAbierto.value = false
  } catch (e) {
    toast.add({ title: (e as { detail: string }).detail || 'No se pudo renovar el préstamo', color: 'error' })
  }
}

async function confirmarPerdido(data: { motivo?: string | null, fecha: string }) {
  try {
    await marcarPerdido(prestamoId.value, data)
    toast.add({ title: 'Préstamo marcado como perdido', color: 'success' })
    perdidoAbierto.value = false
  } catch (e) {
    toast.add({ title: (e as { detail: string }).detail || 'No se pudo marcar el préstamo', color: 'error' })
  }
}

async function despuesDePago() {
  cuotaSeleccionada.value = null
  await byId(prestamoId.value)
}
</script>

<template>
  <div class="p-6 space-y-6">
    <div v-if="loading">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <USkeleton
          v-for="i in 8"
          :key="i"
          class="h-24 w-full"
        />
      </div>
    </div>

    <div
      v-else-if="error"
      class="flex flex-col items-center gap-3 py-10"
    >
      <UIcon
        name="i-lucide-alert-triangle"
        class="text-3xl text-error"
      />
      <p class="text-sm text-gray-500">
        {{ error }}
      </p>
      <UButton
        color="primary"
        variant="outline"
        size="sm"
        icon="i-lucide-refresh-cw"
        @click="inicializar"
      >
        Reintentar
      </UButton>
    </div>

    <template v-else-if="prestamo">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <div class="flex items-center gap-3">
          <UButton
            icon="i-lucide-arrow-left"
            color="neutral"
            variant="ghost"
            @click="() => { router.push('/prestamos') }"
          />
          <div>
            <h1 class="text-2xl font-bold">
              Préstamo #{{ prestamo.id }}
            </h1>
            <p class="text-sm text-gray-500">
              {{ prestamo.cliente?.nombre }} · C.C {{ prestamo.cliente?.cedula }}
            </p>
          </div>
          <EstadoBadge
            entidad="prestamo"
            :estado="prestamo.estado"
          />
        </div>
        <div
          v-if="esActivo"
          class="flex gap-2"
        >
          <UButton
            color="primary"
            icon="i-lucide-credit-card"
            @click="abrirPagoGeneral"
          >
            Registrar pago
          </UButton>
          <UButton
            color="primary"
            icon="i-lucide-refresh-cw"
            variant="outline"
            @click="() => { renovarAbierto = true }"
          >
            Renovar
          </UButton>
          <UButton
            color="error"
            variant="outline"
            icon="i-lucide-flag"
            @click="() => { perdidoAbierto = true }"
          >
            Perdido
          </UButton>
        </div>
      </div>

      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard
          titulo="Capital prestado"
          :valor="formateo.formatoMoneda(prestamo.capital_prestado)"
          icono="i-lucide-coins"
        />
        <StatCard
          titulo="Interés total"
          :valor="formateo.formatoMoneda(prestamo.interes_total)"
          icono="i-lucide-percent"
        />
        <StatCard
          titulo="Monto total"
          :valor="formateo.formatoMoneda(prestamo.monto_total)"
          icono="i-lucide-banknote"
        />
        <StatCard
          titulo="Saldo pendiente"
          :valor="formateo.formatoMoneda(prestamo.saldo_pendiente)"
          icono="i-lucide-wallet"
          color="warning"
        />
        <StatCard
          titulo="Valor cuota"
          :valor="formateo.formatoMoneda(prestamo.valor_cuota)"
          icono="i-lucide-calendar"
        />
        <StatCard
          titulo="N° cuotas"
          :valor="String(prestamo.numero_cuotas)"
          icono="i-lucide-hash"
        />
        <StatCard
          titulo="Fecha préstamo"
          :valor="formateo.formatoFecha(prestamo.fecha_prestamo)"
          icono="i-lucide-calendar-check"
        />
        <StatCard
          titulo="Interés mensual"
          :valor="formateo.formatoPorcentaje(prestamo.porcentaje_interes)"
          icono="i-lucide-percent"
        />
      </div>

      <PrestamoTabs
        :prestamo="prestamo"
        @pagar="abrirPagoCuota"
      />
    </template>

    <PrestamoPagoModal
      :open="pagoAbierto"
      :prestamo="prestamo"
      :cuota="cuotaSeleccionada"
      @update:open="pagoAbierto = $event"
      @pagado="despuesDePago"
    />

    <RenovarModal
      :open="renovarAbierto"
      :prestamo="prestamo"
      @update:open="renovarAbierto = $event"
      @confirmar="confirmarRenovar"
    />

    <MarcarPerdidoModal
      :open="perdidoAbierto"
      :prestamo="prestamo"
      @update:open="perdidoAbierto = $event"
      @confirmar="confirmarPerdido"
    />
  </div>
</template>
