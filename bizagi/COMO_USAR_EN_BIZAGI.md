# Diagramas BPMN para Bizagi Modeler

En esta carpeta hay 4 diagramas en formato BPMN 2.0 (`.bpmn`). Ya están puestos en la tesis
(dibujados en notación BPMN); el profe pidió que se vean hechos en Bizagi, así que hay que
pasarlos a Bizagi Modeler y exportarlos como imagen.

## Opción 1: importar (lo más rápido)

1. Instala Bizagi Modeler (es gratis: https://www.bizagi.com/es/plataforma/modeler).
2. Abre Bizagi Modeler y busca la opción **Importar** en el menú principal; elige el formato
   **BPMN** y selecciona uno de los archivos `.bpmn` de esta carpeta.
3. Revisa que los carriles, tareas y flechas se vean bien; si alguna flecha se cruza, muévela.
4. Exporta el diagrama como imagen PNG (menú **Exportar > Imagen**).

Si tu versión de Bizagi no trae la opción de importar BPMN, usa la opción 2.

## Opción 2: dibujarlo a mano

Crea un diagrama nuevo, pon un **pool** con el nombre indicado, agrega los **carriles** (lanes)
en ese orden y luego los elementos de cada carril, de izquierda a derecha (columna 1, 2, 3...).
Las conexiones van en la lista de flujos. Usa la misma disposición de la imagen `imagenes/<nombre>.png`.

## Cómo ponerlos en la tesis

Guarda cada PNG exportado en la carpeta `imagenes/` con este nombre exacto y vuelve a compilar:
la tesis usa automáticamente la versión de Bizagi en lugar de la dibujada.

| Archivo BPMN | Guardar el PNG de Bizagi como | Dónde aparece |
|---|---|---|
| `bpmn_actual_gestion.bpmn` | `imagenes/bizagi_actual_gestion.png` | Figura del Capítulo III (parte superior) |
| `bpmn_actual_soporte.bpmn` | `imagenes/bizagi_actual_soporte.png` | Figura del Capítulo III (parte inferior) |
| `bpmn_mejorado_gestion.bpmn` | `imagenes/bizagi_mejorado_gestion.png` | Figura de la sección 4.4 (parte superior) |
| `bpmn_mejorado_soporte.bpmn` | `imagenes/bizagi_mejorado_soporte.png` | Figura de la sección 4.4 (parte inferior) |

## bpmn_actual_gestion

**Pool:** Gestión tributaria predial con Sispredios (situación actual)

**Carriles (de arriba hacia abajo):** 1) Contribuyente, 2) Caja, 3) Rentas, 4) Ejecutoría coactiva

| Col. | Carril | Tipo | Nombre |
|---|---|---|---|
| 1 | Contribuyente | Evento de inicio | Presenta declaración jurada |
| 2 | Rentas | Tarea | Registrar predio, pisos y propietarios en Sispredios |
| 3 | Rentas | Tarea | Emitir las deudas anuales en la cuenta corriente |
| 4 | Contribuyente | Compuerta exclusiva | ¿Paga antes del vencimiento? |
| 5 | Contribuyente | Tarea | Pagar en caja o en el banco |
| 5 | Rentas | Tarea | Armar listados a mano en hojas de cálculo |
| 6 | Caja | Tarea | Registrar el pago o importar el archivo del banco |
| 6 | Rentas | Tarea | Enviar cartas de aviso a todos los deudores |
| 7 | Caja | Tarea | Cuadrar la caja al cierre del día |
| 7 | Rentas | Tarea | Emitir valores (OP o RD) |
| 8 | Caja | Evento de fin | Deuda cancelada |
| 8 | Rentas | Compuerta exclusiva | ¿Firma convenio? |
| 9 | Rentas | Tarea | Registrar el fraccionamiento |
| 9 | Ejecutoría coactiva | Tarea | Abrir expediente de cobranza coactiva |
| 10 | Rentas | Evento de fin | Deuda fraccionada |
| 10 | Ejecutoría coactiva | Evento de fin | Cobranza coactiva |

**Flujos:**

