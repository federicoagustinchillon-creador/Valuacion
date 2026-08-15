# -*- coding: utf-8 -*-
"""
modules/part05_estocastico_copulas.py
Parte V: Modelizacion Estocastica Multivariada, Copulas Arqui-medianas, Difusiones de Ito, CIR, Codigo Python y Monte Carlo.
"""

def get_content():
    return r"""
\section{Parte V: Modelizacion Estocastica Multivariada, Copulas y Calculo de Ito}

\subsection{Algebra Lineal y Proyecciones de Hilbert en Modelos Econometricos}

\subsubsection{1. Descomposicion QR y Proyecciones Ortogonales}
Sea $\mathbf{X} \in \mathbb{R}^{T \times k}$ con $\text{rango}(\mathbf{X}) = k$. Su factorizacion QR es $\mathbf{X} = \mathbf{Q}\mathbf{R}$, donde $\mathbf{Q} \in \mathbb{R}^{T \times k}$ satisface $\mathbf{Q}^T\mathbf{Q} = \mathbf{I}_k$ y $\mathbf{R} \in \mathbb{R}^{k \times k}$ es triangular superior no singular.
La matriz de proyeccion ortogonal de Hilbert sobre el subespacio de regresores es:
\begin{equation}
\mathbf{P}_{\mathbf{X}} = \mathbf{X}(\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T = \mathbf{Q}\mathbf{R}(\mathbf{R}^T\mathbf{Q}^T\mathbf{Q}\mathbf{R})^{-1}\mathbf{R}^T\mathbf{Q}^T = \mathbf{Q}\mathbf{Q}^T
\end{equation}
La matriz aniquiladora de residuos ortogonales es $\mathbf{M}_{\mathbf{X}} = \mathbf{I}_T - \mathbf{P}_{\mathbf{X}} = \mathbf{I}_T - \mathbf{Q}\mathbf{Q}^T$, siendo simetrica e idempotente ($\mathbf{M}_{\mathbf{X}}^2 = \mathbf{M}_{\mathbf{X}}$).

\subsubsection{2. Teorema de Frisch-Waugh-Lovell (FWL)}
En el modelo particionado $\mathbf{y} = \mathbf{X}_1 \boldsymbol{\beta}_1 + \mathbf{X}_2 \boldsymbol{\beta}_2 + \mathbf{e}$, el estimador $\hat{\boldsymbol{\beta}}_2$ satisface:
\begin{equation}
\hat{\boldsymbol{\beta}}_2 = (\mathbf{X}_2^T \mathbf{M}_{\mathbf{X}_1} \mathbf{X}_2)^{-1} \mathbf{X}_2^T \mathbf{M}_{\mathbf{X}_1} \mathbf{y}
\end{equation}
lo cual prueba formalmente que estimar el Beta sistematico de Aluar sobre el mercado internacional aísla el riesgo de mercado tras proyectar ortogonalmente el efecto del riesgo soberano local.

\subsubsection{3. Factorizacion de Cholesky para Variables Correlacionadas}
Para una matriz de covarianzas $\mathbf{\Sigma} \in \mathbb{R}^{n \times n}$ simetrica y definida positiva ($\mathbf{z}^T \mathbf{\Sigma} \mathbf{z} > 0, \, \forall \mathbf{z} \ne \mathbf{0}$), existe una unica matriz triangular inferior $\mathbf{L}$ tal que $\mathbf{\Sigma} = \mathbf{L}\mathbf{L}^T$.
Los coeficientes de la factorizacion se calculan analiticamente:
\begin{equation}
L_{jj} = \sqrt{\Sigma_{jj} - \sum_{k=1}^{j-1} L_{jk}^2}, \quad L_{ij} = \frac{1}{L_{jj}} \left( \Sigma_{ij} - \sum_{k=1}^{j-1} L_{ik}L_{jk} \right), \quad i > j
\end{equation}
Dado un vector de normales estandar independientes $\mathbf{Z} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$, el vector transformado $\mathbf{X} = \mathbf{\mu} + \mathbf{L}\mathbf{Z}$ satisface exactamente $\mathbb{E}[X] = \boldsymbol{\mu}$ y $Cov(\mathbf{X}) = \mathbf{L} \mathbb{E}[\mathbf{Z}\mathbf{Z}^T] \mathbf{L}^T = \mathbf{L}\mathbf{L}^T = \mathbf{\Sigma}$.

\begin{center}
\includegraphics[width=0.88\linewidth, height=4.6cm, keepaspectratio]{theory_charts/teoria_05_algebra_proyecciones_cholesky.png}
\captionof{figure}{Figura Teorica: Geometria de Hilbert de Proyecciones OLS y Factorizacion de Cholesky $\mathbf{\Sigma} = \mathbf{L}\mathbf{L}^T$.}
\end{center}

\subsection{Teoria de Copulas no Lineales y Dependencia Asimetrica de Colas}

\begin{teorema}[Teorema de Sklar (1959)]
Sea $H(x_1, x_2)$ una funcion de distribucion acumulada bivariada con marginales continuas $F_1(x_1)$ y $F_2(x_2)$. Existe una unica copula $C: [0, 1]^2 \to [0, 1]$ tal que:
\begin{equation}
H(x_1, x_2) = C(F_1(x_1), F_2(x_2))
\end{equation}
\end{teorema}

\begin{conceptbox}{Por Que la Copula Gaussiana Falla y Se Requiere la Copula de Clayton ($\lambda_L = 0,38$)}
\textbf{El Engano de la Correlacion Lineal en Tiempos de Crisis:}
\begin{itemize}
    \item La correlacion lineal de Pearson asume relacion simetrica e invariante.
    \item La Copula Gaussiana tiene un coeficiente de dependencia de cola inferior nulo: $\lambda_L = \lim_{u \to 0^+} P(U_2 \le u \mid U_1 \le u) = \mathbf{0}$. Asume que la probabilidad de que colapsen simultaneamente el precio del aluminio y el tipo de cambio argentino es cero.
    \item En la realidad de los mercados emergentes, en momentos de panico global los commodities caen y el riesgo soberano se dispara al mismo tiempo.
    \item La \textbf{Copula de Clayton (Arquimediana)} con generador $\phi(t) = \frac{1}{\theta}(t^{-\theta}-1)$ y parametro calibrado $\theta = 1,2258$ arroja una dependencia de cola inferior de $\mathbf{\lambda_L = 2^{-1/\theta} = 0,380}$. Modela con realismo la probabilidad de crisis sistemicas conjuntas, evitando subestimar las colas de perdida en la simulacion Monte Carlo.
\end{itemize}
\end{conceptbox}

\begin{center}
\includegraphics[width=0.88\linewidth, height=4.6cm, keepaspectratio]{theory_charts/teoria_01_copulas_comparativa.png}
\captionof{figure}{Figura Teorica: Comparativa de Dependencia Extrema: Copula Gaussiana ($\lambda_L=0$) vs. Copula de Clayton ($\lambda_L=0,38$).}
\end{center}

\noindent
\begin{minipage}[b]{0.488\linewidth}
    \centering
    \includegraphics[width=\linewidth, height=4.4cm, keepaspectratio]{figures_pristine/figura_20.png}
    \captionof{figure}{\small Distribucion Monte Carlo y Prob. de Suba vs Spot.}
\end{minipage}\hfill
\begin{minipage}[b]{0.488\linewidth}
    \centering
    \includegraphics[width=\linewidth, height=4.4cm, keepaspectratio]{figures_pristine/figura_21.png}
    \captionof{figure}{\small Intervalos de confianza Monte Carlo: P5, P50 y P95.}
\end{minipage}
\vspace{0.15cm}

\subsection{Calculo Estocastico de Ito, Girsanov y Procesos de Difusion}

\subsubsection{1. Variacion Cuadratica y Lema de Ito}
Para el movimiento browniano $(W_t)_{t \ge 0}$, $[W, W]_t = t \implies (dW_t)^2 = dt, \, dW_t dt = 0, \, (dt)^2 = 0$.
Para toda funcion $f(t, X_t) \in C^{1,2}$:
\begin{equation}
df(t, X_t) = \left( \frac{\partial f}{\partial t} + \mu \frac{\partial f}{\partial x} + \frac{1}{2}\sigma^2 \frac{\partial^2 f}{\partial x^2} \right) dt + \sigma \frac{\partial f}{\partial x} dW_t
\end{equation}

\subsubsection{2. Solucion Exacta de Ornstein-Uhlenbeck}
Sea $dS_t = \kappa(\theta - S_t)dt + \sigma dW_t$. Con factor integrante $e^{\kappa t}$:
\begin{equation}
S_t = S_0 e^{-\kappa t} + \theta(1 - e^{-\kappa t}) + \sigma \int_0^t e^{-\kappa(t - s)} dW_s \implies t_{1/2} = \frac{\ln 2}{\kappa} = \textbf{1,8 anos}
\end{equation}

\begin{conceptbox}{Por Que el Movimiento Browniano Geometrico Falla para el Aluminio (Ornstein-Uhlenbeck)}
\textbf{Fuerzas Economicas de Reversion a la Media en Materias Primas:}
\begin{itemize}
    \item El Movimiento Browniano Geometrico (MBG de Black-Scholes) permite que el precio crezca indefinidamente sin cota superior ni inferior.
    \item En los commodities industriales, el precio esta gobernado por la curva global de costos marginales: si el precio sube a $\text{USD } 4.000/\text{t}$, se reactivan plantas inactivas y la sobreoferta tumba el precio; si cae por debajo de $\text{USD } 1.800/\text{t}$, las fundiciones ineficientes quiebran y la oferta se contrae.
    \item El proceso Ornstein-Uhlenbeck modela la atraccion gravitacional hacia el costo marginal de equilibrio $\theta = \text{USD } 2.450/\text{t}$ con velocidad $\kappa = 0,385$.
\end{itemize}
\end{conceptbox}

\subsubsection{3. Proceso CIR y Demostracion de la Condicion de Feller}
Sea $dr_t = \kappa(\theta - r_t)dt + \sigma \sqrt{r_t} dW_t$. La escala de Feller satisface $s'(x) = x^{-\frac{2\kappa\theta}{\sigma^2}} e^{\frac{2\kappa}{\sigma^2}x}$.
La integral $\int_0^{x_0} s'(y)dy$ diverge en el origen si y solo si $\frac{2\kappa\theta}{\sigma^2} \ge 1 \iff \mathbf{2\kappa\theta \ge \sigma^2}$.
En Aluar: $2(0,85)(0,0441) = \textbf{0,0750} > (0,12)^2 = \textbf{0,0144}$ ($\checkmark$ frontera $0$ estrictamente inaccesible).

\begin{center}
\includegraphics[width=0.88\linewidth, height=4.6cm, keepaspectratio]{theory_charts/teoria_02_sde_difusiones.png}
\captionof{figure}{Figura Teorica: Trayectorias Estocasticas de Ornstein-Uhlenbeck (LME) y Proceso CIR con Condicion de Feller.}
\end{center}

\noindent
\begin{minipage}[b]{0.488\linewidth}
    \centering
    \includegraphics[width=\linewidth, height=4.4cm, keepaspectratio]{figures_pristine/figura_26.png}
    \captionof{figure}{\small Proceso Ornstein-Uhlenbeck LME (Cono 90\%) vs MBG.}
\end{minipage}\hfill
\begin{minipage}[b]{0.488\linewidth}
    \centering
    \includegraphics[width=\linewidth, height=4.4cm, keepaspectratio]{figures_pristine/figura_29.png}
    \captionof{figure}{\small Difusion CIR vs Vasicek para curva de tasas y EMBI+.}
\end{minipage}
\vspace{0.15cm}

\begin{center}
\includegraphics[width=0.88\linewidth, height=4.5cm, keepaspectratio]{figures_pristine/figura_31.png}
\captionof{figure}{Evaluacion estocastica del precio objetivo bajo dependencia asimetrica de Copula de Clayton (P5 Clayton ARS 750 vs. Mediana ARS 1.235).}
\end{center}

\begin{codebox}{{engine\_valuacion.py:m9\_monte\_carlo() -- Simulacion Estocastica Vectorial}}
\textbf{Codigo Fuente Real en Python:}
\begin{verbatim}
def m9_monte_carlo(cc, pro, mkt, dn, est, n_sim=20000, semilla=42) -> dict:
    # Motor de Monte Carlo multivariado con distribuciones pesadas y consistencia macro
    rng = np.random.default_rng(semilla)
    wacc, g = cc["wacc"], cc["g_perpetuidad"]
    sd_ke = cc["beta_se"] * cc["erp"]
    sd_wacc = float(np.sqrt((sd_ke * cc["e_sobre_v"]) ** 2))
    sd_g = 0.005

    # 1. Muestreo de colas pesadas bajo Student-t con nu = 4.2 grados de libertad
    NU_STUDENT_T = 4.2
    _t_scale = np.sqrt((NU_STUDENT_T - 2.0) / NU_STUDENT_T)
    w = wacc + sd_wacc * rng.standard_t(NU_STUDENT_T, n_sim) * _t_scale
    gg = g + sd_g * rng.standard_t(NU_STUDENT_T, n_sim) * _t_scale
    shock = rng.normal(0.0, est["sd_shock_margen"], n_sim)

    # 2. Filtrado de convergencia analitica (WACC - g > 1%)
    valido = (w - gg) > 0.01
    w, gg, shock = w[valido], gg[valido], shock[valido]
    n_v = len(w)

    # 3. Proyeccion estocastica y puente de valor
    fcff_base = pro["fcff_terminal_normalizado"] * (1.0 + shock)
    pv_tv = (fcff_base * (1.0 + gg) / (w - gg)) / ((1.0 + w) ** 4.5)
    pv_exp = float(np.sum(pro["fcff"] / ((1.0 + wacc) ** np.array([0.5, 1.5, 2.5, 3.5, 4.5]))))
    ev = pv_exp + pv_tv
    eq = np.maximum(ev - float(dn["deuda_neta_estructural"]), 0.0)
    target_ars = np.maximum(eq / mkt["acciones_mm"] * mkt["ccl"], 0.0)
    
    return {"media": float(target_ars.mean()), "p5": float(np.percentile(target_ars, 5)),
            "p50": float(np.median(target_ars)), "p95": float(np.percentile(target_ars, 95))}
\end{verbatim}
\textbf{Analisis de Sintaxis y Econometria:}
\begin{itemize}
    \item \texttt{rng.standard\_t(NU\_STUDENT\_T, n\_sim)}: Muestrea perturbaciones con exceso de curtosis ($K=8,41$).
    \item \texttt{valido = (w - gg) > 0.01}: Impone la condicion necesaria para la convergencia de Gordon-Shapiro.
\end{itemize}
\end{codebox}
\clearpage
"""
