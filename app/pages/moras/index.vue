<script setup lang="ts">
import { z } from 'zod'
import type { Mora, MoraCreateUpdate } from '#shared/types/mora'
import { useMoras } from '~/composables/domain/useMoras'
import { UiEstadoBadge, UButton } from '#components'

definePageMeta({
  middleware: 'auth'
})

const { moras, loading, error, fetch: fetchMoras, fetchByPrestamo, actualizar, eliminar, procesar } = useMoras()

const toast = useToast()
const formateo = useFormatters()

const filtroPrestamo = ref('')
const modalEdicion = ref(false)
const moraEditando = ref<Mora | null>(null)
const confirmarEliminar = ref<Mora | null>(null)
const enviando = ref(false)
const procesando = ref(false)

const schema = z.object({
  prestamo_id: z.number().positive(),
  cuota_id: z.number().positive(),
  fecha: z.string().min(1),
  valor: z.number().min(0),
  estado: z.string().min(1)
})

const formEdicion = reactive<MoraCreateUpdate>({
  prestamo_id: 0,
  cuota_id: 0,
  fecha: '',
  valor: 0,
  estado: 'pendiente'
})

async function inicializar() {
  await fetchMoras()
}
inicializar()

async function aplicarFiltro() {
  const id = Number(filtroPrestamo.value)
  if (id > 0) {
    await fetchByPrestamo(id)
  } else {
    await fetchMoras()
  }
}

async function procesarMorasAhora() {
  procesando.value = true
  try {
    const resultado = await procesar()
    toast.add({
      title: `Moras procesadas: ${resultado.moras_actualizadas.length} actualizadas`,
      color: 'success'
    })
  } catch (e) {
    toast.add({ title: (e as { detail: string }).detail || 'No se pudieron procesar las moras', color: 'error' })
  } finally {
    procesando.value = false
  }
}

function abrirEdicion(mora: Mora) {
  moraEditando.value = mora
  formEdicion.prestamo_id = mora.prestamo_id
  formEdicion.cuota_id = mora.cuota_id
  formEdicion.fecha = mora.fecha
  formEdicion.valor = mora.valor
  formEdicion.estado = mora.estado
  modalEdicion.value = true
}

async function guardarEdicion() {
  if (!moraEditando.value) return
  const resultado = schema.safeParse(formEdicion)
  if (!resultado.success) {
    toast.add({ title: 'Datos inválidos', color: 'error' })
    return
  }
  enviando.value = true
  try {
    await actualizar(moraEditando.value.id, formEdicion)
    toast.add({ title: 'Mora actualizada', color: 'success' })
    modalEdicion.value = false
  } catch (e) {
    toast.add({ title: (e as { detail: string }).detail || 'No se pudo actualizar', color: 'error' })
  } finally {
    enviando.value = false
  }
}

async function confirmarEliminarMora() {
  if (!confirmarEliminar.value) return
  enviando.value = true
  try {
    await eliminar(confirmarEliminar.value.id)
    toast.add({ title: 'Mora eliminada', color: 'success' })
    confirmarEliminar.value = null
  } catch (e) {
    toast.add({ title: (e as { detail: string }).detail || 'No se pudo eliminar', color: 'error' })
  } finally {
    enviando.value = false
  }
}

const columns = [
  { accessorKey: 'id', header: 'ID', sorted: true },
  {
    header: 'Préstamo',
    cell: (row: Record<string, unknown>) => `#${String(row.prestamo_id ?? '')}`
  },
  {
    header: 'Cuota',
    cell: (row: Record<string, unknown>) => `#${String(row.cuota_id ?? '')}`
  },
  {
    header: 'Fecha',
    cell: (row: Record<string, unknown>) => formateo.formatoFecha(String(row.fecha))
  },
  {
    header: 'Valor',
    cell: (row: Record<string, unknown>) => formateo.formatoMoneda(Number(row.valor))
  },
  {
    header: 'Estado',
    component: UiEstadoBadge,
    componentProps: (row: Record<string, unknown>) => ({ entidad: 'cuota', estado: String(row.estado ?? '') })
  },
  {
    header: 'Acciones',
    component: UButton,
    componentProps: (row: Record<string, unknown>) => ({
      icon: 'i-lucide-ellipsis-vertical',
      color: 'neutral',
      variant: 'ghost',
      label: 'Acciones',
      onClick: () => abrirEdicion(row as unknown as Mora)
    })
  }
]
</script>

<template>
  <div class="p-6 space-y-4">
    <div class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <h1 class="text-2xl font-bold">
          Moras
        </h1>
        <p class="text-sm text-gray-500">
          La mora se calcula al 1% diario sobre el valor de la cuota por los días de atraso.
        </p>
      </div>
      <UButton
        color="warning"
        icon="i-lucide-calculator"
        :loading="procesando"
        @click="procesarMorasAhora"
      >
        Procesar moras ahora
      </UButton>
    </div>

    <UCard>
      <div class="flex items-end gap-3">
        <UFormField label="Filtrar por préstamo">
          <UInput
            v-model="filtroPrestamo"
            placeholder="ID del préstamo"
            type="number"
            min="1"
            icon="i-lucide-search"
          />
        </UFormField>
        <UButton
          color="primary"
          icon="i-lucide-search"
          @click="aplicarFiltro"
        >
          Filtrar
        </UButton>
        <UButton
          color="neutral"
          variant="outline"
          icon="i-lucide-x"
          @click="() => { filtroPrestamo = ''; fetchMoras() }"
        >
          Limpiar
        </UButton>
      </div>
    </UCard>

    <DataTable
      titulo="Moras generadas"
      :data="moras as Record<string, unknown>[]"
      :columns="columns"
      :loading="loading"
      :error="error"
      :llamar-datos="() => fetchMoras()"
      exportar-nombre="moras"
      @retry="fetchMoras"
    />

    <ModalDialog
      :open="modalEdicion"
      titulo="Editar mora"
      @update:open="modalEdicion = $event"
    >
      <template #body>
        <div class="space-y-4">
          <UFormField label="Fecha">
            <UInput
              v-model="formEdicion.fecha"
              type="date"
            />
          </UFormField>
          <UFormField label="Valor">
            <UInput
              v-model="formEdicion.valor"
              type="number"
              min="0"
              step="0.01"
            />
          </UFormField>
          <UFormField label="Estado">
            <USelect
              v-model="formEdicion.estado"
              :items="[
                { label: 'Pendiente', value: 'pendiente' },
                { label: 'Aplicada', value: 'aplicada' },
                { label: 'Cancelada', value: 'cancelada' }
              ]"
            />
          </UFormField>
        </div>
      </template>
      <template #footer>
        <div class="flex justify-end gap-2 pt-2">
          <UButton
            label="Cancelar"
            color="neutral"
            variant="outline"
            :disabled="enviando"
            @click="modalEdicion = false"
          />
          <UButton
            label="Guardar"
            color="primary"
            icon="i-lucide-save"
            :loading="enviando"
            @click="guardarEdicion"
          />
        </div>
      </template>
    </ModalDialog>

    <ConfirmDialog
      :open="!!confirmarEliminar"
      titulo="Eliminar mora"
      :mensaje="`¿Eliminar la mora #${confirmarEliminar?.id}?`"
      :loading="enviando"
      @update:open="(v: boolean) => !v && (confirmarEliminar = null)"
      @confirmar="confirmarEliminarMora"
    />
  </div>
</template>
