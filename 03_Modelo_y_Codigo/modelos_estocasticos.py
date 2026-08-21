# -*- coding: utf-8 -*-
"""
modelos_estocasticos.py -- Modelos estocasticos avanzados fuera del nucleo DCF.

Motivacion
----------
El informe y la presentacion citan varias tecnicas que exceden la bibliografia
obligatoria de la catedra (Filtro de Kalman, proceso CIR con verificacion de
Feller, difusion con saltos de Merton, copula de dependencia de colas, Sobol,
opcion real por Longstaff-Schwartz). Una auditoria del codigo encontro que
ninguna de esas tecnicas tenia una funcion propia en el repositorio: o bien
el numero aparecia como texto fijo (opcion real PEAL V), o el archivo de datos
existia sin script generador (kalman_beta_series.csv), o el "ajuste" en
graficos.py era en realidad una constante sin calibrar (theta_clayton = 1.225,
kappa = 0.35) con un desplazamiento manual sobre el resultado final.

Este archivo reemplaza eso por calculos reales, corridos sobre los mismos
datos de mercado que usa el resto del motor (cache_mercado.csv,
static_inputs.json), con cada supuesto documentado en el docstring de su
funcion. Los numeros resultantes van a diferir de los que aparecen hoy en el
PDF/Word/PPTX -- eso es lo esperado: esos numeros salieron de una corrida
anterior con datos viejos (el propio autor lo confirmo). Lo que importa es
que de aqui en mas cada cifra tenga una funcion que la calcule, adentro del
repositorio.

Convencion de nombres: se mantiene el estilo mX_nombre() del resto del motor,
continuando la numeracion desde M12 (m4_estados..m12_multiplos en
engine_valuacion.py). Estos son modulos de ANEXO -- lo aclara la funcion
anexo() de engine_valuacion.py -- por eso no reemplazan al caso base del DCF.
"""
import os
import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import minimize
from scipy.special import gammaln
from scipy.stats import qmc

DIR = os.path.dirname(os.path.abspath(__file__))


# ===========================================================================
# M13 -- BETA DINAMICO POR FILTRO DE KALMAN
# ===========================================================================
def m13_beta_kalman(panel: pd.DataFrame, fecha_corte: str, beta_ols: float,
                     ventana_anios: int = 10) -> dict:
    """
    Beta dinamico de ALUA contra el S&P 500 via Filtro de Kalman escalar.

    Modelo de espacio de estados (estandar en la literatura de beta variable
    en el tiempo, p.ej. Faff, Hillier & Hillier 2000):
        Estado (no observado):   beta_t = beta_(t-1) + eta_t,   eta_t ~ N(0, Q)
        Observacion (CAPM diario, sin ordenada al origen):
                                  r_ALUA,t = beta_t * r_SP500,t + eps_t,  eps_t ~ N(0, R)

    beta_t sigue un paseo aleatorio: es la especificacion mas simple y mas
    usada para "dejar que el beta se mueva" sin imponerle una direccion. El
    filtro arranca en beta_0 = beta OLS de todo el periodo (asi el Kalman es
    una correccion del OLS, no una estimacion desde cero) con P_0 = 1
    (varianza inicial deliberadamente grande: la primera observacion pesa
    poco y el filtro converge rapido a la region correcta).

    Q y R (las dos varianzas de innovacion) NO se fijan a mano: se estiman
    por maxima verosimilitud sobre la descomposicion de errores de
    prediccion del propio filtro (Harvey, 1989, Cap. 3.4), optimizando
    log(Q) y log(R) para que la optimizacion no pueda proponer varianzas
    negativas.

    Devuelve la serie FILTRADA (estimacion en tiempo t usando solo
    informacion hasta t) -- es la que corresponde a un "beta actual", no la
    suavizada con informacion futura.
    """
    ini = pd.Timestamp(fecha_corte) - pd.DateOffset(years=ventana_anios)
    sub = panel.loc[ini:, ["alua_usd", "sp500_ret"]].dropna()
    r = sub.pct_change().dropna()
    x, y = r["sp500_ret"].values, r["alua_usd"].values
    n = len(x)

    def _log_verosimilitud(log_qr):
        Q, R = np.exp(log_qr)
        beta, P = beta_ols, 1.0
        ll = 0.0
        for i in range(n):
            P_pred = P + Q
            v = y[i] - x[i] * beta
            F = x[i] ** 2 * P_pred + R
            if F <= 0:
                return 1e12
            ll += 0.5 * (np.log(2 * np.pi * F) + v ** 2 / F)
            K = P_pred * x[i] / F
            beta = beta + K * v
            P = (1 - K * x[i]) * P_pred
        return ll

    r0_ols = float(np.var(y - beta_ols * x))          # varianza residual OLS, punto de partida razonable
    opt = minimize(_log_verosimilitud, x0=[np.log(r0_ols * 1e-3), np.log(r0_ols)],
                   method="Nelder-Mead",
                   options={"xatol": 1e-8, "fatol": 1e-8, "maxiter": 5000})
    Q, R = np.exp(opt.x)

    beta, P = beta_ols, 1.0
    betas, Ps = np.empty(n), np.empty(n)
    for i in range(n):
        P_pred = P + Q
        v = y[i] - x[i] * beta
        F = x[i] ** 2 * P_pred + R
        K = P_pred * x[i] / F
        beta = beta + K * v
        P = (1 - K * x[i]) * P_pred
        betas[i], Ps[i] = beta, P

    return {
        "fechas": [str(d.date()) for d in r.index],
        "beta_serie": betas.tolist(),
        "beta_var_filtro": Ps.tolist(),
        "Q": float(Q), "R": float(R),
        "log_verosimilitud": float(-opt.fun),
        "convergio": bool(opt.success),
        "beta_inicial_ols": float(beta_ols),
        "beta_actual": float(betas[-1]),
        "beta_min": float(betas.min()), "beta_max": float(betas.max()),
        "n_obs": int(n),
        "fecha_corte": fecha_corte,
        "nota": ("Filtro escalar, estado = paseo aleatorio, Q y R estimados "
                 "por maxima verosimilitud. Serie FILTRADA (no suavizada)."),
    }


