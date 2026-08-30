<script setup lang="ts">
import type { PrestamoCreate } from '#shared/types/prestamo'
import { useClientes } from '~/composables/domain/useClientes'
import { useTiposPrestamo } from '~/composables/domain/useTipos'
import { useCapital } from '~/composables/domain/useCapital'
import { usePrestamos } from '~/composables/domain/usePrestamos'
import PrestamoForm from '~/components/prestamos/PrestamoForm.vue'

definePageMeta({
  middleware: 'auth'
})

const router = useRouter()
const toast = useToast()

const { clientes, fetch: fetchClientes } = useClientes()
const { tipos, fetch: fetchTipos } = useTiposPrestamo()
const { capital, fetch: fetchCapital } = useCapital()
const { crear } = usePrestamos()

const enviando = ref(false)
const formRef = ref<{ submit: () => void } | null>(null)

async function inicializar() {
  await Promise.all([fetchClientes(), fetchTipos(), fetchCapital()])
}
inicializar()

async function guardar(data: PrestamoCreate) {
  enviando.value = true
  try {
    const prestamo = await crear(data)
    toast.add({ title: 'Préstamo creado correctamente', color: 'success' })
    await fetchCapital()
    router.push(`/prestamos/${prestamo.id}`)
  } catch (e) {
    const err = e as { status: number, detail: string }
    if (err.status === 400 && /capital insuficiente/i.test(err.detail)) {
      toast.add({ title: 'Capital insuficiente para otorgar el préstamo', color: 'error' })
    } else {
      toast.add({ title: err.detail || 'No se pudo crear el préstamo', color: 'error' })
    }
  } finally {
    enviando.value = false
  }
}
</script>

<template>
  <div class="p-6 space-y-4">
    <div>
      <h1 class="text-2xl font-bold">
        Nuevo préstamo
      </h1>
      <p class="text-sm text-gray-500">
        La calculadora en vivo replica las fórmulas del backend.
      </p>
    </div>

    <UCard>
      <template #header>
        <div class="flex items-center justify-between">
          <h3 class="font-bold">
            Datos del préstamo
          </h3>
          <span class="text-sm text-gray-500">
            Capital disponible:
            <span class="font-semibold text-(--color-primary-600)">
              {{ formatoMoneda(capital?.monto_total ?? 0) }}
            </span>
          </span>
        </div>
      </template>

      <PrestamoForm
        ref="formRef"
        :clientes="clientes"
        :tipos-prestamo="tipos"
        :capital-disponible="capital?.monto_total ?? 0"
        @guardar="guardar"
      />

      <template #footer>
        <div class="flex justify-end gap-2">
          <UButton
            label="Cancelar"
            color="neutral"
            variant="outline"
            :disabled="enviando"
            @click="router.back()"
          />
          <UButton
            label="Crear préstamo"
            color="primary"
            icon="i-lucide-hand-coins"
            :loading="enviando"
            @click="formRef?.submit()"
          />
        </div>
      </template>
    </UCard>
  </div>
</template>