- Presenta declaración jurada → Registrar predio, pisos y propietarios en Sispredios
- Registrar predio, pisos y propietarios en Sispredios → Emitir las deudas anuales en la cuenta corriente
- Emitir las deudas anuales en la cuenta corriente → ¿Paga antes del vencimiento?
- ¿Paga antes del vencimiento? → Pagar en caja o en el banco (**Sí**)
- Pagar en caja o en el banco → Registrar el pago o importar el archivo del banco
- Registrar el pago o importar el archivo del banco → Cuadrar la caja al cierre del día
- Cuadrar la caja al cierre del día → Deuda cancelada
- ¿Paga antes del vencimiento? → Armar listados a mano en hojas de cálculo (**No**)
- Armar listados a mano en hojas de cálculo → Enviar cartas de aviso a todos los deudores
- Enviar cartas de aviso a todos los deudores → Emitir valores (OP o RD)
- Emitir valores (OP o RD) → ¿Firma convenio?
- ¿Firma convenio? → Registrar el fraccionamiento (**Sí**)
- Registrar el fraccionamiento → Deuda fraccionada
- ¿Firma convenio? → Abrir expediente de cobranza coactiva (**No**)
- Abrir expediente de cobranza coactiva → Cobranza coactiva

## bpmn_actual_soporte

**Pool:** Atención de soporte técnico de Sispredios (situación actual)

**Carriles (de arriba hacia abajo):** 1) Personal municipal, 2) Desarrollador (Consultoría Informática)

| Col. | Carril | Tipo | Nombre |
|---|---|---|---|
| 1 | Personal municipal | Evento de inicio | Ocurre una incidencia |
| 2 | Personal municipal | Tarea | Reportar la incidencia o el pedido de cambio |
| 3 | Desarrollador (Consultoría Informática) | Tarea | Analizar la incidencia (único desarrollador) |
| 4 | Desarrollador (Consultoría Informática) | Compuerta exclusiva | ¿Dónde está el error? |
| 5 | Desarrollador (Consultoría Informática) | Tarea | Modificar el código en Visual FoxPro |
| 5 | Desarrollador (Consultoría Informática) | Tarea | Corregir los datos con un programa escrito para el caso |
| 6 | Desarrollador (Consultoría Informática) | Tarea | Recompilar el ejecutable completo (27–28 MB) |
| 7 | Desarrollador (Consultoría Informática) | Tarea | Copiar el ejecutable en cada equipo |
| 8 | Desarrollador (Consultoría Informática) | Tarea | Adaptar la corrección en la copia de cada municipalidad |
| 9 | Personal municipal | Tarea | Reanudar el trabajo detenido |
| 10 | Personal municipal | Evento de fin | Incidencia atendida |

**Flujos:**

- Ocurre una incidencia → Reportar la incidencia o el pedido de cambio
- Reportar la incidencia o el pedido de cambio → Analizar la incidencia (único desarrollador)
- Analizar la incidencia (único desarrollador) → ¿Dónde está el error?
- ¿Dónde está el error? → Modificar el código en Visual FoxPro (**Código**)
- Modificar el código en Visual FoxPro → Recompilar el ejecutable completo (27–28 MB)
- Recompilar el ejecutable completo (27–28 MB) → Copiar el ejecutable en cada equipo
- Copiar el ejecutable en cada equipo → Adaptar la corrección en la copia de cada municipalidad
- Adaptar la corrección en la copia de cada municipalidad → Reanudar el trabajo detenido
- ¿Dónde está el error? → Corregir los datos con un programa escrito para el caso (**Datos**)
- Corregir los datos con un programa escrito para el caso → Reanudar el trabajo detenido
- Reanudar el trabajo detenido → Incidencia atendida

## bpmn_mejorado_gestion

**Pool:** Gestión tributaria predial con el sistema web (situación mejorada)

**Carriles (de arriba hacia abajo):** 1) Contribuyente, 2) Caja, 3) Rentas, 4) Ejecutoría coactiva, 5) Sistema web y modelo de ML

