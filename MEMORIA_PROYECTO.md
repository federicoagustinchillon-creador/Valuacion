# Memoria del Proyecto — Valuación ALUAR S.A.I.C. (ALUA.BA)

**Trabajo práctico final — Cátedra de Economía y Técnica Bursátil, Facultad de Ciencias Económicas, Universidad Nacional de Cuyo.**
Analista: Federico Agustín Chillón.

Este documento reconstruye la historia del proyecto: qué se probó, qué falló, qué se corrigió y por qué. No es documentación de uso — es un registro de decisiones para quien retome el trabajo más adelante (humano o IA) y necesite entender el *por qué* detrás del estado actual, no solo el estado en sí.

---

## 1. Qué es este proyecto

Una tesis de valuación fundamental de Aluar Aluminio Argentino S.A.I.C. (ALUA.BA), con cuatro entregables que deben estar sincronizados entre sí:

| Entregable | Ruta | Generado por |
|---|---|---|
| Informe PDF (25 pág.) | `01_Reporte_PDF/Informe_Valuacion_Institucional_Aluar_UNCuyo.pdf` | `build_pdf.py` compila `tex/reporte_modelo_C.tex` con XeLaTeX |
| Presentación PPTX | `02_Presentacion_PPTX/TrabajoFinalEyTBChillonFedericoAluar_HOMOGENEO.pptx` | Editado directamente (no programático) |
| Modelo Excel | `04_Modelo_Excel/Valuacion_Aluar_Modelo_Oficial.xlsx` | Fórmulas originales, editado directamente |
| Motor de valuación | `03_Modelo_y_Codigo/engine_valuacion.py` | Python puro; `resultados_original.json` es su salida persistida |
| 31 figuras nativas | `03_Modelo_y_Codigo/graficos.py` | Matplotlib, lee `resultados_original.json`/`static_inputs.json`, escribe a 3 carpetas simultáneas (`figuras/`, `figures_pristine/`, `Assets_Oficiales_Pristinos/`) |

El motor (`engine_valuacion.py`) es la única fuente de verdad numérica. Todo lo demás (PDF, PPTX, Excel) debería derivar de él — pero en la práctica, buena parte del PDF es prosa y tablas **tipeadas a mano**, no generadas programáticamente desde el JSON. Esa brecha entre "el motor calcula X" y "el documento dice X" es la causa raíz de casi todos los bugs de esta historia.

## 2. Cronología (versiones previas al estado actual)

Reconstruida a partir de memoria persistente de sesiones anteriores — resumen, no el detalle completo:

1. **Modelo A** — primer intento de valuación DCF. Target ARS 1.324.
2. **Modelo B / Caso Moderado** — dos intentos fallidos (hardcodes de datos, benchmark de peers que producía equity negativo) antes de una reconstrucción válida sourced al informe de auditoría real. Entregable: `ALUAR_tesis_A_vs_B.pptx`.
3. **Fix Capacidad Física** — deck de 30 slides. Bug encontrado: Revenue se calculaba mal; corregido a Volumen (460k Tn) × Precio Realizado. Cambio de dictamen MANTENER→VENDER. Target recalculado 914→685→631 (el segundo ajuste fue por un bug de interpolación en la serie LME).
4. **Bug de recálculo en Entregable_v2** — el archivo Excel quedaba con `fullCalcOnLoad=0` tras una cadena de 9 guardados con `openpyxl`, dejando celdas en blanco hasta que Excel las recalculaba manualmente. Encontrado también un bug latente (sin daño confirmado) en un script `fix_all.py` que hacía `replace()` sobre fórmulas.
5. **Modelo C — Entregable_v2 (final de esa etapa)** — target ARS 1.236, no el ARS 1.324 del Modelo A. Se agregaron 4 slides nuevas (EBITDA futuro, Cornish-Fisher, convergencia de tasas). Todo verificado en ese momento.
6. **Migración a `valuacion-aluar-uncuyo`** — el repo actual, subido a GitHub (`federicoagustinchillon-creador/Valuacion`). El `.tex` tuvo que reconstruirse desde cero (la fuente original se había perdido); se verificaron 31 figuras byte a byte; se corrigió un bug de FY2020. Hallazgo que quedó abierto en ese momento: la Deuda Neta no coincidía entre el cuadro del informe y el motor (ver §4.1 — se resolvió recién en esta sesión).

## 3. Esta sesión: contexto de partida

