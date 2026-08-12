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

## 4bis. Segunda ronda de esta sesión: hallazgos visuales del usuario + CVaR Cornish-Fisher + barrido numérico automatizado

Después del §4, el usuario hizo una segunda pasada de revisión visual sobre el PDF ya corregido y encontró más problemas concretos, y pidió además implementar lo que en §4 solo se había dejado documentado como hallazgo abierto (el CVaR Cornish-Fisher sin respaldo), y un barrido automatizado del documento completo contra el motor.

**CVaR Cornish-Fisher — implementado, no solo documentado.** De las 6 filas del Cuadro 15 (VaR/CVaR por metodología), la fila "CVaR Cornish-Fisher" no tenía ninguna clave correspondiente en `resultados_original.json` ni cálculo en ningún script del repo — un número con peso argumental real (el párrafo siguiente lo usa para justificar por qué el informe descarta Cornish-Fisher y usa EVT-GPD) sin ningún respaldo trazable. Implementado en `engine_valuacion.py` (función `anexo()`): el CVaR/ES de Cornish-Fisher no tiene una forma cerrada simple y confiable (los polinomios de Hermite de Boudt-Peterson-Croux 2008 tienen riesgo real de error de transcripción), así que se estimó por **simulación** de la misma transformación de Cornish-Fisher ya validada para el VaR (5 corridas × 5.000.000 sorteos N(0,1), promediadas). Antes de tocar el JSON persistido, se corrió el motor completo en memoria y se compararon sus 1.098 valores numéricos contra el archivo ya guardado — 1.088 coincidían exactamente, los 10 que no eran de la simulación de Montecarlo (varianza de semilla, no relacionado) — confirmando que no había drift de datos antes de mergear **solo** las 5 claves nuevas (diff de 6 líneas en el JSON, nada más tocado). Resultado: -7,12%/-10,49%/-20,35% (antes -4,70%/-7,77%/-20,37%, sin ningún respaldo).

**Hallazgos visuales puntuales del usuario, todos confirmados y corregidos:**
- **Fig05** (EMBI+): las etiquetas de pb y de rendimiento % se superponían en los últimos 2 puntos, donde la curva se aplana. Agregado bbox blanco + más separación vertical.
- **Fig07** (producción global): la flecha de la caja explicativa atravesaba literalmente la etiqueta de dato de la barra Argentina; además el cuadro citaba "0.46 MM Tn" mientras el resto del gráfico decía "0.44" — mismo gráfico, dos números para el mismo dato. Corregido el número (ahora lee el dato real en vez de estar hardcodeado) y redirigida la flecha.
- **Fig20** (distribución Monte Carlo): no tenía ninguna etiqueta de dato más allá de la leyenda. Agregados callouts con caja para Mediana, Spot, P5 y P95.
- **Fig25** (EVT-GPD): el eje X dinámico de una vuelta anterior se había pasado de largo (multiplicador ×1,35), dejando una cola final visualmente insignificante. Reducido a ×1,12.
- **Cuadro 10** (Gráfico de Rangos): mezclaba filas con un solo valor centrado en las 3 columnas (`\multicolumn`) y filas con Mín/Central/Máx reales en columnas separadas — la columna "Central" no quedaba alineada verticalmente fila a fila. Unificado: todas las filas usan las mismas 3 columnas, con "--" explícito donde no aplica.
- **Caja de decisión** (portada): la nota metodológica completa vivía adentro del mismo cuadro que el dictamen COMPRAR, saturándolo. Movida fuera de la caja como párrafo propio; agregada la etiqueta "Dictamen del modelo (no es recomendación personal)" directamente arriba de "COMPRAR".
- **"Mapa de Calor CFA"**: removido el acrónimo suelto del título de sección (el cuerpo del párrafo ya explica el estándar del CFA Institute).
- **Desarrollo complementario agregado**: (a) en la Sección 6 (WACC), un párrafo conectando explícitamente WACC como vara de creación de valor (ROIC vs. WACC) con la disciplina de convergencia terminal ya usada en la sección EVA — antes ese vínculo solo vivía implícito; (b) tras la tabla de sensibilidad de $\lambda$, el caso para un $\lambda$ estructuralmente mayor por exposición de *costos* (no solo ingresos) al ciclo doméstico, contrapesado por el efecto de licuación de costos fijos bajo devaluación ya documentado en otra sección — ninguno de los dos efectos está modelado explícitamente, y el párrafo lo deja dicho en vez de callarlo.

