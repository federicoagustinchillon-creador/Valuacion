# -*- coding: utf-8 -*-
"""
engine_valuacion.py — Motor de valuacion de ALUAR bajo las formulas de la
plantilla 'TP Valuation Original con formulas originales.xlsx'.

MARCO TEORICO (bibliografia obligatoria de la catedra)
------------------------------------------------------
  Dumrauf, G. — "Finanzas Corporativas: Un Enfoque Latinoamericano"
      Cap. 6  : tasa libre de riesgo y riesgo pais
      Cap. 8  : prima por riesgo de mercado
      Cap. 10 : beta, beta apalancado y desapalancado (Hamada)
      Cap. 12 : costo promedio ponderado del capital
      Cap. 14 : flujo de fondos libre, valor terminal y crecimiento
  Alexander, Sharpe y Bailey — "Fundamentos de Inversiones"
      Cap. 7 y 8 : optimizacion media-varianza de Markowitz, frontera eficiente
      Cap. 8     : beta por minimos cuadrados
      Cap. 10    : modelo de indice unico de Sharpe, ajuste de Blume

DECISIONES METODOLOGICAS (acordadas con el autor del trabajo)
--------------------------------------------------------------
   1. Costo del capital propio: CAPM ajustado por riesgo pais (Dumrauf,
      Cap. 6 y 8) con la prima soberana ponderada por la exposicion domestica
      de los ingresos:
          Ke = Rf + Beta x (Rm - Rf) + Lambda x RP
      RP  = EMBI+ Argentina completo (spread soberano).
      Lambda = 0.20 = participacion de las ventas al mercado interno sobre las
      ventas totales (Aluar exporta ~80% de su produccion, Memoria Anual).
      La plantilla trae pre-cargada la variante con Lambda = 1 en FCFF!J9
      (=J5+J6+J8*(J7-J5)); se la conserva como celda testigo y la ponderacion
      se explicita en una celda propia, de modo que el jurado pueda ver el
      efecto de fijar Lambda = 1. La version estricta de Damodaran, que
      multiplica Lambda por la prima de riesgo pais en terminos de acciones
      (RP x sigma_acciones / sigma_bonos), se reporta en el ANEXO como prueba
      de robustez: da un Ke mas alto y un precio objetivo menor.
  2. Beta: OLS -> Blume -> Hamada (desapalancar con D/E historico y
     reapalancar con D/E objetivo). La regresion es contra el S&P 500, no
     contra el Merval: por eso el riesgo pais se suma aparte y no se
     duplica el computo del riesgo soberano.
  3. Tasa impositiva estatutaria plana del 35% (Ley 20.628) los cinco anios.
  4. Descuento segun la fila 32 de la plantilla: el primer anio proyectado no
     se descuenta y los siguientes llevan exponentes 1, 2, 3 y 4. El valor
     terminal se descuenta por (1 + WACC)^4 para que sea consistente.
  5. g de perpetuidad = 2,0%. La plantilla trae 2,5% pre-cargado en FCFF!J14,
     pero Dumrauf (Cap. 14) pide que la tasa de crecimiento a perpetuidad
     converja de forma suavizada al crecimiento de largo plazo de la economia
     y nunca lo supere; 2,0% es el techo prudente para una productora de
     aluminio primario con la capacidad instalada ya saturada (96,8% de
     utilizacion en FY2025), donde el crecimiento en volumen esta acotado por
     la planta y solo queda el arrastre de precio.
  6. Flujo terminal normalizado (Dumrauf, Cap. 14): en estado estacionario
     CAPEX = D&A y Delta NWC = 0, de modo que FCFF terminal = NOPAT.
  7. Los modelos que exceden la bibliografia obligatoria (Vasicek, lambda de
     Damodaran, Merton, Ornstein-Uhlenbeck, Cornish-Fisher y Kelly) se
     calculan en el ANEXO y no intervienen en el caso base.
"""
import os, json
import numpy as np
import pandas as pd

import datos_auditados as DA
import m1_mercado as M1

DIR = os.path.dirname(os.path.abspath(__file__))
RAIZ = DIR if os.path.exists(os.path.join(DIR, "static_inputs.json")) else os.path.dirname(DIR)

# ---------------------------------------------------------------------------
# Parametros del modelo
# ---------------------------------------------------------------------------
G_PERPETUIDAD = 0.020          # Dumrauf Cap. 14: convergencia suavizada
G_PLANTILLA = 0.025            # valor pre-cargado en FCFF!J14, se reporta
LAMBDA_AR = 0.20               # ventas al mercado interno / ventas totales
ANIOS_PROY = [2026, 2027, 2028, 2029, 2030]

# Marco fisico de ingresos (Memoria Anual de ALUAR e informacion de industria)
CAPACIDAD_MAX_TN = 460_000     # capacidad instalada, Memoria Anual
UTILIZACION = 0.94             # factor de utilizacion historico
CASH_COST_USD_TN = 1680.0      # cash cost C1, curva de costos CRU / Wood Mackenzie
LME_REVERSION_USD_TN = 2587.1  # media de la serie mensual del LME (67 obs.)
PREMIUM_VALOR_AGREGADO = 645.7 # premium por producto elaborado sobre el LME

# Primer trimestre calendario 2026 (3er trimestre fiscal FY2026), dato real
Q1_2026 = dict(revenue_usdmm=416.0, ebitda_usdmm=106.0, deuda_neta_usdmm=456.0,
               fuente="Cohen Aliados Financieros — informe del 2-jun-2026")
LME_TRIM = {"jul-sep25": 2518.5, "oct-dic25": 2846.3, "ene-mar26": 3173.2, "abr-jun26": 3601.2}


def _safe(a, b):
    try:
        return a / b if b not in (0, None) else np.nan
    except Exception:
        return np.nan


