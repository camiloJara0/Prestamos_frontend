<script setup lang="ts">
import { z } from 'zod'
import { forgotPassword } from '~/services/api/auth'

definePageMeta({
  layout: 'auth',
  middleware: 'guest'
})

const toast = useToast()

const email = ref('')
const enviando = ref(false)
const enviado = ref(false)
const errorForm = ref<string | null>(null)

const schema = z.object({
  email: z.string().email('Ingresa un email válido')
})

async function solicitar() {
  errorForm.value = null
  const resultado = schema.safeParse({ email: email.value })
  if (!resultado.success) {
    errorForm.value = resultado.error.issues[0]?.message ?? 'Revise el email'
    return
  }
  enviando.value = true
  try {
    await forgotPassword(email.value)
    enviado.value = true
    toast.add({ title: 'Solicitud registrada', color: 'success' })
  } catch (e) {
    errorForm.value = (e as { detail: string }).detail || 'No se pudo procesar la solicitud.'
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
        Recuperar contraseña
      </h2>
      <p class="text-sm text-purple-200/70">
        Te enviaremos un enlace temporal por correo
      </p>
    </div>

    <UAlert
      v-if="errorForm"
      class="mb-5"
      color="error"
      :title="errorForm"
    />

    <UAlert
      v-if="enviado"
      class="mb-5"
      color="success"
      icon="i-lucide-mail-check"
      title="Si el correo existe en el sistema, recibirás un enlace para restablecer tu contraseña."
      description="El enlace vence en 1 hora y solo puede usarse una vez."
    />

    <form
      v-if="!enviado"
      class="space-y-5"
      @submit.prevent="solicitar"
    >
      <UFormField label="Email">
        <UInput
          v-model="email"
          type="email"
          placeholder="tu@email.com"
          icon="i-lucide-mail"
          autocomplete="email"
          size="lg"
          :ui="{ root: 'w-full' }"
        />
      </UFormField>
      <UButton
        type="submit"
        block
        color="primary"
        size="lg"
        icon="i-lucide-send"
        :loading="enviando"
      >
        Enviar enlace
      </UButton>
    </form>

    <div class="mt-6 text-center">
      <NuxtLink
        to="/login"
        class="text-sm text-purple-200/80 hover:text-white"
      >
        ← Volver a iniciar sesión
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