**Barrido numérico automatizado.** Script ad hoc (regex de números en formato español sobre el `.tex`, matching con tolerancia contra todos los valores numéricos aplanados de `resultados_original.json` + `static_inputs.json`): de ~1.220 tokens numéricos, 14 únicos no matchearon. Triage uno por uno — la mayoría eran falsos positivos legítimos (cifras citadas a fuentes primarias distintas del motor, como la Memoria de Aluar o el número de la Ley de Mercado de Capitales), pero aparecieron **dos hallazgos reales nuevos**, misma familia que el CVaR Cornish-Fisher pero esta vez no implementados por falta de datos suficientes en el repo (no por falta de tiempo):

- El cuadro "Criterios de Información y Bondad de Ajuste: Riesgo Soberano" (AR(1) vs. CIR, Log-Likelihood/AIC/BIC) reporta magnitudes (~1.450) que son matemáticamente imposibles con la única serie de EMBI+ que existe en el motor (7 observaciones anuales). No hay ninguna serie diaria de riesgo soberano en el código sobre la cual recalcular esto honestamente — a diferencia del CVaR-CF, acá no se podía implementar sin inventar datos que no están en el repo. Se agregó una nota de limitación de reproducibilidad en la tabla en vez de fabricar un recálculo o borrar el hallazgo silenciosamente.
- Los AIC absolutos de la Student-t ($\nu=4,2$) y la Cópula de Clayton en la Sección 16.3 (distintos del $\Delta$AIC=-88,9 de Clayton vs. Gaussiana, que sí se recalcula en `graficos.py`) tampoco están en ningún script del repo. Misma nota de limitación agregada.
- Los precios de los escenarios Bull/Bear del Marco de Escenarios (ARS 1.481 / 781) y la mención de "~ARS 1.450" bajo compresión de EMBI+ se documentaron en `static_inputs.json` (nueva clave `marco_escenarios_bear_base_bull`) con el mismo patrón de `_fuente` ya usado para `stress_test_embi_max`, en vez de dejarlos como números sueltos sin ningún rastro escrito de por qué no se recalculan.

**Patrón que se repitió tres veces en esta sesión** (Deuda Neta/Liquidez Corriente en §4, CVaR Cornish-Fisher, y ahora AR(1)-vs-CIR/Student-t-AIC): un número presentado como salida del motor ("Elaboración propia en base al motor de valuación") que en realidad no tiene ningún cálculo detrás en el código. La lección para quien continúe: cuando sea posible reproducir el número con los datos ya disponibles en el repo, implementarlo (como con Deuda Neta y CVaR-CF); cuando no lo sea porque falta el dato fuente (como con el EMBI+ diario), no fabricar un número plausible — dejar una nota de limitación explícita, igual que ya hacía el informe con otras limitaciones metodológicas propias (Feller, raíz unitaria del proceso OU, etc.).

## 4ter. Tercera ronda: las 14 figuras que quedaban sin revisar a fondo, + cruce con el PPTX

Tras el §4bis, el usuario pidió explícitamente "analiza igual de profundamente todo lo que no hayas visto hasta ahora". Hasta ese punto, 17 de las 31 figuras habían recibido revisión visual profunda en distintas rondas; quedaban 14 sin ese nivel de escrutinio (fig01, 02, 06, 09, 10, 11, 12, 14, 18, 22, 23, 26, 28, 29). Se revisaron las 14, más un cruce dirigido del PPTX contra los hallazgos de esta ronda.

