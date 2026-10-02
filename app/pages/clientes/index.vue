<script setup lang="ts">
import type { Cliente, ClienteCreate } from '#shared/types/clientes'
import { useClientes } from '~/composables/domain/useClientes'
import { UiEstadoBadge, UButton } from '#components'
import DataTable from '~/components/ui/DataTable.vue'
import ClienteForm from '~/components/clientes/ClienteForm.vue'
import ConfirmDialog from '~/components/ui/ConfirmDialog.vue'

definePageMeta({
  middleware: 'auth'
})

const { clientes, loading, error, fetch, recargar, crear, actualizar, eliminar } = useClientes()
const router = useRouter()

const modalAbierto = ref(false)
const clienteEditando = ref<Cliente | null>(null)
const confirmarEliminar = ref<Cliente | null>(null)
const enviando = ref(false)
const errorCampo = ref<Record<string, string>>({})
const formRef = ref<{ submit: () => void } | null>(null)
const toast = useToast()
const busqueda = ref('')

async function inicializar() {
  await fetch()
}
inicializar()

async function buscarEnServidor() {
  await fetch({ page: 1, limit: 100, q: busqueda.value.trim() || undefined })
}

async function limpiarBusqueda() {
  busqueda.value = ''
  await fetch()
}

function verDetalle(clienteId: number) {
  router.push(`/clientes/${clienteId}`)
}

function abrirNuevo() {
  clienteEditando.value = null
  errorCampo.value = {}
  modalAbierto.value = true
}

function abrirEdicion(cliente: Cliente) {
  clienteEditando.value = cliente
  errorCampo.value = {}
  modalAbierto.value = true
}

async function guardar(data: ClienteCreate) {
  enviando.value = true
  errorCampo.value = {}
  try {
    if (clienteEditando.value) {
      await actualizar(clienteEditando.value.id, data)
      toast.add({ title: 'Cliente actualizado', color: 'success' })
    } else {
      await crear(data)
      toast.add({ title: 'Cliente creado', color: 'success' })
    }
    modalAbierto.value = false
  } catch (e) {
    const err = e as { status: number, detail: string }
    if (err.status === 400 && /cedula/i.test(err.detail)) {
      errorCampo.value = { cedula: 'Ya existe un cliente con esa cédula' }
    } else {
      toast.add({ title: err.detail || 'No se pudo guardar el cliente', color: 'error' })
    }
  } finally {
    enviando.value = false
  }
}

async function confirmarEliminarCliente() {
  if (!confirmarEliminar.value) return
  enviando.value = true
  try {
    await eliminar(confirmarEliminar.value.id)
    toast.add({ title: 'Cliente eliminado', color: 'success' })
    confirmarEliminar.value = null
  } catch (e) {
    toast.add({ title: (e as { detail: string }).detail || 'No se pudo eliminar el cliente', color: 'error' })
  } finally {
    enviando.value = false
  }
}

const columns = [
  { accessorKey: 'id', header: 'ID', sorted: true },
  { accessorKey: 'nombre', header: 'Nombre', sorted: true },
  { accessorKey: 'cedula', header: 'Cédula', sorted: true },
  { accessorKey: 'telefono', header: 'Teléfono' },
  { accessorKey: 'direccion', header: 'Dirección' },
  {
    header: 'Estado',
    component: UiEstadoBadge,
    componentProps: (row: Record<string, unknown>) => ({ entidad: 'cliente', estado: String(row.estado ?? '') })
  },
  {
    header: 'Acciones',
    component: UButton,
    componentProps: (row: Record<string, unknown>) => ({
      icon: 'i-lucide-eye',
      color: 'primary',
      variant: 'ghost',
      label: 'Detalle',
      onClick: () => verDetalle(Number(row.id))
    })
  },
  {
    header: 'Editar',
    component: UButton,
    componentProps: (row: Record<string, unknown>) => ({
      icon: 'i-lucide-pencil',
      color: 'neutral',
      variant: 'ghost',
      label: 'Editar',
      onClick: () => abrirEdicion(row as unknown as Cliente)
    })
  }
]

const filtroGlobal = (row: Record<string, unknown>, termino: string) => {
  return String(row.nombre ?? '').toLowerCase().includes(termino)
    || String(row.cedula ?? '').toLowerCase().includes(termino)
}
</script>

<template>
  <div class="p-6 space-y-4">
    <UiPageHeader
      titulo="Gestión de Clientes"
      descripcion="Padrón de clientes con búsqueda por nombre, cédula o teléfono."
      icono="i-lucide-users"
    />

    <UCard>
      <div class="flex flex-wrap items-end gap-3">
        <UFormField
          label="Búsqueda"
          class="flex-1 min-w-64"
        >
          <UInput
            v-model="busqueda"
            placeholder="Nombre, cédula o teléfono"
            icon="i-lucide-search"
            class="w-full"
            @keyup.enter="buscarEnServidor"
          />
        </UFormField>
        <UButton
          color="primary"
          icon="i-lucide-search"
          @click="buscarEnServidor"
        >
          Buscar
        </UButton>
        <UButton
          color="neutral"
          variant="outline"
          icon="i-lucide-x"
          @click="limpiarBusqueda"
        >
          Limpiar
        </UButton>
      </div>
    </UCard>

    <DataTable
      titulo="Gestión de Clientes"
      :data="clientes as Record<string, unknown>[]"
      :columns="columns"
      :loading="loading"
      :error="error"
      :filtros="[{ columna: 'estado', placeholder: 'Estado', datos: [{ label: 'Activo', value: 'activo' }, { label: 'Inactivo', value: 'inactivo' }] }]"
      :filtro-global="filtroGlobal"
      :agregar="abrirNuevo"
      :llamar-datos="recargar"
      exportar-nombre="clientes"
      @retry="recargar"
    />

    <UModal
      :open="modalAbierto"
      :titulo="clienteEditando ? 'Editar cliente' : 'Nuevo cliente'"
      @update:open="modalAbierto = $event"
    >
      <template #title>
        <slot name="title">
          {{ clienteEditando ? 'Editar cliente' : 'Nuevo cliente' }}
        </slot>
      </template>
      <template #body>
        <ClienteForm
          ref="formRef"
          :cliente="clienteEditando"
          :error-campo="errorCampo"
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
      titulo="Eliminar cliente"
      :mensaje="`¿Eliminar a ${confirmarEliminar?.nombre ?? ''}? El cliente se desactivará.`"
      :loading="enviando"
      @update:open="(v: boolean) => !v && (confirmarEliminar = null)"
      @confirmar="confirmarEliminarCliente"
    />
  </div>
</template>
