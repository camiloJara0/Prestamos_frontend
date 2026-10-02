# -*- coding: utf-8 -*-
"""Genera el Plan Scrum de LoanSoft."""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from apa import Doc  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
CATALOG = json.load(open(os.path.join(HERE, "rf_catalog.json"), encoding="utf-8"))


def sprint_of(code):
    n = int(code.split("-")[1])
    if n <= 11:
        return 0
    if n <= 27:
        return 1
    if n <= 35:
        return 2
    if n <= 43:
        return 3
    if n <= 49:
        return 4
    if n <= 59:
        return 5
    return 6


d = Doc(
    title="**Plan Scrum**",
    subtitle="Backlog, historias de usuario, sprints y casos de prueba de LoanSoft",
    author=["Equipo de Ingeniería de Software · LoanSoft"],
    affiliation=["LoanSoft · Sistema de Gestión de Préstamos"],
    date=["28 de septiembre de 2026"],
    extra=["Versión 1.0",
           "Metodología Scrum · Sprints de dos semanas"],
)

d.abstract(
    "Este documento organiza el trabajo de desarrollo de LoanSoft en un marco Scrum: épicas del "
    "producto, historias de usuario con sus criterios de aceptación, un backlog priorizado, un plan "
    "de sprints con objetivos y entregables, y los casos de prueba CP-001 a CP-075 alineados uno a "
    "uno con los requerimientos funcionales del Documento de Requerimientos del Software. Las "
    "estimaciones y los estados reflejan el avance real observado en el código, no compromisos de "
    "fecha."
)

# ==================================================== 1. Propósito
d.h1("1. Propósito y marco de trabajo")
d.p(
    "El plan traduce los 75 requerimientos funcionales del documento de requisitos en trabajo "
    "organizado y verificable. Cada requerimiento queda asociado a una épica, a una o varias historias "
    "de usuario, a un sprint donde se espera completarlo y a un caso de prueba que permite comprobarlo. "
    "De este modo, la trazabilidad no termina en la matriz del requisitos sino que continúa en el día "
    "a día del equipo: lo que se planifica, se construye y se prueba se referencia con los mismos "
    "códigos."
)
d.p(
    "Se trabaja con sprints de dos semanas. La prioridad del backlog sigue la criticidad financiera "
    "de los requerimientos: primero lo que protege el dinero y la sesión de usuario, después lo que "
    "permite operar la cartera y al final lo que amplía el alcance del producto. El backlog es "
    "viviente: cada revisión puede reordenar ítems, incorporar hallazgos de auditoría o retirar "
    "trabajo que ya no aporta valor."
)

# ==================================================== 2. Roles
d.h1("2. Roles y equipo")
d.table(
    "Roles del equipo y su responsabilidad",
    ["Rol", "Responsabilidad principal", "Participación en la ceremonia"],
    [
        ["Product Owner", "Prioriza el backlog, define criterios de aceptación y acepta el incremento.", "Planning, revisión, decisiones de alcance."],
        ["Scrum Master", "Facilita las ceremonias, retira impedimientos y cuida el proceso.", "Todas las ceremonias."],
        ["Equipo de desarrollo", "Diseña, implementa, prueba y despliega las historias comprometidas.", "Planning, diaria, revisión y retrospectiva."],
        ["Responsable de calidad", "Ejecuta los casos de prueba y gestiona los defectos.", "Planning, revisión, control de calidad."],
        ["Stakeholders del negocio", "Validan las reglas de negocio con casos reales de préstamos.", "Revisión de fin de sprint."],
    ],
    widths=[1.5, 3.2, 2.3],
)
d.p(
    "En la práctica, el equipo es pequeño y sus miembros acumulan más de un rol; la separación anterior "
    "existe para que ninguna responsabilidad quede sin dueño, en especial la aceptación de las "
    "historias y la ejecución de los casos de prueba."
)

