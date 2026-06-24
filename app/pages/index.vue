<script setup lang="ts">
import { ref } from 'vue';

definePageMeta({
  layout: 'login'
})

const login = useLogin()
const mail = ref('')
const password = ref('')
</script>

<template>
  <div class="bg-white h-screen w-[70vh]">
    <div class="w-full h-full flex flex-col items-center justify-center p-10 gap-10">
      <div class="flex flex-col items-center gap-3">
        <div class="bg-purple-100 w-20 h-20 rounded-full flex justify-center items-center">
          <UIcon name="i-lucide-user" class="text-white text-3xl"></UIcon>
        </div>
        <h2 class="text-2xl font-bold text-gray-900">Inicia Sesion</h2>
        <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Repellendus corporis fugiat voluptatibus aut corrupti
        </p>
      </div>
      <div class="flex flex-col gap-3">
        <UInput v-model="mail" placeholder="Admin@mail.com" icon="i-lucide-mail" class="bg-purple-500 w-full"></UInput>
        <UInput v-model="password" placeholder="password" icon="i-lucide-lock" class="bg-purple-500 w-full"></UInput>
        <UButton color="primary" variant="solid" @click="login.enviarLogin(mail, password)">Ingresar</UButton>
      </div>
    </div>
  </div>
</template>
