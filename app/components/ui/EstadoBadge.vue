<script setup lang="ts">
type Entidad = 'prestamo' | 'cuota' | 'cliente' | 'tipo' | 'tipoPrestamo' | 'tipoPago' | 'usuario'
type ColorBadge = 'primary' | 'secondary' | 'success' | 'info' | 'warning' | 'error' | 'neutral'

const props = withDefaults(defineProps<{
  entidad?: Entidad
  estado: string
}>(), {
  entidad: 'prestamo'
})

const MAP: Record<Entidad, Record<string, { color: ColorBadge, label?: string }>> = {
  prestamo: {
    activo: { color: 'info' },
    pagado: { color: 'success' },
    perdido: { color: 'error' },
    renovado: { color: 'neutral' }
  },
  cuota: {
    pendiente: { color: 'neutral' },
    pagado: { color: 'success' },
    vencido: { color: 'error' },
    parcial: { color: 'warning' }
  },
  cliente: {
    activo: { color: 'success' },
    inactivo: { color: 'neutral' }
  },
  tipo: {
    activo: { color: 'success' },
    inactivo: { color: 'neutral' }
  },
  tipoPrestamo: {
    activo: { color: 'success' },
    inactivo: { color: 'neutral' }
  },
  tipoPago: {
    activo: { color: 'success' },
    inactivo: { color: 'neutral' }
  },
  usuario: {
    activo: { color: 'success' },
    inactivo: { color: 'neutral' }
  }
}

const conf = computed<{ color: ColorBadge, label?: string }>(() =>
  MAP[props.entidad]?.[props.estado] ?? { color: 'neutral' }
)
const label = computed(() => conf.value.label ?? props.estado)
</script>

<template>
  <UBadge
    :color="conf.color"
    variant="subtle"
    class="capitalize"
  >
    {{ label }}
  </UBadge>
</template>
