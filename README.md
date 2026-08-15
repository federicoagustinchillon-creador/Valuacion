# Valuación de Aluar Aluminio Argentino S.A.I.C. (BCBA: ALUA)

**Trabajo Final de Grado / Evaluación Curricular**  
*Cátedra de Economía y Técnica Bursátil — Facultad de Ciencias Económicas*  
*Universidad Nacional de Cuyo (UNCuyo)*  
**Autor:** Federico Agustín Chillón  

---

## Descripción del Proyecto

Este repositorio contiene la valuación financiera y el análisis cuantitativo de **Aluar Aluminio Argentino S.A.I.C. (BCBA: ALUA)**. El trabajo integra finanzas corporativas, valuación por descuento de flujos de fondos, econometría de series temporales y teoría de portafolios con modelización en Python y Excel.

### Metodología Aplicada

- **Flujos de Fondos Descontados (DCF)**: Proyección operativa explícita (2026E–2030E) y cálculo del Valor Terminal modelando costos de alúmina, precios LME, matriz energética autogenerada y capacidad física instalada (460.000 t).
- **Costo de Capital (WACC)**: Estimación del costo del patrimonio neto ($K_e$) mediante CAPM con prima de riesgo soberano ponderada por ingresos domésticos ($\lambda \times \text{EMBI+}$, $\lambda=0,20$) y desapalancamiento/reapalancamiento de betas (Hamada).
- **Simulación Monte Carlo**: Evaluación probabilística del precio objetivo con 10.000 iteraciones estocásticas considerando incertidumbre en commodities, tipo de cambio e inflación.
- **Gestión Cuantitativa de Riesgo**: Modelización de colas mediante Value at Risk (VaR), Conditional VaR (CVaR) y Teoría de Valores Extremos (EVT - Generalized Pareto Distribution).
- **Valuación por Múltiplos**: Comparativa sectorial con productores globales de aluminio (EV/EBITDA, Margen EBITDA, Deuda Neta/EBITDA).
- **Reverse DCF y Sensibilidad**: Descomposición de las tasas de crecimiento implícitas en el precio de mercado y matrices bidimensionales (WACC vs. $g$).

### Resultados del Modelo Teórico

- **Precio Objetivo Teórico Base**: **ARS 1.236,00** por acción (USD 0,78 / cotización spot: ARS 982,50 / +25,8% de retorno esperado).
- **Precio Objetivo Teórico Integrado (con Opción Real PEAL V)**: **ARS 1.255,60** por acción (+27,8% de retorno esperado).
- **Dictamen del Modelo Teórico**: **COMPRAR**.
- *Aviso*: Este trabajo fue elaborado con fines exclusivamente académicos y no constituye una oferta, recomendación ni asesoramiento financiero.

---

## Estructura del Repositorio