# ==================================================== 3. Épicas
d.h1("3. Épicas del producto")
d.p(
    "El backlog se agrupa en ocho épicas que corresponden a los módulos funcionales del sistema. "
    "Cada épica indica el rango de requerimientos que abarca, la prioridad con que se atiende y el "
    "sprint donde se concentra el esfuerzo."
)
d.table(
    "Épicas, alcance y sprint de concentración",
    ["Épica", "Alcance", "Requerimientos", "Prioridad", "Sprint"],
    [
        ["EP-01 Seguridad y acceso", "Autenticación, sesiones, usuarios, roles, auditoría y configuración.", "RF-001 a RF-011", "Máxima", "Sprint 0"],
        ["EP-02 Clientes y prospectos", "Alta, búsqueda, edición y baja de clientes; solicitudes de préstamo.", "RF-012 a RF-024", "Máxima", "Sprint 1"],
        ["EP-03 Originación de crédito", "Cálculo financiero, validación de capital y generación de cuotas.", "RF-025 a RF-027", "Máxima", "Sprint 1"],
        ["EP-04 Administración de préstamos", "Listados, detalle, renovación, pérdida y bloques por estado.", "RF-028 a RF-035", "Alta", "Sprint 2"],
        ["EP-05 Pagos y cobro", "Registro de pagos, cuadre, idempotencia, historial y comprobantes.", "RF-036 a RF-043", "Máxima", "Sprint 3"],
        ["EP-06 Mora y cobranza", "Cálculo de moras, procesamiento manual, cobranza y recordatorios.", "RF-044 a RF-049", "Alta", "Sprint 4"],
        ["EP-07 Capital, reportes y tablero", "Libro de movimientos, reportes financieros, exportación e indicadores.", "RF-050 a RF-059", "Alta", "Sprint 5"],
        ["EP-08 Plataforma e integraciones", "PWA, notificaciones, pagos externos, multiempresa y respaldos.", "RF-060 a RF-075", "Media", "Sprint 6"],
    ],
    widths=[1.9, 2.7, 1.2, 0.8, 0.8],
    align_center_cols=(2, 3, 4),
)

# ==================================================== 4. Historias
d.h1("4. Historias de usuario")
d.p(
    "Cada historia se redacta en la forma clásica de usuario, objetivo y valor, y se acompaña de "
    "criterios de aceptación verificables. Al final de cada bloque se indica la trazabilidad con el "
    "requerimiento, su caso de prueba, la prioridad, la estimación en puntos de la escala de "
    "Fibonacci y el estado actual del trabajo en el código."
)

