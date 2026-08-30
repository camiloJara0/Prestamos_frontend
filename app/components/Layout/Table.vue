<script setup>
import { ref, h } from 'vue'
import { useOrdenamiento } from '~/composables/table/useDatosOrdenados'
import { usePaginacion } from '~/composables/table/usePaginacion'

const mostrarFiltros = ref(false)
const mostrarFiltrosAvanzados = ref(false)
const varView = useVarView()
const excelRef = ref(null)

const props = defineProps({
  Propiedades: {
    type: [Object, Array],
    requiered: true,
    default: () => ({})
  }
})

const data = ref(props.Propiedades.data)
// Ordenamiento de datos
const {
  busqueda,
  filtros,
  filtrosConOpciones,
  sortedItems,
  datosOrdenados,
  columnaOrden,
  _menorAMayor,
  borrarFiltros
} = useOrdenamiento(data.value || ref([]), props.Propiedades.filtros || [], props.Propiedades.noFiltrar || [])

// Paginador
const {
  paginaActual,
  itemsPorPagina,
  _totalPaginas,
  ultimaPagina,
  cambiarItemsPorPagina,
  _siguientePagina,
  _paginaAnterior,
  _irAPagina,
  datosPaginados
} = usePaginacion(datosOrdenados)

const _items = ref([
  {
    label: 'Descargar',
    icon: 'i-lucide-file',
    onSelect: () => {
      // Dispara el click directamente sobre el enlace generado
      excelRef.value?.$el.click()
    }
  },
  {
    label: 'Configurar',
    icon: 'i-lucide-settings',
    onSelect: () => {
      varView.showDatosExcel = true
    }
  }
])

const columns = props.Propiedades.columns.map((col) => {
  if (col.sorted) {
    return {
      ...col,
      header: ({ _column }) =>
        h(UButton, {
          color: 'neutral',
          variant: 'ghost',
          label: col.header || col.accessorKey,
          icon: 'i-lucide-arrow-up-down',
          class: '-mx-2.5',
          onClick: () => sortedItems(col.accessorKey)
        })
    }
  }
  return col
})
</script>

