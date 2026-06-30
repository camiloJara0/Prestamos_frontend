<script setup>
import { useClienteStore } from '~/stores/entities/clientes';
import { onMounted } from 'vue';
import createCliente from '~/components/Forms/createCliente.vue'

const clienteStore = useClienteStore()
const { clientes } = storeToRefs(clienteStore)

onMounted(async() => {
    await clienteStore.get()
    console.log(clientes.value)
})
</script>

<template>
    <createCliente/>
    <br>
    <UTable :data="clientes"></UTable>
</template>

<style scoped>
body {
    background-color: #000000 !important;
}
</style>