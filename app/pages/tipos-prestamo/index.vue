<script setup lang="ts">
import type { TipoPrestamo, TipoPrestamoCreate } from '#shared/types/tipo_prestamo'
import { useTiposPrestamo } from '~/composables/domain/useTipos'
import { UiEstadoBadge, UButton } from '#components'
import DataTable from '~/components/ui/DataTable.vue'
import ModalDialog from '~/components/ui/ModalDialog.vue'
import ConfirmDialog from '~/components/ui/ConfirmDialog.vue'

definePageMeta({
  middleware: 'admin'
})

const { tipos, loading, error, fetch, crear, actualizar, eliminar } = useTiposPrestamo()

const modalAbierto = ref(false)
const tipoEditando = ref<TipoPrestamo | null>(null)
const confirmarEliminar = ref<TipoPrestamo | null>(null)
const enviando = ref(false)
const formRef = ref<{ submit: () => void } | null>(null)

const toast = useToast()
const formateo = useFormatters()

async function inicializar() {
  await fetch()
}
inicializar()

function abrirNuevo() {
  tipoEditando.value = null
  modalAbierto.value = true
}

function abrirEdicion(tipo: TipoPrestamo) {
  tipoEditando.value = tipo
  modalAbierto.value = true
}

async function guardar(data: TipoPrestamoCreate) {
  enviando.value = true
  try {
    if (tipoEditando.value) {
      await actualizar(tipoEditando.value.id, data)
      toast.add({ title: 'Tipo de préstamo actualizado', color: 'success' })
    } else {
      await crear(data)
      toast.add({ title: 'Tipo de préstamo creado', color: 'success' })
    }
    modalAbierto.value = false
  } catch (e) {
    toast.add({ title: (e as { detail: string }).detail || 'No se pudo guardar', color: 'error' })
  } finally {
    enviando.value = false
  }
}

async function confirmarEliminarTipo() {
  if (!confirmarEliminar.value) return
  enviando.value = true
  try {
    await eliminar(confirmarEliminar.value.id)
    toast.add({ title: 'Tipo de préstamo eliminado', color: 'success' })
    confirmarEliminar.value = null
  } catch (e) {
    toast.add({ title: (e as { detail: string }).detail || 'No se pudo eliminar', color: 'error' })
  } finally {
    enviando.value = false
  }
}

const columns = [
  { accessorKey: 'id', header: 'ID', sorted: true },
  { accessorKey: 'nombre', header: 'Nombre', sorted: true },
  {
    header: 'Interés mensual',
    cell: (row: Record<string, unknown>) => formateo.formatoPorcentaje(Number(row.interes_mensual))
  },
  { accessorKey: 'max_cuotas', header: 'Máx. cuotas' },
  {
    header: 'Estado',
    component: UiEstadoBadge,
    componentProps: (row: Record<string, unknown>) => ({ entidad: 'tipoPrestamo', estado: String(row.estado ?? '') })
  },
  {
    header: 'Acciones',
    component: UButton,
    componentProps: (row: Record<string, unknown>) => ({
      icon: 'i-lucide-pencil',
      color: 'neutral',
      variant: 'ghost',
      label: 'Editar',
      onClick: () => abrirEdicion(row as unknown as TipoPrestamo)
    })
  }
]
</script>

<template>
  <div class="p-6">
    <DataTable
      titulo="Tipos de Préstamo"
      :data="tipos as Record<string, unknown>[]"
      :columns="columns"
      :loading="loading"
      :error="error"
      :filtros="[{ columna: 'estado', placeholder: 'Estado', datos: [{ label: 'Activo', value: 'activo' }, { label: 'Inactivo', value: 'inactivo' }] }]"
      :agregar="abrirNuevo"
      :llamar-datos="fetch"
      exportar-nombre="tipos-prestamo"
      @retry="fetch"
    />

    <UModal
      :open="modalAbierto"
      :titulo="tipoEditando ? 'Editar tipo de préstamo' : 'Nuevo tipo de préstamo'"
      @update:open="modalAbierto = $event"
    >
      <template #title>
        <slot name="title">
          {{ tipoEditando ? 'Editar tipo de préstamo' : 'Nuevo tipo de préstamo' }}
        </slot>
      </template>
      <template #body>
        <TiposTipoPrestamoForm
          ref="formRef"
          :tipo="tipoEditando"
          @guardar="guardar"
        />
      </template>
      <template #footer>
        <div class="flex justify-end gap-2 pt-2">
          <UButton
            label="Cancelar"
            color="neutral"
            variant="outline"
            :disabled="enviando"
            @click="() => { modalAbierto = false }"
          />
          <UButton
            label="Guardar"
            color="primary"
            icon="i-lucide-save"
            :loading="enviando"
            @click="formRef?.submit()"
          />
        </div>
      </template>
    </UModal>

    <ConfirmDialog
      :open="!!confirmarEliminar"
      titulo="Eliminar tipo de préstamo"
      :mensaje="`¿Eliminar ${confirmarEliminar?.nombre ?? ''}? El tipo se desactivará.`"
      :loading="enviando"
      @update:open="(v: boolean) => !v && (confirmarEliminar = null)"
      @confirmar="confirmarEliminarTipo"
    />
  </div>
</template>
