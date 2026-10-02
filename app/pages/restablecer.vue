<script setup lang="ts">
import { z } from 'zod'
import { resetPassword } from '~/services/api/auth'

definePageMeta({
  layout: 'auth',
  middleware: 'guest'
})

const route = useRoute()
const toast = useToast()

const token = computed(() => String(route.query.token ?? ''))

const password = ref('')
const confirmacion = ref('')
const enviando = ref(false)
const restablecido = ref(false)
const errorForm = ref<string | null>(null)

const schema = z.object({
  password: z.string().min(6, 'La contraseña debe tener al menos 6 caracteres'),
  confirmacion: z.string().min(6, 'La contraseña debe tener al menos 6 caracteres')
}).refine(d => d.password === d.confirmacion, {
  message: 'Las contraseñas no coinciden',
  path: ['confirmacion']
})

async function guardar() {
  errorForm.value = null
  if (!token.value) {
    errorForm.value = 'El enlace no es válido. Solicita uno nuevo.'
    return
  }
  const resultado = schema.safeParse({ password: password.value, confirmacion: confirmacion.value })
  if (!resultado.success) {
    errorForm.value = resultado.error.issues[0]?.message ?? 'Revise las contraseñas'
    return
  }
  enviando.value = true
  try {
    await resetPassword(token.value, password.value)
    restablecido.value = true
    toast.add({ title: 'Contraseña restablecida', color: 'success' })
  } catch (e) {
    errorForm.value = (e as { detail: string }).detail || 'No se pudo restablecer la contraseña. El enlace puede haber expirado.'
  } finally {
    enviando.value = false
  }
}
</script>

<template>
  <div class="glass w-full max-w-xl rounded-3xl p-8 shadow-2xl">
    <div class="flex flex-col items-center gap-3 mb-8">
      <div class="w-16 h-16 rounded-2xl bg-white/15 flex items-center justify-center backdrop-blur-sm">
        <AppLogo />
      </div>
      <h2 class="text-2xl font-bold text-white font-display">
        Nueva contraseña
      </h2>
      <p class="text-sm text-purple-200/70">
        El enlace solo puede usarse una vez
      </p>
    </div>

    <UAlert
      v-if="errorForm"
      class="mb-5"
      color="error"
      :title="errorForm"
    />

    <UAlert
      v-if="restablecido"
      class="mb-5"
      color="success"
      icon="i-lucide-check-circle"
      title="Contraseña actualizada correctamente"
      description="Ya puedes iniciar sesión con tu nueva contraseña."
    />

    <form
      v-if="!restablecido"
      class="space-y-5"
      @submit.prevent="guardar"
    >
      <UFormField
        label="Nueva contraseña"
        :error="errorForm && !token ? errorForm : undefined"
      >
        <UInput
          v-model="password"
          type="password"
          placeholder="••••••"
          icon="i-lucide-lock"
          autocomplete="new-password"
          size="lg"
          :ui="{ root: 'w-full' }"
        />
      </UFormField>
      <UFormField label="Confirmar contraseña">
        <UInput
          v-model="confirmacion"
          type="password"
          placeholder="••••••"
          icon="i-lucide-lock"
          autocomplete="new-password"
          size="lg"
          :ui="{ root: 'w-full' }"
        />
      </UFormField>
      <UButton
        type="submit"
        block
        color="primary"
        size="lg"
        icon="i-lucide-save"
        :loading="enviando"
      >
        Restablecer contraseña
      </UButton>
    </form>

    <div class="mt-6 text-center">
      <NuxtLink
        to="/login"
        class="text-sm text-purple-200/80 hover:text-white"
      >
        {{ restablecido ? 'Ir a iniciar sesión' : '← Volver a iniciar sesión' }}
      </NuxtLink>
    </div>
  </div>
</template>

<style scoped>
.glass {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.12);
}
</style>
