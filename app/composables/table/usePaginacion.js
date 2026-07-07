import { ref, computed } from 'vue';

export function usePaginacion(datos = ref([]), itemsPorPaginaDefault = 10) {
    const paginaActual = ref(1);
    const itemsPorPagina = ref(itemsPorPaginaDefault);

    const totalPaginas = computed(() => {
        const arrayDatos = datos?.value ?? [];
        return Math.ceil(arrayDatos.length / itemsPorPagina.value)
    });

    const cambiarItemsPorPagina = (nuevoValor) => {
        itemsPorPagina.value = parseInt(nuevoValor);
        paginaActual.value = 1;
    };

    const siguientePagina = () => {
        if (paginaActual.value < totalPaginas.value) {
            paginaActual.value++;
        }
    };

    const paginaAnterior = () => {
        if (paginaActual.value > 1) {
            paginaActual.value--;
        }
    };

    const irAPagina = (pagina) => {
        paginaActual.value = pagina;
    }

    const ultimaPagina = computed(() => itemsPorPagina.value * paginaActual.value);

    const datosPaginados = computed(() => {
        const inicio = (paginaActual.value - 1) * itemsPorPagina.value;
        const fin = inicio + itemsPorPagina.value;
        return datos.value.slice(inicio, fin);
    });

    return {
        paginaActual,
        itemsPorPagina,
        totalPaginas,
        ultimaPagina,
        cambiarItemsPorPagina,
        siguientePagina,
        paginaAnterior,
        irAPagina,
        datosPaginados,
    };
}