<script setup lang="ts">
import { z } from 'zod'
import { useTiposPrestamo, useTiposPago } from '~/composables/domain/useTipos'
import { useClientes } from '~/composables/domain/useClientes'
import { useCapital } from '~/composables/domain/useCapital'
import MoneyInput from '~/components/ui/MoneyInput.vue'

const props = defineProps<{
  open: boolean
}>()

const emit = defineEmits<{
  'update:open': [value: boolean]
  'completado': []
}>()

const isOpen = computed({
  get: () => props.open,
  set: v => emit('update:open', v)
})

const toast = useToast()
const formateo = useFormatters()

const { pasoActual, totalPasos, pasos, avanzarPaso, retrocederPaso, completar, omitir, cargando } = useOnboarding()
const { tipos: tiposPrestamo, fetch: fetchTiposPrestamo, crear: crearTipoPrestamo } = useTiposPrestamo()
const { tipos: tiposPago, fetch: fetchTiposPago, crear: crearTipoPago } = useTiposPago()
const { fetch: fetchClientes, crear: crearCliente } = useClientes()
const { capital, fetch: fetchCapital, registrar: registrarCapital } = useCapital()

// Paso 0: Tipos de préstamo
const tipoPrestamoForm = reactive({
  nombre: '',
  descripcion: '',
  interes_mensual: 0,
  max_cuotas: 12
})
const erroresPrestamo = ref<Record<string, string>>({})
const guardandoPrestamo = ref(false)

// Paso 1: Tipos de pago
const tipoPagoForm = reactive({
  nombre: '',
  descripcion: ''
})
const erroresPago = ref<Record<string, string>>({})
const guardandoPago = ref(false)

// Paso 2: Capital inicial
const capitalForm = reactive({
  valor: null as number | null,
  descripcion: 'Capital inicial'
})
const guardandoCapital = ref(false)

// Paso 3: Clientes
const clienteForm = reactive({
  nombre: '',
  cedula: '',
  telefono: ''
})
const erroresCliente = ref<Record<string, string>>({})
const guardandoCliente = ref(false)
const clientesCreados = ref<{ nombre: string, cedula: string }[]>([])

const schemaPrestamo = z.object({
  nombre: z.string().min(1, 'El nombre es requerido'),
  descripcion: z.string().min(1, 'La descripción es requerida'),
  interes_mensual: z.number().positive('El interés debe ser mayor a 0'),
  max_cuotas: z.number().positive('Debe ser mayor a 0')
})

const schemaPago = z.object({
  nombre: z.string().min(1, 'El nombre es requerido'),
  descripcion: z.string().min(1, 'La descripción es requerida')
})

const schemaCliente = z.object({
  nombre: z.string().min(1, 'El nombre es requerido'),
  cedula: z.string().min(3, 'La cédula es requerida')
})

const pasoTerminado = computed(() => {
  switch (pasoActual.value) {
    case 0: return tiposPrestamo.value.length > 0
    case 1: return tiposPago.value.length > 0
    case 2: return capital.value != null && capital.value.monto_total > 0
    case 3: return clientesCreados.value.length > 0
    default: return false
  }
})

async function guardarTipoPrestamo() {
  erroresPrestamo.value = {}
  const resultado = schemaPrestamo.safeParse(tipoPrestamoForm)
  if (!resultado.success) {
    for (const issue of resultado.error.issues) {
      erroresPrestamo.value[issue.path[0] as string] = issue.message
    }
    return
  }
  guardandoPrestamo.value = true
  try {
    await crearTipoPrestamo({
      nombre: tipoPrestamoForm.nombre,
      descripcion: tipoPrestamoForm.descripcion,
      interes_mensual: tipoPrestamoForm.interes_mensual,
      max_cuotas: tipoPrestamoForm.max_cuotas
    })
    toast.add({ title: 'Tipo de préstamo creado', color: 'success' })
    tipoPrestamoForm.nombre = ''
    tipoPrestamoForm.descripcion = ''
    tipoPrestamoForm.interes_mensual = 0
    tipoPrestamoForm.max_cuotas = 12
    await fetchTiposPrestamo()
  } catch {
    toast.add({ title: 'No se pudo crear el tipo de préstamo', color: 'error' })
  } finally {
    guardandoPrestamo.value = false
  }
}

