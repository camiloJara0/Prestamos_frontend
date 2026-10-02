# -*- coding: utf-8 -*-
"""Genera el Roadmap Estratégico de LoanSoft."""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from apa import Doc  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
FIGS = os.path.join(HERE, "figs")
CATALOG = json.load(open(os.path.join(HERE, "rf_catalog.json"), encoding="utf-8"))

d = Doc(
    title="**Roadmap Estratégico**",
    subtitle="Fases, iniciativas y métricas de evolución de LoanSoft",
    author=["Equipo de Ingeniería de Software · LoanSoft"],
    affiliation=["LoanSoft · Sistema de Gestión de Préstamos"],
    date=["28 de septiembre de 2026"],
    extra=["Versión 1.0",
           "Horizonte: estabilización inmediata y 12 meses de evolución"],
)

d.abstract(
    "Este documento define hacia dónde evoluciona LoanSoft después del análisis de su estado actual. "
    "Parte de un diagnóstico honesto: 33 de los 75 requerimientos funcionales están completados, 16 a "
    "medias y 26 sin iniciar. Sobre esa base organiza el trabajo en cuatro fases con objetivos, "
    "requerimientos comprometidos, indicadores de éxito y esfuerzo estimado, y añade las iniciativas "
    "transversales de calidad y plataforma que sostienen el crecimiento."
)

# ==================================================== 1
d.h1("1. Visión y propósito")
d.p(
    "LoanSoft nació como la herramienta que reemplaza el cuaderno de cobro y la hoja de cálculo en un "
    "negocio de préstamos. La visión a doce meses es que la operación completa —originación, cobro, "
    "mora, caja y reportes— ocurra dentro del sistema sin trabajo paralelo, y que los datos del "
    "negocio estén tan bien protegidos y respaldados como lo estaría su dinero."
)
d.p(
    "El roadmap existe para ordenar esa evolución. No promete fechas irreversibles ni desconocidas: "
    "cada fase se define por su objetivo y sus indicadores, de modo que cuando el negocio priorice "
    "diferente, el plan siga siendo legible y reordenable. La regla de prioridad se mantiene simple: "
    "primero lo que protege dinero y datos, después lo que completa la operación diaria, al final lo "
    "que amplía el alcance comercial del producto."
)

# ==================================================== 2
d.h1("2. Estado actual del producto")
d.p(
    "El punto de partida se midió sobre el código, no sobre la intención. De los 75 requerimientos "
    "funcionales, casi la mitad ya tiene implementación completa; el resto se divide entre requerimientos "
    "parcialmente cubiertos y requerimientos aún sin iniciar. La distribución por módulo muestra dónde "
    "conviene cerrar filas antes de abrir alcance nuevo."
)
d.table(
    "Madurez por módulo funcional",
    ["Módulo", "Requerimientos", "Completados", "Parciales", "Pendientes", "Lectura"],
    [
        ["Seguridad y acceso", "RF-001 a RF-011", "7", "3", "1", "Backend sólido; brecha crítica en la protección de rutas del frontend."],
        ["Clientes y solicitudes", "RF-012 a RF-024", "4", "1", "8", "Operación diaria cubierta; el embudo de solicitudes no existe."],
        ["Originación de préstamos", "RF-025 a RF-027", "3", "0", "0", "Módulo completo y con pruebas unitarias de cálculo."],
        ["Administración de préstamos", "RF-028 a RF-035", "6", "1", "1", "Flujos de renovación y pérdida operativos."],
        ["Pagos y cobro", "RF-036 a RF-043", "5", "1", "2", "Cobro confiable; faltan reversión y comprobante."],
        ["Mora y cobranza", "RF-044 a RF-049", "2", "2", "2", "Cálculo automático vivo; la consulta por préstamo está desconectada."],
        ["Capital, reportes y tablero", "RF-050 a RF-059", "4", "4", "2", "Reportes base listos; faltan cartera, cobranza y consolidación."],
        ["Plataforma e integraciones", "RF-060 a RF-075", "2", "4", "10", "PWA en marcha; integraciones externas sin iniciar."],
        ["Total", "75 requerimientos", "33", "16", "26", "Estado general: producto operable con deuda explícita."],
    ],
    widths=[1.8, 1.3, 0.9, 0.8, 0.9, 3.3],
    align_center_cols=(2, 3, 4),
)
d.p(
    "Los pendientes no son todos iguales. Cuatro de ellos —protección de rutas, cabeceras de "
    "seguridad, respaldo de datos y paginación consistente— son de infraestructura y determinan si el "
    "producto puede confiarse; se atienden en la primera fase. Otros corresponden a alcance comercial "
    "nuevo, como pasarela de pago, buró de crédito y firma electrónica, y esperan a que la operación "
    "base esté cerrada."
)

