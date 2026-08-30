<script setup lang="ts">
import { computed, h, ref } from 'vue'
import type { Component } from 'vue'
import { UButton } from '#components'

export interface DataTableColumn {
  accessorKey?: string
  header: string
  sorted?: boolean
  cell?: (row: Record<string, unknown>) => unknown
  component?: Component
  componentProps?: (row: Record<string, unknown>) => Record<string, unknown>
}

export interface DataTableFiltro {
  columna: string
  placeholder: string
  datos?: { label: string, value: string }[]
}

const props = withDefaults(defineProps<{
  titulo: string
  data: Record<string, unknown>[]
  columns: DataTableColumn[]
  filtros?: DataTableFiltro[]
  filtroGlobal?: (row: Record<string, unknown>, termino: string) => boolean
  loading?: boolean
  error?: string | null
  agregar?: () => void
  llamarDatos?: () => void
  exportarNombre?: string
}>(), {
  filtros: () => [],
  loading: false,
  error: null,
  exportarNombre: 'exportar'
})

const emit = defineEmits<{
  retry: []
}>()

const busqueda = ref('')
const filtrosValor = ref<Record<string, string>>({})
const columnaOrden = ref<{ key: string, ascendente: boolean } | null>(null)
const paginaActual = ref(1)
const itemsPorPagina = ref(10)
const mostrarFiltros = ref(false)

const filtrosActivos = computed(() => {
  const activos: string[] = []
  if (busqueda.value.trim()) activos.push('búsqueda')
  for (const f of props.filtros) {
    if (filtrosValor.value[f.columna]) activos.push(f.placeholder)
  }
  if (columnaOrden.value) activos.push('orden')
  return activos
})

const datosFiltrados = computed(() => {
  let datos = [...props.data]

  if (busqueda.value.trim()) {
    const termino = busqueda.value.trim().toLowerCase()
    datos = datos.filter((row) => {
      if (props.filtroGlobal) return props.filtroGlobal(row, termino)
      return Object.values(row).some(v => String(v ?? '').toLowerCase().includes(termino))
    })
  }

  for (const f of props.filtros) {
    const valor = filtrosValor.value[f.columna]
    if (!valor || valor === 'all') continue
    datos = datos.filter(row => String(row[f.columna] ?? '') === valor)
  }

  if (columnaOrden.value) {
    const { key, ascendente } = columnaOrden.value
    datos = [...datos].sort((a, b) => {
      const av = a[key]
      const bv = b[key]
      if (typeof av === 'number' && typeof bv === 'number') return ascendente ? av - bv : bv - av
      return String(av ?? '').localeCompare(String(bv ?? ''), 'es') * (ascendente ? 1 : -1)
    })
  }

  return datos
})

const totalPaginas = computed(() => Math.max(1, Math.ceil(datosFiltrados.value.length / itemsPorPagina.value)))

const datosPaginados = computed(() => {
  const inicio = (paginaActual.value - 1) * itemsPorPagina.value
  return datosFiltrados.value.slice(inicio, inicio + itemsPorPagina.value)
})

watch([datosFiltrados, itemsPorPagina], () => {
  if (paginaActual.value > totalPaginas.value) paginaActual.value = totalPaginas.value
})

function ordenar(key: string) {
  if (columnaOrden.value?.key === key) {
    columnaOrden.value = { key, ascendente: !columnaOrden.value.ascendente }
  } else {
    columnaOrden.value = { key, ascendente: true }
  }
}

function borrarFiltros() {
  busqueda.value = ''
  filtrosValor.value = {}
  columnaOrden.value = null
  paginaActual.value = 1
}

function cambiarItemsPorPagina(valor: string) {
  itemsPorPagina.value = Number(valor)
  paginaActual.value = 1
}

