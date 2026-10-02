<script setup lang="ts">
import type { Pago, PagoCreate } from '#shared/types/pago'
import type { PrestamoDetalle } from '#shared/types/prestamo'
import type { PrestamoCuota } from '#shared/types/prestamo_cuota'
import { usePagos } from '~/composables/domain/usePagos'
import { useTiposPago } from '~/composables/domain/useTipos'
import PagoForm from '~/components/pagos/PagoForm.vue'

const props = defineProps<{
  open: boolean
  prestamo: PrestamoDetalle | null
  cuota?: PrestamoCuota | null
}>()

const emit = defineEmits<{
  'update:open': [value: boolean]
  'pagado': []
}>()

const isOpen = computed({
  get: () => props.open,
  set: v => emit('update:open', v)
})

const toast = useToast()
const formateo = useFormatters()
const { crear, descargarComprobante } = usePagos()
const { tipos: tiposPago, fetch: fetchTiposPago } = useTiposPago()

const formRef = ref<{ submit: () => void } | null>(null)
const enviando = ref(false)
const pagoCreado = ref<Pago | null>(null)
const descargandoComprobante = ref(false)

async function inicializar() {
  pagoCreado.value = null
  await fetchTiposPago()
}

watch(isOpen, (v) => {
  if (v) inicializar()
})

async function guardar(data: PagoCreate) {
  enviando.value = true
  try {
    const pago = await crear(data)
    pagoCreado.value = pago
    toast.add({ title: 'Pago registrado correctamente', color: 'success' })
    emit('pagado')
  } catch (e) {
    const err = e as { status: number, detail: string }
    toast.add({ title: err.detail || 'No se pudo registrar el pago', color: 'error' })
  } finally {
    enviando.value = false
  }
}

async function descargarComprobantePago() {
  if (!pagoCreado.value) return
  descargandoComprobante.value = true
  try {
    await descargarComprobante(pagoCreado.value.id)
    toast.add({ title: 'Comprobante descargado', color: 'success' })
  } catch {
    toast.add({ title: 'No se pudo generar el comprobante', color: 'error' })
  } finally {
    descargandoComprobante.value = false
  }
}

function cerrar() {
  isOpen.value = false
}
</script>

<template>
  <UModal
    :open="isOpen"
    @update:open="isOpen = $event"
  >
    <template #title>
      Registrar pago — Préstamo #{{ prestamo?.id }}
    </template>
    <template #body>
      <div
        v-if="pagoCreado"
        class="space-y-4 py-2 text-center"
      >
        <div class="flex justify-center">
          <div class="w-14 h-14 rounded-full bg-success/10 flex items-center justify-center">
            <UIcon
              name="i-lucide-check"
              class="text-3xl text-success"
            />
          </div>
        </div>
        <div>
          <p class="font-semibold">
            Pago registrado
          </p>
          <p class="text-sm text-gray-500">
            Recibo {{ pagoCreado.referencia_recibo }} · {{ formateo.formatoMoneda(pagoCreado.valor_pagado) }}
          </p>
        </div>
        <UButton
          label="Descargar comprobante (PDF)"
          icon="i-lucide-file-down"
          color="primary"
          variant="outline"
          :loading="descargandoComprobante"
          @click="descargarComprobantePago"
        />
      </div>
      <PagoForm
        v-else
        ref="formRef"
        :prestamo-inicial="prestamo"
        :cuota-inicial="cuota ?? null"
        :tipos-pago="tiposPago"
        @guardar="guardar"
      />
    </template>
    <template #footer>
      <div class="flex justify-end gap-2">
        <UButton
          v-if="pagoCreado"
          label="Cerrar"
          color="primary"
          icon="i-lucide-check"
          @click="cerrar"
        />
        <template v-else>
          <UButton
            label="Cancelar"
            color="neutral"
            variant="outline"
            :disabled="enviando"
            @click="cerrar"
          />
          <UButton
            label="Registrar pago"
            color="primary"
            icon="i-lucide-check"
            :loading="enviando"
            @click="formRef?.submit()"
          />
        </template>
      </div>
    </template>
  </UModal>
</template>