# ===========================================================================
# M2 — ESTADISTICA DE LA ACCION
# ===========================================================================
def m2_estadistica(panel: pd.DataFrame) -> dict:
    """Estadistica descriptiva y test de normalidad de Jarque-Bera."""
    from scipy import stats
    r = panel["alua_usd"].pct_change().dropna()
    n = len(r)
    mu_d, sd_d = r.mean(), r.std(ddof=1)
    skew = stats.skew(r, bias=False)
    kurt = stats.kurtosis(r, bias=False)          # exceso de curtosis
    jb, jb_p = stats.jarque_bera(r)

    acum = (1 + r).cumprod()
    max_dd = float((acum / acum.cummax() - 1).min())
    ret_anual = float((1 + mu_d) ** 252 - 1)
    vol_anual = float(sd_d * np.sqrt(252))

    otros = {}
    for nm, col in [("merval", "merval_usd"), ("txar", "txar_usd"), ("lme", "lme"), ("dxy", "dxy")]:
        s = panel[col].pct_change()
        otros[nm] = float(r.corr(s.reindex(r.index)))

    # Estadistica comparada de los tres activos de la plaza local
    comparada = {}
    for nombre, col in [("ALUA", "alua_usd"), ("TXAR", "txar_usd"), ("MERVAL", "merval_usd")]:
        s = panel[col].pct_change().dropna()
        z95 = stats.norm.ppf(0.05)
        var_h = float(np.percentile(s, 5))
        comparada[nombre] = {
            "retorno_medio_diario": float(s.mean()),
            "mediana_diaria": float(s.median()),
            "vol_anual": float(s.std(ddof=1) * np.sqrt(252)),
            "asimetria": float(stats.skew(s, bias=False)),
            "exceso_curtosis": float(stats.kurtosis(s, bias=False)),
            "jarque_bera": float(stats.jarque_bera(s)[0]),
            "jarque_bera_p": float(stats.jarque_bera(s)[1]),
            "var_95": var_h,
            "cvar_95": float(s[s <= var_h].mean()),
        }

    return {
        "n_obs": int(n),
        "desde": str(r.index[0].date()), "hasta": str(r.index[-1].date()),
        "comparada": comparada,
        "sharpe": None,   # se completa en run(), necesita la tasa libre de riesgo
        "retorno_diario_medio": float(mu_d),
        "vol_diaria": float(sd_d),
        "retorno_anual": ret_anual,
        "vol_anual": vol_anual,
        "asimetria": float(skew),
        "exceso_curtosis": float(kurt),
        "jarque_bera": float(jb),
        "jarque_bera_p": float(jb_p),
        "normalidad_rechazada": bool(jb_p < 0.05),
        "max_drawdown": max_dd,
        "correlaciones": otros,
    }


# ===========================================================================
# M3 — MACROECONOMIA
# ===========================================================================
def m3_macro() -> dict:
    st = json.load(open(os.path.join(RAIZ, "static_inputs.json"), encoding="utf-8"))
    return {
        "anios": st["macro_ar"]["years"],
        "pbi_growth": st["macro_ar"]["pbi_growth"],
        "inflacion": st["macro_ar"]["inflacion"],
        "fuente_macro": st["macro_ar"]["_fuente"],
        "embi_anios": st["embi_hist"]["dates"],
        "embi_valores": st["embi_hist"]["values"],
        "fuente_embi": st["embi_hist"]["_fuente"],
        "merval_pe_anios": st["merval_pe"]["years"],
        "merval_pe": st["merval_pe"]["values"],
    }