async function guardarTipoPago() {
  erroresPago.value = {}
  const resultado = schemaPago.safeParse(tipoPagoForm)
  if (!resultado.success) {
    for (const issue of resultado.error.issues) {
      erroresPago.value[issue.path[0] as string] = issue.message
    }
    return
  }
  guardandoPago.value = true
  try {
    await crearTipoPago({
      nombre: tipoPagoForm.nombre,
      descripcion: tipoPagoForm.descripcion
    })
    toast.add({ title: 'Tipo de pago creado', color: 'success' })
    tipoPagoForm.nombre = ''
    tipoPagoForm.descripcion = ''
    await fetchTiposPago()
  } catch {
    toast.add({ title: 'No se pudo crear el tipo de pago', color: 'error' })
  } finally {
    guardandoPago.value = false
  }
}

async function guardarCapital() {
  if (capitalForm.valor == null || capitalForm.valor <= 0) {
    toast.add({ title: 'Ingresa un valor válido', color: 'error' })
    return
  }
  guardandoCapital.value = true
  try {
    await registrarCapital({
      tipo_movimiento: 'inversion',
      valor: capitalForm.valor,
      descripcion: capitalForm.descripcion,
      fecha: new Date().toISOString().split('T')[0] ?? new Date().toISOString().slice(0, 10)
    })
    toast.add({ title: 'Capital inicial registrado', color: 'success' })
    await fetchCapital()
  } catch {
    toast.add({ title: 'No se pudo registrar el capital', color: 'error' })
  } finally {
    guardandoCapital.value = false
  }
}

async function guardarCliente() {
  erroresCliente.value = {}
  const resultado = schemaCliente.safeParse(clienteForm)
  if (!resultado.success) {
    for (const issue of resultado.error.issues) {
      erroresCliente.value[issue.path[0] as string] = issue.message
    }
    return
  }
  guardandoCliente.value = true
  try {
    await crearCliente({
      nombre: clienteForm.nombre,
      cedula: clienteForm.cedula,
      telefono: clienteForm.telefono || null
    })
    clientesCreados.value.push({ nombre: clienteForm.nombre, cedula: clienteForm.cedula })
    toast.add({ title: 'Cliente creado', color: 'success' })
    clienteForm.nombre = ''
    clienteForm.cedula = ''
    clienteForm.telefono = ''
    await fetchClientes()
  } catch {
    toast.add({ title: 'No se pudo crear el cliente', color: 'error' })
  } finally {
    guardandoCliente.value = false
  }
}

async function finalizar() {
  await completar()
  emit('completado')
  isOpen.value = false
}
</script>

