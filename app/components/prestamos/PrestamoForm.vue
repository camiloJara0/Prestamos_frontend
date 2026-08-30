<script setup lang="ts">
import { z } from 'zod'
import { calcularPrestamo, calcularCuotas } from '~/utils/calculadoraPrestamo'
import type { Cliente } from '#shared/types/clientes'
import type { TipoPrestamo } from '#shared/types/tipo_prestamo'
import type { PrestamoCreate } from '#shared/types/prestamo'

const props = withDefaults(defineProps<{
  clientes?: Cliente[]
  tiposPrestamo?: TipoPrestamo[]
  capitalDisponible?: number
}>(), {
  clientes: () => [],
  tiposPrestamo: () => [],
  capitalDisponible: 0
})

const emit = defineEmits<{
  guardar: [data: PrestamoCreate]
}>()

const schema = z.object({
  cliente_id: z.number().positive('Selecciona un cliente'),
  tipo_prestamo_id: z.number().positive('Selecciona un tipo de préstamo'),
  fecha_prestamo: z.string().min(1, 'La fecha es requerida'),
  capital_prestado: z.number().positive('El capital debe ser mayor a 0'),
  porcentaje_interes: z.number().positive('El interés debe ser mayor a 0'),
  numero_cuotas: z.number().int().min(1, 'Debe haber al menos 1 cuota')
})

const form = reactive({
  cliente_id: 0 as number,
  tipo_prestamo_id: 0 as number,
  fecha_prestamo: hoyLocal(),
  capital_prestado: null as number | null,
  porcentaje_interes: null as number | null,
  numero_cuotas: null as number | null,
  observaciones: ''
})

const errores = ref<Record<string, string>>({})
const busquedaCliente = ref('')
const clienteDropdownAbierto = ref(false)

const clientesFiltrados = computed(() => {
  const t = busquedaCliente.value.trim().toLowerCase()
  if (!t) return props.clientes
  return props.clientes.filter(c =>
    c.nombre.toLowerCase().includes(t) || c.cedula.toLowerCase().includes(t)
  )
})

const capitalInsuficiente = computed(() =>
  (form.capital_prestado ?? 0) > props.capitalDisponible
)

const calculo = computed(() => {
  if (!form.capital_prestado || !form.porcentaje_interes || !form.numero_cuotas) return null
  if (form.capital_prestado <= 0 || form.porcentaje_interes <= 0 || form.numero_cuotas < 1) return null
  return calcularPrestamo({
    capital_prestado: form.capital_prestado,
    porcentaje_interes: form.porcentaje_interes,
    numero_cuotas: form.numero_cuotas
  })
})

const cuotasPreview = computed(() => {
  if (!calculo.value || !form.fecha_prestamo) return []
  return calcularCuotas({
    capital_prestado: form.capital_prestado as number,
    interes_total: calculo.value.interes_total,
    numero_cuotas: form.numero_cuotas as number,
    fecha_prestamo: form.fecha_prestamo
  })
})

const capitalInput = computed({
  get: () => form.capital_prestado != null ? String(form.capital_prestado) : '',
  set: (v) => {
    form.capital_prestado = v === '' ? null : Number(v)
  }
})

const interesInput = computed({
  get: () => form.porcentaje_interes != null ? String(form.porcentaje_interes) : '',
  set: (v) => {
    form.porcentaje_interes = v === '' ? null : Number(v)
  }
})

const cuotasInput = computed({
  get: () => form.numero_cuotas != null ? String(form.numero_cuotas) : '',
  set: (v) => {
    form.numero_cuotas = v === '' ? null : Number(v)
  }
})

watch(() => form.tipo_prestamo_id, (id) => {
  const tipo = props.tiposPrestamo.find(t => t.id === id)
  if (tipo?.interes_mensual != null) {
    form.porcentaje_interes = tipo.interes_mensual
  }
  if (tipo?.max_cuotas != null) {
    form.numero_cuotas = tipo.max_cuotas
  }
})

function seleccionarCliente(cliente: Cliente) {
  form.cliente_id = cliente.id
  busquedaCliente.value = cliente.nombre
  clienteDropdownAbierto.value = false
}

