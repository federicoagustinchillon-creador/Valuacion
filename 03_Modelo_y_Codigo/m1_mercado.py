# -*- coding: utf-8 -*-
"""
m1_mercado.py — Insumos de mercado y series de precios.

La fecha de corte esta CONGELADA al 23-jul-2026 para que el trabajo sea
reproducible y para que cualquier diferencia contra el trabajo de referencia
sea atribuible al cambio metodologico y no a la deriva de los datos de mercado.

Homogeneizacion de moneda (Dumrauf, Cap. 14):
    CCL_t = Precio GGAL.BA_t x 10 / Precio GGAL_t
    P_USD_t = P_ARS_t / ffill(CCL_t)
El factor 10 es la relacion de conversion del ADR (10 acciones ordinarias por ADR).
"""
import os, json, datetime as dt
import numpy as np
import pandas as pd

DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_CSV = os.path.join(DIR, "cache_mercado.csv")

FECHA_CORTE = "2026-07-23"          # ultima rueda incluida
FECHA_INICIO = "2016-07-01"         # 10 anios de historia

TICKERS = {
    "ALUA.BA": "alua_ars",      # ALUAR en BYMA
    "GGAL.BA": "ggal_ars",      # Galicia local  -> numerador del CCL
    "GGAL":    "ggal_adr",      # Galicia ADR    -> denominador del CCL
    "^MERV":   "merval",        # indice S&P Merval
    "^GSPC":   "sp500",         # S&P 500 (mercado del CAPM)
    "TXAR.BA": "txar_ars",      # Ternium Argentina
    "ALI=F":   "lme",           # futuro de aluminio LME
    "DX-Y.NYB": "dxy",          # indice dolar
    "^TNX":    "us10y",         # rendimiento del Tesoro a 10 anios (x100)
}

# --- Insumos que no provienen de una API de precios -------------------------
ERP_US = 0.0418          # Damodaran (NYU Stern), ERP implicito de EE.UU., julio 2026
ERP_FUENTE = "Damodaran (NYU Stern) — ERP implicito de EE.UU., julio 2026"
EMBI_AR = 0.0441         # 441 pb
EMBI_FUENTE = "J.P. Morgan EMBI+ Argentina — 441 pb, julio 2026"
TASA_IMPOSITIVA = 0.35   # Ley 20.628, alicuota estatutaria de sociedades
ACCIONES_MM = 2800.0     # acciones ordinarias en circulacion, en millones


def _descargar():
    import yfinance as yf
    fin = (pd.Timestamp(FECHA_CORTE) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    raw = yf.download(list(TICKERS), start=FECHA_INICIO, end=fin,
                      progress=False, auto_adjust=False)
    px = raw["Close"].rename(columns=TICKERS)
    # Cierre ajustado por dividendos y splits: es el que corresponde para
    # estimar betas y retornos (Alexander, Sharpe y Bailey, Cap. 8).
    adj = raw["Adj Close"].rename(columns={k: v + "_adj" for k, v in TICKERS.items()})
    px = px.join(adj)
    px = px.loc[:FECHA_CORTE]
    return px


def cargar_series(forzar_descarga=False) -> pd.DataFrame:
    """Devuelve el DataFrame de precios de cierre, usando cache en disco."""
    if os.path.exists(CACHE_CSV) and not forzar_descarga:
        df = pd.read_csv(CACHE_CSV, index_col=0, parse_dates=True)
    else:
        df = _descargar()
        df.to_csv(CACHE_CSV)
    return df


def construir_panel(px: pd.DataFrame) -> pd.DataFrame:
    """Agrega el CCL y las series en dolares al panel de precios."""
    d = px.copy()
    d["ccl"] = (d["ggal_ars"] * 10.0 / d["ggal_adr"])
    d["ccl"] = d["ccl"].ffill()
    # Series en dolares para retornos: se usa el cierre ajustado del activo
    # local dividido por el CCL (el CCL en si no lleva ajuste).
    d["alua_usd"] = d["alua_ars_adj"] / d["ccl"]
    d["txar_usd"] = d["txar_ars_adj"] / d["ccl"]
    d["merval_usd"] = d["merval"] / d["ccl"]
    d["sp500_ret"] = d["sp500_adj"]
    return d


def run(forzar_descarga=False) -> dict:
    px = cargar_series(forzar_descarga)
    d = construir_panel(px)

    ccl = float(d["ccl"].dropna().iloc[-1])
    alua_px = float(d["alua_ars"].dropna().iloc[-1])
    rf = float(d["us10y"].dropna().iloc[-1]) / 100.0

    # --- Beta OLS contra el S&P 500, retornos diarios en dolares, 10 anios --
    # Ventana de 10 anios: es la que valida el test de quiebre estructural de
    # Quandt-Andrews (no hay cambio de regimen dentro de la muestra) y la que
    # da una base rica en eventos de cola para el analisis de riesgo.
    ini_beta = pd.Timestamp(FECHA_CORTE) - pd.DateOffset(years=10)
    sub = d.loc[ini_beta:, ["alua_usd", "sp500_ret"]].dropna()
    r = sub.pct_change().dropna()
    x, y = r["sp500_ret"].values, r["alua_usd"].values
    n = len(x)
    xm, ym = x.mean(), y.mean()
    sxx = ((x - xm) ** 2).sum()
    beta_ols = ((x - xm) * (y - ym)).sum() / sxx
    alpha_ols = ym - beta_ols * xm
    resid = y - (alpha_ols + beta_ols * x)
    s2 = (resid ** 2).sum() / (n - 2)
    beta_se = float(np.sqrt(s2 / sxx))
    r2 = 1 - (resid ** 2).sum() / ((y - ym) ** 2).sum()

    # --- Volatilidad anualizada del Merval en dolares, 2 anios --------------
    ini_2y = pd.Timestamp(FECHA_CORTE) - pd.DateOffset(years=2)
    merv_vol = float(d.loc[ini_2y:, "merval_usd"].pct_change().dropna().std() * np.sqrt(252))

    lme_spot = float(d["lme"].dropna().iloc[-1])

    return {
        "fecha_corte": FECHA_CORTE,
        "rf": rf,
        "rf_fuente": "^TNX (CBOE 10-Year Treasury Note Yield) — ultimo cierre al 23-jul-2026",
        "rm": rf + ERP_US,
        "erp_us": ERP_US,
        "erp_fuente": ERP_FUENTE,
        "embi_ar": EMBI_AR,
        "embi_fuente": EMBI_FUENTE,
        "tasa_impositiva": TASA_IMPOSITIVA,
        "ccl": ccl,
        "ccl_fuente": f"GGAL.BA {float(d['ggal_ars'].dropna().iloc[-1]):,.2f} x 10 / GGAL {float(d['ggal_adr'].dropna().iloc[-1]):,.2f}",
        "alua_px_ars": alua_px,
        "alua_px_usd": alua_px / ccl,
        "acciones_mm": ACCIONES_MM,
        "beta_ols": float(beta_ols),
        "beta_se": beta_se,
        "beta_alpha": float(alpha_ols),
        "beta_r2": float(r2),
        "beta_n_obs": int(n),
        "beta_fuente": "OLS diario 10 anios, ALUA.BA homogeneizada a USD via CCL, contra ^GSPC",
        "merval_vol_anual": merv_vol,
        "lme_spot_usd_tn": lme_spot,
    }


if __name__ == "__main__":
    import pprint
    out = run()
    pprint.pprint(out)