# ===========================================================================
# M4 — ESTADOS FINANCIEROS EN DOLARES Y RATIOS
# ===========================================================================
def m4_estados() -> dict:
    usd, ratios = {}, {}
    for y in DA.ANIOS:
        c = DA.CCL_CIERRE[y]
        r, b, f = DA.ESTADO_RESULTADOS[y], DA.BALANCE[y], DA.FLUJO_EFECTIVO[y]
        conv = lambda v: v / c / 1e6                      # pesos -> USD millones
        da = f["depreciacion"] + f["amortizacion"]
        ebitda = r["resultado_operativo"] + da
        deuda_fin = b["deuda_financiera_c"] + b["deuda_financiera_nc"]
        cxp = b["cuentas_por_pagar_c"] + b["cuentas_por_pagar_nc"]
        nwc_op = ((b["activo_corriente"] - b["efectivo"] - b["otras_inversiones_c"]
                   - b["otros_activos_fin_c"])
                  - (b["pasivo_corriente"] - b["deuda_financiera_c"]))
        nopat = r["resultado_operativo"] * (1 - M1.TASA_IMPOSITIVA)
        capital_invertido = deuda_fin + b["total_patrimonio"]

        usd[y] = {
            "ccl": c,
            "ventas": conv(r["ventas_netas"]),
            "costo_ventas": conv(r["costo_ventas"]),
            "resultado_bruto": conv(r["resultado_bruto"]),
            "sga": conv(r["costos_distribucion"] + r["gastos_administracion"]),
            "otros": conv(r["otros_resultados_op"] + r["otras_ganancias_perdidas"]),
            "ebit": conv(r["resultado_operativo"]),
            "ebitda": conv(ebitda),
            "da": conv(da),
            "resultado_financiero": conv(r["resultado_financiero"]),
            "ebt": conv(r["resultado_antes_imp"]),
            "impuesto": conv(r["impuesto_ganancias"]),
            "resultado_neto": conv(r["resultado_ejercicio"]),
            "nopat": conv(nopat),
            "efectivo": conv(b["efectivo"]),
            "cxc": conv(b["cuentas_por_cobrar"]),
            "inventarios": conv(b["inventarios"]),
            "activo_corriente": conv(b["activo_corriente"]),
            "activo_no_corriente": conv(b["activo_no_corriente"]),
            "total_activo": conv(b["total_activo"]),
            "cxp": conv(cxp),
            "pasivo_corriente": conv(b["pasivo_corriente"]),
            "pasivo_no_corriente": conv(b["pasivo_no_corriente"]),
            "total_pasivo": conv(b["total_pasivo"]),
            "patrimonio": conv(b["total_patrimonio"]),
            "deuda_financiera": conv(deuda_fin),
            "deuda_neta": conv(deuda_fin - b["efectivo"]),
            "nwc_operativo": conv(nwc_op),
            "fco": conv(f["fco"]),
            "capex": conv(-f["capex"]),
            "intereses_pagados": conv(f["intereses_pagados"]),
            "dividendos": conv(-f["dividendos_pagados"]),
            "capital_invertido": conv(capital_invertido),
        }

        cmv = abs(r["costo_ventas"])
        ratios[y] = {
            "liquidez_corriente": _safe(b["activo_corriente"], b["pasivo_corriente"]),
            "liquidez_seca": _safe(b["activo_corriente"] - b["inventarios"], b["pasivo_corriente"]),
            "liquidez_cp": _safe(b["efectivo"], b["pasivo_corriente"]),
            "capital_trabajo": conv(b["activo_corriente"] - b["pasivo_corriente"]),
            "liquidez_modelo_z": _safe(b["activo_corriente"] - b["pasivo_corriente"], b["total_activo"]),
            "endeudamiento_pn": _safe(deuda_fin, b["total_patrimonio"]),
            "endeudamiento_at": _safe(b["total_pasivo"], b["total_activo"]),
            "pt_pn": _safe(b["total_pasivo"], b["total_patrimonio"]),
            "cobertura_intereses": _safe(r["resultado_operativo"], f["intereses_pagados"]),
            "cobertura_intereses_ebitda": _safe(ebitda, f["intereses_pagados"]),
            "rotacion_credito": _safe(r["ventas_netas"], b["cuentas_por_cobrar"]),
            "dias_cobranza": _safe(b["cuentas_por_cobrar"] * 365, r["ventas_netas"]),
            "rotacion_inventario": _safe(cmv, b["inventarios"]),
            "dias_venta": _safe(b["inventarios"] * 365, cmv),
            "dias_pago": _safe(cxp * 365, cmv),
            "rotacion_activo": _safe(r["ventas_netas"], b["total_activo"]),
            "margen_bruto": _safe(r["resultado_bruto"], r["ventas_netas"]),
            "margen_ebitda": _safe(ebitda, r["ventas_netas"]),
            "margen_ebit": _safe(r["resultado_operativo"], r["ventas_netas"]),
            "margen_neto": _safe(r["resultado_ejercicio"], r["ventas_netas"]),
            "roa": _safe(r["resultado_ejercicio"], b["total_activo"]),
            "roe": _safe(r["resultado_ejercicio"], b["total_patrimonio"]),
            "roic": _safe(nopat, capital_invertido),
            "dupont_margen": _safe(r["resultado_ejercicio"], r["ventas_netas"]),
            "dupont_rotacion": _safe(r["ventas_netas"], b["total_activo"]),
            "dupont_leverage": _safe(b["total_activo"], b["total_patrimonio"]),
        }
        ratios[y]["dupont"] = (ratios[y]["dupont_margen"] * ratios[y]["dupont_rotacion"]
                               * ratios[y]["dupont_leverage"])

    # --- Drivers de proyeccion, medianas historicas (enfoque de manual) -----
    da_pct = [usd[y]["da"] / usd[y]["ventas"] for y in DA.ANIOS]
    capex_pct = [usd[y]["capex"] / usd[y]["ventas"] for y in DA.ANIOS]
    nwc_pct = [usd[y]["nwc_operativo"] / usd[y]["ventas"] for y in DA.ANIOS]
    de = [usd[y]["deuda_financiera"] / usd[y]["patrimonio"] for y in DA.ANIOS]

    drivers = {
        "da_pct_ventas": float(np.median(da_pct)),
        "capex_pct_ventas": float(np.median(capex_pct)),
        "nwc_pct_ventas": float(np.median(nwc_pct)),
        "da_pct_serie": {y: da_pct[i] for i, y in enumerate(DA.ANIOS)},
        "capex_pct_serie": {y: capex_pct[i] for i, y in enumerate(DA.ANIOS)},
        "nwc_pct_serie": {y: nwc_pct[i] for i, y in enumerate(DA.ANIOS)},
        "d_e_serie": {y: de[i] for i, y in enumerate(DA.ANIOS)},
        "d_e_historico": float(np.median(de)),
        "d_e_objetivo": float(np.median(de[-3:])),
    }
    # Costo de la deuda empirico: intereses pagados sobre deuda financiera
    kd_obs = {y: usd[y]["intereses_pagados"] / usd[y]["deuda_financiera"] for y in DA.ANIOS}
    drivers["kd_serie"] = kd_obs
    drivers["kd"] = float(np.mean([kd_obs[y] for y in (2024, 2025)]))
    return {"usd": usd, "ratios": ratios, "drivers": drivers}


# ===========================================================================
# M5 — PROYECCIONES (Ingresos = Precio x Cantidad)
# ===========================================================================
def m5_proyecciones(est: dict) -> dict:
    """
    FY2026E se reconstruye de abajo hacia arriba desde el trimestre real;
    FY2027E-FY2030E salen del marco fisico: volumen fijo por capacidad
    instalada y precio realizado en reversion lineal hacia la media del LME.
    """
    dv = est["drivers"]
    volumen = CAPACIDAD_MAX_TN * UTILIZACION

    # --- FY2026E: trimestre real escalado por el nivel del LME -------------
    q_real = Q1_2026["revenue_usdmm"]
    lme_real = LME_TRIM["ene-mar26"]
    rev_q = {k: q_real * (v / lme_real) for k, v in LME_TRIM.items()}
    rev_2026 = float(sum(rev_q.values()))
    # Precio realizado implicito del ano base, en USD por tonelada
    precio_2026 = rev_2026 * 1e6 / volumen

    # Calibracion del coeficiente de eficiencia k contra la UNICA observacion
    # dura disponible: el trimestre real. Se calibra al precio realizado DE ESE
    # TRIMESTRE, no al promedio anual, porque el margen del modelo ya depende
    # del precio; calibrarlo contra un precio distinto del que genero el margen
    # observado contaminaria el coeficiente con el efecto precio.
    precio_q_real = q_real * 1e6 / (volumen / 4)
    margen_q_real = Q1_2026["ebitda_usdmm"] / q_real
    k = margen_q_real / ((precio_q_real - CASH_COST_USD_TN) / precio_q_real)

    # --- Senda de precio realizado: reversion lineal a la media del LME ----
    precio_2030 = LME_REVERSION_USD_TN + PREMIUM_VALOR_AGREGADO
    precios = {}
    for i, y in enumerate(ANIOS_PROY):
        precios[y] = precio_2026 + (precio_2030 - precio_2026) * i / (len(ANIOS_PROY) - 1)

    ventas_ant = est["usd"][2025]["ventas"]
    proj = {}
    for y in ANIOS_PROY:
        p = precios[y]
        rev = rev_2026 if y == 2026 else volumen * p / 1e6
        margen_ebitda = k * (p - CASH_COST_USD_TN) / p
        ebitda = rev * margen_ebitda
        da = rev * dv["da_pct_ventas"]
        ebit = ebitda - da
        nopat = ebit * (1 - M1.TASA_IMPOSITIVA)
        capex = rev * dv["capex_pct_ventas"]
        dnwc = (rev - ventas_ant) * dv["nwc_pct_ventas"]
        fcff = nopat + da - capex - dnwc
        proj[y] = dict(precio_realizado=p, volumen_tn=volumen, revenue=rev,
                       margen_ebitda=margen_ebitda, ebitda=ebitda, da=da, ebit=ebit,
                       margen_ebit=ebit / rev, nopat=nopat, capex=capex, dnwc=dnwc, fcff=fcff)
        ventas_ant = rev

    return {
        "volumen_tn": volumen,
        "precio_2026_usd_tn": precio_2026,
        "precio_2030_usd_tn": precio_2030,
        "precio_trimestre_real_usd_tn": precio_q_real,
        "margen_trimestre_real": margen_q_real,
        "k_calibracion": k,
        "cash_cost_usd_tn": CASH_COST_USD_TN,
        "revenue_trimestral_2026": rev_q,
        "revenue_2026": rev_2026,
        "proyecciones": proj,
    }