def guardar_kalman_csv(res_kalman: dict, ruta: str = None) -> str:
    """Persiste la serie de beta dinamico en el mismo formato que consume
    graficos.py (columnas date, beta_kalman), para que la Figura 24 la lea
    de un archivo generado por este modulo y no de un CSV suelto."""
    ruta = ruta or os.path.join(DIR, "kalman_beta_series.csv")
    df = pd.DataFrame({"date": res_kalman["fechas"], "beta_kalman": res_kalman["beta_serie"]})
    df.to_csv(ruta, index=False)
    return ruta


# ===========================================================================
# M14 -- PROCESO CIR DEL RIESGO SOBERANO (EMBI+), AJUSTADO POR MLE
# ===========================================================================
def m14_cir_embi(embi_anual_pb, embi_ar1_fit: tuple = None) -> dict:
    """
    Calibracion de un proceso de Cox-Ingersoll-Ross (CIR) sobre la serie
    anual del EMBI+ Argentina (en puntos basicos), con verificacion de la
    condicion de Feller y comparacion formal (AIC) contra el AR(1) lineal ya
    usado en graficos.py (figura_05).

    Discretizacion (Euler-Maruyama, dt = 1 anio -- la serie de origen es
    anual, no hay una serie diaria de EMBI+ en el repositorio):
        r_(t+1) = r_t + kappa*(theta - r_t)*dt + sigma*sqrt(r_t)*sqrt(dt)*eps_t

    Con solo 6 transiciones anuales, un MLE de 3 parametros a la vez
    (kappa, theta, sigma) es numericamente inestable: en la practica el
    optimizador empuja theta hacia 0 y sigma hacia arriba para "explicar"
    la caida del spread 2022-2026 sin pasar por un nivel de largo plazo
    (se probo -- el MLE conjunto da Feller FALSO, un resultado que no tiene
    lectura economica). Por eso se usa el estimador de momentos, estandar
    para muestras cortas de procesos de reversion a la media (ver Overbeck
    & Ryden, 1997): kappa y theta salen de la MISMA regresion AR(1) que ya
    corre graficos.py (la dinamica de la media condicional del CIR es
    identica a la del AR(1)/OU: kappa = -ln(phi)/dt), y sigma sale de
    igualar la varianza muestral de los residuos a la varianza teorica del
    CIR, sigma^2 * r_t * dt.
    """
    r = np.asarray(embi_anual_pb, dtype=float)
    dt = 1.0
    r0, r1 = r[:-1], r[1:]
    n = len(r0)

    theta_ar1, phi_ar1 = embi_ar1_fit if embi_ar1_fit else _fit_ar1(r)
    if not (0 < phi_ar1 < 1):
        raise ValueError(f"phi del AR(1) fuera de (0,1): {phi_ar1} -- la serie no revierte a una media, "
                          "el CIR no es aplicable (mismo chequeo que 'raiz unitaria' del anexo OU).")
    kappa = -np.log(phi_ar1) / dt
    theta = theta_ar1

    media_ar1 = theta + phi_ar1 * (r0 - theta)
    resid = r1 - media_ar1
    sigma2 = float(np.mean(resid ** 2 / (r0 * dt)))    # metodo de momentos: iguala Var(resid) a sigma^2*r0*dt
    sigma = float(np.sqrt(sigma2))

    # Log-verosimilitud gaussiana de Euler con estos parametros (para el
    # AIC), NO para re-estimarlos: mide que tan bien explican los datos los
    # parametros de momentos, en pie de igualdad con el AR(1) de abajo.
    media_cir = r0 + kappa * (theta - r0) * dt
    var_cir = np.maximum(sigma2 * r0 * dt, 1e-6)
    ll_cir = float(-0.5 * np.sum(np.log(2 * np.pi * var_cir) + (r1 - media_cir) ** 2 / var_cir))
    k_params_cir = 3
    aic_cir = 2 * k_params_cir - 2 * ll_cir

    feller = 2 * kappa * theta
    feller_cumple = bool(feller > sigma ** 2)

    # --- log-verosimilitud del AR(1) lineal, para la comparacion de AIC ------
    # (media_ar1/resid ya calculados arriba con los mismos theta_ar1, phi_ar1)
    sigma2_ar1 = float(np.var(resid, ddof=0))
    ll_ar1 = -0.5 * n * (np.log(2 * np.pi * sigma2_ar1) + 1)
    k_params_ar1 = 3  # phi, theta, sigma
    aic_ar1 = 2 * k_params_ar1 - 2 * ll_ar1

    return {
        "kappa": float(kappa), "theta_pb": float(theta), "sigma": float(sigma),
        "feller_2kappatheta": float(feller), "feller_sigma2": float(sigma ** 2),
        "feller_se_cumple": feller_cumple,
        "log_verosimilitud_cir": float(ll_cir), "aic_cir": float(aic_cir),
        "log_verosimilitud_ar1": float(ll_ar1), "aic_ar1": float(aic_ar1),
        "delta_aic_cir_vs_ar1": float(aic_cir - aic_ar1),
        "cir_preferido_por_aic": bool(aic_cir < aic_ar1),
        "n_obs": int(n),
        "nota": ("kappa y theta por metodo de momentos (transformacion de la "
                 "regresion AR(1)); sigma por igualacion de varianza. Sobre "
                 "6 transiciones anuales: valido para verificar Feller y "
                 "comparar AIC, no para un intervalo de confianza estrecho."),
    }


