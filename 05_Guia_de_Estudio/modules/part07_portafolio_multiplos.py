# -*- coding: utf-8 -*-
"""
modules/part07_portafolio_multiplos.py
Parte VII: Valuacion Relativa por Multiplos, Teoria de Portafolio de Markowitz, Black-Litterman, Codigo Python y Riesgo de Euler.
"""

def get_content():
    return r"""
\section{Parte VII: Valuacion Relativa y Teoria Moderna de Portafolio}

\subsection{Valuacion Relativa y Analisis de Comparables Globales}
\begin{table}[H]
\centering
\caption{\textbf{Valuacion por Multiplos frente a Pares Globales de la Industria del Aluminio}}
\small
\begin{tabular}{lcccccc}
\toprule
\textbf{Compania / Par Global} & \textbf{Pais} & \textbf{EV/EBITDA} & \textbf{P/E} & \textbf{P/BV} & \textbf{Margen EBITDA} & \textbf{Capacidad (kt)} \\
\midrule
Alcoa Corp. (AA) & EE.UU. & 8,4x & 18,2x & 1,65x & 14,2\% & 2.550 \\
Norsk Hydro ASA (NHYDY) & Noruega & 7,2x & 14,8x & 1,42x & 18,5\% & 2.100 \\
Century Aluminum (CENX) & EE.UU. & 7,9x & 16,4x & 1,38x & 11,8\% & 1.015 \\
Chalco (Aluminum Corp. China) & China & 6,8x & 11,5x & 1,12x & 16,4\% & 6.800 \\
\midrule
\textbf{Mediana de la Muestra} & -- & \textbf{7,7x} & \textbf{15,6x} & \textbf{1,40x} & \textbf{15,3\%} & -- \\
Aluar S.A.I.C. (Spot FY2025) & Argentina & 13,4x & 22,4x & 1,78x & 8,4\% & 460 \\
\textbf{Aluar S.A.I.C. (Normalizado 2026E)} & Argentina & \textbf{10,7x} & \textbf{16,8x} & \textbf{1,55x} & \textbf{24,6\%} & 460 \\
\bottomrule
\end{tabular}
\end{table}

\begin{conceptbox}{Por Que el Multiplo EV/EBITDA Superior de Aluar Esta Justificado Fundamentalmente}
\textbf{La Relacion Fundamental entre Margen Operativo y Multiplos:}
\begin{itemize}
    \item Un analista desprevenido podria concluir que Aluar cotiza con sobreprecio al exhibir un EV/EBITDA normalizado de \textbf{10,7x} frente a la mediana global de \textbf{7,7x}.
    \item La teoria de valuacion relativa demuestra que las empresas con margenes operativos superiores y estructuras de costos en el primer cuartil mundial convierten una mayor proporcion de sus ingresos en flujo de caja libre neto ($FCFF$).
    \item Mientras la mediana de pares globales opera con un margen EBITDA del \textbf{15,3\%}, Aluar alcanza un margen normalizado del \textbf{24,6\%} gracias a su autogeneracion hidroelectrica/eolica y Cash Cost C1 de USD 1.680/t.
    \item Al normalizarse la macroeconomia argentina, la expansion del EBITDA operativo hacia USD 302,9 MM en 2026E comprime el multiplo efectivo a niveles altamente competitivos.
\end{itemize}
\end{conceptbox}

\noindent
\begin{minipage}[b]{0.488\linewidth}
    \centering
    \includegraphics[width=\linewidth, height=4.4cm, keepaspectratio]{figures_pristine/figura_11.png}
    \captionof{figure}{\small EV/EBITDA vs. Margen EBITDA frente a pares globales.}
\end{minipage}\hfill
\begin{minipage}[b]{0.488\linewidth}
    \centering
    \includegraphics[width=\linewidth, height=4.4cm, keepaspectratio]{figures_pristine/figura_22.png}
    \captionof{figure}{\small Expansion dinamica de multiplo hacia la mediana global.}
\end{minipage}
\vspace{0.15cm}

\subsection{Optimizacion Cuadratica de Markowitz y Matriz Hessiana Orlada}
Sea el problema de optimizacion de cartera:
\begin{equation}
\min_{\mathbf{w}} \quad \frac{1}{2} \mathbf{w}^T \mathbf{\Sigma} \mathbf{w} \quad \text{sujeto a} \quad \mathbf{w}^T \mathbf{1} = 1, \quad \mathbf{w}^T \boldsymbol{\mu} = \mu_p, \quad \mathbf{w} \ge \mathbf{0}
\end{equation}
El sistema lineal de condiciones de primer orden (KKT) en forma matricial orlada es:
\begin{equation}
\begin{bmatrix}
\mathbf{\Sigma} & \mathbf{1} & \boldsymbol{\mu} \\
\mathbf{1}^T & 0 & 0 \\
\boldsymbol{\mu}^T & 0 & 0
\end{bmatrix}
\begin{bmatrix}
\mathbf{w}^* \\
-\lambda_1 \\
-\lambda_2
\end{bmatrix}
=
\begin{bmatrix}
\mathbf{0} \\
1 \\
\mu_p
\end{bmatrix}
\end{equation}
Dado que la matriz de covarianzas $\mathbf{\Sigma}$ es definida positiva ($\nabla_{\mathbf{w}}^2 \mathcal{L} = \mathbf{\Sigma} > 0$), la condicion de segundo orden garantiza que $\mathbf{w}^*$ es un minimo global estricto.

\begin{center}
\includegraphics[width=0.88\linewidth, height=4.6cm, keepaspectratio]{theory_charts/teoria_08_markowitz_euler_budgeting.png}
\captionof{figure}{Figura Teorica: Frontera Eficiente de Markowitz, Linea CAL y Presupuesto de Riesgo de Euler ($\sum CCR_i = 100\%$).}
\end{center}

\subsection{Deduccion Matematica del Modelo de Black-Litterman (1992)}
El modelo de Black-Litterman combina el equilibrio de mercado del CAPM (*prior*) con las visiones especificas del analista (*views*) mediante inferencia bayesiana:
\begin{enumerate}
    \item \textbf{Prior de Retornos Implicitos de Equilibrio ($\boldsymbol{\Pi}$):}
    \begin{equation}
    \boldsymbol{\Pi} = \delta \mathbf{\Sigma} \mathbf{w}_{\text{mkt}}
    \end{equation}
    donde $\delta = \frac{\mathbb{E}[R_M] - Rf}{\sigma_M^2}$ es el coeficiente de aversion relativa al riesgo del mercado.
    \item \textbf{Estructura de Visiones del Inversionista:}
    \begin{equation}
    \mathbf{P} \boldsymbol{\mu} = \mathbf{q} + \boldsymbol{\epsilon}, \quad \boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{\Omega})
    \end{equation}
    \item \textbf{Distribucion Posterior de Rendimientos Esperados ($\boldsymbol{\mu}_{\text{BL}}$):}
    \begin{equation}
    \boldsymbol{\mu}_{\text{BL}} = \left[ (\tau \mathbf{\Sigma})^{-1} + \mathbf{P}^T \mathbf{\Omega}^{-1} \mathbf{P} \right]^{-1} \left[ (\tau \mathbf{\Sigma})^{-1} \boldsymbol{\Pi} + \mathbf{P}^T \mathbf{\Omega}^{-1} \mathbf{q} \right]
    \end{equation}
\end{enumerate}

\subsection{Demostracion Formal de la Descomposicion de Riesgo de Euler}

\begin{teorema}[Teorema de Euler para Funciones Homogeneas y Presupuesto de Riesgo]
La desviacion estandar de una cartera $\sigma_p(\mathbf{w}) = \sqrt{\mathbf{w}^T \mathbf{\Sigma} \mathbf{w}}$ es una funcion homogenea de grado 1 en las ponderaciones $\mathbf{w}$. En consecuencia:
\begin{equation}
\sigma_p(\mathbf{w}) = \sum_{i=1}^n w_i \frac{\partial \sigma_p}{\partial w_i} = \sum_{i=1}^n w_i MCR_i
\end{equation}
donde el Riesgo Marginal es $MCR_i = \frac{(\mathbf{\Sigma} \mathbf{w})_i}{\sigma_p}$ y la Contribucion Porcentual al Riesgo es $CCR_i = \frac{w_i (\mathbf{\Sigma} \mathbf{w})_i}{\sigma_p^2}$, cumpliendose $\sum_{i=1}^n CCR_i = \textbf{100\%}$.
\end{teorema}

\begin{conceptbox}{Por Que la Descomposicion de Euler es Indispensable para Risk Budgeting}
\textbf{Asignacion Exacta del Riesgo de Portafolio:}
\begin{itemize}
    \item En la gestion tradicional, los inversores miden la exposicion segun el porcentaje del capital invertido ($w_i$).
    \item En la practica, un activo volatil como Aluar que represente el $20\%$ del capital puede ser responsable del \textbf{35\% al 40\% de la volatilidad total} de la cartera.
    \item La identidad de Euler permite al comite de inversiones descomponer matematicamente el 100\% del riesgo sin residuos ni dobles contabilizaciones, asignando limites de presupuesto de riesgo cuantitativo (*risk budgeting*).
\end{itemize}
\end{conceptbox}

\begin{codebox}{{engine\_valuacion.py:m11\_portafolio() -- Optimizacion Markowitz y Riesgo de Euler}}
\textbf{Codigo Fuente Real en Python:}
\begin{verbatim}
def m11_portafolio(panel: pd.DataFrame, rf=0.047) -> dict:
    # Calcula la cartera de Maximo Sharpe (SLSQP) y la descomposicion de riesgo de Euler
    import scipy.optimize as sco
    rets = panel[["alua_usd", "txar_usd", "merval_usd"]].pct_change().dropna()
    mu = rets.mean().values * 252.0
    cov = rets.cov().values * 252.0
    n = len(mu)
    
    # 1. Optimizacion de Maximo Sharpe
    def neg_sharpe(w):
        p_ret = np.dot(w, mu)
        p_vol = np.sqrt(np.dot(w, np.dot(cov, w)))
        return -(p_ret - rf) / p_vol
    
    bnds = tuple((0.0, 1.0) for _ in range(n))
    cons = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0})
    init_w = np.ones(n) / n
    res = sco.minimize(neg_sharpe, init_w, method='SLSQP', bounds=bnds, constraints=cons)
    w_opt = res.x
    
    # 2. Descomposicion de Riesgo de Euler
    p_vol = np.sqrt(np.dot(w_opt, np.dot(cov, w_opt)))
    mcr = np.dot(cov, w_opt) / p_vol
    ccr = (w_opt * np.dot(cov, w_opt)) / (p_vol ** 2)
    
    return {"w_opt": w_opt.tolist(), "p_ret": float(np.dot(w_opt, mu)),
            "p_vol": float(p_vol), "sharpe": float(-(neg_sharpe(w_opt))),
            "mcr": mcr.tolist(), "ccr_pct": (ccr * 100.0).tolist()}
\end{verbatim}
\textbf{Analisis de Sintaxis y Econometria:}
\begin{itemize}
    \item \texttt{sco.minimize(..., method='SLSQP')}: Resuelve la optimizacion cuadratica no lineal con restricciones lineales de igualdad y cotas.
    \item \texttt{ccr = (w\_opt * np.dot(cov, w\_opt)) / (p\_vol ** 2)}: Implementa la identidad de Euler garantizando que $\sum CCR_i = 100\%$.
\end{itemize}
\end{codebox}
\clearpage
"""