HIST = [
    # (id, nombre, relato, criterios, rf, puntos, estado)
    ("US-01", "Iniciar sesión con credenciales",
     "Como usuario autorizado, quiero ingresar con mi correo y contraseña para acceder a las "
     "funciones que me corresponden.",
     ["El sistema acepta correo y contraseña válidos y redirige al tablero.",
      "Con credenciales inválidas muestra un mensaje genérico que no revela si la cuenta existe.",
      "Una cuenta inactiva no puede iniciar sesión.",
      "La sesión se almacena y se mantiene activa durante la jornada."],
     ["RF-001", "RF-004"], 5, "Completada"),
    ("US-02", "Renovar y cerrar la sesión",
     "Como usuario, quiero que la sesión se renueve sola y pueda cerrarla cuando termine mi turno "
     "para que nadie más opere con mi cuenta.",
     ["El token de acceso se renueva de forma automática sin perder el trabajo en curso.",
      "Agotada la renovación, la aplicación devuelve a la pantalla de acceso.",
      "El cierre de sesión limpia los datos locales y el estado del usuario."],
     ["RF-002", "RF-003"], 3, "Completada"),
    ("US-03", "Recuperar la contraseña olvidada",
     "Como usuario, quiero restablecer mi contraseña desde mi correo para no quedar sin acceso a la "
     "operación.",
     ["El sistema envía un enlace de restablecimiento al correo registrado.",
      "El enlace permite definir una contraseña nueva con validación de longitud.",
      "El enlace caduca y no puede reutilizarse."],
     ["RF-006"], 3, "Parcial"),
    ("US-04", "Administrar las cuentas de usuario",
     "Como administrador, quiero crear, editar y desactivar cuentas con rol asignado para controlar "
     "quién opera el sistema.",
     ["Alta con nombre, correo, contraseña y rol sin duplicar correos.",
      "La desactivación retira el acceso sin borrar el historial del usuario.",
      "El listado pagina y filtra por nombre, correo y rol."],
     ["RF-007"], 5, "Completada"),
    ("US-05", "Proteger las rutas privadas del frontend",
     "Como responsable del sistema, quiero que solo los usuarios autenticados con el rol correcto "
     "abran cada pantalla para que la navegación no exponga datos.",
     ["Las rutas privadas redirigen al inicio de sesión sin token válido.",
      "Las pantallas administrativas exigen rol de administrador.",
      "El rol se comprueba también contra el servidor, no solo en el navegador."],
     ["RF-008", "RF-009"], 8, "Pendiente"),
    ("US-06", "Auditar las operaciones sensibles",
     "Como responsable de auditoría, quiero que cada alta, edición o eliminación registre quién, qué y "
     "cuándo para poder reconstruir cualquier controversia.",
     ["La auditoría guarda usuario, tabla, operación, valores previos y nuevos, y marca de tiempo.",
      "El detalle se consulta por usuario, tabla y tipo de operación.",
      "Ninguna operación sensible se ejecuta sin dejar registro."],
     ["RF-010"], 5, "Parcial"),
    ("US-07", "Registrar un cliente nuevo",
     "Como gestor, quiero crear la ficha de un cliente con sus datos de contacto y referencia para "
     "poder ofrecerle un préstamo.",
     ["Los campos obligatorios son nombre completo y cédula.",
      "La cédula no puede repetirse en el sistema.",
      "El cliente nace activo y queda disponible para originar préstamos.",
      "Los campos de referencia y observaciones son opcionales."],
     ["RF-012", "RF-017"], 5, "Completada"),
    ("US-08", "Buscar y listar clientes",
     "Como gestor, quiero localizar un cliente por nombre, cédula o teléfono y ver la lista paginada "
     "para atenderlo sin demora.",
     ["La búsqueda coincide con nombre, cédula o teléfono.",
      "El listado pagina y permite ordenar por fecha de registro.",
      "Sin coincidencias se muestra un estado vacío comprensible."],
     ["RF-013", "RF-014", "RF-070"], 5, "Parcial"),
    ("US-09", "Editar y dar de baja un cliente",
     "Como gestor, quiero actualizar los datos de un cliente o marcarlo inactivo para mantener la "
     "ficha al día y dejar de ofrecerle crédito.",
     ["La edición conserva el historial de préstamos existente.",
      "La baja es lógica: el registro permanece consultable.",
      "Un cliente inactivo no aparece en la originación."],
     ["RF-016"], 3, "Completada"),
    ("US-10", "Mantener el catálogo de tipos de préstamo",
     "Como administrador, quiero definir los productos de crédito con su interés mensual y su máximo "
     "de cuotas para que la originación aplique parámetros oficiales.",
     ["Alta, edición y desactivación de tipos con sus tasas.",
      "Un tipo con operaciones asociadas se desactiva y no se elimina.",
      "Los tipos inactivos dejan de aparecer en los formularios."],
     ["RF-068", "RF-011"], 3, "Completada"),
    ("US-11", "Mantener el catálogo de tipos de pago",
     "Como administrador, quiero administrar los medios de cobro para que cada pago quede clasificado "
     "de forma uniforme.",
     ["Alta, edición y desactivación con descripción.",
      "Los tipos se listan en el formulario de pago en orden definido."],
     ["RF-069"], 3, "Completada"),
    ("US-12", "Originar un préstamo con su plan de cuotas",
     "Como gestor, quiero registrar un préstamo que calcule interés total, monto total y cuotas "
     "mensuales para entregar el dinero con las condiciones acordadas.",
     ["El formulario toma cliente, tipo, fecha, capital, interés y número de cuotas.",
      "El cálculo financiero produce interés total, monto total y valor de cuota consistentes.",
      "Se generan todas las cuotas en estado pendiente con su fecha de vencimiento.",
      "El capital se descuenta del saldo disponible al confirmar."],
     ["RF-025", "RF-027"], 8, "Completada"),
    ("US-13", "Validar la disponibilidad de capital antes de prestar",
     "Como administrador, quiero que el sistema rechace el préstamo si el capital disponible no alcanza "
     "para que la caja nunca quede en números rojos.",
     ["La validación se realiza en el servidor antes de crear el préstamo.",
      "El rechazo informa el saldo disponible y el monto solicitado.",
      "Ningún dato se persiste cuando la validación falla."],
     ["RF-026"], 5, "Completada"),
    ("US-14", "Listar y filtrar los préstamos",
     "Como gestor, quiero ver la cartera con sus estados y saldos y filtrarla por estado y periodo "
     "para encontrar cualquier operación.",
     ["La lista muestra cliente, monto, cuotas pagadas, saldo y estado.",
      "Los filtros por estado y fecha se combinan.",
      "El detalle abre con un solo gesto desde la fila."],
     ["RF-028"], 5, "Completada"),
    ("US-15", "Consultar el detalle de un préstamo",
     "Como gestor, quiero abrir un préstamo y ver sus tarjetas de resumen, sus cuotas y sus pagos "
     "para entender su situación en un vistazo.",
     ["Las tarjetas muestran capital, interés, monto total, cuota y saldo.",
      "La pestaña de cuotas presenta número, vencimiento, valor, estado e importes pagados.",
      "La pestaña de pagos lista el historial de cobros."],
     ["RF-029", "RF-040"], 5, "Completada"),
    ("US-16", "Renovar un préstamo vivo",
     "Como gestor, quiero aplicar un abono al saldo y abrir un nuevo préstamo con nuevas condiciones "
     "para continuar la relación con el cliente.",
     ["La renovación solo está disponible desde estados no terminales.",
      "El abono no puede superar el saldo pendiente.",
      "Se crean el nuevo préstamo y la relación con el anterior.",
      "El préstamo original queda en estado renovado."],
     ["RF-030", "RF-033"], 8, "Completada"),
    ("US-17", "Declarar un préstamo perdido",
     "Como administrador, quiero registrar la incobrabilidad con fecha y motivo para que el saldo se "
     "descuente del capital y quede documentado.",
     ["La declaración solo procede desde estados no terminales.",
      "Fecha y motivo son obligatorios.",
      "El saldo pendiente se descuenta del capital disponible.",
      "El préstamo pasa al estado perdido y deja de ofrecer acciones."],
     ["RF-031", "RF-033"], 5, "Completada"),
    ("US-18", "Registrar un pago con desglose",
     "Como gestor, quiero cobrar una cuota indicando capital, interés y mora para que cada peso quede "
     "clasificado desde el origen.",
     ["El formulario busca el préstamo y lista solo cuotas con saldo.",
      "La suma de capital, interés y mora debe coincidir con el valor pagado.",
      "El cobro actualiza el saldo del préstamo y el estado de la cuota.",
      "Al llegar a cero el préstamo se cierra automáticamente como pagado."],
     ["RF-036", "RF-037", "RF-038", "RF-032"], 8, "Completada"),
    ("US-19", "Evitar cobros duplicados",
     "Como administrador, quiero que un cobro repetido por falla de red no se registre dos veces para "
     "proteger la caja.",
     ["Cada envío lleva una clave única de operación.",
      "Un segundo envío con la misma clave no crea otro cobro.",
      "El sistema devuelve la respuesta original al reintento."],
     ["RF-039"], 5, "Completada"),
    ("US-20", "Revisar los pagos del sistema",
     "Como administrador, quiero consultar el historial de pagos con filtros de fecha, cliente y tipo "
     "para responder ante cualquier consulta.",
     ["El listado pagina y se filtra por periodo y cliente.",
      "Cada fila muestra fecha, préstamo, valor y desglose.",
      "La consulta está disponible sin abrir el detalle de cada préstamo."],
     ["RF-041"], 5, "Parcial"),
    ("US-21", "Revertir un pago registrado por error",
     "Como administrador, quiero anular un cobro con motivo para corregir errores dejando constancia "
     "de la reversión.",
     ["La reversión exige rol de administrador y un motivo.",
      "El saldo, la cuota y el capital se restauran.",
      "La operación queda en auditoría con su trazabilidad."],
     ["RF-042"], 8, "Pendiente"),
    ("US-22", "Calcular moras diariamente",
     "Como sistema, quiero aplicar la mora del día a las cuotas vencidas según la tasa y los días de "
     "gracia configurados para que la penalización sea automática y consistente.",
     ["El proceso corre cada día a la medianoche sin intervención manual.",
      "Solo se gravan cuotas vencidas más allá de los días de gracia.",
      "El proceso es a prueba de fallos: un día sin ejecución no se duplica al siguiente."],
     ["RF-044", "RF-011"], 8, "Completada"),
    ("US-23", "Procesar moras bajo demanda",
     "Como administrador, quiero ejecutar el cálculo de moras en el momento para corregir desfases "
     "detectados.",
     ["El botón ejecuta el mismo proceso del planificador.",
      "El resultado informa el total generado en la ejecución.",
      "La acción está reservada al rol administrador."],
     ["RF-046"], 3, "Parcial"),
    ("US-24", "Consultar las moras de un préstamo",
     "Como gestor, quiero ver las moras aplicadas a un préstamo con su base de cálculo para "
     "explicarle al cliente el monto adeudado.",
     ["El listado muestra fecha, días, base, tasa y valor de la mora.",
      "La consulta responde sin error de recurso inexistente.",
      "Se puede filtrar por préstamo."],
     ["RF-045"], 5, "Pendiente"),
    ("US-25", "Trabajar la cartera de cobranza",
     "Como responsable de cobranza, quiero ver los vencimientos del día con el contacto del cliente "
     "para priorizar las llamadas.",
     ["La lista agrupa cuotas vencidas con antigüedad y saldo.",
      "Incluye teléfono y datos de contacto del cliente.",
      "Desde la fila se abre el préstamo correspondiente."],
     ["RF-047"], 5, "Parcial"),
    ("US-26", "Recibir recordatorios de vencimiento",
     "Como usuario, quiero recibir una notificación push tres días y un día antes del vencimiento "
     "para anticipar el cobro.",
      ["El planificador envía los avisos a los administradores suscritos.",
      "La suscripción se registra y se puede retirar.",
      "Un fallo en el envío no detiene el resto de los avisos."],
     ["RF-048", "RF-060"], 5, "Completada"),
    ("US-27", "Controlar el capital y sus movimientos",
     "Como administrador, quiero ver el saldo disponible y el historial de movimientos para verificar "
     "cómo llegó la caja a su situación actual.",
     ["El saldo distingue aportes, préstamos, pagos y pérdidas.",
      "Cada movimiento registra tipo, valor, fecha y referencia.",
      "El saldo nunca se permite negativo."],
     ["RF-050", "RF-051"], 5, "Parcial"),
    ("US-28", "Producir reportes financieros con exportación",
     "Como administrador, quiero generar el reporte de ganancias y pérdidas de un periodo y "
     "descargarlo en Excel o PDF para cerrar la gestión.",
     ["El reporte muestra intereses cobrados y resultado neto.",
      "El reporte de pérdidas lista los préstamos perdidos con motivo.",
      "La exportación respeta el periodo filtrado sin abrir otra ventana."],
     ["RF-052", "RF-053", "RF-054", "RF-055"], 8, "Parcial"),
    ("US-29", "Ver el tablero de indicadores",
     "Como gestor, quiero abrir el sistema y encontrar capital, cartera, saldo pendiente y ganancia "
     "del periodo en un vistazo.",
     ["Las tarjetas muestran capital actual, préstamos activos, saldo pendiente y ganancia.",
      "Los indicadores se actualizan al recargar.",
      "Sin datos se muestra la leyenda de ausencia de información."],
     ["RF-056", "RF-057", "RF-058", "RF-059"], 5, "Parcial"),
    ("US-30", "Operar sin conexión y actualizarse",
     "Como usuario, quiero que la aplicación funcione con conexión intermitente y se actualice sin "
     "recargar para no interrumpir la jornada.",
     ["Los datos críticos se guardan localmente y se envían al recuperar la red.",
      "La aplicación detecta la pérdida de conexión y lo informa.",
      "La nueva versión se ofrece con aviso, sin recarga silenciosa del trabajo en curso."],
     ["RF-071", "RF-072"], 8, "Parcial"),
    ("US-31", "Proteger la plataforma y respaldar los datos",
     "Como responsable del sistema, quiero cabeceras de seguridad, restricciones de origen y respaldos "
     "programados para sostener la operación ante incidentes.",
     ["Las respuestas incluyen cabeceras de seguridad y CORS acotado al origen del frontend.",
      "El respaldo de base de datos corre de forma programada y periódica.",
      "Existe un procedimiento documentado de restauración."],
     ["RF-074", "RF-075"], 8, "Pendiente"),
    ("US-32", "Registrar una solicitud de préstamo",
     "Como cliente o gestor, quiero capturar una solicitud y su decisión para tener un embudo de "
     "originación antes de formalizar la deuda.",
     ["La solicitud registra cliente, monto solicitado y plazo.",
      "La decisión aprueba o rechaza con observaciones.",
      "Una solicitud aprobada se convierte en préstamo sin volver a digitar los datos."],
     ["RF-020", "RF-021", "RF-022", "RF-023", "RF-024"], 13, "Pendiente"),
]

