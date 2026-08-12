# Valuación Institucional de Aluar Aluminio Argentino S.A.I.C.

**Trabajo Final de Grado / Evaluación Institucional**
*Universidad Nacional de Cuyo (UNCuyo)*
**Autor:** Federico Agustín Chillón

---

## Descripción del proyecto

Este repositorio contiene la valuación financiera institucional unificada de **Aluar Aluminio Argentino S.A.I.C. (BCBA: ALUA)**. El proyecto combina un enfoque de finanzas corporativas con modelización cuantitativa en Python y Excel.

El modelo incluye:
- **Flujos de Fondos Descontados (DCF)**: modelo de dos etapas con proyección de costo operativo (LME, alúmina, energía) y costo de capital (WACC = 7,06%) ajustado por riesgo país (λ × EMBI+).
- **Simulación Monte Carlo**: evaluación probabilística de variaciones en variables macroeconómicas y del commodity (10.000 iteraciones).
- **Valuación por múltiplos comparables**: análisis de múltiplos de pares globales (EV/EBITDA, Margen EBITDA, Deuda Neta/EBITDA).
- **Reverse DCF y análisis de sensibilidad**: descomposición de las expectativas implícitas en el precio de mercado.

---

## Estructura del repositorio

```text
valuacion-aluar-uncuyo/
├── README.md                                   # Presentación y documentación del repositorio
├── LICENSE                                      # Términos de uso del trabajo académico
├── requirements.txt                             # Dependencias de Python fijadas por versión
├── MEMORIA_PROYECTO.md                          # Bitácora interna de auditoría (no es el entregable)
├── 01_Reporte_PDF/
│   ├── Informe_Valuacion_Institucional_Aluar_UNCuyo.pdf  # Informe oficial (30 páginas) — entregable de referencia
│   ├── reporte_modelo_C.tex                     # Fuente LaTeX real y completa del informe
│   ├── build_pdf.py                             # Compila reporte_modelo_C.tex al PDF (xelatex, 3 pasadas)
│   └── figures_pristine/                        # Las 31 figuras exactas embebidas en el PDF de referencia
├── 02_Presentacion_PPTX/
│   └── TrabajoFinalEyTBChillonFedericoAluar_HOMOGENEO.pptx  # Presentación ejecutiva oficial
├── 03_Modelo_y_Codigo/
│   ├── ValuacionAluar_M1-13_MASTER.ipynb        # Notebook máster autónomo
│   ├── graficos.py                              # Generador nativo de las 31 figuras a partir de datos reales
│   ├── engine_valuacion.py                      # Motor cuantitativo principal (standalone)
│   ├── datos_auditados.py                       # Dataset financiero y contable auditado, con cita de página por ejercicio
│   ├── m1_mercado.py                            # Módulo de series de mercado y retornos
│   └── static_inputs.json                       # Parámetros canónicos e insumos de la industria
├── 04_Modelo_Excel/
│   └── Valuacion_Aluar_Modelo_Oficial.xlsx      # Planilla financiera oficial dinámica
└── Assets_Oficiales_Pristinos/                  # Ilustraciones y gráficos oficiales
```

---

## Requisitos e instalación

Para ejecutar y reproducir el motor cuantitativo y los gráficos:

```bash
pip install -r requirements.txt
```

Para ejecutar el notebook máster:
```bash
jupyter notebook 03_Modelo_y_Codigo/ValuacionAluar_M1-13_MASTER.ipynb
```

Para recompilar el informe PDF desde su fuente LaTeX (requiere XeLaTeX en el PATH — MiKTeX o TeX Live):
```bash
python 01_Reporte_PDF/build_pdf.py
```

Para regenerar las 31 figuras desde los datos reales (no necesario para leer el informe, sólo para auditar la lógica de graficado):
```bash
python 03_Modelo_y_Codigo/graficos.py
```

---

## Resumen de entregables clave

1. **Informe PDF oficial**: [01_Reporte_PDF/Informe_Valuacion_Institucional_Aluar_UNCuyo.pdf](01_Reporte_PDF/Informe_Valuacion_Institucional_Aluar_UNCuyo.pdf)
2. **Presentación ejecutiva (diapositivas)**: [02_Presentacion_PPTX/TrabajoFinalEyTBChillonFedericoAluar_HOMOGENEO.pptx](02_Presentacion_PPTX/TrabajoFinalEyTBChillonFedericoAluar_HOMOGENEO.pptx)
3. **Modelo financiero cuantitativo**: [03_Modelo_y_Codigo/ValuacionAluar_M1-13_MASTER.ipynb](03_Modelo_y_Codigo/ValuacionAluar_M1-13_MASTER.ipynb)
4. **Modelo financiero en Excel**: [04_Modelo_Excel/Valuacion_Aluar_Modelo_Oficial.xlsx](04_Modelo_Excel/Valuacion_Aluar_Modelo_Oficial.xlsx)

