<script setup lang="ts">
import type { PrestamoCreate } from '#shared/types/prestamo'
import { useClientes } from '~/composables/domain/useClientes'
import { useTiposPrestamo } from '~/composables/domain/useTipos'
import { useCapital } from '~/composables/domain/useCapital'
import { usePrestamos } from '~/composables/domain/usePrestamos'
import PrestamoForm from '~/components/prestamos/PrestamoForm.vue'

const props = defineProps<{
  open: boolean
}>()

const emit = defineEmits<{
  'update:open': [value: boolean]
  'creado': [prestamoId: number]
}>()

const isOpen = computed({
  get: () => props.open,
  set: v => emit('update:open', v)
})

const toast = useToast()
const formateo = useFormatters()

const { clientes, fetch: fetchClientes } = useClientes()
const { tipos, fetch: fetchTipos } = useTiposPrestamo()
const { capital, fetch: fetchCapital } = useCapital()
const { crear } = usePrestamos()

const enviando = ref(false)
const formRef = ref<{ submit: () => void } | null>(null)

async function inicializar() {
  await Promise.all([fetchClientes(), fetchTipos(), fetchCapital()])
}

watch(isOpen, (v) => {
  if (v) inicializar()
})

async function guardar(data: PrestamoCreate) {
  enviando.value = true
  try {
    const prestamo = await crear(data)
    toast.add({ title: 'Préstamo creado correctamente', color: 'success' })
    await fetchCapital()
    emit('creado', prestamo.id)
    isOpen.value = false
  } catch (e) {
    const err = e as { status: number, detail: string }
    if (err.status === 400 && /capital insuficiente/i.test(err.detail)) {
      toast.add({ title: 'Capital insuficiente para otorgar el préstamo', color: 'error' })
    } else {
      toast.add({ title: err.detail || 'No se pudo crear el préstamo', color: 'error' })
    }
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
      Nuevo préstamo
    </template>
    <template #body>
      <div class="space-y-4">
        <div class="flex justify-end">
          <span class="text-sm text-gray-500">
            Capital disponible:
            <span class="font-semibold text-primary-600">
              {{ formateo.formatoMoneda(capital?.monto_total ?? 0) }}
            </span>
          </span>
        </div>

        <PrestamoForm
          ref="formRef"
          :clientes="clientes"
          :tipos-prestamo="tipos"
          :capital-disponible="capital?.monto_total ?? 0"
          @guardar="guardar"
        />
      </div>
    </template>
    <template #footer>
      <div class="flex justify-end gap-2">
        <UButton
          label="Cancelar"
          color="neutral"
          variant="outline"
          :disabled="enviando"
          @click="isOpen = false"
        />
        <UButton
          label="Crear préstamo"
          color="primary"
          icon="i-lucide-hand-coins"
          :loading="enviando"
          @click="formRef?.submit()"
        />
      </div>
    </template>
  </UModal>
</template>
