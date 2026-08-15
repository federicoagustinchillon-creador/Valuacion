# -*- coding: utf-8 -*-
"""
modules/part03_costo_capital.py
Parte III: Costo de Capital (WACC), Teoria de Estructura de Capital, Modelos de Desapalancamiento y Codigo Python.
"""

def get_content():
    return r"""
\section{Parte III: Costo de Capital, Entorno Macroeconomico y Desapalancamiento}

\subsection{Entorno Macroeconomico y Riesgo Soberano Argentino}
La estimacion del costo del capital propio en economias emergentes requiere modelar la exposicion de los flujos de la compania frente al riesgo soberano local y la dinamica inflacionaria y cambiaria.

\noindent
\begin{minipage}[b]{0.488\linewidth}
    \centering
    \includegraphics[width=\linewidth, height=4.4cm, keepaspectratio]{figures_pristine/figura_03.png}
    \captionof{figure}{\small PBI real (\%) e inflacion anual (\%) en Argentina (2020--2026).}
\end{minipage}\hfill
\begin{minipage}[b]{0.488\linewidth}
    \centering
    \includegraphics[width=\linewidth, height=4.4cm, keepaspectratio]{figures_pristine/figura_04.png}
    \captionof{figure}{\small Evolucion historica del riesgo pais EMBI+ Argentina (pb).}
\end{minipage}
\vspace{0.15cm}

\begin{center}
\includegraphics[width=0.88\linewidth, height=4.5cm, keepaspectratio]{figures_pristine/figura_05.png}
\captionof{figure}{Trayectoria proyectada del EMBI+ bajo proceso AR(1) y tasa de rendimiento soberano implícita.}
\end{center}

\subsection{Por Que el CAPM Tradicional Falla en Mercados Emergentes y Metodologia CAPM-$\lambda$}

\begin{conceptbox}{Por Que No Usar CAPM Simple ni Sumar el 100\% del EMBI+ (Damodaran Country Risk Exposure)}
\textbf{El Dilema del Costo de Capital en Mercados Emergentes:}
\begin{enumerate}
    \item \textbf{Fallo del CAPM Tradicional ($Ke = Rf + \beta \times ERP$):} Asume mercados financieros integrados globalmente sin fricciones ni riesgo soberano. Si se aplicara ciegamente a Aluar, arrojaria un $Ke \approx 8,4\%$, ignorando el riesgo pais argentino, la inestabilidad cambiaria y las restricciones regulatorias locales.
    \item \textbf{Fallo del Enfoque Ingenuo ($Ke = Rf + \beta \times ERP + EMBI+$ con $\lambda = 1,0$):} Sumar el riesgo pais integro ($441\text{ a }1.500\text{ pb}$) asume que Aluar sufre el riesgo de default del Tesoro argentino en igual medida que un banco comercial domestico o una distribuidora electrica regulada en pesos. Esto elevaria el $Ke$ al $15\text{--}20\%$, castigando absurdamente a una empresa cuyos ingresos estan $100\%$ dolarizados.
    \item \textbf{La Solucion Rigurosa: Metodologia CAPM-$\lambda$ de Aswath Damodaran (2012):}
    \begin{equation}
    Ke = Rf + \beta_L \cdot ERP + \lambda \cdot EMBI+
    \end{equation}
    donde el factor $\lambda$ mide la proporcion real de exposicion de la empresa al riesgo operativo local.
    \item \textbf{Deduccion y Calibracion de $\lambda = 0,20$ para Aluar:}
    \begin{equation}
    \lambda = \frac{\% \text{ Ventas Domesticas Sensibles}}{\% \text{ Empresa Promedio de la Economia}} \approx \frac{25\%}{100\%} \times 0,80 = \mathbf{0,20}
    \end{equation}
    Dado que Aluar exporta el \textbf{75\% de su produccion al mercado internacional} cobrando directamente en dolares en cuentas del exterior, y que el 25\% vendido localmente se comercializa a \textbf{paridad de importacion en dolares oficiales}, su exposicion al riesgo soberano local es de apenas el 20\%, sumando un spread justo de $+88\text{ pb}$ sobre el costo de capital internacional.
\end{enumerate}
\end{conceptbox}

\subsection{Demostracion Formal del Teorema de Modigliani-Miller con Impuestos (1963)}

\begin{teorema}[Valor de la Firma Apalancada y Escudo Fiscal]
Bajo impuestos corporativos a tasa constante $t$ y deuda perpetua libre de riesgo con interes $K_d$, el valor de la empresa apalancada ($V_L$) es igual al valor de la empresa desapalancada ($V_U$) mas el valor presente del escudo fiscal (*Interest Tax Shield*):
\begin{equation}
V_L = V_U + t \cdot D
\end{equation}
\end{teorema}

\begin{proof}
Consideremos dos empresas idénticas en riesgo operativo que generan un flujo perpetuo antes de intereses e impuestos $EBIT$:
\begin{enumerate}
    \item \textbf{Empresa No Apalancada ($U$):} No posee deuda. Su flujo neto disponible para los accionistas es:
    \begin{equation}
    CF_U = EBIT(1 - t) \implies V_U = \frac{EBIT(1 - t)}{K_u}
    \end{equation}
    \item \textbf{Empresa Apalancada ($L$):} Posee deuda por monto nominal $D$ a tasa $K_d$. El gasto por intereses es $K_d D$. El flujo total combinado para accionistas y acreedores es:
    \begin{equation}
    CF_L = (EBIT - K_d D)(1 - t) + K_d D = EBIT(1 - t) + t K_d D = CF_U + t K_d D
    \end{equation}
    \item \textbf{Arbitraje por Cartera Replicante:}
    \begin{itemize}
        \item \textbf{Estrategia A:} Comprar el $1\%$ del capital accionario de la empresa apalancada $L$. Flujo recibido: $0,01 \cdot (EBIT - K_d D)(1 - t)$.
        \item \textbf{Estrategia B (Apalancamiento Casero comprando 1\% de $U$ y pidiendo prestado $0,01 \cdot D$):}
        Flujo recibido: $0,01 \cdot [EBIT(1 - t) + t K_d D - K_d D(1 - t)] = 0,01 \cdot (EBIT - K_d D)(1 - t)$.
    \end{itemize}
    Por la ley del precio unico en ausencia de arbitraje:
    \begin{equation}
    V_L = PV(CF_U) + PV(t K_d D) = V_U + \sum_{k=1}^{\infty} \frac{t K_d D}{(1 + K_d)^k} = V_U + t K_d D \left( \frac{1}{K_d} \right) = V_U + t \cdot D
    \end{equation}
\end{enumerate}
\end{proof}

\subsection{Deduccion Rigurosa y Comparacion de Ecuaciones de Desapalancamiento}

\begin{table}[H]
\centering
\caption{\textbf{Comparacion Teorica de Ecuaciones de Desapalancamiento de Beta}}
\small
\begin{tabular}{llcl}
\toprule
\textbf{Modelo / Autor} & \textbf{Hipotesis de Politica de Deuda} & \textbf{Tasa Escudo Fiscal} & \textbf{Formula del Beta Apalancado ($\beta_L$)} \\
\midrule
\textbf{Hamada (1972)} & Deuda nominal fija perpetua & $K_d$ & $\beta_L = \beta_U [1 + (1 - t)\frac{D}{E}]$ \\
\textbf{Miles-Ezzell (1980)} & Rebalanceo anual del ratio $D/V$ & $K_d$ (ano 1), $K_u$ ($>1$) & $\beta_L = \beta_U [1 + (1 - t \frac{K_d}{1+K_d})\frac{D}{E}]$ \\
\textbf{Harris-Pringle (1985)} & Rebalanceo continuo instantaneo de $D/V$ & $K_u$ & $\beta_L = \beta_U [1 + \frac{D}{E}] - \beta_D \frac{D}{E}$ \\
\bottomrule
\end{tabular}
\end{table}

\begin{conceptbox}{Por Que Se Utiliza la Formula de Hamada en la Valuacion de Aluar}
\textbf{Fundamento Financiero:}
\begin{itemize}
    \item Aluar financia sus grandes proyectos industriales (como PEAL) mediante emisiones puntuales de Obligaciones Negociables (ONs) a plazo fijo (3 a 5 anos) y prestamos sindicados, en lugar de ajustar dinamicamente su deuda dia a dia para mantener un ratio $D/V$ milimetrico.
    \item La formula de Hamada refleja con precision la estructura de deuda fija nominal y permite aislar el riesgo operativo puro ($\beta_U = 0,675$) a partir de la estructura financiera historica ($D/E_{\text{hist}} = 0,5023$) y reapalancar ($\beta_L = 0,888$) hacia la estructura de capital objetivo ($D/E_{\text{target}} = 0,4861$).
\end{itemize}
\end{conceptbox}

\subsection{Estimacion Empirica del Beta OLS y Ajuste Bayesiano de Blume y Vasicek}
A partir de la serie de 2.520 retornos diarios de ALUA.BA contra el indice S\&P 500 en dolares durante la ventana 2016--2026:
\begin{equation}
R_{i,t} = \alpha_i + \beta_{\text{OLS}} R_{M,t} + \epsilon_t \implies \hat{\beta}_{\text{OLS}} = \frac{\sum (R_{M,t} - \bar{R}_M)(R_{i,t} - \bar{R}_i)}{\sum (R_{M,t} - \bar{R}_M)^2} = \mathbf{0,8420 \pm 0,0620}
\end{equation}

\begin{conceptbox}{Por Que Aplicar el Ajuste de Marshall Blume (1975) ($\beta_{\text{Blume}} = \frac{2}{3}\beta_{\text{OLS}} + \frac{1}{3}(1,0)$)}
\textbf{La Racionalidad de la Reversion a la Media del Riesgo Sistematico:}
\begin{itemize}
    \item Los betas estimados por regresion lineal simple (OLS) estan sujetos a errores muestrales y ruido de corto plazo.
    \item Las investigaciones empiricas de Marshall Blume (1975) demostraron que los betas corporativos tienden sistematicamente hacia $1,0$ a lo largo del tiempo: empresas con betas inferiores a $1$ tienden a diversificar sus operaciones o tomar mas apalancamiento, mientras que empresas con betas muy altos tienden a madurar.
    \item Ajustar el beta muestral de $0,842$ a \textbf{0,895} es un acto de prudencia metodologica que eleva la tasa de descuento WACC y evita sobreestimar el valor intrinseco de la accion.
\end{itemize}
\end{conceptbox}

\noindent
\begin{minipage}[b]{0.488\linewidth}
    \centering
    \includegraphics[width=\linewidth, height=4.4cm, keepaspectratio]{figures_pristine/figura_13.png}
    \captionof{figure}{\small Cascada de ajuste metodologico del Beta ($\beta_{OLS} \to \beta_L$).}
\end{minipage}\hfill
\begin{minipage}[b]{0.488\linewidth}
    \centering
    \includegraphics[width=\linewidth, height=4.4cm, keepaspectratio]{figures_pristine/figura_14.png}
    \captionof{figure}{\small Desglose aditivo del costo del equity ($Ke$) y WACC (7,06\%).}
\end{minipage}
\vspace{0.15cm}

\begin{codebox}{{engine\_valuacion.py:m6\_costo\_capital() -- Beta, Blume, Hamada y WACC}}
\textbf{Codigo Fuente Real en Python:}
\begin{verbatim}
def m6_costo_capital(eecc: dict, mkt: dict, macro: dict, tasa_tax=0.35, lambda_ar=0.20) -> dict:
    # Calcula el Beta OLS, ajuste de Blume, desapalancamiento/reapalancamiento de Hamada y WACC
    # 1. Beta OLS y Blume
    beta_ols = float(mkt["beta_ols"])          # 0,8420
    se_beta = float(mkt["beta_se"])            # 0,0620
    beta_blume = (2.0 / 3.0) * beta_ols + (1.0 / 3.0) * 1.0  # 0,8947
    
    # 2. Desapalancamiento de Hamada (Historico)
    de_hist = float(eecc["de_historico_mediana"])  # 0,5023
    beta_u = beta_blume / (1.0 + (1.0 - tasa_tax) * de_hist)  # 0,6745
    
    # 3. Reapalancamiento de Hamada (Target)
    de_target = float(mkt["de_target"])        # 0,4861 (E/V = 67,29%, D/V = 32,71%)
    beta_l = beta_u * (1.0 + (1.0 - tasa_tax) * de_target)    # 0,8876
    
    # 4. Costo del Equity (Ke) segun CAPM-lambda Damodaran
    rf = float(macro["rf_treasury_10y"])       # 4,70%
    erp = float(macro["erp_damodaran"])        # 4,18%
    embi = float(macro["embi_spread"])         # 4,41% (441 pb)
    ke = rf + beta_l * erp + lambda_ar * embi  # 9,30%
    
    # 5. Costo de la Deuda despues de impuestos y WACC
    kd = float(mkt["tasa_kd_promedio"])        # 3,80% (ONs hard dollar)
    kd_after_tax = kd * (1.0 - tasa_tax)       # 2,47%
    e_sobre_v = float(mkt["e_sobre_v"])        # 67,29%
    d_sobre_v = float(mkt["d_sobre_v"])        # 32,71%
    wacc = ke * e_sobre_v + kd_after_tax * d_sobre_v  # 7,06%
    
    return {"beta_blume": beta_blume, "beta_u": beta_u, "beta_l": beta_l,
            "ke": ke, "wacc": wacc, "e_sobre_v": e_sobre_v, "d_sobre_v": d_sobre_v}
\end{verbatim}
\textbf{Analisis de Sintaxis y Econometria:}
\begin{itemize}
    \item \texttt{beta\_blume}: Pondera $2/3$ la evidencia muestral y $1/3$ el prior incondicional $\beta = 1$.
    \item \texttt{beta\_u}: Aisla el riesgo operativo puro neutralizando el escudo fiscal del apalancamiento historico.
    \item \texttt{ke = rf + beta\_l * erp + lambda\_ar * embi}: Aplica el factor de exposicion $\lambda = 0,20$ sin incurrir en duplicacion de riesgo sistematico.
\end{itemize}
\end{codebox}
\clearpage
"""
