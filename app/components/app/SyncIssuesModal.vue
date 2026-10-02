<script setup lang="ts">
import { getPendientes, marcarFailed, incrementarIntentos } from '~/services/db/outbox'

const props = defineProps<{
  open: boolean
}>()

const emit = defineEmits<{
  'update:open': [value: boolean]
}>()

const toast = useToast()
const items = ref<Awaited<ReturnType<typeof getPendientes>>>([])
const procesando = ref(false)

async function cargar() {
  items.value = await getPendientes()
}

watch(() => props.open, (val) => {
  if (val) cargar()
})

async function reintentar(id: string) {
  procesando.value = true
  try {
    const item = items.value.find(i => i.id === id)
    if (!item) return
    await incrementarIntentos(id)
    toast.add({ title: 'Reintentando...', color: 'info' })
    await cargar()
  } finally {
    procesando.value = false
  }
}

function descartar(id: string) {
  marcarFailed(id, 'Descartado por el usuario')
  toast.add({ title: 'Operación descartada', color: 'warning' })
  cargar()
}
</script>

<template>
  <UModal
    :open="open"
    title="Operaciones pendientes"
    :ui="{ content: 'max-w-lg' }"
    @update:open="emit('update:open', $event)"
  >
    <template #body>
      <div
        v-if="!items.length"
        class="text-center py-6 text-gray-500"
      >
        No hay operaciones pendientes.
      </div>
      <div
        v-else
        class="space-y-3"
      >
        <div
          v-for="item in items"
          :key="item.id"
          class="flex items-start justify-between gap-3 p-3 rounded-lg border border-gray-200 dark:border-gray-700"
        >
          <div class="min-w-0">
            <p class="text-sm font-medium">
              {{ item.tipo }} — {{ new Date(item.createdAt).toLocaleString('es-CO') }}
            </p>
            <p class="text-xs text-gray-500 mt-1">
              Intentos: {{ item.intentos }}
              <span v-if="item.lastError"> · {{ item.lastError }}</span>
            </p>
          </div>
          <div class="flex gap-1 shrink-0">
            <UButton
              icon="i-lucide-refresh-cw"
              color="primary"
              variant="ghost"
              size="xs"
              :loading="procesando"
              @click="reintentar(item.id)"
            />
            <UButton
              icon="i-lucide-trash-2"
              color="error"
              variant="ghost"
              size="xs"
              @click="descartar(item.id)"
            />
          </div>
        </div>
      </div>
    </template>
  </UModal>
</template>