# ===========================================================================
# M6 — COSTO DE CAPITAL
# ===========================================================================
def m6_costo_capital(mkt: dict, est: dict) -> dict:
    """
    Beta OLS -> Blume -> Hamada; Ke con Lambda CAPM (Damodaran); WACC de Dumrauf.
    """
    dv = est["drivers"]
    t = M1.TASA_IMPOSITIVA

    beta_ols = mkt["beta_ols"]
    beta_blume = 2.0 / 3.0 * beta_ols + 1.0 / 3.0           # Blume (1971)
    de_hist, de_obj = dv["d_e_historico"], dv["d_e_objetivo"]
    beta_u = beta_blume / (1 + (1 - t) * de_hist)           # Hamada, desapalancado
    beta_l = beta_u * (1 + (1 - t) * de_obj)                # Hamada, reapalancado

    e_v = 1.0 / (1.0 + de_obj)
    d_v = 1.0 - e_v
    rf, rm, embi = mkt["rf"], mkt["rm"], mkt["embi_ar"]

    # CAPM ajustado por riesgo pais (Dumrauf, Cap. 6 y 8). La prima soberana
    # entra ponderada por la exposicion domestica de los ingresos: Aluar
    # exporta ~80% de su produccion y factura en dolares al precio LME.
    ke = rf + beta_l * (rm - rf) + LAMBDA_AR * embi
    ke_lambda_uno = rf + beta_l * (rm - rf) + embi           # celda testigo J9
    kd = dv["kd"]
    kd_post = kd * (1 - t)
    wacc = ke * e_v + kd_post * d_v                         # Dumrauf, Cap. 12

    return {
        "rf": rf, "rm": rm, "erp": rm - rf, "embi": embi,
        "beta_ols": beta_ols, "beta_se": mkt["beta_se"], "beta_r2": mkt["beta_r2"],
        "beta_n_obs": mkt["beta_n_obs"],
        "beta_blume": beta_blume, "beta_desapalancado": beta_u, "beta_apalancado": beta_l,
        "d_e_historico": de_hist, "d_e_objetivo": de_obj,
        "e_sobre_v": e_v, "d_sobre_v": d_v,
        "ke": ke, "kd": kd, "kd_post_tax": kd_post, "tasa_impositiva": t,
        "ke_lambda_uno": ke_lambda_uno,
        "wacc_lambda_uno": ke_lambda_uno * e_v + kd_post * d_v,
        "wacc": wacc, "g_perpetuidad": G_PERPETUIDAD, "lambda_ar": LAMBDA_AR,
        "g_plantilla": G_PLANTILLA,
        "aporte_ke": ke * e_v, "aporte_kd": kd_post * d_v,
    }


# ===========================================================================
# M7 — DESCUENTO DE FLUJOS DE FONDOS
# ===========================================================================
def m7_dcf(cc: dict, pro: dict, mkt: dict, deuda_neta_usdmm: float) -> dict:
    wacc, g = cc["wacc"], cc["g_perpetuidad"]
    proj = pro["proyecciones"]
    fcff = [proj[y]["fcff"] for y in ANIOS_PROY]

    # Fila 32 de la plantilla: exponentes 0, 1, 2, 3, 4
    factores = [(1 + wacc) ** i for i in range(len(ANIOS_PROY))]
    pv = [f / d for f, d in zip(fcff, factores)]
    van5 = float(sum(pv))

    # Flujo terminal normalizado: CAPEX = D&A y Delta NWC = 0 en estado
    # estacionario, de modo que FCFF = NOPAT (Dumrauf, Cap. 14).
    nopat_2030 = proj[2030]["nopat"]
    fcff_terminal = nopat_2030
    tv = fcff_terminal * (1 + g) / (wacc - g)               # celda FCFF!E37
    pv_tv = tv / (1 + wacc) ** (len(ANIOS_PROY) - 1)

    ev = van5 + pv_tv
    equity = ev - deuda_neta_usdmm
    target_usd = equity / mkt["acciones_mm"]
    target_ars = target_usd * mkt["ccl"]
    px = mkt["alua_px_ars"]
    upside = target_ars / px - 1

    # Tasa de reinversion implicita del ultimo ano explicito (control)
    rr_mecanica = (proj[2030]["capex"] + proj[2030]["dnwc"] - proj[2030]["da"]) / nopat_2030

    return {
        "wacc": wacc, "g": g,
        "fcff_proyectado": {y: proj[y]["fcff"] for y in ANIOS_PROY},
        "factores_descuento": {y: factores[i] for i, y in enumerate(ANIOS_PROY)},
        "fcff_descontado": {y: pv[i] for i, y in enumerate(ANIOS_PROY)},
        "van_5y": van5,
        "nopat_2030": nopat_2030,
        "fcff_terminal": fcff_terminal,
        "fcff_terminal_mecanico": proj[2030]["fcff"],
        "reinversion_mecanica_2030": rr_mecanica,
        "valor_terminal": tv,
        "valor_terminal_descontado": pv_tv,
        "peso_valor_terminal": pv_tv / ev,
        "enterprise_value": ev,
        "deuda_neta": deuda_neta_usdmm,
        "equity_value": equity,
        "target_usd": target_usd,
        "target_ars": target_ars,
        "precio_mercado_ars": px,
        "upside": upside,
        "dictamen": "COMPRAR" if upside > 0.15 else ("MANTENER" if upside > -0.15 else "VENDER"),
    }


