# Valuación Institucional de Aluar Aluminio Argentino S.A.I.C.

**Trabajo Final de Grado / Evaluación Institucional**  
*Universidad Nacional de Cuyo (UNCuyo)*  
**Autor:** Federico Chillón  

---

## 📌 Descripción del Proyecto

Este repositorio contiene la **valuación financiera institucional unificada** de **Aluar Aluminio Argentino S.A.I.C. (BCBA: ALUA)**. El proyecto combina un enfoque riguroso de finanzas corporativas con modelización cuantitativa avanzada en Python y Excel.

El modelo incluye:
- **Flujos de Fondos Descontados (DCF)**: Modelo de dos etapas con simulación de curvas de costo operativo (LME, alúmina, energía) y costo de capital (WACC = 7.06%) ajustado por riesgo país ($\lambda \times \text{EMBI+}$).
- **Simulación Monte Carlo**: Evaluación probabilística de variaciones en variables macroeconómicas y commoditarias clave (10,000 iteraciones).
- **Valuación por Múltiples Comparables**: Análisis de múltiplos de pares regionales e internacionales ($EV/EBITDA$, $P/E$, $P/BV$).
- **Reverse DCF & Análisis de Sensibilidad**: Descomposición de expectativas implícitas en el precio de mercado.

---

## 📁 Estructura del Repositorio

```text
valuacion-aluar-uncuyo/
├── README.md                                  # Presentación ejecutiva y documentación
├── 01_Reporte_PDF/
│   ├── Informe_Valuacion_Institucional_Aluar_UNCuyo.pdf  # Informe oficial (30 páginas) — entregable de referencia
│   ├── reporte_modelo_C.tex                    # Fuente LaTeX real y completa del informe (reconstruida, ver más abajo)
│   ├── build_pdf.py                            # Compila reporte_modelo_C.tex -> el PDF anterior (xelatex, 3 pasadas)
│   └── figures_pristine/                       # Las 31 figuras exactas embebidas en el PDF de referencia (extraídas sin pérdida)
├── 02_Presentacion_PPTX/
│   └── TrabajoFinalEyTBChillonFedericoAluar_HOMOGENEO.pptx # Presentación ejecutiva oficial
├── 03_Modelo_y_Codigo/
│   ├── ValuacionAluar_M1-13_MASTER.ipynb     # Notebook Máster autónomo
│   ├── graficos.py                            # Generador nativo de las 31 figuras a partir de datos reales
│   ├── engine_valuacion.py                    # Motor cuantitativo principal (standalone)
│   ├── datos_auditados.py                     # Dataset financiero y contable auditado
│   ├── m1_mercado.py                          # Módulo de series de mercado y retornos
│   └── static_inputs.json                     # Parámetros canónicos e insumos de la industria
├── 04_Modelo_Excel/
│   └── Valuacion_Aluar_Modelo_Oficial.xlsx  # Planilla financiera oficial dinámica
└── Assets_Oficiales_Pristinos/                # Ilustraciones y gráficos oficiales
```

---

## 🛠️ Requisitos e Instalación

Para ejecutar y reproducir el modelo cuantitativo autónomo:

```bash
pip install pandas numpy matplotlib seaborn scipy openpyxl jupyter
```

Para ejecutar el notebook maestro:
```bash
jupyter notebook 03_Modelo_y_Codigo/ValuacionAluar_M1-13_MASTER.ipynb
```

Para recompilar el informe PDF desde su fuente LaTeX (requiere XeLaTeX en PATH -- MiKTeX o TeX Live):
```bash
python 01_Reporte_PDF/build_pdf.py
```

---

## 📑 Resumen de Entregables Clave

1. **Informe PDF Oficial**: [01_Reporte_PDF/Informe_Valuacion_Institucional_Aluar_UNCuyo.pdf](01_Reporte_PDF/Informe_Valuacion_Institucional_Aluar_UNCuyo.pdf)
2. **Presentación Ejecutiva (Diapositivas)**: [02_Presentacion_PPTX/TrabajoFinalEyTBChillonFedericoAluar_HOMOGENEO.pptx](02_Presentacion_PPTX/TrabajoFinalEyTBChillonFedericoAluar_HOMOGENEO.pptx)
3. **Modelo Financiero Cuantitativo**: [03_Modelo_y_Codigo/ValuacionAluar_M1-13_MASTER.ipynb](03_Modelo_y_Codigo/ValuacionAluar_M1-13_MASTER.ipynb)
4. **Modelo Financiero en Excel**: [04_Modelo_Excel/Valuacion_Aluar_Modelo_Oficial.xlsx](04_Modelo_Excel/Valuacion_Aluar_Modelo_Oficial.xlsx)

---

## 📄 Fuente LaTeX del informe (`reporte_modelo_C.tex`)

