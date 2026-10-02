# -*- coding: utf-8 -*-
"""Genera el Manual Técnico de LoanSoft."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from apa import Doc  # noqa: E402

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")

d = Doc(
    title="**Manual Técnico**",
    subtitle="Arquitectura, código fuente y operación de LoanSoft",
    author=["Equipo de Ingeniería de Software · LoanSoft"],
    affiliation=["LoanSoft · Sistema de Gestión de Préstamos"],
    date=["28 de septiembre de 2026"],
    extra=["Versión 1.0",
           "Dirigido a desarrolladores, integradores y responsables de infraestructura"],
)

d.abstract(
    "Este manual describe la arquitectura de LoanSoft tal como está implementada: frontend Nuxt 4, "
    "backend FastAPI, base de datos relacional y procesos programados. Documenta la estructura de "
    "directorios, las decisiones de diseño, los contratos de servicio, la configuración de entorno, "
    "los procedimientos de verificación y la deuda técnica detectada, con la evidencia de archivo y "
    "línea que permite localizar cada hallazgo. Su propósito es que un desarrollador nuevo pueda "
    "comprender, ejecutar y modificar el sistema sin necesidad de conocimiento previo del proyecto."
)

# ============================================================ 1. Introducción
d.h1("1. Introducción")
d.p(
    "LoanSoft se implementa como una aplicación de dos capas separadas por una interfaz REST: el "
    "frontend se encarga de la experiencia de uso y de la tolerancia a fallos de red, y el backend "
    "concentra la lógica financiera, la seguridad y la persistencia. Esta separación es deliberada: "
    "los cálculos monetarios solo se ejecutan en el servidor para que exista un único criterio de "
    "verdad."
)
d.h2("1.1 Público y alcance")
d.p(
    "El manual está dirigido a perfiles técnicos. No describe el uso cotidiano de las pantallas, que "
    "se documenta en el manual de usuario, sino cómo está construido el producto, cómo se ejecuta en "
    "desarrollo y producción, cómo se verifica su correcto funcionamiento y qué aspectos del código "
    "requieren atención antes de una entrega."
)
d.h2("1.2 Convenciones del documento")
d.p(
    "Las rutas de archivo se expresan con la forma *app/pages/prestamos/index.vue* para el frontend y "
    "*app/routes/prestamo.py* para el backend. Cuando un hallazgo se acompaña de evidencia, se cita "
    "el archivo y la línea aproximada, de modo que pueda reproducirse localmente. Los comandos "
    "aparecen en bloques de texto independientes para poder copiarlos sin procesar el resto del "
    "contenido."
)

# ==================================================== 2. Arquitectura general
d.h1("2. Arquitectura general")
d.p(
    "El sistema se organiza en tres niveles: una capa de acceso donde el usuario interactúa, un "
    "núcleo de servicios que ejecuta el negocio y una capa de persistencia que conserva los datos. "
    "Entre la capa de acceso y el núcleo existe una API REST que es el único camino de entrada a la "
    "lógica de negocio; no hay acceso directo a la base de datos desde el navegador."
)
d.figure(os.path.join(FIGS, "fig1_arquitectura.png"),
         "Arquitectura general de LoanSoft y flujo de comunicación entre capas.")

d.h2("2.1 Frontend")
d.p(
    "El frontend está construido con Nuxt 4 sobre Vue 3, con compilación en modo estricto de "
    "TypeScript. Organiza el código por capas: las vistas residen en *app/pages*, los componentes "
    "reutilizables en *app/components*, la orquestación de casos de uso en *app/composables*, el "
    "acceso a la API en *app/services/api*, el almacenamiento local en *app/services/db* y el estado "
    "compartido en *app/stores*."
)
d.p(
    "La comunicación con el servidor se centraliza en un único cliente HTTP (*useApi*) que inyecta "
    "el token de acceso, renueva la sesión cuando expira, normaliza los errores y soporta "
    "descargas binarias. Ningún componente debe construir direcciones de servicio por su cuenta: "
    "todas pasan por los servicios de la capa *services/api*."
)
d.figure(os.path.join(FIGS, "fig5_capas_frontend.png"),
         "Capas del frontend y dependencia entre ellas.")

d.h2("2.2 Backend")
d.p(
    "El backend usa FastAPI con SQLAlchemy 2 y Pydantic 2. Cada dominio del negocio dispone de un "
    "router, un servicio y un esquema, siguiendo una estructura de paquetes tripartita: *routes* "
    "define las rutas y las dependencias, *services* implementa la lógica y *schemas* declara los "
    "contratos de entrada y salida. Las consultas paginadas se resuelven con la utilidad central de "
    "*app/utils/pagination.py*, que devuelve siempre la misma estructura con elementos, total, "
    "página y límite."
)
d.p(
    "Al iniciar, la aplicación ejecuta dos tareas en su ciclo de vida: crea las tablas que falten y "
    "arranca el planificador de trabajos. Al apagar, detiene el planificador de forma ordenada. Esta "
    "secuencia está definida en *app/main.py* y garantiza que los procesos programados no queden "
    "huérfanos."
)

d.h2("2.3 Modelo de datos")
d.p(
    "El modelo comprende 17 tablas organizadas en cuatro grupos: identidad y control (usuarios, "
    "tokens, auditoría, suscripciones push, configuración e idempotencia), catálogos (tipos de "
    "préstamo y tipos de pago), operación (clientes, préstamos, cuotas, pagos y moras) y contabilidad "
    "(capital y movimientos de capital). Las tablas de renovaciones y préstamos perdidos conservan "
    "el histórico de las decisiones de riesgo."
)
d.figure(os.path.join(FIGS, "fig6_entorno_relaciones.png"),
         "Entidades principales y relaciones entre tablas del modelo de datos.")
d.p(
    "El esquema no se gestiona con un migrador versionado: el arranque crea las tablas faltantes y "
    "aplica ajustes simples sobre la estructura existente. Esta decisión simplifica el arranque en "
    "desarrollo, pero obliga a implementar un plan de migración antes de evolucionar el modelo en "
    "producción."
)

d.h2("2.4 Flujo de operaciones críticas")
d.p(
    "El ciclo del préstamo parte del registro del cliente, continúa con la creación del préstamo —que "
    "descuenta capital y genera cuotas— y avanza por el cobro hasta el cierre. Cada rama posterior "
    "(renovación, pérdida, reportes) se alimenta del mismo libro de movimientos."
)
d.figure(os.path.join(FIGS, "fig2_flujo_credito.png"),
         "Ciclo completo de una operación de crédito en el sistema.")
d.p(
    "El cobro es la operación con más controles. El servidor valida el desglose contra el total, "
    "aplica el pago al saldo, suma el capital al fondo, actualiza el estado de la cuota y evalúa el "
    "cierre del préstamo dentro de una única transacción; si cualquiera de esos pasos falla, no "
    "queda ningún efecto parcial."
)
d.figure(os.path.join(FIGS, "fig3_flujo_pago.png"),
         "Secuencia de validación y efectos del registro de un pago.")
d.p(
    "Los estados del préstamo son terminales una vez alcanzados: un préstamo pagado, perdido o "
    "renovado no admite nuevas operaciones de cobro ni de riesgo."
)
d.figure(os.path.join(FIGS, "fig4_estados.png"),
         "Máquina de estados del préstamo y transiciones permitidas.")

# ==================================================== 3. Stack tecnológico
d.h1("3. Stack tecnológico")
d.p(
    "Las versiones están fijadas en los archivos de dependencias de cada capa. El frontend se instala "
    "con pnpm y el backend con pip a partir de su archivo de requisitos."
)
d.table(
    "Tecnologías del frontend",
    ["Tecnología", "Versión declarada", "Uso en el producto"],
    [
        ["Nuxt", "4.4.6", "Compilación, enrutado, renderizado en servidor y plugins."],
        ["Vue", "3", "Componentes reactivos y composición de interfaz."],
        ["TypeScript", "6.0.3 en estricto", "Tipado de servicios, store y componentes."],
        ["Pinia", "4.0.2", "Estado global de sesión, sincronización y formato."],
        ["Nuxt UI", "4.8.1", "Kit de componentes de interfaz."],
        ["Tailwind CSS", "4.3.0", "Sistema de diseño y utilidades de estilo."],
        ["Zod", "4.4.3", "Validación de formularios en cliente."],
        ["Dexie", "4.4.6", "Acceso a IndexedDB para almacenamiento local."],
        ["Vite PWA", "1.1.1", "Manifest, service worker y caché offline."],
        ["Vitest", "4.1.10", "Pruebas unitarias."],
        ["ESLint", "10.4.1", "Análisis de estilo y calidad de código."],
    ],
    widths=[1.6, 1.4, 3.5],
)
d.table(
    "Tecnologías del backend",
    ["Tecnología", "Versión declarada", "Uso en el producto"],
    [
        ["FastAPI", "0.135.1", "API REST, validación de esquemas y documentación automática."],
        ["SQLAlchemy", "2.0.48", "Acceso a datos y mapeo objeto-relacional."],
        ["Pydantic", "2.12.5", "Contratos de entrada y salida de datos."],
        ["PyMySQL", "1.1.2", "Conector de MySQL para producción."],
        ["bcrypt / passlib", "4.0.1", "Cifrado de contraseñas."],
        ["PyJWT / jwcrypto", "última compatible", "Firmado de tokens de acceso y refresco."],
        ["APScheduler", "última compatible", "Trabajos programados de moras y avisos."],
        ["pywebpush / py-vapid", "última compatible", "Envío de notificaciones web push."],
        ["openpyxl / reportlab", "última compatible", "Exportación de reportes a Excel y PDF."],
        ["Uvicorn", "0.42.0", "Servidor ASGI de ejecución."],
    ],
    widths=[1.6, 1.4, 3.5],
)

# ================================================ 4. Estructura de proyecto
d.h1("4. Estructura del proyecto")
d.p(
    "El repositorio del frontend organiza el código por responsabilidad y reserva dos áreas "
    "especiales: *shared/types* para los contratos de datos compartidos entre vistas y servicios, y "
    "*tests* para las pruebas unitarias."
)
d.table(
    "Estructura de directorios del frontend",
    ["Directorio", "Contenido", "Regla de dependencia"],
    [
        ["app/pages", "15 vistas organizadas por ruta, incluidas login, perfil, clientes, préstamos, pagos, moras, cobranza, capital, reportes, usuarios y catálogos.", "Puede usar composables y componentes; no llama a la API de forma directa."],
        ["app/components", "31 componentes: kit de interfaz, diálogos y componentes de dominio.", "Recibe datos por propiedades y emite eventos."],
        ["app/composables", "17 composables: cliente HTTP, formateadores, notificaciones, offline, onboarding, push, instalación, atajos y composables de dominio por módulo.", "Orquesta servicios y estado; no conoce rutas de la API."],
        ["app/services/api", "12 servicios: auth, clientes, préstamos, pagos, moras, capital, tipos, usuarios, reportes, push, extractos y onboarding.", "Única capa que conoce las direcciones del backend."],
        ["app/services/db", "5 módulos: base de datos local, repositorio, cola de salida, auditoría local y cobranza offline.", "Persistencia local en IndexedDB."],
        ["app/stores", "3 stores: sesión, sincronización y vista.", "Estado global con Pinia."],
        ["app/middleware", "3 middlewares: auth, guest y admin.", "Protección de rutas entre cliente y servidor."],
        ["shared/types", "19 archivos de tipos compartidos entre vistas y servicios.", "Fuente única de formas de datos."],
        ["tests/unit", "3 suites: cálculo de préstamos, fechas y formato monetario.", "Se ejecutan con Vitest."],
    ],
    widths=[1.4, 3.6, 2.0],
)
d.p(
    "El backend replica la misma idea con una separación por capas: *routes* para la interfaz HTTP, "
    "*services* para la lógica, *schemas* para los contratos, *models* para las entidades y "
    "*utils* para utilidades transversales como la paginación. *app/core* concentra la configuración "
    "y la seguridad, y *app/dependencies* las dependencias de autenticación y autorización."
)
d.table(
    "Estructura de directorios del backend",
    ["Directorio", "Contenido", "Regla de dependencia"],
    [
        ["app/routes", "14 routers: autenticación, usuarios, clientes, tipos, capital, préstamos, pagos, moras, reportes, auditoría, notificaciones, push y tablero.", "Resuelve parámetros y delega en servicios."],
        ["app/services", "17 módulos: lógica de negocio por dominio más planificador y push.", "Única capa que modifica datos."],
        ["app/schemas", "Esquemas Pydantic de entrada, salida y paginación.", "Validan y documentan los contratos."],
        ["app/models", "17 entidades que mapean las tablas de la base de datos.", "Sin dependencias de la API."],
        ["app/utils", "Paginación y utilidades comunes.", "Sin estado."],
        ["app/core", "Configuración y primitivas de seguridad.", "Sin dependencias de dominio."],
        ["app/dependencies", "Dependencias de sesión y rol.", "Usadas por los routers."],
    ],
    widths=[1.4, 3.6, 2.0],
)

# ================================================= 5. Interfaz de servicios
d.h1("5. Interfaz de servicios")
d.p(
    "El backend publica 14 routers bajo un único prefijo de versión heredado de la raíz de la API. "
    "Todos los endpoints devuelven JSON y utilizan los códigos de estado estándar: creación con 200 "
    "u 201, validación con 400, credenciales inválidas con 401, autorización insuficiente con 403 y "
    "recurso inexistente con 404."
)
d.table(
    "Routers publicados por el backend",
    ["Prefijo", "Operaciones principales", "Observaciones"],
    [
        ["/auth", "login, refresh, logout, me, change-password, forgot-password, reset-password", "Emite par de tokens y gestiona su revocación."],
        ["/usuarios", "CRUD de cuentas con rol y estado", "Restringido a administración."],
        ["/clientes", "alta, listado paginado con búsqueda, detalle, edición y baja", "Soporta búsqueda libre por nombre, cédula o teléfono."],
        ["/tipo_prestamo", "CRUD del catálogo de tipos de préstamo", "Interés mensual y máximo de cuotas."],
        ["/tipo_pago", "CRUD del catálogo de medios de pago", "Se usa al registrar cobros."],
        ["/capital", "consulta de capital, creación y listado de movimientos", "El listado de movimientos está paginado."],
        ["/prestamos", "alta, listado paginado, detalle, renovar, marcar_perdido, ajustar-capital", "Centraliza las transiciones de estado."],
        ["/pagos", "registro de pagos con idempotencia y listado paginado", "Devuelve la estructura paginada estándar."],
        ["/mora", "listado paginado de moras y procesamiento manual", "Prefijo singular; no hay rutas por préstamo."],
        ["/reportes", "ganancias, perdidas, cartera, cobranza y exportación a Excel y PDF", "Aceptan rango de fechas."],
        ["/auditoria", "listado por usuario, tabla y tipo de operación", "Permite reconstruir operaciones sensibles."],
        ["/notificacion", "subscribe y unsubscribe de suscripciones push", "Guarda el endpoint del navegador."],
        ["/push", "envío de notificaciones y prueba de envío", "Requiere llaves VAPID configuradas."],
        ["/dashboard", "resumen consolidado del tablero", "No aprovechado por el frontend."],
    ],
    widths=[1.1, 3.5, 2.3],
)

d.h2("5.1 Contrato de paginación")
d.p(
    "Todos los listados que manejan colecciones devuelven la misma estructura: colección de "
    "elementos, total de registros, número de página actual y tamaño de página. El servidor interpreta "
    "los parámetros como número de página y límite, con página mínima de uno y límite mínimo de uno. "
    "Esta uniformidad es deliberada y responde al requerimiento de consistencia de listados."
)
d.p(
    "El punto débil está en el cliente: los servicios de clientes, pagos y moras envían un parámetro "
    "de desplazamiento que el servidor ignora, de modo que la petición siempre resuelve la primera "
    "página. Los servicios de capital, préstamos y usuarios sí envían número de página y funcionan "
    "como se espera. Unificar el parámetro en la capa de servicios es una corrección de alcance "
    "reducido con impacto directo en la usabilidad."
)

d.h2("5.2 Idempotencia")
d.p(
    "El registro de pagos soporta claves de idempotencia: la primera petición con una clave se procesa "
    "y su respuesta queda almacenada; cualquier repetición con la misma clave devuelve la respuesta "
    "original, y una repetición con un cuerpo distinto se rechaza con conflicto. Este mecanismo "
    "protege ante dobles envíos y reintentos automáticos del cliente."
)

d.h2("5.3 Manejo de errores")
d.p(
    "Los servicios del backend responden con un cuerpo de error que incluye el detalle legible de la "
    "causa. El cliente HTTP del frontend normaliza esos cuerpos a un formato único con mensaje "
    "amigable, de modo que las pantallas muestren siempre un texto comprensible sin condicionales "
    "por cada endpoint."
)

# ================================================================ 6. Seguridad
d.h1("6. Seguridad")
d.p(
    "La estrategia de seguridad combina cifrado de credenciales, tokens firmados y envueltos, "
    "autorización por rol en servidor y registro de auditoría. La principal debilidad no está en el "
    "servidor sino en el cliente, donde los middlewares de protección no están activos."
)
d.table(
    "Controles de seguridad implementados",
    ["Control", "Implementación", "Ubicación"],
    [
        ["Cifrado de contraseñas", "Hash con bcrypt y doce rondas de coste.", "app/core/security.py"],
        ["Firma de tokens", "Algoritmo HS256 con vencimiento de 60 minutos para acceso y 7 días para refresco.", "app/core/security.py"],
        ["Protección de los tokens", "El token firmado se envuelve con un cifrado de contenido A256KW y A256CBC-HS512 antes de emitirse.", "app/core/security.py"],
        ["Revocación", "Los tokens se persisten con un indicador de actividad que permite cerrar la sesión en servidor.", "app/services/auth.py"],
        ["Autorización", "Dependencias de sesión y rol aplicadas en los routers sensibles.", "app/dependencies"],
        ["Auditoría", "Registro de operaciones sobre préstamos, pagos, capital y moras con autor, valores y origen.", "app/services/auditoria.py"],
        ["CORS", "Lista explícita de orígenes permitidos, ampliable con variable de entorno.", "app/main.py"],
        ["Validación de entrada", "Esquemas Pydantic en todos los puntos de entrada.", "app/schemas"],
        ["Protección de rutas del cliente", "Middlewares auth y admin sin efecto: la protección de auth está deshabilitada y admin solo comprueba una cookie que no se crea.", "app/middleware"],
    ],
    widths=[1.6, 3.4, 1.8],
)
d.p(
    "Conviene subrayar que el control de acceso real es el del servidor: incluso con la interfaz "
    "abierta, un usuario sin rol no puede ejecutar operaciones restringidas. El riesgo residual de "
    "los middlewares inactivos es la exposición de la interfaz y de los datos que ella consulta con "
    "un token válido en el navegador."
)

# ================================================ 7. Procesos programados
d.h1("7. Procesos programados")
d.p(
    "Un planificador de fondo ejecuta una tarea diaria a medianoche que encadena dos operaciones: el "
    "cálculo de moras y el envío de recordatorios de vencimiento. La tarea tiene una ventana de "
    "tolerancia de una hora, de modo que un apagón momentáneo no la pierde, y registra en consola el "
    "resultado de cada ejecución."
)
d.table(
    "Trabajos programados",
    ["Trabajo", "Frecuencia", "Efecto", "Manejo de fallos"],
    [
        ["Procesamiento de moras", "Diario a las 00:00", "Genera la mora de las cuotas vencidas aplicando la tasa y los días de gracia configurados.", "Una falla no detiene el planificador y se reintenta en la siguiente ejecución."],
        ["Recordatorios de vencimiento", "Diario a las 00:00", "Envía avisos push a los administradores activos sobre cuotas que vencen en tres días y en un día.", "Se omiten los destinatarios sin suscripción válida."],
        ["Procesamiento manual de moras", "Bajo demanda", "Ejecuta el mismo cálculo desde la interfaz administrativa.", "Restringido a administradores; devuelve total de moras generadas."],
    ],
    widths=[1.6, 1.2, 2.6, 1.6],
)
d.p(
    "El planificador se detiene de forma ordenada cuando la aplicación se apaga, evitando ejecuciones "
    "a medias. Como el cálculo depende de la hora del servidor, cualquier desfase de zona horaria "
    "desplaza la generación de moras y debe controlarse en el despliegue."
)

# ================================================= 8. Configuración
d.h1("8. Configuración y variables de entorno")
d.p(
    "El backend carga su configuración desde un archivo de variables mediante ajustes tipados: si "
    "falta una variable obligatoria, el servidor no arranca. El frontend, en cambio, solo expone la "
    "dirección de la API como configuración pública y el resto se resuelve en compilación."
)
d.table(
    "Variables de entorno del backend",
    ["Variable", "Obligatoria", "Función"],
    [
        ["SECRET_KEY", "Sí", "Secreto para firmar los tokens de acceso y refresco."],
        ["DATABASE_URL", "Sí", "Cadena de conexión a la base de datos; en desarrollo se usa SQLite."],
        ["ENCRYPTION_KEY", "Sí", "Semilla para derivar la clave que envuelve los tokens."],
        ["FRONTEND_URL", "No", "Origen del cliente admitido en CORS (por defecto el puerto 3000)."],
        ["VAPID_PUBLIC_KEY", "Sí", "Llave pública del servicio de notificaciones push."],
        ["VAPID_PRIVATE_KEY", "Sí", "Llave privada del servicio de notificaciones push."],
        ["VAPID_CLAIM_EMAIL", "No", "Correo de contacto declarado en las llaves push."],
    ],
    widths=[1.6, 1.0, 4.0],
    align_center_cols=(1,),
)
d.table(
    "Configuración del frontend",
    ["Clave", "Origen", "Función"],
    [
        ["NUXT_PUBLIC_API_BASE", "Variable de entorno", "Dirección base del backend; por defecto el servidor local en el puerto 8000."],
        ["typescript.strict", "nuxt.config.ts", "Compilación en modo estricto."],
        ["pwa.manifest", "nuxt.config.ts", "Nombre, colores, idioma e iconos de la aplicación instalable."],
        ["pwa.workbox", "nuxt.config.ts", "Políticas de caché de recursos y respuestas de la API."],
        ["eslint.config", "nuxt.config.ts", "Reglas de estilo, entre ellas la ausencia de coma final."],
    ],
    widths=[1.8, 1.4, 3.6],
)
d.p(
    "Existe un desajuste de configuración que debe corregirse antes de publicar: las reglas de caché "
    "del service worker apuntan a la dirección local del backend y no a la dirección efectiva del "
    "entorno, por lo que en producción las respuestas de la API no se cachean como se espera."
)

# =============================================== 9. Desarrollo y verificación
d.h1("9. Desarrollo, verificación y calidad")
d.p(
    "El frontend expone comandos estándar para desarrollo, compilación y verificación. El backend se "
    "ejecuta con un servidor ASGI y no incluye una batería automatizada de pruebas propia; la "
    "verificación del servidor se realiza hoy mediante la documentación interactiva y las pruebas de "
    "integración manuales."
)
d.table(
    "Comandos de trabajo",
    ["Ámbito", "Comando", "Propósito"],
    [
        ["Frontend", "pnpm install", "Instala las dependencias fijadas."],
        ["Frontend", "pnpm dev", "Arranca el servidor de desarrollo con recarga."],
        ["Frontend", "pnpm build", "Compila la aplicación para producción."],
        ["Frontend", "pnpm lint", "Verifica el estilo del código."],
        ["Frontend", "pnpm typecheck", "Comprueba los tipos en modo estricto."],
        ["Frontend", "pnpm test", "Ejecuta las pruebas unitarias con Vitest."],
        ["Backend", "uvicorn app.main:app --reload", "Arranca la API con recarga automática."],
        ["Backend", "pip install -r requirements.txt", "Instala las dependencias del servidor."],
        ["Documentación", "python _build/gen_srs.py", "Regenera los documentos Word del repositorio."],
    ],
    widths=[1.2, 2.6, 3.0],
)
d.p(
    "La verificación automatizada actual cubre tres suites unitarias del frontend: cálculo financiero "
    "de préstamos, manejo de fechas y formato monetario. No existen pruebas de extremo a extremo ni "
    "pruebas del backend, y no hay integración continua que ejecute la verificación antes de fusionar "
    "cambios. Estas carencias son el primer objetivo de la fase de estabilización."
)

d.h2("9.1 Criterios de calidad del código")
d.p(
    "El código del frontend debe pasar lint y typecheck sin errores antes de fusionarse, y los "
    "cambios en servicios deben mantener los tipos compartidos sincronizados con los contratos del "
    "servidor. El backend debe conservar la atomicidad de las operaciones financieras: ninguna "
    "modificación puede dejar movimientos sin correspondencia en el capital."
)

# =================================================== 10. Despliegue
d.h1("10. Despliegue y operación")
d.p(
    "El proyecto no incluye todavía automatización de despliegue: no existen contenedores, orquestación "
    "ni pipelines de integración. El despliegue se realiza actualmente de forma manual y requiere los "
    "pasos siguientes."
)
d.numbered(1, "Compilar el frontend con el comando de construcción y publicar la carpeta generada en "
              "un servidor estático detrás de HTTPS.")
d.numbered(2, "Instalar las dependencias del backend, definir las variables de entorno obligatorias y "
              "arrancar el servidor ASGI con un proceso supervisor.")
d.numbered(3, "Crear la base de datos de producción y verificar que el proceso de creación de tablas "
              "termina sin errores.")
d.numbered(4, "Configurar el respaldo de la base de datos y probar una restauración antes de operar.")
d.numbered(5, "Actualizar la dirección pública de la API en la configuración del frontend y verificar "
              "que la caché del service worker apunta al dominio publicado.")
d.numbered(6, "Comprobar que el planificador diario registra ejecuciones después del primer "
              "reinicio.")
d.p(
    "En la puesta en producción deben habilitarse además las cabeceras de seguridad y la política de "
    "contenidos, cuya ausencia está identificada como pendiente en el documento de requerimientos. La "
    "ausencia de integración continua obliga a ejecutar a mano las verificaciones de estilo, tipos y "
    "pruebas antes de cada publicación."
)

# ============================================= 11. Deuda técnica
d.h1("11. Deuda técnica y hallazgos")
d.p(
    "El análisis del código identificó los siguientes hallazgos, ordenados por impacto en la "
    "operación. Cada uno incluye su ubicación y el efecto observable, de modo que pueda corregirse "
    "de forma aislada."
)
d.table(
    "Hallazgos prioritarios con evidencia en código",
    ["Hallazgo", "Ubicación", "Efecto", "Corrección sugerida"],
    [
        ["Protección de rutas deshabilitada en el cliente", "app/middleware/auth.ts",
         "Las páginas que declaran el middleware de autenticación no redirigen al inicio de sesión.",
         "Restablecer la validación de sesión y el refresco antes de navegar."],
        ["Middleware de administración sin verificación de rol", "app/middleware/admin.ts",
         "Comprueba una cookie que nunca se crea, por lo que las cinco páginas administrativas no son accesibles.",
         "Leer la identidad del almacén de sesión y validar el rol real."],
        ["Rutas de moras desalineadas", "app/services/api/mora.ts frente a app/routes/mora.py",
         "El cliente invoca rutas con prefijo plural que el servidor no publica, por lo que el módulo devuelve recurso inexistente.",
         "Unificar el prefijo y añadir las rutas por préstamo que el cliente espera."],
        ["Contrato de paginación inconsistente", "app/services/api/clientes.ts, pago.ts y mora.ts",
         "Envían desplazamiento en lugar de número de página y muestran siempre la primera página.",
         "Usar el parámetro de página en toda la capa de servicios."],
        ["Tipo de respuesta incompatible en pagos", "app/services/api/pago.ts",
         "Se declara una lista plana mientras el servidor devuelve un objeto paginado, por lo que el historial redirige al detalle.",
         "Alinear el tipo con la estructura paginada estándar."],
        ["Datos simulados en la importación de extractos",          "app/components/app/ImportExtractModal.vue",
         "La pantalla devuelve resultados inventados en lugar de procesar el archivo cargado.",
         "Implementar el procesamiento real o retirar la pantalla hasta que exista."],
        ["Almacenamiento local sin uso", "app/services/db (outbox, repository, audit)",
         "La operación offline y la auditoría local están construidas pero ninguna pantalla las activa.",
         "Conectar la cola de salida a los servicios de escritura."],
        ["Suscripción push con variables sin definir", "app/composables/usePushNotifications.ts",
         "Lee claves de entorno de desarrollo que no existen, por lo que la suscripción no se registra.",
         "Publicar las llaves como configuración pública y validar su presencia."],
        ["Caché fijada al servidor local", "nuxt.config.ts (pwa.workbox.runtimeCaching)",
         "Las reglas apuntan a la dirección local del backend en cualquier entorno.",
         "Resolver la dirección desde la configuración pública."],
        ["Iconos del manifiesto inexistentes", "public/icons",
         "El manifiesto declara iconos que no están en el paquete, lo que afecta la instalación.",
         "Añadir los recursos o ajustar el manifiesto."],
        ["Documentación del repositorio desactualizada", "README.md",
         "El archivo sigue siendo la presentación de la plantilla inicial y no describe el producto.",
         "Reemplazarlo por el arranque real del proyecto."],
        ["Componente sin uso", "app/components/Layout/Table.vue",
         "No es utilizado por ninguna vista y genera confusión sobre el componente estándar de tablas.",
         "Eliminarlo o integrarlo como componente oficial."],
        ["Pruebas limitadas", "tests/unit (3 suites)",
         "No hay cobertura del backend ni pruebas de integración ni de extremo a extremo.",
         "Añadir pruebas de los servicios financieros y un flujo básico de extremo a extremo."],
        ["Sin integración continua ni despliegue automatizado", "repositorio",
         "Las verificaciones dependen de la disciplina manual antes de cada publicación.",
         "Configurar un pipeline que ejecute lint, tipos, pruebas y compilación."],
    ],
    widths=[1.8, 1.6, 2.2, 1.8],
)

d.h2("11.1 Riesgos financieros derivados del código")
d.p(
    "Más allá de los defectos de interfaz, hay tres riesgos económicos que conviene vigilar. El "
    "primero es la ausencia de reversión de pagos: una vez registrado un cobro, su corrección "
    "requiere intervención directa en la base de datos. El segundo es la falta de respaldo "
    "automatizado, que pone en riesgo el histórico de movimientos de capital. El tercero es la "
    "inexistencia de cabeceras de seguridad y cifrado forzado, que expone el canal de comunicación "
    "en despliegues mal configurados."
)

d.h2("11.2 Arquitectura objetivo")
d.p(
    "El crecimiento previsto del producto apunta a una arquitectura de servicios acotados detrás de un "
    "punto de entrada único, con identidad, cartera, cobranza y reportes como unidades desplegables "
    "independientes y una capa de plataforma que aporta almacenamiento, caché y observabilidad. Esta "
    "meta es progresiva: el monolito actual bien delimitado es un punto de partida válido, y la "
    "extracción de servicios debe seguir al orden de valor: primero reportes, después cobranza y "
    "finalmente identidad."
)
d.figure(os.path.join(FIGS, "fig7_microservicios.png"),
         "Arquitectura objetivo con servicios de dominio y plataforma transversal.")

d.references([
    "Equipo de Ingeniería de Software. (2026). *BLUEPRINT_LOANSOFT: alcance, fases y deuda del "
    "sistema LoanSoft*. LoanSoft.",
    "Equipo de Ingeniería de Software. (2026). *PLAN_FRONTEND_NUXT4: stack técnico y requerimientos "
    "de backend B1 a B11*. LoanSoft.",
    "Equipo de Ingeniería de Software. (2026). *BACKEND_ENDPOINTS: inventario de interfaces del "
    "servidor*. LoanSoft.",
    "FastAPI. (s. f.). *FastAPI documentation*. https://fastapi.tiangolo.com/",
    "Nuxt. (s. f.). *Nuxt 4 documentation*. https://nuxt.com/",
    "SQLAlchemy. (s. f.). *SQLAlchemy 2.0 documentation*. https://www.sqlalchemy.org/",
    "Pydantic. (s. f.). *Pydantic documentation*. https://docs.pydantic.dev/",
])
d.save(os.path.join(OUT, "02_Manual_Tecnico.docx"))
print("Manual técnico generado")