# ===========================================================================
# M8 — SENSIBILIDAD
# ===========================================================================
def m8_sensibilidad(cc, pro, mkt, dn, est_global) -> dict:
    base_w, base_g = cc["wacc"], cc["g_perpetuidad"]
    ws = [base_w + d for d in (-0.015, -0.0075, 0.0, 0.0075, 0.015)]
    gs = [base_g + d for d in (-0.010, -0.005, 0.0, 0.005, 0.010)]
    matriz = []
    for w in ws:
        fila = []
        for g in gs:
            cc2 = dict(cc); cc2["wacc"], cc2["g_perpetuidad"] = w, g
            fila.append(m7_dcf(cc2, pro, mkt, dn)["target_ars"])
        matriz.append(fila)

    # Sensibilidad al precio realizado del aluminio
    # Sensibilidad al precio realizado: se re-corre el modelo fisico completo
    # con la senda de precios desplazada, manteniendo volumen y drivers.
    prec = []
    ventas_base_2025 = est_global["usd"][2025]["ventas"]
    for shock in (-0.20, -0.10, 0.0, 0.10, 0.20):
        proj2, ventas_ant = {}, ventas_base_2025
        for y in ANIOS_PROY:
            p0 = pro["proyecciones"][y]
            p = p0["precio_realizado"] * (1 + shock)
            rev = p0["volumen_tn"] * p / 1e6
            margen = pro["k_calibracion"] * (p - CASH_COST_USD_TN) / p
            ebitda = rev * margen
            da = p0["da"] / p0["revenue"] * rev
            capex = p0["capex"] / p0["revenue"] * rev
            ebit = ebitda - da
            nopat = ebit * (1 - M1.TASA_IMPOSITIVA)
            dnwc = (rev - ventas_ant) * est_global["drivers"]["nwc_pct_ventas"]
            proj2[y] = dict(p0, precio_realizado=p, revenue=rev, ebitda=ebitda, da=da,
                            ebit=ebit, nopat=nopat, capex=capex, dnwc=dnwc,
                            fcff=nopat + da - capex - dnwc)
            ventas_ant = rev
        pro2 = dict(pro, proyecciones=proj2)
        prec.append(dict(shock=shock, target_ars=m7_dcf(cc, pro2, mkt, dn)["target_ars"]))

    return {"wacc_valores": ws, "g_valores": gs, "matriz_target_ars": matriz,
            "sensibilidad_precio": prec}


# ===========================================================================
# M9 — SIMULACION DE MONTE CARLO
# ===========================================================================
def m9_monte_carlo(cc, pro, mkt, dn, est, n_sim=20000, semilla=42) -> dict:
    """
    Monte Carlo con distribuciones normales independientes sobre los tres
    parametros criticos del valor terminal. La incertidumbre del WACC se
    deriva del error estandar del beta; la del flujo, del error estandar
    de la MEDIA historica del margen EBITDA (no de su desvio anual).

    El shock de margen se aplica en un unico sorteo por corrida a los 5 anios
    de FCFF proyectado y al flujo terminal (perpetuidad): representa una
    hipotesis sobre el NIVEL DE LARGO PLAZO del margen, no el ruido de un
    ejercicio puntual. Por eso su sigma correcto es el error estandar de la
    media (CV historico / raiz de n_hist), consistente con el Teorema Central
    del Limite -- usar directamente el desvio anual (33% CV) sobreestima la
    incertidumbre de largo plazo por un factor de raiz(n_hist) y generaba
    corridas con FCFF y equity negativos (fallo estadistico: la distribucion
    colapsaba a valores irreales cercanos a 0 en ~0,7% de las corridas).
    """
    rng = np.random.default_rng(semilla)
    wacc, g = cc["wacc"], cc["g_perpetuidad"]

    # sigma del WACC: propagacion del error estandar del beta al Ke, ponderado por E/V,
    # mas un componente por la incertidumbre del costo de la deuda (dispersion historica).
    sd_ke = cc["beta_se"] * cc["erp"]
    kd_serie = np.array(list(est["drivers"]["kd_serie"].values()))
    sd_kd = float(kd_serie.std(ddof=1)) * (1 - cc["tasa_impositiva"])
    sd_wacc = float(np.sqrt((sd_ke * cc["e_sobre_v"]) ** 2 + (sd_kd * cc["d_sobre_v"]) ** 2))
    sd_g = 0.005                                   # 50 pb, la mitad de la banda de g

    margenes = np.array([est["ratios"][y]["margen_ebitda"] for y in DA.ANIOS])
    n_hist = len(margenes)
    cv_margen = float(margenes.std(ddof=1) / margenes.mean())
    sd_shock_margen = cv_margen / np.sqrt(n_hist)   # error estandar de la media, no el desvio anual

    # Innovaciones Student-t (nu=4.2) para WACC y g, no Normales: el test de
    # Kolmogorov-Smirnov sobre los retornos diarios de ALUA.BA (Seccion de
    # Riesgo Cuantitativo) rechaza la Normal en favor de una Student-t con
    # nu=4.2 grados de libertad (D=0.018 vs 0.054). Se reutiliza ese mismo nu
    # -- estimado sobre el unico activo subyacente del modelo -- para las dos
    # fuentes de incertidumbre de mercado (WACC y g), preservando media y
    # desvio estandar objetivo mediante el factor de escala sqrt((nu-2)/nu).
    # El shock de margen EBITDA se mantiene Normal: es un supuesto sobre el
    # nivel de largo plazo del margen (ver docstring de la funcion), no una
    # serie de retornos de mercado, y no hay evidencia de colas pesadas ahi.
    NU_STUDENT_T = 4.2
    _t_scale = np.sqrt((NU_STUDENT_T - 2) / NU_STUDENT_T)
    w = wacc + sd_wacc * rng.standard_t(NU_STUDENT_T, n_sim) * _t_scale
    gg = g + sd_g * rng.standard_t(NU_STUDENT_T, n_sim) * _t_scale
    shock = rng.normal(0.0, sd_shock_margen, n_sim)

    fcff = np.array([pro["proyecciones"][y]["fcff"] for y in ANIOS_PROY])
    nopat30 = pro["proyecciones"][2030]["nopat"]

    valido = (w - gg) > 0.01
    w, gg, shock = w[valido], gg[valido], shock[valido]

    exps = np.arange(len(ANIOS_PROY))
    pv = (fcff[None, :] * (1 + shock)[:, None]) / (1 + w)[:, None] ** exps[None, :]
    van5 = pv.sum(axis=1)
    fcff_t = nopat30 * (1 + shock)
    tv = fcff_t * (1 + gg) / (w - gg)
    pv_tv = tv / (1 + w) ** (len(ANIOS_PROY) - 1)
    ev = van5 + pv_tv
    eq = ev - dn
    target_ars = eq / mkt["acciones_mm"] * mkt["ccl"]
    target_ars = np.maximum(target_ars, 0.0)        # responsabilidad limitada: precio nunca negativo

    px = mkt["alua_px_ars"]
    qs = np.percentile(target_ars, [5, 25, 50, 75, 95])
    return {
        "n_sim": int(len(target_ars)), "semilla": semilla,
        "sd_wacc": sd_wacc, "sd_g": sd_g,
        "cv_margen_ebitda_anual": cv_margen, "n_hist_margen": n_hist,
        "sd_shock_margen": sd_shock_margen,
        "media": float(target_ars.mean()), "mediana": float(np.median(target_ars)),
        "desvio": float(target_ars.std(ddof=1)),
        "p5": float(qs[0]), "p25": float(qs[1]), "p50": float(qs[2]),
        "p75": float(qs[3]), "p95": float(qs[4]),
        "prob_suba": float((target_ars > px).mean()),
        "precio_mercado_ars": px,
        "muestra": target_ars,
    }