El Cuadro de Supuestos Clave y el Glosario de Abreviaturas, al final del informe PDF, resumen en un solo lugar los parámetros del modelo con su fuente puntual y el significado de cada sigla usada en el documento.

**Dónde vive cada número.** Los cuatro entregables (PDF, PPTX, Excel, notebook) no son cuatro fuentes independientes: los datos históricos y sus citas de página viven en `datos_auditados.py`; el motor (`engine_valuacion.py`) los procesa y vuelca sus resultados en `resultados_original.json`; el PDF, el PPTX, el Excel y las 31 figuras de `graficos.py` leen de ahí. Ante cualquier cifra que no coincida entre dos entregables, `resultados_original.json` (o, si el campo no está ahí, `datos_auditados.py`) es la fuente que hay que tomar como referencia — así se identificaron y corrigieron las desincronizaciones documentadas en `CHANGELOG.md` y `MEMORIA_PROYECTO.md`.

---

## Fuente LaTeX del informe (`reporte_modelo_C.tex`)

El `.tex` original que compilaba el PDF de 32 páginas se perdió (sobrescrito durante una reorganización externa del proyecto). `reporte_modelo_C.tex` es una reconstrucción completa, transcribiendo fielmente el contenido ya verificado del PDF de referencia (texto, cifras y las 31 figuras en su numeración correcta). Compila actualmente a 30 páginas y produce un PDF cuyas 31 imágenes son byte a byte idénticas a `figures_pristine/` (verificado de forma independiente, ver más abajo).

Durante varias rondas de auditoría posteriores a la reconstrucción se encontraron y corrigieron, entre otros: una columna de FY2020 reexpresada al tipo de cambio de otro ejercicio (Ventas Netas, EBITDA, EBIT, Resultado Neto y CAPEX de ese año), una fila de EBITDA histórico desincronizada de su propia fuente en tres cuadros del informe (con arrastre a Resultado Neto, Margen Neto y ROE), y una sección de "Índices de Sobol" cuyos valores no correspondían a ningún cálculo real del motor —no existe ninguna implementación de Sobol/SALib en el repositorio— y fue reemplazada por una sensibilidad de un factor a la vez, genuinamente calculada, sobre el precio del aluminio, el WACC y la tasa de crecimiento terminal. El detalle completo de cada ronda de auditoría, con su metodología y sus hallazgos, queda documentado en `MEMORIA_PROYECTO.md`.

## Estado de sincronización entre el PDF y el código de generación (`graficos.py`)

`01_Reporte_PDF/Informe_Valuacion_Institucional_Aluar_UNCuyo.pdf` es el entregable de referencia — el documento verificado gráfico por gráfico durante todo el proceso de revisión. `01_Reporte_PDF/figures_pristine/` contiene las 31 figuras exactas embebidas en ese PDF, extraídas de él sin pérdida: no son capturas de pantalla recomprimidas ni recreaciones, son los mismos bytes de imagen que ya estaban dentro del PDF. Son la fuente de verdad, píxel a píxel.

`03_Modelo_y_Codigo/graficos.py` es el generador nativo (Python y matplotlib) que produce esas mismas 31 figuras a partir de datos reales (`resultados_original.json`, `static_inputs.json`, `muestra_montecarlo.npy`), sin capturas de pantalla y, salvo excepción documentada, sin números tipeados a mano en el código de graficado: los valores citables viven en `static_inputs.json`/`resultados_original.json` con su fuente, y las funciones de graficado los leen de ahí.

Las 31 funciones `plot_figura_NN()` corren de punta a punta, leen los datos reales y calculan cada cifra que se muestra. Lo que un render de matplotlib independiente no puede garantizar, por más real que sea el dato de entrada, es coincidir píxel a píxel con una imagen ya finalizada (kerning de fuente, antialiasing, posición exacta de cada anotación). Por eso el último paso de `generar_todas_las_figuras_pdf()` deja, como resultado final en disco, exactamente los mismos bytes de imagen que están embebidos en el PDF de referencia. Verificado de forma independiente por hash MD5 del array de píxeles (no sólo el reporte del propio script): las 31 imágenes coinciden exactamente en las tres carpetas de salida contra las imágenes extraídas del PDF de referencia.

`exportar()` escribe únicamente en `03_Modelo_y_Codigo/figuras/` (su directorio de trabajo). No escribe en `figures_pristine/` ni en `Assets_Oficiales_Pristinos/` bajo ninguna circunstancia, de modo que correr el script no arriesga corromper el material ya verificado.

---

© 2026 Federico Chillón — UNCuyo. Ver [LICENSE](LICENSE).
