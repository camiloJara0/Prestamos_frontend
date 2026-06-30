<script setup lang="ts">
import createCliente from '~/components/Forms/createCliente.vue'
import { usePrestamosStore } from '~/stores/entities/prestamos.ts'
import { onMounted } from 'vue';

const prestamosStore = usePrestamosStore()
const { prestamos } = storeToRefs(prestamosStore)

onMounted(async() => {
    await prestamosStore.get()
    console.log(prestamosStore.value)
})
</script>

<template>
    <createCliente />
    <br>
    <UTable :data="prestamos"></UTable>
</template>