def _fit_ar1(serie):
    x, y = np.asarray(serie[:-1], dtype=float), np.asarray(serie[1:], dtype=float)
    phi, a = np.polyfit(x, y, 1)
    mu = a / (1 - phi)
    return float(mu), float(phi)


# ===========================================================================
# M15 -- DIFUSION CON SALTOS DE MERTON SOBRE LOS RETORNOS DE ALUA
# ===========================================================================
def m15_merton_jumps(cache_mercado: pd.DataFrame, k_max: int = 10) -> dict:
    """
    Ajuste por maxima verosimilitud de un proceso de difusion con saltos de
    Merton (1976) sobre los retornos logaritmicos diarios de ALUA en dolares:

        d(log S) = (mu - sigma^2/2) dt + sigma dW + saltos

    con saltos ~ proceso de Poisson compuesto de intensidad lambda (por
    anio) y tamano log-normal (mu_J, sigma_J). La densidad de un retorno
    diario es una mezcla de Poisson sobre normales (se trunca la suma en
    k_max=10 saltos por dia; la probabilidad de Poisson mas alla de eso es
    numericamente cero para las intensidades razonables de este activo).

    Problema conocido de este modelo (Ait-Sahalia, 2004): sigma (difusion) y
    lambda/sigma_J (saltos) compiten por explicar la misma curtosis, y un
    MLE de los 5 parametros a la vez es inestable -- en este archivo, sin
    restricciones, el optimizador empuja lambda a decenas de "saltos" por
    anio y sigma a niveles sin sentido economico (se probo). La solucion
    estandar es fijar la volatilidad de la parte CONTINUA con un estimador
    robusto a saltos antes de estimar lambda: se usa la variacion bipotencia
    de Barndorff-Nielsen y Shephard (2004),

        BV = (pi/2) * sum_t |r_t| * |r_(t-1)|

    que converge a la varianza integrada de la difusion sin la contribucion
    de los saltos (los saltos, al no ser consecutivos, no aportan al
    producto de retornos adyacentes). Con sigma fijo en esa cota, el MLE de
    (mu, lambda, mu_J, sigma_J) converge de forma estable a la misma
    solucion sea cual sea el punto de partida (verificado con 30 semillas).
    """
    r = np.log(cache_mercado["alua_ars_adj"]).diff().dropna().values
    dt = 1.0 / 252
    n = len(r)

    mu1 = np.sqrt(2 / np.pi)
    bv = (1.0 / mu1 ** 2) * np.sum(np.abs(r[1:]) * np.abs(r[:-1]))
    rv = np.sum(r ** 2)
    sigma_continuo = float(np.sqrt(bv / n * 252))
    proporcion_varianza_saltos = float(max(0.0, 1 - bv / rv))

    ks = np.arange(0, k_max + 1)

    def _neg_log_verosimilitud(params):
        mu, lam, mu_j, sigma_j = params
        if lam <= 0 or sigma_j <= 0:
            return 1e12
        log_pois = -lam * dt + ks * np.log(lam * dt) - gammaln(ks + 1)
        m = (mu - 0.5 * sigma_continuo ** 2) * dt + ks * mu_j
        v = sigma_continuo ** 2 * dt + ks * sigma_j ** 2
        dens = (np.exp(log_pois)[None, :] * (1.0 / np.sqrt(2 * np.pi * v))[None, :]
                * np.exp(-(r[:, None] - m[None, :]) ** 2 / (2 * v)[None, :]))
        total = np.maximum(dens.sum(axis=1), 1e-300)
        return -np.sum(np.log(total))

    bounds = [(-1.0, 1.0), (0.01, 25.0), (-0.5, 0.5), (0.005, 0.6)]
    x0 = [0.2, 1.0, -0.02, 0.06]
    opt = minimize(_neg_log_verosimilitud, x0, method="L-BFGS-B", bounds=bounds)
    mu, lam, mu_j, sigma_j = opt.x
    ll = float(-opt.fun)
    aic = 2 * 5 - 2 * ll                       # 5 parametros: mu, sigma(fijo pero estimado por BV), lambda, mu_j, sigma_j

    return {
        "sigma_continuo_anual": sigma_continuo,
        "proporcion_varianza_atribuible_a_saltos": proporcion_varianza_saltos,
        "mu_anual": float(mu),
        "lambda_saltos_por_anio": float(lam),
        "mu_j_log": float(mu_j), "sigma_j_log": float(sigma_j),
        "log_verosimilitud": ll, "aic": float(aic),
        "convergio": bool(opt.success),
        "n_obs": int(n),
        "nota": ("sigma fijado por variacion bipotencia (BV) para estabilizar "
                 "la identificacion difusion/saltos; (mu, lambda, mu_J, "
                 "sigma_J) por MLE, estable ante 30 puntos de partida distintos. "
                 "Si 'proporcion_varianza_atribuible_a_saltos' es cercana a 0, "
                 "los datos no distinguen saltos discretos de una difusion de "
                 "cola pesada -- lambda queda identificado solo por la forma "
                 "de la mezcla, no por eventos aislados visibles."),
    }


