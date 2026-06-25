<script setup>
import { useClienteStore } from '~/stores/entities/clientes';
import { onMounted } from 'vue';

const clienteStore = useClienteStore()
const { clientes } = storeToRefs(clienteStore)

onMounted(async() => {
    await clienteStore.get()
    console.log(clientes.value)
})
</script>

<template>
    <UTable :data="clientes"></UTable>
</template>