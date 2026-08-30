<template>
  <div class="relative min-h-screen w-full overflow-hidden">
    <div class="bg-linear-to-br from-[#4c1d95] via-[#7c3aed] to-[#a78bfa] absolute inset-0 z-0" />
    <div
      class="absolute inset-0 z-10 opacity-20"
      style="background-image: radial-gradient(circle at 20% 20%, rgba(255,255,255,0.15) 0, transparent 40%), radial-gradient(circle at 80% 70%, rgba(255,255,255,0.12) 0, transparent 40%)"
    />
    <div class="relative z-30 flex flex-col items-center justify-center min-h-screen px-4 w-full">
      <slot />
    </div>
  </div>
</template>