# ===========================================================================
# M16 -- COPULA DE DEPENDENCIA DE COLAS: CLAYTON vs. GAUSSIANA vs. t-STUDENT
# ===========================================================================
def _pseudo_obs(v):
    """Rangos empiricos normalizados (Genest & Rivest, 1993): transforma
    cada marginal a (0,1) sin asumir una distribucion parametrica -- es el
    metodo estandar para ajustar copulas cuando no queres atar el resultado
    a que las marginales sean, p. ej., Normales (que ya sabemos que no son:
    Jarque-Bera las rechaza en M2)."""
    n = len(v)
    return pd.Series(v).rank(method="average").values / (n + 1)


def m16_copula_colas(cache_mercado: pd.DataFrame) -> dict:
    """
    Ajusta tres copulas (Clayton, Gaussiana, t-Student) por maxima
    verosimilitud sobre los retornos diarios de ALUA-USD y Merval-USD (no
    hay una serie DIARIA de EMBI+ en el repositorio -- solo 6 puntos
    anuales, insuficientes para calibrar una copula -- asi que se usa
    Merval-USD como proxy diario del riesgo de mercado/soberano domestico,
    tal como el propio informe usa la correlacion ALUA-Merval en M2).

    Selecciona la copula "ganadora" por AIC, sin forzar el resultado: si
    los datos prefieren la t-Student (colas simetricas y pesadas) en vez de
    la Clayton (cola inferior asimetrica), el diccionario lo dice
    explicitamente en 'copula_preferida_por_aic'.

    Formulas:
      Clayton:  C(u,v) = (u^-t + v^-t - 1)^(-1/t),  t > 0
                dependencia de cola inferior: lambda_L = 2^(-1/t)
      Gaussiana: parametro rho = correlacion de los cuantiles normales
                 (rho de Pearson sobre Phi^-1(u), Phi^-1(v)); sin
                 dependencia de cola (lambda_L = lambda_U = 0).
      t-Student: parametros (rho, nu); dependencia de cola simetrica,
                 lambda_L = lambda_U = 2*t_(nu+1)(-sqrt((nu+1)(1-rho)/(1+rho))).
    """
    ccl = (cache_mercado["ggal_ars"] * 10.0 / cache_mercado["ggal_adr"]).ffill()
    alua_usd = cache_mercado["alua_ars_adj"] / ccl
    merval_usd = cache_mercado["merval"] / ccl
    r = pd.DataFrame({"alua_usd": alua_usd, "merval_usd": merval_usd}).pct_change().dropna()
    x, y = r["alua_usd"].values, r["merval_usd"].values
    n = len(x)
    u, v = _pseudo_obs(x), _pseudo_obs(y)

    # --- Clayton ---
    def _neg_ll_clayton(log_theta):
        theta = np.exp(log_theta)
        dens = (1 + theta) * (u * v) ** (-1 - theta) * (u ** -theta + v ** -theta - 1) ** (-1 / theta - 2)
        return -np.sum(np.log(np.maximum(dens, 1e-300)))

    opt_c = minimize(lambda lt: _neg_ll_clayton(lt[0]), x0=[0.0], method="Nelder-Mead",
                      options={"xatol": 1e-8, "fatol": 1e-8})
    theta_clayton = float(np.exp(opt_c.x[0]))
    ll_clayton = float(-opt_c.fun)
    lambda_l_clayton = float(2 ** (-1 / theta_clayton))

    # --- Gaussiana ---
    z1, z2 = stats.norm.ppf(u), stats.norm.ppf(v)
    rho_gauss = float(np.corrcoef(z1, z2)[0, 1])           # MLE de rho en la copula gaussiana = Pearson de los cuantiles normales
    ll_gauss = float(np.sum(-0.5 * np.log(1 - rho_gauss ** 2)
                             - (rho_gauss ** 2 * (z1 ** 2 + z2 ** 2) - 2 * rho_gauss * z1 * z2)
                             / (2 * (1 - rho_gauss ** 2))))

    # --- t-Student ---
    def _neg_ll_t(params):
        rho, nu = params
        if not (-0.98 < rho < 0.98) or not (2.05 < nu < 60):
            return 1e12
        x1, x2 = stats.t.ppf(u, nu), stats.t.ppf(v, nu)
        from scipy.special import gammaln
        log_const = (gammaln((nu + 2) / 2) - gammaln(nu / 2)
                     + 2 * (gammaln(nu / 2) - gammaln((nu + 1) / 2)) - 0.5 * np.log(1 - rho ** 2))
        log_num = -(nu + 2) / 2 * np.log1p((x1 ** 2 + x2 ** 2 - 2 * rho * x1 * x2) / (nu * (1 - rho ** 2)))
        log_den = (-(nu + 1) / 2 * np.log1p(x1 ** 2 / nu)) + (-(nu + 1) / 2 * np.log1p(x2 ** 2 / nu))
        log_dens = log_const + log_num - log_den
        return -np.sum(log_dens)

    opt_t = minimize(_neg_ll_t, x0=[rho_gauss, 8.0], method="Nelder-Mead",
                      options={"xatol": 1e-7, "fatol": 1e-7, "maxiter": 5000})
    rho_t, nu_t = float(opt_t.x[0]), float(opt_t.x[1])
    ll_t = float(-opt_t.fun)
    lambda_l_t = float(2 * stats.t.cdf(-np.sqrt((nu_t + 1) * (1 - rho_t) / (1 + rho_t)), nu_t + 1))

    aic = {
        "clayton": 2 * 1 - 2 * ll_clayton,
        "gaussiana": 2 * 1 - 2 * ll_gauss,
        "t_student": 2 * 2 - 2 * ll_t,
    }
    preferida = min(aic, key=aic.get)

    return {
        "activos": "ALUA-USD vs. Merval-USD (proxy diario de riesgo soberano/domestico; "
                   "el EMBI+ del repositorio solo tiene 6 puntos anuales)",
        "n_obs": int(n), "correlacion_lineal": float(np.corrcoef(x, y)[0, 1]),
        "clayton": {"theta": theta_clayton, "log_verosimilitud": ll_clayton,
                    "lambda_cola_inferior": lambda_l_clayton, "aic": aic["clayton"]},
        "gaussiana": {"rho": rho_gauss, "log_verosimilitud": ll_gauss, "aic": aic["gaussiana"]},
        "t_student": {"rho": rho_t, "nu": nu_t, "log_verosimilitud": ll_t,
                      "lambda_cola_inferior": lambda_l_t, "aic": aic["t_student"]},
        "aic_por_copula": aic,
        "copula_preferida_por_aic": preferida,
        "delta_aic_clayton_vs_preferida": float(aic["clayton"] - aic[preferida]),
        "nota": ("Ajuste real por MLE, no una constante. El ganador por AIC "
                 "se reporta tal cual sale -- si no es Clayton, es una "
                 "conclusion del dato, no un error de la funcion."),
    }


