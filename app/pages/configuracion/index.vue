<script setup lang="ts">
import type { Configuracion } from '#shared/types/configuracion'
import { getConfiguraciones, actualizarConfiguracion } from '~/services/api/configuracion'

definePageMeta({
  middleware: 'admin'
})

const toast = useToast()

type Metadato = {
  titulo: string
  descripcion: string
  sufijo: string
  icono: string
  entero?: boolean
}

const metadatos: Record<string, Metadato> = {
  tasa_mora_diaria: {
    titulo: 'Tasa de mora diaria',
    descripcion: 'Porcentaje diario que se aplica a las cuotas vencidas. Los procesos de mora leen este valor antes de calcular.',
    sufijo: '%',
    icono: 'i-lucide-percent'
  },
  interes_minimo: {
    titulo: 'Interés mínimo',
    descripcion: 'Porcentaje mínimo de interés aceptado al crear un préstamo.',
    sufijo: '%',
    icono: 'i-lucide-trending-down'
  },
  dias_gracia_mora: {
    titulo: 'Días de gracia',
    descripcion: 'Días posteriores al vencimiento que se aplican sin generar mora.',
    sufijo: 'días',
    icono: 'i-lucide-calendar-clock',
    entero: true
  }
}

const configuraciones = ref<Configuracion[]>([])
const valores = ref<Record<string, string>>({})
const errores = ref<Record<string, string>>({})
const guardando = ref<string | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)

async function cargar() {
  loading.value = true
  error.value = null
  try {
    configuraciones.value = await getConfiguraciones()
    const inicial: Record<string, string> = {}
    for (const c of configuraciones.value) inicial[c.clave] = c.valor
    valores.value = inicial
  } catch {
    error.value = 'No se pudo cargar la configuración del sistema.'
  } finally {
    loading.value = false
  }
}
cargar()

function validar(clave: string, valor: string): string | null {
  const meta = metadatos[clave]
  const limpio = valor.trim()
  if (limpio === '') return 'El valor es obligatorio'
  const numero = Number(limpio)
  if (!Number.isFinite(numero)) return 'Debe ser un valor numérico'
  if (numero < 0) return 'No puede ser negativo'
  if (meta?.entero && !Number.isInteger(numero)) return 'Debe ser un número entero'
  return null
}

async function guardar(c: Configuracion) {
  const valor = valores.value[c.clave] ?? ''
  const mensaje = validar(c.clave, valor)
  if (mensaje) {
    errores.value = { ...errores.value, [c.clave]: mensaje }
    return
  }
  errores.value = { ...errores.value, [c.clave]: '' }
  guardando.value = c.clave
  try {
    const actualizada = await actualizarConfiguracion(c.clave, valor.trim())
    configuraciones.value = configuraciones.value.map(item => item.clave === c.clave ? actualizada : item)
    toast.add({ title: `Parámetro '${c.clave}' actualizado`, color: 'success' })
  } catch (e) {
    toast.add({ title: (e as { detail: string }).detail || 'No se pudo guardar el parámetro', color: 'error' })
  } finally {
    guardando.value = null
  }
}
</script>

<template>
  <div class="p-6 space-y-4">
    <UiPageHeader
      titulo="Configuración del sistema"
      descripcion="Parámetros de negocio editables sin modificar código."
      icono="i-lucide-settings"
    />

    <UAlert
      icon="i-lucide-info"
      color="info"
      title="Valores numéricos y no negativos"
      description="Si un parámetro no existe, los procesos aplican el valor por defecto documentado en el código. Toda modificación queda registrada en la auditoría con usuario e IP."
    />

    <UAlert
      v-if="error"
      icon="i-lucide-alert-triangle"
      color="error"
      :title="error"
      :actions="[{ label: 'Reintentar', color: 'primary', variant: 'outline', onClick: cargar }]"
    />

    <USkeleton
      v-if="loading"
      class="h-40 rounded-xl"
    />

    <div
      v-else
      class="grid grid-cols-1 md:grid-cols-3 gap-4"
    >
      <UCard
        v-for="c in configuraciones"
        :key="c.clave"
      >
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon
              :name="metadatos[c.clave]?.icono ?? 'i-lucide-settings'"
              class="text-primary"
            />
            <div>
              <h3 class="font-bold">
                {{ metadatos[c.clave]?.titulo ?? c.clave }}
              </h3>
              <p class="text-xs text-gray-500">
                <code>{{ c.clave }}</code>
              </p>
            </div>
          </div>
        </template>

        <p class="text-sm text-gray-500 mb-4">
          {{ metadatos[c.clave]?.descripcion ?? c.descripcion }}
        </p>

        <UFormField
          :label="`Valor (${metadatos[c.clave]?.sufijo ?? 'valor'})`"
          :error="errores[c.clave] || undefined"
        >
          <div class="flex gap-2 w-full">
            <UInput
              v-model="valores[c.clave]"
              type="number"
              :min="0"
              :step="metadatos[c.clave]?.entero ? 1 : 0.01"
              class="w-full"
            />
            <UButton
              color="primary"
              icon="i-lucide-save"
              :loading="guardando === c.clave"
              @click="guardar(c)"
            />
          </div>
        </UFormField>
      </UCard>
    </div>
  </div>
</template>
