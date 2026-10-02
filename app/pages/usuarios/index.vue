<script setup lang="ts">
import { z } from 'zod'
import type { Usuario } from '#shared/types/usuario'
import { getUsuarios, createUsuario, updateUsuario, deleteUsuario } from '~/services/api/usuarios'
import type { RespuestaPaginada } from '#shared/types/paginacion'
import ConfirmDialog from '~/components/ui/ConfirmDialog.vue'

definePageMeta({
  middleware: 'admin'
})

const toast = useToast()

const usuarios = ref<RespuestaPaginada<Usuario> | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)
const paginaActual = ref(1)
const porPagina = ref(10)
const modalAbierto = ref(false)
const usuarioEditando = ref<Usuario | null>(null)
const confirmarEliminar = ref<Usuario | null>(null)
const enviando = ref(false)

const buscar = ref('')
const filtroEstado = ref<string | undefined>(undefined)

const schema = z.object({
  nombre: z.string().min(1, 'El nombre es requerido').max(100, 'Máximo 100 caracteres'),
  email: z.string().email('Email inválido'),
  rol: z.enum(['admin', 'usuario']),
  password: z.string().min(6, 'Mínimo 6 caracteres').optional().or(z.literal('')),
  estado: z.enum(['activo', 'inactivo']).default('activo')
})

const form = reactive({
  nombre: '',
  email: '',
  rol: 'usuario' as 'admin' | 'usuario',
  password: '',
  estado: 'activo' as 'activo' | 'inactivo'
})

const errores = ref<Record<string, string>>({})

async function inicializar() {
  await cargarUsuarios()
}

async function cargarUsuarios() {
  loading.value = true
  error.value = null
  try {
    usuarios.value = await getUsuarios(paginaActual.value, porPagina.value)
  } catch (e) {
    error.value = (e as { detail: string }).detail || 'No se pudieron cargar los usuarios'
  } finally {
    loading.value = false
  }
}

inicializar()

const usuariosFiltrados = computed(() => {
  let items = usuarios.value?.items ?? []
  if (buscar.value) {
    const term = buscar.value.toLowerCase()
    items = items.filter(u => u.nombre.toLowerCase().includes(term) || u.email.toLowerCase().includes(term))
  }
  if (filtroEstado.value) {
    items = items.filter(u => u.estado === filtroEstado.value)
  }
  return items
})

function abrirNuevo() {
  usuarioEditando.value = null
  form.nombre = ''
  form.email = ''
  form.rol = 'usuario'
  form.password = ''
  form.estado = 'activo'
  errores.value = {}
  modalAbierto.value = true
}

function abrirEdicion(usuario: Usuario) {
  usuarioEditando.value = usuario
  form.nombre = usuario.nombre
  form.email = usuario.email
  form.rol = usuario.rol
  form.password = ''
  form.estado = usuario.estado
  errores.value = {}
  modalAbierto.value = true
}

function validar() {
  const resultado = schema.safeParse(form)
  if (!resultado.success) {
    errores.value = {}
    for (const issue of resultado.error.issues) {
      errores.value[issue.path[0] as string] = issue.message
    }
    return false
  }
  errores.value = {}
  return true
}

async function guardar() {
  if (!validar()) return
  enviando.value = true
  try {
    if (usuarioEditando.value) {
      const payload: Record<string, unknown> = {
        nombre: form.nombre,
        email: form.email,
        rol: form.rol,
        estado: form.estado
      }
      if (form.password) payload.password = form.password
      await updateUsuario(usuarioEditando.value.id, payload)
      toast.add({ title: 'Usuario actualizado', color: 'success' })
    } else {
      if (!form.password) {
        errores.value.password = 'La contraseña es requerida'
        enviando.value = false
        return
      }
      await createUsuario({
        nombre: form.nombre,
        email: form.email,
        rol: form.rol,
        password: form.password
      })
      toast.add({ title: 'Usuario creado', color: 'success' })
    }
    modalAbierto.value = false
    await cargarUsuarios()
  } catch (e) {
    toast.add({ title: (e as { detail: string }).detail || 'No se pudo guardar', color: 'error' })
  } finally {
    enviando.value = false
  }
}

async function confirmarEliminarUsuario() {
  if (!confirmarEliminar.value) return
  enviando.value = true
  try {
    await deleteUsuario(confirmarEliminar.value.id)
    toast.add({ title: 'Usuario desactivado', color: 'success' })
    confirmarEliminar.value = null
    await cargarUsuarios()
  } catch (e) {
    toast.add({ title: (e as { detail: string }).detail || 'No se pudo desactivar', color: 'error' })
  } finally {
    enviando.value = false
  }
}
</script>

