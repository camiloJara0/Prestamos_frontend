<template>
    <!-- Color de fondo gradient -->
    <div class="bg-linear-to-r from-(--color-default) to-(--color-default-400) absolute inset-0 z-0"></div>
    <!-- Imagen de fondo -->
    <div class="bg-[url('/assets/img/fondo.png')] bg-cover bg-center absolute inset-0 z-10 opacity-50"></div>
    <!-- Imagen sombra-->
    <!-- <div class="bg-[rgba(0,0,0,0.9)] absolute inset-0 z-20"></div> -->


    <div class="containerAuthentication relative z-30 flex flex-col justify-center items-start">
        <slot></slot>
    </div>
</template>