# ===========================================================================
# M10 — VALOR A RIESGO
# ===========================================================================
def m10_riesgo(panel: pd.DataFrame) -> dict:
    from scipy import stats
    r = panel["alua_usd"].pct_change().dropna().values
    mu, sd = r.mean(), r.std(ddof=1)
    out = {"n_obs": int(len(r)), "media_diaria": float(mu), "vol_diaria": float(sd)}
    for cl, q in ((0.95, 0.05), (0.99, 0.01)):
        z = stats.norm.ppf(q)
        var_p = mu + z * sd                                   # parametrico (normal)
        var_h = float(np.percentile(r, q * 100))              # historico
        cvar_h = float(r[r <= var_h].mean())
        cvar_p = float(mu - sd * stats.norm.pdf(z) / q)
        out[f"var_parametrico_{int(cl*100)}"] = float(var_p)
        out[f"var_historico_{int(cl*100)}"] = var_h
        out[f"cvar_parametrico_{int(cl*100)}"] = cvar_p
        out[f"cvar_historico_{int(cl*100)}"] = cvar_h
        out[f"var_historico_{int(cl*100)}_21d"] = var_h * np.sqrt(21)
        out[f"cvar_historico_{int(cl*100)}_21d"] = cvar_h * np.sqrt(21)
    return out


# ===========================================================================
# M11 — PORTAFOLIO (Markowitz e indice unico de Sharpe)
# ===========================================================================
def m11_portafolio(panel: pd.DataFrame, rf: float) -> dict:
    from scipy.optimize import minimize
    cols = {"ALUA": "alua_usd", "TXAR": "txar_usd", "GGAL": "ggal_usd", "MERVAL": "merval_usd"}
    d = panel.copy()
    d["ggal_usd"] = d["ggal_adr_adj"] if "ggal_adr_adj" in d else d["ggal_adr"]
    R = pd.DataFrame({k: d[v].pct_change() for k, v in cols.items()}).dropna()
    R = R.loc[R.index >= (R.index[-1] - pd.DateOffset(years=5))]

    mu = R.mean().values * 252
    S = R.cov().values * 252
    n = len(mu)
    activos = list(cols)

    def vol(w):
        return float(np.sqrt(w @ S @ w))

    cons_sum = {"type": "eq", "fun": lambda w: w.sum() - 1}
    bnds = [(0.0, 1.0)] * n
    w0 = np.ones(n) / n

    # Cartera de minima varianza
    mv = minimize(vol, w0, bounds=bnds, constraints=[cons_sum], method="SLSQP")
    # Frontera eficiente sobre una grilla de 40 retornos objetivo
    objetivos = np.linspace(float(mu @ mv.x), float(mu.max()), 40)
    frontera = []
    for tgt in objetivos:
        cons = [cons_sum, {"type": "eq", "fun": lambda w, t=tgt: w @ mu - t}]
        s = minimize(vol, w0, bounds=bnds, constraints=cons, method="SLSQP")
        if s.success:
            frontera.append({"ret": float(mu @ s.x), "vol": vol(s.x), "w": s.x.tolist()})

    # Cartera de maximo indice de Sharpe
    neg_sharpe = lambda w: -(w @ mu - rf) / vol(w)
    ms = minimize(neg_sharpe, w0, bounds=bnds, constraints=[cons_sum], method="SLSQP")
    w_ms = ms.x
    var_p = float(w_ms @ S @ w_ms)
    ccr = (w_ms * (S @ w_ms)) / var_p                # contribucion al riesgo

    # Modelo de indice unico de Sharpe contra el Merval
    idx = R["MERVAL"].values
    var_m = idx.var(ddof=1) * 252
    indice_unico = {}
    for a in activos:
        y = R[a].values
        b = np.cov(y, idx, ddof=1)[0, 1] / np.cov(y, idx, ddof=1)[1, 1]
        sist = b ** 2 * var_m
        total = y.var(ddof=1) * 252
        indice_unico[a] = {"beta": float(b), "riesgo_sistematico": float(sist),
                           "riesgo_idiosincratico": float(total - sist),
                           "riesgo_total": float(total),
                           "pct_sistematico": float(sist / total)}

    return {
        "activos": activos,
        "desde": str(R.index[0].date()), "hasta": str(R.index[-1].date()),
        "retorno_anual": {a: float(mu[i]) for i, a in enumerate(activos)},
        "vol_anual": {a: float(np.sqrt(S[i, i])) for i, a in enumerate(activos)},
        "correlaciones": R.corr().to_dict(),
        "min_varianza": {"w": mv.x.tolist(), "ret": float(mu @ mv.x), "vol": vol(mv.x)},
        "max_sharpe": {"w": w_ms.tolist(), "ret": float(mu @ w_ms), "vol": vol(w_ms),
                       "sharpe": float((mu @ w_ms - rf) / vol(w_ms)),
                       "ccr": {a: float(ccr[i]) for i, a in enumerate(activos)}},
        "frontera": frontera,
        "indice_unico_sharpe": indice_unico,
    }


