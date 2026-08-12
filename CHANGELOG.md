# Historial de cambios

Resumen, orientado al lector externo, de las rondas de revisión que llevaron el repositorio a su estado actual. El detalle completo de cada hallazgo, con su metodología de verificación, está en `MEMORIA_PROYECTO.md`; este archivo sólo ordena cronológicamente qué cambió y por qué.

## Reconstrucción del informe (`reporte_modelo_C.tex`)
El archivo `.tex` original que compilaba el PDF de 32 páginas se perdió durante una reorganización externa del proyecto. Se reconstruyó por completo transcribiendo el contenido ya verificado del PDF de referencia, y se reemplazaron las 31 figuras por versiones generadas en código (`graficos.py`) a partir de datos reales, en vez de capturas de pantalla.

## Auditoría de datos y fórmulas, por rondas

- **Ronda 1.** Corrección de un bug de reexpresión monetaria en FY2020 (Ventas Netas, EBITDA, EBIT, Resultado Neto y CAPEX de ese ejercicio tomaban la columna comparativa reexpresada al tipo de cambio de otro año en vez de la cifra del informe anual propio). Corrección de Deuda Neta y Liquidez Corriente históricas, que no derivaban de los estados financieros auditados del motor.
- **Ronda 2.** Implementación trazable del CVaR paramétrico Cornish-Fisher (antes citado en el texto sin respaldo en el motor). Barrido numérico automatizado de aproximadamente 1.220 tokens numéricos del informe contra las fuentes de datos.
- **Ronda 3.** Auditoría gráfico por gráfico de las 14 figuras que no habían sido revisadas a fondo: un dato fabricado y un error de discretización en una simulación estocástica, corregidos.
- **Ronda 4.** Una fila de EBITDA histórico (FY2021–FY2023) desincronizada de su propia fuente en tres cuadros del informe, con arrastre a Resultado Neto, Margen Neto, ROE y Deuda Neta/EBITDA. Redondeo incorrecto en una celda de la proyección de FCFF (FY2028). Referencia bibliográfica sin ninguna cita en el cuerpo del texto, eliminada con renumeración de las citas siguientes.
- **Ronda 5.** Primera auditoría a nivel de fórmula (no sólo de texto o valores) del modelo de Excel: 440 celdas con caché de fórmula vacío —se muestran en blanco en cualquier visor que no recalcule, como una vista previa de GitHub o de Google Sheets, aunque Excel las recalcula solas al abrir el archivo— y un valor grande escrito directo en una fórmula sin celda de origen ni comentario de fuente. Ambos corregidos: recálculo completo del libro y comentarios de fuente agregados a las celdas correspondientes.
- **Ronda 6.** Una sección del informe ("Índices de Sobol") presentaba una tabla de sensibilidad cuyos valores no correspondían a ningún cálculo real: no existe ninguna implementación de análisis de Sobol ni de la librería SALib en el repositorio. Se reemplazó por una sensibilidad de un factor a la vez, genuinamente calculada recorriendo el modelo DCF completo, sobre el precio del aluminio, el costo de capital y la tasa de crecimiento terminal. Se agregaron además un Cuadro de Supuestos Clave, un Glosario de Abreviaturas, un índice de figuras y tablas, una sección de Política de Dividendos, y notas explícitas sobre el alcance del universo de comparables y la ausencia de consenso de analistas y calificación crediticia en el modelo.

## Higiene del repositorio
Se sacaron de seguimiento de git las carpetas de respaldo de rondas anteriores (quedan en el disco local, no en el repositorio público). Se agregaron `LICENSE` y `requirements.txt` con las versiones de dependencias fijadas al entorno de verificación.
