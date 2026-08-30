<script setup lang="ts">
import { z } from 'zod'
import type { PrestamoDetalle } from '#shared/types/prestamo'
import type { PrestamoCuota } from '#shared/types/prestamo_cuota'
import type { TipoPago } from '#shared/types/tipo_pago'
import { sugerirDesglosePago, validarCuadrePago, topePago } from '~/utils/calculadoraPrestamo'
import MoneyInput from '../ui/MoneyInput.vue'

const props = defineProps<{
  prestamoInicial?: PrestamoDetalle | null
  cuotaInicial?: PrestamoCuota | null
  tiposPago?: TipoPago[]
}>()
console.log(props.tiposPago)
const emit = defineEmits<{
  guardar: [data: {
    prestamo_id: number
    cliente_id: number
    cuota_id: number
    tipo_pago_id: number
    fecha_pago: string
    valor_pagado: number
    capital_pagado: number
    interes_pagado: number
    mora_pagada: number
    observaciones?: string | null
  }]
}>()

const schema = z.object({
  prestamo_id: z.number().positive('Selecciona un préstamo'),
  cuota_id: z.number().positive('Selecciona una cuota'),
  tipo_pago_id: z.number().positive('Selecciona un tipo de pago'),
  fecha_pago: z.string().min(1, 'La fecha es requerida'),
  valor_pagado: z.number().positive('El valor debe ser mayor a 0'),
  capital_pagado: z.number().min(0, 'No puede ser negativo'),
  interes_pagado: z.number().min(0, 'No puede ser negativo'),
  mora_pagada: z.number().min(0, 'No puede ser negativo')
})

const form = reactive({
  prestamo_id: props.prestamoInicial?.id ?? 0,
  cuota_id: props.cuotaInicial?.id ?? 0,
  tipo_pago_id: 0,
  fecha_pago: hoyLocal(),
  valor_pagado: props.cuotaInicial?.valor_cuota ?? null as number | null,
  capital_pagado: props.cuotaInicial?.capital ?? null as number | null,
  interes_pagado: props.cuotaInicial?.interes ?? null as number | null,
  mora_pagada: props.cuotaInicial?.mora ?? null as number | null,
  observaciones: ''
})

const errores = ref<Record<string, string>>({})
const busquedaPrestamo = ref('')
const prestamoSeleccionado = ref<PrestamoDetalle | null>(props.prestamoInicial ?? null)
const cuotasPendientes = ref<PrestamoCuota[]>([])
const busquedaAbierta = ref(false)
const buscandoPrestamo = ref(false)

const cuotaSeleccionada = computed(() =>
  cuotasPendientes.value.find(c => c.id === form.cuota_id)
)

const validacion = computed(() => {
  if (form.valor_pagado == null || form.capital_pagado == null || form.interes_pagado == null || form.mora_pagada == null) {
    return { valido: false, diferencia: 0, razon: 'Completa todos los campos del desglose' }
  }
  const resultado = validarCuadrePago({
    valor_pagado: form.valor_pagado,
    capital_pagado: form.capital_pagado,
    interes_pagado: form.interes_pagado,
    mora_pagada: form.mora_pagada
  })
  const tope = topePago(cuotaSeleccionada.value?.valor_cuota ?? 0, cuotaSeleccionada.value?.mora ?? 0)
  const excedeTope = form.valor_pagado > tope
  return {
    valido: resultado.valido && !excedeTope,
    diferencia: resultado.diferencia,
    razon: excedeTope ? 'El valor excede el tope permitido' : undefined
  }
})

const valorInput = computed({
  get: () => form.valor_pagado != null ? String(form.valor_pagado) : '',
  set: (v: string) => {
    form.valor_pagado = v === '' ? null : Number(v)
    sugerirDesglose()
  }
})

const capitalInput = computed({
  get: () => form.capital_pagado != null ? String(form.capital_pagado) : '',
  set: (v: string) => { form.capital_pagado = v === '' ? null : Number(v) }
})

const interesInput = computed({
  get: () => form.interes_pagado != null ? String(form.interes_pagado) : '',
  set: (v: string) => { form.interes_pagado = v === '' ? null : Number(v) }
})

const moraInput = computed({
  get: () => form.mora_pagada != null ? String(form.mora_pagada) : '',
  set: (v: string) => { form.mora_pagada = v === '' ? null : Number(v) }
})

function sugerirDesglose() {
  if (!cuotaSeleccionada.value || form.valor_pagado == null) return
  const sugerido = sugerirDesglosePago({
    valorPagado: form.valor_pagado,
    capitalCuota: cuotaSeleccionada.value.capital,
    interesCuota: cuotaSeleccionada.value.interes
  })
  form.capital_pagado = sugerido.capital_pagado
  form.interes_pagado = sugerido.interes_pagado
  form.mora_pagada = sugerido.mora_pagada
}

watch(() => form.cuota_id, () => {
  if (cuotaSeleccionada.value) {
    form.valor_pagado = cuotaSeleccionada.value.valor_cuota
    sugerirDesglose()
  }
})

async function buscarPrestamo() {
  const termino = busquedaPrestamo.value.trim()
  if (!termino) return
  buscandoPrestamo.value = true
  try {
    const { getPrestamos } = await import('~/services/api/prestamo')
    const { getPrestamoById } = await import('~/services/api/prestamo')
    const resultados = await getPrestamos({ busqueda: termino, estado: 'activo', limit: 10 })
    if (resultados.length === 1) {
      const id = resultados[0]?.id
      if (id == null) return
      const detalle = await getPrestamoById(id)
      prestamoSeleccionado.value = detalle
      form.prestamo_id = detalle.id
      cuotasPendientes.value = detalle.cuotas.filter(c => c.estado === 'pendiente')
      if (cuotasPendientes.value.length === 1 && cuotasPendientes.value[0]) {
        form.cuota_id = cuotasPendientes.value[0].id
      }
    } else if (resultados.length > 1) {
      busquedaAbierta.value = true
    }
  } finally {
    buscandoPrestamo.value = false
  }
}