# ==================================================== 3
d.h1("3. Fases del roadmap")
d.p(
    "El horizonte se divide en cuatro fases. La fase 0 se ejecuta de inmediato y su alcance proviene "
    "de los hallazgos críticos del análisis; las tres siguientes se distribuyen en los doce meses "
    "siguientes. Cada fase declara qué requerimientos abarca, cuál es su objetivo, cómo se sabe que "
    "terminó y cuánto esfuerzo se estima."
)
d.table(
    "Fases, alcance e indicadores de éxito",
    ["Fase", "Horizonte", "Objetivo", "Requerimientos", "Indicador de cierre"],
    [
        ["Fase 0 · Estabilización", "Inmediato (4 a 6 semanas)",
         "Cerrar los riesgos de seguridad y continuidad detectados en el análisis.",
         "RF-008, RF-074, RF-075, RF-070",
         "Rutas privadas protegidas y probadas; cabeceras de seguridad activas; respaldo programado verificado con una restauración de prueba."],
        ["Fase 1 · Cierre operativo", "Meses 1 a 3",
         "Que la operación diaria no tenga pantallas rotas ni consultas que fallen.",
         "RF-045, RF-046, RF-047, RF-041, RF-057, RF-058, RF-014, RF-015",
         "Cero errores de recurso inexistente en mora y cobranza; historial global de pagos navegable; tablero con distribución de cartera."],
        ["Fase 2 · Control gerencial", "Meses 3 a 6",
         "Dar a la administración las herramientas de corrección y de reporte.",
         "RF-042, RF-043, RF-051, RF-059, RF-053, RF-054, RF-034, RF-035, RF-006, RF-010, RF-011",
         "Pagos reversibles con auditoría; reportes de cartera y cobranza en interfaz; recuperación de contraseña operativa."],
        ["Fase 3 · Expansión comercial", "Meses 6 a 12",
         "Ampliar el alcance del producto hacia el mercado.",
         "RF-020 a RF-024, RF-060 a RF-067, RF-073",
         "Embudo de solicitudes activo; notificaciones multicanal; integración de pagos y firma en piloto; base multiempresa evaluada."],
    ],
    widths=[1.4, 1.2, 1.9, 1.6, 3.9],
)

# ==================================================== 4
d.h1("4. Detalle por fase")
d.h2("4.1 Fase 0 · Estabilización")
d.p(
    "La fase 0 es la única que no admite negociación de alcance: nace de los hallazgos que impiden "
    "confiar en el sistema. Comprende activar la protección de rutas del frontend, que hoy está "
    "comentada y deja las pantallas administrativas sin defensa; añadir las cabeceras de seguridad "
    "sobre las respuestas HTTP y acotar el origen permitido; implementar el respaldo programado de la "
    "base de datos con un procedimiento de restauración probado; y unificar el parámetro de "
    "paginación entre frontend y backend para que los listados no pierdan registros."
)
d.p(
    "Se trabaja sobre las cinco pantallas administrativas —usuarios, tipos de préstamo, tipos de pago, "
    "capital y moras— cuya accesibilidad depende del middleware de rol. El cierre de la fase exige "
    "evidencia: una prueba de regresión de navegación con una cuenta de cada rol y una restauración "
    "completa desde el respaldo."
)
d.h2("4.2 Fase 1 · Cierre operativo")
d.p(
    "La fase 1 atiende lo que el usuario nota todos los días. Se repara la consulta de moras, cuyo "
    "servicio apunta a un prefijo distinto al del servidor y responde con error; se completa la "
    "pantalla de cobranza con los datos que hoy no se leen; se habilita el historial global de pagos "
    "con filtros de periodo y cliente; se termina la distribución de cartera y los indicadores de "
    "cobranza del tablero; y se cierra la búsqueda de clientes con su página de detalle y el "
    "historial financiero del cliente."
)
d.p(
    "La fase termina cuando el circuito cliente → préstamo → cobro → mora → tablero se puede recorrer "
    "de punta a punta sin errores de consola y sin recaer en procedimientos manuales fuera del "
    "sistema."
)
d.h2("4.3 Fase 2 · Control gerencial")
d.p(
    "La fase 2 convierte al administrador en dueño de las correcciones y de los números. Incluye la "
    "reversión de pagos con motivo y auditoría, el comprobante descargable de cada cobro, el "
    "registro de ingresos y egresos de caja, la consolidación del tablero desde el resumen del "
    "servidor, los reportes de cartera y de cobranza que ya existen sin interfaz propia, "
    "el ajuste puntual de capital y la reestructuración de préstamos, la "
    "recuperación de contraseña por correo, la auditoría visible por usuario y tabla y la "
    "configuración de parámetros de mora desde la interfaz."
)
d.p(
    "Con esta fase el negocio cierra el mes dentro del sistema: genera reportes exportables, corrige "
    "errores de captura con trazabilidad y administra sus parámetros sin intervención del equipo de "
    "desarrollo."
)
d.h2("4.4 Fase 3 · Expansión comercial")
d.p(
    "La fase 3 abre alcance nuevo. El embudo de solicitudes permite capturar la petición del cliente, "
    "evaluarla, decidirla y convertirla en préstamo sin redigitalizar; el centro de notificaciones y "
    "los canales de correo y mensajería amplían la comunicación más allá del push; la pasarela de "
    "pago habilita el cobro digital; el scoring y la firma electrónica modernizan la decisión de "
    "crédito; la importación de extractos acerca el cierre bancario al sistema; y el aislamiento por "
    "empresa prepara un modelo de varios negocios sobre la misma plataforma."
)
d.figure(os.path.join(FIGS, "fig7_microservicios.png"),
         "Arquitectura objetivo hacia la que converge la fase 3: separación del núcleo de negocio "
         "de los servicios de canales e integraciones.")