<template>
  <div class="p-6 space-y-6">
    <UiPageHeader
      titulo="Usuarios"
      descripcion="Gestión de usuarios del sistema. Solo administradores."
      icono="i-lucide-user-cog"
    >
      <template #actions>
        <UButton
          label="Nuevo usuario"
          icon="i-lucide-plus"
          color="primary"
          @click="abrirNuevo"
        />
      </template>
    </UiPageHeader>

    <div class="flex flex-wrap gap-3">
      <UInput
        v-model="buscar"
        placeholder="Buscar por nombre o email..."
        icon="i-lucide-search"
        class="w-64"
      />
      <USelect
        v-model="filtroEstado"
        placeholder="Estado"
        class="w-40"
        :items="[{ label: 'Activo', value: 'activo' }, { label: 'Inactivo', value: 'inactivo' }]"
      />
    </div>

    <USkeleton
      v-if="loading"
      class="h-[300px] rounded-lg"
    />

    <UAlert
      v-else-if="error"
      color="error"
      title="Error"
      :description="error"
    >
      <template #footer>
        <UButton
          label="Reintentar"
          color="error"
          variant="outline"
          size="xs"
          @click="cargarUsuarios"
        />
      </template>
    </UAlert>

    <UCard v-else>
      <UTable
        sticky
        :data="usuariosFiltrados"
        :columns="[
          { accessorKey: 'id', header: 'ID' },
          { accessorKey: 'nombre', header: 'Nombre' },
          { accessorKey: 'email', header: 'Email' },
          { accessorKey: 'rol', header: 'Rol', cell: ({ row }) => row.original.rol === 'admin' ? 'Administrador' : 'Usuario' },
          { accessorKey: 'estado', header: 'Estado', cell: ({ row }) => row.original.estado === 'activo' ? 'Activo' : 'Inactivo' },
          { accessorKey: 'acciones', header: 'Acciones' }
        ]"
      >
        <template #acciones-cell="{ row }">
          <div class="flex gap-1">
            <UButton
              icon="i-lucide-pencil"
              color="neutral"
              variant="ghost"
              size="xs"
              @click="abrirEdicion(row.original)"
            />
            <UButton
              v-if="row.original.estado === 'activo'"
              icon="i-lucide-user-x"
              color="error"
              variant="ghost"
              size="xs"
              @click="confirmarEliminar = row.original"
            />
          </div>
        </template>
      </UTable>

      <div
        v-if="usuarios && usuarios.pages > 1"
        class="flex justify-center gap-2 mt-4"
      >
        <UButton
          label="Anterior"
          color="neutral"
          variant="outline"
          :disabled="paginaActual <= 1"
          @click="paginaActual--; cargarUsuarios()"
        />
        <span class="text-sm text-gray-500 py-2">
          Página {{ usuarios.page }} de {{ usuarios.pages }}
        </span>
        <UButton
          label="Siguiente"
          color="neutral"
          variant="outline"
          :disabled="paginaActual >= (usuarios?.pages ?? 1)"
          @click="paginaActual++; cargarUsuarios()"
        />
      </div>

      <EmptyState
        v-if="!loading && !error && usuariosFiltrados.length === 0"
        icono="i-lucide-users"
        titulo="Sin usuarios"
        descripcion="No se encontraron usuarios con los filtros aplicados."
      />
    </UCard>

    <UModal
      :open="modalAbierto"
      @update:open="modalAbierto = $event"
    >
      <template #title>
        {{ usuarioEditando ? 'Editar usuario' : 'Nuevo usuario' }}
      </template>
      <template #body>
        <form
          class="grid grid-cols-1 sm:grid-cols-2 gap-4"
          @submit.prevent="guardar"
        >
          <UFormField
            label="Nombre *"
            :error="errores.nombre"
          >
            <UInput
              v-model="form.nombre"
              class="w-full"
              placeholder="Nombre completo"
            />
          </UFormField>
          <UFormField
            label="Email *"
            :error="errores.email"
          >
            <UInput
              v-model="form.email"
              class="w-full"
              type="email"
              placeholder="correo@ejemplo.com"
            />
          </UFormField>
          <UFormField
            label="Rol *"
          >
            <USelect
              v-model="form.rol"
              class="w-full"
              :items="[{ label: 'Administrador', value: 'admin' }, { label: 'Usuario', value: 'usuario' }]"
            />
          </UFormField>
          <UFormField
            label="Estado"
          >
            <USelect
              v-model="form.estado"
              class="w-full"
              :items="[{ label: 'Activo', value: 'activo' }, { label: 'Inactivo', value: 'inactivo' }]"
            />
          </UFormField>
          <UFormField
            :label="usuarioEditando ? 'Nueva contraseña (vacío = no cambiar)' : 'Contraseña *'"
            :error="errores.password"
            class="sm:col-span-2"
          >
            <UInput
              v-model="form.password"
              class="w-full"
              type="password"
              :placeholder="usuarioEditando ? 'Dejar vacío para no cambiar' : 'Mínimo 6 caracteres'"
            />
          </UFormField>
        </form>
      </template>
      <template #footer>
        <div class="flex justify-end gap-2 pt-2">
          <UButton
            label="Cancelar"
            color="neutral"
            variant="outline"
            :disabled="enviando"
            @click="modalAbierto = false"
          />
          <UButton
            label="Guardar"
            color="primary"
            icon="i-lucide-save"
            :loading="enviando"
            @click="guardar"
          />
        </div>
      </template>
    </UModal>

    <ConfirmDialog
      :open="!!confirmarEliminar"
      titulo="Desactivar usuario"
      :mensaje="`¿Desactivar a ${confirmarEliminar?.nombre ?? ''}? No podrá iniciar sesión.`"
      confirmar-texto="Desactivar"
      :loading="enviando"
      @update:open="(v: boolean) => !v && (confirmarEliminar = null)"
      @confirmar="confirmarEliminarUsuario"
    />
  </div>
</template>