**El hallazgo más grave de toda la sesión — Fig11, datos fabricados.** El código tenía el comentario literal `# Generar márgenes sintéticos empíricos para la misma cantidad de pares`, seguido de un array hardcodeado de "márgenes EBITDA" para Aluar y 6 pares globales. Esos números no salían de ningún cálculo ni cita: eran inventados. Peor aún, el margen "sintético" asignado a Aluar (24,2%) ni siquiera coincidía con el margen real de Aluar ya citado en el resto del propio informe (14,9%, verificado contra el motor). Se reemplazó con un dataset de 4 compañías (Aluar, Alcoa, Norsk Hydro, Chalco) con las 3 métricas (EV/EBITDA, Margen EBITDA, Deuda Neta/EBITDA) verificadas contra el Cuadro de Comparables del informe.

**Hallazgo en cadena.** Al verificar el múltiplo EV/EBITDA de Aluar contra el motor para reconstruir Fig11, apareció que el Cuadro de Comparables citaba 10,2x -- pero `resultados_original.json:m12_multiplos.ev_ebitda_fy25 = 13,43x` es el valor real, recalculado en vivo desde el motor (market cap + deuda neta sobre EBITDA FY25 real), y coincide exactamente con lo que otra figura del mismo informe (Fig22, "Convergencia del múltiplo EV/EBITDA") ya mostraba de forma independiente. El Cuadro de Comparables tenía el número viejo/no reproducible. Se corrigió a 13,4x en el cuadro y en Fig11, y se retituló Fig11 de "Descuento Fundamental" a "Premio Fundamental" -- con el número correcto, Aluar cotiza CON premio sobre sus pares (coherente con la prosa de esa sección, que ya decía "premio persistente"), no con descuento como decía el título viejo.

**Bug de discretización estocástica -- Fig26 (OU vs. MBG del LME).** `kappa` y `sigma` se calibran con `fit_ar1()` sobre la serie YA mensualizada de LME -- son, por construcción, la tasa de reversión y el desvío POR PASO MENSUAL. El paso de simulación Euler-Maruyama los multiplicaba de nuevo por `dt=1/12`, como si fueran tasas anualizadas que había que convertir a mensuales. Ese doble descuento del tiempo volvía la reversión ~12 veces más lenta de lo que el propio ajuste de datos implicaba: la mediana simulada del proceso OU apenas se movía hacia su propia media de largo plazo (theta=2.814 USD/Tn) en los 5 años de proyección, contradiciendo visualmente el propósito mismo del gráfico (mostrar que el OU SÍ revierte, a diferencia del MBG). Corregido el paso Euler (un paso = un mes, sin reescalar). Se encontraron además dos números de texto no relacionados con el bug de código pero igual de reales: "$\kappa=0,80$" citado en la sección no correspondía a ningún cálculo (el kappa mensual real es 0,0316) -- posiblemente remanente de una calibración anterior nunca actualizada -- y la ecuación diferencial estocástica mostrada en el informe describía un proceso log-OU cuando el código simula un OU de nivel de precio (sin logaritmo en ningún paso de la simulación). Se corrigieron ambos.

