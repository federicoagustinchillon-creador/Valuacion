# -*- coding: utf-8 -*-
"""
modules/part06_riesgo_evt.py
Parte VI: Gestion Cuantitativa de Riesgo de Mercado, EVT-GPD, Modelo de Merton (DD), Codigo Python y Criterio de Kelly.
"""

def get_content():
    return r"""
\section{Parte VI: Gestion Cuantitativa de Riesgo de Mercado, EVT y Dimensionamiento}

\subsection{Axiomatica de Medidas de Riesgo Coherentes (Artzner et al., 1999)}

\begin{definicion}[Medida de Riesgo Coherente]
Una funcion $\rho: \mathcal{X} \to \mathbb{R}$ es coherente si satisface:
\begin{enumerate}
    \item \textbf{Invarianza por Traslacion:} $\rho(X + c) = \rho(X) - c$.
    \item \textbf{Subaditividad:} $\rho(X_1 + X_2) \le \rho(X_1) + \rho(X_2)$.
    \item \textbf{Homogeneidad Positiva:} $\rho(\lambda X) = \lambda \rho(X)$ para $\lambda \ge 0$.
    \item \textbf{Monotonicidad:} Si $X_1 \le X_2$, entonces $\rho(X_1) \ge \rho(X_2)$.
\end{enumerate}
\end{definicion}

\begin{conceptbox}{Por Que el VaR Falla y el Expected Shortfall (CVaR) es la Unica Medida Coherente}
\textbf{El Fallo de Subaditividad del Value at Risk (VaR):}
\begin{itemize}
    \item En distribuciones con colas pesadas o asimetria, el VaR viola el axioma de subaditividad: se pueden construir carteras donde $VaR(A+B) > VaR(A) + VaR(B)$, penalizando absurdamente la diversificacion.
    \item Ademas, el VaR es "ciego" a la gravedad de las perdidas extremas: solo indica que la perdida superara el umbral con probabilidad $1-\alpha$, pero no distingue si la perdida mas alla del corte es del $11\%$ o del $70\%$.
    \item El \textbf{Expected Shortfall ($ES_\alpha = \frac{1}{1-\alpha}\int_0^{1-\alpha} VaR_u du$)} promedia todas las perdidas en la cola extrema ($ES_{99\%} = -15,78\%$), es estrictamente coherente y convexo, permitiendo optimizacion de carteras sin minimos locales espurios.
\end{itemize}
\end{conceptbox}

\begin{center}
\includegraphics[width=0.88\linewidth, height=4.5cm, keepaspectratio]{figures_pristine/figura_25.png}
\captionof{figure}{Ajuste EVT-GPD sobre la cola de perdidas de ALUA.BA: $VaR_{99\%} = -10,44\%$ y $ES_{99\%} = -15,78\%$ frente a subestimacion de la distribucion Normal.}
\end{center}

\subsection{Teoria de Valores Extremos y Distribucion Pareto Generalizada (EVT-GPD)}

\begin{teorema}[Teorema de Pickands-Balkema-de Haan (1975)]
Para un umbral $u$ suficientemente alto, los excesos $Y = X - u \mid X > u$ convergen a la Pareto Generalizada:
\begin{equation}
G_{\xi, \beta}(y) = 1 - \left( 1 + \xi \frac{y}{\beta} \right)^{-1/\xi}
\end{equation}
\end{teorema}

\subsubsection{1. Estimacion por Maxima Verosimilitud (MLE) de la GPD}
La funcion de log-verosimilitud para una muestra de $k$ excesos $\{y_1, \dots, y_k\}$ sobre el umbral $u$ es:
\begin{equation}
\ln L(\xi, \beta) = -k \ln \beta - \left( 1 + \frac{1}{\xi} \right) \sum_{i=1}^k \ln\left( 1 + \xi \frac{y_i}{\beta} \right)
\end{equation}
Maximizando numericamente mediante el algoritmo BFGS se obtienen los estimadores $\hat{\xi} = \textbf{0,280}$ y $\hat{\beta} = \textbf{0,0191}$.

\subsubsection{2. Deduccion Analitica de las Formulas Cerradas de VaR y Expected Shortfall}
Igualando la probabilidad de supervivencia de la cola a $1 - q$:
\begin{equation}
P(X > x) = \frac{N_u}{N}\left( 1 + \xi \frac{x - u}{\beta} \right)^{-1/\xi} = 1 - q
\end{equation}
Despejando $x = VaR_q^{\text{EVT}}$:
\begin{equation}
VaR_q^{\text{EVT}} = u + \frac{\beta}{\xi} \left[ \left( \frac{N}{N_u}(1 - q) \right)^{-\xi} - 1 \right] = \textbf{-10,44\%}
\end{equation}
Integrando los cuantiles extremos mas alla del VaR:
\begin{equation}
ES_q^{\text{EVT}} = \frac{VaR_q^{\text{EVT}}}{1 - \xi} + \frac{\beta - \xi u}{1 - \xi} = \textbf{-15,78\%}
\end{equation}

\begin{center}
\includegraphics[width=0.88\linewidth, height=4.6cm, keepaspectratio]{theory_charts/teoria_04_evt_gpd_pot.png}
\captionof{figure}{Figura Teorica: Ajuste Pareto Generalizado (POT) de Excesos sobre Umbral y Cuantiles EVT 99\%.}
\end{center}

\subsection{Demostracion del Fallo de Cornish-Fisher (Caveat de Jaschke 2001)}
\begin{equation}
z_{\text{CF}}(\alpha) = z_\alpha + \frac{S}{6}(z_\alpha^2 - 1) + \frac{K}{24}(z_\alpha^3 - 3z_\alpha) - \frac{S^2}{36}(2z_\alpha^3 - 5z_\alpha)
\end{equation}

\begin{conceptbox}{Por Que Cornish-Fisher Quiebra para Curtosis $K > 6$ (El Caveat de Jaschke)}
\textbf{La Perdida de Monotonia Cuantilica:}
\begin{itemize}
    \item La expansion de Cornish-Fisher es un polinomio de tercer grado disenado para corregir cuantiles normales por asimetria $S$ y curtosis $K$.
    \item Sin embargo, Stefan Jaschke (2001, RiskLab ETH Zurich) demostro que cuando el exceso de curtosis supera $K > 6$, la derivada $\frac{\partial z_{\text{CF}}}{\partial z_\alpha}$ se vuelve estrictamente negativa en las colas ($z_\alpha < -2,33$).
    \item Esto provoca una aberracion matematica inadmisible: el polinomio se pliega sobre si mismo y asigna \textbf{menores perdidas a niveles de confianza mas exigentes} (por ejemplo, el VaR 99,9\% resulta menor que el VaR 99\%).
    \item Dado que la serie de ALUA.BA presenta una curtosis empirica de \textbf{8,41}, Cornish-Fisher queda formalmente invalidado, haciendo obligatorio el uso de la Teoria de Valores Extremos (EVT-GPD).
\end{itemize}
\end{conceptbox}

\begin{center}
\includegraphics[width=0.88\linewidth, height=4.6cm, keepaspectratio]{theory_charts/teoria_03_cornish_fisher_quiebre.png}
\captionof{figure}{Figura Teorica: Demostracion Grafica del Quiebre de Monotonia y Region de Invalidez de Cornish-Fisher ($K=8,41$).}
\end{center}

\subsection{Modelo Estructural de Merton (1974) y Distancia al Default (DD)}
\begin{equation}
DD = \frac{\ln(V_0 / D) + \left( \mu_V - \frac{1}{2}\sigma_V^2 \right) T}{\sigma_V \sqrt{T}} = \frac{\ln(2639,6 / 456,0) + (0,08 - 0,0242)(1)}{0,22 \times 1} = \mathbf{8,23\sigma} \implies \text{EDF} < 0,0001\%
\end{equation}

\begin{conceptbox}{Por Que el Equity es un Call sobre los Activos Corporativos (Merton 1974)}
\textbf{Intuicion del Modelo Estructural de Credito:}
\begin{itemize}
    \item Merton (1974) demostro que tener acciones de una empresa endeudada equivale a ser dueno de una opcion de compra europea ($Call$) sobre el valor total de los activos de la firma ($V$), con precio de ejercicio igual al valor nominal de la deuda ($D$).
    \item Si al vencimiento $V_T > D$, los accionistas ejercen su opcion pagando la deuda y quedandose con el excedente ($Equity = V_T - D$). Si $V_T < D$, los accionistas declaran la quiebra y entregan los activos a los acreedores, acotando su perdida a cero por responsabilidad limitada.
    \item La \textbf{Distancia al Default ($DD = 8,23\sigma$)} indica que el valor de los activos de Aluar tendria que caer mas de 8 desviaciones estandar en un ano para que la empresa no pueda pagar sus deudas, confirmando una probabilidad de quiebra estructural virtualmente nula.
\end{itemize}
\end{conceptbox}

\begin{center}
\includegraphics[width=0.88\linewidth, height=4.6cm, keepaspectratio]{theory_charts/teoria_09_merton_distancia_default.png}
\captionof{figure}{Figura Teorica: Modelo Estructural de Merton, Barrera de Deuda y Distancia al Default ($DD = 8,23\sigma$).}
\end{center}

\subsection{Dimensionamiento de Posicion de Cartera y Criterio de Half-Kelly}

\begin{conceptbox}{Por Que Usar Half-Kelly (53,5\%) y Limite Prudencial del 20,0\%}
\textbf{La Racionalidad de Acotar el Criterio de Kelly Puro:}
\begin{itemize}
    \item La formula de Kelly puro ($f^* = \frac{\mu - Rf}{\sigma^2} = \frac{0,258 - 0,047}{0,444^2} = \mathbf{107,0\%}$) maximiza asintoticamente la tasa de crecimiento logaritmico de la riqueza.
    \item Sin embargo, asume que los parametros de retorno y volatilidad se conocen con certeza matematica absoluta. En presencia de error de estimacion, Full-Kelly expone al inversor a una probabilidad del \textbf{33\% de sufrir un drawdown del 50\%} de la cartera.
    \item El enfoque \textbf{Half-Kelly ($f^* / 2 = 53,5\%$)} reduce la varianza de la riqueza acumulada en un $50\%$ a cambio de sacrificar solo el $25\%$ del crecimiento esperado.
    \item Finalmente, aplicando la politica institucional de control de riesgo de cartera (limite maximo por activo singular), la posicion se acota al \textbf{tope prudencial del 20,0\%}, blindando la cartera contra eventos de cola.
\end{itemize}
\end{conceptbox}

\noindent
\begin{minipage}[b]{0.488\linewidth}
    \centering
    \includegraphics[width=\linewidth, height=4.4cm, keepaspectratio]{figures_pristine/figura_23.png}
    \captionof{figure}{\small Asignacion Half-Kelly (53,5\%) y tope de riesgo (20,0\%).}
\end{minipage}\hfill
\begin{minipage}[b]{0.488\linewidth}
    \centering
    \includegraphics[width=\linewidth, height=4.4cm, keepaspectratio]{figures_pristine/figura_28.png}
    \captionof{figure}{\small Matriz de riesgos: probabilidad vs impacto.}
\end{minipage}
\vspace{0.15cm}

\begin{codebox}{{engine\_valuacion.py:m10\_riesgo() -- EVT-GPD, Merton DD y Criterio de Kelly}}
\textbf{Codigo Fuente Real en Python:}
\begin{verbatim}
def m10_riesgo(panel: pd.DataFrame) -> dict:
    # Calcula metricas de riesgo de cola EVT-GPD, Merton Distance-to-Default y Kelly sizing
    from scipy import stats
    r = panel["alua_usd"].pct_change().dropna()
    perdidas = -r[r < 0]  # Vector de perdidas positivas
    
    # 1. Ajuste EVT-GPD sobre umbral u = 3,5%
    u = 0.035
    excesos = perdidas[perdidas > u] - u
    c_xi, _, scale_beta = stats.genpareto.fit(excesos, floc=0)
    xi = float(c_xi)
    beta = float(scale_beta)
    
    # 2. VaR y ES analiticos EVT 99%
    n_total = len(perdidas)
    n_u = len(excesos)
    q = 0.99
    var_99_evt = float(u + (beta / xi) * (((n_total / n_u) * (1.0 - q)) ** (-xi) - 1.0))
    es_99_evt = float((var_99_evt / (1.0 - xi)) + ((beta - xi * u) / (1.0 - xi)))
    
    # 3. Distancia al Default de Merton (1974)
    v0, d = 2639.6, 456.0
    mu_v, sigma_v = 0.08, 0.22
    dd = float((np.log(v0 / d) + (mu_v - 0.5 * sigma_v**2)) / sigma_v)
    edf = float(stats.norm.cdf(-dd))
    
    # 4. Dimensionamiento optimo segun Criterio de Kelly
    mu_ret = 0.258
    rf_ret = 0.047
    sigma_ret = 0.444
    f_kelly = float((mu_ret - rf_ret) / (sigma_ret ** 2))   # 107,0%
    f_half_kelly = float(f_kelly / 2.0)                     # 53,5%
    f_recomendada = float(min(f_half_kelly, 0.20))          # Tope prudencial 20,0%
    
    return {"var_99_evt": -var_99_evt, "es_99_evt": -es_99_evt, "xi": xi, "beta": beta,
            "merton_dd": dd, "merton_edf": edf, "kelly_f": f_kelly, "f_prudencial": f_recomendada}
\end{verbatim}
\textbf{Analisis de Sintaxis y Econometria:}
\begin{itemize}
    \item \texttt{stats.genpareto.fit(excesos, floc=0)}: Fija la localizacion en cero para estimar la escala y la forma de Pareto.
    \item \texttt{var\_99\_evt} y \texttt{es\_99\_evt}: Utilizan las formulas analiticas exactas del Teorema de Balkema-de Haan.
    \item \texttt{f\_recomendada}: Acota el apalancamiento teorico al 20,0\% para evitar riesgo de ruina.
\end{itemize}
\end{codebox}
\clearpage
"""
