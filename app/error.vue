<script setup lang="ts">
interface Props {
  clear?: (error: { statusCode: number, message: string }) => void
  error?: { statusCode: number, message: string } | null
}

defineProps<Props>()

const router = useRouter()
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100 dark:bg-gray-950 p-6">
    <UCard class="max-w-md w-full text-center">
      <div class="flex flex-col items-center gap-4 py-4">
        <div class="bg-purple-100 dark:bg-purple-900/40 w-16 h-16 rounded-2xl flex items-center justify-center">
          <UIcon
            name="i-lucide-alert-triangle"
            class="text-purple-600 dark:text-purple-300 text-3xl"
          />
        </div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
          {{ error?.statusCode === 404 ? 'Página no encontrada' : 'Algo salió mal' }}
        </h1>
        <p class="text-gray-500 dark:text-gray-400">
          {{ error?.statusCode === 404
            ? 'La página que buscas no existe o fue movida.'
            : 'Ocurrió un error inesperado. Intenta nuevamente o vuelve al inicio.' }}
        </p>
        <div class="flex gap-3 mt-2">
          <UButton
            color="primary"
            variant="solid"
            icon="i-lucide-home"
            @click="() => { router.push('/') }"
          >
            Volver al inicio
          </UButton>
          <UButton
            color="neutral"
            variant="outline"
            icon="i-lucide-refresh-cw"
            @click="clear?.($event as any)"
          >
            Reintentar
          </UButton>
        </div>
      </div>
    </UCard>
  </div>
</template>
