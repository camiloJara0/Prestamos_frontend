<script setup>
import { useClienteStore } from '~/stores/pages/clientes'
import { onMounted, computed } from 'vue'
import { useClientesActions } from '~/composables/pages/clientes'

const clienteStore = useClienteStore()
const { clientes } = storeToRefs(clienteStore)

const {
  columns,
  agregarCliente
} = useClientesActions()

onMounted(async () => {
  await clienteStore.get()
  console.log(clientes.value)
})

const propiedadesTabla = computed(() => {
  return {
    titulo: 'Gestión de Clientes',
    agregar: agregarCliente,
    data: clientes,
    columns: columns,
    filtros: [
      { columna: 'estado', placeholder: 'Estado' }
    ]
  }
})
</script>

<template>
  <LayoutTable :Propiedades="propiedadesTabla" />
</template>
