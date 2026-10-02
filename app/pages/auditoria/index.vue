<script setup lang="ts">
import type { Auditoria } from '#shared/types/auditoria'
import type { RespuestaPaginada } from '#shared/types/paginacion'
import { getAuditoria, getAuditoriaPorOperacion, getAuditoriaPorTabla } from '~/services/api/auditoria'
import { getUsuarios } from '~/services/api/usuarios'
import EmptyState from '~/components/ui/EmptyState.vue'

definePageMeta({
  middleware: 'admin'
})

const formateo = useFormatters()

const registros = ref<RespuestaPaginada<Auditoria> | null>(null)
const nombresUsuarios = ref<Record<number, string>>({})
const loading = ref(false)
const error = ref<string | null>(null)
const paginaActual = ref(1)

const filtroTabla = ref('')
const filtroOperacion = ref('')

const tablasDisponibles = [
  { label: 'Todas las tablas', value: '' },
  { label: 'Préstamos', value: 'prestamos' },
  { label: 'Pagos', value: 'pagos' },
  { label: 'Movimientos de capital', value: 'movimientos_capital' },
  { label: 'Moras', value: 'moras' },
  { label: 'Configuración', value: 'configuracion_sistema' },
  { label: 'Reestructuraciones', value: 'prestamos_reestructuraciones' },
  { label: 'Clientes', value: 'clientes' },
  { label: 'Usuarios', value: 'usuarios' }
]

const operacionesDisponibles = [
  { label: 'Todas las operaciones', value: '' },
  { label: 'Creación (CREATE)', value: 'CREATE' },
  { label: 'Edición (UPDATE)', value: 'UPDATE' },
  { label: 'Eliminación (DELETE)', value: 'DELETE' }
]

async function cargar() {
  loading.value = true
  error.value = null
  try {
    if (filtroTabla.value) {
      registros.value = await getAuditoriaPorTabla(filtroTabla.value, paginaActual.value, 25)
    } else if (filtroOperacion.value) {
      registros.value = await getAuditoriaPorOperacion(filtroOperacion.value, paginaActual.value, 25)
    } else {
      registros.value = await getAuditoria(paginaActual.value, 25)
    }
  } catch {
    error.value = 'No se pudo cargar la auditoría.'
  } finally {
    loading.value = false
  }
}

async function cargarUsuarios() {
  try {
    const respuesta = await getUsuarios(1, 100)
    const mapa: Record<number, string> = {}
    for (const u of respuesta.items) mapa[u.id] = u.nombre
    nombresUsuarios.value = mapa
  } catch {
    nombresUsuarios.value = {}
  }
}

async function inicializar() {
  await Promise.all([cargar(), cargarUsuarios()])
}
inicializar()

function aplicarFiltros() {
  paginaActual.value = 1
  cargar()
}

function limpiarFiltros() {
  filtroTabla.value = ''
  filtroOperacion.value = ''
  aplicarFiltros()
}

const filas = computed(() => (registros.value?.items ?? []).map(a => ({
  fecha: formateo.formatoFecha(a.fecha),
  usuario: a.usuario_id != null ? (nombresUsuarios.value[a.usuario_id] ?? `#${a.usuario_id}`) : 'Sistema',
  tabla: a.tabla_afectada,
  operacion: a.tipo_operacion,
  registro: a.registro_id != null ? `#${a.registro_id}` : '—',
  ip: a.ip_address ?? '—',
  descripcion: a.descripcion ?? '—'
})))

const columns = [
  { accessorKey: 'fecha', header: 'Fecha' },
  { accessorKey: 'usuario', header: 'Usuario' },
  { accessorKey: 'tabla', header: 'Tabla' },
  { accessorKey: 'operacion', header: 'Operación' },
  { accessorKey: 'registro', header: 'Registro' },
  { accessorKey: 'ip', header: 'IP' },
  { accessorKey: 'descripcion', header: 'Descripción' }
]
</script>

<template>
  <div class="p-6 space-y-4">
    <UiPageHeader
      titulo="Auditoría"
      descripcion="Quién realizó qué operación sobre préstamos, pagos, capital y moras."
      icono="i-lucide-shield-check"
    />

    <UAlert
      icon="i-lucide-info"
      color="info"
      title="Trazabilidad completa"
      description="Cada operación sensible registra usuario, tabla, tipo de operación, valores anteriores y nuevos, dirección IP y marca de tiempo."
    />

    <UCard>
      <div class="flex flex-wrap items-end gap-3">
        <UFormField label="Tabla">
          <USelect
            v-model="filtroTabla"
            :items="tablasDisponibles"
            class="w-56"
          />
        </UFormField>
        <UFormField label="Operación">
          <USelect
            v-model="filtroOperacion"
            :items="operacionesDisponibles"
            class="w-56"
            :disabled="!!filtroTabla"
          />
        </UFormField>
        <UButton
          color="primary"
          icon="i-lucide-search"
          :loading="loading"
          @click="aplicarFiltros"
        >
          Filtrar
        </UButton>
        <UButton
          color="neutral"
          variant="outline"
          icon="i-lucide-x"
          @click="limpiarFiltros"
        >
          Limpiar
        </UButton>
      </div>
    </UCard>

    <UCard>
      <UAlert
        v-if="error"
        icon="i-lucide-alert-triangle"
        color="error"
        :title="error"
        :actions="[{ label: 'Reintentar', color: 'primary', variant: 'outline', onClick: cargar }]"
      />

      <EmptyState
        v-else-if="!loading && !registros?.items?.length"
        icono="i-lucide-shield-check"
        titulo="Sin registros de auditoría"
        descripcion="Aún no se han registrado operaciones sensibles."
      />

      <USkeleton
        v-else-if="loading"
        class="h-64 rounded-lg"
      />

      <UTable
        v-else
        sticky
        :data="filas"
        :columns="columns"
        class="max-h-[55vh]"
      />

      <div
        v-if="registros && registros.pages > 1"
        class="flex items-center justify-between pt-4"
      >
        <span class="text-sm text-gray-500">
          {{ registros.total }} eventos · Página {{ registros.page }} de {{ registros.pages }}
        </span>
        <div class="flex gap-2">
          <UButton
            color="neutral"
            variant="outline"
            icon="i-lucide-chevron-left"
            label="Anterior"
            :disabled="loading || registros.page <= 1"
            @click="paginaActual--; cargar()"
          />
          <UButton
            color="neutral"
            variant="outline"
            label="Siguiente"
            icon-right="i-lucide-chevron-right"
            :disabled="loading || registros.page >= registros.pages"
            @click="paginaActual++; cargar()"
          />
        </div>
      </div>
    </UCard>
  </div>
</template>
