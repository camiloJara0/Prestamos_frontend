<script setup lang="ts">
const props = defineProps<{
  data: { label: string, value: number, color: string }[]
  size?: number
}>()

const total = computed(() => props.data.reduce((sum, d) => sum + d.value, 0))

const conicGradient = computed(() => {
  if (total.value === 0) return 'conic-gradient(#374151 0% 100%)'
  let accumulated = 0
  const stops: string[] = []
  for (const item of props.data) {
    const start = (accumulated / total.value) * 100
    accumulated += item.value
    const end = (accumulated / total.value) * 100
    stops.push(`${item.color} ${start}% ${end}%`)
  }
  return `conic-gradient(${stops.join(', ')})`
})
</script>

<template>
  <div class="flex items-center gap-4">
    <div
      class="rounded-full shrink-0"
      :style="{
        width: `${size ?? 140}px`,
        height: `${size ?? 140}px`,
        background: conicGradient
      }"
    />
    <div class="flex flex-col gap-1.5">
      <div
        v-for="item in data"
        :key="item.label"
        class="flex items-center gap-2 text-sm"
      >
        <span
          class="w-2.5 h-2.5 rounded-full shrink-0"
          :style="{ backgroundColor: item.color }"
        />
        <span class="text-gray-600">{{ item.label }}</span>
        <span class="font-medium ml-auto">{{ item.value }}</span>
      </div>
    </div>
  </div>
</template>