<template>
  <!-- Titulo, Acciones y Filtros -->
  <UCard class="mb-3">
    <template #header>
      <div class="flex justify-between items-center">
        <h3 class="font-bold text-lg md:w-fit w-1/2 pr-1">
          {{ props.Propiedades.titulo }}
        </h3>
        <div class="flex flex-wrap justify-end gap-2">
          <UButton
            v-for="button in props.Propiedades.buttons"
            :key="button.texto || button.icon"
            :variant="button.variant"
            :color="button.color"
            loading-auto
            :trailing-icon="button.icon"
            size="md"
            @click="button.accion"
          >
            <span class="hidden md:block">{{ button.texto }}</span>
          </UButton>

          <!-- <client-only v-if="Propiedades.excel">
                        <UDropdownMenu :items="items">
                            <UButton label="Open" variant="subtle" color="secondary" trailing-icon="lucide-table"
                                size="md">
                                <span class="hidden md:block">Exportar</span>
                            </UButton>
                        </UDropdownMenu>

                        <div>
                            <download-excel ref="excelRef"
                                :data="Array.isArray(datosOrdenados) ? datosOrdenados : props.Propiedades.data"
                                :name="props.Propiedades.titulo" type="xlsx" style="display: none;">
                                .
                            </download-excel>
                        </div>

                    </client-only> -->

          <UButton
            variant="solid"
            color="primary"
            trailing-icon="lucide-list-filter"
            size="md"
            @click="() => { mostrarFiltros = !mostrarFiltros }"
          >
            <span class="hidden md:block">Filtrar</span>
          </UButton>
          <UButton
            v-if="props.Propiedades.agregar"
            variant="solid"
            color="primary"
            trailing-icon="lucide-plus"
            size="md"
            @click="props.Propiedades.agregar"
          >
            <span class="hidden md:block">Agregar</span>
          </UButton>
          <UButton
            v-if="props.Propiedades.llamadatos"
            icon="i-lucide-cloud-sync"
            color="primary"
            variant="ghost"
            size="md"
            @click="props.Propiedades.llamadatos?.(true)"
          />
        </div>
      </div>
      <div
        v-if="mostrarFiltros"
        class="w-full"
      >
        <div class="w-full py-4">
          <USeparator />
        </div>
        <div class="flex justify-between items-center mb-4">
          <div class="flex items-center gap-2">
            <i class="fa-solid fa-filter text-gray-400" />
            <p class="text-sm font-medium text-gray-600 dark:text-gray-300">
              Filtros de la tabla
              <span
                v-if="busqueda !== '' || Object.values(filtros).some(v => v !== '') || columnaOrden"
                class="text-xs px-2 py-1 rounded-full bg-blue-100 text-blue-600 dark:bg-blue-900 dark:text-blue-300"
              >
                Filtros activos
              </span>
            </p>
          </div>

          <div class="flex gap-2">
            <UButton
              v-if="filtrosConOpciones.length > 3"
              :color="mostrarFiltrosAvanzados ? 'bg-blue-800 dark:bg-blue-700' : 'bg-gray-800 text-gray-700 dark:bg-gray-700 dark:text-gray-200'"
              tooltip="Filtros Avanzados"
              @click="mostrarFiltrosAvanzados = !mostrarFiltrosAvanzados"
            >
              <i class="fa-solid fa-sliders" />
            </UButton>
            <UButton
              v-if="busqueda !== '' || Object.values(filtros).some(v => v !== '') || columnaOrden"
              color="dark:text-gray-200 dark:bg-red-600 text-gray-700 bg-red-400"
              tooltip="Limpiar filtros"
              tooltip-position="top"
              @click="borrarFiltros"
            >
              <i class="fa-solid fa-xmark" />
            </UButton>
          </div>
        </div>

        <div
          class="flex flex-wrap items-end justify-between gap-3"
        >
          <UInput
            v-model="busqueda"
            placeholder="Buscar dato en la Tabla..."
            icon="lucide-search"
            variant="outline"
            size="lg"
            class="md:w-90 w-full"
          />

          <div class="md:flex flex-wrap justify-end gap-3 w-full md:w-fit grid grid-cols-2">
            <USelect
              v-for="(filtro, key) in filtrosConOpciones.slice(0, 3)"
              :key="key"
              v-model="filtros[filtro.columna]"
              :placeholder="filtro.placeholder"
              :items="[{ label: 'Todos', value: 'all' }, ...filtro.datos]"
              class="md:w-45 w-full"
            />
          </div>
        </div>
        <div
          v-if="mostrarFiltrosAvanzados"
          class="mt-4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 justify-items-end"
        >
          <USelect
            v-for="(filtro, key) in filtrosConOpciones.slice(3)"
            :key="key"
            v-model="filtros[filtro.columna]"
            :placeholder="filtro.placeholder"
            :items="[{ label: 'Todos', value: 'all' }, ...filtro.datos]"
            class="w-full"
          />
        </div>
      </div>
    </template>
  </UCard>
  <!-- Tabla -->
  <UTable
    sticky
    :loading="!props.Propiedades.data || varView.cargando || varView.actualizando"
    loading-color="primary"
    loading-animation="carousel"
    :data="datosPaginados"
    :columns="columns"
    class="flex-1 max-h-[62vh]"
  />
  <!-- Paginador -->
  <div class="flex justify-between mt-3">
    <UPagination
      v-model:page="paginaActual"
      active-color="primary"
      active-variant="subtle"
      :sibling-count="1"
      :total="datosOrdenados.length"
      :items-per-page="itemsPorPagina"
    />
    <p class="text-sm text-gray-500 md:flex gap-1 hidden items-center">
      Mostrando
      <span class="text-gray-500">{{ ultimaPagina - itemsPorPagina + 1 }} al {{ ultimaPagina }}</span>
      <span class="text-gray-500">de {{ datosOrdenados.length }}</span>
      <select
        name="numRegistros"
        class="ml-3 text-sm bg-transparent border border-gray-300 dark:border-gray-600 rounded-md px-2 py-1 text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition"
        @change="cambiarItemsPorPagina($event.target.value)"
      >
        <option
          value="10"
          selected
        >
          10
        </option>
        <option value="20">
          20
        </option>
        <option value="50">
          50
        </option>
      </select>
    </p>
  </div>
</template>
