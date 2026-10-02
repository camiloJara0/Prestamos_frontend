<script setup lang="ts">
import type { PagoCreate } from '#shared/types/pago'
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
const { crear } = usePagos()
const { tipos: tiposPago, fetch: fetchTiposPago } = useTiposPago()

const formRef = ref<{ submit: () => void } | null>(null)
const enviando = ref(false)

async function inicializar() {
  await fetchTiposPago()
}

watch(isOpen, (v) => {
  if (v) inicializar()
})

async function guardar(data: PagoCreate) {
  enviando.value = true
  try {
    await crear(data)
    toast.add({ title: 'Pago registrado correctamente', color: 'success' })
    emit('pagado')
    isOpen.value = false
  } catch (e) {
    const err = e as { status: number, detail: string }
    toast.add({ title: err.detail || 'No se pudo registrar el pago', color: 'error' })
  } finally {
    enviando.value = false
  }
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
      <PagoForm
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
          label="Cancelar"
          color="neutral"
          variant="outline"
          :disabled="enviando"
          @click="() => { isOpen = false }"
        />
        <UButton
          label="Registrar pago"
          color="primary"
          icon="i-lucide-check"
          :loading="enviando"
          @click="formRef?.submit()"
        />
      </div>
    </template>
  </UModal>
</template>