**Otros hallazgos de esta ronda:**
- Fig01: "2007 Expansión Fase II (460 kt/año)" y "2026 Capacidad Plena 460 kt" presentaban el mismo número de capacidad como dos hitos nuevos distintos dentro de la misma figura -- contradicción interna que además invalidaba una aclaración que yo mismo había agregado en la ronda anterior (§4bis) asumiendo que 460kt era un hito de 2026. Releída la evidencia (el 2007 ya dice "460 kt/año" explícitamente), se reetiquetó 2026 como el hito de autogeneración energética, no de capacidad, y se corrigió la aclaración de la portada en consecuencia.
- Fig06: ~300 observaciones consecutivas de la serie LME (jun-2018 a ago-2019) resultaron ser un artefacto de *forward-fill* -- 23 valores únicos repartidos en 302 días hábiles, no precios reales. Sin dato de mercado real disponible en el repo para corregirlo (sería fabricar el precio que faltó); se documentó como limitación, afectando también al test de Engle-Granger que corre sobre la misma serie.
- Fig10: tres números distintos para el mismo dato en tres lugares del informe (percentil de Aluar en la curva de costos C1 global: 21% en el subtítulo hardcodeado del propio gráfico, 28% en la portada, 29% en la línea vertical que el gráfico sí calcula dinámicamente). Unificados los tres a 29%, y el subtítulo de Fig10 se recalculó para que ya no pueda desincronizarse de la línea que dibuja.
- Fig07 y Fig12: flechas de anotación que atravesaban literalmente la etiqueta de dato que señalaban (mismo patrón de bug encontrado en rondas anteriores en otras figuras). Corregidas las trayectorias.
- Fig18: la leyenda en "lower right" colisionaba con la barra más ancha del gráfico (Monte Carlo P5-P95), tapando el "Spot"/"Target". Reposicionada.
- Fig23: el gráfico y el texto recomendaban Half-Kelly (36,8%) sin mencionar que excede el propio límite de política de riesgo del modelo (20% CVaR máximo de tolerancia al *drawdown*), visible en la 4ª barra del mismo gráfico. Es una tensión real entre dos criterios independientes (Kelly = tamaño óptimo de crecimiento; CVaR = tolerancia de política), no un error de cálculo -- pero el texto la ocultaba en vez de resolverla. Se agregó la reconciliación explícita: el tamaño recomendado es el menor de los dos (20%, no 36,8%).