for hid, hname, relato, criterios, rfs, puntos, estado in HIST:
    d.h3(f"{hid} · {hname}")
    d.p(relato)
    d.p("**Criterios de aceptación:**")
    for c in criterios:
        d.bullet(c)
    prioridad = "P1" if any(CATALOG[r]["prioridad"] in ("Máxima", "Maxima") for r in rfs) else (
        "P2" if any(CATALOG[r]["prioridad"] == "Alta" for r in rfs) else "P3")
    d.p(f"**Trazabilidad:** {' · '.join(rfs)} · Caso de prueba "
        f"{' · '.join('CP-' + r.split('-')[1] for r in rfs)} · Prioridad {prioridad} · "
        f"Estimación {puntos} puntos · Estado: {estado}.")

# ==================================================== 5. Backlog
d.h1("5. Backlog priorizado")
d.p(
    "El siguiente orden es el que se propone para el refinamiento. La prioridad P1 corresponde a "
    "requerimientos de criticidad máxima, P2 a los de alta prioridad y P3 a los de alcance diferido. "
    "La columna de estado refleja el avance observado en el código al cierre del análisis."
)
rows = []
for hid, hname, _r, _c, rfs, puntos, estado in HIST:
    prioridad = "P1" if any(CATALOG[r]["prioridad"] in ("Máxima", "Maxima") for r in rfs) else (
        "P2" if any(CATALOG[r]["prioridad"] == "Alta" for r in rfs) else "P3")
    epica = next((e for e in [
        ("EP-01", range(1, 12)), ("EP-02", range(12, 25)), ("EP-03", range(25, 28)),
        ("EP-04", range(28, 36)), ("EP-05", range(36, 44)), ("EP-06", range(44, 50)),
        ("EP-07", range(50, 60)), ("EP-08", range(60, 76))]
        if int(rfs[0].split("-")[1]) in e[1]), ("EP-08",))[0]
    rows.append([hid, hname, epica, prioridad, str(puntos), estado])
