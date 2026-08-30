<script setup lang="ts">
import { z } from 'zod'

definePageMeta({
  layout: 'auth',
  middleware: 'guest'
})

const auth = useAuthStore()
const toast = useToast()

const email = ref('')
const password = ref('')
const enviando = ref(false)
const errorForm = ref<string | null>(null)
const errores = ref<Record<string, string>>({})

const schema = z.object({
  email: z.string().email('Ingresa un email válido'),
  password: z.string().min(6, 'La contraseña debe tener al menos 6 caracteres')
})

function validar() {
  const resultado = schema.safeParse({ email: email.value, password: password.value })
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

async function ingresar() {
  errorForm.value = null
  if (!validar()) return
  enviando.value = true
  try {
    await auth.login(email.value, password.value)
    toast.add({ title: 'Bienvenido', color: 'success' })
    await navigateTo('/')
  } catch (e) {
    const err = e as { status: number, detail: string }
    if (err.status === 401) {
      errorForm.value = 'Email o contraseña incorrectos'
    } else {
      errorForm.value = err.detail || 'No se pudo iniciar sesión. Intenta nuevamente.'
    }
  } finally {
    enviando.value = false
  }
}
</script>

<template>
  <div class="glass w-full max-w-xl rounded-2xl p-8 shadow-2xl">
    <div class="flex flex-col items-center gap-2 mb-6">
      <div class="w-14 h-14 rounded-2xl bg-white/15 flex items-center justify-center backdrop-blur-sm">
        <AppLogo />
      </div>
      <h2 class="text-2xl font-bold text-white">
        Inicia sesión
      </h2>
      <p class="text-sm text-purple-200/80">
        LoanSoft · Gestión de Préstamos
      </p>
    </div>

    <UAlert
      v-if="errorForm"
      class="mb-4"
      color="error"
      :title="errorForm"
    />

    <form
      class="space-y-4"
      @submit.prevent="ingresar"
    >
      <UFormField
        label="Email"
        :error="errores.email"
      >
        <UInput
          v-model="email"
          type="email"
          placeholder="admin@test.com"
          icon="i-lucide-mail"
          autocomplete="email"
          :ui="{ root: 'w-full' }"
        />
      </UFormField>
      <UFormField
        label="Contraseña"
        :error="errores.password"
      >
        <UInput
          v-model="password"
          type="password"
          placeholder="••••••"
          icon="i-lucide-lock"
          autocomplete="current-password"
          :ui="{ root: 'w-full' }"
        />
      </UFormField>
      <UButton
        type="submit"
        block
        color="primary"
        size="lg"
        icon="i-lucide-log-in"
        :loading="enviando"
      >
        Ingresar
      </UButton>
    </form>
  </div>
</template>

<style scoped>
.glass {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(14px);
  border: 1px solid rgba(255, 255, 255, 0.18);
}
</style>