**Cruce con el PPTX.** Sin capacidad de renderizar el PPTX a imagen en este entorno (sin LibreOffice/PowerPoint disponible), se hizo un cruce de texto dirigido: buscar en el PPTX los mismos números que se acababan de corregir en el PDF. La mayoría no aparecían en el PPTX (no replica esas tablas/cifras). Sí apareció el mismo problema de Fig23: un stat-box de la slide de Portafolio decía "ALOCACIÓN HALF-KELLY 36.8% Cartera" sin el límite CVaR, y la slide de conclusión decía "Tamaño de posición recomendado: 36.8% de la cartera". Corregidos ambos, con cuidado de no romper el layout de las cajas de estadísticas (2,95" de ancho) -- edición mínima manteniendo la misma longitud de texto en el stat-box, sin poder verificar visualmente el resultado final por falta de herramienta de render.

## 5. Metodología de auditoría usada en esta sesión

No hubo una sola técnica — se combinaron varias según el tipo de bug buscado:

1. **Trazabilidad numérica**: para cualquier número en el `.tex`, buscar su clave correspondiente en `resultados_original.json` / `static_inputs.json`. Si no aparece, es sospechoso. Si aparece pero no coincide, es un bug confirmado.
2. **Consistencia interna de tablas**: verificar que las filas de una misma tabla sean matemáticamente consistentes entre sí (ej.: Deuda Neta ÷ EBITDA debe reproducir la fila de ratio de la misma tabla). Una tabla puede estar "sincronizada consigo misma" y aun así estar mal — pero si ni siquiera eso se cumple, es la señal más barata de un bug.
3. **Diff de motor completo antes de tocar el JSON**: antes de persistir cualquier valor nuevo calculado, correr el motor completo en memoria y comparar los ~1.100 valores numéricos contra el archivo ya guardado. Si algo además de lo esperado cambia, hay drift de datos y no es seguro mergear a ciegas.
4. **Grep de patrones de IA**: frases de relleno conocidas ("es importante destacar", "framework", "sinergia", "holístico", patrón "no es X, es Y" sobreusado) sobre el texto completo, no solo títulos.
5. **Duplicados**: contar apariciones de cada `\captionof{figure}`, cada `\subsection{}`, cada `figura_NN.png` incluido — más de una aparición de lo mismo es una bandera roja de contenido pegado dos veces por sesiones distintas sin coordinación.
6. **Verificación visual dirigida**: para hallazgos específicos señalados por el usuario (ej. "GARCH no tiene nube"), leer la imagen renderizada — pero evitando una revisión pixel a pixel de las 31 figuras por costo, salvo pedido explícito.
7. **Barrido numérico automatizado**: extraer con regex todos los números en formato español del `.tex`, aplanar recursivamente ambos JSON de datos a una lista de valores, y hacer matching con tolerancia (relativa + absoluta, probando además escalas ×100/×0,01/×1000 para capturar conversiones de unidad) para encontrar qué números del documento no tienen ningún valor cercano en ninguno de los dos JSON. Mucho más barato que revisar tabla por tabla a mano, con la salvedad de que hay que triar los resultados: la mayoría de los "no matcheados" son falsos positivos legítimos (fechas, números de ley, parámetros de metodología, cifras citadas a una fuente primaria distinta del motor) y no bugs.

## 6. Estado actual (a la fecha de este documento)

- El PDF (`Informe_Valuacion_Institucional_Aluar_UNCuyo.pdf`, 26 páginas) compila desde el archivo correcto (`reporte_modelo_C.tex`), verificado.
- Las 31 figuras de `graficos.py` se regeneran limpiamente y se verificaron idénticas en sus 3 carpetas de salida.
- PPTX y Excel se barrieron por texto/celdas (no por imagen) buscando los mismos patrones de bug encontrados en el PDF — no se encontraron las mismas fallas replicadas ahí.
- El barrido numérico automatizado (§4bis) cubrió el 100% de los números del `.tex` contra el motor — es la verificación más exhaustiva hecha en esta sesión, con 2 limitaciones de reproducibilidad reales quedando documentadas (no ocultas) en vez de resueltas, por falta de datos fuente en el repo (no por falta de esfuerzo).
- Quedan **sin el mismo nivel de escrutinio** en esta sesión: revisión pixel a pixel de la mayoría de las 31 figuras (se hizo en rondas anteriores, más los 4 hallazgos puntuales de fig05/07/20/25 en §4bis; el resto de las figuras no se re-auditó visualmente en esta sesión), y una auditoría de imagen (no solo texto) del PPTX.

## 7. Reglas del proyecto que quedaron obsoletas (no aplican al estado actual)

El repo tiene varios archivos en `.claude/rules/` que referencian una arquitectura anterior — `ALUAR_tesis.pptx` como único target, `run_pipeline.py`, `module13_synthesis.py`, `update_presentation_v10.py`, `build_pptx_final20.py`, numeración de slides S1-S29 de un deck de 53/62 slides. **Ninguno de esos archivos existe en el repo actual** (`valuacion-aluar-uncuyo`); el target vigente es `01_Reporte_PDF/Informe_Valuacion_Institucional_Aluar_UNCuyo.pdf` vía `build_pdf.py` + `reporte_modelo_C.tex`, y el PPTX vigente es `02_Presentacion_PPTX/TrabajoFinalEyTBChillonFedericoAluar_HOMOGENEO.pptx`. Las correcciones de calidad de gráfico que sí describen esas reglas (bbox_inches='tight', sin menciones crudas a "notebook", paleta de colores) siguen vigentes como estándar y se verificaron cumplidas en `graficos.py`.

## 8. Para quien retome este proyecto

- Antes de confiar en cualquier número del `.tex`, verificar contra `resultados_original.json`. Si no está ahí, no asumir que es correcto solo porque "suena razonable" — este documento tiene un historial real de números sin respaldo que sonaban razonables.
- Antes de compilar, verificar que `build_pdf.py` apunte al archivo `.tex` que realmente se está editando. Esto ya falló una vez en esta sesión.
- Si otra sesión o herramienta (humana o IA) trabajó sobre el repo en paralelo sin coordinación, no asumir que sus cambios son compatibles con los propios — diffear explícitamente antes de construir sobre ellos.
- Los archivos de respaldo (`01_Reporte_PDF/backup/`, `01_Reporte_PDF/backup_20260811_auditoria_360/`) son snapshots dejados por sesiones anteriores, no están en `.gitignore` — decidir si vale la pena limpiarlos del repo o mantenerlos como historial.