order = {"P1": 0, "P2": 1, "P3": 2}
rows.sort(key=lambda r: (order[r[3]], -int(r[4])))
d.table(
    "Backlog priorizado del producto",
    ["Historia", "Descripción", "Épica", "Prioridad", "Puntos", "Estado"],
    rows,
    widths=[0.7, 2.9, 0.8, 0.8, 0.6, 1.2],
    align_center_cols=(0, 2, 3, 4),
)
total_pts = sum(int(r[4]) for r in rows)
d.p(
    f"El backlog acumula {len(rows)} historias y {total_pts} puntos de esfuerzo. Considerando una "
    "velocidad sostenida de entre 26 y 32 puntos por sprint, el trabajo planificado se distribuye en "
    "los sprints descritos a continuación, con margen para correcciones y hallazgos de auditoría."
)

# ==================================================== 6. Sprints
d.h1("6. Plan de sprints")
d.p(
    "Cada sprint se define por un objetivo de negocio verificable, no por un listado de tareas. El "
    "objetivo es la frase que el equipo consulta cuando debe decidir si una historia entra o entra "
    "más tarde en el sprint."
)
d.table(
    "Plan de sprints de dos semanas",
    ["Sprint", "Objetivo", "Historias", "Puntos", "Entregable"],
    [
        ["Sprint 0", "Operar con sesión segura y cuentas controladas.", "US-01, US-02, US-04, US-05, US-06", "26",
         "Acceso, renovación de sesión, usuarios y auditoría; protección de rutas lista para pruebas."],
        ["Sprint 1", "Tener la cartera de clientes lista y poder originar un préstamo.", "US-07, US-08, US-09, US-10, US-11, US-12, US-13", "32",
         "Clientes de punta a punta, catálogos activos y originación con cálculo validado."],
        ["Sprint 2", "Gestionar la vida de un préstamo después de la entrega.", "US-14, US-15, US-16, US-17", "23",
         "Cartera filtrable, detalle completo, renovación y declaración de pérdida."],
        ["Sprint 3", "Cobrar con caja cuadrada y sin duplicados.", "US-18, US-19, US-20, US-21", "26",
         "Registro de pagos con cuadre, idempotencia, historial y reversión."],
        ["Sprint 4", "Recuperer la morosidad de forma automática y explicable.", "US-22, US-23, US-24, US-25, US-26", "26",
         "Moras diarias y manuales, consulta por préstamo, cobranza y recordatorios."],
        ["Sprint 5", "Cerrar la gestión con números confiables.", "US-27, US-28, US-29", "18",
         "Libro de capital, reportes con exportación y tablero de indicadores."],
        ["Sprint 6", "Sostener la operación en dispositivos y ante incidentes.", "US-30, US-31", "16",
         "Operación offline con actualización avisada, cabeceras de seguridad y respaldos."],
        ["Backlog futuro", "Ampliar el alcance comercial del producto.", "US-03, US-32", "16",
         "Recuperación de contraseña y embudo de solicitudes; en refinamiento."],
    ],
    widths=[1.0, 2.3, 1.6, 0.6, 2.5],
    align_center_cols=(3,),
)