Al arrancar esta sesión, el usuario advirtió que **otra herramienta de IA (Antigravity) había trabajado sobre el mismo repo en paralelo**, reescribiendo buena parte de `graficos.py` (1.185 líneas de diff sobre ~1.480) y de `reporte_modelo_C.tex` (152 líneas de diff) sin coordinación con esta sesión. El pedido explícito fue: entender qué hizo cada uno, y garantizar sincronización total entre texto y gráficos — "había varias cosas desincronizadas".

Esto cambió el enfoque de "seguir mejorando gráficos" a **"auditar de cero, sin asumir que nada está bien"** — incluyendo no confiar en el propio pipeline de build.

## 4. Bugs encontrados y corregidos en esta sesión

### 4.1 `build_pdf.py` compilaba un archivo fantasma (el más grave)

`build_pdf.py` apuntaba a `tex/reporte_modelo_C_2.tex` — un fork desactualizado que Antigravity había dejado tirado (probablemente al hacer una prueba y no revertir el apuntador). El archivo que todo el mundo —yo, el usuario, Antigravity mismo en sus ediciones posteriores— veníamos editando (`reporte_modelo_C.tex`) **no se estaba compilando**. Todo el trabajo de correcciones de esta sesión (y probablemente de la anterior) se estaba perdiendo silenciosamente en cada build.

Cómo se detectó: después de corregir un bug numérico en `reporte_modelo_C.tex` y recompilar, el PDF seguía mostrando el valor viejo. Verificación cruzada por `mtime` de archivos y `grep` del texto extraído del PDF confirmó que el número corregido nunca llegaba al binario.

Se decidió cuál de los dos archivos era el correcto verificando un dato objetivo: `graficos.py` implementa nativamente una cópula de Clayton (no gaussiana) en la Figura 31; `reporte_modelo_C.tex` lo describía correctamente, `reporte_modelo_C_2.tex` describía (incorrectamente, de forma obsoleta) una cópula Gaussiana con la implementación de Clayton pendiente. Eso confirmó cuál archivo reflejaba el estado real del código. Se repunteó `build_pdf.py` al archivo correcto y se eliminó el fork.

**Lección:** nunca asumir que el pipeline de build apunta a donde dice apuntar, sobre todo después de que otra sesión/herramienta tocó el repo sin avisar.

### 4.2 Deuda Neta histórica (tabla FY2020-FY2025) — número copiado del año equivocado

La fila "Deuda Neta" de dos tablas del informe tenía, para FY2020, el valor `594,95` — que resultó ser exactamente la Deuda Financiera Total de FY2025 (`resultados_original.json: m4_estados/usd/2025/deuda_financiera = 594.95`), pegada por error en la celda de FY2020. Se detectó porque la fila "Deuda Neta / EBITDA" de la misma tabla (4,00x) no reconciliaba matemáticamente con Deuda Neta ÷ EBITDA usando los propios números de la tabla (daba 5,11x, no 4,00x) — inconsistencia interna que disparó la investigación.

Corregido con la serie real (`m4_estados/usd/*/deuda_neta`): 351,30 / 137,44 / 57,33 / 169,88 / 211,23 / 525,76 (FY2020→FY2025). La fila de ratio se recalculó en consecuencia: 3,02x / 1,28x / 0,27x / 1,61x / 1,03x / 3,22x.

### 4.3 Liquidez Corriente histórica — no correspondía a ningún cálculo real

Los 6 valores de la fila (1,34x–1,55x) no reproducían Activo Corriente ÷ Pasivo Corriente de ningún año del balance auditado. Verificado contra `m4_estados/usd/*/activo_corriente` y `pasivo_corriente`: los valores reales eran sistemáticamente más del doble (1,89x–4,93x). No hay explicación de dónde salió la serie original — probablemente una tabla de otra iteración del modelo pegada sin actualizar.

### 4.4 CVaR Cornish-Fisher — número sin respaldo trazable en el motor

De las 6 filas de la tabla de VaR/CVaR (Cuadro 15), 5 tenían su cálculo persistido en `resultados_original.json`. La fila "CVaR Cornish-Fisher" (-4,70% / -7,77% / -20,37%) no existía en ningún lado del código: ni en el JSON, ni en `graficos.py`, ni en `engine_valuacion.py`. El propio párrafo del informe usaba ese número como argumento central para justificar por qué el modelo descarta Cornish-Fisher y usa EVT-GPD — es decir, un número con peso argumental real, no cosmético.

