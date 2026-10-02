<script setup lang="ts">
import { z } from 'zod'
import EmptyState from '~/components/ui/EmptyState.vue'
import { changePassword } from '~/services/api/auth'
import { obtenerLog, exportarLog } from '~/services/db/audit'
import { formatoFecha } from '~/utils/fecha'

definePageMeta({
  middleware: 'auth'
})

const auth = useAuthStore()
const toast = useToast()
const { isSupported: pushSoportado, isSubscribed: pushActivo, loading: pushCargando, togglePush } = usePushNotifications()

const logs = ref<Awaited<ReturnType<typeof obtenerLog>>>([])
const loadingLogs = ref(false)
const filtroEntidad = ref('all')

async function cargarLogs() {
  loadingLogs.value = true
  try {
    logs.value = await obtenerLog({
      entidad: filtroEntidad.value || undefined,
      limit: 100
    })
  } finally {
    loadingLogs.value = false
  }
}

async function exportar() {
  const data = await exportarLog()
  const blob = new Blob([data], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'auditoria-loansoft.json'
  a.click()
  URL.revokeObjectURL(url)
  toast.add({ title: 'Auditoría exportada', color: 'success' })
}

cargarLogs()

const passwordActual = ref('')
const passwordNuevo = ref('')
const passwordConfirmar = ref('')
const enviandoPassword = ref(false)
const erroresPassword = ref<Record<string, string>>({})

const schemaPassword = z.object({
  password_actual: z.string().min(1, 'La contraseña actual es requerida'),
  password_nuevo: z.string().min(6, 'Mínimo 6 caracteres'),
  password_confirmar: z.string()
}).refine(data => data.password_nuevo === data.password_confirmar, {
  message: 'Las contraseñas no coinciden',
  path: ['password_confirmar']
})

async function cambiarPassword() {
  erroresPassword.value = {}
  const resultado = schemaPassword.safeParse({
    password_actual: passwordActual.value,
    password_nuevo: passwordNuevo.value,
    password_confirmar: passwordConfirmar.value
  })

  if (!resultado.success) {
    for (const issue of resultado.error.issues) {
      erroresPassword.value[issue.path[0] as string] = issue.message
    }
    return
  }

  enviandoPassword.value = true
  try {
    await changePassword({
      password_actual: passwordActual.value,
      password_nuevo: passwordNuevo.value
    })
    toast.add({ title: 'Contraseña cambiada exitosamente', color: 'success' })
    passwordActual.value = ''
    passwordNuevo.value = ''
    passwordConfirmar.value = ''
  } catch (e) {
    toast.add({ title: (e as { detail: string }).detail || 'No se pudo cambiar la contraseña', color: 'error' })
  } finally {
    enviandoPassword.value = false
  }
}

async function toggleNotificaciones(on: boolean) {
  await togglePush(on)
  toast.add({
    title: on ? 'Notificaciones activadas' : 'Notificaciones desactivadas',
    color: on ? 'success' : 'info'
  })
}
</script>

<template>
  <div class="p-6 space-y-6">
    <UiPageHeader
      titulo="Perfil"
      descripcion="Gestiona tu cuenta y contraseña."
      icono="i-lucide-user"
    />

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <UCard>
        <template #header>
          <h3 class="font-bold">
            Datos del usuario
          </h3>
        </template>
        <div class="space-y-3">
          <div class="flex items-center gap-3">
            <span class="text-sm text-gray-500 w-24">Nombre:</span>
            <span class="font-medium">{{ auth.user?.nombre ?? '—' }}</span>
          </div>
          <div class="flex items-center gap-3">
            <span class="text-sm text-gray-500 w-24">Email:</span>
            <span class="font-medium">{{ auth.user?.email ?? '—' }}</span>
          </div>
          <div class="flex items-center gap-3">
            <span class="text-sm text-gray-500 w-24">Rol:</span>
            <UiEstadoBadge
              :entidad="'usuario'"
              :estado="auth.user?.rol ?? 'usuario'"
            />
          </div>
        </div>
      </UCard>

      <UCard>
        <template #header>
          <h3 class="font-bold">
            Notificaciones push
          </h3>
        </template>
        <div class="space-y-4">
          <p class="text-sm text-gray-500">
            Recibe recordatorios de vencimiento de cuotas y alertas importantes del sistema.
          </p>
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <UIcon
                :name="pushActivo ? 'i-lucide-bell-ring' : 'i-lucide-bell-off'"
                class="text-lg"
                :class="pushActivo ? 'text-green-500' : 'text-gray-400'"
              />
              <span class="text-sm font-medium">
                {{ pushActivo ? 'Activadas' : 'Desactivadas' }}
              </span>
            </div>
            <USwitch
              :model-value="pushActivo"
              :disabled="!pushSoportado || pushCargando"
              @update:model-value="toggleNotificaciones"
            />
          </div>
          <p
            v-if="!pushSoportado"
            class="text-xs text-amber-600 dark:text-amber-400"
          >
            Tu navegador no soporta notificaciones push.
          </p>
        </div>
      </UCard>

      <UCard>
        <template #header>
          <h3 class="font-bold">
            Cambiar contraseña
          </h3>
        </template>
        <form
          class="space-y-4"
          @submit.prevent="cambiarPassword"
        >
          <UFormField
            label="Contraseña actual"
            :error="erroresPassword.password_actual"
          >
            <UInput
              v-model="passwordActual"
              class="w-full"
              type="password"
              placeholder="Tu contraseña actual"
            />
          </UFormField>
          <UFormField
            label="Nueva contraseña"
            :error="erroresPassword.password_nuevo"
          >
            <UInput
              v-model="passwordNuevo"
              class="w-full"
              type="password"
              placeholder="Mínimo 6 caracteres"
            />
          </UFormField>
          <UFormField
            label="Confirmar contraseña"
            :error="erroresPassword.password_confirmar"
          >
            <UInput
              v-model="passwordConfirmar"
              class="w-full"
              type="password"
              placeholder="Repite la nueva contraseña"
            />
          </UFormField>
          <div class="flex justify-end">
            <UButton
              label="Cambiar contraseña"
              color="primary"
              icon="i-lucide-lock"
              :loading="enviandoPassword"
              @click="cambiarPassword"
            />
          </div>
        </form>
      </UCard>
    </div>

    <UCard>
      <template #header>
        <div class="flex justify-between items-center">
          <h3 class="font-bold">
            Auditoría local
          </h3>
          <div class="flex gap-2">
            <USelect
              v-model="filtroEntidad"
              :items="[
                { label: 'Todas', value: 'all' },
                { label: 'Préstamo', value: 'prestamo' },
                { label: 'Pago', value: 'pago' },
                { label: 'Cliente', value: 'cliente' },
                { label: 'Capital', value: 'capital' },
                { label: 'Auth', value: 'auth' }
              ]"
              @update:model-value="cargarLogs"
            />
            <UButton
              label="Exportar JSON"
              icon="i-lucide-download"
              color="primary"
              variant="outline"
              size="sm"
              @click="exportar"
            />
          </div>
        </div>
      </template>
      <EmptyState
        v-if="!logs.length && !loadingLogs"
        icono="i-lucide-file-text"
        titulo="Sin registros"
        descripcion="No hay eventos de auditoría registrados."
      />
      <div
        v-else
        class="space-y-2 max-h-[50vh] overflow-y-auto"
      >
        <div
          v-for="log in logs"
          :key="log.id"
          class="flex items-start gap-3 p-2 rounded border border-gray-100 dark:border-gray-800 text-sm"
        >
          <span class="text-xs text-gray-400 shrink-0 w-36">{{ formatoFecha(log.timestamp) }}</span>
          <span class="text-xs px-2 py-0.5 rounded-full bg-gray-100 dark:bg-gray-800">{{ log.accion }}</span>
          <span class="text-gray-600 dark:text-gray-300">{{ log.entidad }} #{{ log.entidadId ?? '—' }}</span>
          <span
            v-if="log.usuario"
            class="text-gray-400 ml-auto shrink-0"
          >{{ log.usuario }}</span>
        </div>
      </div>
    </UCard>
  </div>
</template>
