# -*- coding: utf-8 -*-
"""Genera el Documento de Requerimientos del Software (SRS) de LoanSoft."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from apa import Doc  # noqa: E402

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")


def rf(d, code, nombre, desc, obj, actores, flujo, alt, reglas, valid, dep, prio, estado):
    d.h3(f"{code} · {nombre}")
    d.p(f"**Descripción.** {desc} **Objetivo de negocio.** {obj} **Actores.** {actores}")
    d.p(f"**Flujo principal.** {flujo} **Flujos alternativos y de excepción.** {alt} "
        f"**Reglas de negocio.** {reglas} **Validaciones.** {valid} **Dependencias.** {dep} "
        f"**Prioridad.** {prio}. **Estado de implementación.** {estado}.")


d = Doc(
    title="**Documento de Requerimientos del Software**",
    subtitle="Sistema LoanSoft: plataforma de originación, cartera y cobranza de préstamos",
    author=["Equipo de Ingeniería de Software · LoanSoft"],
    affiliation=["LoanSoft · Sistema de Gestión de Préstamos"],
    date=["28 de septiembre de 2026"],
    extra=["Versión 1.0",
           "Documento de requisitos basado en el análisis del código fuente del frontend y del backend"],
)

d.abstract(
    "LoanSoft es una plataforma financiera para originar, administrar y cobrar préstamos con garantía "
    "personal. Este documento define los requerimientos funcionales y no funcionales del sistema, su "
    "estado real de implementación y la trazabilidad entre requisitos, componentes de software y casos "
    "de prueba. El análisis se realizó sobre el código fuente real del frontend (Nuxt 4) y del backend "
    "(FastAPI), por lo que cada requisito se clasifica como Completada, Parcial o Pendiente. Se "
    "identificaron 75 requerimientos funcionales en once módulos y 48 requerimientos no funcionales "
    "en ocho categorías. Los hallazgos críticos corresponden a controles de acceso no activos en el "
    "frontend, a un módulo de moras desalineado con las rutas del backend, a inconsistencias de "
    "paginación entre ambas capas y a funcionalidades financiero-contables todavía sin interfaz de "
    "usuario."
)

# ============================================================ 1. Introducción
d.h1("1. Introducción")
d.p(
    "El presente documento establece los requerimientos del software LoanSoft, una aplicación web "
    "diseñada para administrar el ciclo completo de un portafolio de préstamos: registro de clientes, "
    "originación, desembolso, cobro de cuotas, cálculo de moras, gestión de capital y reportes "
    "financieros. Sirve como referencia común entre negocio, diseño, desarrollo y pruebas, y constituye "
    "la base para la aceptación de cada incremento del producto."
)

d.h2("1.1 Propósito y alcance")
d.p(
    "El alcance comprende la aplicación web responsiva (frontend), la API REST (backend), la base de "
    "datos relacional y los procesos programados que sostienen el negocio, entre ellos el cálculo "
    "diario de moras y el envío de recordatorios. Se documentan también los módulos previstos que "
    "aún no existen en el código, con el fin de distinguir con claridad lo que está entregado de lo "
    "que falta por construir."
)
d.p(
    "Quedan fuera de alcance los canales móviles nativos, la integración con burós de crédito, las "
    "pasarelas de pago y la firma electrónica, todos ellos identificados en este documento como "
    "requerimientos pendientes de etapas posteriores."
)

d.h2("1.2 Definiciones, acrónimos y abreviaturas")
d.p(
    "Para evitar ambigüedades, este documento utiliza la terminología del dominio financiero tal como "
    "aparece en el código: *capital prestado* es el monto entregado al cliente; *interés* es la "
    "utilidad devengada por cuota; *cuota* es la fracción mensual de capital e interés; *mora* es la "
    "penalización diaria aplicada a cuotas vencidas; *saldo pendiente* es lo que falta por pagar del "
    "monto total; y *cartera* es el conjunto de préstamos vigentes."
)
d.table(
    "Definiciones y acrónimos utilizados",
    ["Término o acrónimo", "Definición"],
    [
        ["SRS", "Software Requirements Specification, documento de requerimientos del software."],
        ["RF / RNF", "Requerimiento funcional / requerimiento no funcional."],
        ["CP", "Caso de prueba asociado a un requerimiento."],
        ["KPI", "Indicador clave de desempeño mostrado en el tablero principal."],
        ["Idempotencia", "Propiedad que permite repetir una operación sin producir efectos adicionales."],
        ["Aprobado / Pendiente", "Estado de implementación: entregado en código o aún sin construir."],
        ["Activo / Pagado / Perdido / Renovado", "Estados de un préstamo en el modelo de negocio."],
        ["B1 a B11", "Requerimientos de backend acordados en el plan técnico del proyecto."],
    ],
    widths=[1.5, 5],
)

d.h2("1.3 Referencias")
d.p(
    "Los requisitos se derivan de la documentación de diseño del propio proyecto y de las guías "
    "oficiales del stack tecnológico: *BLUEPRINT_LOANSOFT.md* (fases, alcance y deuda identificada), "
    "*PLAN_FRONTEND_NUXT4.md* (stack y requerimientos de backend B1 a B11), *BACKEND_ENDPOINTS.md* "
    "(inventario de endpoints y su estado), *PLAN_NUEVOS_MODULOS.md* (módulos previstos) y "
    "*PROPUESTA_REDISENO_ESTRUCTURAL.md* (organización de rutas). Como referencias técnicas se "
    "consultan las guías de Nuxt 4, FastAPI, SQLAlchemy 2, Pydantic 2 y la especificación APA 7 para "
    "la presentación de este documento."
)

d.h2("1.4 Visión general del documento")
d.p(
    "El capítulo 2 describe el producto, sus usuarios y su entorno de operación. El capítulo 3 "
    "detalla los 75 requerimientos funcionales agrupados en once módulos. El capítulo 4 presenta los "
    "requerimientos no funcionales. El capítulo 5 establece las matrices de trazabilidad que vinculan "
    "requisitos, código y casos de prueba. Los capítulos 6 y 7 recogen las reglas de negocio "
    "financieras, los supuestos y los riesgos. El capítulo 8 documenta el control de versiones del "
    "documento."
)

# ==================================================== 2. Descripción general
d.h1("2. Descripción general del producto")
d.p(
    "LoanSoft reemplaza el control manual de un prestamista individual por un sistema que calcula y "
    "resguarda cada movimiento monetario. El producto garantiza que el capital se mueva de forma "
    "coherente: se descuenta al desembolsar, se incrementa con cada abono de capital, se reduce "
    "cuando un préstamo se declara perdido y queda documentado en un libro de movimientos consultable."
)

d.h2("2.1 Perspectiva del producto")
d.p(
    "El sistema está compuesto por un frontend Nuxt 4 que implementa renderizado en servidor, "
    "persistencia offline con IndexedDB y notificaciones push; un backend FastAPI que concentra la "
    "lógica financiera y la seguridad; y una base de datos MySQL en producción con respaldo SQLite en "
    "desarrollo. Las dos capas se comunican mediante una API REST versionada en tokens JWT, con "
    "refresco automático en el cliente."
)
d.p(
    "El producto no es una calculadora aislada: su valor está en que cada operación queda registrada, "
    "auditada y reconciliada contra el capital disponible. Por eso los requerimientos de este "
    "documento conceden prioridad máxima a la integridad financiera y al control de acceso."
)

d.h2("2.2 Características principales del producto")
d.p(
    "En su estado actual el producto ofrece autenticación con tokens, administración de usuarios y "
    "roles, ficha de clientes con búsqueda, originación de préstamos con cálculo automático de cuotas, "
    "registro de pagos con desglose capital-interés-mora, renovación y pérdida de préstamos, cálculo "
    "programado de moras, libro de movimientos de capital, reportes de ganancias y pérdidas con "
    "exportación, tablero de indicadores y notificaciones push."
)
d.p(
    "El producto se entrega además como aplicación instalable (PWA) con caché de recursos, aunque los "
    "mecanismos de sincronización offline y de auditoría local existentes en el código aún no están "
    "conectados a las pantallas."
)

d.h2("2.3 Clases de usuarios")
d.p(
    "El backend reconoce actualmente dos roles: **administrador** y **usuario**. La diferencia "
    "operativa es que el administrador administra cuentas, tipos y parámetros, además de ejecutar el "
    "procesamiento manual de moras, mientras que el usuario operativo concentra la gestión de "
    "clientes, préstamos y pagos. El frontend menciona perfiles más granulares en su propuesta de "
    "diseño, pero dichos perfiles no existen todavía en el servidor."
)
d.table(
    "Perfiles de usuario y capacidades",
    ["Perfil", "Capacidades", "Restricciones"],
    [
        ["Administrador", "Gestiona usuarios, tipos de préstamo y de pago, ejecuta procesamiento manual de moras, consulta toda la operación.",
         "No puede eliminar registros históricos de pagos ni alterar movimientos de capital."],
        ["Usuario operativo", "Registra clientes, crea préstamos, registra pagos, consulta cartera y reportes.",
         "Sin acceso a administración de cuentas ni a parámetros del sistema."],
        ["Cliente final", "Destinatario de los cobros y recordatorios; no ingresa al sistema.",
         "Sin credenciales ni acceso a la aplicación."],
    ],
    widths=[1.3, 3.4, 2.3],
)

d.h2("2.4 Restricciones del entorno")
d.p(
    "El sistema opera bajo restricciones propias de un servicio financiero: los cálculos monetarios se "
    "expresan con dos decimales y cualquier diferencia de cuadre mayor a un centavo se rechaza; las "
    "operaciones de creación de préstamo, pago y pérdida exigen capital disponible previo; y la "
    "disponibilidad del servicio debe sostenerse durante horarios de cobro extendidos. A ello se suma "
    "la restricción tecnológica de mantener un único código de verdad para el negocio, evitando que "
    "frontend y backend calculen montos de forma independiente."
)

d.h2("2.5 Supuestos y dependencias")
d.p(
    "Se asume que la base de datos está respaldada de forma periódica por el responsable de "
    "infraestructura, que el dominio opera bajo HTTPS y que los procesos programados corren con el "
    "servicio backend activo las 24 horas. El producto depende de las librerías declaradas en el "
    "manifiesto de dependencias del frontend y de los paquetes del backend, cuyas versiones están "
    "fijadas en sus respectivos archivos de bloqueo."
)

# ================================================ 3. Requerimientos funcionales
d.h1("3. Requerimientos funcionales")
d.p(
    "Este capítulo enumera los requerimientos funcionales del sistema. Cada requisito se presenta con "
    "una etiqueta única, seguida de su descripción, objetivo de negocio, actores, flujo principal, "
    "flujos alternativos, reglas de negocio, validaciones, dependencias, prioridad y estado de "
    "implementación. Los estados se califican como **Completada** cuando el requisito está operativo "
    "en código, **Parcial** cuando existe pero con limitaciones documentadas y **Pendiente** cuando no "
    "hay implementación. Las prioridades se clasifican en **Máxima** (el negocio no opera sin él), "
    "**Alta** (impacto directo en la operación diaria) y **Media** (mejora de eficiencia o de alcance)."
)
d.p(
    "Al final de cada módulo se resume el estado de sus requisitos en una tabla de consolidación. Los "
    "indicadores de estado se obtuvieron de la lectura directa del código fuente, no de estimaciones "
    "de esfuerzo."
)

# ------------------------------------------------------------------- 3.1
d.h2("3.1 Seguridad, autenticación y administración")
d.p(
    "El módulo sostiene la confiabilidad del sistema: sin autenticación y control de roles no existe "
    "operación financiera defendible. El backend implementa el ciclo completo de tokens y gestión de "
    "cuentas; la brecha crítica se encuentra en el frontend, donde los middlewares de protección están "
    "inactivos."
)
d.table(
    "Consolidado del módulo de seguridad",
    ["Código", "Requisito", "Prioridad", "Estado"],
    [
        ["RF-001", "Inicio de sesión", "Máxima", "Completada"],
        ["RF-002", "Renovación de sesión", "Máxima", "Completada"],
        ["RF-003", "Cierre de sesión", "Máxima", "Completada"],
        ["RF-004", "Identidad del usuario activo", "Alta", "Completada"],
        ["RF-005", "Cambio de contraseña", "Alta", "Completada"],
        ["RF-006", "Recuperación de contraseña", "Media", "Parcial"],
        ["RF-007", "Administración de usuarios", "Alta", "Completada"],
        ["RF-008", "Protección de rutas en el frontend", "Máxima", "Pendiente"],
        ["RF-009", "Autorización por rol en el backend", "Máxima", "Completada"],
        ["RF-010", "Auditoría de operaciones sensibles", "Alta", "Parcial"],
        ["RF-011", "Configuración del sistema", "Alta", "Parcial"],
    ],
    widths=[0.9, 3.6, 1.2, 1.2],
    align_center_cols=(0, 2, 3),
)
rf(d, "RF-001", "Inicio de sesión con credenciales",
   "El sistema permite autenticar a un usuario con correo electrónico y contraseña.",
   "Garantizar que solo personal autorizado opere sobre la cartera.",
   "Cualquier usuario con cuenta registrada.",
   "El usuario ingresa correo y contraseña; el servidor valida las credenciales, devuelve un token de "
   "acceso y uno de refresco, y la aplicación redirige al tablero principal.",
   "Si las credenciales son inválidas se responde un mensaje genérico que no revele si la cuenta "
   "existe; si la cuenta está inactiva el acceso se deniega.",
   "El bloqueo de cuenta tras intentos fallidos está previsto pero no implementado.",
   "Correo con formato válido y contraseña de al menos 6 caracteres.",
   "Backend de autenticación y almacén de usuarios.",
   "Máxima", "Completada.")
rf(d, "RF-002", "Renovación automática de sesión",
   "El cliente renueva el token de acceso mediante el token de refresco antes de que expire.",
   "Mantener al usuario operativo sin interrupciones durante su jornada.",
   "Aplicación web (cliente HTTP).",
   "Ante una respuesta de expiración, el cliente solicita la renovación, repite la petición original "
   "y conserva la sesión.",
   "Si el refresco también está vencido, la sesión se cierra y el usuario vuelve a la pantalla de "
   "inicio de sesión.",
   "Un solo refresco en curso por pestaña para evitar carreras.",
   "El token de refresco debe estar activo en el servidor.",
   "RF-001.",
   "Alta", "Completada.")
rf(d, "RF-003", "Cierre de sesión",
   "El usuario puede cerrar su sesión y el servidor revoca el token asociado.",
   "Evitar el uso de credenciales abandonadas en equipos compartidos.",
   "Usuario autenticado.",
   "El usuario activa la opción de salida; el cliente limpia el estado local y el servidor marca el "
   "token como inactivo.",
   "Si el servidor no responde, la sesión local se igualmente elimina para no dejar credenciales en "
   "el navegador.",
   "El cierre es siempre local, con revocación en el servidor como mejor esfuerzo.",
   "Ninguna.",
   "RF-001.",
   "Alta", "Completada.")
rf(d, "RF-004", "Consulta de la identidad activa",
   "La aplicación recupera los datos del usuario autenticado al iniciar.",
   "Personalizar la interfaz y conocer el rol vigente en cada pantalla.",
   "Usuario autenticado.",
   "Al cargar, el cliente consulta el perfil, almacena nombre y rol, y decide qué menús mostrar.",
   "Si la consulta falla, se conserva la última identidad conocida y se reintenta con el refresco de "
   "token.",
   "El rol definido en el servidor prevalece sobre cualquier valor guardado localmente.",
   "Token de acceso vigente.",
   "RF-001, RF-002.",
   "Alta", "Completada.")
rf(d, "RF-005", "Cambio de contraseña",
   "El usuario autenticado puede actualizar su contraseña desde su perfil.",
   "Reducir el riesgo de credenciales comprometidas sin depender de un administrador.",
   "Usuario autenticado.",
   "Desde el perfil, el usuario indica la contraseña actual y la nueva; el servidor valida la actual, "
   "aplica la política mínima de longitud y confirma el cambio.",
   "Si la contraseña actual es incorrecta se muestra un error sin revelar detalle adicional; el "
   "cambio invalida la sesión actual del navegador.",
   "La contraseña nueva exige al menos 6 caracteres; no se permite reutilizar la actual.",
   "Los campos son obligatorios y la confirmación debe coincidir en el cliente.",
   "RF-001.",
   "Alta", "Completada.")
rf(d, "RF-006", "Recuperación de contraseña por correo",
   "El sistema expone los endpoints de solicitud y restablecimiento de contraseña mediante correo "
   "electrónico.",
   "Permitir el reingreso cuando un usuario olvida su contraseña.",
   "Usuario sin sesión, sistema de correo.",
   "El usuario solicita la recuperación; el servidor genera un token temporal, envía el correo y, al "
   "recibir el token con la contraseña nueva, actualiza el registro.",
   "El token expira y solo puede usarse una vez; el correo no existe actualmente por falta de "
   "configuración de servidor SMTP.",
   "La ventana de vigencia del token la define el servidor.",
   "Correo válido y coincidencia de la nueva contraseña.",
   "Configuración de correo no disponible en el entorno actual.",
   "Media", "Parcial.")
rf(d, "RF-007", "Administración de usuarios",
   "El administrador crea, edita, desactiva y lista las cuentas de acceso con su rol.",
   "Controlar quién opera sobre la cartera y con qué permisos.",
   "Administrador.",
   "El administrador registra un usuario con nombre, correo, contraseña y rol; lo edita para cambiar "
   "permisos; lo desactiva para retirar el acceso; y consulta la lista paginada.",
   "No se permite crear usuarios con correo duplicado; un administrador no puede desactivar su propia "
   "cuenta desde la pantalla de usuarios.",
   "Solo roles válidos del servidor: administrador y usuario.",
   "Correo con formato válido, contraseña obligatoria en creación y longitud mínima de 6.",
   "RF-001, RF-009.",
   "Alta", "Completada.")
rf(d, "RF-008", "Protección de rutas del frontend",
   "Toda ruta que requiera sesión debe redirigir al inicio de sesión cuando no exista token válido.",
   "Impedir el acceso directo a pantallas sensibles escribiendo la dirección en el navegador.",
   "Usuario no autenticado.",
   "El middleware de autenticación debe evaluar la sesión antes de resolver la ruta y redirigir al "
   "login cuando corresponda; el middleware de administración debe verificar el rol real del usuario.",
   "Si la sesión caducó, se intenta renovar una vez antes de redirigir.",
   "La regla de administración debe leer la identidad del almacén de sesión, no una cookie "
   "inexistente.",
   "Los middlewares de autenticación y de administración del frontend se encuentran comentados o "
   "consultan una cookie que nunca se crea, por lo que las rutas quedan abiertas.",
   "RF-001, RF-009.",
   "Máxima", "Pendiente.")
rf(d, "RF-009", "Autorización por rol en el backend",
   "Cada endpoint sensible exige un rol específico antes de ejecutar la operación.",
   "Asegurar que la seguridad no dependa de la interfaz.",
   "Cualquier cliente de la API.",
   "El servidor resuelve el token, identifica el rol y deniega con estado de autorización cuando el "
   "rol no corresponde al endpoint.",
   "Un token sin rol válido se rechaza aunque la interfaz lo permita.",
   "Las operaciones de administración, tipos y procesamiento de moras requieren rol administrador.",
   "Token de acceso vigente y rol coincidente.",
   "RF-001.",
   "Máxima", "Completada.")
rf(d, "RF-010", "Auditoría de operaciones sensibles",
   "El sistema registra quién realizó qué operación sobre préstamos, pagos, capital y moras.",
   "Poder reconstruir cualquier discrepancia económica ante una revisión.",
   "Sistema, administrador.",
   "Al ejecutar una operación sensible, el servidor escribe una fila de auditoría con usuario, "
   "tabla, tipo de operación, valores anteriores y posteriores, dirección IP y marca de tiempo.",
   "Si la auditoría falla, la operación principal no debe quedar registrada a medias.",
   "Ninguna operación financiera puede desactivar la auditoría.",
   "La tabla de auditoría y el servicio de registro ya existen en el backend.",
   "RF-009.",
   "Alta", "Parcial.")
rf(d, "RF-011", "Configuración del sistema",
   "Los parámetros de negocio editables (tasa de mora diaria y días de gracia) se almacenan en una "
   "tabla de configuración y son consultados por los procesos de cálculo.",
   "Permitir ajustar la política de mora sin modificar código.",
   "Administrador, procesos programados.",
   "El administrador modifica el valor; los procesos de mora leen el valor vigente antes de calcular.",
   "Si el parámetro no existe, se aplica el valor por defecto documentado en el código.",
   "Los valores deben ser numéricos y no negativos.",
   "El servidor valida tipo y rango antes de persistir.",
   "RF-044.",
   "Alta", "Parcial.")

# ------------------------------------------------------------------- 3.2
d.h2("3.2 Gestión de clientes")
d.p(
    "El cliente es la unidad sobre la que se apoya toda la cartera. El módulo cubre el alta, la "
    "consulta y la baja lógica, con identificación única por cédula. El detalle completo de un "
    "cliente con su historial financiero es la principal brecha funcional del módulo."
)
d.table(
    "Consolidado del módulo de clientes",
    ["Código", "Requisito", "Prioridad", "Estado"],
    [
        ["RF-012", "Alta de cliente", "Máxima", "Completada"],
        ["RF-013", "Listado paginado con filtros", "Alta", "Completada"],
        ["RF-014", "Búsqueda por nombre, cédula o teléfono", "Alta", "Parcial"],
        ["RF-015", "Detalle del cliente con historial", "Alta", "Pendiente"],
        ["RF-016", "Edición y baja de clientes", "Alta", "Completada"],
        ["RF-017", "Bloqueo de operación por cliente bloqueado", "Alta", "Completada"],
        ["RF-018", "Historial financiero del cliente", "Alta", "Pendiente"],
        ["RF-019", "Estadísticas del cliente", "Media", "Pendiente"],
    ],
    widths=[0.9, 3.6, 1.2, 1.2],
    align_center_cols=(0, 2, 3),
)
rf(d, "RF-012", "Alta de cliente",
   "El sistema permite registrar un cliente con sus datos de identificación y contacto.",
   "Incorporar deudores verificables a la operación.",
   "Usuario operativo, administrador.",
   "El usuario completa el formulario con nombre, cédula, teléfono, correo y dirección; el sistema "
   "verifica que la cédula no exista y persiste el registro con estado activo.",
   "Si la cédula ya está registrada se muestra un error que apunta al registro existente.",
   "La cédula es el identificador único del cliente.",
   "Nombre obligatorio, cédula obligatoria y única, teléfono y correo con formato válido.",
   "RF-013.",
   "Máxima", "Completada.")
rf(d, "RF-013", "Listado paginado de clientes",
   "El sistema presenta los clientes en páginas con número de página y tamaño definido.",
   "Responder rápido aunque el padrón crezca.",
   "Usuario operativo, administrador.",
   "El usuario abre la lista, navega entre páginas y aplica filtros de estado.",
   "Si la página solicitada supera el total, se devuelve la última página disponible.",
   "El backend interpreta los parámetros de paginación como número de página y límite.",
   "El frontend envía parámetros de desplazamiento en varios servicios, por lo que la navegación "
   "solo avanza de forma confiable en los servicios que envían número de página.",
   "RF-012.",
   "Alta", "Completada.")
rf(d, "RF-014", "Búsqueda de clientes por texto libre",
   "El usuario puede localizar un cliente escribiendo parte de su nombre, cédula o teléfono.",
   "Reducir el tiempo de atención en mostrador.",
   "Usuario operativo, administrador.",
   "El usuario escribe en el campo de búsqueda y el sistema filtra el padrón por coincidencia "
   "parcial.",
   "Sin coincidencias se muestra un estado vacío con la sugerencia de registrar un cliente.",
   "La búsqueda se aplica sobre nombre, cédula y teléfono.",
   "El backend ya soporta el parámetro de búsqueda libre, pero los servicios del frontend no lo "
   "envían.",
   "RF-013.",
   "Alta", "Parcial.")
rf(d, "RF-015", "Detalle del cliente",
   "El sistema debe ofrecer una vista de cliente con su información personal y su actividad "
   "financiera en pestañas.",
   "Dar al gestor una imagen completa antes de decidir un nuevo préstamo.",
   "Usuario operativo, administrador.",
   "Desde el listado, el usuario abre la ficha del cliente, que muestra datos personales, préstamos "
   "activos y cerrados, y pagos recientes.",
   "Si el cliente no tiene operación registrada, la ficha lo indica explícitamente.",
   "La ficha debe reflejar el estado real de cada préstamo.",
   "Actualmente no existe página de detalle de cliente en la aplicación.",
   "RF-012, RF-013.",
   "Alta", "Pendiente.")
rf(d, "RF-016", "Edición y baja de clientes",
   "El sistema permite actualizar los datos de un cliente y desactivarlo sin borrar su historial.",
   "Mantener el padrón vigente sin perder trazabilidad histórica.",
   "Usuario operativo, administrador.",
   "El usuario edita los campos, guarda los cambios o marca la baja; el sistema conserva el registro "
   "para que los préstamos antiguos sigan siendo consultables.",
   "No se permite eliminar un cliente con préstamos en curso; la baja es lógica.",
   "La cédula no puede reasignarse a otro cliente.",
   "El formulario valida los mismos campos que el alta.",
   "RF-012.",
   "Alta", "Completada.")
rf(d, "RF-017", "Bloqueo de operación por cliente bloqueado",
   "El servidor impide crear préstamos a clientes con la cuenta bloqueada.",
   "Evitar otorgar crédito a deudores en mora prolongada.",
   "Usuario operativo.",
   "Al intentar crear un préstamo, el servidor verifica el estado del cliente y deniega la operación "
   "si está bloqueado.",
   "El usuario recibe un mensaje que indica el estado del cliente.",
   "Solo un administrador puede reactivar el cliente.",
   "El estado debe ser activo.",
   "RF-009, RF-025.",
   "Alta", "Completada.")
rf(d, "RF-018", "Historial financiero del cliente",
   "La ficha del cliente debe consolidar sus préstamos, pagos, moras y declaraciones de pérdida.",
   "Concentrar la evidencia crediticia en un solo lugar.",
   "Usuario operativo, administrador.",
   "El sistema consulta los préstamos del cliente y sus pagos asociados, y presenta el resumen "
   "ordenado por fecha.",
   "Si un préstamo fue renovado, se muestra la cadena de renovaciones.",
   "El historial nunca se edita; solo se consulta.",
   "Requiere el detalle de cliente y los endpoints de moras por préstamo.",
   "RF-015, RF-045.",
   "Alta", "Pendiente.")
rf(d, "RF-019", "Estadísticas del cliente",
   "La aplicación debe mostrar indicadores del comportamiento de pago del cliente: puntualidad, "
   "saldo total y mora acumulada.",
   "Apoyar decisiones de renovación con datos objetivos.",
   "Usuario operativo, administrador.",
   "El sistema calcula los indicadores a partir de sus préstamos y los presenta en la ficha.",
   "Sin operaciones registradas los indicadores se muestran en cero.",
   "Los indicadores se calculan en el servidor para evitar discrepancias.",
   "Requiere detalle de cliente e histórico de pagos.",
   "RF-018.",
   "Media", "Pendiente.")

# ------------------------------------------------------------------- 3.3
d.h2("3.3 Solicitudes de préstamo")
d.p(
    "La originación formal mediante solicitudes es el módulo con mayor brecha: el diseño prevé un "
    "flujo de evaluación con aprobación y rechazo, pero en el código actual no existe ninguna "
    "solicitud registrable. El préstamo se crea de forma directa desde el formulario de originación, "
    "por lo que todos los requisitos de este módulo se declaran pendientes."
)
d.table(
    "Consolidado del módulo de solicitudes",
    ["Código", "Requisito", "Prioridad", "Estado"],
    [
        ["RF-020", "Registro de solicitud", "Alta", "Pendiente"],
        ["RF-021", "Flujo de evaluación y decisión", "Alta", "Pendiente"],
        ["RF-022", "Conversión de solicitud en préstamo", "Alta", "Pendiente"],
        ["RF-023", "Notificación del estado de la solicitud", "Media", "Pendiente"],
        ["RF-024", "Permisos del módulo", "Alta", "Pendiente"],
    ],
    widths=[0.9, 3.6, 1.2, 1.2],
    align_center_cols=(0, 2, 3),
)
rf(d, "RF-020", "Registro de solicitud de préstamo",
   "El sistema debe permitir capturar una solicitud con monto solicitado, plazo, tipo de préstamo y "
   "motivo, asociada a un cliente.",
   "Formalizar la petición antes de comprometer capital.",
   "Usuario operativo.",
   "El usuario selecciona el cliente, indica monto y plazo, y guarda la solicitud en estado "
   "pendiente.",
   "Si el cliente está bloqueado la solicitud se rechaza en captura.",
   "Una solicitud no modifica el capital ni genera cuotas.",
   "Monto positivo, plazo dentro de los límites del tipo de préstamo.",
   "RF-012, RF-068.",
   "Alta", "Pendiente.")
rf(d, "RF-021", "Flujo de evaluación, aprobación y rechazo",
   "El sistema debe registrar la evaluación de una solicitud y permitir aprobarla o rechazarla con "
   "motivo.",
   "Separar quien solicita de quien autoriza.",
   "Evaluador, administrador.",
   "La solicitud avanza de pendiente a aprobada o rechazada, dejando registro del evaluador y de la "
   "fecha.",
   "Una solicitud aprobada caduca si no se convierte en préstamo en el plazo definido.",
   "Solo perfiles autorizados pueden decidir.",
   "El estado previo debe ser pendiente.",
   "RF-020, RF-024.",
   "Alta", "Pendiente.")
rf(d, "RF-022", "Conversión de solicitud a préstamo",
   "Una solicitud aprobada debe poder convertirse en préstamo aprovechando los datos capturados.",
   "Evitar la doble captura y el error de transcripción.",
   "Usuario operativo.",
   "El usuario abre la solicitud aprobada, confirma los datos y el sistema crea el préstamo con el "
   "cálculo estándar de cuotas.",
   "Si el capital disponible es insuficiente la conversión se detiene con el aviso correspondiente.",
   "La solicitud aprobada se consume una sola vez.",
   "Monto y plazo ya validados en la solicitud.",
   "RF-021, RF-025, RF-026.",
   "Alta", "Pendiente.")
rf(d, "RF-023", "Notificación del estado de la solicitud",
   "El sistema debe notificar al usuario cuando una solicitud cambie de estado.",
   "Acelerar la respuesta al cliente final.",
   "Sistema, usuario operativo.",
   "Al decidirse la solicitud, se envía una notificación push al usuario responsable.",
   "Si el navegador no tiene suscripción push activa, la notificación queda solo en el registro "
   "interno.",
   "Una notificación por cambio de estado.",
   "Suscripción push configurada.",
   "RF-060.",
   "Media", "Pendiente.")
rf(d, "RF-024", "Permisos del módulo de solicitudes",
   "El sistema debe restringir la decisión de aprobación a los perfiles autorizados.",
   "Preservar la separación de funciones.",
   "Administrador.",
   "El servidor valida el rol antes de ejecutar la aprobación o el rechazo.",
   "Un usuario operativo puede capturar y consultar, pero no decidir.",
   "Aplica la política de roles vigente.",
   "Token con rol válido.",
   "RF-009.",
   "Alta", "Pendiente.")

# ------------------------------------------------------------------- 3.4
d.h2("3.4 Originación y administración de préstamos")
d.p(
    "Este es el módulo más maduro del producto. Crea el préstamo con su cálculo financiero, genera "
    "las cuotas, gestiona renovaciones y pérdidas y mantiene el saldo pendiente actualizado. Las "
    "reglas de cálculo descritas aquí se extrajeron directamente de los servicios del backend y "
    "constituyen la referencia para las pruebas."
)
d.table(
    "Consolidado del módulo de préstamos",
    ["Código", "Requisito", "Prioridad", "Estado"],
    [
        ["RF-025", "Creación de préstamo con cálculo financiero", "Máxima", "Completada"],
        ["RF-026", "Validación de capital disponible", "Máxima", "Completada"],
        ["RF-027", "Generación de cuotas", "Máxima", "Completada"],
        ["RF-028", "Listado y filtros de préstamos", "Alta", "Completada"],
        ["RF-029", "Detalle de préstamo con cuotas y pagos", "Alta", "Completada"],
        ["RF-030", "Renovación de préstamo", "Alta", "Completada"],
        ["RF-031", "Declaración de préstamo perdido", "Alta", "Completada"],
        ["RF-032", "Cierre automático al saldar", "Alta", "Completada"],
        ["RF-033", "Bloqueos por estado terminal", "Alta", "Completada"],
        ["RF-034", "Ajuste de capital del préstamo", "Media", "Parcial"],
        ["RF-035", "Reestructuración de préstamo", "Media", "Pendiente"],
    ],
    widths=[0.9, 3.6, 1.2, 1.2],
    align_center_cols=(0, 2, 3),
)
rf(d, "RF-025", "Creación de préstamo con cálculo financiero",
   "El sistema crea un préstamo calculando el interés total, el monto total y el valor de la cuota a "
   "partir del capital prestado, el porcentaje de interés y el número de cuotas.",
   "Formalizar la deuda con cifras consistentes y reproducibles.",
   "Usuario operativo.",
   "El usuario selecciona el cliente, el tipo de préstamo, el capital y el plazo; el servidor calcula "
   "interés total como capital por interés por número de cuotas, suma el monto total, divide en "
   "cuotas y registra el préstamo activo con saldo pendiente igual al monto total.",
   "Si el cliente está bloqueado o el capital es insuficiente, la creación se deniega antes de "
   "persistir.",
   "El interés se calcula de forma simple por cuota; la cuota se obtiene dividiendo el monto total "
   "entre el número de cuotas y la última cuota absorbe el redondeo.",
   "Capital positivo, porcentaje de interés dentro del rango del tipo de préstamo, número de cuotas "
   "dentro del máximo permitido.",
   "RF-026, RF-027, RF-068.",
   "Máxima", "Completada.")
rf(d, "RF-026", "Validación de capital disponible",
   "El servidor verifica que el capital global cubra el monto prestado antes de desembolsar.",
   "Evitar otorgar dinero que la caja no tiene.",
   "Sistema, usuario operativo.",
   "Al confirmar la creación, se compara el capital disponible con el monto solicitado y, si es "
   "insuficiente, se responde un error sin efectos parciales.",
   "Si el registro de capital no existe, se crea en cero y la operación se rechaza.",
   "Toda salida de capital reduce el saldo global y genera su movimiento.",
   "Se requiere capital igual o mayor al prestado.",
   "RF-050.",
   "Máxima", "Completada.")
rf(d, "RF-027", "Generación de cuotas",
   "El sistema genera la tabla de cuotas del préstamo con número, valor, capital, interés y estado.",
   "Permitir el cobro parcial y el seguimiento por periodo.",
   "Sistema.",
   "Al crear el préstamo se insertan las cuotas en estado pendiente; la última cuota ajusta capital e "
   "interés para que la suma exacta coincida con el total del préstamo.",
   "Si el cálculo no cuadra por redondeo, el ajuste se concentra en la última cuota.",
   "La suma de los valores de cuota debe ser igual al monto total con tolerancia de un centavo.",
   "La validación de cuadre se realiza dentro de la misma transacción de creación.",
   "RF-025.",
   "Máxima", "Completada.")
rf(d, "RF-028", "Listado y filtros de préstamos",
   "El sistema presenta los préstamos paginados con filtros por estado, tipo, cliente y rango de "
   "fechas.",
   "Localizar operaciones con rapidez en carteras grandes.",
   "Usuario operativo, administrador.",
   "El usuario aplica filtros y el sistema devuelve las páginas correspondientes con sus totales.",
   "Sin resultados se muestra el estado vacío con la opción de crear un préstamo.",
   "Los estados disponibles son activo, pagado, perdido y renovado.",
   "El frontend envía desplazamiento en lugar de número de página, por lo que la paginación solo "
   "funciona de forma confiable en los servicios que envían número de página.",
   "RF-025.",
   "Alta", "Completada.")
rf(d, "RF-029", "Detalle de préstamo",
   "La vista de préstamo muestra los datos financieros, el estado, la lista de cuotas y los pagos "
   "registrados.",
   "Dar al gestor el contexto completo en la atención.",
   "Usuario operativo, administrador.",
   "El usuario abre el préstamo y consulta capital, interés, saldo, cuotas con sus estados y el "
   "histórico de pagos.",
   "Si el préstamo está cerrado, las acciones de pago y renovación no se muestran.",
   "Las acciones disponibles dependen del estado: registrar pago, renovar y marcar como perdido solo "
   "en préstamos activos.",
   "El préstamo debe existir y estar visible para el usuario.",
   "RF-028, RF-036.",
   "Alta", "Completada.")
rf(d, "RF-030", "Renovación de préstamo",
   "El sistema permite renovar un préstamo activo aplicando un abono al saldo y creando un nuevo "
   "préstamo con las condiciones actualizadas.",
   "Recuperar cartera y reiniciar el ciclo de crédito con el saldo vivo.",
   "Usuario operativo.",
   "El usuario indica abono, nuevo interés y nuevo plazo; el servidor valida, descuenta el abono, "
   "calcula el nuevo capital, crea el préstamo derivado y marca el original como renovado.",
   "Si el abono supera el saldo se deniega la operación; si el préstamo no está activo, la "
   "renovación no está permitida.",
   "La renovación solo procede desde estado activo; el capital nuevo es saldo menos abono.",
   "Abono no mayor que el saldo pendiente y valores de interés y plazo válidos.",
   "RF-029, RF-050.",
   "Alta", "Completada.")
rf(d, "RF-031", "Declaración de préstamo perdido",
   "El sistema permite marcar un préstamo activo como perdido, descontar su saldo del capital y "
   "registrar el motivo.",
   "Registrar contablemente la pérdida y liberar el capital comprometido.",
   "Usuario operativo, administrador.",
   "El usuario indica fecha y motivo; el servidor guarda el registro de pérdida, cambia el estado, "
   "descuenta el saldo del capital global y escribe el movimiento correspondiente.",
   "Si el préstamo no está activo, la operación se deniega; si el capital no alcanza, la operación "
   "se aborta sin efectos parciales.",
   "El valor perdido es el saldo pendiente al momento de la declaración.",
   "Fecha válida y motivo opcional.",
   "RF-050.",
   "Alta", "Completada.")
rf(d, "RF-032", "Cierre automático al saldar",
   "El sistema cambia automáticamente el préstamo a estado pagado cuando su saldo llega a cero.",
   "Cerrar la deuda sin intervención manual y liberar al cliente.",
   "Sistema.",
   "Tras cada pago, si el saldo resultante es menor o igual a cero, el préstamo pasa a pagado y las "
   "cuotas pendientes se ajustan.",
   "Si el saldo se aproxima a cero dentro de la tolerancia, se fija exactamente a cero.",
   "Ningún préstamo pagado admite nuevos pagos.",
   "El cálculo de saldo se realiza en el servidor dentro de la misma transacción del pago.",
   "RF-036.",
   "Alta", "Completada.")
rf(d, "RF-033", "Bloqueos por estado terminal",
   "El sistema impide renovar o declarar perdido un préstamo que ya está pagado, perdido o renovado.",
   "Proteger la coherencia de los estados del portafolio.",
   "Usuario operativo.",
   "Antes de ejecutar la acción, el servidor verifica el estado y responde con un mensaje que "
   "explica la restricción.",
   "La restricción se aplica también si la interfaz permitiera el botón.",
   "Solo el estado activo admite renovación y pérdida.",
   "Estado vigente del préstamo.",
   "RF-030, RF-031.",
   "Alta", "Completada.")
rf(d, "RF-034", "Ajuste de capital del préstamo",
   "El sistema permite corregir el capital de un préstamo con trazabilidad del movimiento resultante.",
   "Subsanar errores de captura sin romper el libro de capital.",
   "Administrador.",
   "El administrador indica el nuevo capital; el servidor recalcula intereses y cuotas, y registra "
   "el ajuste como movimiento de capital.",
   "Si el nuevo capital es inválido o el préstamo está cerrado, la operación se deniega.",
   "Toda corrección queda documentada con usuario y fecha.",
   "Préstamo activo y capital positivo.",
   "RF-050.",
   "Media", "Parcial.")
rf(d, "RF-035", "Reestructuración de préstamo",
   "El sistema debe permitir renegociar plazo e interés de un préstamo en mora generando un plan de "
   "pagos nuevo sin cancelar el histórico.",
   "Recuperar cartera problemática antes de declararla perdida.",
   "Administrador.",
   "El administrador propone el nuevo plan, el sistema lo aprueba y genera las cuotas de "
   "reestructuración vinculadas al préstamo original.",
   "Una reestructuración múltiple sobre el mismo préstamo exige cerrar la anterior.",
   "La reestructuración no cambia el capital ya desembolsado.",
   "Requiere el modelo de estados y el libro de capital.",
   "RF-030, RF-050.",
   "Media", "Pendiente.")
# ------------------------------------------------------------------- 3.5
d.h2("3.5 Registro de pagos")
d.p(
    "El cobro es el punto donde el sistema se expone a errores de caja. Por ello el backend valida el "
    "desglose del pago contra el valor total con tolerancia de un centavo, exige idempotencia y "
    "actualiza saldo, cuota y capital en una sola transacción. La brecha principal del módulo está en "
    "la consulta histórica global y en la ausencia de reversión de pagos."
)
d.table(
    "Consolidado del módulo de pagos",
    ["Código", "Requisito", "Prioridad", "Estado"],
    [
        ["RF-036", "Registro de pago con desglose", "Máxima", "Completada"],
        ["RF-037", "Validación de cuadre del pago", "Máxima", "Completada"],
        ["RF-038", "Actualización de saldo, cuota y capital", "Máxima", "Completada"],
        ["RF-039", "Idempotencia en el registro de pagos", "Máxima", "Completada"],
        ["RF-040", "Historial de pagos del préstamo", "Alta", "Completada"],
        ["RF-041", "Historial global de pagos", "Alta", "Parcial"],
        ["RF-042", "Reversión o ajuste de pagos", "Alta", "Pendiente"],
        ["RF-043", "Comprobante de pago", "Media", "Pendiente"],
    ],
    widths=[0.9, 3.6, 1.2, 1.2],
    align_center_cols=(0, 2, 3),
)
rf(d, "RF-036", "Registro de pago con desglose",
   "El sistema permite registrar un pago desglosado en capital, interés y mora contra una cuota "
   "específica.",
   "Cobrar dejando evidencia del destino de cada peso.",
   "Usuario operativo.",
   "El usuario selecciona el préstamo, la cuota y el monto; indica el reparto entre capital, interés "
   "y mora; el sistema valida y persiste el pago con su fecha.",
   "Si el monto no alcanza para cubrir la cuota más mora, el sistema lo acepta como pago parcial "
   "dentro del reparto informado.",
   "El desglose debe sumar el valor pagado; no se admiten montos negativos.",
   "Los tres componentes son obligatorios y su suma debe coincidir con el valor pagado dentro de un "
   "centavo.",
   "RF-037, RF-038, RF-039.",
   "Máxima", "Completada.")
rf(d, "RF-037", "Validación de cuadre del pago",
   "El servidor rechaza cualquier pago cuyo desglose no cuadre con el total o que supere lo adeudado.",
   "Impedir descuadres de caja que distorsionen la utilidad.",
   "Sistema.",
   "Antes de persistir, el servidor compara capital más interés más mora contra el valor pagado con "
   "tolerancia de un centavo y verifica que el valor no supere la suma de la cuota y la mora "
   "pendiente.",
   "Un descuadre responde con un mensaje que indica el faltante o el excedente.",
   "La tolerancia es de 0,01; por debajo se acepta y por encima se rechaza.",
   "Monto no negativo y cuota existente.",
   "RF-036.",
   "Máxima", "Completada.")
rf(d, "RF-038", "Actualización de saldo, cuota y capital",
   "Tras cada pago el sistema descuenta el capital pagado del saldo del préstamo, actualiza el estado "
   "de la cuota y suma el capital al fondo global.",
   "Mantener coherentes la deuda, la caja y la cuota.",
   "Sistema.",
   "En una sola transacción se reduce el saldo pendiente, se suma el capital pagado al capital "
   "global, se registra el movimiento de capital, se marca la cuota como pagada o parcial y se evalúa "
   "el cierre automático.",
   "Si cualquier paso falla, la operación completa se revierte.",
   "El capital global nunca puede quedar negativo por un pago.",
   "Cuota y préstamo existentes, capital global inicializado.",
   "RF-032, RF-050.",
   "Máxima", "Completada.")
rf(d, "RF-039", "Idempotencia en el registro de pagos",
   "La repetición accidental de un mismo pago no debe duplicar el cobro.",
   "Blindar la caja contra dobles clics y reintentos de red.",
   "Usuario operativo, cliente HTTP.",
   "Cada petición de pago lleva una clave única; si el servidor ya procesó esa clave devuelve la "
   "respuesta original en lugar de repetir el efecto.",
   "Una clave reutilizada con un cuerpo distinto se rechaza con conflicto.",
   "La clave identifica la operación, no la sesión.",
   "Encabezado de idempotencia presente en la solicitud.",
   "RF-036.",
   "Máxima", "Completada.")
rf(d, "RF-040", "Historial de pagos del préstamo",
   "La vista de préstamo lista los pagos registrados con fecha, valor y desglose.",
   "Permitir la conciliación frente al cliente.",
   "Usuario operativo, administrador.",
   "Al abrir el préstamo se listan sus pagos ordenados por fecha, con el desglose de cada uno.",
   "Sin pagos se muestra el estado vacío.",
   "El histórico no admite edición desde la interfaz.",
   "Préstamo existente.",
   "RF-029.",
   "Alta", "Completada.")
rf(d, "RF-041", "Historial global de pagos",
   "La aplicación debe ofrecer un listado global de todos los pagos con filtros por cliente, fecha y "
   "tipo de pago.",
   "Conciliar la caja del día sin recorrer préstamo por préstamo.",
   "Usuario operativo, administrador.",
   "El usuario abre el historial, filtra y pagina los pagos de toda la operación.",
   "Sin coincidencias se muestra el estado vacío.",
   "El endpoint devuelve una estructura paginada con elementos, total y páginas.",
   "El servicio del frontend declara una lista plana mientras el servidor devuelve un objeto "
   "paginado, por lo que la pantalla de historial redirige al detalle de préstamo.",
   "RF-013, RF-040.",
   "Alta", "Parcial.")
rf(d, "RF-042", "Reversión o ajuste de pagos",
   "El sistema debe permitir anular un pago registrado por error, con motivo y auditoría.",
   "Corregir cobros mal registrados sin borrar evidencia.",
   "Administrador.",
   "El administrador anula el pago; el sistema revierte el saldo, la cuota y el capital, y deja el "
   "registro anulado en lugar de eliminarlo.",
   "No se admite anular pagos de un préstamo cerrado sin reabrirlo.",
   "Toda anulación genera movimiento de capital en sentido inverso.",
   "Motivo obligatorio y rol administrador.",
   "RF-038, RF-010.",
   "Alta", "Pendiente.")
rf(d, "RF-043", "Comprobante de pago",
   "El sistema debe poder generar un comprobante descargable del pago registrado.",
   "Entregar al cliente evidencia de su abono.",
   "Usuario operativo.",
   "Tras registrar el pago, el usuario descarga el comprobante en PDF con los datos del préstamo, la "
   "cuota y el desglose.",
   "Si el generador falla, el pago sigue registrado y el comprobante queda pendiente de emisión.",
   "El comprobante no sustituye el registro contable del pago.",
   "Motor de generación de PDF del backend.",
   "RF-036, RF-055.",
   "Media", "Pendiente.")

# ------------------------------------------------------------------- 3.6
d.h2("3.6 Mora y cobranza")
d.p(
    "El cálculo de moras es el proceso programado más importante del producto: corre a diario, aplica "
    "la tasa y los días de gracia configurados y alimenta el cobro. Sin embargo, la capa de "
    "presentación no se conecta al endpoint real del servidor, por lo que la consulta de moras desde "
    "la interfaz devuelve errores de recurso inexistente. El módulo de cobranza presenta una lista "
    "siempre vacía por un desajuste en la forma de los datos."
)
d.table(
    "Consolidado del módulo de mora y cobranza",
    ["Código", "Requisito", "Prioridad", "Estado"],
    [
        ["RF-044", "Cálculo diario de moras", "Máxima", "Completada"],
        ["RF-045", "Consulta de moras por préstamo", "Alta", "Pendiente"],
        ["RF-046", "Procesamiento manual de moras", "Alta", "Parcial"],
        ["RF-047", "Gestión de cobranza", "Alta", "Parcial"],
        ["RF-048", "Recordatorios de cobro", "Alta", "Completada"],
        ["RF-049", "Centro de notificaciones", "Media", "Pendiente"],
    ],
    widths=[0.9, 3.6, 1.2, 1.2],
    align_center_cols=(0, 2, 3),
)
rf(d, "RF-044", "Cálculo diario de moras",
   "El servidor ejecuta a diario un proceso que detecta cuotas vencidas, aplica la tasa configurada y "
   "registra la mora correspondiente.",
   "Devengar la penalización de forma automática y auditable.",
   "Sistema.",
   "El planificador diario recorre las cuotas vencidas dentro de la ventana de gracia, calcula la "
   "mora, la persiste en estado generada y la asocia a la cuota y al préstamo.",
   "Si un cálculo falla, se reintenta en la siguiente ejecución sin duplicar moras del mismo día.",
   "La tasa diaria y los días de gracia provienen de la configuración del sistema; cada cuota solo "
   "genera una mora por fecha.",
   "Cuota vencida y sin mora registrada para esa fecha.",
   "RF-011.",
   "Máxima", "Completada.")
rf(d, "RF-045", "Consulta de moras por préstamo",
   "El sistema debe listar las moras de un préstamo y permitir su consulta individual.",
   "Sustentar la discusión de cobro con el detalle de la penalización.",
   "Usuario operativo, administrador.",
   "Desde el préstamo o el módulo de moras, el usuario consulta las moras generadas con su fecha y "
   "valor.",
   "Sin moras se muestra el estado vacío.",
   "Solo se listan las moras en estado generada.",
   "La interfaz invoca rutas con prefijo plural mientras el servidor expone un prefijo distinto, por "
   "lo que las consultas terminan en recurso inexistente.",
   "RF-044.",
   "Alta", "Pendiente.")
rf(d, "RF-046", "Procesamiento manual de moras",
   "El administrador puede ejecutar el cálculo de moras en el momento en lugar de esperar al "
   "proceso diario.",
   "Corregir inmediatamente un desfase detectado en auditoría.",
   "Administrador.",
   "El administrador dispara el procesamiento; el servidor ejecuta el mismo algoritmo del proceso "
   "programado y devuelve el total de moras generadas.",
   "Si el proceso falla, se responde el detalle del error y no se genera mora parcial.",
   "La operación requiere rol administrador.",
   "Configuración del sistema disponible.",
   "RF-011, RF-044.",
   "Alta", "Parcial.")
rf(d, "RF-047", "Gestión de cobranza",
   "El módulo de cobranza debe presentar las cuotas vencidas con su cliente, saldo y acción sugerida, "
   "para gestionar el cobro.",
   "Organizar la jornada de cobro sobre las deudas realmente vencidas.",
   "Usuario operativo.",
   "El usuario abre la agenda, revisa las cuotas vencidas del día, registra el contacto y marca las "
   "acciones realizadas.",
   "Sin vencimientos se muestra el estado vacío con la fecha consultada.",
   "La agenda se alimenta de cuotas vencidas y moras generadas.",
   "La pantalla existe pero interpreta una forma de datos que el servidor no devuelve, por lo que la "
   "lista resulta siempre vacía.",
   "RF-044, RF-045.",
   "Alta", "Parcial.")
rf(d, "RF-048", "Recordatorios de cobro",
   "El servidor envía recordatorios push a los usuarios responsables sobre vencimientos y cuotas "
   "atrasadas.",
   "Reducir la mora temprana con avisos oportunos.",
   "Sistema, usuario operativo.",
   "El planificador detecta vencimientos próximos o atrasados y envía una notificación push a las "
   "suscripciones registradas.",
   "Si el navegador no tiene suscripción o la suscripción caducó, se descarta sin afectar el proceso.",
   "Un aviso por evento y por destinatario.",
   "Suscripciones push válidas y configuración de llaves del servicio.",
   "RF-060.",
   "Alta", "Completada.")
rf(d, "RF-049", "Centro de notificaciones",
   "La aplicación debe ofrecer una bandeja de notificaciones donde el usuario consulte los avisos "
   "recibidos.",
   "No depender de que el navegador muestre la notificación en el momento exacto.",
   "Usuario operativo.",
   "El usuario abre la bandeja, lee los avisos sin marcar y los marca como leídos.",
   "Los avisos antiguos se archivan tras un periodo configurable.",
   "Los avisos provienen de eventos de cobro, solicitudes y seguridad.",
   "Requiere almacenamiento de avisos en servidor.",
   "RF-048.",
   "Media", "Pendiente.")

# ------------------------------------------------------------------- 3.7
d.h2("3.7 Capital, caja y reportes financieros")
d.p(
    "El capital es el recurso que sostiene la operación y el libro de movimientos su contabilidad "
    "sencilla. El backend registra cada salida y entrada con su tipo y su fecha; la interfaz ya "
    "consulta el saldo y el detalle de movimientos. Los reportes de cartera y cobranza existen en el "
    "servidor pero no tienen pantalla propia."
)
d.table(
    "Consolidado del módulo financiero",
    ["Código", "Requisito", "Prioridad", "Estado"],
    [
        ["RF-050", "Capital global y libro de movimientos", "Máxima", "Completada"],
        ["RF-051", "Ingresos y egresos de caja", "Alta", "Pendiente"],
        ["RF-052", "Reporte de ganancias y pérdidas", "Alta", "Completada"],
        ["RF-053", "Reporte de cartera", "Alta", "Parcial"],
        ["RF-054", "Reporte de cobranza", "Alta", "Parcial"],
        ["RF-055", "Exportación a Excel y PDF", "Alta", "Completada"],
    ],
    widths=[0.9, 3.6, 1.2, 1.2],
    align_center_cols=(0, 2, 3),
)
rf(d, "RF-050", "Capital global y libro de movimientos",
   "El sistema mantiene el capital disponible y registra cada movimiento con tipo, valor, fecha y "
   "préstamo asociado.",
   "Tener una contabilidad mínima del recurso prestado.",
   "Sistema, administrador.",
   "Al desembolsar se descuenta el capital, al cobrar se suma el capital pagado, al declarar la "
   "pérdida se descuenta el saldo y cada operación genera su fila de movimiento; la interfaz muestra "
   "el saldo actual y el historial paginado.",
   "Si el capital es insuficiente, la salida se deniega antes de aplicarse.",
   "Los tipos de movimiento distinguen préstamo otorgado, pago recibido, pérdida y ajustes.",
   "Capital inicializado y transacción válida.",
   "RF-026, RF-031, RF-038.",
   "Máxima", "Completada.")
rf(d, "RF-051", "Ingresos y egresos de caja",
   "El sistema debe registrar movimientos de caja ajenos a los préstamos, como gastos de operación y "
   "aportes de capital.",
   "Reflejar la realidad económica completa del negocio, no solo la cartera.",
   "Administrador.",
   "El administrador registra el movimiento con concepto, valor y fecha; el sistema lo refleja en el "
   "saldo de capital cuando corresponde.",
   "Los egresos no pueden dejar el capital en negativo.",
   "Toda entrada o salida exige concepto y fecha.",
   "Requiere el libro de movimientos ampliado con concepto libre.",
   "RF-050.",
   "Alta", "Pendiente.")
rf(d, "RF-052", "Reporte de ganancias y pérdidas",
   "El sistema genera el reporte de utilidad por intereses cobrados y el de pérdidas por préstamos "
   "incobrables en un rango de fechas.",
   "Conocer la rentabilidad real del portafolio.",
   "Administrador.",
   "El usuario selecciona el periodo; el sistema calcula intereses cobrados, capital perdido y "
   "resultado neto, y los presenta con detalle por préstamo.",
   "Sin operaciones en el periodo el reporte lo indica explícitamente.",
   "Las ganancias consideran intereses efectivamente cobrados, no devengados.",
   "Histórico de pagos y de declaraciones de pérdida.",
   "RF-036, RF-031.",
   "Alta", "Completada.")
rf(d, "RF-053", "Reporte de cartera",
   "El sistema debe generar el estado de la cartera: saldos por préstamo, antigüedad y distribución "
   "por estado.",
   "Medir la exposición del negocio en cada momento.",
   "Administrador.",
   "El usuario solicita el reporte por periodo; el sistema devuelve el detalle de saldos y su "
   "agrupación por estado y antigüedad.",
   "Sin cartera vigente el reporte devuelve ceros y la nota correspondiente.",
   "El capital pendiente se toma del saldo del préstamo.",
   "El endpoint existe en el servidor pero no tiene pantalla asociada.",
   "RF-028, RF-050.",
   "Alta", "Parcial.")
rf(d, "RF-054", "Reporte de cobranza",
   "El sistema debe informar lo cobrado por periodo, desglosado por capital, interés y mora.",
   "Comparar lo planificado contra lo efectivamente recaudado.",
   "Administrador.",
   "El usuario define el periodo y el sistema presenta los totales cobrados con su desglose y el "
   "detalle por día.",
   "Sin cobros en el periodo se muestra el estado vacío.",
   "Solo se contabilizan pagos confirmados.",
   "Histórico de pagos; el endpoint está disponible sin interfaz.",
   "RF-036.",
   "Alta", "Parcial.")
rf(d, "RF-055", "Exportación a Excel y PDF",
   "El sistema permite descargar los reportes financieros en formatos Excel y PDF respetando los "
   "filtros aplicados.",
   "Compartir información con contabilidad y socios.",
   "Administrador, usuario operativo.",
   "El usuario elige el formato; el servidor genera el archivo y el cliente lo descarga sin "
   "abrir otra pestaña.",
   "Si la generación falla, se muestra el error y los filtros se conservan.",
   "El archivo refleja exactamente el periodo filtrado.",
   "Generadores de Excel y PDF del backend.",
   "RF-052, RF-053, RF-054.",
   "Alta", "Completada.")

# ------------------------------------------------------------------- 3.8
d.h2("3.8 Tablero de indicadores")
d.p(
    "El tablero es la primera pantalla del producto y concentra los indicadores de salud del negocio. "
    "Hoy se construye a partir de varias consultas independientes; el servidor ofrece una consulta "
    "consolidada que el frontend no utiliza todavía, y la distribución de cartera se interpreta con la "
    "estructura equivocada."
)
d.table(
    "Consolidado del módulo de tablero",
    ["Código", "Requisito", "Prioridad", "Estado"],
    [
        ["RF-056", "Indicadores principales", "Alta", "Completada"],
        ["RF-057", "Distribución de cartera por estado", "Alta", "Parcial"],
        ["RF-058", "Indicadores de cobranza y mora", "Alta", "Parcial"],
        ["RF-059", "Consulta consolidada del tablero", "Media", "Pendiente"],
    ],
    widths=[0.9, 3.6, 1.2, 1.2],
    align_center_cols=(0, 2, 3),
)
rf(d, "RF-056", "Indicadores principales del tablero",
   "El tablero muestra capital disponible, préstamos activos, clientes registrados y monto cobrado.",
   "Dar visibilidad inmediata del estado del negocio.",
   "Usuario operativo, administrador.",
   "Al abrir la aplicación se consultan los indicadores y se presentan con su formato monetario.",
   "Si alguna consulta falla, el tablero muestra los indicadores disponibles y la advertencia.",
   "Los valores deben reflejar el cierre del día en curso.",
   "Endpoints de capital, préstamos y clientes.",
   "RF-050, RF-028.",
   "Alta", "Completada.")
rf(d, "RF-057", "Distribución de cartera por estado",
   "El tablero muestra la proporción de cartera activa, pagada, perdida y renovada.",
   "Detectar de un vistazo la concentración de riesgo.",
   "Usuario operativo, administrador.",
   "El sistema agrupa los préstamos por estado y presenta la distribución como gráfico.",
   "Sin préstamos registrados se muestra un estado vacío.",
   "Los porcentajes deben sumar el total de la cartera consultada.",
   "El frontend interpreta la respuesta como un mapa de etiquetas cuando el servidor devuelve una "
   "lista de pares, por lo que la gráfica queda vacía.",
   "RF-028.",
   "Alta", "Parcial.")
rf(d, "RF-058", "Indicadores de cobranza y mora",
   "El tablero debe informar el monto vencido, la mora pendiente y el cobro del día.",
   "Anticiparse al cierre de caja.",
   "Usuario operativo, administrador.",
   "El sistema calcula los indicadores de vencimiento y los presenta junto a los principales.",
   "Sin vencimientos el indicador se muestra en cero.",
   "El cobro del día se considera por fecha de pago.",
   "Endpoints de moras y pagos con el desajuste de rutas ya descrito.",
   "RF-044, RF-041.",
   "Alta", "Parcial.")
rf(d, "RF-059", "Consulta consolidada del tablero",
   "El servidor debe ofrecer una única consulta que resuelva todos los indicadores del tablero con "
   "el mismo criterio de fecha.",
   "Reducir las peticiones de apertura y evitar cifras incoherentes entre sí.",
   "Cliente web.",
   "El cliente llama una sola vez al endpoint consolidado y pinta todos los indicadores con la "
   "respuesta.",
   "Si la consulta consolidada falla, el cliente puede degradar al esquema de consultas múltiples.",
   "Un solo punto de verdad para el criterio de corte.",
   "El endpoint existe en el backend pero el frontend realiza varias consultas independientes.",
   "RF-056.",
   "Media", "Pendiente.")

# ------------------------------------------------------------------- 3.9
d.h2("3.9 Comunicaciones con el usuario")
d.p(
    "El canal push es el único efectivamente operativo y aun así depende de variables de entorno que "
    "no están configuradas en el cliente. Correo, mensajes de texto y mensajería instantánea no "
    "existen en ninguna capa."
)
d.table(
    "Consolidado del módulo de comunicaciones",
    ["Código", "Requisito", "Prioridad", "Estado"],
    [
        ["RF-060", "Notificaciones web push", "Alta", "Parcial"],
        ["RF-061", "Notificaciones por correo", "Alta", "Pendiente"],
        ["RF-062", "Notificaciones por texto y mensajería", "Media", "Pendiente"],
        ["RF-063", "Plantillas de mensajes", "Media", "Pendiente"],
    ],
    widths=[0.9, 3.6, 1.2, 1.2],
    align_center_cols=(0, 2, 3),
)
rf(d, "RF-060", "Notificaciones web push",
   "El usuario puede suscribir su navegador a notificaciones y el servidor envía avisos sobre "
   "vencimientos y eventos de la operación.",
   "Avisar sin depender de que el usuario tenga la aplicación abierta.",
   "Usuario operativo, sistema.",
   "El usuario autoriza las notificaciones, el cliente registra la suscripción en el servidor y los "
   "procesos programados envían los avisos correspondientes.",
   "Si el navegador rechaza el permiso, la operación se registra como no disponible.",
   "La suscripción se elimina al desuscribirse o caducar.",
   "El cliente lee llaves de entorno de variables de desarrollo que no están definidas, por lo que la "
   "suscripción no llega a registrarse en el navegador.",
   "RF-048.",
   "Alta", "Parcial.")
rf(d, "RF-061", "Notificaciones por correo",
   "El sistema debe enviar correos por eventos relevantes: creación de préstamo, cambio de contraseña "
   "y recordatorios de pago.",
   "Llegar a usuarios que no trabajan con la pestaña abierta.",
   "Sistema.",
   "Ante el evento, el sistema compone el mensaje con la plantilla correspondiente y lo envía al "
   "correo registrado.",
   "Un fallo de envío no debe revertir el evento de negocio.",
   "Las plantillas deben ser editables sin desplegar código.",
   "Requiere servidor de correo configurado.",
   "RF-063.",
   "Alta", "Pendiente.")
rf(d, "RF-062", "Notificaciones por texto y mensajería",
   "El sistema debe poder enviar avisos por mensaje de texto y por mensajería instantánea al cliente "
   "final.",
   "Comunicarse con deudores que no usan la aplicación.",
   "Sistema.",
   "Ante un vencimiento, el sistema envía el aviso al número registrado mediante el proveedor "
   "contratado.",
   "Sin proveedor o sin consentimiento, el envío se omite y queda registrado.",
   "Se respetan las ventanas horarias de envío.",
   "Integración con proveedor externo.",
   "RF-063.",
   "Media", "Pendiente.")
rf(d, "RF-063", "Plantillas de mensajes",
   "El sistema debe gestionar plantillas de mensajes con variables reemplazables para cada canal.",
   "Unificar el tono y reducir el trabajo de redacción.",
   "Administrador.",
   "El administrador crea o edita la plantilla, define las variables y la previsualiza antes de "
   "activarla.",
   "Una plantilla activada no puede eliminarse si tiene envíos en curso.",
   "Toda plantilla exige asunto y cuerpo.",
   "Almacenamiento de plantillas y motor de sustitución.",
   "RF-061, RF-062.",
   "Media", "Pendiente.")

# ------------------------------------------------------------------ 3.10
d.h2("3.10 Integraciones externas")
d.p(
    "Ninguna integración externa está construida. Conviene señalar que la pantalla de importación de "
    "extractos existe con datos de prueba inventados, lo que contradice la política del proyecto de no "
    "mostrar información ficticia en la interfaz; este comportamiento debe corregirse antes de "
    "entregar el módulo."
)
d.table(
    "Consolidado del módulo de integraciones",
    ["Código", "Requisito", "Prioridad", "Estado"],
    [
        ["RF-064", "Pasarela de pago", "Media", "Pendiente"],
        ["RF-065", "Scoring y buró de crédito", "Media", "Pendiente"],
        ["RF-066", "Firma electrónica de contratos", "Media", "Pendiente"],
        ["RF-067", "Importación de extractos bancarios", "Media", "Pendiente"],
    ],
    widths=[0.9, 3.6, 1.2, 1.2],
    align_center_cols=(0, 2, 3),
)
rf(d, "RF-064", "Integración con pasarela de pago",
   "El sistema debe permitir pagar cuotas mediante una pasarela de pago en línea.",
   "Ampliar los medios de cobro más allá del efectivo.",
   "Cliente final, sistema.",
   "El usuario selecciona pagar en línea, la pasarela confirma la transacción y el sistema registra "
   "el pago con la referencia externa.",
   "Una transacción no conciliada queda pendiente y no descuenta saldo.",
   "Ningún pago se registra sin confirmación de la pasarela.",
   "Credenciales y contrato con el proveedor.",
   "RF-036.",
   "Media", "Pendiente.")
rf(d, "RF-065", "Scoring y buró de crédito",
   "El sistema debe consultar el historial crediticio del cliente y derivar un puntaje para apoyar la "
   "evaluación.",
   "Cuantificar el riesgo antes de desembolsar.",
   "Evaluador, sistema.",
   "Durante la evaluación, el sistema consulta el buró, recibe el puntaje y lo adjunta a la "
   "solicitud.",
   "Sin respuesta del buró, la evaluación continúa con la advertencia correspondiente.",
   "El puntaje es informativo y no sustituye la decisión humana.",
   "Convenio con el proveedor de información.",
   "RF-021.",
   "Media", "Pendiente.")
rf(d, "RF-066", "Firma electrónica de contratos",
   "El sistema debe generar el contrato del préstamo y recoger la firma electrónica del cliente.",
   "Sustituir el papel y agilizar la entrega.",
   "Cliente final, usuario operativo.",
   "Al aprobar la solicitud, el sistema emite el contrato, lo envía a firma y archiva el documento "
   "firmado junto al préstamo.",
   "Sin firma el préstamo no se desembolsa cuando el flujo lo exija.",
   "El documento firmado forma parte del expediente del préstamo.",
   "Proveedor de firma y almacenamiento de documentos.",
   "RF-022.",
   "Media", "Pendiente.")
rf(d, "RF-067", "Importación de extractos bancarios",
   "El sistema debe leer extractos bancarios y conciliarlos con los pagos registrados.",
   "Acelerar la conciliación de cobros por transferencia.",
   "Usuario operativo, administrador.",
   "El usuario carga el archivo, el sistema interpreta las transacciones, las propone contra los "
   "pagos pendientes y permite confirmar la conciliación.",
   "Transacciones no reconocidas quedan en una lista de excepciones.",
   "Ningún archivo importado se persiste sin confirmación del usuario.",
   "La pantalla actual devuelve datos simulados en lugar de leer el archivo; debe reemplazarse por "
   "el procesamiento real.",
   "RF-036.",
   "Media", "Pendiente.")

# ------------------------------------------------------------------ 3.11
d.h2("3.11 Configuración, catálogos y plataforma")
d.p(
    "Los catálogos de tipo de préstamo y tipo de pago están completos en ambas capas. En cambio, los "
    "requisitos de plataforma que afectan a todo el producto, como la paginación consistente, el modo "
    "sin conexión, la actualización de la aplicación y el soporte multiempresa, se encuentran en "
    "distintos grados de madurez."
)
d.table(
    "Consolidado del módulo de configuración y plataforma",
    ["Código", "Requisito", "Prioridad", "Estado"],
    [
        ["RF-068", "Catálogo de tipos de préstamo", "Alta", "Completada"],
        ["RF-069", "Catálogo de tipos de pago", "Alta", "Completada"],
        ["RF-070", "Paginación consistente", "Alta", "Parcial"],
        ["RF-071", "Operación sin conexión", "Media", "Parcial"],
        ["RF-072", "Actualización de la aplicación", "Alta", "Parcial"],
        ["RF-073", "Multiempresa", "Media", "Pendiente"],
        ["RF-074", "Seguridad de la plataforma", "Máxima", "Pendiente"],
        ["RF-075", "Respaldo y recuperación", "Máxima", "Pendiente"],
    ],
    widths=[0.9, 3.6, 1.2, 1.2],
    align_center_cols=(0, 2, 3),
)
rf(d, "RF-068", "Catálogo de tipos de préstamo",
   "El administrador administra los tipos de préstamo con su nombre, interés mensual y máximo de "
   "cuotas.",
   "Parametrizar la oferta de crédito sin tocar código.",
   "Administrador.",
   "El administrador crea, edita y desactiva tipos; los formularios de originación listan los tipos "
   "activos.",
   "No se permite eliminar un tipo con préstamos asociados; se desactiva.",
   "Interés mensual mayor que cero y cuotas dentro del rango permitido.",
   "Nombre obligatorio y único.",
   "RF-025.",
   "Alta", "Completada.")
rf(d, "RF-069", "Catálogo de tipos de pago",
   "El administrador administra los tipos de pago disponibles al registrar un cobro.",
   "Reflejar los medios de cobro reales del negocio.",
   "Administrador.",
   "El administrador crea, edita y desactiva tipos de pago; el formulario de pago lista los activos.",
   "No se permite eliminar un tipo con pagos asociados.",
   "Todo cobro debe corresponder a un tipo de pago activo.",
   "Nombre obligatorio y único.",
   "Formulario de pago.",
   "Alta", "Completada.")
rf(d, "RF-070", "Paginación consistente",
   "Todos los listados del sistema deben usar el mismo contrato de paginación con número de página, "
   "tamaño y total.",
   "Que la navegación entre páginas sea predecible en toda la aplicación.",
   "Cliente web.",
   "El cliente envía número de página y tamaño, y recibe elementos, total y total de páginas.",
   "Una página fuera de rango devuelve la última disponible.",
   "El contrato del servidor es número de página y límite.",
   "Varios servicios del frontend envían desplazamiento en lugar de número de página, de modo que "
   "los listados afectados muestran siempre la primera página.",
   "RF-013.",
   "Alta", "Parcial.")
rf(d, "RF-071", "Operación sin conexión",
   "La aplicación debe conservar en el navegador los datos consultados y las operaciones pendientes "
   "para sincronizarlas al recuperar la conexión.",
   "Permitir la atención en zonas con conectividad intermitente.",
   "Usuario operativo, sistema.",
   "Al perder la conexión, la aplicación sigue leyendo la caché local y encola las operaciones; al "
   "recuperarlas, las sinciza con el servidor evitando duplicados.",
   "Una operación en conflicto se resuelve a favor del servidor y se notifica al usuario.",
   "Las operaciones encoladas conservan la clave de idempotencia.",
   "Los servicios de almacenamiento local existen en el código, pero ninguna pantalla los usa.",
   "RF-039, RF-070.",
   "Media", "Parcial.")
rf(d, "RF-072", "Actualización de la aplicación",
   "La aplicación instalable debe avisar al usuario cuando hay una nueva versión y aplicarla sin "
   "perder datos.",
   "Mantener a todos los usuarios sobre la versión vigente.",
   "Usuario operativo, sistema.",
   "Cuando el service worker detecta una versión nueva, muestra el aviso de actualización; al "
   "confirmar, recarga y deja la versión actualizada.",
   "Sin confirmación, la actualización espera al siguiente inicio.",
   "Las operaciones en curso no se interrumpen.",
   "El manifiesto de la aplicación declara iconos que no existen en el paquete y no existe pantalla "
   "de aviso de actualización.",
   "RF-071.",
   "Alta", "Parcial.")
rf(d, "RF-073", "Soporte multiempresa",
   "El sistema debe soportar varias empresas u oficinas con sus usuarios, catálogos y carteras "
   "aislados.",
   "Escalar el producto a más de un operador sin duplicar instalaciones.",
   "Administrador de plataforma.",
   "Cada operación se ejecuta dentro de la empresa activa del usuario; los datos de una empresa nunca "
   "son visibles desde otra.",
   "El administrador de plataforma puede cambiar de empresa con auditoría.",
   "El aislamiento se aplica en servidor, no solo en la interfaz.",
   "El modelo de datos actual no incluye clave de empresa.",
   "RF-009, RF-074.",
   "Media", "Pendiente.")
rf(d, "RF-074", "Seguridad de la plataforma",
   "La aplicación debe servirse con cifrado, cabeceras de seguridad, política de contenidos y "
   "protección frente a scripting entre sitios.",
   "Proteger información financiera sensible en tránsito y en el navegador.",
   "Infraestructura, desarrollo.",
   "El servidor añade las cabeceras de seguridad y la política de contenidos; las respuestas "
   "sensible a credenciales no se almacenan en caché.",
   "Una violación de la política se registra y bloquea el recurso.",
   "Todo el tráfico viaja por HTTPS.",
   "El proyecto no define cabeceras de seguridad ni política de contenidos, y no existe integración "
   "continua que lo verifique.",
   "RF-009.",
   "Máxima", "Pendiente.")
rf(d, "RF-075", "Respaldo y recuperación",
   "La base de datos debe respaldarse de forma periódica y poder restaurarse ante una pérdida.",
   "Asegurar la continuidad del negocio ante un fallo de datos.",
   "Infraestructura.",
   "Se ejecutan respaldos automáticos con retención definida y se practican restauraciones.",
   "Ante un desastre, la restauración se ejecuta en un entorno limpio y verificado.",
   "El respaldo incluye el esquema y los datos transaccionales.",
   "No existe procedimiento automatizado de respaldo ni de restauración en el proyecto.",
   "RF-074.",
   "Máxima", "Pendiente.")

# ============================================== 4. Requerimientos no funcionales
d.h1("4. Requerimientos no funcionales")
d.p(
    "Los requerimientos no funcionales definen las condiciones de operación del producto: qué tan "
    "rápido responde, qué tan disponible debe estar, cómo se despliega y cómo se mantiene. Se "
    "presentan agrupados en ocho categorías y con un estado de cumplimiento verificado contra el "
    "código y la infraestructura descrita en el proyecto. Donde el estado es Parcial o Pendiente se "
    "indica la condición concreta que falta por cumplir."
)

d.h2("4.1 Seguridad")
d.p(
    "La seguridad se resuelve en dos planos: autenticación y autorización en el servidor, y "
    "endurecimiento del canal en la plataforma. El primer plano está construido; el segundo apenas "
    "comienza. Los requisitos de este grupo tienen prioridad máxima porque de ellos depende la "
    "confidencialidad de la información financiera de los clientes."
)
d.table(
    "Requerimientos no funcionales de seguridad",
    ["Código", "Requerimiento", "Criterio de aceptación", "Estado"],
    [
        ["RNF-001", "Transporte cifrado", "Todo el tráfico se sirve por HTTPS; ninguna petición sensible viaja en claro.", "Pendiente"],
        ["RNF-002", "Tokens firmados", "Acceso y refresco firmados con secreto de servidor y expiración explícita.", "Completada"],
        ["RNF-003", "Contraseñas protegidas", "Las contraseñas se almacenan con hash y sal, jamás en texto plano.", "Completada"],
        ["RNF-004", "Autorización en servidor", "Todo endpoint sensible valida el rol antes de ejecutar.", "Completada"],
        ["RNF-005", "Cabeceras de seguridad", "Presentación de contenido, política de referrer y protección frente a scripting entre sitios.", "Pendiente"],
        ["RNF-006", "Política de contraseñas", "Longitud mínima de 6 caracteres y verificación de la contraseña actual en el cambio.", "Completada"],
        ["RNF-007", "Segregación de funciones", "El administrador concentra la gestión de cuentas y parámetros; el usuario operativo no las modifica.", "Completada"],
        ["RNF-008", "Auditoría de acciones", "Toda operación financiera registra autor, fecha, valores y dirección.", "Parcial"],
        ["RNF-009", "Protección del navegador", "Recursos con caché controlado y sin exponer credenciales en almacenamiento persistente.", "Parcial"],
    ],
    widths=[0.9, 1.6, 3.4, 1.1],
    align_center_cols=(0, 3),
)

d.h2("4.2 Rendimiento")
d.p(
    "El rendimiento se concentra en dos operaciones: la apertura del tablero y la consulta de "
    "listados. Ambas se benefician de la paginación y de la consulta consolidada que el backend ya "
    "ofrece pero el frontend no aprovecha."
)
d.table(
    "Requerimientos no funcionales de rendimiento",
    ["Código", "Requerimiento", "Criterio de aceptación", "Estado"],
    [
        ["RNF-010", "Respuesta de listados", "Los listados paginados responden con un tope de diez registros por defecto y no cargan la cartera completa.", "Completada"],
        ["RNF-011", "Apertura del tablero", "El tablero renderiza en una sola consulta consolidada en lugar de varias llamadas independientes.", "Pendiente"],
        ["RNF-012", "Búsqueda reactiva", "La búsqueda de clientes filtra sin recargar la página y con un límite de peticiones.", "Parcial"],
        ["RNF-013", "Consultas indexadas", "Las búsquedas por cliente, estado y fecha se resuelven sobre índices de la base de datos.", "Parcial"],
        ["RNF-014", "Transferencia mínima", "Las respuestas solo incluyen los campos que la pantalla necesita.", "Parcial"],
        ["RNF-015", "Caché de recursos estáticos", "Los recursos del cliente se sirven con caché de larga duración y versionado.", "Completada"],
    ],
    widths=[0.9, 1.6, 3.4, 1.1],
    align_center_cols=(0, 3),
)

d.h2("4.3 Disponibilidad y recuperación")
d.p(
    "La operación de cobro no puede suspenderse por mantenimientos prolongados ni por la caída de un "
    "proceso. Los requisitos de este grupo fijan el objetivo de disponibilidad, la tolerancia a "
    "fallos de la base de datos y la política de respaldo, esta última aún sin procedimiento "
    "automatizado."
)
d.table(
    "Requerimientos no funcionales de disponibilidad",
    ["Código", "Requerimiento", "Criterio de aceptación", "Estado"],
    [
        ["RNF-016", "Objetivo de disponibilidad", "El servicio busca un 99,5 % de disponibilidad mensual en horario de cobro.", "Pendiente"],
        ["RNF-017", "Continuidad de procesos programados", "El cálculo diario de moras se ejecuta aunque una ejecución previa haya fallado.", "Completada"],
        ["RNF-018", "Transaccionalidad", "Cada operación financiera se aplica completa o no se aplica.", "Completada"],
        ["RNF-019", "Respaldo automático", "La base de datos se respalda diariamente con retención definida.", "Pendiente"],
        ["RNF-020", "Prueba de restauración", "Se practica al menos una restauración por trimestre en entorno limpio.", "Pendiente"],
    ],
    widths=[0.9, 1.6, 3.4, 1.1],
    align_center_cols=(0, 3),
)

d.h2("4.4 Escalabilidad")
d.p(
    "El producto debe acompañar el crecimiento del portafolio sin rediseños. El backend horizontaliza "
    "fácilmente porque la lógica de negocio está en servicios sin estado; el cuello de botella "
    "previsible es la base de datos y el volumen de movimientos de capital."
)
d.table(
    "Requerimientos no funcionales de escalabilidad",
    ["Código", "Requerimiento", "Criterio de aceptación", "Estado"],
    [
        ["RNF-021", "Servidor sin estado", "Las sesiones viven en tokens, de modo que puede añadirse una instancia adicional del API.", "Completada"],
        ["RNF-022", "Crecimiento de la cartera", "Los listados siguen siendo navegables con más de cien mil préstamos gracias a la paginación por página.", "Parcial"],
        ["RNF-023", "Crecimiento de movimientos", "El libro de movimientos de capital se consulta por rangos de fecha y página.", "Completada"],
        ["RNF-024", "Ajuste horizontal", "El despliegue permite añadir réplicas de base de datos sin cambiar el código.", "Parcial"],
        ["RNF-025", "Procesamiento por lotes", "El cálculo de moras particiona el trabajo por fecha para no bloquear la operación.", "Parcial"],
    ],
    widths=[0.9, 1.6, 3.4, 1.1],
    align_center_cols=(0, 3),
)

d.h2("4.5 Mantenibilidad")
d.p(
    "La mantenibilidad es donde el proyecto muestra su mayor deuda: el código está organizado por "
    "capas y es legible, pero carece de pruebas automatizadas del backend, de integración continua y "
    "de documentación de arquitectura vigente. Los requisitos de este grupo marcan el estándar mínimo "
    "para considerar el producto sostenible."
)
d.table(
    "Requerimientos no funcionales de mantenibilidad",
    ["Código", "Requerimiento", "Criterio de aceptación", "Estado"],
    [
        ["RNF-026", "Tipado estricto", "El frontend compila en modo estricto sin excepciones y el backend valida con esquemas tipados.", "Completada"],
        ["RNF-027", "Pruebas automatizadas", "Existen pruebas de unidad para los servicios críticos y pruebas de integración del backend.", "Parcial"],
        ["RNF-028", "Integración continua", "Cada cambio ejecuta verificación de estilo, compilación y pruebas antes de fusionarse.", "Pendiente"],
        ["RNF-029", "Control de versiones", "Todo cambio se versiona con mensajes descriptivos y revisión previa.", "Completada"],
        ["RNF-030", "Documentación viva", "La documentación de operación se actualiza en cada entrega.", "Parcial"],
        ["RNF-031", "Eliminación de código muerto", "No permanecen componentes sin uso ni datos simulados en la interfaz.", "Pendiente"],
    ],
    widths=[0.9, 1.6, 3.4, 1.1],
    align_center_cols=(0, 3),
)

d.h2("4.6 Observabilidad")
d.p(
    "Sin observabilidad no hay operación financiera defendible: hace falta saber qué ocurrió, cuándo y "
    "por quién. El backend ya escribe auditoría en las operaciones sensibles y expone respuestas con "
    "detalle de error; falta centralizar los registros y vigilar la salud del servicio."
)
d.table(
    "Requerimientos no funcionales de observabilidad",
    ["Código", "Requerimiento", "Criterio de aceptación", "Estado"],
    [
        ["RNF-032", "Registros de aplicación", "Cada petición deja traza con identificador, duración y resultado.", "Parcial"],
        ["RNF-033", "Registros de negocio", "Los eventos financieros quedan en auditoría con autor y valores.", "Parcial"],
        ["RNF-034", "Métricas de salud", "Se monitoriza el tiempo de respuesta y la tasa de error del API.", "Pendiente"],
        ["RNF-035", "Alertas de proceso", "Un fallo del cálculo de moras o del envío de avisos genera una alerta.", "Pendiente"],
        ["RNF-036", "Trazabilidad de peticiones", "Las respuestas de error incluyen el detalle suficiente para diagnosticar sin reproducción.", "Completada"],
    ],
    widths=[0.9, 1.6, 3.4, 1.1],
    align_center_cols=(0, 3),
)

d.h2("4.7 Cumplimiento y tratamiento de datos")
d.p(
    "El sistema maneja datos personales y financieros de clientes que no son usuarios del producto, lo "
    "que exige minimizar la información recogida, restringir su consulta y conservarla solo el tiempo "
    "necesario. Los requisitos de este grupo se alinean con buenas prácticas de protección de datos "
    "personales."
)
d.table(
    "Requerimientos no funcionales de cumplimiento",
    ["Código", "Requerimiento", "Criterio de aceptación", "Estado"],
    [
        ["RNF-037", "Minimización de datos", "La ficha del cliente solo pide datos necesarios para evaluar y cobrar.", "Parcial"],
        ["RNF-038", "Control de acceso a datos", "Un usuario solo consulta la cartera autorizada; la restricción se aplica en servidor.", "Parcial"],
        ["RNF-039", "Conservación y borrado", "Se define retención por defecto y procedimiento de supresión de clientes sin operación.", "Pendiente"],
        ["RNF-040", "Registro de accesos", "Los inicios y cierres de sesión quedan registrados con fecha y origen.", "Parcial"],
        ["RNF-041", "Copia de privacidad", "La interfaz informa al cliente final sobre el uso de sus datos cuando corresponda.", "Pendiente"],
        ["RNF-042", "Integridad de los registros", "Los históricos de pagos, moras y movimientos no admiten eliminación desde la interfaz.", "Completada"],
    ],
    widths=[0.9, 1.6, 3.4, 1.1],
    align_center_cols=(0, 3),
)

d.h2("4.8 Compatibilidad y accesibilidad")
d.p(
    "El producto se usa en oficinas con equipos diversos y en dispositivos móviles durante la "
    "cobranza, por lo que la compatibilidad con navegadores actuales y la accesibilidad básica no son "
    "opcionales. La instalación como aplicación y el funcionamiento sin conexión completan este "
    "grupo."
)
d.table(
    "Requerimientos no funcionales de compatibilidad",
    ["Código", "Requerimiento", "Criterio de aceptación", "Estado"],
    [
        ["RNF-043", "Navegadores admitidos", "Las dos versiones principales de los navegadores de escritorio y móvil soportadas actualmente.", "Completada"],
        ["RNF-044", "Diseño responsivo", "Las pantallas principales se operan sin desplazamiento horizontal en tableta.", "Completada"],
        ["RNF-045", "Accesibilidad performativa", "Los controles tienen etiqueta accesible y contraste suficiente; los formularios anuncian sus errores.", "Parcial"],
        ["RNF-046", "Aplicación instalable", "El manifiesto declara íconos y nombre válidos y la aplicación se instala desde el navegador.", "Parcial"],
        ["RNF-047", "Funcionamiento sin conexión", "La consulta de listados recientes es posible sin red mediante la caché local.", "Parcial"],
        ["RNF-048", "Internacionalización", "Los textos y formatos monetarios se centralizan para admitir un segundo idioma en el futuro.", "Parcial"],
    ],
    widths=[0.9, 1.6, 3.4, 1.1],
    align_center_cols=(0, 3),
)

# ==================================================== 5. Matriz de trazabilidad
d.h1("5. Matrices de trazabilidad")
d.p(
    "La trazabilidad vincula cada requerimiento con su ubicación en el código, con los endpoints que "
    "lo soportan y con el caso de prueba que lo verifica. Permite responder con precisión qué se "
    "rompe cuando un componente cambia y qué requisitos quedan sin cubrir por una modificación. La "
    "columna de ubicación indica el archivo o directorio donde se implementa o debería implementarse "
    "el requisito; la columna de casos de prueba referencia la serie CP descrita en el plan de "
    "pruebas."
)

d.table(
    "Trazabilidad de los módulos de seguridad, clientes y solicitudes",
    ["RF", "Ubicación en el código", "Endpoints asociados", "CP", "Estado"],
    [
        ["RF-001", "app/pages/login.vue · app/services/api/auth.ts", "POST /auth/login", "CP-001", "Completada"],
        ["RF-002", "app/composables/useApi.ts", "POST /auth/refresh", "CP-002", "Completada"],
        ["RF-003", "stores/auth.ts · app/pages/index.vue", "POST /auth/logout", "CP-003", "Completada"],
        ["RF-004", "stores/auth.ts", "GET /auth/me", "CP-004", "Completada"],
        ["RF-005", "app/pages/perfil.vue", "POST /auth/change-password", "CP-005", "Completada"],
        ["RF-006", "sin interfaz en frontend", "POST /auth/forgot-password · POST /auth/reset-password", "CP-006", "Parcial"],
        ["RF-007", "app/pages/usuarios/index.vue", "GET · POST · PUT · DELETE /usuarios", "CP-007", "Completada"],
        ["RF-008", "app/middleware/auth.ts · app/middleware/admin.ts", "no aplica", "CP-008", "Pendiente"],
        ["RF-009", "prestamos_backend/app/dependencies", "todos los endpoints protegidos", "CP-009", "Completada"],
        ["RF-010", "servicios del backend · app/services/audit.ts sin uso", "auditoría interna", "CP-010", "Parcial"],
        ["RF-011", "tabla configuracion_sistema", "parámetros de mora", "CP-011", "Parcial"],
        ["RF-012", "app/pages/clientes/index.vue", "POST /clientes", "CP-012", "Completada"],
        ["RF-013", "app/pages/clientes/index.vue", "GET /clientes", "CP-013", "Completada"],
        ["RF-014", "app/services/api/cliente.ts sin parámetro de búsqueda", "GET /clientes?q=", "CP-014", "Parcial"],
        ["RF-015", "sin página de detalle", "GET /clientes/{id}", "CP-015", "Pendiente"],
        ["RF-016", "app/pages/clientes/index.vue", "PUT · DELETE /clientes/{id}", "CP-016", "Completada"],
        ["RF-017", "servicio de creación de préstamos", "POST /prestamos", "CP-017", "Completada"],
        ["RF-018", "sin implementar", "prestamos y pagos por cliente", "CP-018", "Pendiente"],
        ["RF-019", "sin implementar", "estadísticas por cliente", "CP-019", "Pendiente"],
        ["RF-020", "sin implementar", "POST /solicitudes", "CP-020", "Pendiente"],
        ["RF-021", "sin implementar", "PUT /solicitudes/{id}/decision", "CP-021", "Pendiente"],
        ["RF-022", "sin implementar", "POST /solicitudes/{id}/convertir", "CP-022", "Pendiente"],
        ["RF-023", "sin implementar", "notificación de estado", "CP-023", "Pendiente"],
        ["RF-024", "sin implementar", "autorización del módulo", "CP-024", "Pendiente"],
    ],
    widths=[0.7, 2.5, 2.2, 0.6, 1.0],
    align_center_cols=(0, 3, 4),
)

d.table(
    "Trazabilidad de los módulos de préstamos, pagos y mora",
    ["RF", "Ubicación en el código", "Endpoints asociados", "CP", "Estado"],
    [
        ["RF-025", "app/pages/prestamos/nuevo.vue · servicio de préstamos", "POST /prestamos", "CP-025", "Completada"],
        ["RF-026", "servicio de préstamos (validación de capital)", "POST /prestamos", "CP-026", "Completada"],
        ["RF-027", "generación de cuotas en el servicio de préstamos", "POST /prestamos", "CP-027", "Completada"],
        ["RF-028", "app/pages/prestamos/index.vue", "GET /prestamos", "CP-028", "Completada"],
        ["RF-029", "app/pages/prestamos/[id].vue", "GET /prestamos/{id}", "CP-029", "Completada"],
        ["RF-030", "RenovarPrestamoModal · app/pages/prestamos/[id].vue", "POST /prestamos/{id}/renovar", "CP-030", "Completada"],
        ["RF-031", "MarcarPerdidoModal", "POST /prestamos/{id}/perdido", "CP-031", "Completada"],
        ["RF-032", "cierre automático tras el pago", "POST /pagos", "CP-032", "Completada"],
        ["RF-033", "validaciones de estado en el servicio", "renovar · perdido", "CP-033", "Completada"],
        ["RF-034", "ajuste de capital del préstamo", "PUT /prestamos/{id}/capital", "CP-034", "Parcial"],
        ["RF-035", "sin implementar", "POST /prestamos/{id}/reestructurar", "CP-035", "Pendiente"],
        ["RF-036", "RegistrarPagoModal · app/services/api/pago.ts", "POST /pagos", "CP-036", "Completada"],
        ["RF-037", "validación de cuadre en el servicio de pagos", "POST /pagos", "CP-037", "Completada"],
        ["RF-038", "actualización de saldo y capital", "POST /pagos", "CP-038", "Completada"],
        ["RF-039", "capa de idempotencia del backend", "POST /pagos con clave", "CP-039", "Completada"],
        ["RF-040", "pestaña de pagos del préstamo", "GET /pagos", "CP-040", "Completada"],
        ["RF-041", "historial global redirigido al detalle", "GET /pagos paginado", "CP-041", "Parcial"],
        ["RF-042", "sin implementar", "POST /pagos/{id}/revertir", "CP-042", "Pendiente"],
        ["RF-043", "sin implementar", "GET /pagos/{id}/comprobante", "CP-043", "Pendiente"],
        ["RF-044", "planificador diario del backend", "POST /mora/procesar-manual", "CP-044", "Completada"],
        ["RF-045", "app/services/api/mora.ts con prefijo incorrecto", "GET /mora/ y /mora/prestamo/{id}", "CP-045", "Pendiente"],
        ["RF-046", "app/pages/moras/index.vue", "POST /mora/procesar-manual", "CP-046", "Parcial"],
        ["RF-047", "app/pages/cobranza/index.vue", "cuotas vencidas", "CP-047", "Parcial"],
        ["RF-048", "planificador de avisos push", "suscripciones push", "CP-048", "Completada"],
        ["RF-049", "sin implementar", "bandeja de avisos", "CP-049", "Pendiente"],
    ],
    widths=[0.7, 2.5, 2.2, 0.6, 1.0],
    align_center_cols=(0, 3, 4),
)

d.table(
    "Trazabilidad de los módulos financieros, tablero y plataforma",
    ["RF", "Ubicación en el código", "Endpoints asociados", "CP", "Estado"],
    [
        ["RF-050", "app/pages/capital/index.vue · servicio de capital", "GET /capital · GET /capital/movimientos", "CP-050", "Completada"],
        ["RF-051", "sin implementar", "movimientos de caja", "CP-051", "Pendiente"],
        ["RF-052", "app/pages/reportes/index.vue", "GET /reportes/ganancias · /reportes/perdidas", "CP-052", "Completada"],
        ["RF-053", "sin interfaz", "GET /reportes/cartera", "CP-053", "Parcial"],
        ["RF-054", "sin interfaz", "GET /reportes/cobranza", "CP-054", "Parcial"],
        ["RF-055", "descarga desde reportes", "GET /reportes/{tipo}.{formato}", "CP-055", "Completada"],
        ["RF-056", "app/pages/index.vue", "endpoints de capital, préstamos y clientes", "CP-056", "Completada"],
        ["RF-057", "gráfica de distribución del tablero", "distribución de cartera", "CP-057", "Parcial"],
        ["RF-058", "indicadores de vencimiento del tablero", "moras y pagos", "CP-058", "Parcial"],
        ["RF-059", "sin aprovechar", "GET /dashboard/resumen", "CP-059", "Pendiente"],
        ["RF-060", "usePushNotifications con variables sin definir", "POST · DELETE /push", "CP-060", "Parcial"],
        ["RF-061", "sin implementar", "envío de correos", "CP-061", "Pendiente"],
        ["RF-062", "sin implementar", "mensajería externa", "CP-062", "Pendiente"],
        ["RF-063", "sin implementar", "plantillas", "CP-063", "Pendiente"],
        ["RF-064", "sin implementar", "pasarela de pago", "CP-064", "Pendiente"],
        ["RF-065", "sin implementar", "consulta de buró", "CP-065", "Pendiente"],
        ["RF-066", "sin implementar", "firma electrónica", "CP-066", "Pendiente"],
        ["RF-067", "ImportExtractModal con datos simulados", "importación de extractos", "CP-067", "Pendiente"],
        ["RF-068", "app/pages/tipos-prestamo/index.vue", "GET · POST · PUT · DELETE /tipos-prestamo", "CP-068", "Completada"],
        ["RF-069", "app/pages/tipos-pago/index.vue", "GET · POST · PUT · DELETE /tipos-pago", "CP-069", "Completada"],
        ["RF-070", "servicios con parámetro de desplazamiento", "listados paginados", "CP-070", "Parcial"],
        ["RF-071", "servicios locales sin uso", "sincronización diferida", "CP-071", "Parcial"],
        ["RF-072", "service worker sin aviso de actualización", "caché de la aplicación", "CP-072", "Parcial"],
        ["RF-073", "sin implementar", "aislamiento por empresa", "CP-073", "Pendiente"],
        ["RF-074", "sin cabeceras de seguridad", "cabeceras HTTP", "CP-074", "Pendiente"],
        ["RF-075", "sin procedimiento automatizado", "respaldo de base de datos", "CP-075", "Pendiente"],
    ],
    widths=[0.7, 2.5, 2.2, 0.6, 1.0],
    align_center_cols=(0, 3, 4),
)

d.p(
    "Como resumen de cobertura, de los 75 requerimientos funcionales 33 se encuentran completados, 16 "
    "parcialmente implementados y 26 pendientes. El grupo de mayor criticidad —seguridad, préstamos y "
    "pagos— concentra la mayor parte de los requisitos completados, mientras que las brechas se "
    "localizan en la protección de rutas del cliente, en la consulta de moras y en los módulos de "
    "originación formal y comunicaciones."
)

# ============================================ 6. Reglas de negocio financieras
d.h1("6. Reglas de negocio e invariantes financieras")
d.p(
    "Las siguientes reglas son de obligatorio cumplimiento porque sostienen la integridad del dinero "
    "manejado por el sistema. Se transcriben de la lógica vigente en los servicios del backend, de "
    "modo que funcionan como especificación ejecutable y como lista de verificación para las "
    "pruebas."
)
d.numbered(1, "**Capital desembolsado.** Al crear un préstamo el capital global se reduce exactamente en "
             "el monto prestado, y se registra un movimiento de tipo préstamo otorgado con esa "
             "misma magnitud y fecha.")
d.numbered(2, "**Interés total.** El interés total es capital prestado por el porcentaje de interés "
             "por el número de cuotas, redondeado a dos decimales; el monto total es capital más "
             "interés total.")
d.numbered(3, "**Cuotas.** El valor de la cuota es monto total dividido entre el número de cuotas; la "
             "última cuota absorbe el redondeo para que la suma de las cuotas sea exactamente igual "
             "al monto total.")
d.numbered(4, "**Cobro.** El valor pagado debe ser igual a la suma de capital, interés y mora con una "
             "tolerancia de un centavo; cualquier diferencia mayor se rechaza.")
d.numbered(5, "**Saldo.** Cada pago reduce el saldo pendiente exactamente en la parte de capital "
             "pagado; el interés y la mora no modifican la deuda, solo la utilidad y la penalización.")
d.numbered(6, "**Capital del fondo.** Todo pago suma su componente de capital al capital global y "
             "genera el movimiento correspondiente; toda pérdida descuenta el saldo del préstamo y "
             "genera su movimiento.")
d.numbered(7, "**Cierre.** Cuando el saldo llega a cero o resulta negativo dentro de la tolerancia, "
             "se fija a cero y el préstamo pasa a estado pagado.")
d.numbered(8, "**Estados terminales.** Un préstamo pagado, perdido o renovado no admite nuevos pagos, "
             "renovaciones ni declaraciones de pérdida.")
d.numbered(9, "**Renovación.** Solo procede sobre préstamos activos; el capital del nuevo préstamo es "
             "el saldo pendiente menos el abono, y el abono nunca puede superar el saldo.")
d.numbered(10, "**Mora.** La mora se calcula una sola vez por cuota y fecha, aplicando la tasa diaria "
               "y los días de gracia vigentes en la configuración del sistema.")
d.numbered(11, "**Idempotencia.** Repetir una operación de pago con la misma clave no produce un "
               "segundo cobro, y reutilizar la clave con un cuerpo distinto se rechaza.")
d.numbered(12, "**Atomicidad.** Si cualquiera de los pasos anteriores falla, la operación completa se "
               "revierte y no quedan efectos parciales ni movimientos huérfanos.")

d.figure(os.path.join(FIGS, "fig2_flujo_credito.png"),
         "Ciclo de vida financiero del préstamo, desde la originación hasta el cierre contable.")
d.figure(os.path.join(FIGS, "fig4_estados.png"),
         "Estados del préstamo y transiciones permitidas según la lógica vigente del servidor.")

# ================================================ 7. Supuestos, riesgos y dependencias
d.h1("7. Supuestos, riesgos y dependencias")
d.p(
    "El alcance descrito se apoya en un conjunto de supuestos que conviene hacer explícitos. En "
    "primer lugar, se asume que el operador mantiene un respaldo periódico de la base de datos, dado "
    "que el proyecto no incluye un procedimiento automatizado. En segundo lugar, se asume que el "
    "dominio se publica bajo cifrado, aunque el código no fuerce esa condición. Finalmente, se asume "
    "que los procesos programados permanecen activos las veinticuatro horas, ya que de ellos depende "
    "el devengue de moras y el envío de recordatorios."
)
d.p(
    "Los riesgos de mayor impacto identificados durante el análisis son cuatro. El primero es la "
    "ausencia de protección efectiva de rutas en el cliente, que permite navegar sin sesión y "
    "dificulta el control de acceso por rol. El segundo es el desajuste entre las rutas de moras "
    "declaradas por el frontend y las publicadas por el servidor, que deja inoperativo todo el "
    "módulo. El tercero es la inconsistencia de paginación entre capas, que oculta registros porque "
    "el listado siempre se resuelve sobre la primera página. El cuarto son los datos simulados "
    "presentes en la pantalla de importación de extractos, que contradicen la exigencia de no "
    "mostrar información inventada."
)
d.p(
    "Entre las dependencias externas figuran la configuración de un servidor de correo para la "
    "recuperación de contraseñas, las llaves de notificación push del navegador, el proveedor de "
    "mensajería cuando se implementen los avisos al cliente final y el proveedor de infraestructura "
    "que garantice el respaldo y el cifrado del canal. Ninguna de estas dependencias afecta a los "
    "requisitos ya entregados."
)

# ============================================== 8. Control del documento
d.h1("8. Control de versiones y aprobación")
d.table(
    "Historial de versiones del documento",
    ["Versión", "Fecha", "Descripción del cambio", "Responsable"],
    [
        ["1.0", "28 de septiembre de 2026", "Versión inicial con los requerimientos funcionales y no funcionales verificados contra el código fuente.", "Equipo de Ingeniería de Software"],
    ],
    widths=[0.8, 1.5, 3.4, 1.5],
    align_center_cols=(0,),
)
d.p(
    "Toda modificación posterior a esta versión deberá actualizar la matriz de trazabilidad del "
    "capítulo 5 y revisar el estado de implementación de los requisitos afectados, de modo que el "
    "documento siga reflejando la realidad del producto y no una intención de diseño."
)

d.references([
    "Equipo de Ingeniería de Software. (2026). *BLUEPRINT_LOANSOFT: alcance, fases y deuda del "
    "sistema LoanSoft*. LoanSoft.",
    "Equipo de Ingeniería de Software. (2026). *PLAN_FRONTEND_NUXT4: stack técnico y requerimientos "
    "de backend B1 a B11*. LoanSoft.",
    "Equipo de Ingeniería de Software. (2026). *BACKEND_ENDPOINTS: inventario de interfaces del "
    "servidor y su estado*. LoanSoft.",
    "Equipo de Ingeniería de Software. (2026). *PLAN_NUEVOS_MODULOS: módulos previstos y avance*. "
    "LoanSoft.",
    "Equipo de Ingeniería de Software. (2026). *PROPUESTA_REDISENO_ESTRUCTURAL: organización de "
    "rutas y pantallas*. LoanSoft.",
    "FastAPI. (s. f.). *FastAPI documentation*. https://fastapi.tiangolo.com/",
    "Nuxt. (s. f.). *Nuxt 4 documentation*. https://nuxt.com/",
    "Python Software Association. (s. f.). *Django-style documentation for SQLAlchemy*. "
    "https://www.sqlalchemy.org/",
])
d.save(os.path.join(OUT, "01_Documento_de_Requerimientos_del_Software.docx"))
print("SRS generada")