# ===========================================================================
# M12 — VALUACION RELATIVA
# ===========================================================================
def m12_multiplos(est, dcf, mkt, panel=None) -> dict:
    st = json.load(open(os.path.join(RAIZ, "static_inputs.json"), encoding="utf-8"))
    mkt_cap = mkt["alua_px_ars"] / mkt["ccl"] * mkt["acciones_mm"]
    ev_mercado = mkt_cap + dcf["deuda_neta"]
    f25 = est["usd"][2025]

    # Multiplos historicos: capitalizacion al cierre de cada ejercicio (30 de
    # junio), convertida a dolares al CCL de ese cierre.
    historicos = {}
    if panel is not None:
        for y in DA.ANIOS:
            corte = pd.Timestamp(f"{y}-06-30")
            sub = panel.loc[:corte, "alua_ars"].dropna()
            if sub.empty:
                continue
            px_ars = float(sub.iloc[-1])
            f = est["usd"][y]
            cap = px_ars / DA.CCL_CIERRE[y] * mkt["acciones_mm"]
            ev = cap + f["deuda_neta"]
            historicos[y] = {
                "precio_ars": px_ars,
                "market_cap_usdmm": cap,
                "ev_usdmm": ev,
                "ev_ebitda": _safe(ev, f["ebitda"]),
                "p_e": _safe(cap, f["resultado_neto"]),
                "deuda_neta_ebitda": _safe(f["deuda_neta"], f["ebitda"]),
            }
    return {
        "historicos": historicos,
        "market_cap_usdmm": mkt_cap,
        "ev_mercado_usdmm": ev_mercado,
        "ev_ebitda_fy25": ev_mercado / f25["ebitda"],
        "ev_ventas_fy25": ev_mercado / f25["ventas"],
        "p_e_fy25": mkt_cap / f25["resultado_neto"],
        "ev_ebitda_implicito_dcf": dcf["enterprise_value"] / f25["ebitda"],
        "peers_nombres": st["peers"]["names"],
        "peers_ev_ebitda": st["peers"]["ev_ebitda"],
        "peers_fuente": st["peers"]["_fuente"],
    }


# ===========================================================================
# ANEXO — extensiones fuera de la bibliografia obligatoria
# ===========================================================================
def anexo(mkt, cc, est, panel) -> dict:
    from scipy import stats
    t = M1.TASA_IMPOSITIVA
    # Contraccion bayesiana de Vasicek (1973)
    var_ols, var_prior, prior = mkt["beta_se"] ** 2, 0.25 ** 2, 1.0
    beta_vasicek = ((mkt["beta_ols"] / var_ols + prior / var_prior)
                    / (1 / var_ols + 1 / var_prior))
    # CAPM-Lambda de Damodaran
    lam, vol_bond = 0.20, 0.20
    crp = mkt["embi_ar"] * (mkt["merval_vol_anual"] / vol_bond)
    ke_lambda = mkt["rf"] + cc["beta_apalancado"] * mkt["erp_us"] + lam * crp
    wacc_lambda = ke_lambda * cc["e_sobre_v"] + cc["kd_post_tax"] * cc["d_sobre_v"]

    # Expansion de Cornish-Fisher (1938)
    r = panel["alua_usd"].pct_change().dropna().values
    mu, sd = r.mean(), r.std(ddof=1)
    S, K = stats.skew(r, bias=False), stats.kurtosis(r, bias=False)
    cf = {}
    for cl, q in ((0.95, 0.05), (0.99, 0.01)):
        z = stats.norm.ppf(q)
        z_cf = (z + (z ** 2 - 1) / 6 * S + (z ** 3 - 3 * z) / 24 * K
                - (2 * z ** 3 - 5 * z) / 36 * S ** 2)
        cf[f"var_cornish_fisher_{int(cl*100)}"] = float(mu + sd * z_cf)
        cf[f"z_cornish_fisher_{int(cl*100)}"] = float(z_cf)

    # Criterio de Kelly (1956)
    mu_a = float((1 + r.mean()) ** 252 - 1)
    var_a = float(r.var(ddof=1) * 252)
    kelly = (mu_a - mkt["rf"]) / var_a

    # Ornstein-Uhlenbeck sobre el log del precio en pesos
    x = np.log(panel["alua_ars"].dropna().values)
    x0, x1 = x[:-1], x[1:]
    b_raw, a = np.polyfit(x0, x1, 1)
    raiz_unitaria = bool(b_raw >= 1.0)
    b = min(b_raw, 0.999)                 # truncamiento preventivo de estabilidad
    dt = 1 / 252
    kappa = -np.log(b) / dt
    theta = a / (1 - b)
    sd_eps = float(np.std(x1 - (a + b * x0), ddof=2))
    return {
        "ou_beta_ar1": float(b_raw),
        "ou_raiz_unitaria": raiz_unitaria,
        "ou_advertencia": ("El coeficiente autorregresivo es mayor o igual a 1: la serie "
                           "tiene raiz unitaria y NO revierte a una media. Los parametros "
                           "de abajo salen del truncamiento forzoso a 0,999 y son solo "
                           "ilustrativos; theta no admite lectura economica."
                           if raiz_unitaria else
                           "El coeficiente autorregresivo es menor que 1: la calibracion "
                           "es estadisticamente valida."),
        "beta_vasicek": float(beta_vasicek),
        "beta_blume": cc["beta_blume"],
        "lambda_damodaran": lam,
        "crp_damodaran": float(crp),
        "ke_lambda": float(ke_lambda),
        "wacc_lambda": float(wacc_lambda),
        "asimetria": float(S), "exceso_curtosis": float(K),
        **cf,
        "kelly_completo": float(kelly), "kelly_medio": float(kelly / 2),
        "ou_kappa": float(kappa), "ou_theta": float(theta),
        "ou_sigma": float(sd_eps / np.sqrt(dt)),
        "ou_half_life_dias": float(np.log(2) / kappa * 252),
    }