for sprint, objetivo, hist, entregable in [
    ("Sprint 0 · Fundamentos de seguridad",
     "El sistema debe ser inaccesible para quien no tenga cuenta y toda operación sensible debe "
     "quedar firmada por un usuario. Este sprint se prioriza porque ningún otro módulo es defendible "
     "sin autenticación, roles y auditoría.",
     "US-01, US-02, US-04, US-05 y US-06",
     "El entregable es una sesión estable con renovación automática, catálogo de cuentas con roles y "
     "auditoría operativa, más la implementación de la protección de rutas que hoy está inactiva en el "
     "frontend."),
    ("Sprint 1 · Clientes y originación",
     "El equipo debe poder pasar de cero a un préstamo firmado con su plan de cuotas, sin datos de "
     "prueba y sin saltos manuales de cálculo. El backlog de este sprint concentra la mayor cantidad "
     "de historias porque es la puerta de entrada de todo el flujo.",
     "US-07, US-08, US-09, US-10, US-11, US-12 y US-13",
     "El entregable es el ciclo completo de cliente y originación: alta, búsqueda, edición, catálogos "
     "activos, cálculo de cuotas y bloqueo por capital insuficiente."),
    ("Sprint 2 · Vida del préstamo",
     "Una vez entregado el dinero, la operación necesita seguir su evolución: consultar la cartera, "
     "ver el detalle y resolver renovaciones y pérdidas sin dejar cabos sueltos contablemente.",
     "US-14, US-15, US-16 y US-17",
     "El entregable es la administración de la cartera con listados filtrables, detalle completo y "
     "las dos decisiones de riesgo documentadas."),
    ("Sprint 3 · Cobro confiable",
     "El cobro es el momento en que el sistema toca dinero real; el objetivo es que cada cobro "
     "cuadre, quede clasificado y no se duplique aunque la red falle.",
     "US-18, US-19, US-20 y US-21",
     "El entregable es el registro de pagos con validación de cuadre, protección de duplicados, "
     "historial de consultas y el flujo de reversión con auditoría."),
    ("Sprint 4 · Mora y cobranza",
     "La morosidad se gestiona con datos, no con recordatorios manuales: el objetivo es que el "
     "sistema calcule, explique y avise por su cuenta.",
     "US-22, US-23, US-24, US-25 y US-26",
     "El entregable es el cálculo automático y manual de moras, la consulta explicativa por préstamo, "
     "la lista de cobranza y los recordatorios push."),
    ("Sprint 5 · Cierre gerencial",
     "La administración necesita cerrar el periodo con números que pueda defender: capital trazable, "
     "reportes exportables y un tablero que responda de un vistazo.",
     "US-27, US-28 y US-29",
     "El entregable es el libro de movimientos de capital, los reportes de ganancias y pérdidas con "
     "exportación a Excel y PDF, y el tablero de indicadores."),
    ("Sprint 6 · Sostenibilidad de la plataforma",
     "La operación no puede detenerse por una caída de red ni por una actualización; este sprint "
     "refuerza la plataforma sobre la que corre todo lo anterior.",
     "US-30 y US-31",
     "El entregable es la operación con conexión intermitente, la actualización avisada de la "
     "aplicación, las cabeceras de seguridad y el respaldo programado de datos."),
]:
    d.h2(sprint)
    d.p(f"**Objetivo.** {objetivo}")
    d.p(f"**Historias comprometidas.** {hist}.")
    d.p(f"**Entregable.** {entregable}")