function exportarCSV() {
  if (!datosFiltrados.value.length) return
  const headers = props.columns.filter(c => c.accessorKey).map(c => c.header)
  const filas = datosFiltrados.value.map((row) => {
    const obj: Record<string, unknown> = {}
    for (const col of props.columns) {
      if (col.accessorKey) obj[col.header] = row[col.accessorKey]
    }
    return obj
  })
  const escapar = (v: unknown) => {
    const s = String(v ?? '')
    return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s
  }
  const lineas = [headers.join(','), ...filas.map(row => headers.map(h => escapar(row[h])).join(','))]
  const blob = new Blob(['\uFEFF' + lineas.join('\n')], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${props.exportarNombre}.csv`
  a.click()
  URL.revokeObjectURL(url)
}

function valorCelda(row: Record<string, unknown>, col: DataTableColumn): unknown {
  if (col.cell) return col.cell(row)
  if (col.accessorKey) return row[col.accessorKey]
  return ''
}

const columnasTabla = computed(() =>
  props.columns.map(col => ({
    id: col.accessorKey ?? col.header,
    ...(col.accessorKey ? { accessorKey: col.accessorKey } : {}),
    header: col.sorted
      ? ({ column }: { column: { toggleSorting: () => void, getIsSorted: () => string | boolean } }) =>
          h(UButton, {
            size: 'xs',
            variant: 'ghost',
            color: 'neutral',
            label: col.header,
            icon: column.getIsSorted() === 'asc' ? 'i-lucide-arrow-up' : column.getIsSorted() === 'desc' ? 'i-lucide-arrow-down' : 'i-lucide-arrow-up-down',
            class: '-mx-2',
            onClick: () => {
              column.toggleSorting()
              if (col.accessorKey) ordenar(col.accessorKey)
            }
          })
      : col.header,
    cell: ({ row }: { row: { original: Record<string, unknown> } }) => {
      if (col.component) {
        return h(col.component, col.componentProps?.(row.original) ?? {})
      }
      return valorCelda(row.original, col)
    }
  }))
)
</script>

<template>
  <div>
    <UCard class="mb-3">
      <template #header>
        <div class="flex justify-between items-center gap-3">
          <h3 class="font-bold text-lg truncate">
            {{ titulo }}
          </h3>
          <div class="flex flex-wrap justify-end gap-2">
            <UButton
              v-if="datosFiltrados.length"
              variant="outline"
              color="neutral"
              icon="i-lucide-download"
              size="sm"
              @click="exportarCSV"
            >
              Exportar
            </UButton>
            <UButton
              v-if="filtros.length"
              variant="outline"
              color="neutral"
              icon="i-lucide-list-filter"
              size="sm"
              @click="mostrarFiltros = !mostrarFiltros"
            >
              Filtrar
            </UButton>
            <UButton
              v-if="llamarDatos"
              icon="i-lucide-cloud-sync"
              color="neutral"
              variant="ghost"
              size="sm"
              @click="llamarDatos"
            />
            <UButton
              v-if="agregar"
              color="primary"
              icon="i-lucide-plus"
              size="sm"
              @click="agregar"
            >
              Agregar
            </UButton>
          </div>
        </div>

        <div
          v-if="mostrarFiltros"
          class="mt-4 space-y-3"
        >
          <UInput
            v-model="busqueda"
            placeholder="Buscar..."
            icon="i-lucide-search"
          />
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            <USelect
              v-for="f in filtros"
              :key="f.columna"
              v-model="filtrosValor[f.columna]"
              :placeholder="f.placeholder"
              :items="[{ label: 'Todos', value: 'all' }, ...(f.datos ?? [])]"
            />
          </div>
          <div
            v-if="filtrosActivos.length"
            class="flex flex-wrap items-center gap-2"
          >
            <span class="text-xs px-2 py-1 rounded-full bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300">
              Filtros activos
            </span>
            <UButton
              color="error"
              variant="ghost"
              size="xs"
              icon="i-lucide-x"
              @click="borrarFiltros"
            >
              Limpiar
            </UButton>
          </div>
        </div>
      </template>
    </UCard>

    <UCard>
      <div v-if="loading">
        <div class="space-y-3 py-4">
          <USkeleton
            v-for="i in 5"
            :key="i"
            class="h-10 w-full"
          />
        </div>
      </div>

      <div
        v-else-if="error"
        class="flex flex-col items-center gap-3 py-10"
      >
        <UIcon
          name="i-lucide-alert-triangle"
          class="text-3xl text-error"
        />
        <p class="text-sm text-gray-500">
          {{ error }}
        </p>
        <UButton
          color="primary"
          variant="outline"
          size="sm"
          icon="i-lucide-refresh-cw"
          @click="emit('retry')"
        >
          Reintentar
        </UButton>
      </div>

      <div v-else-if="!datosFiltrados.length">
        <EmptyState
          titulo="Sin resultados"
          descripcion="No hay datos que coincidan con la búsqueda."
        />
      </div>

      <UTable
        v-else
        sticky
        :data="datosPaginados"
        :columns="columnasTabla"
        class="max-h-[62vh]"
      />

      <div class="flex flex-wrap items-center justify-between gap-3 mt-3">
        <UPagination
          v-model:page="paginaActual"
          :total="datosFiltrados.length"
          :items-per-page="itemsPorPagina"
          :max-pages="5"
        />
        <div class="flex items-center gap-2 text-sm text-gray-500">
          <span>{{ datosFiltrados.length }} registros</span>
          <select
            class="bg-transparent border border-gray-300 dark:border-gray-600 rounded-md px-2 py-1 text-sm"
            :value="itemsPorPagina"
            @change="cambiarItemsPorPagina(($event.target as HTMLSelectElement).value)"
          >
            <option value="10">
              10
            </option>
            <option value="20">
              20
            </option>
            <option value="50">
              50
            </option>
          </select>
        </div>
      </div>
    </UCard>
  </div>
</template>
