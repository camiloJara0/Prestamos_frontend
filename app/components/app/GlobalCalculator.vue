<script setup lang="ts">
const props = defineProps<{
  open: boolean
}>()

const emit = defineEmits<{
  'update:open': [value: boolean]
}>()

const isOpen = computed({
  get: () => props.open,
  set: v => emit('update:open', v)
})

const display = ref('0')
const operador = ref<string | null>(null)
const valorAnterior = ref<string | null>(null)
const resetPantalla = ref(false)

function ingresarDigito(digito: string) {
  if (resetPantalla.value) {
    display.value = digito === '.' ? '0.' : digito
    resetPantalla.value = false
    return
  }
  if (digito === '.' && display.value.includes('.')) return
  if (display.value === '0' && digito !== '.') {
    display.value = digito
  } else {
    display.value += digito
  }
}

function ingresarOperador(op: string) {
  calcular()
  valorAnterior.value = display.value
  operador.value = op
  resetPantalla.value = true
}

function calcular() {
  if (operador.value == null || valorAnterior.value == null) return
  const a = parseFloat(valorAnterior.value)
  const b = parseFloat(display.value)
  let resultado: number

  switch (operador.value) {
    case '+':
      resultado = a + b
      break
    case '-':
      resultado = a - b
      break
    case '×':
      resultado = a * b
      break
    case '÷':
      resultado = b === 0 ? NaN : a / b
      break
    default:
      return
  }

  display.value = Number.isNaN(resultado) ? 'Error' : String(Math.round(resultado * 1e10) / 1e10)
  operador.value = null
  valorAnterior.value = null
  resetPantalla.value = true
}

function limpiar() {
  display.value = '0'
  operador.value = null
  valorAnterior.value = null
  resetPantalla.value = false
}

function borrarUltimo() {
  if (resetPantalla.value) return
  display.value = display.value.length > 1 ? display.value.slice(0, -1) : '0'
}

function signo() {
  if (display.value === '0' || display.value === 'Error') return
  display.value = display.value.startsWith('-') ? display.value.slice(1) : '-' + display.value
}

function porcentaje() {
  const valor = parseFloat(display.value)
  if (!Number.isNaN(valor)) {
    display.value = String(valor / 100)
  }
}

const esOperador = (op: string) => operador.value === op

function onKeydown(e: KeyboardEvent) {
  if (!isOpen.value) return
  if (e.key >= '0' && e.key <= '9') {
    ingresarDigito(e.key)
    return
  }
  if (e.key === '.') {
    ingresarDigito('.')
    return
  }
  if (e.key === '+') {
    ingresarOperador('+')
    return
  }
  if (e.key === '-') {
    ingresarOperador('-')
    return
  }
  if (e.key === '*') {
    ingresarOperador('×')
    return
  }
  if (e.key === '/') {
    e.preventDefault()
    ingresarOperador('÷')
    return
  }
  if (e.key === 'Enter' || e.key === '=') {
    calcular()
    return
  }
  if (e.key === 'Escape') {
    limpiar()
    isOpen.value = false
    return
  }
  if (e.key === 'Backspace') {
    borrarUltimo()
    return
  }
}

if (import.meta.client) {
  window.addEventListener('keydown', onKeydown)
  onUnmounted(() => window.removeEventListener('keydown', onKeydown))
}
</script>

<template>
  <UModal
    :open="isOpen"
    @update:open="isOpen = $event"
  >
    <template #title>
      Calculadora
    </template>
    <template #body>
      <div class="space-y-3">
        <div class="bg-gray-100 dark:bg-gray-800 rounded-lg p-4 text-right">
          <div class="text-xs text-gray-400 h-4">
            {{ valorAnterior }} {{ operador }}
          </div>
          <div class="text-3xl font-mono font-bold truncate">
            {{ display }}
          </div>
        </div>

        <div class="grid grid-cols-4 gap-2">
          <UButton
            label="C"
            color="neutral"
            variant="outline"
            @click="limpiar"
          />
          <UButton
            label="%"
            color="neutral"
            variant="outline"
            @click="porcentaje"
          />
          <UButton
            label="⌫"
            color="neutral"
            variant="outline"
            @click="borrarUltimo"
          />
          <UButton
            label="÷"
            :color="esOperador('÷') ? 'primary' : 'neutral'"
            :variant="esOperador('÷') ? 'solid' : 'outline'"
            @click="ingresarOperador('÷')"
          />

          <UButton
            label="7"
            color="neutral"
            variant="ghost"
            @click="ingresarDigito('7')"
          />
          <UButton
            label="8"
            color="neutral"
            variant="ghost"
            @click="ingresarDigito('8')"
          />
          <UButton
            label="9"
            color="neutral"
            variant="ghost"
            @click="ingresarDigito('9')"
          />
          <UButton
            label="×"
            :color="esOperador('×') ? 'primary' : 'neutral'"
            :variant="esOperador('×') ? 'solid' : 'outline'"
            @click="ingresarOperador('×')"
          />

          <UButton
            label="4"
            color="neutral"
            variant="ghost"
            @click="ingresarDigito('4')"
          />
          <UButton
            label="5"
            color="neutral"
            variant="ghost"
            @click="ingresarDigito('5')"
          />
          <UButton
            label="6"
            color="neutral"
            variant="ghost"
            @click="ingresarDigito('6')"
          />
          <UButton
            label="-"
            :color="esOperador('-') ? 'primary' : 'neutral'"
            :variant="esOperador('-') ? 'solid' : 'outline'"
            @click="ingresarOperador('-')"
          />

          <UButton
            label="1"
            color="neutral"
            variant="ghost"
            @click="ingresarDigito('1')"
          />
          <UButton
            label="2"
            color="neutral"
            variant="ghost"
            @click="ingresarDigito('2')"
          />
          <UButton
            label="3"
            color="neutral"
            variant="ghost"
            @click="ingresarDigito('3')"
          />
          <UButton
            label="+"
            :color="esOperador('+') ? 'primary' : 'neutral'"
            :variant="esOperador('+') ? 'solid' : 'outline'"
            @click="ingresarOperador('+')"
          />

          <UButton
            label="±"
            color="neutral"
            variant="ghost"
            @click="signo"
          />
          <UButton
            label="0"
            color="neutral"
            variant="ghost"
            @click="ingresarDigito('0')"
          />
          <UButton
            label="."
            color="neutral"
            variant="ghost"
            @click="ingresarDigito('.')"
          />
          <UButton
            label="="
            color="primary"
            @click="calcular"
          />
        </div>
      </div>
    </template>
  </UModal>
</template>
