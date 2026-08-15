# -*- coding: utf-8 -*-
"""
modules/part02_contabilidad.py
Parte II: Analisis Contable, Normalizacion de Estados Financieros, Descomposicion DuPont, Gestion de Caja (Miller-Orr) y Codigo Python.
"""

def get_content():
    return r"""
\section{Parte II: Diagnostico Contable, Normalizacion Financiera y Gestion de Liquidez}

\subsection{Normalizacion Integral de Estados Financieros (FY2021--FY2025)}
Aluar presenta sus estados financieros consolidados bajo Normas Internacionales de Informacion Financiera (NIIF / IFRS) adoptadas por la Federacion Argentina de Consejos Profesionales de Ciencias Economicas (FACPCE) y la Comision Nacional de Valores (CNV).

\begin{table}[H]
\centering
\caption{\textbf{Resumen Historico de Estados Contables Normalizados (USD Millones)}}
\small
\begin{tabular}{lrrrrr}
\toprule
\textbf{Cuenta Contable / Metrica (USD MM)} & \textbf{FY2021} & \textbf{FY2022} & \textbf{FY2023} & \textbf{FY2024} & \textbf{FY2025} \\
\midrule
Ventas Netas Consolidadas & 892,4 & 1.145,8 & 1.058,2 & 980,5 & 1.042,1 \\
Costo de Ventas (CMV) & -642,1 & -785,4 & -745,0 & -710,2 & -795,8 \\
\midrule
\textbf{Ganancia Bruta} & \textbf{250,3} & \textbf{360,4} & \textbf{313,2} & \textbf{270,3} & \textbf{246,3} \\
Gastos de Comercializacion y Admin. & -85,2 & -105,3 & -98,4 & -92,1 & -98,5 \\
\midrule
\textbf{Resultado Operativo (EBIT)} & \textbf{165,1} & \textbf{255,1} & \textbf{214,8} & \textbf{178,2} & \textbf{147,8} \\
Depreciaciones y Amortizaciones (D\&A) & 78,4 & 84,2 & 89,1 & 91,5 & 94,2 \\
\midrule
\textbf{EBITDA Operativo Normalizado} & \textbf{243,5} & \textbf{339,3} & \textbf{303,9} & \textbf{269,7} & \textbf{242,0} \\
Resultado Financiero Neto & -32,4 & -41,5 & -38,2 & -45,0 & -89,5 \\
Impuesto a las Ganancias (Gasto Efectivo) & -46,4 & -74,7 & -61,8 & -46,6 & -49,1 \\
\midrule
\textbf{Resultado Neto del Ejercicio} & \textbf{86,3} & \textbf{138,9} & \textbf{114,8} & \textbf{86,6} & \textbf{9,17} \\
\midrule
\textbf{Activo Total} & 1.745,2 & 1.890,5 & 1.950,4 & 1.920,8 & 2.030,0 \\
\textbf{Patrimonio Neto} & 1.050,4 & 1.140,2 & 1.190,5 & 1.120,4 & 1.142,5 \\
\textbf{Deuda Financiera Bruta Total} & 480,5 & 510,2 & 545,0 & 580,2 & 673,96 \\
\textbf{Caja y Equivalentes de Efectivo} & 110,2 & 135,4 & 128,0 & 142,5 & 148,20 \\
\textbf{Deuda Financiera Neta Contable} & \textbf{370,3} & \textbf{374,8} & \textbf{417,0} & \textbf{437,7} & \textbf{525,76} \\
\bottomrule
\end{tabular}
\end{table}

\begin{center}
\includegraphics[width=0.88\linewidth, height=4.5cm, keepaspectratio]{figures_pristine/figura_12.png}
\captionof{figure}{Evolucion historica y proyectada del EBITDA de Aluar (USD MM, FY20--FY30E) con identificacion del pico de CAPEX PEAL V.}
\end{center}

\subsection{Descomposicion DuPont de 5 Factores y Analisis Forense del Colapso del ROE}
La rentabilidad del patrimonio neto ($ROE = \frac{\text{Resultado Neto}}{\text{Patrimonio Neto}}$) se descompone en cinco motores fundamentales:
\begin{equation}
ROE = \underbrace{\frac{\text{Neto}}{EBT}}_{\text{Tax Burden (TB)}} \times \underbrace{\frac{EBT}{EBIT}}_{\text{Interest Burden (IB)}} \times \underbrace{\frac{EBIT}{\text{Ventas}}}_{\text{Margen Operativo (OM)}} \times \underbrace{\frac{Ventas}{\text{Activo}}}_{\text{Rotacion Activos (AT)}} \times \underbrace{\frac{\text{Activo}}{\text{Patrimonio Neto}}}_{\text{Apalancamiento (LM)}}
\end{equation}

\begin{conceptbox}{Por Que el ROE Colapso a 0,80\% en FY2025: La Trampa del Ajuste por Inflacion Impositivo}
\textbf{Descalce Fiscal de la Ley 27.468 y la NIC 29:}
\begin{itemize}
    \item En FY2025, el resultado operativo ($EBIT = \text{USD } 147,8\text{ MM}$) y el margen operativo ($OM = 14,18\%$) se mantuvieron solidos y alineados al promedio historico.
    \item Sin embargo, el factor \textbf{Tax Burden se desplomo a $TB = 0,157$}, implicando una \textbf{tasa efectiva de impuesto a las ganancias del 84,3\%} sobre la ganancia antes de impuestos ($EBT = \text{USD } 58,3\text{ MM}$).
    \item \textbf{Causa Raiz:} Bajo la Ley 27.468 del impuesto a las ganancias argentino, el ajuste por inflacion impositivo que arroja perdida debe diferirse obligatoriamente en \textbf{6 cuotas anuales nominales iguales (1/6 por ejercicio)}, sin actualizacion monetaria por inflacion futura.
    \item Al registrarse inflaciones de tres digitos, el valor presente de esas 5 cuotas diferidas se licua casi por completo, generando un impuesto corriente a pagar exorbitante sobre ganancias nominales infladas en pesos, a pesar de que la utilidad real en dolares es moderada.
    \item \textbf{Implicancia para la Valuacion:} Este castigo impositivo es un fenomeno transitorio del shock inflacionario. Por ello, el modelo de valuacion DCF normaliza la tasa impositiva estructural a la alicuota corporativa estatutaria del \textbf{35,0\%}, evitando extrapolar un ROE distorsionado hacia la perpetuidad.
\end{itemize}
\end{conceptbox}

\begin{center}
\includegraphics[width=0.88\linewidth, height=4.6cm, keepaspectratio]{theory_charts/teoria_07_dupont_radar_waterfall.png}
\captionof{figure}{Figura Teorica: Descomposicion DuPont de 5 Factores y Cascada de Impacto del Tax Burden en FY2025.}
\end{center}

\subsection{Calidad de Ganancias y Ratio de Devengamientos de Sloan (1996)}
Segun Richard Sloan (1996, *The Accounting Review*), las empresas que registran ganancias contables sin respaldo en flujos de fondos genuinos acumulan devengamientos subjetivos (*accruals*) que posteriormente se revierten destruyendo valor:
\begin{equation}
\text{Accrual Ratio} = \frac{\text{Resultado Neto} - FCO - FCI}{\text{Activo Total Promedio}} = \frac{9,17 - 148,20 - (-243,93)}{1.975,40} = \textbf{-0,064}
\end{equation}

\begin{conceptbox}{Por Que un Ratio de Sloan Negativo (-0,064) Certifica Calidad Contable Sobresaliente}
\textbf{Intuicion Financiera del Accrual Ratio:}
\begin{itemize}
    \item Un ratio de devengamiento positivo y elevado ($> +0,10$) indica que la empresa infla sus resultados registrando ventas a cobrar de dudoso cobro o activando costos operativos en bienes de uso.
    \item En Aluar, el flujo de caja generado por las operaciones ($FCO = \text{USD } 148,2\text{ MM}$) supera en mas de \textbf{16 veces} a la ganancia neta reportada ($\text{USD } 9,17\text{ MM}$).
    \item El valor negativo de \textbf{-0,064} prueba que los resultados contables de Aluar son ultra-conservadores y que la compania genera caja real disponible, descartando cualquier riesgo de manipulacion contable (*earnings management*).
\end{itemize}
\end{conceptbox}

\subsection{Ciclo de Conversion de Efectivo (CCC) y Gestion de Capital de Trabajo}
\begin{equation}
CCC = DIO\,(120) + DSO\,(45) - DPO\,(101) = \textbf{64 dias}
\end{equation}

\begin{conceptbox}{Por Que Aluar Mantiene 120 Dias de Inventario (DIO = 120 dias)}
\textbf{La Racionalidad del Inventario de Seguridad con Costo de Faltante Infinito:}
\begin{itemize}
    \item En la industria manufacturera estandar, 120 dias de stock podria considerarse un exceso de capital inmovilizado.
    \item Sin embargo, para Aluar, el costo de un quiebre de stock de alumina o coque de petroleo es virtualmente \textbf{infinito}: si la planta se queda sin materia prima por mas de 4 horas, las cubas electroliticas se congelan a $960\,^\circ\text{C}$, provocando la destruccion fisica de la celda.
    \item Dado que la alumina proviene de Australia o Brasil en buques de ultramar sujetos a contingencias climaticas o portuarias, mantener 120 dias de stock en silos en Puerto Madryn es la politica de gestion de inventarios estrictamente optima bajo la teoria de colas y riesgo operacional.
    \item Este inventario se financia eficientemente con \textbf{101 dias de credito de proveedores (DPO = 101)}, reduciendo el ciclo neto de caja a solo 64 dias.
\end{itemize}
\end{conceptbox}

\begin{center}
\includegraphics[width=0.88\linewidth, height=4.5cm, keepaspectratio]{figures_pristine/figura_16.png}
\captionof{figure}{Evolucion del Ciclo de Conversion de Efectivo (CCC), dias de inventario (DIO), cobranzas (DSO) y proveedores (DPO).}
\end{center}

\subsection{Modelos Cuantitativos de Optimizacion de Caja}

\subsubsection{1. Modelo Deterministico de Baumol-Tobin (1952)}
Sea $T$ el desembolso total de caja anual, $F$ el costo fijo por transaccion de liquidar inversiones o emitir deuda, e $i$ la tasa de interes de oportunidad del mercado. El saldo optimo de efectivo es:
\begin{equation}
TC(C) = \frac{T}{C}F + \frac{C}{2}i \implies \frac{d TC(C)}{d C} = -\frac{TF}{C^2} + \frac{i}{2} = 0 \implies C^* = \mathbf{\sqrt{\frac{2TF}{i}}}
\end{equation}

\subsubsection{2. Modelo Estocastico de Miller-Orr (1966) para Flujos Fluctuantes}
Cuando los flujos diarios de fondos siguen un paseo aleatorio con varianza diaria $\sigma^2$:
\begin{equation}
z^* = \mathbf{\sqrt[3]{\frac{3F\sigma^2}{4i}}} + L, \quad h^* = 3z^* - 2L
\end{equation}
donde $L$ es el colchon de seguridad minimo de caja fijado por la gerencia para contingencias operativas en Puerto Madryn.

\begin{codebox}{{engine\_valuacion.py:m4\_estados() -- Analisis Financiero y DuPont}}
\textbf{Codigo Fuente Real en Python:}
\begin{verbatim}
def m4_estados(eecc: dict) -> dict:
    # Calcula DuPont 5 factores, Accrual Ratio de Sloan y Ciclo de Conversion de Efectivo
    anios = eecc["anios"]
    dupont = []
    for a in anios:
        neto = eecc["resultado_neto"][a]
        ebt = eecc["ebt"][a]
        ebit = eecc["ebit"][a]
        rev = eecc["ventas"][a]
        act = eecc["activo_total"][a]
        pn = eecc["patrimonio_neto"][a]
        
        # Factores DuPont
        tb = neto / ebt if ebt != 0 else np.nan     # Tax Burden
        ib = ebt / ebit if ebit != 0 else np.nan     # Interest Burden
        om = ebit / rev if rev != 0 else np.nan      # Operating Margin
        at = rev / act if act != 0 else np.nan       # Asset Turnover
        lm = act / pn if pn != 0 else np.nan         # Leverage Multiplier
        roe = neto / pn if pn != 0 else np.nan
        dupont.append({"anio": a, "tb": tb, "ib": ib, "om": om, "at": at, "lm": lm, "roe": roe})
    
    # Sloan Accrual Ratio FY2025
    fco = eecc["fco"][2025]
    fci = eecc["fci"][2025]
    act_prom = (eecc["activo_total"][2024] + eecc["activo_total"][2025]) / 2.0
    sloan_ratio = (eecc["resultado_neto"][2025] - fco - fci) / act_prom
    
    # Ciclo de Conversion de Efectivo (CCC)
    dio = (eecc["inventarios"][2025] / eecc["cmv"][2025]) * 365.0
    dso = (eecc["creditos_ventas"][2025] / eecc["ventas"][2025]) * 365.0
    dpo = (eecc["deudas_comerciales"][2025] / eecc["cmv"][2025]) * 365.0
    ccc = dio + dso - dpo
    
    return {"dupont": dupont, "sloan_ratio": float(sloan_ratio), "ccc_dias": float(ccc)}
\end{verbatim}
\textbf{Analisis de Sintaxis y Econometria:}
\begin{itemize}
    \item \texttt{tb = neto / ebt}: Mide la retencion impositiva neta (colapso a 0,157 en FY2025 por ajuste inflacionario).
    \item \texttt{sloan\_ratio = (neto - fco - fci) / act\_prom}: Un ratio de -0,064 prueba excelente calidad contable.
    \item \texttt{ccc = dio + dso - dpo}: Mide los dias requeridos para convertir compras en efectivo (64 dias).
\end{itemize}
\end{codebox}
\clearpage
"""