# ==================================================== 7. Casos de prueba
d.h1("7. Casos de prueba")
d.p(
    "Cada requerimiento funcional tiene un caso de prueba numerado en paralelo: RF-036 se verifica con "
    "CP-036. El caso hereda la prioridad del requisito y se ejecuta en el sprint donde se compromete "
    "la historia que lo implementa. La columna de tipo indica si hoy existe automatización de pruebas "
    "para el comportamiento; el repositorio cuenta con pruebas unitarias del cálculo financiero, de "
    "fechas y de formato, de modo que el resto de los casos se ejecuta de forma funcional manual."
)
cp_rows = []
for i in range(1, 76):
    code = "RF-%03d" % i
    info = CATALOG[code]
    prioridad = ("P1" if info["prioridad"] in ("Máxima", "Maxima")
                 else "P2" if info["prioridad"] == "Alta" else "P3")
    tipo = "Unitario" if i in (25, 27) else "Funcional manual"
    cp_rows.append(["CP-%03d" % i, code, info["nombre"], prioridad,
                    "Sprint %d" % sprint_of(code), tipo])
d.table(
    "Matriz de casos de prueba CP-001 a CP-075",
    ["Caso", "Requisito", "Objetivo de verificación", "Prioridad", "Sprint", "Tipo"],
    cp_rows,
    widths=[0.7, 0.7, 3.0, 0.7, 0.9, 1.0],
    align_center_cols=(0, 1, 3, 4),
)
d.p(
    "Un caso se considera aprobado cuando el requisito se comporta como se describe en el documento "
    "de requisitos, incluidas sus condiciones de aceptación y sus reglas de negocio asociadas; se "
    "considera reprobado cuando el comportamiento observado se desvía, y bloqueado cuando no puede "
    "ejecutarse por una falla previa. Los resultados se registran en la revisión de fin de sprint "
    "junto con los defectos detectados."
)

