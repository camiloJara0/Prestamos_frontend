<script setup>
import '~/assets/css/main.css'

useHead({
  htmlAttrs: {
    lang: 'es'
  },
  meta: [
    { name: 'viewport', content: 'width=device-width, initial-scale=1' },
    { name: 'theme-color', content: '#7c3aed' }
  ],
  link: [
    { rel: 'icon', href: '/favicon.ico' }
  ]
})

useSeoMeta({
  title: 'LoanSoft — Gestión de Préstamos',
  description: 'Sistema profesional de gestión de préstamos: clientes, cartera, pagos, moras y reportes.'
})
</script>

<template>
  <UApp>
    <NuxtLayout>
      <UMain>
        <NuxtPage />
      </UMain>
    </NuxtLayout>
  </UApp>
</template>