d.p(
    "Esta fase se ejecuta por pilotos: cada integración se prueba con un grupo reducido de usuarios "
    "antes de abrirse al resto, y ninguna entra en producción sin criterio de reversión definido."
)

# ==================================================== 5
d.h1("5. Calendario por trimestres")
d.p(
    "El calendario siguiente traduce las fases en trimestres de ejecución. Los rangos son intencionales "
    "y se revisan en cada trimestre; la secuencia entre fases sí es un compromiso, porque ninguna fase "
    "posterior aporta valor si la anterior no cerró."
)
d.table(
    "Calendario de ejecución por trimestre",
    ["Trimestre", "Fase dominante", "Hitos principales"],
    [
        ["T1", "Fase 0", "Protección de rutas activa, cabeceras de seguridad, respaldo verificado, paginación unificada."],
        ["T1 – T2", "Fase 1", "Mora y cobranza reparadas, historial de pagos global, tablero completo, detalle de cliente."],
        ["T2 – T3", "Fase 2", "Reversión de pagos, comprobantes, caja, reportes de cartera y cobranza, recuperación de contraseña."],
        ["T3 – T4", "Fase 3", "Solicitudes de préstamo, centro de notificaciones, pilotos de pagos y firma, evaluación multiempresa."],
    ],
    widths=[1.0, 1.6, 5.4],
)

# ==================================================== 6
d.h1("6. Iniciativas transversales")
d.p(
    "Algunas iniciativas no pertenecen a un módulo sino a la salud del producto y se ejecutan en "
    "paralelo a las fases. Su avance se mide con sus propios indicadores y su omisión compromete a "
    "todas las demás."
)
d.table(
    "Iniciativas transversales y su indicador",
    ["Iniciativa", "Qué incluye", "Indicador"],
    [
        ["Pruebas automatizadas", "Ampliar desde las pruebas unitarias de cálculo existentes hacia flujo de pagos, cuadre e idempotencia.", "Cobertura automatizada de los casos CP de dinero: 80 por ciento."],
        ["Integración continua", "Validación automática de formato, tipos y pruebas en cada cambio antes de combinarlo.", "Ningún cambio se integra sin pasar todas las validaciones."],
        ["Observabilidad", "Registro de errores del navegador y del servidor con alertas de fallo en procesos nocturnos.", "Detección de incidentes antes de que lo reporte el usuario."],
        ["Desempeño y accesibilidad", "Tiempos de respuesta en listados, contraste y navegación por teclado.", "Listados principales bajo dos segundos y revisión de accesibilidad trimestral."],
        ["Gestión de riesgo técnico", "Seguimiento de los hallazgos de auditoría con archivo, responsable y fecha.", "Descenso continuo de hallazgos abiertos en cada revisión."],
    ],
    widths=[1.7, 3.7, 2.6],
)

# ==================================================== 7
d.h1("7. Métricas del producto")
d.p(
    "El roadmap se mide con dos familias de indicadores. Las métricas de negocio dicen si el sistema "
    "está mejorando la operación real del prestamista; las métricas de producto dicen si el software "
    "está mejorando en calidad y adopción. Ambas se revisan en la misma reunión trimestral."
)
d.table(
    "Métricas de negocio y de producto",
    ["Familia", "Métrica", "Cómo se obtiene", "Dirección deseada"],
    [
        ["Negocio", "Morosidad de la cartera", "Saldo vencido frente a saldo total de la cartera.", "A la baja."],
        ["Negocio", "Tiempo medio de cobro", "Días entre vencimiento y pago efectivo.", "A la baja."],
        ["Negocio", "Capital rotativo", "Préstamos originados por período frente al capital disponible.", "A la alza con riesgo controlado."],
        ["Negocio", "Cobros registrados en el sistema", "Pagos capturados frente a cobros totales del negocio.", "Cercano al cien por ciento."],
        ["Producto", "Tasa de aprobación de casos de prueba", "Casos aprobados sobre ejecutados por sprint.", "Cien por ciento en dinero."],
        ["Producto", "Disponibilidad", "Tiempo accesible frente al tiempo total.", "99,5 por ciento o más."],
        ["Producto", "Adopción de la aplicación instalada", "Aperturas desde el acceso instalado frente al total.", "A la alza."],
        ["Producto", "Hallazgos de auditoría abiertos", "Conteo de observaciones sin resolver.", "A la baja."],
    ],
    widths=[1.0, 1.9, 3.0, 1.5],
)