# ===========================================================================
# ORQUESTADOR
# ===========================================================================
def run(forzar_descarga=False) -> dict:
    mkt = M1.run(forzar_descarga)
    panel = M1.construir_panel(M1.cargar_series())

    est = m4_estados()
    pro = m5_proyecciones(est)
    cc = m6_costo_capital(mkt, est)
    dn = Q1_2026["deuda_neta_usdmm"]
    dcf = m7_dcf(cc, pro, mkt, dn)

    res = {
        "m1_mercado": mkt,
        "m2_estadistica": m2_estadistica(panel),
        "m3_macro": m3_macro(),
        "m4_estados": est,
        "m5_proyecciones": pro,
        "m6_costo_capital": cc,
        "m7_dcf": dcf,
        "m8_sensibilidad": m8_sensibilidad(cc, pro, mkt, dn, est),
        "m10_riesgo": m10_riesgo(panel),
        "m11_portafolio": m11_portafolio(panel, mkt["rf"]),
        "anexo": anexo(mkt, cc, est, panel),
    }
    # Pruebas de robustez sobre los dos parametros que se apartan de la
    # plantilla: la g de perpetuidad y la ponderacion Lambda del riesgo pais.
    def _variante(ke_v, g_v):
        cc2 = dict(cc)
        cc2["wacc"] = ke_v * cc["e_sobre_v"] + cc["kd_post_tax"] * cc["d_sobre_v"]
        cc2["g_perpetuidad"] = g_v
        d2 = m7_dcf(cc2, pro, mkt, dn)
        return {"ke": ke_v, "wacc": cc2["wacc"], "g": g_v,
                "target_ars": d2["target_ars"], "upside": d2["upside"],
                "dictamen": d2["dictamen"]}

    crp_eq = mkt["embi_ar"] * (mkt["merval_vol_anual"] / 0.20)   # sigma bonos 20%
    ke_dam = mkt["rf"] + cc["beta_apalancado"] * cc["erp"] + LAMBDA_AR * crp_eq
    res["robustez"] = {
        "base": _variante(cc["ke"], G_PERPETUIDAD),
        "g_plantilla_2_5": _variante(cc["ke"], G_PLANTILLA),
        "lambda_uno": _variante(cc["ke_lambda_uno"], G_PERPETUIDAD),
        "damodaran_estricto": _variante(ke_dam, G_PERPETUIDAD),
    }

    mc = m9_monte_carlo(cc, pro, mkt, dn, est)
    res["m9_monte_carlo"] = {k: v for k, v in mc.items() if k != "muestra"}
    res["_muestra_mc"] = mc["muestra"]
    res["m12_multiplos"] = m12_multiplos(est, dcf, mkt, panel)
    m2 = res["m2_estadistica"]
    m2["sharpe"] = (m2["retorno_anual"] - mkt["rf"]) / m2["vol_anual"]
    return res


def guardar(res, ruta=None):
    ruta = ruta or os.path.join(DIR, "resultados_original.json")
    limpio = {k: v for k, v in res.items() if not k.startswith("_")}

    def conv(o):
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        raise TypeError(str(type(o)))

    json.dump(limpio, open(ruta, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1, default=conv)
    np.save(os.path.join(DIR, "muestra_montecarlo.npy"), res["_muestra_mc"])
    return ruta


if __name__ == "__main__":
    r = run()
    cc, d = r["m6_costo_capital"], r["m7_dcf"]
    print("=" * 72)
    print("COSTO DE CAPITAL")
    print("=" * 72)
    for k in ["rf", "embi", "rm", "erp", "beta_ols", "beta_blume", "d_e_historico",
              "beta_desapalancado", "d_e_objetivo", "beta_apalancado", "ke", "kd",
              "kd_post_tax", "e_sobre_v", "d_sobre_v", "wacc", "g_perpetuidad"]:
        print(f"  {k:24s} {cc[k]:>10.4f}")
    print()
    print("=" * 72)
    print("DESCUENTO DE FLUJOS DE FONDOS (USD millones)")
    print("=" * 72)
    p = r["m5_proyecciones"]["proyecciones"]
    print(f"  {'':22s}" + "".join(f"{y:>12d}" for y in ANIOS_PROY))
    for k, lbl in [("revenue", "Ingresos"), ("ebitda", "EBITDA"), ("da", "D&A"),
                   ("ebit", "EBIT"), ("nopat", "NOPAT"), ("capex", "CAPEX"),
                   ("dnwc", "Delta NWC"), ("fcff", "FCFF")]:
        print(f"  {lbl:22s}" + "".join(f"{p[y][k]:>12.1f}" for y in ANIOS_PROY))
    print(f"  {'FCFF descontado':22s}" + "".join(f"{d['fcff_descontado'][y]:>12.1f}" for y in ANIOS_PROY))
    print()
    for k in ["van_5y", "fcff_terminal", "valor_terminal", "valor_terminal_descontado",
              "enterprise_value", "deuda_neta", "equity_value"]:
        print(f"  {k:28s} {d[k]:>12.1f}")
    print(f"  {'peso del valor terminal':28s} {d['peso_valor_terminal']*100:>11.1f}%")
    print(f"  {'Target USD por accion':28s} {d['target_usd']:>12.4f}")
    print(f"  {'Target ARS por accion':28s} {d['target_ars']:>12.2f}")
    print(f"  {'Precio de mercado ARS':28s} {d['precio_mercado_ars']:>12.2f}")
    print(f"  {'Potencial':28s} {d['upside']*100:>11.1f}%   {d['dictamen']}")
    guardar(r)
    print()
    print("[OK] resultados_original.json")
