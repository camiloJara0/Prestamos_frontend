# -*- coding: utf-8 -*-
"""Genera el Documento de Requerimientos Funcionales a partir de la Guía de Tareas."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from apa import Doc  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
FIGS = os.path.join(HERE, "figs")

HAB = "Habilitada"
PAR = "Parcialmente habilitada"
PRE = "Prevista en el alcance"

# (capítulo, título, objetivo del módulo, [(id, nombre, objetivo, rf[], rn[], consideraciones)])
CAPS = [
    (4, "Acceso y perfil",
     "Este módulo garantiza que solo el personal autorizado utilice el sistema y que cada operación "
     "realizada quede asociada a una persona identificada. Define las capacidades de acceso, "
     "identificación, cierre y custodia de credenciales sobre las que se apoya todo el resto del "
     "alcance funcional.",
     [
         ("RF-4.1", "Autenticación de usuarios",
          "Permitir el acceso al sistema únicamente a cuentas activas y con credenciales válidas.",
          ["El sistema debe permitir el inicio de sesión mediante correo electrónico y contraseña.",
           "El sistema debe validar las credenciales antes de conceder el acceso.",
           "El sistema debe mantener la sesión activa durante la jornada del usuario y renovarla "
           "automáticamente mientras mantenga actividad.",
           "El sistema debe denegar el acceso a cuentas en estado inactivo."],
          ["RN-4.1.1 El mensaje emitido cuando las credenciales no coinciden no debe revelar si la "
           "cuenta existe.",
           "RN-4.1.2 Las cuentas inactivas no podrán iniciar sesión, aun cuando sus credenciales "
           "sean correctas."],
          "Capacidad habilitada actualmente en el producto."),
         ("RF-4.2", "Cierre de sesión",
          "Permitir al usuario terminar su turno dejando su cuenta protegida.",
          ["El sistema debe permitir cerrar la sesión de forma explícita desde el menú de usuario.",
           "El sistema debe retirar del dispositivo la información de la sesión cerrada.",
           "El sistema debe exigir un nuevo inicio de sesión para continuar operando."],
          ["RN-4.2.1 El cierre de sesión debe estar disponible en todo momento, desde cualquier "
           "pantalla del sistema."],
          "Capacidad habilitada actualmente en el producto."),
         ("RF-4.3", "Identificación del usuario activo",
          "Dejar visible en todo momento con qué cuenta se está operando.",
          ["El sistema debe mostrar de forma permanente el nombre de la cuenta activa.",
           "El sistema debe permitir consultar el perfil con nombre, correo y rol asignado.",
           "El sistema debe asociar a la cuenta activa la autoría de cada operación que se registre."],
          ["RN-4.3.1 Si la identidad o el rol mostrado no corresponden a quien opera, debe "
           "suspenderse el uso de la cuenta y solicitarse su corrección."],
          "Capacidad habilitada actualmente en el producto."),
         ("RF-4.4", "Cambio de contraseña",
          "Permitir al usuario renovar su contraseña conservando el control de su cuenta.",
          ["El sistema debe permitir cambiar la contraseña desde el perfil del usuario.",
           "El sistema debe validar la contraseña actual antes de aplicar el cambio.",
           "El sistema debe exigir la confirmación de la contraseña nueva y una longitud mínima de "
           "seis caracteres.",
           "El sistema debe conservar el resto de los datos del perfil sin modificación."],
          ["RN-4.4.1 La contraseña nueva y su confirmación deben coincidir exactamente.",
           "RN-4.4.2 Si la contraseña actual no coincide, no debe modificarse ningún dato."],
          "Capacidad habilitada actualmente en el producto."),
         ("RF-4.5", "Recuperación de contraseña",
          "Permitir restablecer el acceso cuando una contraseña se pierde, sin depender de la "
          "presencia física del administrador.",
          ["El sistema debe permitir solicitar el restablecimiento mediante el correo registrado.",
           "El sistema debe enviar un enlace de recuperación de un solo uso y con vigencia limitada.",
           "El sistema debe registrar la contraseña nueva con las mismas validaciones del cambio "
           "ordinario."],
          [],
          "Capacidad prevista en una versión futura del alcance. Hasta entonces, la reposición de "
          "contraseñas la realiza el administrador desde la administración de usuarios."),
     ]),

    (5, "Cuentas, catálogos y ajustes",
     "Este módulo prepara el sistema antes de que inicie la operación: define quién puede usarlo, con "
     "qué productos de crédito, bajo qué condiciones de cobro y bajo qué parámetros de mora. Sus "
     "capacidades corresponden al rol administrador y sostienen la coherencia de toda la operación "
     "posterior.",
     [
         ("RF-5.1", "Alta de cuentas de usuario",
          "Permitir incorporar personal al sistema con las funciones que le corresponden.",
          ["El sistema debe permitir registrar cuentas con nombre, correo electrónico, contraseña y "
           "rol.",
           "El sistema debe impedir el registro de un correo ya utilizado por otra cuenta.",
           "El sistema debe asociar a cada cuenta su fecha de alta y su estado."],
          ["RN-5.1.1 El rol asignado determina las pantallas y las acciones disponibles para la "
           "cuenta.",
           "RN-5.1.2 La contraseña de alta debe cumplir la misma longitud mínima exigida en el "
           "cambio de contraseña."],
          "Capacidad parcialmente habilitada: su acceso desde el menú está sujeto a la activación "
          "correspondiente; mientras tanto, los altas se coordinan con el responsable del sistema."),
         ("RF-5.2", "Modificación de cuentas de usuario",
          "Mantener actualizada la información de las cuentas conforme cambia el equipo.",
          ["El sistema debe permitir editar nombre, correo y rol de una cuenta existente.",
           "El sistema debe conservar el historial de operaciones registradas por la cuenta "
           "modificada."],
          ["RN-5.2.1 La modificación de una cuenta no debe alterar los registros de autoría "
           "anteriores."],
          "Capacidad parcialmente habilitada, con la misma consideración de acceso que el alta."),
         ("RF-5.3", "Suspensión de cuentas de usuario",
          "Retirar el acceso a personas que dejan de operar, sin perder su historial.",
          ["El sistema debe permitir cambiar el estado de una cuenta a inactivo.",
           "El sistema debe impedir el inicio de sesión de las cuentas inactivas.",
           "El sistema debe permitir reactivar una cuenta cuando corresponda."],
          ["RN-5.3.1 La suspensión no debe eliminar la cuenta ni las operaciones que su titular "
           "registró."],
          "Capacidad parcialmente habilitada, con la misma consideración de acceso que el alta."),
         ("RF-5.4", "Catálogo de tipos de préstamo",
          "Definir los productos de crédito con los que opera el negocio.",
          ["El sistema debe permitir registrar tipos de préstamo con nombre, descripción, interés "
           "mensual, máximo de cuotas y estado.",
           "El sistema debe ofrecer en la originación únicamente los tipos en estado activo.",
           "El sistema debe utilizar los valores del tipo seleccionado para completar las condiciones "
           "del préstamo."],
          ["RN-5.4.1 Un tipo con préstamos asociados debe desactivarse, no eliminarse, para conservar "
           "el sentido de los históricos.",
           "RN-5.4.2 Los tipos inactivos no deben aparecer en los formularios de originación."],
          "Capacidad parcialmente habilitada, con la misma consideración de acceso que el alta."),
         ("RF-5.5", "Catálogo de tipos de pago",
          "Clasificar los medios de cobro que el negocio acepta.",
          ["El sistema debe permitir registrar tipos de pago con nombre, descripción y estado.",
           "El sistema debe ofrecer en el registro de cobros únicamente los tipos activos."],
          ["RN-5.5.1 Los tipos desactivados deben conservarse para la lectura de cobros históricos."],
          "Capacidad parcialmente habilitada, con la misma consideración de acceso que el alta."),
         ("RF-5.6", "Configuración general del sistema",
          "Centralizar los parámetros que regulan la operación, en especial los de mora.",
          ["El sistema debe permitir consultar y modificar la tasa de mora, los días de gracia y los "
           "datos generales del negocio.",
           "El sistema debe aplicar los parámetros vigentes a todos los cálculos posteriores a su "
           "modificación."],
          ["RN-5.6.1 Un cambio de parámetro no debe recalcular los cargos ya aplicados con la "
           "regla anterior.",
           "RN-5.6.2 Toda modificación de parámetro debe quedar identificada con su fecha."],
          "Capacidad parcialmente habilitada: mientras no exista la pantalla de configuración, los "
          "ajustes se tramitan con el responsable del sistema."),
         ("RF-5.7", "Auditoría de operaciones sensibles",
          "Dejar evidencia de quién modificó qué y cuándo, para responder ante cualquier revisión.",
          ["El sistema debe registrar automáticamente cada alta, modificación y baja, con la cuenta "
           "que la ejecutó, la sección afectada, el valor anterior, el valor nuevo y la fecha y hora.",
           "El sistema debe permitir consultar la auditoría filtrando por cuenta, por sección y por "
           "tipo de acción."],
          ["RN-5.7.1 Ninguna operación sobre datos del negocio debe ejecutarse sin dejar registro de "
           "auditoría."],
          "Capacidad parcialmente habilitada: la captura automática opera; la consulta masiva se "
          "solicita al responsable del sistema hasta contar con su pantalla."),
     ]),

    (6, "Clientes",
     "Este módulo administra la cartera de personas atendidas. Sin una ficha de cliente vigente no es "
     "posible originar un préstamo, por lo que sus capacidades constituyen la puerta de entrada de la "
     "operación y la base de la trazabilidad de cobranza.",
     [
         ("RF-6.1", "Registro de clientes",
          "Permitir incorporar a la cartera a una persona con sus datos de contacto y referencia.",
          ["El sistema debe permitir registrar nombre completo, cédula, teléfono, dirección, persona "
           "de referencia, teléfono de referencia, estado y observaciones.",
           "El sistema debe validar que nombre y cédula estén presentes antes de aceptar el registro.",
           "El sistema debe poner la ficha a disposición de la originación una vez registrada."],
          ["RN-6.1.1 La cédula debe ser única en todo el sistema.",
           "RN-6.1.2 Un cliente solo podrá recibir préstamos mientras su estado sea activo.",
           "RN-6.1.3 Ante una cédula duplicada, el sistema debe rechazar el registro y conservar lo "
           "capturado para su corrección."],
          "Capacidad habilitada actualmente en el producto."),
         ("RF-6.2", "Búsqueda de clientes",
          "Localizar rápidamente a una persona al atenderla.",
          ["El sistema debe permitir buscar clientes por nombre, cédula o teléfono.",
           "El sistema debe presentar únicamente los registros coincidentes."],
          [],
          "Capacidad habilitada actualmente en el producto."),
         ("RF-6.3", "Listado y consulta de clientes",
          "Conocer la cartera registrada y su composición.",
          ["El sistema debe presentar el listado de clientes con sus datos principales, ordenado y "
           "paginado.",
           "El sistema debe permitir filtrar el listado y avanzar o retroceder entre páginas.",
           "El sistema debe informar cuando no existan coincidencias."],
          ["RN-6.3.1 El listado debe mostrar bloques paginados; no debe intentar presentar la cartera "
           "completa de una sola vez."],
          "Capacidad habilitada actualmente en el producto."),
         ("RF-6.4", "Detalle del cliente",
          "Reunir la información completa de una persona en una sola vista de consulta.",
          ["El sistema debe permitir consultar la ficha completa de un cliente con sus datos de "
           "contacto y su situación."],
          [],
          "Capacidad prevista en una versión futura del alcance; hasta entonces la información se "
          "consulta desde el listado."),
         ("RF-6.5", "Edición de fichas de cliente",
          "Mantener actualizados los datos de contacto y de referencia.",
          ["El sistema debe permitir modificar los campos de la ficha de un cliente existente.",
           "El sistema debe conservar los préstamos y cobros históricos del cliente sin alteración."],
          ["RN-6.5.1 La edición de la ficha no debe modificar condiciones de operaciones ya "
           "registradas."],
          "Capacidad habilitada actualmente en el producto."),
         ("RF-6.6", "Baja de clientes",
          "Retirar de la operación activa a personas que ya no atiende el negocio.",
          ["El sistema debe permitir cambiar el estado del cliente a inactivo.",
           "El sistema debe impedir que los clientes inactivos sean seleccionados en la originación."],
          ["RN-6.6.1 La baja es lógica: la ficha y su historial permanecen consultables.",
           "RN-6.6.2 Un cliente inactivo puede reactivarse cuando corresponda."],
          "Capacidad habilitada actualmente en el producto."),
         ("RF-6.7", "Historial financiero del cliente",
          "Disponer de la relación completa de préstamos y cobros de una persona para sustentar "
          "decisiones de crédito y de cobranza.",
          ["El sistema debe permitir consultar, por cliente, sus préstamos y sus pagos registrados."],
          [],
          "Capacidad prevista en una versión futura del alcance."),
         ("RF-6.8", "Estadísticas del cliente",
          "Medir el comportamiento de pago de cada persona.",
          ["El sistema debe calcular por cliente indicadores tales como saldo pendiente, "
           "comportamiento de pago y cantidad de préstamos."],
          [],
          "Capacidad prevista en una versión futura del alcance."),
     ]),

    (7, "Solicitudes de préstamo",
     "Este módulo organiza el embudo previo a la entrega de dinero: el cliente solicita, el negocio "
     "evalúa y decide, y la decisión aprobada se convierte en operación. Su propósito es que ningún "
     "préstamo nazca sin una decisión documentada.",
     [
         ("RF-7.1", "Registro de solicitudes",
          "Capturar los pedidos de crédito antes de decidir sobre ellos.",
          ["El sistema debe permitir registrar solicitudes con cliente, monto solicitado, plazo, "
           "observaciones y fecha.",
           "El sistema debe asignar a toda solicitud un estado inicial pendiente de decisión y "
           "responsable."],
          ["RN-7.1.1 Toda solicitud debe quedar asociada a un cliente registrado."],
          "Capacidad prevista en una versión futura del alcance."),
         ("RF-7.2", "Evaluación y decisión de solicitudes",
          "Dejar constancia formal de la decisión de crédito.",
          ["El sistema debe permitir resolver una solicitud con decisión de aprobación o rechazo, "
           "con motivo y fecha.",
           "El sistema debe impedir que una solicitud resuelta vuelva a decidirse."],
          ["RN-7.2.1 Toda decisión debe registrarse con su motivo y su fecha."],
          "Capacidad prevista en una versión futura del alcance."),
         ("RF-7.3", "Conversión de solicitud en préstamo",
          "Formalizar la operación aprobada sin volver a capturar los datos.",
          ["El sistema debe permitir generar un préstamo a partir de una solicitud aprobada, "
           "conservando cliente, monto y plazo."],
          ["RN-7.3.1 La conversión no debe exigir la redigitación de datos ya capturados en la "
           "solicitud."],
          "Capacidad prevista en una versión futura del alcance."),
         ("RF-7.4", "Notificación del estado de la solicitud",
          "Mantener informado al solicitante sobre el avance de su pedido.",
          ["El sistema debe informar los cambios de estado de una solicitud a quien la originó."],
          [],
          "Capacidad prevista en una versión futura del alcance."),
     ]),

    (8, "Originación de préstamos",
     "Este módulo formaliza la entrega de dinero. Su propósito es que cada operación nazca con su "
     "cálculo financiero correcto, su calendario de cuotas completo y su efecto sobre la caja, sin "
     "posibilidad de originar crédito sin respaldo de capital.",
     [
         ("RF-8.1", "Creación de préstamos con cálculo financiero",
          "Originar un préstamo con todas sus condiciones calculadas en el momento de su aprobación.",
          ["El sistema debe permitir registrar préstamos con cliente, tipo de préstamo, fecha, capital "
           "a prestar, interés mensual, número de cuotas y observaciones.",
           "El sistema debe calcular el interés total, el monto total y el valor de cada cuota.",
           "El sistema debe generar el calendario completo de cuotas en estado pendiente, con su "
           "fecha de vencimiento.",
           "El sistema debe descontar el capital prestado del saldo de caja disponible."],
          ["RN-8.1.1 Solo podrán seleccionarse clientes en estado activo.",
           "RN-8.1.2 Cliente, tipo, fecha, capital, interés y número de cuotas son datos obligatorios.",
           "RN-8.1.3 Las condiciones del préstamo deben provenir del tipo de préstamo seleccionado y "
           "respetar sus límites.",
           "RN-8.1.4 Toda cuota nace en estado pendiente."],
          "Capacidad habilitada actualmente en el producto."),
         ("RF-8.2", "Validación de capital disponible",
          "Impedir que se otorgue crédito sin respaldo en caja.",
          ["El sistema debe verificar el capital disponible antes de crear el préstamo.",
           "El sistema debe informar el saldo disponible y el monto solicitado cuando la operación no "
           "proceda."],
          ["RN-8.2.1 Si el capital no alcanza, el préstamo no debe crearse ni debe modificarse ningún "
           "dato.",
           "RN-8.2.2 La caja nunca debe quedar con saldo negativo."],
          "Capacidad habilitada actualmente en el producto."),
         ("RF-8.3", "Consulta del plan de cuotas",
          "Permitir revisar el calendario generado antes de entregar el dinero.",
          ["El sistema debe presentar las cuotas de un préstamo con número, fecha de vencimiento, "
           "valor e estado."],
          ["RN-8.3.1 El plan consultado debe coincidir con las condiciones aprobadas en la "
           "originación."],
          "Capacidad habilitada actualmente en el producto."),
         ("RF-8.4", "Listado y consulta de préstamos",
          "Disponer de la cartera completa con sus estados y saldos.",
          ["El sistema debe presentar el listado de préstamos con cliente, monto, cuotas pagadas "
           "frente al total, saldo pendiente y estado.",
           "El sistema debe permitir filtrar por estado y por período, y paginar el resultado."],
          ["RN-8.4.1 Los estados disponibles para filtrar son activo, pagado, perdido y renovado."],
          "Capacidad habilitada actualmente en el producto."),
         ("RF-8.5", "Detalle del préstamo",
          "Reunir en una sola vista la situación completa de una operación.",
          ["El sistema debe permitir consultar un préstamo con sus tarjetas de resumen: capital "
           "prestado, interés, monto total, valor de la cuota y saldo pendiente.",
           "El sistema debe organizar el detalle en secciones de cuotas, pagos e información general."],
          [],
          "Capacidad habilitada actualmente en el producto."),
     ]),

    (9, "Seguimiento del préstamo",
     "Este módulo administra la vida de la operación después de la entrega de dinero. Su propósito es "
     "que cada préstamo evolucione bajo reglas claras de estado: se cobra, se renueva, se ajusta o se "
     "declara perdido, y siempre con el efecto correcto sobre la caja.",
     [
         ("RF-9.1", "Consulta del resumen del préstamo",
          "Permitir evaluar la situación de una operación de un vistazo.",
          ["El sistema debe presentar capital prestado, interés, monto total, valor de la cuota y "
           "saldo pendiente de cada préstamo.",
           "El sistema debe mostrar el estado vigente de la operación."],
          [],
          "Capacidad habilitada actualmente en el producto."),
         ("RF-9.2", "Renovación de préstamos",
          "Permitir continuar la relación con el cliente aplicando un abono y abriendo una nueva "
          "operación.",
          ["El sistema debe permitir registrar una renovación indicando abono al saldo, interés "
           "mensual, número de cuotas, fecha y observaciones.",
           "El sistema debe abrir el préstamo nuevo vinculado con el anterior.",
           "El sistema debe aplicar el abono sobre el saldo pendiente del préstamo original."],
          ["RN-9.2.1 La renovación solo procede desde estados no terminales (activo).",
           "RN-9.2.2 El abono no puede superar el saldo pendiente.",
           "RN-9.2.3 El préstamo original queda en estado renovado y deja de admitir pagos ni nuevas "
           "acciones."],
          "Capacidad habilitada actualmente en el producto."),
         ("RF-9.3", "Declaración de pérdida",
          "Permitir asumir formalmente la incobrabilidad de una operación.",
          ["El sistema debe permitir declarar un préstamo perdido indicando fecha y motivo.",
           "El sistema debe descontar el saldo pendiente del capital de caja al confirmar la "
           "declaración."],
          ["RN-9.3.1 La declaración solo procede desde estados no terminales (activo).",
           "RN-9.3.2 Fecha y motivo son obligatorios.",
           "RN-9.3.3 El préstamo queda en estado perdido, con su motivo conservado, y deja de admitir "
           "acciones.",
           "RN-9.3.4 La declaración no puede deshacerse desde la interfaz de operación."],
          "Capacidad habilitada actualmente en el producto."),
         ("RF-9.4", "Ajuste del capital del préstamo",
          "Corregir el monto prestado cuando un cobro o una devolución lo exijan.",
          ["El sistema debe permitir ajustar el capital de un préstamo y recalcular su monto total."],
          ["RN-9.4.1 El ajuste es una corrección excepcional y debe quedar registrado en la "
           "auditoría del sistema."],
          "Capacidad parcialmente habilitada: requiere validación previa del responsable de la "
          "operación."),
         ("RF-9.5", "Reestructuración de préstamos",
          "Renegociar plazo y cuotas manteniendo la misma deuda.",
          ["El sistema debe permitir reestructurar un préstamo con un nuevo plan de cuotas sin "
           "aplicar abono."],
          ["RN-9.5.1 La reestructuración solo procede desde estados no terminales."],
          "Capacidad prevista en una versión futura del alcance."),
         ("RF-9.6", "Control de estados del préstamo",
          "Asegurar que cada operación recorra su ciclo completo y que los estados finales queden "
          "protegidos.",
          ["El sistema debe mantener el estado de cada préstamo: activo, pagado, perdido o renovado.",
           "El sistema debe cerrar automáticamente el préstamo como pagado cuando su saldo llegue a "
           "cero.",
           "El sistema debe impedir pagos, renovaciones y declaraciones sobre préstamos en estado "
           "final."],
          ["RN-9.6.1 Los estados pagado, perdido y renovado son estados terminales: no admiten "
           "acciones posteriores.",
           "RN-9.6.2 El cierre por saldo cero debe ocurrir sin intervención del usuario."],
          "Capacidad habilitada actualmente en el producto."),
     ]),

    (10, "Registro de cobros",
     "Este módulo registra el dinero que entra. Su propósito es que cada cobro quede clasificado desde "
     "su origen, cuadre exactamente con lo recibido, actualice la deuda y la caja, y no pueda "
     "duplicarse aunque el envío se repita.",
     [
         ("RF-10.1", "Registro de pagos",
          "Capturar el cobro de una cuota con su desglose financiero.",
          ["El sistema debe permitir registrar pagos indicando préstamo, cuota, tipo de pago, fecha, "
           "valor pagado y su desglose entre capital, interés y mora, más observaciones.",
           "El sistema debe validar que la suma de capital, interés y mora coincida con el valor "
           "pagado.",
           "El sistema debe actualizar el saldo del préstamo y el estado de la cuota atendida.",
           "El sistema debe incrementar la caja en el capital efectivamente cobrado.",
           "El sistema debe cerrar el préstamo como pagado cuando el saldo llegue a cero."],
          ["RN-10.1.1 Solo deben ofrecerse en el cobro las cuotas con saldo pendiente.",
           "RN-10.1.2 La diferencia entre el desglose y el valor pagado no puede exceder un centavo.",
           "RN-10.1.3 Un envío repetido del mismo cobro no debe generar un segundo registro.",
           "RN-10.1.4 Si el desglose no cuadra, no debe persistirse ningún dato."],
          "Capacidad habilitada actualmente en el producto."),
         ("RF-10.2", "Historial de pagos por préstamo",
          "Responder con exactitud a lo que un cliente ha pagado.",
          ["El sistema debe presentar los pagos de un préstamo con fecha, valor y desglose de capital, "
           "interés y mora, en orden cronológico."],
          [],
          "Capacidad habilitada actualmente en el producto."),
         ("RF-10.3", "Historial global de pagos",
          "Consultar todos los cobros del sistema sin abrir cada operación.",
          ["El sistema debe permitir consultar el conjunto de pagos registrados, filtrado por fecha, "
           "cliente y tipo de pago, con paginación."],
          ["RN-10.3.1 La consulta global debe respetar los mismos criterios de página empleados en el "
           "resto de los listados."],
          "Capacidad parcialmente habilitada: la vista global aún no responde; mientras tanto, la "
          "información se consulta operación por operación."),
         ("RF-10.4", "Reversión de pagos",
          "Corregir cobros capturados por error dejando constancia del ajuste.",
          ["El sistema debe permitir anular un pago mediante una operación inversa que restaure saldo, "
           "cuota y caja.",
           "El sistema debe exigir motivo y rol de administrador para reversar.",
           "El sistema debe registrar la reversión en la auditoría."],
          ["RN-10.4.1 Toda reversión debe ser trazable: quién la hizo, cuándo y por qué."],
          "Capacidad prevista en una versión futura del alcance."),
         ("RF-10.5", "Comprobante de pago",
          "Entregar al cliente una constancia descargable de lo pagado.",
          ["El sistema debe generar un comprobante con los datos de un cobro registrado, en formato "
           "descargable."],
          [],
          "Capacidad prevista en una versión futura del alcance."),
     ]),

    (11, "Mora y cobranza",
     "Este módulo gestiona el atraso. Su propósito es que la mora se aplique de forma automática y "
     "explicable, y que la jornada de cobro se organice sobre información confiable de vencimientos y "
     "contactos.",
     [
         ("RF-11.1", "Cálculo automático de moras",
          "Aplicar diariamente la penalización por atraso sin intervención manual.",
          ["El sistema debe calcular las moras una vez al día, sobre las cuotas vencidas.",
           "El sistema debe aplicar la tasa de mora y los días de gracia vigentes en la "
           "configuración.",
           "El sistema debe informar el resultado del cálculo del día."],
          ["RN-11.1.1 Solo deben gravarse cuotas vencidas más allá de los días de gracia.",
           "RN-11.1.2 La mora de un mismo día no debe aplicarse dos veces."],
          "Capacidad habilitada actualmente en el producto."),
         ("RF-11.2", "Consulta de moras por préstamo",
          "Explicar al cliente el origen exacto de un recargo.",
          ["El sistema debe permitir consultar las moras de un préstamo con fecha, días aplicados, "
           "base, tasa y valor."],
          [],
          "Capacidad parcialmente habilitada: la consulta masiva puede no responder; hasta su "
          "corrección, el detalle se obtiene en las cuotas del préstamo."),
         ("RF-11.3", "Procesamiento manual de moras",
          "Ejecutar el cálculo bajo demanda para corregir desfases detectados.",
          ["El sistema debe permitir ejecutar el cálculo de moras de forma inmediata.",
           "El sistema debe informar el total generado por la ejecución."],
          ["RN-11.3.1 El cálculo manual debe producir el mismo resultado que el proceso nocturno.",
           "RN-11.3.2 La ejecución manual está reservada al rol administrador."],
          "Capacidad parcialmente habilitada, sujeta al acceso de la pantalla de moras."),
         ("RF-11.4", "Gestión de la cartera de cobranza",
          "Organizar la jornada de cobro sobre las deudas vencidas.",
          ["El sistema debe presentar las deudas vencidas con antigüedad, saldo pendiente y datos de "
           "contacto del cliente.",
           "El sistema debe permitir abrir el préstamo correspondiente desde cada vencimiento."],
          ["RN-11.4.1 La lista debe ordenarse por antigüedad de atraso."],
          "Capacidad parcialmente habilitada: la lista puede no poblarse; mientras tanto, los "
          "vencimientos se identifican filtrando los préstamos con cuotas vencidas."),
         ("RF-11.5", "Recordatorios de vencimiento",
          "Anticipar el cobro avisando con anticipación al personal responsable.",
          ["El sistema debe enviar avisos tres días y un día antes del vencimiento de una cuota.",
           "El sistema debe remitir los avisos a los administradores suscritos.",
           "El sistema debe conservar la suscripción y permitir retirarla."],
          ["RN-11.5.1 El fallo en un aviso no debe impedir el envío de los demás.",
           "RN-11.5.2 Los avisos solo se emiten a cuentas suscritas y con notificaciones permitidas."],
          "Capacidad habilitada actualmente en el producto, sujeta a la suscripción del usuario."),
         ("RF-11.6", "Centro de avisos",
          "Reunir en un solo lugar los avisos emitidos por el sistema.",
          ["El sistema debe permitir consultar el historial de avisos de vencimiento y eventos del "
           "sistema."],
          [],
          "Capacidad prevista en una versión futura del alcance."),
     ]),

    (12, "Caja y capital",
     "Este módulo mantiene visible el dinero con que el negocio presta. Su propósito es que el saldo "
     "esté siempre actualizado, que cada movimiento tenga explicación y que la caja nunca se comprometa "
     "en números rojos.",
     [
         ("RF-12.1", "Consulta del capital disponible",
          "Informar en todo momento cuánto dinero hay disponible para prestar.",
          ["El sistema debe presentar el capital disponible actualizado.",
           "El sistema debe verificar la disponibilidad de capital en cada operación que lo afecte."],
          ["RN-12.1.1 El capital disponible nunca debe resultar negativo."],
          "Capacidad parcialmente habilitada, sujeta al acceso de la pantalla de capital."),
         ("RF-12.2", "Libro de movimientos de capital",
          "Explicar cómo se llegó al saldo actual, movimiento por movimiento.",
          ["El sistema debe registrar cada movimiento de capital con tipo, valor, fecha y referencia "
           "al préstamo relacionado.",
           "El sistema debe permitir consultar el historial de movimientos."],
          ["RN-12.2.1 Los tipos de movimiento distinguen aportes, préstamos otorgados, cobros de "
           "capital y pérdidas.",
           "RN-12.2.2 Con el historial debe poder reconstruirse el saldo en cualquier fecha."],
          "Capacidad parcialmente habilitada, sujeta al acceso de la pantalla de capital."),
         ("RF-12.3", "Ingresos y egresos manuales de caja",
          "Registrar movimientos de dinero que no derivan de un préstamo o de un cobro.",
          ["El sistema debe permitir registrar aportes, retiros y gastos con su motivo y fecha."],
          ["RN-12.3.1 Ningún movimiento manual puede dejar el saldo en negativo."],
          "Capacidad prevista en una versión futura del alcance."),
     ]),

    (13, "Tablero y reportes",
     "Este módulo cierra la gestión con números. Su propósito es que la dirección cuente con "
     "indicadores confiables del negocio y con documentos exportables para la contabilidad y el "
     "seguimiento del período.",
     [
         ("RF-13.1", "Indicadores principales del tablero",
          "Mostrar la salud del negocio de un vistazo al iniciar la jornada.",
          ["El sistema debe calcular y presentar capital actual, préstamos activos, saldo pendiente "
           "total, ganancia del periodo, total prestado y préstamos perdidos.",
           "El sistema debe actualizar los indicadores en cada consulta del tablero.",
           "El sistema debe indicar expresamente la ausencia de datos cuando un indicador no tenga "
           "base para calcularse."],
          ["RN-13.1.1 No debe presentarse un valor de cero como si fuera un resultado real cuando no "
           "existan datos."],
          "Capacidad habilitada actualmente en el producto."),
         ("RF-13.2", "Distribución de la cartera",
          "Mostrar la proporción de la cartera en cada estado.",
          ["El sistema debe presentar la distribución de los préstamos por estado como complemento de "
           "los indicadores."],
          [],
          "Capacidad parcialmente habilitada."),
         ("RF-13.3", "Indicadores de cobranza y mora",
          "Vigilar el atraso y lo que se está cobrando.",
          ["El sistema debe presentar los indicadores de vencimiento y de cobranza del período."],
          [],
          "Capacidad parcialmente habilitada."),
         ("RF-13.4", "Reporte de ganancias y pérdidas",
          "Cuantificar el resultado del negocio en un período.",
          ["El sistema debe generar un reporte con los intereses cobrados, la cantidad de préstamos y "
           "el resultado neto del período seleccionado.",
           "El sistema debe incluir el detalle por préstamo que sustenta cada cifra."],
          ["RN-13.4.1 El reporte debe reflejar exclusivamente el período seleccionado."],
          "Capacidad habilitada actualmente en el producto."),
         ("RF-13.5", "Reporte de cartera",
          "Conocer los saldos por préstamo, su antigüedad y su distribución.",
          ["El sistema debe generar un reporte de cartera con saldos, antigüedad y estado de cada "
           "préstamo."],
          [],
          "Capacidad prevista en una versión futura del alcance: el cálculo existe y falta habilitar "
          "su consulta."),
         ("RF-13.6", "Reporte de cobranza",
          "Cuantificar lo cobrado en un período y su composición.",
          ["El sistema debe generar un reporte con el total cobrado y su desglose de capital, interés "
           "y mora."],
          [],
          "Capacidad prevista en una versión futura del alcance, con la misma consideración que el "
          "reporte de cartera."),
         ("RF-13.7", "Exportación de reportes",
          "Permitir compartir y archivar los reportes en formatos habituales de gestión.",
          ["El sistema debe permitir descargar los reportes en Excel y en PDF.",
           "El sistema debe respetar en la descarga los mismos filtros aplicados en la consulta."],
          ["RN-13.7.1 La descarga no debe requerir abrir una ventana adicional ni alterar los "
           "filtros vigentes."],
          "Capacidad habilitada actualmente en el producto."),
         ("RF-13.8", "Resumen consolidado del período",
          "Ofrecer un único cierre del período que integre tablero y reportes.",
          ["El sistema debe presentar un resumen consolidado de los indicadores y resultados del "
           "período seleccionado."],
          [],
          "Capacidad prevista en una versión futura del alcance."),
     ]),

    (14, "Comunicaciones y continuidad operativa",
     "Este módulo sostiene la jornada de trabajo: avisos al dispositivo, uso de la aplicación como "
     "herramienta propia, continuidad ante fallas de conexión y actualización sin interrupciones. Su "
     "propósito es que los contratiempos menores no interrumpan la operación.",
     [
         ("RF-14.1", "Notificaciones al dispositivo",
          "Acercar los avisos importantes sin depender de que el usuario abra el sistema.",
          ["El sistema debe permitir suscribir las notificaciones y retirar la suscripción.",
           "El sistema debe remitir a la suscripción vigente los avisos de vencimiento del personal "
           "suscripto."],
          ["RN-14.1.1 La activación requiere la autorización del navegador por parte del usuario."],
          "Capacidad parcialmente habilitada: la suscripción opera, pero su configuración final "
          "está pendiente."),
         ("RF-14.2", "Instalación de la aplicación",
          "Permitir usar LoanSoft como una aplicación independiente en el dispositivo.",
          ["El sistema debe ofrecer la instalación de la aplicación en computadora y en dispositivo "
           "móvil.",
           "El sistema debe abrirse tras la instalación en su propia ventana, sin barras del "
           "navegador."],
          [],
          "Capacidad parcialmente habilitada: su distribución requiere completar el empaquetado de "
          "la aplicación."),
         ("RF-14.3", "Operación con conexión intermitente",
          "Mantener la continuidad del trabajo cuando la red falla.",
          ["El sistema debe avisar expresamente la pérdida de conexión.",
           "El sistema debe conservar localmente las operaciones críticas registradas sin conexión y "
           "enviarlas al recuperarla.",
           "El sistema debe evitar el cierre abrupto de la ventana durante la caída."],
          ["RN-14.3.1 No deben darse por definitivas las operaciones sensibles mientras persista la "
           "interrupción.",
           "RN-14.3.2 Al recuperar la conexión, las operaciones en espera deben enviarse sin duplicar "
           "registros."],
          "Capacidad parcialmente habilitada: la operación local existe y su alcance sigue en "
          "ampliación."),
         ("RF-14.4", "Actualización de la versión",
          "Renovar el sistema sin interrumpir el trabajo en curso.",
          ["El sistema debe avisar la disponibilidad de una versión nueva.",
           "El sistema debe aplicar la actualización solo cuando el usuario lo acepte."],
          ["RN-14.4.1 No debe recargarse la aplicación de forma silenciosa mientras el usuario tenga "
           "una operación en curso."],
          "Capacidad parcialmente habilitada: el aviso existe y requiere su ajuste final."),
         ("RF-14.5", "Calculadora auxiliar",
          "Resolver cálculos rápidos frente al cliente sin perder el contexto de trabajo.",
          ["El sistema debe permitir realizar operaciones aritméticas auxiliares sin abandonar la "
           "pantalla en que se está trabajando."],
          [],
          "Capacidad habilitada actualmente en el producto."),
     ]),

    (15, "Alcance de futuras versiones",
     "Las capacidades de este capítulo ya están previstas en los requerimientos del software pero no "
     "forman parte de la operación actual. Se listan para que Product Owners y patrocinadores puedan "
     "priorizarlas durante la planificación.",
     [
         ("RF-15.1", "Importación de extractos bancarios",
          "Conciliar la caja con el movimiento bancario.",
          ["El sistema debe permitir cargar un extracto bancario y contrastarlo con los cobros "
           "registrados."],
          [], "Capacidad prevista en el alcance, sin habilitar."),
         ("RF-15.2", "Cobro en línea",
          "Aceptar pagos digitales sin intermediación manual.",
          ["El sistema debe permitir cobrar mediante tarjeta o transferencia guiada y acreditar el "
           "pago a la cuota correspondiente."],
          [], "Capacidad prevista en el alcance, sin habilitar."),
         ("RF-15.3", "Evaluación de riesgo crediticio",
          "Apoyar la decisión de crédito con información de comportamiento.",
          ["El sistema debe permitir consultar el comportamiento de pago del cliente para sustentar la "
           "decisión de otorgamiento."],
          [], "Capacidad prevista en el alcance, sin habilitar."),
         ("RF-15.4", "Firma electrónica de contratos",
          "Formalizar la operación sin cita presencial.",
          ["El sistema debe permitir la firma electrónica del acuerdo de préstamo con fecha y hora."],
          [], "Capacidad prevista en el alcance, sin habilitar."),
         ("RF-15.5", "Avisos por correo electrónico",
          "Llegar a quien no trabaje frente a la pantalla.",
          ["El sistema debe remitir por correo los recordatorios de vencimiento y los eventos del "
           "sistema."],
          [], "Capacidad prevista en el alcance, sin habilitar."),
         ("RF-15.6", "Avisos por mensaje de texto",
          "Ampliar la cobertura de los avisos a otros canales.",
          ["El sistema debe remitir los avisos de vencimiento mediante mensaje de texto."],
          [], "Capacidad prevista en el alcance, sin habilitar."),
         ("RF-15.7", "Plantillas de mensajes",
          "Estandarizar la redacción de las comunicaciones salientes.",
          ["El sistema debe permitir editar las plantillas de los mensajes, conservando los datos que "
           "se completan automáticamente."],
          [], "Capacidad prevista en el alcance, sin habilitar."),
         ("RF-15.8", "Operación multiempresa",
          "Administrar más de un negocio sobre la misma plataforma sin mezclar sus datos.",
          ["El sistema debe aislar los datos de cada negocio atendido por la misma cuenta."],
          [], "Capacidad prevista en el alcance, sin habilitar."),
     ]),
]

PERFILES = [
    ("Gestor", "Autenticación y perfil, registro y búsqueda de clientes, originación de préstamos, "
               "seguimiento de operaciones, registro de cobros, consulta de moras y revisión del "
               "tablero (RF-4.1 a RF-4.4, RF-6.1 a RF-6.6, RF-8.1 a RF-8.5, RF-9.1 a RF-9.4, "
               "RF-10.1 a RF-10.3, RF-11.1, RF-11.5, RF-13.1)."),
    ("Administrador", "Todas las capacidades del alcance, con énfasis en cuentas de usuario, "
                      "catálogos, configuración, auditoría, procesamiento de moras, reversión de "
                      "cobros y reportes (RF-5.1 a RF-5.7, RF-9.3, RF-11.3, RF-12.1 a RF-12.3, "
                      "RF-13.4 a RF-13.7)."),
    ("Responsable de cobranza", "Búsqueda de clientes, consulta de préstamos y cobros, cartera de "
                                "vencimientos, moras y recordatorios (RF-6.2, RF-6.3, RF-8.4, "
                                "RF-10.2, RF-11.1 a RF-11.5)."),
    ("Dirección", "Tablero, reportes con exportación, auditoría y control de capital (RF-13.1 a "
                   "RF-13.8, RF-5.7, RF-12.1, RF-12.2)."),
]


def main():
    d = Doc(
        title="**Documento de Requerimientos Funcionales**",
        subtitle="Alcance funcional del sistema de gestión de préstamos LoanSoft",
        author=["Analítica Funcional · Product Ownership · LoanSoft"],
        affiliation=["LoanSoft · Sistema de Gestión de Préstamos"],
        date=["28 de septiembre de 2026"],
        extra=["Versión 1.0",
               "Documento de análisis, planificación y aprobación de alcance"],
    )

    d.abstract(
        "Este documento define el alcance funcional del sistema LoanSoft para su validación y "
        "aprobación durante las fases de análisis, planificación y desarrollo. Parte del flujo de "
        "procesos del negocio y de las tareas que el sistema debe cubrir, y las traduce en "
        "requerimientos funcionales numerados, reglas de negocio y consideraciones operativas, "
        "dirigidos a Product Owners, patrocinadores, prestamistas y especialistas en contabilidad y "
        "gestión financiera. No constituye un manual de operación ni describe su implementación."
    )

    # ------------------------------------------------------------- 1
    d.h1("1. Introducción")
    d.p(
        "El presente documento tiene como propósito definir, validar y aprobar el alcance funcional "
        "del sistema de gestión de préstamos LoanSoft. Está dirigido a quienes deciden y priorizan el "
        "producto: Product Owners, patrocinadores del proyecto, usuarios prestamistas y personas con "
        "conocimiento en contabilidad y gestión financiera. Su lectura permite conocer qué debe hacer "
        "el sistema, bajo qué reglas de negocio y con qué estado de habilitación, antes de comprometer "
        "esfuerzo en desarrollo."
    )
    d.p(
        "La estructura del documento conserva el flujo de procesos del negocio: comienza por el acceso "
        "y la preparación del sistema, continúa con la gestión de clientes y la originación de "
        "préstamos, avanza por el seguimiento, el cobro y la mora, y cierra con la caja, el tablero y "
        "los reportes. El capítulo 3 lista el conjunto completo de capacidades y los capítulos "
        "siguientes las expresan como requerimientos funcionales numerados, cada uno con su objetivo, "
        "sus reglas de negocio y sus consideraciones operativas."
    )
    d.p(
        "Cada capacidad se identifica con un código RF-capítulo.número que conserva el orden original "
        "del flujo, de modo que sea posible rastrear cualquier requerimiento desde su módulo. Las "
        "capacidades se redactan en forma de obligación para el sistema: qué debe permitir, registrar, "
        "calcular, validar, controlar o generar. La formulación sobre el usuario ha sido sustituida por "
        "la capacidad que el sistema debe ofrecer."
    )
    d.table(
        "Estados de habilitación de las capacidades",
        ["Estado", "Significado para la validación de alcance"],
        [
            [HAB, "La capacidad forma parte del producto actual y puede validarse hoy."],
            [PAR, "La capacidad existe o está parcialmente construida, y su uso está sujeto a una "
                   "condición que debe resolverse antes de depender de ella."],
            [PRE, "La capacidad está incluida en el alcance del proyecto y se habilitará en una "
                   "versión futura."],
        ],
        widths=[1.7, 5.3],
    )
    d.p(
        "Dos consideraciones generales enmarcan todos los módulos. Primera: el acceso a cada "
        "capacidad está determinado por el rol de la cuenta, de modo que el sistema debe mostrar y "
        "habilitar únicamente las funciones correspondientes. Segunda: el sistema debe presentar los "
        "listados de forma paginada y filtrable, por lo que la ausencia de un registro en pantalla no "
        "implica su inexistencia sin antes revisar los filtros y el control de páginas."
    )

    # ------------------------------------------------------------- 2
    d.h1("2. Flujo de procesos del sistema")
    d.p(
        "El sistema acompaña la operación del negocio en seis momentos encadenados, y cada momento "
        "entrega el insumo que necesita el siguiente: sin clientes registrados no se originan "
        "préstamos; sin préstamos no hay cuotas que cobrar; sin cobros no hay resultados que cerrar. "
        "El flujo presentado a continuación es la columna vertebral sobre la que se organiza el "
        "restante alcance funcional."
    )
    d.figure(os.path.join(FIGS, "fig9_flujo_tareas.png"),
             "Flujo general de procesos de LoanSoft y orden de encadenamiento de los seis momentos.")
    d.table(
        "Momentos del proceso, entradas y salidas",
        ["Momento", "Entradas requeridas", "Salida que entrega al momento siguiente"],
        [
            ["1. Preparación", "Cuentas de usuarios, catálogos de crédito y medios de pago, capital "
                               "inicial.",
             "Sistema parametrizado y personal autorizado para operar."],
            ["2. Clientes", "Datos de identificación y contacto de la persona atendida.",
             "Fichas activas habilitadas para originar préstamos."],
            ["3. Originación", "Cliente activo, capital disponible y condiciones pactadas.",
             "Préstamo con su plan de cuotas y el efecto registrado sobre la caja."],
            ["4. Cobro", "Dinero recibido y su desglose entre capital, interés y mora.",
             "Cuotas atendidas, saldo actualizado y caja incrementada."],
            ["5. Seguimiento y cobranza", "Cartera de vencimientos, parámetros de mora y avisos del "
                                          "sistema.",
             "Moras aplicadas, cartera de cobro ordenada y recordatorios emitidos."],
            ["6. Cierre", "Período de gestión cerrado.",
             "Tablero revisado y reportes exportables para contabilidad y dirección."],
        ],
        widths=[1.5, 2.7, 2.8],
    )

    # ------------------------------------------------------------- 3
    d.h1("3. Catálogo de capacidades funcionales")
    d.p(
        "El catálogo siguiente enumera las setenta capacidades del sistema en el orden del flujo de "
        "procesos. Funciona como índice general del documento: identificada una capacidad, su código "
        "remite al capítulo donde se detallan sus requerimientos funcionales."
    )
    rows = []
    for cap_num, cap_titulo, _objetivo, items in CAPS:
        for cid, nombre, _obj, _rf, _rn, estado in items:
            rows.append([cid, nombre, f"{cap_num}. {cap_titulo}", estado])
    d.table(
        "Listado completo de capacidades funcionales",
        ["Código", "Capacidad", "Módulo", "Estado"],
        rows,
        widths=[0.8, 2.9, 2.1, 1.6],
        align_center_cols=(0,),
    )
    hab = sum(1 for r in rows if r[3] == HAB)
    par = sum(1 for r in rows if r[3] == PAR)
    pre = sum(1 for r in rows if r[3] == PRE)
    d.p(
        f"De las {len(rows)} capacidades listadas, {hab} están habilitadas y validables hoy, {par} "
        f"parcialmente habilitadas y {pre} previstas en el alcance sin habilitar. Los capítulos "
        "siguientes desarrollan cada una de ellas."
    )

    # ------------------------------------------------------------- 4..15
    for cap_num, cap_titulo, objetivo, items in CAPS:
        d.h1(f"{cap_num}. {cap_titulo}")
        d.p(f"**Objetivo del módulo.** {objetivo}")
        for i, (cid, nombre, obj, rf, rn, estado) in enumerate(items, start=1):
            d.h3(f"{cid} · {nombre}")
            d.p(f"**Objetivo funcional.** {obj}")
            d.p("**Requerimientos funcionales.**")
            for n, item in enumerate(rf, start=1):
                d.numbered(n, item)
            if rn:
                d.p("**Reglas de negocio.**")
                for r in rn:
                    d.bullet(r)
            d.p(f"**Consideraciones operativas.** {estado}")

    # ------------------------------------------------------------- 16
    d.h1("16. Perfiles de usuario y asignación de capacidades")
    d.p(
        "No todos los perfiles utilizan la totalidad de las capacidades. La siguiente asignación "
        "resume el conjunto habitual de cada perfil según el negocio; el sistema debe restringir la "
        "visualización y el uso de las capacidades conforme al rol de la cuenta autenticada."
    )
    d.table(
        "Asignación de capacidades por perfil",
        ["Perfil", "Capacidades que utiliza con mayor frecuencia"],
        [list(p) for p in PERFILES],
        widths=[1.7, 5.3],
    )
    d.p(
        "**Reglas de negocio del capítulo.** RN-16.1 El acceso a una capacidad debe determinarse por "
        "el rol de la cuenta, y su ausencia en el menú no constituye una falla del sistema. "
        "RN-16.2 Toda capacidad marcada como parcialmente habilitada debe acompañarse de su "
        "consideración operativa para que la validación de alcance no la dé por concluida. "
        "RN-16.3 Toda capacidad marcada como prevista debe incorporarse al plan de trabajo con su "
        "capítulo correspondiente."
    )
    d.p(
        "**Consideraciones operativas.** El presente documento es la referencia de alcance para las "
        "fases de análisis, planificación y desarrollo; su aprobación por parte de Product Owners y "
        "patrocinadores habilita la priorización de las capacidades en el plan de trabajo, y su "
        "modificación posterior debe registrar la versión y el motivo del cambio."
    )

    d.save(os.path.join(OUT, "07_Documento_de_Requerimientos_Funcionales.docx"))
    print("Documento de requerimientos funcionales generado")


if __name__ == "__main__":
    main()