# ==================================================== 8. Ceremonias
d.h1("8. Ceremonias y definiciones de trabajo")
d.table(
    "Ceremonias del equipo",
    ["Ceremonia", "Frecuencia", "Duración orientativa", "Resultado esperado"],
    [
        ["Planificación de sprint", "Inicio de sprint", "2 horas", "Objetivo del sprint e historias comprometidas."],
        ["Reunión diaria", "Diaria", "15 minutos", "Avance, impedimientos y ajuste del plan del día."],
        ["Refinamiento de backlog", "Semanal", "1 hora", "Historias refinadas y estimadas para el siguiente sprint."],
        ["Revisión de fin de sprint", "Fin de sprint", "1 hora", "Incremento demostrado y aceptado por los stakeholders."],
        ["Retrospectiva", "Fin de sprint", "45 minutos", "Mejoras de proceso comprometidas para el siguiente sprint."],
    ],
    widths=[1.8, 1.2, 1.4, 2.6],
)
d.p(
    "La **Definition of Ready** exige que una historia entre a un sprint con criterios de aceptación "
    "cerrados, dependencias resueltas, diseño de interfaz definido y su trazabilidad con requerimiento "
    "y caso de prueba asignados. Sin esos cuatro elementos la historia permanece en refinamiento."
)
d.p(
    "La **Definition of Done** exige que la historia esté implementada en frontend y backend, con las "
    "validaciones de servidor, con la auditoría correspondiente si toca datos sensibles, probada contra "
    "su caso de prueba, revisada estáticamente por otro miembro del equipo, documentada en el manual "
    "correspondiente y desplegada en el entorno de pruebas. Una historia que cumpla todo salvo la "
    "documentación se considera terminada con deuda explícita registrada en el sprint."
)

# ==================================================== 9. Métricas
d.h1("9. Métricas y control del plan")
d.p(
    "El plan se controla con pocas métricas, elegidas por su capacidad de revelar problemas antes de "
    "que se conviertan en sorpresas. La velocidad promedio mide los puntos entregados por sprint y es "
    "la base para comprometer el siguiente. El porcentaje de historias comprometidas que se terminan "
    "mide la realista del plan; por debajo del 80 por ciento de forma sostenida se reduce el alcance. "
    "Los defectos por historia miden la calidad del incremento y la tasa de casos de prueba aprobados "
    "mide la cobertura funcional real del sistema."
)
d.table(
    "Indicadores de seguimiento del equipo",
    ["Indicador", "Fórmula", "Meta"],
    [
        ["Velocidad", "Puntos terminados por sprint.", "Entre 26 y 32 puntos."],
        ["Compromiso cumplido", "Historias terminadas dividido entre historias comprometidas.", "80 por ciento o más."],
        ["Tasa de aprobación de casos", "Casos aprobados dividido entre casos ejecutados.", "95 por ciento o más."],
        ["Defectos por historia", "Defectos abiertos dividido entre historias terminadas.", "Menor que 0,5."],
        ["Deuda técnica registrada", "Hallazgos de auditoría abiertos.", "Descenso continuo mes a mes."],
    ],
    widths=[1.8, 3.4, 1.8],
)

# ==================================================== 10. Riesgos
d.h1("10. Riesgos del plan")
d.table(
    "Riesgos del plan de trabajo",
    ["Riesgo", "Impacto potencial", "Respuesta prevista"],
    [
        ["Corregir la protección de rutas revela fallos en pantallas administrativas.", "Retraso en el Sprint 0.", "Alinear la prueba de rol con el backend desde el primer día."],
        ["El arreglo del endpoint de moras afecta pantallas ya entregadas.", "Regresiones en cobranza.", "Cubrir el módulo con su caso CP-045 antes de cerrar el sprint."],
        ["Las historias de integraciones externas no tienen proveedor definido.", "Bloqueo del Sprint 6.", "Mantenerlas en backlog futuro hasta firmar el alcance."],
        ["La automatización de pruebas es todavía mínima.", "Mayor esfuerzo de verificación manual.", "Automatizar primero cálculo financiero y pagos, donde está el riesgo de dinero."],
        ["Cambios de alcance solicitados a mitad de sprint.", "Contaminación del objetivo del sprint.", "Todo cambio entra al backlog y se negocia en la planificación siguiente."],
    ],
    widths=[2.6, 2.0, 2.4],
)

d.references([
    "Equipo de Ingeniería de Software. (2026). *Documento de Requerimientos del Software de LoanSoft*. "
    "LoanSoft.",
    "Schwaber, K., & Sutherland, J. (2020). *The Scrum Guide: The Definitive Guide to Scrum*. "
    "Scrum.org.",
    "Equipo de Ingeniería de Software. (2026). *Manual Técnico de LoanSoft*. LoanSoft.",
])
d.save(os.path.join(OUT, "04_Plan_Scrum.docx"))
print("Plan Scrum generado")