```text
valuacion-aluar-uncuyo/
├── README.md                                   # Presentación y documentación del proyecto
├── LICENSE                                      # Términos de uso académico
├── CHANGELOG.md                                 # Historial de versiones y entregables
├── requirements.txt                             # Dependencias de Python fijadas por versión
├── 01_Reporte_PDF/
│   ├── Informe_Valuacion_Aluar_UNCuyo.pdf       # Informe ejecutivo final (30 páginas)
│   ├── build_pdf.py                             # Script de compilación XeLaTeX (3 pasadas)
│   └── tex/
│       └── reporte_valuacion.tex                # Código fuente LaTeX del informe
├── 02_Presentacion_PPTX/
│   └── TrabajoFinalEyTBChillonFedericoAluar_HOMOGENEO.pptx  # Presentación de diapositivas
├── 03_Modelo_y_Codigo/
│   ├── ValuacionAluar_M1-13_MASTER.ipynb        # Notebook interactivo consolidado (M1 a M13)
│   ├── engine_valuacion.py                      # Motor de cálculo cuantitativo standalone
│   ├── datos_auditados.py                       # Base de datos financieros auditados (FY2020–FY2025)
│   ├── graficos.py                              # Generador de las 31 figuras del informe
│   ├── m1_mercado.py                            # Ingesta y homogenización de series de mercado (CCL/USD)
│   ├── static_inputs.json                       # Parámetros macroeconómicos y de la industria
│   ├── resultados_original.json                 # Resultados persistidos del motor de cálculo
│   ├── cache_mercado.csv                        # Serie histórica de mercado congelada (2016–2026)
│   ├── kalman_beta_series.csv                   # Serie estimada de beta dinámico
│   ├── muestra_montecarlo.npy                   # Muestra estocástica de Monte Carlo (10k iteraciones)
│   └── figuras/                                 # 31 figuras en formato PNG y PDF
├── 04_Modelo_Excel/
│   └── Valuacion_Aluar_Modelo_Oficial.xlsx      # Planilla financiera con fórmulas dinámicas
└── 05_Guia_de_Estudio/
    ├── GUIA_DE_ESTUDIO_ALUAR.pdf                # Guía y tratado de estudio integral (51 páginas)
    ├── GUIA_DE_ESTUDIO_ALUAR.tex                # Código fuente LaTeX modular
    ├── build_master_encyclopedia.py             # Script de compilación XeLaTeX de la guía
    ├── README.md                                # Índice temático y mapa de estudio móvil
    ├── modules/                                 # 12 módulos analíticos de teoría y demostraciones
    └── theory_charts/                           # 10 diagramas teóricos conceptuales
```

---

## Requisitos e Instalación

Para instalar las dependencias de Python:

```bash
pip install -r requirements.txt
```

### Ejecución del Notebook Maestro

```bash
jupyter notebook 03_Modelo_y_Codigo/ValuacionAluar_M1-13_MASTER.ipynb
```

### Ejecución del Motor de Cálculo

```bash
python 03_Modelo_y_Codigo/engine_valuacion.py
```

### Generación de Figuras

```bash
python 03_Modelo_y_Codigo/graficos.py
```

### Compilación del Informe PDF

Para compilar el informe desde la fuente LaTeX (requiere XeLaTeX y tipografía Georgia):

```bash
python 01_Reporte_PDF/build_pdf.py
```

---

## Entregables Principales

1. **Informe PDF**: [01_Reporte_PDF/Informe_Valuacion_Aluar_UNCuyo.pdf](01_Reporte_PDF/Informe_Valuacion_Aluar_UNCuyo.pdf)
2. **Presentación (PPTX)**: [02_Presentacion_PPTX/TrabajoFinalEyTBChillonFedericoAluar_HOMOGENEO.pptx](02_Presentacion_PPTX/TrabajoFinalEyTBChillonFedericoAluar_HOMOGENEO.pptx)
3. **Modelo en Notebook**: [03_Modelo_y_Codigo/ValuacionAluar_M1-13_MASTER.ipynb](03_Modelo_y_Codigo/ValuacionAluar_M1-13_MASTER.ipynb)
4. **Modelo en Excel**: [04_Modelo_Excel/Valuacion_Aluar_Modelo_Oficial.xlsx](04_Modelo_Excel/Valuacion_Aluar_Modelo_Oficial.xlsx)

---

## Fuentes de Información

- **Estados Contables y Memorias Anuales de Aluar (2020–2025)**: Comisión Nacional de Valores (CNV) y Bolsas y Mercados Argentinos (BYMA).
- **Mercado y Tasas**: J.P. Morgan (EMBI+), NYU Stern / Damodaran (ERP & Betas), CBOE (US 10-Year Treasury Yield), London Metal Exchange (LME Aluminium Spot & Futures).
- **Industria**: International Aluminium Institute (IAI) y reportes financieros de pares internacionales.

---

© 2026 Federico Agustín Chillón — UNCuyo. Ver [LICENSE](LICENSE).