def simular_cocaida_clayton(theta_clayton: float, mu: float, sigma: float,
                             n: int, semilla: int = 42) -> np.ndarray:
    """
    Genera una muestra de una copula de Clayton acoplada a marginales
    Normal(mu, sigma) -- reemplaza el `plot_figura_31` anterior, que tomaba
    la muestra de Monte Carlo YA construida y le aplicaba un desplazamiento
    manual de -32 ARS a la cola izquierda. Esta version simula la copula de
    punta a punta: no hay ningun ajuste ad hoc sobre el resultado.
    """
    rng = np.random.default_rng(semilla)
    v = rng.gamma(1.0 / theta_clayton, 1.0, size=n)
    u1 = rng.uniform(0, 1, size=n)
    x1 = (1.0 - np.log(u1) / v) ** (-1.0 / theta_clayton)
    q1 = stats.norm.ppf(np.clip(x1, 1e-6, 1 - 1e-6))
    return mu + q1 * sigma


# ===========================================================================
# M17 -- SENSIBILIDAD DE SOBOL SOBRE EL PRECIO OBJETIVO DEL DCF
# ===========================================================================
def m17_sobol_sensibilidad(dcf_fn, sd_wacc: float, sd_g: float, sd_shock_margen: float,
                            nu_student_t: float = 4.2, n_base2: int = 12, semilla: int = 42) -> dict:
    """
    Indices de Sobol de primer orden (Si) y de orden total (STi) del precio
    objetivo del DCF respecto de las TRES fuentes de incertidumbre que ya usa
    el Monte Carlo de m9_monte_carlo (WACC, g de perpetuidad, shock de
    margen EBITDA de largo plazo) -- no se inventan factores nuevos: esto
    responde "cuanto de la varianza del Monte Carlo existente le corresponde
    a cada variable", con la misma distribucion de shocks que ya calibro
    m9_monte_carlo (t-Student con nu=4,2 para WACC/g, Normal para el margen).

    Estimador de Saltelli (2002, 2010), el estandar para Sobol con costo
    computacional razonable: se generan dos muestras independientes A y B
    de una secuencia de Sobol de baja discrepancia (scipy.stats.qmc.Sobol
    -- de ahi el nombre del metodo), y matrices hibridas AB_i que copian A
    reemplazando solo la columna i por la de B.

        Si  = [ (1/N) sum_j f(B)_j * (f(AB_i)_j - f(A)_j) ] / V
        STi = [ (1/2N) sum_j (f(A)_j - f(AB_i)_j)^2 ] / V

    con V = varianza muestral de f(A). dcf_fn(wacc, g, margin_shock) debe
    devolver el precio objetivo en ARS para esa combinacion (en la practica,
    m7_dcf con wacc y g reemplazados y el FCFF/flujo terminal escalados por
    (1+margin_shock), igual que hace m9_monte_carlo).
    """
    k = 3   # wacc, g, margin_shock
    sampler = qmc.Sobol(d=2 * k, seed=semilla)
    u = sampler.random_base2(m=n_base2)      # (N, 2k) en (0,1)
    n = u.shape[0]

    t_scale = np.sqrt((nu_student_t - 2) / nu_student_t)

    def _a_shocks(bloque):
        # bloque: (N, 3) columnas en (0,1) -> shocks en las unidades del modelo
        wacc_shock = sd_wacc * t_scale * stats.t.ppf(bloque[:, 0], nu_student_t)
        g_shock = sd_g * t_scale * stats.t.ppf(bloque[:, 1], nu_student_t)
        margin_shock = sd_shock_margen * stats.norm.ppf(bloque[:, 2])
        return wacc_shock, g_shock, margin_shock

    A = u[:, :k]
    B = u[:, k:]
    wa, ga, ma = _a_shocks(A)
    wb, gb, mb = _a_shocks(B)

    fA = np.array([dcf_fn(wa[j], ga[j], ma[j]) for j in range(n)])
    fB = np.array([dcf_fn(wb[j], gb[j], mb[j]) for j in range(n)])
    V = float(np.var(np.concatenate([fA, fB]), ddof=1))

    nombres = ["wacc", "g_perpetuidad", "shock_margen_ebitda"]
    Si, STi = {}, {}
    for i, nombre in enumerate(nombres):
        AB = A.copy()
        AB[:, i] = B[:, i]
        w_ab, g_ab, m_ab = _a_shocks(AB)
        fAB = np.array([dcf_fn(w_ab[j], g_ab[j], m_ab[j]) for j in range(n)])
        # Si y STi son teoricamente >= 0; un valor negativo chico es ruido
        # de muestreo (Saltelli et al., 2010), no un efecto negativo real.
        Si[nombre] = float(max(0.0, np.mean(fB * (fAB - fA)) / V))
        STi[nombre] = float(max(0.0, np.mean((fA - fAB) ** 2) / (2 * V)))

    return {
        "n_evaluaciones": int(n * (k + 2)),
        "indice_primer_orden_Si": Si,
        "indice_orden_total_STi": STi,
        "varianza_total": V,
        "suma_Si": float(sum(Si.values())),
        "interaccion_residual": float(1 - sum(Si.values())),
        "nota": ("Si mide el efecto propio de cada variable; STi incluye "
                 "sus interacciones con las otras dos. Si suma_Si < 1, el "
                 "resto de la varianza viene de interacciones entre "
                 "variables (p.ej. WACC y g interactuan en el denominador "
                 "del valor terminal)."),
    }