function validar() {
  const resultado = schema.safeParse({
    ...form,
    valor_pagado: form.valor_pagado ?? undefined,
    capital_pagado: form.capital_pagado ?? undefined,
    interes_pagado: form.interes_pagado ?? undefined,
    mora_pagada: form.mora_pagada ?? undefined
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
  if (!validar()) return
  emit('guardar', {
    prestamo_id: form.prestamo_id,
    cliente_id: prestamoSeleccionado.value?.cliente_id ?? 0,
    cuota_id: form.cuota_id,
    tipo_pago_id: form.tipo_pago_id,
    fecha_pago: form.fecha_pago,
    valor_pagado: Number(form.valor_pagado),
    capital_pagado: Number(form.capital_pagado),
    interes_pagado: Number(form.interes_pagado),
    mora_pagada: Number(form.mora_pagada),
    observaciones: form.observaciones || undefined
  })
}

defineExpose({ submit, validar })

watch(() => props.prestamoInicial, (p) => {
  if (p) {
    prestamoSeleccionado.value = p
    form.prestamo_id = p.id
    cuotasPendientes.value = p.cuotas.filter(c => c.estado === 'pendiente')
  }
})

watch(() => props.cuotaInicial, (c) => {
  if (c) {
    form.cuota_id = c.id
    form.valor_pagado = c.valor_cuota
    sugerirDesglose()
  }
})
</script>

<template>
  <form
    class="space-y-6"
    @submit.prevent="submit"
  >
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <UFormField
        label="Buscar préstamo *"
        :error="errores.prestamo_id"
        class="sm:col-span-2"
      >
        <div class="flex gap-2">
          <UInput
            v-model="busquedaPrestamo"
            placeholder="Nombre o cédula del cliente"
            icon="i-lucide-search"
            class="flex-1"
            @keyup.enter="buscarPrestamo"
          />
          <UButton
            color="primary"
            icon="i-lucide-search"
            :loading="buscandoPrestamo"
            @click="buscarPrestamo"
          >
            Buscar
          </UButton>
        </div>
      </UFormField>

      <template v-if="prestamoSeleccionado">
        <UAlert
          class="sm:col-span-2"
          color="info"
          icon="i-lucide-check-circle"
        >
          <template #title>
            Préstamo #{{ prestamoSeleccionado.id }} — {{ prestamoSeleccionado.cliente?.nombre ?? `Cliente #${prestamoSeleccionado.cliente_id}` }}
          </template>
          <template #description>
            Saldo: {{ formatoMoneda(prestamoSeleccionado.saldo_pendiente) }} · Cuotas pendientes: {{ cuotasPendientes.length }}
          </template>
        </UAlert>

        <UFormField
          label="Cuota a pagar *"
          :error="errores.cuota_id"
        >
          <USelect
            v-model="form.cuota_id"
            :items="cuotasPendientes.map(c => ({
              label: `Cuota ${c.numero_cuota} — vence ${formatoFecha(c.fecha_vencimiento)} — ${formatoMoneda(c.valor_cuota)}`,
              value: c.id
            }))"
            placeholder="Selecciona una cuota"
            class="w-full"
          />
        </UFormField>

        <UFormField
          label="Tipo de pago *"
          :error="errores.tipo_pago_id"
        >
          <USelect
            v-model="form.tipo_pago_id"
            :items="tiposPago?.map(t => ({ label: t.nombre, value: t.id })) ?? []"
            placeholder="Selecciona un tipo"
            class="w-full"
          />
        </UFormField>

        <UFormField
          label="Fecha de pago *"
          :error="errores.fecha_pago"
        >
          <UInput
            v-model="form.fecha_pago"
            type="date"
          />
        </UFormField>

        <UFormField
          label="Valor pagado *"
          :error="errores.valor_pagado"
        >
          <MoneyInput v-model="valorInput" />
        </UFormField>
      </template>
    </div>

    <template v-if="cuotaSeleccionada">
      <div class="rounded-xl border border-primary-500/20 p-4 bg-primary-500/5">
        <h4 class="font-semibold text-sm mb-3">
          Desglose del pago
        </h4>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <UFormField
            label="Capital"
            :error="errores.capital_pagado"
          >
            <MoneyInput v-model="capitalInput" />
          </UFormField>
          <UFormField
            label="Interés"
            :error="errores.interes_pagado"
          >
            <MoneyInput v-model="interesInput" />
          </UFormField>
          <UFormField
            label="Mora"
            :error="errores.mora_pagada"
          >
            <MoneyInput v-model="moraInput" />
          </UFormField>
        </div>

        <div class="mt-3 flex items-center gap-3">
          <UBadge
            :color="validacion.valido ? 'success' : 'error'"
            variant="subtle"
          >
            {{ validacion.valido ? 'Desglose válido' : `Diferencia: ${formatoMoneda(validacion.diferencia)}` }}
          </UBadge>
          <span class="text-xs text-gray-500">
            Capital ({{ formatoMoneda(cuotaSeleccionada.capital) }}) + Interés ({{ formatoMoneda(cuotaSeleccionada.interes) }}) + Mora = Valor pagado
          </span>
        </div>
      </div>

      <UFormField label="Observaciones">
        <UInput
          v-model="form.observaciones"
          placeholder="Opcional"
        />
      </UFormField>
    </template>
  </form>
</template>