| Col. | Carril | Tipo | Nombre |
|---|---|---|---|
| 1 | Contribuyente | Evento de inicio | Presenta declaración jurada |
| 2 | Rentas | Tarea | Registrar el predio en el sistema web |
| 3 | Sistema web y modelo de ML | Tarea de servicio (automática) | Calcular y emitir las deudas automáticamente |
| 4 | Contribuyente | Compuerta exclusiva | ¿Paga antes del vencimiento? |
| 5 | Contribuyente | Tarea | Pagar en caja |
| 5 | Sistema web y modelo de ML | Tarea de servicio (automática) | Modelo ML: grupo, deuda esperada y acción sugerida |
| 6 | Caja | Tarea | Cobrar y emitir recibo correlativo |
| 6 | Rentas | Tarea | Priorizar la cobranza con la lista (tramos A, B y C) |
| 7 | Caja | Tarea | Cerrar la caja del día por cajero |
| 7 | Rentas | Tarea | Enviar recordatorios y valores a los priorizados |
| 8 | Caja | Evento de fin | Deuda cancelada |
| 8 | Rentas | Compuerta exclusiva | ¿Firma convenio? |
| 9 | Rentas | Tarea | Registrar el fraccionamiento |
| 9 | Ejecutoría coactiva | Tarea | Recibir el valor transferido y asignarlo a un auxiliar |
| 10 | Rentas | Evento de fin | Deuda fraccionada |
| 10 | Ejecutoría coactiva | Evento de fin | Cobranza coactiva |

**Flujos:**

- Presenta declaración jurada → Registrar el predio en el sistema web
- Registrar el predio en el sistema web → Calcular y emitir las deudas automáticamente
- Calcular y emitir las deudas automáticamente → ¿Paga antes del vencimiento?
- ¿Paga antes del vencimiento? → Pagar en caja (**Sí**)
- Pagar en caja → Cobrar y emitir recibo correlativo
- Cobrar y emitir recibo correlativo → Cerrar la caja del día por cajero
- Cerrar la caja del día por cajero → Deuda cancelada
- ¿Paga antes del vencimiento? → Modelo ML: grupo, deuda esperada y acción sugerida (**No**)
- Modelo ML: grupo, deuda esperada y acción sugerida → Priorizar la cobranza con la lista (tramos A, B y C)
- Priorizar la cobranza con la lista (tramos A, B y C) → Enviar recordatorios y valores a los priorizados
- Enviar recordatorios y valores a los priorizados → ¿Firma convenio?
- ¿Firma convenio? → Registrar el fraccionamiento (**Sí**)
- Registrar el fraccionamiento → Deuda fraccionada
- ¿Firma convenio? → Recibir el valor transferido y asignarlo a un auxiliar (**No**)
- Recibir el valor transferido y asignarlo a un auxiliar → Cobranza coactiva

## bpmn_mejorado_soporte

**Pool:** Atención de soporte técnico con el sistema web (situación mejorada)

**Carriles (de arriba hacia abajo):** 1) Personal municipal, 2) Desarrolladores, 3) Sistema web

| Col. | Carril | Tipo | Nombre |
|---|---|---|---|
| 1 | Personal municipal | Evento de inicio | Ocurre una incidencia |
| 2 | Personal municipal | Tarea | Reportar la incidencia o el pedido de cambio |
| 3 | Desarrolladores | Tarea | Analizar la incidencia |
| 4 | Desarrolladores | Tarea | Corregir el código en la única base de código |
| 5 | Desarrolladores | Tarea | Revisar e integrar el cambio (pull request) |
| 6 | Sistema web | Tarea de servicio (automática) | Desplegar la nueva versión para todas las municipalidades |
| 7 | Personal municipal | Tarea | Recargar el navegador y continuar |
| 8 | Personal municipal | Evento de fin | Incidencia atendida |

**Flujos:**

- Ocurre una incidencia → Reportar la incidencia o el pedido de cambio
- Reportar la incidencia o el pedido de cambio → Analizar la incidencia
- Analizar la incidencia → Corregir el código en la única base de código
- Corregir el código en la única base de código → Revisar e integrar el cambio (pull request)
- Revisar e integrar el cambio (pull request) → Desplegar la nueva versión para todas las municipalidades
- Desplegar la nueva versión para todas las municipalidades → Recargar el navegador y continuar
- Recargar el navegador y continuar → Incidencia atendida
