<script setup lang="ts">
import type { ResultadoImportacion } from '#shared/types/extracto'
import { importarExtracto } from '~/services/api/extractos'

const props = defineProps<{
  open: boolean
}>()

const emit = defineEmits<{
  'update:open': [value: boolean]
}>()

const isOpen = computed({
  get: () => props.open,
  set: v => emit('update:open', v)
})

const toast = useToast()
const archivo = ref<File | null>(null)
const cargando = ref(false)
const resultado = ref<ResultadoImportacion | null>(null)
const arrastrando = ref(false)

const formatosSoportados = '.csv,.xlsx,.xls'

function onDrop(e: DragEvent) {
  arrastrando.value = false
  const file = e.dataTransfer?.files[0]
  if (file) seleccionarArchivo(file)
}

function onFileChange(e: Event) {
  const input = e.target as HTMLInputElement
  const file = input.files?.[0]
  if (file) seleccionarArchivo(file)
}

function seleccionarArchivo(file: File) {
  const extensionesPermitidas = ['csv', 'xlsx', 'xls']
  const extension = file.name.split('.').pop()?.toLowerCase()
  if (!extension || !extensionesPermitidas.includes(extension)) {
    toast.add({ title: 'Formato no soportado. Usa CSV o Excel.', color: 'error' })
    return
  }
  if (file.size > 10 * 1024 * 1024) {
    toast.add({ title: 'El archivo supera el tamaño máximo de 10 MB', color: 'error' })
    return
  }
  archivo.value = file
}

function eliminarArchivo() {
  archivo.value = null
  resultado.value = null
}

async function procesar() {
  if (!archivo.value) return
  cargando.value = true
  try {
    resultado.value = await importarExtracto(archivo.value)
    toast.add({ title: 'Extracto procesado correctamente', color: 'success' })
  } catch {
    toast.add({ title: 'Error al procesar el extracto', color: 'error' })
  } finally {
    cargando.value = false
  }
}

function cerrar() {
  archivo.value = null
  resultado.value = null
  isOpen.value = false
}

watch(isOpen, (v) => {
  if (!v) {
    archivo.value = null
    resultado.value = null
  }
})
</script>

<template>
  <UModal
    :open="isOpen"
    :ui="{ content: 'max-w-lg' }"
    @update:open="isOpen = $event"
  >
    <template #title>
      Importar extracto bancario
    </template>
    <template #body>
      <div
        v-if="!resultado"
        class="space-y-4"
      >
        <div
          class="border-2 border-dashed rounded-xl p-8 text-center transition-colors cursor-pointer"
          :class="arrastrando ? 'border-primary bg-primary/5' : 'border-gray-300 dark:border-gray-700 hover:border-primary/50'"
          @dragover.prevent="arrastrando = true"
          @dragleave="arrastrando = false"
          @drop.prevent="onDrop"
          @click="($refs.fileInput as HTMLInputElement).click()"
        >
          <UIcon
            name="i-lucide-upload-cloud"
            class="text-4xl text-gray-400 mb-3"
          />
          <p class="text-sm font-medium text-gray-700 dark:text-gray-300">
            Arrastra un archivo aquí o haz clic para seleccionar
          </p>
          <p class="text-xs text-gray-400 mt-1">
            Formatos soportados: CSV, XLSX · Máximo 10 MB
          </p>
          <input
            ref="fileInput"
            type="file"
            :accept="formatosSoportados"
            class="hidden"
            @change="onFileChange"
          >
        </div>

        <div
          v-if="archivo"
          class="flex items-center gap-3 p-3 rounded-lg bg-gray-50 dark:bg-gray-800"
        >
          <UIcon
            name="i-lucide-file-spreadsheet"
            class="text-lg text-primary"
          />
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium truncate">
              {{ archivo.name }}
            </p>
            <p class="text-xs text-gray-400">
              {{ (archivo.size / 1024).toFixed(1) }} KB
            </p>
          </div>
          <UButton
            icon="i-lucide-x"
            color="neutral"
            variant="ghost"
            size="xs"
            @click="eliminarArchivo"
          />
        </div>
      </div>

      <div
        v-else
        class="space-y-4"
      >
        <div class="grid grid-cols-2 gap-3">
          <div class="p-3 rounded-lg bg-green-50 dark:bg-green-900/20 text-center">
            <p class="text-2xl font-bold text-green-600 dark:text-green-400">
              {{ resultado.cuotas_identificadas.length }}
            </p>
            <p class="text-xs text-green-600 dark:text-green-400">
              Cuotas identificadas
            </p>
          </div>
          <div class="p-3 rounded-lg bg-blue-50 dark:bg-blue-900/20 text-center">
            <p class="text-2xl font-bold text-blue-600 dark:text-blue-400">
              {{ resultado.pagos_aplicados.length }}
            </p>
            <p class="text-xs text-blue-600 dark:text-blue-400">
              Pagos aplicados
            </p>
          </div>
          <div class="p-3 rounded-lg bg-red-50 dark:bg-red-900/20 text-center">
            <p class="text-2xl font-bold text-red-600 dark:text-red-400">
              {{ resultado.errores.length }}
            </p>
            <p class="text-xs text-red-600 dark:text-red-400">
              Errores
            </p>
          </div>
          <div class="p-3 rounded-lg bg-amber-50 dark:bg-amber-900/20 text-center">
            <p class="text-2xl font-bold text-amber-600 dark:text-amber-400">
              {{ resultado.pendientes_revision.length }}
            </p>
            <p class="text-xs text-amber-600 dark:text-amber-400">
              Pendientes revisión
            </p>
          </div>
        </div>

        <div
          v-if="resultado.errores.length"
          class="space-y-2"
        >
          <h4 class="text-sm font-semibold text-red-600">
            Errores
          </h4>
          <div
            v-for="(item, i) in resultado.errores"
            :key="i"
            class="text-xs p-2 rounded bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300"
          >
            {{ item.detalle }} — ${{ item.valor_pagado.toLocaleString('es-CO') }}
          </div>
        </div>

        <div
          v-if="resultado.pendientes_revision.length"
          class="space-y-2"
        >
          <h4 class="text-sm font-semibold text-amber-600">
            Pendientes de revisión
          </h4>
          <div
            v-for="(item, i) in resultado.pendientes_revision"
            :key="i"
            class="text-xs p-2 rounded bg-amber-50 dark:bg-amber-900/20 text-amber-700 dark:text-amber-300"
          >
            {{ item.detalle }} — ${{ item.valor_pagado.toLocaleString('es-CO') }}
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <div class="flex justify-end gap-2">
        <UButton
          label="Cerrar"
          color="neutral"
          variant="outline"
          @click="cerrar"
        />
        <UButton
          v-if="!resultado"
          label="Procesar"
          color="primary"
          icon="i-lucide-upload"
          :loading="cargando"
          :disabled="!archivo"
          @click="procesar"
        />
      </div>
    </template>
  </UModal>
</template>