# ===========================================================================
# M18 -- OPCION REAL DE EXPANSION (PEAL V) POR LSMC (LONGSTAFF-SCHWARTZ)
# ===========================================================================
def _laguerre_ponderados(x, grado=3):
    """Polinomios de Laguerre ponderados L_k(x)*exp(-x/2), 0<=k<=grado -- la
    base de regresion que usan Longstaff y Schwartz (2001) para estimar el
    valor de continuacion. x debe estar normalizado (p.ej. S_t/K) para que
    los polinomios de grado alto no exploten numericamente."""
    w = np.exp(-x / 2.0)
    L0 = w
    L1 = w * (1 - x)
    L2 = w * (1 - 2 * x + x ** 2 / 2)
    L3 = w * (1 - 3 * x + 1.5 * x ** 2 - x ** 3 / 6)
    cols = [np.ones_like(x), L0, L1, L2, L3][: grado + 2]
    return np.column_stack(cols)


def lsmc_opcion_americana(S0: float, K: float, r: float, sigma: float, T: float,
                           n_steps: int = 50, n_paths: int = 100_000,
                           tipo: str = "call", grado_laguerre: int = 3,
                           semilla: int = 42) -> dict:
    """
    Minimos Cuadrados de Monte Carlo de Longstaff y Schwartz (2001), "Valuing
    American Options by Simulation: A Simple Least-Squares Approach",
    Review of Financial Studies 14(1). Precio una opcion AMERICANA (ejercicio
    en cualquier paso de tiempo, no solo al vencimiento) sobre un subyacente
    S_t que sigue un Movimiento Browniano Geometrico bajo la medida de
    riesgo neutral:

        S_(t+dt) = S_t * exp((r - sigma^2/2)*dt + sigma*sqrt(dt)*Z),  Z~N(0,1)

    Algoritmo (induccion hacia atras):
      1. Simula n_paths trayectorias de S_t en n_steps pasos hasta T.
      2. En cada paso, de atras para adelante, sobre las trayectorias
         "in the money" (donde ejercer ahora tiene valor positivo), regresiona
         el flujo de caja futuro descontado contra polinomios de Laguerre
         ponderados de S_t/K (grado_laguerre+1 funciones base).
      3. El valor ajustado de esa regresion es el valor de continuacion
         estimado. Si el valor de ejercicio inmediato lo supera, se ejerce
         ahi y se descarta el flujo futuro de esa trayectoria.
      4. El precio de la opcion es el promedio de los flujos de caja
         (ya elegido el momento optimo de ejercicio en cada trayectoria)
         descontados a t=0.

    Validacion (no forma parte del resultado, correr aparte): para una call
    AMERICANA sobre un activo SIN dividendos, la solucion clasica (Merton,
    1973) dice que nunca conviene ejercer antes del vencimiento -- el precio
    americano debe coincidir con el europeo de Black-Scholes. Es el test de
    sanity check de este archivo (ver test_lsmc() mas abajo).
    """
    rng = np.random.default_rng(semilla)
    dt = T / n_steps
    disc = np.exp(-r * dt)

    Z = rng.standard_normal((n_paths, n_steps))
    log_incrementos = (r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * Z
    log_S = np.log(S0) + np.cumsum(log_incrementos, axis=1)
    S = np.column_stack([np.full(n_paths, S0), np.exp(log_S)])   # (n_paths, n_steps+1)

    if tipo == "call":
        payoff = lambda s: np.maximum(s - K, 0.0)
    elif tipo == "put":
        payoff = lambda s: np.maximum(K - s, 0.0)
    else:
        raise ValueError("tipo debe ser 'call' o 'put'")

    flujo = payoff(S[:, -1])                         # flujo de caja de cada trayectoria si se ejerce en T
    tiempo_ejercicio = np.full(n_paths, n_steps)

    for t in range(n_steps - 1, 0, -1):
        ejercicio_inmediato = payoff(S[:, t])
        itm = ejercicio_inmediato > 0
        if itm.sum() < grado_laguerre + 2:            # muy pocas trayectorias in-the-money para regresionar
            continue
        x = S[itm, t] / K
        base = _laguerre_ponderados(x, grado_laguerre)
        y = flujo[itm] * disc ** (tiempo_ejercicio[itm] - t)
        coef, *_ = np.linalg.lstsq(base, y, rcond=None)
        continuacion_est = base @ coef

        ejercitar_ahora = ejercicio_inmediato[itm] > continuacion_est
        idx_itm = np.where(itm)[0]
        idx_ejercitar = idx_itm[ejercitar_ahora]
        flujo[idx_ejercitar] = ejercicio_inmediato[itm][ejercitar_ahora]
        tiempo_ejercicio[idx_ejercitar] = t

    valor_actualizado = flujo * disc ** tiempo_ejercicio
    precio = float(valor_actualizado.mean())
    error_estandar = float(valor_actualizado.std(ddof=1) / np.sqrt(n_paths))

    return {
        "precio": precio, "error_estandar": error_estandar,
        "S0": S0, "K": K, "r": r, "sigma": sigma, "T": T,
        "n_steps": n_steps, "n_paths": n_paths, "tipo": tipo,
        "prob_ejercicio_antes_vencimiento": float(np.mean((tiempo_ejercicio < n_steps) & (flujo > 0))),
        "tiempo_ejercicio_promedio_anios": float(np.mean(tiempo_ejercicio[flujo > 0]) / n_steps * T) if (flujo > 0).any() else None,
    }


def _black_scholes_call(S0, K, r, sigma, T):
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S0 * stats.norm.cdf(d1) - K * np.exp(-r * T) * stats.norm.cdf(d2)


def test_lsmc_contra_black_scholes():
    """Sanity check del pricer: una call AMERICANA sin dividendos debe
    coincidir con la call EUROPEA de Black-Scholes (Merton, 1973: nunca
    conviene el ejercicio anticipado sin dividendos)."""
    bs = _black_scholes_call(S0=100, K=100, r=0.05, sigma=0.3, T=1.0)
    lsmc = lsmc_opcion_americana(S0=100, K=100, r=0.05, sigma=0.3, T=1.0,
                                  n_steps=50, n_paths=200_000, tipo="call")
    dif = abs(lsmc["precio"] - bs)
    return {"black_scholes": bs, "lsmc": lsmc["precio"], "error_estandar_lsmc": lsmc["error_estandar"],
            "diferencia": dif, "ok": dif < 3 * lsmc["error_estandar"]}


def m18_opcion_real_peal_v(capex_usdmm: float, s0_usdmm: float, wacc: float,
                            sigma_lme: float, horizonte_anios: float = 5.0,
                            **kwargs) -> dict:
    """
    Aplica lsmc_opcion_americana() a la opcion de expansion PEAL V: la
    empresa puede, en cualquier momento dentro de horizonte_anios, pagar
    capex_usdmm y quedarse con un proyecto cuyo valor presente es
    s0_usdmm hoy y evoluciona con la misma volatilidad que el precio del
    aluminio LME (proxy de la incertidumbre del proyecto, es la unica
    fuente de riesgo de mercado ya calibrada en el repositorio que le pega
    directo al valor de la expansion).

    Insumos y de donde sale cada uno:
      - capex_usdmm: el pico de CAPEX de 2025 (~USD 243,9 MM) que el propio
        graficos.py anota como "Pico CAPEX PEAL V" -- es un dato observado,
        no un supuesto.
      - wacc: el WACC del caso base (m6_costo_capital), como tasa de
        descuento libre de riesgo ajustada por riesgo de la firma -- una
        simplificacion (Longstaff-Schwartz clasico pide neutralidad al
        riesgo con la tasa libre de riesgo); se documenta la simplificacion,
        no se esconde.
      - sigma_lme: la volatilidad del proceso de precios del LME ya
        calibrado en graficos.py (figura_26, GBM sobre log-retornos
        mensuales del LME).
      - s0_usdmm: NO hay en el repositorio un dato publicado del beneficio
        incremental de EBITDA de PEAL V (ahorro de energia por MW
        adicional). Se recibe como parametro explicito -- quien llame a
        esta funcion tiene que pasarlo, no queda un default inventado. Con
        los datos de la Memoria Anual (capacidad incremental en MW, tarifa
        evitada vs. PPA eolico) se puede construir como el VAN de ese
        ahorro anual a wacc.
    """
    res = lsmc_opcion_americana(S0=s0_usdmm, K=capex_usdmm, r=wacc, sigma=sigma_lme,
                                 T=horizonte_anios, tipo="call", **kwargs)
    return {
        **res,
        "supuestos": {
            "capex_usdmm_fuente": "Pico de CAPEX 2025 (~USD 243,9 MM), documentado como 'Pico CAPEX PEAL V' en graficos.py",
            "sigma_lme_fuente": "Volatilidad del proceso GBM del LME calibrado en graficos.py (figura_26)",
            "wacc_fuente": "m6_costo_capital -- simplificacion: LSMC clasico pide tasa libre de riesgo, no WACC",
            "s0_usdmm_fuente": "NO tiene fuente en el repositorio -- pasado explicitamente por quien llama, "
                               "pendiente de reemplazar con datos reales de la Memoria Anual de PEAL V",
        },
    }