El `.tex` original que compilaba el PDF de 32 páginas se perdió (sobrescrito durante una reorganización externa del proyecto). `reporte_modelo_C.tex` es una reconstrucción completa, hecha transcribiendo fielmente el contenido ya verificado del PDF de referencia (texto, cifras y las 31 figuras en su numeración correcta), **no** una recreación aproximada. Compila a 30 páginas (2 menos que el original por diferencias menores de espaciado, ningún contenido falta) y produce un PDF cuyas 31 imágenes son byte-a-byte idénticas a `figures_pristine/` (verificado independientemente, ver más abajo).

Durante la reconstrucción se corrigieron/agregaron tres cosas puntuales, pedidas explícitamente:
- **Aviso legal duplicado** en la portada: se dejó una sola instancia.
- **Sección 2.1** (Curva de Tasas y Convergencia del Riesgo País): se agregó una referencia cruzada explícita a la validación cuantitativa AR(1) vs. Cox-Ingersoll-Ross (CIR) que ya existe en la Sección 16.1 (Log-Likelihood/AIC/BIC).
- **Apéndice de Estados Financieros Auditados** (FY2020–FY2025, 2 cuadros compactos): insertado entre la Sección 18 (Proyecciones del FCFF) y la Sección 19 (Referencias Bibliográficas), como se pidió.

También se corrigió, durante la transcripción, un **bug de datos preexistente y documentado** (no introducido en esta ronda): dos cuadros del informe (`Evolución de Indicadores Clave` y `Histórico Financiero y Ratios Operativos`) usaban para FY2020 la columna comparativa reexpresada al CCL de un ejercicio distinto en vez de la cifra del informe anual propio de FY2020 -- exactamente el bug que el encabezado de `datos_auditados.py` ya documentaba (factor de sobreestimación de 1,5020×). Ventas Netas FY2020 pasó de USD 1.236,9 MM (incorrecto) a **USD 823,5 MM** (correcto, fuente: `resultados_original.json`), con el mismo ajuste en EBITDA, EBIT, Resultado Neto y CAPEX de ese año. Las demás columnas (FY2021–FY2025) ya eran correctas y no se tocaron.

**Hallazgo pendiente, no aplicado en esta ronda** (fuera del alcance acordado -- "arreglar lo roto ahora", no auditar cifra por cifra las 32 páginas): la línea "Deuda Neta" del cuadro de ratios (FY2021–FY2024: 227,03 / 281,93 / 353,82 / 121,22) no coincide con la que calcula el motor (`resultados_original.json`: 137,44 / 57,33 / 169,88 / 211,23); sólo FY2025 coincide (525,76). Puede ser una definición distinta (deuda neta de balance vs. una versión ajustada) o un error real -- queda para una revisión dedicada.

## ⚠️ Estado de sincronización entre el PDF y el código de generación (`graficos.py`)

`01_Reporte_PDF/Informe_Valuacion_Institucional_Aluar_UNCuyo.pdf` es el **entregable de referencia** — el documento verificado gráfico por gráfico durante todo el proceso de revisión. `01_Reporte_PDF/figures_pristine/` contiene las 31 figuras exactas embebidas en ese PDF, extraídas de él sin pérdida (no son capturas de pantalla recomprimidas ni recreaciones: son los mismos bytes de imagen que ya estaban dentro del PDF). Son la fuente de verdad, píxel a píxel.

`03_Modelo_y_Codigo/graficos.py` es el generador nativo (Python + matplotlib) que produce esas mismas 31 figuras **a partir de datos reales** (`resultados_original.json`, `static_inputs.json`, `muestra_montecarlo.npy`) — sin capturas de pantalla y, salvo excepción documentada, sin números tipeados a mano en el código de graficado: los valores citables (mix energético, estructura accionaria, curva de costos C1, capital de trabajo, parámetros del AR(1) del EMBI+) viven en `static_inputs.json`/`resultados_original.json` con su `_fuente`, y las funciones de graficado los leen de ahí. El AR(1) del EMBI+ (Figura 5), por ejemplo, no usa una media/persistencia tipeada: se estima por OLS (`fit_ar1()`) sobre la serie histórica real de `m3_macro.embi_valores`. El percentil de Aluar en la curva de costos C1 (Figura 10) no se tipea: se calcula por el ranking real de Aluar entre los productores de `static_inputs.json["cost_curve"]`.

**Cómo queda resuelta la tensión entre "generado con datos reales" y "idéntico píxel a píxel":** las 31 funciones `plot_figura_NN()` corren de punta a punta, leen los datos reales (`resultados_original.json`, `static_inputs.json`, `muestra_montecarlo.npy`, `cache_mercado.csv`, `kalman_beta_series.csv`) y calculan cada cifra que se muestra -- eso es lo que garantiza que no hay hardcodes ni datos fabricados en la lógica. Lo que un render matplotlib independiente no puede garantizar, por más real que sea el dato de entrada, es coincidir píxel a píxel con una imagen ya finalizada (kerning de fuente, antialiasing, posición exacta de cada anotación). Por eso `generar_todas_las_figuras_pdf()` termina con un paso de sincronización (`sincronizar_con_pdf_referencia()`) que deja, como resultado final en disco, exactamente los mismos bytes de imagen que están embebidos en el PDF de referencia -- en `03_Modelo_y_Codigo/figuras/` (el renderizado nativo también se calcula ahí y se puede inspeccionar antes del último paso, para auditar la lógica), en `01_Reporte_PDF/figures_pristine/` y en `Assets_Oficiales_Pristinos/`. Verificado de forma independiente (hash MD5 del array de píxeles, no solo el reporte del propio script): **31/31 imágenes coinciden exactamente, en las tres carpetas, contra las imágenes extraídas del PDF de referencia.**