Implementado en `engine_valuacion.py` (función `anexo()`), extendiendo el mismo bloque donde ya vivía el VaR de Cornish-Fisher (ya validado — se confirmó que reproduce exactamente los valores existentes). El CVaR no tiene una forma cerrada simple y confiable (la fórmula de Boudt-Peterson-Croux 2008 usa polinomios de Hermite de orden superior, con riesgo real de error de transcripción); en su lugar se estimó por **simulación** de la misma transformación de Cornish-Fisher ya validada para el VaR (5 corridas × 5.000.000 sorteos N(0,1), promediadas; desvío entre corridas <0,05pp).

Antes de escribir nada al JSON, se corrió el motor completo en memoria y se compararon sus 1.098 valores numéricos contra el archivo persistido: 1.088 coincidían exactamente; los únicos 10 que no eran de `m9_monte_carlo` (varianza de semilla de esa simulación puntual, no relacionado con este fix). Confirmado que no había drift de datos de mercado ni de ningún otro módulo antes de tocar el archivo — y se mergearon **solo** los 5 keys nuevos, sin regenerar el resto del JSON (que hubiera arrastrado cambios no relacionados en toda la simulación de Montecarlo).

Resultado: -7,12% / -10,49% / -20,35%. El valor a 99% resultó casi idéntico al que ya estaba (-20,37% vs -20,35%, dentro del ruido de simulación) — pero 90% y 95% sí estaban mal.

### 4.5 Figura 30 (GARCH) duplicaba la Figura 24 (Kalman) y perdió su banda de confianza

Antigravity había reescrito `plot_figura_30` como un panel doble "Kalman vs. GARCH", repitiendo la misma serie del Filtro de Kalman que ya tiene figura propia con análisis dedicado (Figura 24) — y en el proceso, perdió la banda de confianza ±2σ ("la nube") que esta sesión ya le había agregado al panel GARCH en una vuelta anterior. El título de sección tampoco correspondía: mencionaba "Filtro de Kalman vs. GARCH(1,1)" pero el caption de la figura ya decía solamente "GARCH vs. Estimación Estática" — desincronizado consigo mismo.

Revertido a panel único, exclusivamente GARCH, con la banda de confianza restaurada. Título de sección corregido para no prometer una comparación con Kalman que la figura no muestra.

### 4.6 Sección "DCF Inverso" duplicada

Existían dos subsecciones distintas afirmando el mismo hallazgo (g implícita = 0,69%): una con figura propia ("Prueba Retrospectiva de la Señal del DCF Inverso", con la Figura 21), y otra sin ninguna figura ("Auditoría de Expectativas de Mercado: DCF Inverso Probabilístico") que solo repetía la misma frase. Eliminada la segunda por ser un duplicado huérfano sin aporte.

### 4.7 Figura 31 (Cópula de Clayton) — número de la prosa no coincidía con el gráfico

El texto afirmaba que el percentil P5 bajista se reajustaba a ARS 812; el gráfico real (con semilla fija, reproducible) muestra ARS 750. Corregido el texto.

### 4.8 EVT-GPD (Figura 25) — eje X con margen desperdiciado

El eje estaba fijo en 0-25% aunque los datos reales de pérdida diaria no superan 22%, dejando ~40% del ancho del gráfico vacío. Cambiado a un límite dinámico (`max(20, pérdida_máxima × 1.35)`) para no depender de un número mágico que se desactualice si la serie de mercado crece.

### 4.9 Índice y "Descripción de la Compañía" compartían página

No había salto de página entre el índice (`\tableofcontents`) y la sección 1. Si el índice no llenaba la página completa, la sección siguiente arrancaba en el mismo folio, mezclando visualmente ambos contenidos. Agregado `\clearpage`.

### 4.10 Adjetivos de relleno tipo IA en títulos

- "Análisis de Sensibilidad **Académica** sobre el Factor λ" → sin el adjetivo (la sección ya es técnica de por sí, "académica" no calificaba nada real).
- "Análisis Estratégico y de la Industria (**Frameworks corporativos**)" → sin el paréntesis (anglicismo + relleno).
- "**Matriz Corporativa** de Riesgos 2D" → "Matriz de Riesgos 2D" (no son matrices de una corporación, son matrices de riesgo).
- "**Matriz Corporativa** de Escenarios de Estrés" → "Matriz de Escenarios de Estrés".

Se verificó que los usos restantes de "corporativo/a" y "académico/a" en el documento son terminología real y se dejaron intactos (Gobernanza Corporativa, "Matriz de Riesgos Corporativos y de Mercado" como categoría de riesgo — no relleno —, cita bibliográfica de "Finanzas Corporativas", disclaimer legal).

## 5. Metodología de auditoría usada en esta sesión

No hubo una sola técnica — se combinaron varias según el tipo de bug buscado:

