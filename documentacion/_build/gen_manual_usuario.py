# -*- coding: utf-8 -*-
"""Genera el Manual de Usuario de LoanSoft."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from apa import Doc  # noqa: E402

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")

d = Doc(
    title="**Manual de Usuario**",
    subtitle="Guía operativa del sistema LoanSoft",
    author=["Equipo de Ingeniería de Software · LoanSoft"],
    affiliation=["LoanSoft · Sistema de Gestión de Préstamos"],
    date=["28 de septiembre de 2026"],
    extra=["Versión 1.0",
           "Dirigido a gestores, administradores y personal de cobranza"],
)

d.abstract(
    "Este manual explica, paso a paso, cómo operar LoanSoft en la rutina de un negocio de préstamos: "
    "acceder al sistema, registrar clientes, crear préstamos, cobrar cuotas, revisar moras, mover "
    "capital y producir reportes. Describe cada pantalla tal como está construida hoy, con los campos "
    "reales del formulario, las validaciones que aplica el sistema y las limitaciones conocidas que "
    "el usuario debe tener presentes."
)

# ============================================================ 1. Introducción
d.h1("1. Introducción")
d.p(
    "LoanSoft centraliza la operación de préstamos en un solo lugar. En lugar de llevar cuadernos de "
    "cobro, cálculos manuales y hojas de cálculo dispersas, el sistema mantiene la ficha de cada "
    "cliente, el detalle de cada préstamo, el estado de cada cuota y un registro de cada movimiento "
    "de dinero. Cuando un dato se registra en el sistema, queda disponible para el resto de las "
    "pantallas: lo que se cobra en el módulo de préstamos alimenta el tablero, los reportes y el "
    "libro de capital."
)
d.h2("1.1 Para quién es este manual")
d.p(
    "El manual está pensado para tres perfiles. El **gestor** atiende clientes, registra préstamos y "
    "cobra cuotas. El **administrador** además administra usuarios, catálogos y parámetros del "
    "sistema, y ejecuta el procesamiento de moras. El **responsable de cobranza** consulta los "
    "vencimientos y da seguimiento a las deudas atrasadas. Cada procedimiento indica en su momento "
    "cuál de los perfiles puede realizarlo."
)
d.h2("1.2 Requisitos de acceso")
d.p(
    "Se necesita un navegador actualizado en una computadora o un dispositivo móvil con conexión a "
    "internet, una cuenta activa entregada por el administrador y la dirección pública del sistema. "
    "La primera vez que se ingresa conviene cambiar la contraseña asignada desde el perfil. La "
    "aplicación también puede instalarse en el dispositivo para abrirse como una ventana independiente."
)
d.h2("1.3 Cómo está organizado el manual")
d.p(
    "El capítulo 2 describe el acceso y el perfil. El capítulo 3 explica los elementos de navegación "
    "comunes a todas las pantallas. De los capítulos 4 a 11 se describe cada módulo con su "
    "procedimiento de trabajo. El capítulo 12 reúne los problemas frecuentes con su solución y el "
    "capítulo 13 define la terminología utilizada."
)

# ======================================================= 2. Primeros pasos
d.h1("2. Primeros pasos: acceso y perfil")
d.h2("2.1 Inicio de sesión")
d.p(
    "Al abrir el sistema aparece la pantalla de acceso con dos campos: correo electrónico y "
    "contraseña. Se escribe el correo asignado, la contraseña de al menos seis caracteres y se pulsa "
    "el botón de ingreso. Si las credenciales son correctas, el sistema guarda la sesión y muestra el "
    "tablero. Si no lo son, aparece un mensaje de error sin indicar si el problema está en el correo "
    "o en la contraseña; en ese caso se revisan ambos datos y se vuelve a intentar."
)
d.p(
    "La sesión permanece activa durante la jornada. Si el navegador la da por vencida, el sistema "
    "intenta renovarla de forma automática; si ya no es posible, devuelve a la pantalla de acceso. "
    "Para salir de forma deliberada se usa la opción de cierre de sesión del menú de usuario, "
    "situado en la parte superior derecha junto al nombre."
)
d.h2("2.2 Cambio de contraseña")
d.p(
    "Desde el perfil se actualiza la contraseña. El formulario pide la contraseña actual, la nueva y "
    "su confirmación; la nueva debe tener al menos seis caracteres y las dos últimas entradas deben "
    "coincidir. Al guardar, el sistema valida la contraseña actual, aplica el cambio y limpia los "
    "campos. Si la contraseña actual es incorrecta, el formulario lo indica y no se modifica nada."
)
d.h2("2.3 Asistente de configuración inicial")
d.p(
    "En el primer ingreso el sistema ofrece un asistente breve para dejar la operación lista: se "
    "registran los tipos de préstamo con su interés mensual y su máximo de cuotas, los tipos de pago "
    "disponibles, el capital inicial con el que cuenta la caja y un primer cliente. El asistente "
    "permite omitir cualquier paso y retomarse después, de modo que nunca bloquea el uso normal del "
    "sistema."
)

# ======================================================= 3. Navegación
d.h1("3. Navegación general")
d.p(
    "La aplicación se organiza en un conjunto reducido de pantallas accesibles desde el menú lateral. "
    "El siguiente mapa resume dónde está cada función y en qué orden se suele recorrer: se parte del "
    "tablero, se trabaja con clientes, préstamos y pagos, y se cierra con la gestión, la cobranza y "
    "el control administrativo."
)
d.figure(os.path.join(FIGS, "fig8_mapa_navegacion.png"),
         "Mapa de navegación de las pantallas principales de LoanSoft.")
d.table(
    "Pantallas del sistema y su propósito",
    ["Pantalla", "Ruta", "Qué se hace allí"],
    [
        ["Tablero", "/", "Revisar los indicadores del negocio de un vistazo."],
        ["Clientes", "/clientes", "Registrar, buscar, editar y dar de baja clientes."],
        ["Préstamos", "/prestamos", "Listar y filtrar préstamos; crear uno nuevo."],
        ["Detalle de préstamo", "/prestamos/{id}", "Ver cuotas, registrar pagos, renovar o marcar como perdido."],
        ["Nuevo préstamo", "/prestamos/nuevo", "Originar un préstamo con su plan de cuotas."],
        ["Pagos", "/pagos", "Revisar el cobro registrado en el día."],
        ["Cobranza", "/cobranza", "Trabajar las deudas vencidas."],
        ["Moras", "/moras", "Consultar y procesar las penalizaciones."],
        ["Capital", "/capital", "Ver el saldo disponible y su historial de movimientos."],
        ["Reportes", "/reportes", "Producir ganancias, pérdidas y exportaciones."],
        ["Usuarios", "/usuarios", "Administrar cuentas y roles."],
        ["Tipos de préstamo", "/tipos-prestamo", "Administrar el catálogo de crédito."],
        ["Tipos de pago", "/tipos-pago", "Administrar los medios de cobro."],
        ["Perfil", "/perfil", "Consultar los datos propios y cambiar la contraseña."],
    ],
    widths=[1.7, 1.6, 3.7],
)
d.h2("3.1 Elementos comunes")
d.p(
    "La cabecera muestra el nombre del usuario, que además da acceso a su perfil y al cierre de "
    "sesión, e incluye el botón de importación de extractos, cuya pantalla aún funciona con datos de "
    "demostración y por lo tanto no debe usarse en operación real. Junto a la navegación aparecen "
    "elementos de apoyo: un indicador de sincronización que informa si hay operaciones pendientes de "
    "envío, un aviso de conexión cuando la red se interrumpe, una calculadora rápida para resolver "
    "operaciones sin salir de la pantalla y un asistente de instalación cuando el navegador permite "
    "añadir la aplicación al escritorio."
)
d.p(
    "Los listados comparten un mismo comportamiento: encabezado con título y acción principal, barra "
    "de filtros, tabla con sus columnas y control de paginación en la parte inferior. Los estados "
    "vacíos explican por qué no hay datos y, cuando corresponde, ofrecen el botón para crear el "
    "primer registro."
)

# ============================================================ 4. Tablero
d.h1("4. El tablero")
d.p(
    "El tablero es la primera pantalla después del ingreso y reúne los indicadores que definen la "
    "salud del negocio. Se organiza en tarjetas de resumen y gráficos de distribución."
)
d.table(
    "Indicadores del tablero",
    ["Indicador", "Qué representa", "Cómo se calcula"],
    [
        ["Capital actual", "Dinero disponible para prestar en este momento.", "Capital total menos los préstamos otorgados más los cobros de capital."],
        ["Préstamos activos", "Cantidad de préstamos vigentes que se están pagando.", "Préstamos en estado activo."],
        ["Saldo pendiente total", "Dinero que falta por cobrar de toda la cartera.", "Suma de los saldos pendientes de los préstamos activos."],
        ["Ganancia del periodo", "Utilidad reconocida en el periodo consultado.", "Intereses efectivamente cobrados."],
        ["Total prestado", "Monto desembolsado históricamente.", "Suma de los capitales prestados."],
        ["Préstamos perdidos", "Declaraciones de incobrabilidad registradas.", "Préstamos marcados como perdidos."],
    ],
    widths=[1.6, 2.6, 3.0],
)
d.p(
    "Cuando el sistema no tiene información suficiente para un indicador, la tarjeta muestra la leyenda "
    "de ausencia de datos en lugar de un cero engañoso. Los importes se presentan con el formato "
    "monetario configurado y se actualizan al recargar la pantalla o al abrir una nueva sesión."
)

# ============================================================ 5. Clientes
d.h1("5. Gestión de clientes")
d.p(
    "El cliente es la puerta de entrada de la operación: no se puede originar un préstamo sin una "
    "ficha de cliente registrada. La pantalla de clientes concentra el alta, la búsqueda, la edición "
    "y la baja lógica."
)
d.h2("5.1 Registro de un cliente")
d.p(
    "Se abre el formulario de cliente desde el botón de alta y se completan los campos. Los "
    "obligatorios están marcados con asterisco: nombre completo y cédula. Teléfono, dirección, "
    "persona de referencia, teléfono de referencia y observaciones son opcionales, pero cuanto más "
    "completa esté la ficha, más fácil será el cobro posterior. El campo de estado permite dejar el "
    "cliente activo o inactivo; un cliente inactivo no podrá recibir préstamos nuevos."
)
d.table(
    "Campos del formulario de cliente",
    ["Campo", "Obligatorio", "Observaciones"],
    [
        ["Nombre completo", "Sí", "Nombre y apellidos del titular."],
        ["Cédula", "Sí", "Identificador único; no puede repetirse."],
        ["Teléfono", "No", "Número de contacto principal."],
        ["Dirección", "No", "Domicilio declarado."],
        ["Persona de referencia", "No", "Contacto alternativo para cobranza."],
        ["Teléfono de referencia", "No", "Número de la persona de referencia."],
        ["Estado", "Sí", "Activo o inactivo; controla la posibilidad de prestar."],
        ["Observaciones", "No", "Notas internas sobre el cliente."],
    ],
    widths=[2.0, 1.0, 4.0],
    align_center_cols=(1,),
)
d.p(
    "Al guardar, el sistema valida el formato de la cédula y comprueba que no exista otra ficha con el "
    "mismo número. Si la cédula ya está registrada, el formulario señala el conflicto y conserva lo "
    "escrito para que se corrija únicamente el dato erróneo."
)
d.h2("5.2 Búsqueda y edición")
d.p(
    "Para localizar un cliente se escribe en el campo de búsqueda parte de su nombre, su cédula o su "
    "teléfono, y la lista se reduce a los coincidentes. Desde la fila seleccionada se abre la ficha "
    "para editarla, con los mismos campos del alta, o para darla de baja. La baja es lógica: el "
    "registro se conserva para que los préstamos históricos sigan siendo consultables, pero el "
    "cliente deja de estar disponible para nueva operación."
)

# ============================================================ 6. Préstamos
d.h1("6. Originación y administración de préstamos")
d.p(
    "El módulo de préstamos es el corazón del sistema. Aquí se crea la deuda con su plan de cuotas, "
    "se consulta su evolución, se registran los cobros y se resuelven las decisiones de riesgo como "
    "la renovación o la declaración de pérdida."
)
d.h2("6.1 Crear un préstamo")
d.p(
    "Desde el listado se pulsa el botón de nuevo préstamo y se completa el formulario. El sistema "
    "solicita el cliente, el tipo de préstamo, la fecha, el capital a prestar, el interés mensual y "
    "el número de cuotas. Al elegir el tipo de préstamo, el interés y el máximo de cuotas se "
    "completan con los valores del catálogo, aunque pueden ajustarse dentro de los límites "
    "permitidos. El campo de observaciones admite notas sobre las condiciones acordadas."
)
d.table(
    "Campos del formulario de préstamo",
    ["Campo", "Obligatorio", "Qué controla"],
    [
        ["Cliente", "Sí", "Titular de la deuda; solo aparecen clientes activos."],
        ["Tipo de préstamo", "Sí", "Define interés mensual y máximo de cuotas."],
        ["Fecha del préstamo", "Sí", "Fecha desde la que se devenga y se cobra."],
        ["Capital a prestar", "Sí", "Monto entregado; debe estar disponible en caja."],
        ["Interés mensual (%)", "Sí", "Porcentaje aplicado por cuota."],
        ["Número de cuotas", "Sí", "Plazo en cuotas mensuales."],
        ["Observaciones", "No", "Notas de la operación."],
    ],
    widths=[2.0, 1.0, 4.0],
    align_center_cols=(1,),
)
d.p(
    "Al confirmar, el sistema calcula el interés total, el monto total y el valor de la cuota, genera "
    "todas las cuotas en estado pendiente y descuenta el capital prestado del saldo disponible. Si "
    "el capital no alcanza, el sistema rechaza la operación y explica el motivo; en ese caso no se "
    "crea el préstamo ni se modifica el capital."
)
d.h2("6.2 Listado y filtros")
d.p(
    "La pantalla de préstamos presenta la cartera con sus datos principales: cliente, monto, cuotas "
    "pagadas frente al total, saldo pendiente y estado. Los filtros permiten acotar por estado —activo, "
    "pagado, perdido o renovado— y por periodo, lo que agiliza la localización de una operación "
    "concreta."
)
d.h2("6.3 Detalle de un préstamo")
d.p(
    "Al abrir un préstamo se muestran sus tarjetas de resumen con capital prestado, interés, monto "
    "total, valor de la cuota y saldo pendiente, junto con el estado actual. Debajo aparecen las "
    "pestañas con las cuotas, los pagos y la información general del préstamo."
)
d.p(
    "Cuando el préstamo está activo, la cabecera ofrece tres acciones. **Registrar pago** abre el "
    "formulario de cobro descrito en el capítulo siguiente. **Renovar** permite aplicar un abono al "
    "saldo y abrir un nuevo préstamo con las condiciones actualizadas, indicando abono, interés mensual, "
    "número de cuotas, fecha de renovación y observaciones; el abono nunca puede superar el saldo "
    "pendiente. **Perdido** registra la declaración de incobrabilidad con su fecha y su motivo, y "
    "descuenta el saldo del capital disponible. Una vez que el préstamo está pagado, perdido o "
    "renovado, estas acciones dejan de estar disponibles."
)
d.p(
    "Las cuotas se presentan con su número, fecha de vencimiento, valor, estado y los importes ya "
    "pagados de capital, interés y mora. Los estados posibles de una cuota son pendiente, vencida, "
    "parcial y pagada."
)

# ============================================================ 7. Pagos
d.h1("7. Registro de pagos")
d.p(
    "El cobro se registra desde el detalle del préstamo, y también desde la pantalla de pagos para "
    "revisar lo cobrado. El formulario pide buscar el préstamo, indicar la cuota a pagar, el tipo de "
    "pago, la fecha, el valor pagado y el desglose entre capital, interés y mora. El campo de "
    "observaciones admite notas sobre el cobro, como la referencia de una transferencia."
)
d.table(
    "Campos del formulario de pago",
    ["Campo", "Obligatorio", "Observaciones"],
    [
        ["Buscar préstamo", "Sí", "Se localiza por el identificador o el cliente."],
        ["Cuota a pagar", "Sí", "Solo se listan cuotas con saldo."],
        ["Tipo de pago", "Sí", "Efectivo, transferencia u otro medio del catálogo."],
        ["Fecha de pago", "Sí", "Fecha en que se recibió el dinero."],
        ["Valor pagado", "Sí", "Monto total recibido."],
        ["Capital", "Sí", "Parte que reduce la deuda."],
        ["Interés", "Sí", "Parte que reconoce la utilidad."],
        ["Mora", "Sí", "Parte que cubre la penalización."],
        ["Observaciones", "No", "Referencia o nota del cobro."],
    ],
    widths=[2.0, 1.0, 4.0],
    align_center_cols=(1,),
)
d.p(
    "El sistema exige que la suma de capital, interés y mora coincida con el valor pagado dentro de un "
    "centavo. Si hay diferencia, el formulario lo indica y no se guarda nada: así se evitan descuadres "
    "de caja difíciles de explicar después. Registrado el pago, el saldo del préstamo baja en la parte "
    "de capital, la cuota pasa a parcial o pagada según corresponda, el capital disponible sube y, si "
    "el saldo llega a cero, el préstamo se cierra automáticamente como pagado."
)
d.p(
    "El sistema también evita cobros duplicados: si una misma operación se envía dos veces por un "
    "problema de conexión, la segunda no genera un cobro adicional. En cuanto a la revisión, el "
    "detalle del préstamo lista todos sus pagos con fecha, valor y desglose; hoy la consulta global de "
    "todos los pagos del sistema no está disponible y redirige al detalle del préstamo correspondiente."
)

# ==================================================== 8. Moras y cobranza
d.h1("8. Moras y cobranza")
d.p(
    "Las moras se generan de forma automática cada día a medianoche sobre las cuotas vencidas, "
    "aplicando la tasa diaria y los días de gracia definidos en la configuración del sistema. El "
    "usuario no calcula nada manualmente: consulta el resultado y actúa en consecuencia."
)
d.p(
    "La pantalla de moras lista las penalizaciones generadas y ofrece el botón de procesamiento "
    "inmediato para quienes administran el sistema, útil cuando se detecta un desfase o cuando se "
    "corrigió una tasa. El procesamiento manual ejecuta exactamente el mismo cálculo que el proceso "
    "diario y devuelve el total de moras generadas en esa ejecución."
)
d.p(
    "La pantalla de cobranza está orientada a la jornada de trabajo: agrupa las deudas vencidas para "
    "que el responsable de cobro pueda visitar o llamar con la información correcta. Limitaciones "
    "conocidas: la consulta de moras por préstamo aún no se conecta con el servidor, por lo que esa "
    "vista puede devolver un error de recurso inexistente, y la lista de cobranza puede aparecer vacía "
    "aunque existan vencimientos; en ambos casos la vía de respaldo es consultar las cuotas en el "
    "detalle de cada préstamo."
)

# ============================================================ 9. Capital
d.h1("9. Capital y movimientos")
d.p(
    "El capital es el dinero disponible para prestar. La pantalla de capital muestra el saldo actual "
    "y el historial de cada movimiento con su tipo, valor, fecha y el préstamo asociado. Los tipos de "
    "movimiento distinguen el préstamo otorgado, que descuenta, el pago recibido, que incrementa, y "
    "la pérdida, que descuenta de nuevo."
)
d.p(
    "Esta pantalla es el libro de contabilidad mínimo del negocio: ante cualquier duda sobre un monto, "
    "el detalle de movimientos permite reconstruir cómo se llegó al saldo actual. El saldo nunca debe "
    "ser negativo; si una operación lo dejaría así, el sistema la rechaza antes de aplicarla."
)

# ============================================================ 10. Reportes
d.h1("10. Reportes y exportaciones")
d.p(
    "La pantalla de reportes produce dos documentos principales con el periodo seleccionado. El "
    "reporte de ganancias muestra los intereses cobrados y el resultado neto, con el detalle por "
    "préstamo. El reporte de pérdidas lista los préstamos declarados incobrables con su valor y su "
    "motivo. Ambos incluyen tarjetas de resumen y tablas de detalle."
)
d.table(
    "Reportes disponibles",
    ["Reporte", "Contenido", "Exportación"],
    [
        ["Ganancias", "Intereses cobrados, cantidad de préstamos y resultado del periodo.", "Excel y PDF"],
        ["Pérdidas", "Préstamos perdidos, valor perdido y motivos registrados.", "Excel y PDF"],
        ["Cartera", "Saldos por préstamo, antigüedad y distribución por estado.", "Pendiente de interfaz"],
        ["Cobranza", "Total cobrado en el periodo con desglose de capital, interés y mora.", "Pendiente de interfaz"],
    ],
    widths=[1.4, 4.1, 1.5],
)
d.p(
    "Para exportar se elige el formato y el sistema descarga el archivo respetando el periodo filtrado "
    "sin abrir otra ventana. Los reportes de cartera y de cobranza ya existen en el servidor pero "
    "todavía no tienen pantalla propia, por lo que no aparecen en la interfaz."
)

# ==================================================== 11. Administración
d.h1("11. Administración")
d.p(
    "El perfil de administrador dispone de tres pantallas adicionales. En **usuarios** se crean "
    "cuentas con nombre, correo, contraseña y rol, se editan y se desactivan; la desactivación retira "
    "el acceso sin borrar el historial de operaciones del usuario. En **tipos de préstamo** se "
    "administra el catálogo con nombre, descripción, interés mensual, máximo de cuotas y estado. En "
    "**tipos de pago** se administran los medios de cobro con nombre, descripción y estado."
)
d.p(
    "Antes de eliminar un tipo con operaciones asociadas, el sistema recomienda desactivarlo para no "
    "romper la trazabilidad histórica. Los tipos inactivos dejan de aparecer en los formularios de "
    "originación y de cobro, pero se conservan en los registros antiguos."
)
d.p(
    "Limitación conocida: en la versión actual la protección de las pantallas administrativas no "
    "reconoce el rol del usuario, por lo que esas direcciones pueden no abrirse desde el menú. Mientras "
    "se corrige, las operaciones administrativas deben coordinarse con el equipo responsable del "
    "sistema."
)

# =============================================== 12. Solución de problemas
d.h1("12. Solución de problemas")
d.p(
    "La siguiente tabla recoge las situaciones más frecuentes y la acción recomendada. Si una "
    "situación persiste después de aplicar la acción indicada, conviene registrar el mensaje mostrado "
    "por el sistema y la hora exacta para reportarlo."
)
d.table(
    "Problemas frecuentes y solución recomendada",
    ["Situación", "Causa probable", "Acción recomendada"],
    [
        ["La aplicación devuelve al inicio de sesión al cambiar de pestaña", "La sesión expiró.", "Volver a ingresar; el sistema renueva la sesión automáticamente cuando es posible."],
        ["No aparecen registros en una lista que sí existen", "El filtro está demasiado estrecho o se consultó la primera página.", "Limpiar los filtros, ampliar el periodo y revisar la paginación."],
        ["El sistema rechaza un pago", "La suma de capital, interés y mora no coincide con el valor pagado.", "Ajustar el desglose para que cuadre con el total recibido."],
        ["No se puede crear un préstamo por falta de capital", "El saldo disponible es menor que el monto solicitado.", "Revisar la pantalla de capital y, si corresponde, registrar un aporte."],
        ["Un cliente no aparece al crear el préstamo", "La ficha está inactiva.", "Editar el cliente y ponerlo en estado activo."],
        ["La lista de moras muestra un error", "Consulta desconectada del servidor.", "Revisar las cuotas en el detalle del préstamo y reportar la incidencia."],
        ["La pantalla de cobranza aparece vacía", "Falla conocida en la lectura de datos.", "Usar el detalle de préstamos como respaldo."],
        ["Las páginas de administración no abren", "Protección de rutas sin reconocer el rol.", "Coordinar con el equipo responsable del sistema."],
        ["Los recordatorios push no llegan", "El navegador no autorizó las notificaciones.", "Permitir notificaciones desde la configuración del sitio."],
        ["La aplicación no se instala en el dispositivo", "Faltan los iconos del manifiesto.", "Abrirla en el navegador de escritorio o reportar la incidencia."],
        ["Se registró un cobro por error", "No existe anulación desde la interfaz.", "Reportar al administrador para su reversión con auditoría."],
    ],
    widths=[2.2, 2.1, 2.7],
)

# ============================================================ 13. Glosario
d.h1("13. Glosario")
d.table(
    "Términos utilizados en el manual",
    ["Término", "Significado"],
    [
        ["Capital prestado", "Dinero entregado al cliente en la originación."],
        ["Capital disponible", "Saldo que la caja puede prestar en este momento."],
        ["Cuota", "Fracción mensual de capital e interés que el cliente debe pagar."],
        ["Vencida", "Cuota cuya fecha ya pasó sin cobro completo."],
        ["Parcial", "Cuota con un abono que no cubre su valor total."],
        ["Mora", "Penalización diaria aplicada a las cuotas vencidas."],
        ["Saldo pendiente", "Dinero que falta por pagar del monto total del préstamo."],
        ["Renovación", "Apertura de un nuevo préstamo que absorbe el saldo vivo del anterior."],
        ["Préstamo perdido", "Declaración formal de que la deuda no se cobrará."],
        ["Cartera", "Conjunto de préstamos vigentes del negocio."],
        ["Idempotencia", "Garantía de que un cobro repetido no se registra dos veces."],
    ],
    widths=[1.8, 5.2],
)

d.references([
    "Equipo de Ingeniería de Software. (2026). *Documento de Requerimientos del Software de LoanSoft*. "
    "LoanSoft.",
    "Equipo de Ingeniería de Software. (2026). *Manual Técnico de LoanSoft*. LoanSoft.",
    "Equipo de Ingeniería de Software. (2026). *BLUEPRINT_LOANSOFT: alcance y fases del sistema*. "
    "LoanSoft.",
])
d.save(os.path.join(OUT, "03_Manual_de_Usuario.docx"))
print("Manual de usuario generado")
