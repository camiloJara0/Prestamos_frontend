# -*- coding: utf-8 -*-
"""Genera la Guía de Tareas del Usuario (documento para usuarios del sistema)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from apa import Doc  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
FIGS = os.path.join(HERE, "figs")

DISP = "Disponible"
LIM = "Con limitaciones"
FUT = "Próximamente"

# Cada capítulo aporta sus tareas: (título, introducción,
# [(n.º, tarea, cuándo se hace, estado, pasos, resultado)])
CAPS = [
    ("4. Acceso y perfil",
     "Toda tarea empieza con una sesión abierta. Estas cinco tareas son las que usted realiza para "
     "entrar, identificarse y cuidar el acceso a su cuenta; son el punto de partida de todo lo demás.",
     [
         ("T-01", "Iniciar sesión",
          "Al llegar al sistema y cada vez que la sesión haya terminado por inactividad.", DISP,
          ["Escriba su correo electrónico.",
           "Escriba su contraseña.",
           "Pulse el botón de ingreso."],
          "Se abre la pantalla principal con su nombre en la parte superior. Si la contraseña no "
          "coincide aparece un aviso y no se muestra ningún dato del negocio. Si la sesión lleva mucho "
          "tiempo abierta, el sistema la renueva por su cuenta mientras siga trabajando."),
         ("T-02", "Cerrar sesión",
          "Al terminar su turno o cuando deje la computadora disponible para otra persona.", DISP,
          ["Abra el menú de su nombre, en la esquina superior derecha.",
           "Elija la opción de cierre de sesión."],
          "La cuenta queda cerrada: quien se siente después debe volver a ingresar con su propia "
          "contraseña para ver cualquier dato."),
         ("T-03", "Comprobar con qué cuenta estoy trabajando",
          "Cuando quiera confirmar que los datos del sistema se están registrando a su nombre.", DISP,
          ["Mire su nombre junto al menú superior.",
           "Abra su perfil para ver el correo y el rol asignado."],
          "Si el nombre o el rol no coinciden con el que le corresponde, deje de trabajar y solicite "
          "la corrección al administrador, porque todo lo que haga quedará asociado a esa cuenta."),
         ("T-04", "Cambiar mi contraseña",
          "Cuando quiera renovarla o cuando el administrador se lo indique.", DISP,
          ["Abra su perfil.",
           "Escriba su contraseña actual.",
           "Escriba la contraseña nueva y vuelva a escribirla para confirmarla.",
           "Guarde el cambio."],
          "La contraseña nueva debe tener al menos seis caracteres y las dos entradas deben coincidir. "
          "Si la contraseña actual es incorrecta, el sistema lo advierte y no cambia nada."),
         ("T-05", "Recuperar una contraseña olvidada",
          "Cuando nadie recuerde la contraseña de una cuenta.", FUT,
          ["Mientras tanto, solicite al administrador que le asigne una nueva desde la pantalla de "
           "usuarios."],
          "Cuando la tarea esté disponible, la recuperación llegará por correo electrónico con un "
          "enlace que solo podrá usarse una vez."),
     ]),

    ("5. Cuentas, catálogos y ajustes",
     "Son las tareas del administrador. Permiten preparar el sistema antes de que empiece la operación: "
     "quién puede usarlo, con qué productos de crédito y bajo qué reglas. Conviene revisarlas cada vez "
     "que cambien las condiciones del negocio.",
     [
         ("T-06", "Dar de alta una cuenta de usuario",
          "Al incorporar una persona al equipo o al crear su propia cuenta de trabajo.", LIM,
          ["Abra la pantalla de Usuarios y pulse el botón de alta.",
           "Escriba nombre, correo electrónico y contraseña.",
           "Elija el rol que le corresponde a esa persona.",
           "Guarde."],
          "La persona ya puede iniciar sesión con ese correo. El sistema no permite repetir un correo "
          "registrado. Estas pantallas pueden no abrirse mientras el equipo responsable no active su "
          "acceso; solicítelo antes de planear el alta."),
         ("T-07", "Modificar una cuenta de usuario",
          "Cuando cambien el nombre, el correo o el rol de una persona.", LIM,
          ["Busque a la persona en el listado.",
           "Abrá y edite los campos que correspondan.",
           "Guarde."],
          "El cambio se aplica de inmediato y conserva el historial de operaciones que esa persona ya "
          "registró."),
         ("T-08", "Suspender el acceso de una persona",
          "Cuando alguien deje de trabajar con el sistema.", LIM,
          ["Busque a la persona en el listado.",
           "Pase su estado a inactivo y guarde."],
          "Deja de poder iniciar sesión sin borrar nada de lo que hizo. Si vuelve a necesitar acceso, "
          "basta con activar la cuenta de nuevo."),
         ("T-09", "Definir los tipos de préstamo",
          "Al preparar los productos de crédito o cuando cambien los intereses y los plazos.", LIM,
          ["Abra la pantalla de Tipos de préstamo y pulse el botón de alta.",
           "Escriba el nombre del producto y una descripción.",
           "Indique el interés mensual y el máximo de cuotas.",
           "Déjelo activo y guarde."],
          "Al crear un préstamo, elegir ese tipo completa solo el interés y el número de cuotas. Si un "
          "tipo ya se usa en préstamos antiguos, conviene desactivarlo en vez de borrarlo, para no "
          "perder el sentido de esos historiales."),
         ("T-10", "Definir los tipos de pago",
          "Al incorporar un medio de cobro nuevo, como transferencia o depósito.", LIM,
          ["Abra la pantalla de Tipos de pago y pulse el botón de alta.",
           "Escriba el nombre y una descripción.",
           "Déjelo activo y guarde."],
          "El tipo nuevo aparece en el formulario de cobro; los desactivados dejan de aparecer pero "
          "conservan el valor de los cobros antiguos."),
         ("T-11", "Ajustar la configuración general",
          "Cuando cambie la tasa de mora, los días de gracia o los datos generales del negocio.", LIM,
          ["Por ahora, solicite el cambio al equipo responsable del sistema.",
           "Cuando la pantalla esté disponible: abra Configuración, revise los valores vigentes, "
           "ajuste los que correspondan y guarde."],
          "A partir de ese momento, las moras que se calculan cada día usan los valores nuevos. "
          "Cambie solo lo que tenga claridad de su efecto, porque afecta a toda la cartera."),
         ("T-12", "Revisar quién hizo cada cambio",
          "Cuando necesite aclarar un alta, una edición o una eliminación.", LIM,
          ["Por ahora, solicite el reporte al equipo responsable del sistema.",
           "Cuando la pantalla esté disponible: ábrela, filtre por persona, por sección o por tipo de "
           "acción y consulte el resultado."],
          "Cada fila indicará quién actuó, qué registro tocó, qué valor tenía antes, cuál quedó y la "
          "fecha y hora exactas. Es la evidencia que resuelve cualquier discusión sobre un cambio."),
     ]),

    ("6. Clientes",
     "Sin ficha de cliente no hay préstamo posible. Este capítulo cubre el trabajo diario sobre la "
     "cartera de clientes: registrarlos, encontrarlos, corregirlos y sacarlos de operación cuando ya "
     "no corresponde prestarles.",
     [
         ("T-13", "Registrar un cliente",
          "Antes de crear su primer préstamo.", DISP,
          ["Abra la pantalla de Clientes y pulse el botón de alta.",
           "Escriba el nombre completo y la cédula, que son obligatorios.",
           "Complete teléfono, dirección, persona de referencia, teléfono de referencia y observaciones "
           "si los tiene.",
           "Déjelo en estado activo y guarde."],
          "La cédula no puede repetirse: si ya existe una ficha con ese número, el sistema lo advierte "
          "y conserva lo escrito para que corrija solo ese dato. Con la ficha guardada, el cliente ya "
          "puede recibir un préstamo."),
         ("T-14", "Buscar un cliente",
          "Cuando atienda a alguien por teléfono o se acerque al mostrador.", DISP,
          ["Escriba parte del nombre, la cédula o el teléfono en el buscador de la pantalla de "
           "Clientes."],
          "La lista se reduce a las coincidencias y desde ahí puede abrir la ficha para editarla o "
          "crear un préstamo a su nombre."),
         ("T-15", "Listar los clientes con filtros",
          "Cuando necesite revisar cuántos clientes hay o encontrar alguno por sus datos.", DISP,
          ["Abra la pantalla de Clientes y revise el listado.",
           "Use los filtros disponibles para acotar la búsqueda.",
           "Pase de página con el control inferior cuando la lista sea larga."],
          "Cada página muestra un bloque manejable de registros con sus datos principales, sin cargar "
          "la lista completa de una vez."),
         ("T-16", "Ver el detalle de un cliente",
          "Cuando quiera ver la ficha completa de una persona en su propia página.", FUT,
          ["Por ahora, consulte los datos desde el listado de clientes."],
          "La página de detalle reunirá ficha, préstamos y pagos de esa persona en un solo lugar."),
         ("T-17", "Editar la ficha de un cliente",
          "Cuando un teléfono o una dirección cambien.", DISP,
          ["Busque al cliente.",
           "Abrá su ficha y corrija lo que corresponda.",
           "Guarde."],
          "La edición no afecta los préstamos que el cliente ya tiene: quedan tal como se firmaron."),
         ("T-18", "Dar de baja a un cliente",
          "Cuando el cliente deje de operar con el negocio.", DISP,
          ["Busque al cliente.",
           "Pase su estado a inactivo y guarde."],
          "La ficha se conserva para consultar su historial, pero el nombre deja de aparecer al crear "
          "préstamos nuevos."),
         ("T-19", "Revisar el historial financiero de un cliente",
          "Cuando necesite ver todo lo que una persona debe y lo que ya pagó.", FUT,
          ["Mientras tanto, revise sus préstamos desde el listado general filtrando por esa persona."],
          "La tarea concentrará sus préstamos, sus pagos y su comportamiento de pago en una sola vista."),
         ("T-20", "Ver las estadísticas de un cliente",
          "Cuando quiera comparar el comportamiento de pago entre clientes.", FUT,
          ["No disponible todavía."],
          "Mostrará indicadores simples como saldo pendiente, puntualidad y cantidad de préstamos."),
     ]),

    ("7. Solicitudes de préstamo",
     "Es el embudo previo a la entrega de dinero: el cliente pide, el negocio evalúa y decide. Hoy la "
     "operación salta directamente de la ficha del cliente a la creación del préstamo; estas tareas "
     "organizarán ese paso intermedio.",
     [
         ("T-21", "Registrar una solicitud de préstamo",
          "Cuando el cliente pida dinero y aún no se decida su otorgamiento.", FUT,
          ["Cuando esté disponible: abra la pantalla de Solicitudes, pulse el botón de alta, elija el "
           "cliente, indique el monto solicitado y el plazo, escriba las observaciones y guarde."],
          "La solicitud queda en estado pendiente de decisión, con fecha y responsable."),
         ("T-22", "Evaluar y decidir una solicitud",
          "Cuando el negocio revise el pedido y defina si otorga o no el crédito.", FUT,
          ["Abrá la solicitud, registre su decisión de aprobar o rechazar y escriba el motivo."],
          "La decisión queda firmada con fecha y observaciones, y la solicitud pasa a estado resuelto."),
         ("T-23", "Convertir una solicitud aprobada en préstamo",
          "Inmediatamente después de aprobar un pedido.", FUT,
          ["Desde la solicitud aprobada, use la acción de conversión y confirme los datos del "
           "préstamo."],
          "El préstamo nace con los datos ya cargados, sin volver a digitar nombre, monto ni plazo."),
         ("T-24", "Informar el estado de la solicitud",
          "Cuando el cliente pregunte cómo va su pedido.", FUT,
          ["Consulte el estado de la solicitud y compártalo con el cliente."],
          "El sistema también podrá avisar el cambio de estado al cliente, para que la comunicación no "
          "dependa de una llamada manual."),
     ]),

    ("8. Crear préstamos",
     "Es el momento en que el negocio entrega dinero. El sistema calcula el crédito completo en ese "
     "acto: interés, monto total y calendario de cuotas, con el descuento correspondiente de la caja.",
     [
         ("T-25", "Crear un préstamo",
          "Cuando el cliente acepte las condiciones y se entregue el dinero.", DISP,
          ["Abra la pantalla de Préstamos y pulse el botón de nuevo préstamo.",
           "Elija el cliente (solo aparecen los activos) y el tipo de préstamo.",
           "Indique la fecha, el capital a prestar, el interés mensual y el número de cuotas.",
           "Escriba las observaciones de la operación y guarde."],
          "El sistema calcula el interés total, el monto total y el valor de cada cuota; genera todas "
          "las cuotas en estado pendiente con su fecha de vencimiento; y descuenta el capital prestado "
          "de la caja. Si el capital no alcanza, rechaza la operación explicando cuánto hay disponible "
          "y no guarda nada."),
         ("T-26", "Comprobar el capital disponible antes de prestar",
          "Justo antes de aprobar un préstamo de monto alto.", LIM,
          ["Abra la pantalla de Capital y observe el saldo disponible.",
           "Compárelo con el monto que piensa prestar."],
          "Si el saldo no alcanza, el préstamo será rechazado al guardarlo; en ese caso primero se "
          "registra un aporte de capital. La pantalla de Capital puede no abrirse mientras el equipo "
          "responsable no active su acceso."),
         ("T-27", "Revisar el plan de cuotas generado",
          "Al terminar de crear el préstamo y antes de entregar el dinero.", DISP,
          ["Abra el préstamo recién creado.",
           "Pase a la pestaña de cuotas.",
           "Revise fechas, valores y estados."],
          "Debe ver todas las cuotas pendientes con su fecha de vencimiento y el valor calculado. Si "
          "algo no coincide con lo acordado, corrija el préstamo antes de entregar el dinero."),
         ("T-28", "Listar y filtrar los préstamos",
          "Cuando necesite encontrar una operación o revisar la cartera.", DISP,
          ["Abra la pantalla de Préstamos.",
           "Filtre por estado (activo, pagado, perdido o renovado) o por período.",
           "Pase de página con el control inferior."],
          "La lista muestra cliente, monto, cuotas pagadas frente al total, saldo pendiente y estado "
          "de cada préstamo."),
         ("T-29", "Abrir el detalle de un préstamo",
          "Cuando necesite ver una operación completa.", DISP,
          ["Desde la lista de préstamos, pulse sobre la fila que le interese."],
          "Se abre el préstamo con sus tarjetas de resumen y sus pestañas de cuotas, pagos e "
          "información general."),
     ]),

    ("9. Dar seguimiento a un préstamo",
     "Una vez entregado el dinero, el préstamo pasa por varios momentos: se paga, se renueva o se "
     "declara incobrable. Estas tareas son las decisiones que usted toma sobre cada operación.",
     [
         ("T-30", "Ver el resumen de un préstamo",
          "Al abrir cualquier préstamo.", DISP,
          ["Observe las tarjetas de la parte superior: capital prestado, interés, monto total, valor "
           "de la cuota y saldo pendiente."],
          "Es la vista rápida de la operación. Debajo, las pestañas muestran el detalle de las cuotas, "
          "los pagos recibidos y los datos generales."),
         ("T-31", "Renovar un préstamo",
          "Cuando el cliente no pueda saldar y ambas partes acuerden continuar la operación.", DISP,
          ["Abra el préstamo mientras esté activo.",
           "Pulse la acción de renovar.",
           "Indique el abono al saldo, el interés mensual, el número de cuotas y la fecha.",
           "Escriba las observaciones y guarde."],
          "El abono no puede superar el saldo pendiente. Al confirmar, el abono reduce la deuda, se "
          "abre el préstamo nuevo con las condiciones pactadas y el anterior queda como renovado, sin "
          "admitir más pagos ni acciones."),
         ("T-32", "Declarar un préstamo perdido",
          "Cuando se agotaron los intentos de cobro y se decide asumir la pérdida.", DISP,
          ["Abra el préstamo mientras esté activo.",
           "Pulse la acción de perdido.",
           "Indique la fecha y escriba el motivo.",
           "Confirme."],
          "El saldo pendiente se descuenta de la caja y el préstamo queda como perdido, con su motivo "
          "guardado. No se puede deshacer desde la pantalla; por eso el motivo debe ser claro."),
         ("T-33", "Ajustar el capital de un préstamo",
          "Cuando un cobro o un descuento obliguen a corregir el monto prestado.", LIM,
          ["Abra el préstamo y use la acción de ajuste de capital."],
          "El ajuste recalcula el monto total de la operación. Es una corrección excepcional: si la "
          "discrepancia es habitual, revise primero cómo se están registrando los cobros."),
         ("T-34", "Reestructurar un préstamo",
          "Cuando se acuerde cambiar el plazo sin aplicar un abono.", FUT,
          ["No disponible todavía."],
          "Permitirá renegociar plazo y cuotas manteniendo la misma deuda."),
         ("T-35", "Seguir el estado de un préstamo hasta cerrarlo",
          "Durante toda la vida del préstamo.", DISP,
          ["Revise la etiqueta de estado del préstamo en cada visita.",
           "Interprete el estado: activo significa que sigue cobrándose; pagado, que el saldo llegó a "
           "cero; perdido o renovado, que la operación ya se cerró por una decisión."],
          "Cuando el saldo llega a cero, el sistema cierra solo el préstamo como pagado. Los estados "
          "finales dejan de ofrecer las acciones de pago, renovación y pérdida, para que no se puedan "
          "tocar operaciones ya cerradas."),
     ]),

    ("10. Cobrar",
     "Es la tarea que se repite cada día. Un cobro bien registrado mantiene la caja, las cuotas y los "
     "reportes en acuerdo, y evita discusiones posteriores con el cliente.",
     [
         ("T-36", "Registrar el pago de una cuota",
          "Cada vez que el cliente entregue dinero.", DISP,
          ["Abra el préstamo y pulse la acción de registrar pago.",
           "Elija la cuota a pagar: solo aparecen las que tienen saldo.",
           "Indique el tipo de pago, la fecha y el valor pagado.",
           "Desglose ese valor entre capital, interés y mora.",
           "Escriba las observaciones, como la referencia de la transferencia, y guarde."],
          "El sistema exige que capital, interés y mora sumen exactamente el valor pagado; si hay "
          "diferencia, lo advierte y no guarda nada. Al confirmar, baja el saldo del préstamo, marca "
          "la cuota como pagada o parcial, sube la caja y, si el saldo llega a cero, cierra el "
          "préstamo como pagado. Si por un problema de conexión envía dos veces el mismo cobro, el "
          "segundo intento no lo registra otra vez."),
         ("T-37", "Ver los pagos de un préstamo",
          "Cuando el cliente pregunte qué ha pagado.", DISP,
          ["Abra el préstamo y pase a la pestaña de pagos."],
          "Aparece cada cobro con su fecha, valor y desglose de capital, interés y mora, en orden "
          "cronológico."),
         ("T-38", "Consultar todos los pagos del sistema",
          "Cuando necesite un historial general de cobros, no de un solo préstamo.", LIM,
          ["Por ahora, consulte los pagos abriendo cada préstamo por separado; la vista global todavía "
           "no funciona."],
          "Cuando esté disponible, reunirá todos los cobros con filtros de fecha, cliente y tipo de "
          "pago."),
         ("T-39", "Revertir un pago registrado por error",
          "Cuando un cobro se capturó mal y hay que anularlo.", FUT,
          ["Mientras tanto, solicite la corrección al administrador del sistema y documente el motivo."],
          "La tarea pedirá motivo y rol de administrador, y devolverá el saldo, la cuota y la caja a "
          "como estaban, dejando constancia del ajuste."),
         ("T-40", "Descargar el comprobante de un pago",
          "Cuando el cliente pide prueba de lo pagado.", FUT,
          ["No disponible todavía."],
          "Entregará un comprobante descargable con los datos del cobro."),
     ]),

    ("11. Moras y cobranza",
     "La mora se aplica sola cada madrugada. Estas tareas son las de consulta y las de acción: revisar "
     "cuánto se aplicó, explicarlo al cliente y preparar la jornada de cobro.",
     [
         ("T-41", "Revisar qué mora se aplicó hoy",
          "Cada mañana, antes de empezar a cobrar.", LIM,
          ["Abra la pantalla de Moras y consulte las del día.",
           "Si la pantalla no responde, revise la mora en cada cuota del préstamo correspondiente."],
          "El sistema calcula la mora cada día a medianoche sobre las cuotas vencidas, respetando la "
          "tasa y los días de gracia de la configuración; usted no calcula nada a mano."),
         ("T-42", "Consultar las moras de un préstamo",
          "Cuando el cliente pide explicación de un recargo.", LIM,
          ["Intente la consulta desde la pantalla de Moras; hoy puede devolver un error.",
           "Mientras tanto, revise el detalle de la mora dentro de las cuotas del préstamo."],
          "La consulta mostrará fecha, días aplicados, base, tasa y valor, que es lo necesario para "
          "explicar el cobro al cliente."),
         ("T-43", "Procesar las moras de inmediato",
          "Cuando se detecte un desfase o se corrija una tasa.", LIM,
          ["Abra la pantalla de Moras y ejecute el procesamiento manual.",
           "Lea el total informado por la ejecución."],
          "El cálculo manual hace exactamente lo mismo que el proceso nocturno; sirve para no esperar "
          "a la madrugada siguiente. Reservado al rol de administrador."),
         ("T-44", "Preparar la lista de cobranza del día",
          "Al empezar la jornada de cobro.", LIM,
          ["Abra la pantalla de Cobranza; hoy la lista puede aparecer vacía.",
           "Como respaldo, filtre los préstamos con cuotas vencidas y ordénelos por antigüedad."],
          "La lista reunirá deudas vencidas con antigüedad, saldo y los datos de contacto del cliente, "
          "y permitirá abrir el préstamo desde cada fila."),
         ("T-45", "Recibir avisos de vencimiento",
          "Tres días y un día antes de que venza una cuota.", DISP,
          ["Permita las notificaciones cuando el sistema se lo pida.",
           "Revise los avisos que llegan a su dispositivo."],
          "Los avisos salen solos para los administradores suscritos y mencionan la cuota por vencer. "
          "Si no llegan, verifique que el navegador tenga las notificaciones permitidas."),
         ("T-46", "Consultar el centro de avisos",
          "Cuando quiera revisar avisos anteriores en un solo lugar.", FUT,
          ["No disponible todavía."],
          "Acumulará los avisos de vencimiento, de pagos y de eventos del sistema."),
     ]),

    ("12. La caja",
     "El capital es el dinero con el que el negocio presta. Estas tareas lo mantienen visible y "
     "explicado: cuánto hay y de dónde salió cada movimiento.",
     [
         ("T-47", "Ver el capital disponible",
          "Antes de aprobar un préstamo y al cerrar el día.", LIM,
          ["Abra la pantalla de Capital y observe el saldo."],
          "El saldo nunca queda negativo: el sistema rechaza cualquier operación que lo dejara en "
          "números rojos. La pantalla puede no abrirse mientras el equipo responsable no active su "
          "acceso."),
         ("T-48", "Consultar los movimientos de la caja",
          "Cuando el saldo no coincida con lo esperado o al cerrar el mes.", LIM,
          ["Abra la pantalla de Capital y revise el historial de movimientos."],
          "Cada movimiento indica su tipo (aporte, préstamo, cobro o pérdida), el valor, la fecha y el "
          "préstamo relacionado, lo que permite reconstruir el saldo paso a paso."),
         ("T-49", "Registrar un ingreso o un egreso de caja",
          "Cuando entre o salga dinero que no viene de un préstamo o de un cobro.", FUT,
          ["No disponible todavía."],
          "Permitirá registrar aportes, retiros y gastos con su motivo, siempre sobre el saldo "
          "disponible."),
     ]),

    ("13. Tablero y reportes",
     "Es el cierre de la gestión: mirar los números del negocio y producir los documentos que se "
     "comparten con la contabilidad o con la dirección.",
     [
         ("T-50", "Revisar el tablero al empezar el día",
          "Al iniciar sesión.", DISP,
          ["Observe las tarjetas del tablero: capital actual, préstamos activos, saldo pendiente "
           "total, ganancia del periodo, total prestado y préstamos perdidos."],
          "Es la fotografía del negocio de un vistazo. Cuando no hay datos suficientes, la tarjeta lo "
          "dice con claridad en lugar de mostrar un cero que confunda."),
         ("T-51", "Ver la distribución de la cartera",
          "Cuando quiera saber qué proporción de la cartera está activa, pagada o perdida.", LIM,
          ["Revise la gráfica de distribución del tablero."],
          "La gráfica complementa las tarjetas con la proporción de cada estado en la cartera."),
         ("T-52", "Revisar los indicadores de cobranza y mora",
          "Cuando quiera vigilar el atraso.", LIM,
          ["Revise los indicadores de vencimiento del tablero."],
          "Muestran cuánto hay vencido y cuánto se está cobrando; junto con la lista de cobranza, "
          "definen las prioridades del día."),
         ("T-53", "Generar el reporte de ganancias y pérdidas",
          "Al cerrar un período de gestión.", DISP,
          ["Abra la pantalla de Reportes.",
           "Elija el período.",
           "Genere el reporte."],
          "Muestra los intereses cobrados, la cantidad de préstamos y el resultado del período, con el "
          "detalle por préstamo que permite explicar cada cifra."),
         ("T-54", "Generar el reporte de cartera",
          "Cuando necesite el detalle de saldos por préstamo y su antigüedad.", FUT,
          ["No disponible todavía; el cálculo existe pero falta su pantalla."],
          "Listará cada préstamo con saldo, antigüedad y estado, con la distribución de la cartera."),
         ("T-55", "Generar el reporte de cobranza",
          "Cuando necesite el total cobrado en un período.", FUT,
          ["No disponible todavía; el cálculo existe pero falta su pantalla."],
          "Mostrará lo cobrado con desglose de capital, interés y mora."),
         ("T-56", "Descargar un reporte en Excel o PDF",
          "Después de generar cualquier reporte.", DISP,
          ["Elija el formato de descarga."],
          "El archivo se descarga respetando el período filtrado, sin abrir otra ventana, listo para "
          "enviarlo o archivarlo."),
         ("T-57", "Ver el resumen consolidado del período",
          "Cuando quiera un único número de cierre del período.", FUT,
          ["No disponible todavía."],
          "Unirá la consulta del tablero con los reportes del período elegido."),
     ]),

    ("14. Comunicaciones y trabajo diario",
     "Son las tareas que acompañan la jornada: avisos, instalación en el dispositivo, uso sin "
     "conexión y actualizaciones. No están en el centro de la operación, pero evitan que pequeños "
     "contratiempos interrumpan el trabajo.",
     [
         ("T-58", "Activar las notificaciones en mi dispositivo",
          "Una sola vez, al empezar a usar el sistema.", LIM,
          ["Pulse la opción de activación de notificaciones que aparece en la aplicación.",
           "Permita las notificaciones cuando el navegador se lo pida."],
          "A partir de ahí llegará el aviso de vencimientos suscritos. Si no llega, revise que el "
          "navegador tenga las notificaciones permitidas para el sitio."),
         ("T-59", "Instalar la aplicación en el dispositivo",
          "Cuando quiera abrirla como una ventana propia, sin el navegador.", LIM,
          ["Use el aviso de instalación cuando aparezca o la opción del navegador."],
          "La aplicación se abre en su propia ventana y se muestra en el inicio del dispositivo. Hoy "
          "puede no ofrecerse mientras se completa su empaquetado."),
         ("T-60", "Seguir trabajando cuando se cae internet",
          "Cuando la conexión se interrumpa en plena jornada.", LIM,
          ["El sistema avisa que no hay conexión; siga trabajando y no cierre la ventana.",
           "Al recuperar la conexión, lo registrado se envía solo."],
          "Los datos críticos quedan guardados en el dispositivo mientras tanto. Si el aviso de "
          "conexión persiste, suspenda operaciones sensibles y avise al administrador."),
         ("T-61", "Actualizar la aplicación cuando salga una versión nueva",
          "Cuando el sistema avise que hay una versión mejorada.", LIM,
          ["Espere el aviso de actualización.",
           "Acepte cuando termine de trabajar en lo que esté haciendo."],
          "Así se evita que la pantalla cambie a mitad de una operación; el aviso llega sin recargar "
          "por su cuenta el trabajo en curso."),
         ("T-62", "Usar la calculadora rápida",
          "Cuando necesite resolver un cálculo sin salir de la pantalla que esté viendo.", DISP,
          ["Abra la calculadora desde el menú de apoyo.",
           "Escriba los valores y lea el resultado."],
          "Sirve para comprobar un interés o una cuota frente al cliente, sin perder el lugar en el "
          "que estaba."),
     ]),

    ("15. Tareas de futuras versiones",
     "Estas tareas ya están previstas en los requerimientos del software pero todavía no se pueden "
     "ejecutar. Se listan aquí para que sepan qué vendrá y puedan priorizarlo con el equipo.",
     [
         ("T-63", "Importar un extracto del banco",
          "Para cerrar la caja contra el movimiento bancario.", FUT,
          ["No disponible todavía."],
          "Cargará el extracto y ayudará a conciliarlo con los cobros registrados."),
         ("T-64", "Cobrar en línea desde el sistema",
          "Cuando el cliente prefiera pagar con tarjeta o transferencia guiada.", FUT,
          ["No disponible todavía."],
          "Registraría el pago digital y lo acreditaría a la cuota correspondiente."),
         ("T-65", "Consultar el riesgo crediticio de un cliente",
          "Antes de aprobar un préstamo a un cliente nuevo o con historial largo.", FUT,
          ["No disponible todavía."],
          "Aportará información de comportamiento de pago para sostener la decisión."),
         ("T-66", "Firmar el contrato del préstamo por internet",
          "Al formalizar la operación sin cita presencial.", FUT,
          ["No disponible todavía."],
          "Dejará constancia firmada del acuerdo con fecha y hora."),
         ("T-67", "Recibir los avisos por correo",
          "Para quien no trabaje frente a la pantalla.", FUT,
          ["No disponible todavía."],
          "Enviarán los mismos recordatorios de vencimiento y eventos al correo registrado."),
         ("T-68", "Recibir los avisos por mensaje de texto",
          "Para llegar a quien no usa correo ni notificaciones.", FUT,
          ["No disponible todavía."],
          "Ampliará los canales de aviso con la misma información de vencimientos."),
         ("T-69", "Personalizar los mensajes que envía el sistema",
          "Cuando se quiera cambiar la redacción de los avisos.", FUT,
          ["No disponible todavía."],
          "Permitirá editar las plantillas de mensaje manteniendo los datos que se rellenan solos."),
         ("T-70", "Trabajar varios negocios con la misma cuenta",
          "Cuando un mismo equipo administre más de un negocio.", FUT,
          ["No disponible todavía."],
          "Separará los datos de cada negocio para que uno no se mezcle con el otro."),
     ]),
]


def main():
    d = Doc(
        title="**Guía de Tareas del Usuario**",
        subtitle="Todas las tareas del programa, en el orden en que se trabajan",
        author=["Equipo de Ingeniería de Software · LoanSoft"],
        affiliation=["LoanSoft · Sistema de Gestión de Préstamos"],
        date=["28 de septiembre de 2026"],
        extra=["Versión 1.0",
               "Documento para quienes usan LoanSoft en su operación diaria"],
    )

    d.abstract(
        "Esta guía reúne todas las tareas que realiza quien usa LoanSoft, ordenadas según el flujo "
        "natural del trabajo: primero el acceso y la preparación, después los clientes, la creación "
        "de préstamos, el cobro, la cobranza y el cierre con reportes. Cada tarea explica cuándo se "
        "hace, cómo se hace y qué resultado deja, sin referencias técnicas. El catálogo completo "
        "aparece en el capítulo 3 y las descripciones detalladas en los capítulos siguientes."
    )

    # ---------------------------------------------------------- 1
    d.h1("1. Cómo leer esta guía")
    d.p(
        "La guía está pensada para leerse de dos maneras. Si prefiere una visión general, el capítulo "
        "2 explica el flujo completo del trabajo y el capítulo 3 lista las setenta tareas del "
        "sistema. Si necesita resolver algo concreto, vaya al capítulo que corresponda a lo que está "
        "haciendo: cada tarea tiene su número y su nombre, y todas siguen el mismo orden en toda la "
        "guía."
    )
    d.p(
        "Cada tarea se presenta con cuatro elementos: su cuándo, que indica el momento en que se "
        "realiza; sus pasos, numerados en el orden en que se ejecutan; su resultado, que dice qué "
        "queda registrado después de hacerla; y su estado, según la siguiente escala."
    )
    d.table(
        "Estados que aparecen en las tareas",
        ["Estado", "Qué significa para usted"],
        [
            [DISP, "La tarea se puede realizar hoy desde el menú del sistema."],
            [LIM, "La tarea existe, pero conviene conocer una restricción o una alternativa temporal "
                   "antes de depender de ella."],
            [FUT, "La tarea está prevista y todavía no se puede ejecutar; se explica para que sepan "
                   "qué viene."],
        ],
        widths=[1.6, 5.4],
    )
    d.p(
        "Dos reglas generales conviene tener presentes. La primera: cada persona ve en el menú solo "
        "las pantallas que su rol le permite; si una función no le aparece, no es un error, es que su "
        "cuenta no la incluye, y se solicita al administrador. La segunda: las listas largas se "
        "muestran por páginas, con un control en la parte inferior; si no encuentra un registro, "
        "revise que no haya quedado en otra página o con un filtro activo."
    )

    # ---------------------------------------------------------- 2
    d.h1("2. El flujo completo del trabajo")
    d.p(
        "El sistema acompaña una jornada típica en seis momentos. Cada momento deja listo el dato "
        "que necesita el siguiente: sin clientes registrados no se crea el préstamo; sin préstamo no "
        "hay cuotas que cobrar; sin cobros no hay números que cerrar. Por eso el orden importa y "
        "por eso esta guía sigue la misma secuencia."
    )
    d.figure(os.path.join(FIGS, "fig9_flujo_tareas.png"),
             "Los seis momentos del trabajo con LoanSoft y el orden en que se encadenan.")
    d.table(
        "Los seis momentos, lo que se necesita y lo que queda listo",
        ["Momento", "Lo que se necesita para empezar", "Lo que queda listo al terminar"],
        [
            ["1. Preparar", "Cuentas de usuario, catálogos y capital inicial.",
             "Un sistema ajustado al negocio y con personal autorizado."],
            ["2. Clientes", "Los datos de la persona que pedirá el dinero.",
             "Fichas activas listas para recibir préstamos."],
            ["3. Crear el préstamo", "Cliente activo, capital disponible y condiciones acordadas.",
             "El préstamo con su plan de cuotas y el descuento de la caja."],
            ["4. Cobrar", "El dinero entregado por el cliente y el desglose del cobro.",
             "Cuotas saldadas, saldo actualizado y caja al día."],
            ["5. Dar seguimiento", "La lista de vencimientos y los avisos del sistema.",
             "Moras aplicadas, cobranza organizada y avisos enviados."],
            ["6. Cerrar", "Un período de gestión cerrado.",
             "Tablero revisado y reportes descargados para compartir."],
        ],
        widths=[1.3, 2.8, 2.9],
    )

    # ---------------------------------------------------------- 3
    d.h1("3. Catálogo de todas las tareas")
    d.p(
        "Este catálogo lista las setenta tareas del sistema en el orden en que se trabajan. Sirve "
        "como índice general: identifique la tarea que le interesa y busque su número en el capítulo "
        "correspondiente para ver los pasos detallados."
    )
    rows = []
    for cap_titulo, _intro, tareas in CAPS:
        area = cap_titulo.split(". ", 1)[1]
        for num, nombre, _cuando, estado, _pasos, _res in tareas:
            rows.append([num, nombre, area, estado])
    d.table(
        "Listado completo de tareas del sistema",
        ["N.º", "Tarea", "Área", "Estado"],
        rows,
        widths=[0.7, 3.1, 2.3, 1.4],
        align_center_cols=(0,),
    )
    disp = sum(1 for r in rows if r[3] == DISP)
    lim = sum(1 for r in rows if r[3] == LIM)
    fut = sum(1 for r in rows if r[3] == FUT)
    d.p(
        f"De las {len(rows)} tareas listadas, {disp} están disponibles hoy, {lim} funcionan con "
        f"limitaciones que conviene conocer y {fut} pertenecen a futuras versiones. Los capítulos "
        "siguientes explican cada una con sus pasos."
    )

    # ---------------------------------------------------------- 4..15
    for cap_titulo, intro, tareas in CAPS:
        d.h1(cap_titulo)
        d.p(intro)
        for num, nombre, cuando, estado, pasos, resultado in tareas:
            d.h3(f"{num} · {nombre}")
            d.p(f"**Cuándo se hace.** {cuando}")
            d.p("**Pasos.**")
            for i, paso in enumerate(pasos, start=1):
                d.numbered(i, paso)
            d.p(f"**Resultado.** {resultado}")
            d.p(f"**Estado.** {estado}")

    # ---------------------------------------------------------- 16
    d.h1("16. Tareas según su rol")
    d.p(
        "No todas las personas hacen todas las tareas. La siguiente tabla resume qué conjunto le "
        "corresponde a cada perfil según el día a día del negocio; el sistema se encarga de mostrar "
        "solo lo que le toca a cada cuenta."
    )
    d.table(
        "Tareas habituales por perfil",
        ["Perfil", "Tareas que realiza con más frecuencia"],
        [
            ["Gestor", "T-01 a T-05, registro y búsqueda de clientes, creación de préstamos, "
                       "registro de pagos, consulta de estados y revisión del tablero."],
            ["Administrador", "Todas las tareas, con énfasis en cuentas de usuario, catálogos, "
                              "configuración, auditoría, moras y reportes."],
            ["Responsable de cobranza", "Búsqueda de clientes, consulta de préstamos y pagos, lista "
                                        "de cobranza, moras y avisos de vencimiento."],
            ["Dirección", "Tablero, reportes con exportación, auditoría y revisión de capital."],
        ],
        widths=[1.7, 5.3],
    )
    d.p(
        "Cuando una tarea no le aparezca en su menú, no la busque en otra parte: solicite al "
        "administrador que revise el rol de su cuenta. Cuando una tarea figure como disponible con "
        "limitaciones, lea primero la sección de su capítulo antes de depender de ella en plena "
        "jornada."
    )
    d.save(os.path.join(OUT, "06_Guia_de_Tareas_del_Usuario.docx"))
    print("Guía de tareas generada")


if __name__ == "__main__":
    main()