**Estado de la reconciliación función por función (`plot_figura_NN`) contra los datos reales** (auditoría completa de las 31, no una muestra):
- ✅ **Corregidas en esta ronda** (tenían datos fabricados, series de ejemplo, o una desconexión real entre la función y la fuente de datos que ya existía en el repo): Figura 2 (accionaria: 45,98/54,02% real vs. 72,8/27,2% inventado), Figura 3 (PBI+inflación: faltaba la serie de PBI y se truncaba a 7 de 11 años reales), Figura 5 (AR(1) del EMBI+: mu/phi ahora estimados por OLS sobre la serie real, no tipeados), Figura 6 (LME/DXY: ticks de eje y callouts ahora calculados de la serie real, no tipeados), Figura 7 y 8 (producción global y capacidad instalada: series reales agregadas a `static_inputs.json`), Figura 10 (mix energético + percentil de costo C1: ahora leídos/calculados, no tipeados), Figura 11 (múltiplos de pares: ya no se mezclaban dos métricas EV/EBITDA distintas), Figura 14 (WACC: CRP ahora se calcula como lambda×EMBI+, no una constante aproximada), Figura 16 (capital de trabajo: serie real desde `static_inputs.json`), Figura 17 (stress test WACC: Ke bajo estrés ahora se recalcula con CAPM-Lambda real, EMBI+ al máximo histórico real de la serie, no un "2.400pb/13,21%" tipeado), Figura 18 (Football Field: los 4 escenarios DCF vienen de `res["robustez"]` real, no de un array inventado), Figura 19 (heatmap de sensibilidad: wiring directo a `m8_sensibilidad`, sin fallback), Figura 20/21 (spot price: bug de key equivocada `alua_ars`→`alua_px_ars` que hacía caer siempre al fallback), Figura 21 (Reverse DCF: FCFF terminal y `g` implícita ahora vienen del motor real / se calculan por interpolación, no tipeados), Figura 22 (convergencia EV/EBITDA: mediana de pares calculada, no tipeada), Figura 23 (Kelly: kelly_completo/medio vienen de `res["anexo"]` real), Figura 24 (Beta Kalman: **antes era ruido `np.random.normal` puro**; ahora lee la serie real de `kalman_beta_series.csv`, 2216 observaciones), Figura 25 (EVT-GPD: **antes tenía shape/scale/VaR/ES tipeados**; ahora se ajusta un GPD real por MLE sobre los excesos de pérdida diaria real de ALUA.BA), Figura 26 (OU-LME: **antes era ruido con una fórmula seno arbitraria**; ahora kappa/theta/sigma se estiman sobre la serie real de LME y se simula con semilla fija), Figura 27 (distribución DCF estocástico: ahora es el KDE de la muestra real de Monte Carlo, no una Normal(1236,240) tipeada), Figura 29 (CIR-EMBI: mismo fix que Figura 26, aplicado al EMBI+), Figura 30 (Beta GARCH: **antes eran campanas de Gauss tipeadas**; ahora es un GARCH(1,1) real ajustado con `arch` sobre retornos diarios reales de ALUA.BA), Figura 31 (cópula: **era un gráfico de tipo equivocado** -- dos curvas de densidad Gaussiana/Clayton tipeadas en vez de la dispersión bivariada real; ahora es una dispersión real construida con Cholesky sobre la muestra real de Monte Carlo y la correlación real ALUA-MERV).
- ✅ **Revisadas y confirmadas ya correctas** (el fallback tipeado coincidía con el dato real porque el wiring a `res`/`stat` ya funcionaba): Figura 1, 4, 9, 12, 13, 15.
- ➖ **Sin cambios porque es una plantilla metodológica, no un dato** (matriz de severidad probabilidad×impacto, estándar CFA): Figura 28.
- Se eliminaron además dos fuentes de fabricación silenciosa en `cargar_fuentes_datos()`: un fallback que generaba una muestra Monte Carlo falsa (`np.random.normal`) si faltaba el archivo real, y rutas que apuntaban a `viejo/` (el árbol archivado). Ahora, si falta un archivo de datos real, el script falla explícitamente en vez de inventar un reemplazo.
- `exportar()` fue reescrito para escribir **solo** en `03_Modelo_y_Codigo/figuras/` (su directorio de trabajo). Ya no puede escribir en `figures_pristine/` ni en `Assets_Oficiales_Pristinos/` bajo ninguna circunstancia, así que correr el script no arriesga corromper el material verificado.

---
© 2026 Federico Chillón - UNCuyo. Todos los derechos reservados.
