<script setup lang="ts">
import type { CobranzaNota } from '~/services/db/db'
import { agregarNota, obtenerNotas } from '~/services/db/cobranza'
import EmptyState from '~/components/ui/EmptyState.vue'

const props = defineProps<{
  open: boolean
  prestamoId: number | null
}>()

const emit = defineEmits<{
  'update:open': [value: boolean]
}>()

const isOpen = computed({
  get: () => props.open,
  set: v => emit('update:open', v)
})

const toast = useToast()
const notas = ref<CobranzaNota[]>([])
const cargando = ref(false)
const texto = ref('')
const guardando = ref(false)

async function cargarNotas() {
  if (!props.prestamoId) return
  cargando.value = true
  try {
    notas.value = await obtenerNotas(props.prestamoId)
  } finally {
    cargando.value = false
  }
}

watch(isOpen, (v) => {
  if (v) {
    texto.value = ''
    cargarNotas()
  }
})

async function guardarNota() {
  const contenido = texto.value.trim()
  if (!props.prestamoId || !contenido) return
  guardando.value = true
  try {
    await agregarNota(props.prestamoId, 'contacto', contenido)
    texto.value = ''
    await cargarNotas()
    toast.add({ title: 'Contacto registrado', color: 'success' })
  } catch {
    toast.add({ title: 'No se pudo registrar el contacto', color: 'error' })
  } finally {
    guardando.value = false
  }
}

function formatoFechaHora(fecha: string) {
  const d = new Date(fecha)
  return Number.isNaN(d.getTime()) ? '—' : d.toLocaleString('es-CO')
}
</script>

<template>
  <UModal
    :open="isOpen"
    @update:open="isOpen = $event"
  >
    <template #title>
      Registro de contacto · Préstamo #{{ prestamoId }}
    </template>

    <template #body>
      <div class="space-y-4">
        <UFormField label="Nota de contacto">
          <UTextarea
            v-model="texto"
            :rows="3"
            placeholder="Resultado del contacto con el cliente (llamada, visita, acuerdo...)"
            class="w-full"
          />
        </UFormField>

        <UButton
          color="primary"
          icon="i-lucide-save"
          :loading="guardando"
          :disabled="!texto.trim()"
          @click="guardarNota"
        >
          Registrar contacto
        </UButton>

        <div class="space-y-2">
          <h4 class="text-sm font-semibold">
            Historial de contactos
          </h4>

          <USkeleton
            v-if="cargando"
            class="h-20 rounded-lg"
          />

          <EmptyState
            v-else-if="!notas.length"
            icono="i-lucide-message-square"
            titulo="Sin contactos"
            descripcion="Aún no se han registrado contactos para este préstamo."
          />

          <div
            v-for="nota in notas"
            :key="nota.id"
            class="p-3 rounded-lg bg-gray-50 dark:bg-gray-800 text-sm"
          >
            <div class="flex justify-between gap-2 text-xs text-gray-500">
              <span>{{ formatoFechaHora(nota.fecha) }}</span>
              <span>{{ nota.usuario ?? '—' }}</span>
            </div>
            <p class="mt-1 whitespace-pre-wrap">
              {{ nota.contenido }}
            </p>
          </div>
        </div>
      </div>
    </template>
  </UModal>
</template>