<template>
  <UModal
    :open="isOpen"
    :ui="{ content: 'max-w-xl' }"
    @update:open="isOpen = $event"
  >
    <template #title>
      <div class="flex items-center gap-2">
        <UIcon
          name="i-lucide-rocket"
          class="text-primary"
        />
        <span>Configuración inicial</span>
      </div>
    </template>
    <template #body>
      <div class="space-y-6">
        <div class="flex items-center justify-between">
          <div
            v-for="(paso, i) in pasos"
            :key="paso.id"
            class="flex items-center"
          >
            <div
              class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold transition-colors"
              :class="i < pasoActual ? 'bg-green-500 text-white' : i === pasoActual ? 'bg-primary text-white' : 'bg-gray-200 dark:bg-gray-700 text-gray-500'"
            >
              <UIcon
                v-if="i < pasoActual"
                name="i-lucide-check"
                class="w-4 h-4"
              />
              <span v-else>{{ i + 1 }}</span>
            </div>
            <div
              v-if="i < pasos.length - 1"
              class="w-8 h-0.5 mx-1"
              :class="i < pasoActual ? 'bg-green-500' : 'bg-gray-200 dark:bg-gray-700'"
            />
          </div>
        </div>

        <div class="text-center">
          <UIcon
            :name="pasos[pasoActual]?.icono ?? 'i-lucide-circle'"
            class="text-3xl text-primary mb-2"
          />
          <h3 class="text-lg font-bold">
            {{ pasos[pasoActual]?.titulo }}
          </h3>
          <p class="text-sm text-gray-500">
            {{ pasos[pasoActual]?.descripcion }}
          </p>
        </div>

        <div
          v-if="pasoActual === 0"
          class="space-y-4"
        >
          <div class="space-y-2 max-h-32 overflow-y-auto">
            <div
              v-for="tipo in tiposPrestamo"
              :key="tipo.id"
              class="flex items-center gap-2 p-2 rounded bg-green-50 dark:bg-green-900/20 text-sm"
            >
              <UIcon
                name="i-lucide-check-circle"
                class="text-green-500"
              />
              <span class="font-medium">{{ tipo.nombre }}</span>
              <span class="text-gray-400">· {{ tipo.interes_mensual }}% mensual · máx {{ tipo.max_cuotas }} cuotas</span>
            </div>
            <p
              v-if="!tiposPrestamo.length"
              class="text-xs text-gray-400 text-center"
            >
              Aún no has creado tipos de préstamo
            </p>
          </div>
          <div class="grid grid-cols-2 gap-3">
            <UFormField
              label="Nombre *"
              :error="erroresPrestamo.nombre"
              class="col-span-2"
            >
              <UInput
                v-model="tipoPrestamoForm.nombre"
                placeholder="Ej: Personal"
              />
            </UFormField>
            <UFormField
              label="Descripción *"
              :error="erroresPrestamo.descripcion"
              class="col-span-2"
            >
              <UInput
                v-model="tipoPrestamoForm.descripcion"
                placeholder="Descripción breve"
              />
            </UFormField>
            <UFormField
              label="Interés mensual (%)"
              :error="erroresPrestamo.interes_mensual"
            >
              <UInput
                v-model.number="tipoPrestamoForm.interes_mensual"
                type="number"
                min="0"
                step="0.5"
              />
            </UFormField>
            <UFormField
              label="Máx. cuotas"
              :error="erroresPrestamo.max_cuotas"
            >
              <UInput
                v-model.number="tipoPrestamoForm.max_cuotas"
                type="number"
                min="1"
              />
            </UFormField>
          </div>
          <UButton
            label="Agregar tipo"
            icon="i-lucide-plus"
            color="primary"
            size="sm"
            :loading="guardandoPrestamo"
            @click="guardarTipoPrestamo"
          />
        </div>

        <div
          v-if="pasoActual === 1"
          class="space-y-4"
        >
          <div class="space-y-2 max-h-32 overflow-y-auto">
            <div
              v-for="tipo in tiposPago"
              :key="tipo.id"
              class="flex items-center gap-2 p-2 rounded bg-green-50 dark:bg-green-900/20 text-sm"
            >
              <UIcon
                name="i-lucide-check-circle"
                class="text-green-500"
              />
              <span class="font-medium">{{ tipo.nombre }}</span>
            </div>
            <p
              v-if="!tiposPago.length"
              class="text-xs text-gray-400 text-center"
            >
              Aún no has creado tipos de pago
            </p>
          </div>
          <UFormField
            label="Nombre *"
            :error="erroresPago.nombre"
          >
            <UInput
              v-model="tipoPagoForm.nombre"
              placeholder="Ej: Efectivo, Transferencia"
            />
          </UFormField>
          <UFormField
            label="Descripción *"
            :error="erroresPago.descripcion"
          >
            <UInput
              v-model="tipoPagoForm.descripcion"
              placeholder="Descripción breve"
            />
          </UFormField>
          <UButton
            label="Agregar tipo"
            icon="i-lucide-plus"
            color="primary"
            size="sm"
            :loading="guardandoPago"
            @click="guardarTipoPago"
          />
        </div>

        <div
          v-if="pasoActual === 2"
          class="space-y-4"
        >
          <div
            v-if="capital && capital.monto_total > 0"
            class="p-3 rounded bg-green-50 dark:bg-green-900/20 text-sm"
          >
            <p class="font-medium text-green-700 dark:text-green-300">
              Capital actual: {{ formateo.formatoMoneda(capital.monto_total) }}
            </p>
          </div>
          <div
            v-else
            class="p-3 rounded bg-amber-50 dark:bg-amber-900/20 text-sm"
          >
            <p class="text-amber-700 dark:text-amber-300">
              Aún no has registrado capital inicial
            </p>
          </div>
          <MoneyInput
            v-model="capitalForm.valor"
            label="Capital inicial *"
            placeholder="$ 0"
          />
          <UFormField label="Descripción">
            <UInput
              v-model="capitalForm.descripcion"
              placeholder="Ej: Capital inicial del negocio"
            />
          </UFormField>
          <UButton
            label="Registrar capital"
            icon="i-lucide-wallet"
            color="primary"
            size="sm"
            :loading="guardandoCapital"
            @click="guardarCapital"
          />
        </div>

        <div
          v-if="pasoActual === 3"
          class="space-y-4"
        >
          <div class="space-y-2 max-h-32 overflow-y-auto">
            <div
              v-for="(c, i) in clientesCreados"
              :key="i"
              class="flex items-center gap-2 p-2 rounded bg-green-50 dark:bg-green-900/20 text-sm"
            >
              <UIcon
                name="i-lucide-check-circle"
                class="text-green-500"
              />
              <span class="font-medium">{{ c.nombre }}</span>
              <span class="text-gray-400">· CC {{ c.cedula }}</span>
            </div>
            <p
              v-if="!clientesCreados.length"
              class="text-xs text-gray-400 text-center"
            >
              Aún no has creado clientes
            </p>
          </div>
          <UFormField
            label="Nombre completo *"
            :error="erroresCliente.nombre"
          >
            <UInput
              v-model="clienteForm.nombre"
              placeholder="Nombre del cliente"
            />
          </UFormField>
          <UFormField
            label="Cédula *"
            :error="erroresCliente.cedula"
          >
            <UInput
              v-model="clienteForm.cedula"
              placeholder="Número de cédula"
            />
          </UFormField>
          <UFormField label="Teléfono">
            <UInput
              v-model="clienteForm.telefono"
              placeholder="Opcional"
            />
          </UFormField>
          <UButton
            label="Agregar cliente"
            icon="i-lucide-user-plus"
            color="primary"
            size="sm"
            :loading="guardandoCliente"
            @click="guardarCliente"
          />
        </div>
      </div>
    </template>
    <template #footer>
      <div class="flex justify-between">
        <div class="flex gap-2">
          <UButton
            label="Omitir"
            color="neutral"
            variant="ghost"
            size="sm"
            @click="omitir"
          />
        </div>
        <div class="flex gap-2">
          <UButton
            v-if="pasoActual > 0"
            label="Atrás"
            color="neutral"
            variant="outline"
            size="sm"
            @click="retrocederPaso"
          />
          <UButton
            v-if="pasoActual < totalPasos - 1"
            label="Siguiente"
            color="primary"
            size="sm"
            :disabled="!pasoTerminado"
            @click="avanzarPaso"
          />
          <UButton
            v-else
            label="Finalizar"
            color="success"
            icon="i-lucide-check"
            size="sm"
            :loading="cargando"
            @click="finalizar"
          />
        </div>
      </div>
    </template>
  </UModal>
</template>
