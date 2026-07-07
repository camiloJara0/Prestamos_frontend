import { ref, computed, watch, unref } from 'vue';

export function useOrdenamiento(datos = ref([]), columnas = [], noBuscarPor = []) {
    // Función para acceder a propiedades anidadas usando notación de punto
    function getNestedValue(obj, path) {
        return path.split('.').reduce((acc, key) => acc?.[key], obj);
    }
    const busqueda = ref('');
    const filtros = ref({});
    const menorAMayor = ref(true);
    const columnaOrden = ref('');
    const indicePorColumna = ref({});
    const indiceBusquedaGlobal = ref([]);
    const cacheOrdenes = {};

    columnas.forEach(col => {
        filtros.value[col.columna] = col.value ?? '';  // si existe col.value lo asigna
    });

    watch(datos, (nuevosDatos) => {
        // Reindexar cada vez que cambian los datos
        if (!nuevosDatos || nuevosDatos.length === 0) return;

        // Índices hash para filtros categóricos - soportan propiedades anidadas
        const indiceTemp = {};
        const indiceGlobalTemp = {};

        for (const item of nuevosDatos) {
            // Indexar todas las propiedades del item
            for (const [col, valor] of Object.entries(item)) {
                if (!indiceTemp[col]) indiceTemp[col] = {};
                const val = String(valor).toLowerCase();
                if (!indiceTemp[col][val]) indiceTemp[col][val] = [];
                indiceTemp[col][val].push(item);

                // --- Índice global (palabras clave) ---
                const palabras = val.split(/\s+/); // separar por espacios
                for (const palabra of palabras) {
                    if (!indiceGlobalTemp[palabra]) indiceGlobalTemp[palabra] = [];
                    indiceGlobalTemp[palabra].push(item);
                }
            }

            // Indexar también las propiedades anidadas definidas en columnas
            for (const col of columnas) {
                const columnaReal = col.columnaReal || col.columna;
                if (columnaReal.includes('.')) {
                    const valor = getNestedValue(item, columnaReal);
                    if (valor !== null && valor !== undefined) {
                        if (!indiceTemp[columnaReal]) indiceTemp[columnaReal] = {};
                        const val = String(valor).toLowerCase();
                        if (!indiceTemp[columnaReal][val]) indiceTemp[columnaReal][val] = [];
                        indiceTemp[columnaReal][val].push(item);

                        // --- Índice global para propiedades anidadas ---
                        const palabras = val.split(/\s+/);
                        for (const palabra of palabras) {
                            if (!indiceGlobalTemp[palabra]) indiceGlobalTemp[palabra] = [];
                            indiceGlobalTemp[palabra].push(item);
                        }
                    }
                }
            }
        }
        indicePorColumna.value = indiceTemp;
        indiceBusquedaGlobal.value = indiceGlobalTemp;

        // Limpiar cache de ordenamientos
        Object.keys(cacheOrdenes).forEach(k => delete cacheOrdenes[k]);
    }, { immediate: true });

    const sortedItems = (nombreColumna) => {
        if (columnaOrden.value === nombreColumna) {
            menorAMayor.value = !menorAMayor.value;
        } else {
            columnaOrden.value = nombreColumna;
            menorAMayor.value = false;
        }

    };

    const datosOrdenados = computed(() => {
        let resultado = [...unref(datos)];

        // Datos por busqueda Global de datos
        if (busqueda.value.trim() !== '') {
            columnaOrden.value = '';
            menorAMayor.value = true;
            Object.keys(cacheOrdenes).forEach(k => delete cacheOrdenes[k]);
            const termino = busqueda.value.trim().toLowerCase();
            resultado = resultado.filter(item => {
                // Buscar en propiedades simples
                let encontrado = Object.entries(item).some(([key, valor]) =>
                    !noBuscarPor?.includes(key) &&
                    String(valor).toLowerCase().includes(termino)
                );

                // Buscar en propiedades anidadas definidas en columnas
                if (!encontrado) {
                    encontrado = columnas.some(col => {
                        const columnaReal = col.columnaReal || col.columna;
                        if (columnaReal.includes('.')) {
                            const valor = getNestedValue(item, columnaReal);
                            return valor && String(valor).toLowerCase().includes(termino);
                        }
                        return false;
                    });
                }

                return encontrado;
            });
        }

        // Datos por filtros en columnas
        const filtroFecha = { mes: null, año: null };

        for (const [columna, valorFiltro] of Object.entries(filtros.value)) {
            if (valorFiltro && valorFiltro !== "" && valorFiltro !== "all") {
                columnaOrden.value = '';
                menorAMayor.value = true;
                Object.keys(cacheOrdenes).forEach(k => delete cacheOrdenes[k]);
                const colDef = columnas.find(c => c.columna === columna);
                const columnaReal = colDef?.columnaReal || columna;

                if (colDef?.tipo === 'mes') {
                    filtroFecha.mes = Number(valorFiltro);
                } else if (colDef?.tipo === 'año') {
                    filtroFecha.año = Number(valorFiltro);
                } else {
                    // Soportar propiedades anidadas
                    if (columnaReal.includes('.')) {
                        resultado = resultado.filter(item => {
                            const valor = getNestedValue(item, columnaReal);
                            return valor && String(valor).toLowerCase() === String(valorFiltro).toLowerCase();
                        });
                    } else {
                        const val = String(valorFiltro).toLowerCase();
                        const indiceCol = indicePorColumna.value[columnaReal];
                        if (indiceCol && indiceCol[val]) {
                            resultado = resultado.filter(item => indiceCol[val].includes(item));
                        } else {
                            resultado = [];
                        }
                    }
                }
            }
        }


        // Aplicar filtro combinado de fecha
        if (filtroFecha.mes || filtroFecha.año) {
            resultado = resultado.filter(item => {
                const colDef = columnas.find(c => c.tipo === 'mes' || c.tipo === 'año');
                const columnaReal = colDef?.columnaReal || 'fecha';
                const fechaValue = getNestedValue(item, columnaReal);
                const fecha = new Date(fechaValue + "T00:00:00");
                const mes = fecha.getMonth() + 1;
                const año = fecha.getFullYear();

                if (filtroFecha.mes && filtroFecha.año) {
                    return mes === filtroFecha.mes && año === filtroFecha.año;
                } else if (filtroFecha.mes) {
                    return mes === filtroFecha.mes;
                } else if (filtroFecha.año) {
                    return año === filtroFecha.año;
                }
            });
        }

        // Datos menor a mayor - mayor a menor con cache
        if (columnaOrden.value) {
            const key = `${columnaOrden.value}_${menorAMayor.value ? "asc" : "desc"}`;
            if (!cacheOrdenes[key]) {
                cacheOrdenes[key] = [...resultado].sort((a, b) => {
                    // Soportar propiedades anidadas
                    const valorA = columnaOrden.value.includes('.') 
                        ? getNestedValue(a, columnaOrden.value)
                        : a[columnaOrden.value];
                    const valorB = columnaOrden.value.includes('.') 
                        ? getNestedValue(b, columnaOrden.value)
                        : b[columnaOrden.value];

                    if (typeof valorA === "number" && typeof valorB === "number") {
                        return menorAMayor.value ? valorA - valorB : valorB - valorA;
                    } else {
                        return menorAMayor.value
                            ? String(valorA).localeCompare(String(valorB))
                            : String(valorB).localeCompare(String(valorA));
                    }
                });
            }
            resultado = cacheOrdenes[key];
        }

        return resultado;
    });

    // Generar opciones por datos no repetidos de columna a filtrar
    const filtrosConOpciones = computed(() => {
        return columnas.map(col => {
            const columnaReal = col.columnaReal || col.columna;

            if (col.tipo === 'mes') {
                const meses = [
                    { label: 'Enero', value: 1 },
                    { label: 'Febrero', value: 2 },
                    { label: 'Marzo', value: 3 },
                    { label: 'Abril', value: 4 },
                    { label: 'Mayo', value: 5 },
                    { label: 'Junio', value: 6 },
                    { label: 'Julio', value: 7 },
                    { label: 'Agosto', value: 8 },
                    { label: 'Septiembre', value: 9 },
                    { label: 'Octubre', value: 10 },
                    { label: 'Noviembre', value: 11 },
                    { label: 'Diciembre', value: 12 }
                ];
                return { ...col, datos: meses };
            } else if (col.tipo === 'año') {
                const añosUnicos = [
                    ...new Set(
                        unref(datos)
                            .map(d => {
                                const fecha = getNestedValue(d, columnaReal);
                                if (!fecha) return null;
                                const parsed = new Date(fecha);
                                return isNaN(parsed) ? null : parsed.getFullYear();
                            })
                            .filter(v => v !== null)
                    )
                ];
                return {
                    ...col,
                    datos: añosUnicos.map(a => ({ label: String(a), value: a }))
                };
            } else {
                const valoresUnicos = [
                    ...new Set(unref(datos).map(d => getNestedValue(d, columnaReal)).filter(v => v !== null && v !== undefined))
                ];
                return {
                    ...col,
                    datos: valoresUnicos.map(v => ({ label: v, value: v }))
                };
            }
        });
    });

    const borrarFiltros = () => {
        busqueda.value = ''
        filtros.value = {}
        menorAMayor.value = true;
        columnaOrden.value = '';
        Object.keys(cacheOrdenes).forEach(k => delete cacheOrdenes[k]); // limpiar cache
    }

    return {
        busqueda,
        filtros,
        filtrosConOpciones,
        sortedItems,
        datosOrdenados,
        columnaOrden,
        menorAMayor,
        borrarFiltros
    };
}