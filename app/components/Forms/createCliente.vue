<script setup>
const state = reactive({
  email: '',
  password: ''
})
</script>

<template>


    <h1>Prestamos</h1>
  <UModal
    title="Modal with description"
    description="Lorem ipsum dolor sit amet, consectetur adipiscing elit."
  >
    <UButton label="Crear cliente" color="primary" variant="subtle" />

    <template #body>
      <Placeholder class="h-48" />

        <UForm class="space-y-4">
    <UFormField label="Email" name="email">
      <UInput v-model="state.email" />
    </UFormField>

    <UFormField label="Password" name="password">
      <UInput v-model="state.password" type="password" />
    </UFormField>

    <UButton type="submit">
      Submit
    </UButton>
  </UForm>
    </template>
  </UModal>
</template>

