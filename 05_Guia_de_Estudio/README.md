# Guía de Estudio y Tratado de Valuación: Aluar S.A.I.C.

**Documento Maestro Descargable para Estudio:**
📄 **[Descargar / Ver GUIA_DE_ESTUDIO_ALUAR.pdf](./GUIA_DE_ESTUDIO_ALUAR.pdf)** *(51 páginas, compilado institucional en XeLaTeX con 31 figuras y 10 esquemas teóricos)*

---

## Estructura de Contenidos por Módulo

| Módulo | Título y Eje Temático | Conceptos Clave y Demostraciones |
| :--- | :--- | :--- |
| **Parte I** | **Análisis Estratégico, Termodinámica e Industria** | Proceso Bayer, Hall-Héroult, Ley de Faraday, Cash Cost C1 (P18%, USD 1.680/t), riesgo de congelamiento de cubas a 960°C, 5 Fuerzas de Porter, ventaja CBAM europeo (+USD 983/t). |
| **Parte II** | **Diagnóstico Contable Forense y Normalización IFRS** | Estados FY21-FY25 en USD, DuPont 5 factores, colapso de Tax Burden (84,3% tasa efectiva por Ley 27.468 / NIC 29), Sloan Accrual Ratio (-0,064), CCC 64 días (120 días stock de alúmina), modelos Baumol-Tobin y Miller-Orr. |
| **Parte III** | **Costo de Capital (WACC) y Macroeconomía** | PBI vs. Inflación, EMBI+ AR(1), CAPM-$\lambda$ de Damodaran ($\lambda=0,20$), demostración Modigliani-Miller con impuestos, Hamada vs. Miles-Ezzell vs. Harris-Pringle, ajuste Blume ($\beta_L = 0,888$), WACC 7,06%. |
| **Parte IV** | **Valuación DCF y Opciones Reales** | FCFF vs. FCFE vs. DDM, integral de descuento Mid-Year ($t=0,5; 1,5; \dots$), demostración Gordon-Shapiro, disciplina de reinversión $ROIC=WACC$ ($RR=28,33\%$), puente de valuación a Target Base ARS 1.236,00, opciones reales PEAL V (HJB / LSMC, +ARS 19,60). |
| **Parte V** | **Modelos Estocásticos, Cópulas y Difusiones de Itô** | Proyecciones QR de Hilbert, teorema Frisch-Waugh-Lovell (FWL), Cholesky, teorema de Sklar, Cópula de Clayton ($\lambda_L=0,38$), reversión a la media Ornstein-Uhlenbeck (LME), difusión CIR y condición de Feller ($2\kappa\theta \ge \sigma^2$), Monte Carlo Student-t ($\nu=4,2$). |
| **Parte VI** | **Gestión de Riesgo Extremo (EVT-GPD), Merton y Kelly** | Axiomas de Artzner, no subaditividad del VaR vs. convexidad del Expected Shortfall (CVaR), teorema Pickands-Balkema-de Haan (GPD POT, $VaR_{99\%} = -10,44\%$, $ES_{99\%} = -15,78\%$), quiebre Cornish-Fisher para $K>6$, modelo estructural de Merton ($DD = 8,23\sigma$), asignación Half-Kelly (53,5%, tope 20%). |
| **Parte VII** | **Valuación Relativa y Teoría de Portafolio** | Comparables globales (EV/EBITDA vs. Margen Peers), optimización Markowitz (KKT orlada), modelo Black-Litterman (Prior $\Pi$, Views $P\mu=q$, Posterior $\mu_{BL}$), teorema de Euler de descomposición de riesgo ($\sum CCR_i = 100\%$). |
| **Parte VIII** | **Econometría de Series de Tiempo y Diagnóstico** | Dinámica LME vs. DXY, espectro SVD/PCA (83,2% varianza), Filtro de Kalman para beta dinámico en espacio de estados, ecuaciones ARMA Yule-Walker, raíz unitaria ADF, rechazo cointegración Engle-Granger, volatilidad GARCH(1,1)-t. |
| **Parte IX** | **Arquitectura de Software Cuantitativo** | Pipeline determinista sin I/O en motor analítico, single source of truth `static_inputs.json`, vectorización en memoria contigua C (BLAS/LAPACK), automatización COM Office. |
| **Parte X** | **Marco Regulatorio (RIGI, CBAM y MATER)** | 5 pilares RIGI (Ley 27.742): alícuota 25%, amortización acelerada en 2 años (art. 182), devolución IVA en 3 meses, 0% aranceles, libre disponibilidad de divisas $\to$ Target RIGI ARS 1.304,10 (+32,8%). MATER renovable. |
| **Parte XI** | **Banco Maestro de 35 Preguntas de Examen** | 35 preguntas y respuestas rigurosas para defensa oral y mesa de examen. |
| **Parte XII** | **Bibliografía Comentada** | 17 referencias fundamentales desde Markowitz (1952) hasta Damodaran (2012). |

---

## Compilación Local

Para compilar el PDF a partir del código fuente LaTeX modular:
```bash
python build_master_encyclopedia.py
```
*Genera `GUIA_DE_ESTUDIO_ALUAR.tex` y compila `GUIA_DE_ESTUDIO_ALUAR.pdf` mediante 2 pasadas de XeLaTeX.*