# ==================================================== 8
d.h1("8. Esfuerzo estimado")
d.p(
    "Las estimaciones siguientes son de orden de magnitud, calculadas sobre el trabajo ya ejecutado y "
    "la complejidad de cada alcance. Se expresan en personas-sprint, donde un sprint equivale a dos "
    "semanas de una persona del equipo; sirven para dimensionar, no para comprometer fechas."
)
d.table(
    "Esfuerzo estimado por fase",
    ["Fase", "Personas-sprint", "Sprints equivalentes", "Observación"],
    [
        ["Fase 0 · Estabilización", "2", "2", "Trabajo concentrado y de bajo diseño, alto riesgo si se omite."],
        ["Fase 1 · Cierre operativo", "6", "6", "Reparaciones y terminación de interfaces existentes."],
        ["Fase 2 · Control gerencial", "9", "9", "Nuevos flujos de corrección, reportes y configuración."],
        ["Fase 3 · Expansión comercial", "14", "14", "Integraciones externas con pruebas de piloto."],
        ["Iniciativas transversales", "8", "8", "Distribuidas a lo largo de las cuatro fases."],
        ["Total estimado", "39", "39", "Aproximadamente dieciocho meses de una persona, o seis meses de un equipo de tres."],
    ],
    widths=[2.0, 1.3, 1.5, 3.2],
    align_center_cols=(1, 2),
)

# ==================================================== 9
d.h1("9. Riesgos y dependencias")
d.table(
    "Riesgos externos y dependencias del roadmap",
    ["Riesgo o dependencia", "Efecto posible", "Mitigación"],
    [
        ["Integraciones externas sin proveedor contratado.", "Fase 3 bloqueada parcialmente.", "Contratar alcance antes de iniciar y mantener un modo de operación sin la integración."],
        ["Regulación de protección de datos personales y financieros.", "Retrabajo de manejo de información y consentimientos.", "Revisión legal trimestral y cifrado de datos sensibles de forma permanente."],
        ["Equipo pequeño con roles compartidos.", "Velocidad menor que la planificada.", "Priorizar por valor, evitar trabajo en paralelo excesivo y automatizar verificación."],
        ["Deuda técnica conocida en autenticación y paginación.", "Regresiones durante las fases iniciales.", "Concentrar la deuda en la fase 0 antes de abrir alcance nuevo."],
        ["Caída de la base de datos o pérdida de datos.", "Interrupción de la operación y pérdida de historial.", "Respaldo programado con restauración probada, entregado en la fase 0."],
        ["Cambios de prioridad del negocio.", "Reordenamiento costoso del plan.", "Revisión trimestral del roadmap y alcance por objetivos, no por fechas."],
    ],
    widths=[2.4, 2.0, 3.6],
)

# ==================================================== 10
d.h1("10. Gobernanza del roadmap")
d.p(
    "El roadmap se revisa cada tres meses con el Product Owner y los responsables del negocio. En esa "
    "revisión se confirman los indicadores de cierre de la fase en curso, se reordena el backlog de "
    "las fases siguientes y se decide la entrada de nuevas iniciativas. Una fase solo se declara "
    "terminada cuando su indicador de cierre tiene evidencia: pruebas ejecutadas, reportes "
    "verificados o restauraciones realizadas, nunca por declaración de avance."
)
d.p(
    "Cualquier cambio de alcance queda registrado en la versión del roadmap, con su fecha y su motivo, "
    "de modo que el documento sirva también como memoria de las decisiones tomadas. La caducidad del "
    "documento es deliberada: después de doce meses se sustituye por una nueva versión construida "
    "sobre los resultados realmente obtenidos."
)

d.references([
    "Equipo de Ingeniería de Software. (2026). *Documento de Requerimientos del Software de LoanSoft*. "
    "LoanSoft.",
    "Equipo de Ingeniería de Software. (2026). *Plan Scrum de LoanSoft*. LoanSoft.",
    "Equipo de Ingeniería de Software. (2026). *Manual Técnico de LoanSoft*. LoanSoft.",
])
d.save(os.path.join(OUT, "05_Roadmap_Estrategico.docx"))
print("Roadmap generado")
