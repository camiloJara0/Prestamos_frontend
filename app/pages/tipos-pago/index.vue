<script setup lang="ts">
import type { TipoPago, TipoPagoCreate } from '#shared/types/tipo_pago'
import { useTiposPago } from '~/composables/domain/useTipos'
import { UButton } from '#components'
import DataTable from '~/components/ui/DataTable.vue'
import ConfirmDialog from '~/components/ui/ConfirmDialog.vue'
import TipoPagoForm from '~/components/tipos/TipoPagoForm.vue'

definePageMeta({
  middleware: 'admin'
})

const { tipos, loading, error, fetch, crear, actualizar, eliminar } = useTiposPago()

const modalAbierto = ref(false)
const tipoEditando = ref<TipoPago | null>(null)
const confirmarEliminar = ref<TipoPago | null>(null)
const enviando = ref(false)
const formRef = ref<{ submit: () => void } | null>(null)

const toast = useToast()

async function inicializar() {
  await fetch()
}
inicializar()

function abrirNuevo() {
  tipoEditando.value = null
  modalAbierto.value = true
}

function abrirEdicion(tipo: TipoPago) {
  tipoEditando.value = tipo
  modalAbierto.value = true
}

async function guardar(data: TipoPagoCreate) {
  enviando.value = true
  try {
    if (tipoEditando.value) {
      await actualizar(tipoEditando.value.id, data)
      toast.add({ title: 'Tipo de pago actualizado', color: 'success' })
    } else {
      await crear(data)
      toast.add({ title: 'Tipo de pago creado', color: 'success' })
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
    toast.add({ title: 'Tipo de pago eliminado', color: 'success' })
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
  { accessorKey: 'descripcion', header: 'Descripción' },
  {
    header: 'Acciones',
    component: UButton,
    componentProps: (row: Record<string, unknown>) => ({
      icon: 'i-lucide-pencil',
      color: 'neutral',
      variant: 'ghost',
      label: 'Editar',
      onClick: () => abrirEdicion(row as unknown as TipoPago)
    })
  }
]
</script>

<template>
  <div class="p-6">
    <DataTable
      titulo="Tipos de Pago"
      :data="tipos as Record<string, unknown>[]"
      :columns="columns"
      :loading="loading"
      :error="error"
      :agregar="abrirNuevo"
      :llamar-datos="fetch"
      exportar-nombre="tipos-pago"
      @retry="fetch"
    />

    <UModal
      :open="modalAbierto"
      :titulo="tipoEditando ? 'Editar tipo de pago' : 'Nuevo tipo de pago'"
      @update:open="modalAbierto = $event"
    >
      <template #title>
        <slot name="title">
          {{ tipoEditando ? 'Editar tipo de pago' : 'Nuevo tipo de pago' }}
        </slot>
      </template>
      <template #body>
        <TipoPagoForm
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
      titulo="Eliminar tipo de pago"
      :mensaje="`¿Eliminar ${confirmarEliminar?.nombre ?? ''}?`"
      :loading="enviando"
      @update:open="(v: boolean) => !v && (confirmarEliminar = null)"
      @confirmar="confirmarEliminarTipo"
    />
  </div>
</template>