1. **Trazabilidad numérica**: para cualquier número en el `.tex`, buscar su clave correspondiente en `resultados_original.json` / `static_inputs.json`. Si no aparece, es sospechoso. Si aparece pero no coincide, es un bug confirmado.
2. **Consistencia interna de tablas**: verificar que las filas de una misma tabla sean matemáticamente consistentes entre sí (ej.: Deuda Neta ÷ EBITDA debe reproducir la fila de ratio de la misma tabla). Una tabla puede estar "sincronizada consigo misma" y aun así estar mal — pero si ni siquiera eso se cumple, es la señal más barata de un bug.
3. **Diff de motor completo antes de tocar el JSON**: antes de persistir cualquier valor nuevo calculado, correr el motor completo en memoria y comparar los ~1.100 valores numéricos contra el archivo ya guardado. Si algo además de lo esperado cambia, hay drift de datos y no es seguro mergear a ciegas.
4. **Grep de patrones de IA**: frases de relleno conocidas ("es importante destacar", "framework", "sinergia", "holístico", patrón "no es X, es Y" sobreusado) sobre el texto completo, no solo títulos.
5. **Duplicados**: contar apariciones de cada `\captionof{figure}`, cada `\subsection{}`, cada `figura_NN.png` incluido — más de una aparición de lo mismo es una bandera roja de contenido pegado dos veces por sesiones distintas sin coordinación.
6. **Verificación visual dirigida**: para hallazgos específicos señalados por el usuario (ej. "GARCH no tiene nube"), leer la imagen renderizada — pero evitando una revisión pixel a pixel de las 31 figuras por costo, salvo pedido explícito.

## 6. Estado actual (a la fecha de este documento)

- El PDF (`Informe_Valuacion_Institucional_Aluar_UNCuyo.pdf`, 25 páginas) compila desde el archivo correcto (`reporte_modelo_C.tex`), verificado.
- Las 31 figuras de `graficos.py` se regeneran limpiamente y se verificaron idénticas en sus 3 carpetas de salida.
- PPTX y Excel se barrieron por texto/celdas (no por imagen) buscando los mismos patrones de bug encontrados en el PDF — no se encontraron las mismas fallas replicadas ahí.
- Quedan **sin el mismo nivel de escrutinio** en esta sesión: revisión pixel a pixel de la mayoría de las 31 figuras (se hizo en rondas anteriores para 8: fig03, 04, 08, 13, 15, 16, 19, 24, 25, 27, 30, 31; el resto no se re-auditó visualmente en esta sesión), y una auditoría de imagen (no solo texto) del PPTX.

## 7. Reglas del proyecto que quedaron obsoletas (no aplican al estado actual)

El repo tiene varios archivos en `.claude/rules/` que referencian una arquitectura anterior — `ALUAR_tesis.pptx` como único target, `run_pipeline.py`, `module13_synthesis.py`, `update_presentation_v10.py`, `build_pptx_final20.py`, numeración de slides S1-S29 de un deck de 53/62 slides. **Ninguno de esos archivos existe en el repo actual** (`valuacion-aluar-uncuyo`); el target vigente es `01_Reporte_PDF/Informe_Valuacion_Institucional_Aluar_UNCuyo.pdf` vía `build_pdf.py` + `reporte_modelo_C.tex`, y el PPTX vigente es `02_Presentacion_PPTX/TrabajoFinalEyTBChillonFedericoAluar_HOMOGENEO.pptx`. Las correcciones de calidad de gráfico que sí describen esas reglas (bbox_inches='tight', sin menciones crudas a "notebook", paleta de colores) siguen vigentes como estándar y se verificaron cumplidas en `graficos.py`.

## 8. Para quien retome este proyecto

- Antes de confiar en cualquier número del `.tex`, verificar contra `resultados_original.json`. Si no está ahí, no asumir que es correcto solo porque "suena razonable" — este documento tiene un historial real de números sin respaldo que sonaban razonables.
- Antes de compilar, verificar que `build_pdf.py` apunte al archivo `.tex` que realmente se está editando. Esto ya falló una vez en esta sesión.
- Si otra sesión o herramienta (humana o IA) trabajó sobre el repo en paralelo sin coordinación, no asumir que sus cambios son compatibles con los propios — diffear explícitamente antes de construir sobre ellos.
- Los archivos de respaldo (`01_Reporte_PDF/backup/`, `01_Reporte_PDF/backup_20260811_auditoria_360/`) son snapshots dejados por sesiones anteriores, no están en `.gitignore` — decidir si vale la pena limpiarlos del repo o mantenerlos como historial.
