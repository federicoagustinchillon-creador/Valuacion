# Valuación Fundamental, Modelos Estocásticos y Econometría Financiera
## Aluar Aluminio Argentino S.A.I.C. (BYMA: ALUA)

**Facultad de Ciencias Económicas — Universidad Nacional de Cuyo (UNCuyo)**  
**Cátedra de Evaluación y Tributación de Bases (EyTB)**  
**Autor:** Federico Agustín Chillón  
**Fecha:** Agosto de 2026  

---

### Resumen Ejecutivo de la Valuación
* **Dictamen del Modelo Teórico:** **COMPRAR**
* **Precio Objetivo Base (DCF Dumrauf):** **ARS 1.236,00** (USD 0,78)
* **Opción Real de Expansión Eólica (PEAL V):** **+ARS 19,60** (USD 0,01)
* **Target Teórico Integrado:** **ARS 1.255,60** (USD 0,79)
* **Cotización de Mercado al Cierre:** **ARS 982,50** | **Retorno Esperado:** **+27,8%**
* **Costo Promedio Ponderado del Capital (WACC):** **7,06%** en USD ($\lambda = 0,20$)

---

### Estructura y Navegación del Repositorio

El repositorio público de entrega comprende **4 módulos temáticos oficiales**:

```
valuacion-aluar-uncuyo/
│
├── 01_Reporte_PDF/
│   ├── Informe_Valuacion_Aluar_UNCuyo.pdf   # Informe Institucional de Valuación (16 páginas exactas, XeLaTeX)
│   └── Informe_Valuacion_Aluar_UNCuyo.docx  # Informe Institucional en Word (16 páginas exactas, paridad 1:1)
│
├── 02_Presentacion_PPTX/
│   └── Presentacion_Valuacion_Aluar_UNCuyo.pptx # Diapositivas ejecutivas institucionales (16:9)
│
├── 03_Modelo_y_Codigo/
│   ├── engine_valuacion.py                  # Motor cuantitativo puro en Python 3.12 (12 módulos analíticos)
│   ├── Modelo_Cuantitativo_Aluar.ipynb      # Jupyter Notebook interactivo con simulaciones y gráficos
│   ├── datos_auditados.py                   # Serie histórica y estados contables auditados
│   ├── graficos.py                          # Generador de figuras de alta resolución (300 DPI)
│   └── figuras/                             # 31 figuras analíticas oficiales del informe
│
├── 04_Modelo_Excel/
│   └── Valuacion_Aluar_Modelo_Oficial.xlsx  # Modelo financiero integral en Excel con DCF dinámico
│
├── CHANGELOG.md                             # Registro de versiones y cambios del proyecto
├── LICENSE                                  # Licencia de uso académico
├── README.md                                # Este documento maestro de navegación
└── requirements.txt                         # Dependencias de Python (NumPy, SciPy, Statsmodels, docx)
```

---

### Síntesis Metodológica

1. **Valuación por Flujos Descontados (FCFF):**
   * Descuento a mitad de período (*Mid-Year Discounting*).
   * Modelo CAPM-$\lambda$ de Damodaran (Dumrauf Cap. 14) con factor de exposición soberana $\lambda = 0,20$.
   * Desapalancamiento y reapalancamiento del Beta por Hamada (1972) con ajuste bayesiano de Marshall Blume ($\beta_L = 0,888$).
2. **Opciones Reales (PEAL V):**
   * Algoritmo de Mínimos Cuadrados Monte Carlo de Longstaff-Schwartz (LSMC) con regresión sobre polinomios ortogonales de Laguerre.
3. **Modelización Estocástica y Simulación:**
   * Proceso de Reversión a la Media de Ornstein-Uhlenbeck para el precio spot del aluminio LME ($t_{1/2} = 3,46$ meses).
   * Proceso Cox-Ingersoll-Ross (CIR) con verificación matemática de la Condición de Feller ($2\kappa\theta > \sigma^2$) para la dinámica de tasas.
4. **Teoría de Cópulas y Dependencia Asimétrica en Caídas:**
   * Cópula de Clayton ($\lambda_L = 0,38$, $\Delta\text{AIC} = -88,9$) para modelar la correlación extrema no lineal entre el commodity y el riesgo soberano.
5. **Gestión Cuantitativa de Riesgo (EVT-GPD):**
   * Modelo Peaks Over Threshold (POT) con Distribución Pareto Generalizada para estimación robusta de VaR 99% (-8,20%) y CVaR 99% (-10,35%).
   * Asignación prudencial de capital bajo el Criterio de *Half-Kelly* ($f = 20,0\%$).

---

### Instrucciones de Reproducibilidad y Ejecución

* **Ejecutar el Motor Cuantitativo Completo:**
  ```bash
  python 03_Modelo_y_Codigo/engine_valuacion.py
  ```
* **Ejecutar el Notebook Interactivo:**
  ```bash
  jupyter notebook 03_Modelo_y_Codigo/Modelo_Cuantitativo_Aluar.ipynb
  ```

---
*Mendoza, República Argentina — Agosto de 2026*
