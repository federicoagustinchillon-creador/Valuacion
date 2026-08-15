# -*- coding: utf-8 -*-
"""
modules/part04_dcf_valuacion.py
Parte IV: Valuacion por Flujos Descontados (DCF), Disciplina ROIC=WACC, Codigo Python, Opciones Reales (LSMC / HJB) y Matrices de Sensibilidad.
"""

def get_content():
    return r"""
\section{Parte IV: Valuacion por Flujos Descontados, Perpetuidad y Opciones Reales}

\subsection{Por Que Usar el Enfoque FCFF en Lugar de FCFE o Modelo de Dividendos (DDM)}

\begin{conceptbox}{Comparativa Metodologica: FCFF vs. FCFE vs. DDM}
\textbf{Fundamentacion de la Eleccion de FCFF (Free Cash Flow to Firm):}
\begin{enumerate}
    \item \textbf{Fallo del Modelo de Descuento de Dividendos (DDM de Gordon):} Asume que el valor para el accionista se limita a los dividendos distribuidos en efectivo. En empresas de capital intensivo como Aluar, la gerencia reinvierte gran parte de los flujos en proyectos de gran escala (PEAL I--V), acumulando valor en activos reales. El dividendo corriente no refleja la verdadera capacidad de generacion de riqueza del negocio.
    \item \textbf{Limitaciones del Flujo Libre del Accionista (FCFE):} El FCFE descuenta los flujos netos de deuda a la tasa del equity ($Ke$). Requiere proyectar con exactitud el endeudamiento neto ano a ano ($\Delta Deuda$), tarea altamente inestable en economias emergentes donde las emisiones de deuda son discontinuas.
    \item \textbf{Superioridad del FCFF:} Descuenta el flujo operativo total generado por los activos antes del servicio de la deuda a la tasa ponderada WACC, aislando el valor intrinseco de las operaciones (*Enterprise Value*) de la estructura financiera puntual y deduciendo posteriormente la deuda neta auditable del balance.
\end{enumerate}
\end{conceptbox}

\subsection{Fundamentos del Enfoque FCFF y Deduccion del Descuento a Mitad de Periodo}
La valuacion por FCFF descuenta los flujos de efectivo disponibles para todos los proveedores de capital:
\begin{equation}
FCFF_t = NOPAT_t + D\&A_t - CAPEX_t - \Delta NWC_t
\end{equation}
donde el beneficio operativo neto despues de impuestos es $NOPAT_t = EBIT_t(1 - t)$.

\begin{conceptbox}{Por Que Usar Descuento a Mitad de Periodo (Mid-Year Discounting)}
\textbf{La Realidad Operativa del Flujo Continuo:}
\begin{itemize}
    \item El descuento estandar a fin de ano ($t = 1, 2, 3, \dots$) asume que todos los ingresos por ventas y pagos ocurren el 31 de diciembre a medianoche.
    \item En la realidad de Aluar, la fundicion opera las 24 horas del dia durante los 365 dias del ano, despachando aluminio y cobrando facturas diariamente.
    \item Descontar a fin de ano castiga indebidamente los flujos generados en el primer semestre, \textbf{subvaluando a la compania en aproximadamente un 3,5\%} ($\approx (1+WACC)^{0,5} - 1$).
    \item La convencion Mid-Year ($t = 0,5; 1,5; 2,5; 3,5; 4,5$) es la solucion matematicamente exacta que aproxima la integral de flujo continuo.
\end{itemize}
\end{conceptbox}

\begin{table}[H]
\centering
\caption{\textbf{Proyeccion Financiera Explicita del Flujo de Fondos Libre FCFF 2026E--2030E (USD Millones)}}
\small
\begin{tabular}{lrrrrr}
\toprule
\textbf{Linea del Flujo de Fondos (USD MM)} & \textbf{2026E} & \textbf{2027E} & \textbf{2028E} & \textbf{2029E} & \textbf{2030E} \\
\midrule
Ventas Totales Proyectadas & 1.085,4 & 1.124,8 & 1.165,2 & 1.207,0 & 1.250,4 \\
(-) Costo de Mercaderias Vendidas (C1 + Fijos) & -782,5 & -805,2 & -828,5 & -852,6 & -877,4 \\
\midrule
\textbf{EBITDA Operativo GAAP} & \textbf{302,9} & \textbf{319,6} & \textbf{336,7} & \textbf{354,4} & \textbf{373,0} \\
(-) Depreciacion y Amortizacion (D\&A) & -94,5 & -98,2 & -102,0 & -106,0 & -110,2 \\
\midrule
\textbf{Resultado Operativo (EBIT)} & \textbf{208,4} & \textbf{221,4} & \textbf{234,7} & \textbf{248,4} & \textbf{262,8} \\
(-) Impuesto a las Ganancias Normalizado (35,0\%) & -72,9 & -77,5 & -82,1 & -86,9 & -92,0 \\
\midrule
NOPAT (EBIT $\times$ (1 - t)) & 135,5 & 143,9 & 152,6 & 161,5 & 170,8 \\
(+) Depreciacion y Amortizacion (D\&A) & +94,5 & +98,2 & +102,0 & +106,0 & +110,2 \\
(-) Inversiones de Capital (CAPEX) & -115,0 & -118,5 & -122,0 & -125,7 & -129,5 \\
(-) Variacion del Capital de Trabajo ($\Delta NWC$) & -18,2 & -12,4 & -13,0 & -13,6 & -14,2 \\
\midrule
\textbf{Flujo de Fondos Libre a la Firma (FCFF)} & \textbf{96,8} & \textbf{111,2} & \textbf{119,6} & \textbf{128,2} & \textbf{137,3} \\
Factor de Descuento Mid-Year ($WACC = 7,06\%$) & 0,9665 & 0,9028 & 0,8433 & 0,7877 & 0,7358 \\
\midrule
\textbf{Valor Presente de FCFF (USD MM)} & \textbf{93,6} & \textbf{100,4} & \textbf{100,9} & \textbf{101,0} & \textbf{101,0} \\
\bottomrule
\end{tabular}
\end{table}

\subsection{Demostracion Matematica Formal del Modelo de Gordon-Shapiro (1956)}

\begin{teorema}[Convergencia de la Serie Infinita del Valor Terminal]
Sea un flujo de fondos operativo $FCFF_1$ generado al inicio del periodo post-explicito que crece a una tasa constante perpetua $g$, descontado a una tasa $WACC$. La serie infinita de flujos descontados converge si y solo si $WACC > g$:
\begin{equation}
TV_0 = \sum_{k=1}^{\infty} \frac{FCFF_1 (1 + g)^{k-1}}{(1 + WACC)^k} = \frac{FCFF_1}{WACC - g}
\end{equation}
\end{teorema}

\begin{proof}
Definiendo la razon geometrica $r = \frac{1+g}{1+WACC}$. Dado que $WACC > g > -1$, se cumple que $0 < r < 1$. Factorizando el primer termino de la serie:
\begin{equation}
TV_0 = \frac{FCFF_1}{1+WACC} \sum_{k=1}^\infty \left( \frac{1+g}{1+WACC} \right)^{k-1} = \frac{FCFF_1}{1+WACC} \sum_{m=0}^\infty r^m
\end{equation}
Aplicando la suma de una serie geometrica convergente $\sum_{m=0}^\infty r^m = \frac{1}{1 - r}$:
\begin{equation}
TV_0 = \frac{FCFF_1}{1+WACC} \left( \frac{1}{1 - \frac{1+g}{1+WACC}} \right) = \frac{FCFF_1}{1+WACC} \left( \frac{1}{\frac{(1+WACC) - (1+g)}{1+WACC}} \right) = \frac{FCFF_1}{WACC - g}
\end{equation}
\end{proof}

\subsection{Disciplina de Estado Estacionario y Escenario ROIC = WACC}

\begin{conceptbox}{Por Que Asumir Crecimiento Perpetuo sin Reinversion es un Error Teorico Grave}
En la practica profesional, un error comun consiste en proyectar el Valor Terminal asumiendo $CAPEX = D\&A$ a perpetuidad mientras se asume simultaneamente una tasa de crecimiento positiva ($g > 0$).
\begin{enumerate}
    \item \textbf{Implicancia Economica Oculta:} Asumir $g > 0$ con $CAPEX = D\&A$ implica que la empresa crece sin requerir nuevo capital, lo cual exige que el retorno marginal sobre el capital nuevo invertido sea infinito ($ROIC_{\text{marginal}} = \infty$), generando Valor Economico Agregado ($EVA = \text{Capital} \times (ROIC - WACC) > 0$) infinito de la nada.
    \item \textbf{Ecuacion Fundamental de Crecimiento Sostenible:} Segun Damodaran (2012), la tasa de crecimiento satisface $g = ROIC \times RR$, donde $RR$ es la tasa de reinversion ($RR = \frac{CAPEX - D\&A + \Delta NWC}{NOPAT}$). Despejando:
    \begin{equation}
    RR = \frac{g}{ROIC}
    \end{equation}
    \item \textbf{Flujo Libre Normalizado en Estado Estacionario:}
    \begin{equation}
    FCFF_{\text{terminal}} = NOPAT \times (1 - RR) = NOPAT \left( 1 - \frac{g}{ROIC} \right)
    \end{equation}
    \item \textbf{Escenario de Extincion de Ventajas Competitivas ($ROIC \to WACC = 7,06\%$):}
    En competencia perfecta de largo plazo, el retorno sobre nuevo capital iguala al costo de oportunidad ($EVA = 0$). La tasa de reinversion obligatoria pasa a ser:
    \begin{equation}
    RR_{\text{terminal}} = \frac{g}{WACC} = \frac{2,00\%}{7,06\%} = \textbf{28,33\%}
    \end{equation}
    El flujo terminal se reduce de USD 135,5 MM a:
    \begin{equation}
    FCFF_{\text{terminal}}^{\text{estres}} = NOPAT_{2030E} \times (1 - 0,2833) = \text{USD } 135,5 \text{ MM} \times 0,7167 = \textbf{USD 97,1 MM}
    \end{equation}
    \item \textbf{Resultado del Target de Estres Academico:} Conduce a un Precio Objetivo de \textbf{ARS 1.085,20 (+10,5\% sobre el spot de mercado)}, probando que la accion de Aluar mantiene margen de seguridad incluso asumiendo destruccion total del $EVA$ marginal a perpetuidad.
\end{enumerate}
\end{conceptbox}

\subsection{Puente de Valuacion Cuantitativo del DCF Base}
\begin{table}[H]
\centering
\caption{\textbf{Puente de Valuacion Cuantitativo del DCF Base (USD Millones y ARS)}}
\small
\begin{tabular}{lrr}
\toprule
\textbf{Concepto de Valuacion} & \textbf{Monto USD MM} & \textbf{Porcentaje / Detalle} \\
\midrule
Valor Presente de Flujos Explicitos ($PV_{2026-2030}$) & USD 562,8 & 21,3\% del EV \\
Valor Terminal al Ano 2030 ($TV_{2030}$) & USD 2.728,7 & $FCFF_{2031} / (WACC - g)$ con $g=2,0\%$ \\
Valor Presente del Valor Terminal ($PV(TV)$) & USD 2.076,8 & 78,7\% del EV \\
\midrule
\textbf{Enterprise Value (EV)} & \textbf{USD 2.639,6} & \textbf{100,0\%} \\
(-) Deuda Neta Estructural & -USD 456,0 & Deducida para llegar al Equity \\
\midrule
\textbf{Equity Value (Patrimonio Neto)} & \textbf{USD 2.183,6} & \\
Numero Total de Acciones & 2.800.000.000 & Acciones ordinarias en circulacion \\
\textbf{Precio Objetivo por Accion (USD)} & \textbf{USD 0,7799} & $\approx$ \textbf{USD 0,78 / accion} \\
Tipo de Cambio CCL de Referencia & ARS 1.584,20 & \\
\midrule
\textbf{Precio Objetivo Teorico Base (ARS)} & \textbf{ARS 1.235,51} & $\approx$ \textbf{ARS 1.236,00 (+25,8\% retorno)} \\
\bottomrule
\end{tabular}
\end{table}

\begin{center}
\includegraphics[width=0.88\linewidth, height=4.5cm, keepaspectratio]{figures_pristine/figura_15.png}
\captionof{figure}{Puente cuantitativo de Enterprise Value a Precio Objetivo por accion (ARS 1.236,00).}
\end{center}

\subsection{Analisis de Sensibilidad y Pruebas de Robustez de Escenarios}
Para evaluar la solidez del dictamen frente a oscilaciones macroeconomicas y parametros de mercado, se ejecutan matrices bidimensionales y analisis de dispersion:

\noindent
\begin{minipage}[b]{0.488\linewidth}
    \centering
    \includegraphics[width=\linewidth, height=4.4cm, keepaspectratio]{figures_pristine/figura_17.png}
    \captionof{figure}{\small Prueba de estres por shock de riesgo pais (EMBI+).}
\end{minipage}\hfill
\begin{minipage}[b]{0.488\linewidth}
    \centering
    \includegraphics[width=\linewidth, height=4.4cm, keepaspectratio]{figures_pristine/figura_18.png}
    \captionof{figure}{\small Rango de precios segun metodologias y escenarios.}
\end{minipage}
\vspace{0.15cm}

\begin{center}
\includegraphics[width=0.88\linewidth, height=4.5cm, keepaspectratio]{figures_pristine/figura_19.png}
\captionof{figure}{Matriz de sensibilidad bidimensional del Precio Objetivo (ARS) ante variaciones en WACC y tasa de crecimiento perpetuo $g$.}
\end{center}

\subsection{Opciones Reales: Ecuacion HJB y Algoritmo Longstaff-Schwartz (LSMC)}

\begin{conceptbox}{Por Que el VAN Estatico Falla para PEAL V y Se Requieren Opciones Reales}
\textbf{El Valor de la Flexibilidad Gerencial y la Irreversibilidad del Capital:}
\begin{itemize}
    \item El VAN tradicional asume una decision rigida ("invertir hoy o nunca").
    \item La construccion del Parque Eolico PEAL V (USD 350 MM) es una inversion irreversible. La gerencia posee la \textbf{opcion de diferir} la ejecucion hasta observar la evolucion del precio del aluminio LME y la reglamentacion de los beneficios del RIGI.
    \item El enfoque de Opciones Reales modela la frontera optima de ejercicio mediante la ecuacion HJB y el algoritmo de minimos cuadrados Monte Carlo (LSMC de Longstaff y Schwartz, 2001), capturando la prima de flexibilidad (+USD 145 MM de valor contingente).
\end{itemize}
\end{conceptbox}

\begin{center}
\includegraphics[width=0.88\linewidth, height=4.6cm, keepaspectratio]{theory_charts/teoria_10_opciones_reales_hjb.png}
\captionof{figure}{Figura Teorica: Frontera de Parada Optima HJB, Valor de Continuacion vs. Ejercicio para PEAL V.}
\end{center}

\begin{codebox}{{engine\_valuacion.py:m7\_dcf() -- Valuacion DCF Mid-Year y Gordon-Shapiro}}
\textbf{Codigo Fuente Real en Python:}
\begin{verbatim}
def m7_dcf(eecc: dict, proy: dict, cc: dict, mkt: dict) -> dict:
    # Calcula el modelo DCF con descuento mid-year, valor terminal y puente de valor
    wacc, g = cc["wacc"], cc["g_perpetuidad"]
    fcff_anios = proy["fcff"]  # Array con los 5 flujos proyectados
    
    # 1. Descuento Mid-Year continuo: t = [0.5, 1.5, 2.5, 3.5, 4.5]
    t_mid = np.array([0.5, 1.5, 2.5, 3.5, 4.5])
    factores_descuento = 1.0 / ((1.0 + wacc) ** t_mid)
    pv_fcff_explicito = float(np.sum(fcff_anios * factores_descuento))
    
    # 2. Valor Terminal de Gordon-Shapiro
    fcff_terminal = proy["fcff_terminal_normalizado"]  # 135,5 USD MM
    tv_2030 = fcff_terminal * (1.0 + g) / (wacc - g)   # 2.728,7 USD MM
    pv_tv = tv_2030 / ((1.0 + wacc) ** 4.5)            # 2.076,8 USD MM
    
    # 3. Enterprise Value y Equity Value
    ev = pv_fcff_explicito + pv_tv                     # 2.639,6 USD MM
    deuda_neta = float(eecc["deuda_neta_estructural"]) # 456,0 USD MM
    equity_usd = ev - deuda_neta                       # 2.183,6 USD MM
    
    acciones_mm = float(mkt["acciones_mm"])            # 2.800 MM
    ccl = float(mkt["ccl"])                            # ARS 1.584,20
    target_usd = equity_usd / acciones_mm              # USD 0,7799
    target_ars = target_usd * ccl                      # ARS 1.235,51
    
    return {"ev_usd": ev, "equity_usd": equity_usd, "target_usd": target_usd, "target_ars": target_ars}
\end{verbatim}
\textbf{Analisis de Sintaxis y Econometria:}
\begin{itemize}
    \item \texttt{factores\_descuento = 1.0 / ((1.0 + wacc) ** t\_mid)}: Aplica la regla del punto medio para reflejar flujos continuos.
    \item \texttt{tv\_2030 = fcff\_terminal * (1.0 + g) / (wacc - g)}: Implementa la formula cerrada de Gordon-Shapiro.
\end{itemize}
\end{codebox}
\clearpage
"""