function validar() {
  const resultado = schema.safeParse({
    ...form,
    capital_prestado: form.capital_prestado ?? undefined,
    porcentaje_interes: form.porcentaje_interes ?? undefined,
    numero_cuotas: form.numero_cuotas ?? undefined
  })
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

function submit() {
  if (!validar() || capitalInsuficiente.value) return
  emit('guardar', {
    cliente_id: form.cliente_id,
    tipo_prestamo_id: form.tipo_prestamo_id,
    fecha_prestamo: form.fecha_prestamo,
    capital_prestado: Number(form.capital_prestado),
    porcentaje_interes: Number(form.porcentaje_interes),
    numero_cuotas: Number(form.numero_cuotas),
    observaciones: form.observaciones || null
  })
}

defineExpose({ submit, validar, form })
</script>

<template>
  <form
    class="space-y-6"
    @submit.prevent="submit"
  >
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <UFormField
        label="Cliente *"
        :error="errores.cliente_id"
        class="sm:col-span-2"
      >
        <div class="relative">
          <UInput
            :model-value="busquedaCliente"
            placeholder="Buscar por nombre o cédula"
            icon="i-lucide-user-search"
            class="w-full"
            @update:model-value="(v) => { busquedaCliente = v; form.cliente_id = 0; clienteDropdownAbierto = true }"
            @focus="clienteDropdownAbierto = true"
          />
          <div
            v-if="clienteDropdownAbierto"
            class="absolute z-10 w-full mt-1 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg max-h-60 overflow-y-auto"
          >
            <button
              v-for="cliente in clientesFiltrados"
              :key="cliente.id"
              type="button"
              class="w-full text-left px-3 py-2 text-sm hover:bg-purple-50 dark:hover:bg-purple-950/30"
              @click="seleccionarCliente(cliente)"
            >
              <span class="font-medium">{{ cliente.nombre }}</span>
              <span class="text-xs text-gray-400 ml-2">{{ cliente.cedula }}</span>
            </button>
            <p
              v-if="!clientesFiltrados.length"
              class="px-3 py-2 text-sm text-gray-400"
            >
              Sin resultados
            </p>
          </div>
        </div>
      </UFormField>

      <UFormField
        label="Tipo de préstamo *"
        :error="errores.tipo_prestamo_id"
      >
        <USelect
          v-model="form.tipo_prestamo_id"
          :items="tiposPrestamo.filter(t => t.estado === 'activo').map(t => ({ label: t.nombre, value: t.id }))"
          placeholder="Selecciona un tipo"
            class="w-full"
        />
      </UFormField>

      <UFormField label="Fecha del préstamo *">
        <UInput
          v-model="form.fecha_prestamo"
          type="date"
            class="w-full"
        />
      </UFormField>

      <UFormField
        label="Capital a prestar *"
        :error="errores.capital_prestado || (capitalInsuficiente ? 'El capital supera el disponible' : '')"
      >
        <UInput
          v-model="capitalInput"
          type="number"
          min="0"
          step="0.01"
          placeholder="Ej: 1000000"
            class="w-full"
        />
      </UFormField>

      <UFormField
        label="Interés mensual (%) *"
        :error="errores.porcentaje_interes"
      >
        <UInput
          v-model="interesInput"
          type="number"
          min="0"
          step="0.01"
          placeholder="Ej: 2.5"
            class="w-full"
        />
      </UFormField>

      <UFormField
        label="Número de cuotas *"
        :error="errores.numero_cuotas"
      >
        <UInput
          v-model="cuotasInput"
          type="number"
          min="1"
          step="1"
          placeholder="Ej: 12"
            class="w-full"
        />
      </UFormField>

      <UFormField
        label="Observaciones"
      >
        <UInput
          v-model="form.observaciones"
          placeholder="Opcional"
            class="w-full"
        />
      </UFormField>
    </div>

    <UAlert
      v-if="capitalInsuficiente"
      color="error"
      title="Capital insuficiente"
      :description="`El capital disponible es ${formatoMoneda(capitalDisponible)}. Reduce el monto del préstamo.`"
    />

    <div
      v-if="calculo"
      class="rounded-xl border border-primary-500/20 p-4 bg-primary-500/5"
    >
      <h4 class="font-semibold text-sm mb-3">
        Resumen del préstamo
      </h4>
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-sm">
        <div>
          <p class="text-xs text-gray-500">
            Interés total
          </p>
          <p class="font-semibold">
            {{ formatoMoneda(calculo.interes_total) }}
          </p>
        </div>
        <div>
          <p class="text-xs text-gray-500">
            Monto total
          </p>
          <p class="font-semibold">
            {{ formatoMoneda(calculo.monto_total) }}
          </p>
        </div>
        <div>
          <p class="text-xs text-gray-500">
            Valor cuota
          </p>
          <p class="font-semibold">
            {{ formatoMoneda(calculo.valor_cuota) }}
          </p>
        </div>
        <div>
          <p class="text-xs text-gray-500">
            Saldo inicial
          </p>
          <p class="font-semibold">
            {{ formatoMoneda(calculo.saldo_pendiente) }}
          </p>
        </div>
      </div>

      <div
        v-if="cuotasPreview.length"
        class="mt-4"
      >
        <p class="text-xs text-gray-500 mb-2">
          Primeras cuotas
        </p>
        <div class="space-y-1.5">
          <div
            v-for="cuota in cuotasPreview.slice(0, 5)"
            :key="cuota.numero_cuota"
            class="flex justify-between text-sm bg-white/50 dark:bg-white/5 rounded-md px-3 py-1.5"
          >
            <span>Cuota {{ cuota.numero_cuota }} · vence {{ formatoFecha(cuota.fecha_vencimiento) }}</span>
            <span class="font-medium">{{ formatoMoneda(cuota.valor_cuota) }}</span>
          </div>
        </div>
      </div>
    </div>
  </form>
</template>
