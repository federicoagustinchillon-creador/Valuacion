# -*- coding: utf-8 -*-
"""
gráficos.py — Biblioteca de gráficos del trabajo.

Replica la identidad visual del deck de referencia: misma paleta institucional,
misma tipografía, mismo andamiaje de título-conclusión, subtítulo, unidad y pie
de fuente. Todo gráfico se exporta con bbox_inches='tight'.

El pie de fuente NUNCA menciona notebooks, módulos ni nombres de archivo.
"""
import os, json, datetime as _dt, textwrap as _tw
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib import font_manager as fm
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

DIR = os.path.dirname(os.path.abspath(__file__))
RAIZ = DIR if os.path.exists(os.path.join(DIR, "static_inputs.json")) else os.path.dirname(DIR)
FIGDIR = os.path.join(DIR, "figuras")
os.makedirs(FIGDIR, exist_ok=True)

_PREFERIDAS = ["Segoe UI", "Calibri", "Arial", "Liberation Sans", "DejaVu Sans"]
_DISPONIBLES = {f.name for f in fm.fontManager.ttflist}
FONT = next((f for f in _PREFERIDAS if f in _DISPONIBLES), "DejaVu Sans")

_PREFERIDAS_TITULO = ["Georgia", "Cambria", "Times New Roman", "DejaVu Serif"]
TITLE_FONT = next((f for f in _PREFERIDAS_TITULO if f in _DISPONIBLES), FONT)

C = {
    "navy": "#0B2545", "blue": "#13497B", "blue_lt": "#9DB8D2",
    "grid": "#E4E9F0", "ink": "#1A1A1A", "muted": "#6B7280",
    "value": "#1B7F4B", "risk": "#B11226", "aluar": "#E8833A",
    "panel": "#FFFFFF",
}
SZ = {"title": 15, "subtitle": 11, "axis": 10.5, "tick": 9.5,
      "legend": 9.5, "annot": 9, "source": 8}
LW = {"hairline": 0.7, "thin": 0.8, "light": 1.0, "medium": 1.2,
      "regular": 1.6, "bold": 2.0, "heavy": 2.4}

FUENTE = ("Elaboración propia en base a estados financieros de Aluar e "
          "información de mercado")
_HOY = _dt.date.today().strftime("%d-%b-%Y")

MARG = dict(left=0.085, right=0.860, top=0.80, bottom=0.190)
TITLE_Y, SUB_Y, SRC_Y = 0.955, 0.895, 0.022
_WRAP = 128
_LINE_H = 0.026


def apply_aluar_theme():
    plt.rcParams.update({
        "figure.facecolor": "white", "savefig.facecolor": "white",
        "axes.facecolor": "white", "font.family": FONT,
        "axes.edgecolor": C["muted"], "axes.linewidth": LW["thin"],
        "axes.grid": False, "axes.grid.axis": "y",
        "grid.color": C["grid"], "grid.linewidth": 0.9,
        "axes.axisbelow": True, "axes.spines.top": False, "axes.spines.right": False,
        "xtick.color": C["ink"], "ytick.color": C["ink"],
        "xtick.labelsize": SZ["tick"], "ytick.labelsize": SZ["tick"],
        "text.color": C["ink"], "figure.dpi": 110,
    })


apply_aluar_theme()


def marco(título, subtítulo, unidad, nota="", figsize=(11.0, 6.6)):
    """Lienzo institucional: título-conclusión, subtítulo, unidad y pie de fuente."""
    apply_aluar_theme()
    pie = f"Fuente: {FUENTE}. {_HOY}."
    if nota:
        pie += f" Nota: {nota}"
    líneas = _tw.wrap(pie, width=_WRAP) or [pie]
    m = dict(MARG)
    m["bottom"] = MARG["bottom"] + _LINE_H * max(0, len(líneas) - 1)
    fig = plt.figure(figsize=figsize)
    fig.subplots_adjust(**m)
    ax = fig.add_subplot(111)
    fig.text(m["left"], TITLE_Y, título, ha="left", va="top",
             fontsize=SZ["title"], fontweight="bold", color=C["navy"],
             fontfamily=TITLE_FONT)
    fig.text(m["left"], SUB_Y, subtítulo, ha="left", va="top",
             fontsize=SZ["subtitle"], color=C["muted"])
    if unidad:
        fig.text(m["right"], SUB_Y, unidad, ha="right", va="top",
                 fontsize=SZ["subtitle"], style="italic", color=C["muted"])
    for i, ln in enumerate(líneas):
        fig.text(m["left"], SRC_Y + _LINE_H * (len(líneas) - 1 - i), ln,
                 ha="left", va="bottom", fontsize=SZ["source"], color=C["muted"])
    return fig, ax


def exportar(fig, nombre):
    ruta = os.path.join(FIGDIR, f"{nombre}.pdf")
    fig.savefig(ruta, dpi=200, facecolor="white", edgecolor="none",
                bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    return ruta


def marco_ppt(nota="", figsize=(6.0, 6.5)):
    """Lienzo SIN título/subtítulo horneados (van como textbox nativo en el pptx,
    para consistencia tipográfica y mejor legibilidad a tamaño compacto). Solo
    ejes + pie de fuente. Usar con exportar_fijo para tamaño de salida idéntico
    entre gráficos, evitando la asimetría del recorte dinámico de bbox='tight'."""
    apply_aluar_theme()
    pie = f"Fuente: {FUENTE}. {_HOY}."
    if nota:
        pie += f" Nota: {nota}"
    ancho_wrap = int(_WRAP * 0.62 * (figsize[0] / 6.0))
    líneas = _tw.wrap(pie, width=max(ancho_wrap, 20)) or [pie]
    m = dict(left=0.16, right=0.84, top=0.95, bottom=0.20)
    m["bottom"] = m["bottom"] + 0.034 * max(0, len(líneas) - 1)
    fig = plt.figure(figsize=figsize)
    fig.subplots_adjust(**m)
    ax = fig.add_subplot(111)
    for i, ln in enumerate(líneas):
        fig.text(m["left"], 0.03 + 0.034 * (len(líneas) - 1 - i), ln,
                 ha="left", va="bottom", fontsize=SZ["source"] + 1, color=C["muted"])
    return fig, ax


def exportar_fijo(fig, nombre, dpi=200):
    """Como exportar(), pero SIN bbox_inches='tight': el PNG queda exactamente
    en figsize*dpi pixeles, igual para todos los gráficos que compartan
    figsize -- necesario para que queden simétricos al insertarlos con el
    mismo ancho en el pptx (el recorte dinámico de 'tight' varía por gráfico)."""
    ruta = os.path.join(FIGDIR, f"{nombre}.pdf")
    fig.savefig(ruta, dpi=dpi, facecolor="white", edgecolor="none")
    plt.close(fig)
    return ruta


def _pct_y(ax, dec=0):
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1, decimals=dec))
    ax.tick_params(length=0)
    ax.margins(x=0.02)


def _grid(ax):
    ax.grid(axis="y", color=C["grid"], linewidth=0.9)
    ax.set_axisbelow(True)


def _fs(w_in, h_in, escala=1.5):
    return (w_in * escala, h_in * escala)


# ===========================================================================
# S02 — Tasas de renta fija relevantes para el costo de capital
# ===========================================================================
def g_renta_fija(res, figsize):
    cc = res["m6_costo_capital"]
    etiquetas = ["Tasa libre de riesgo\n(Tesoro EE.UU. 10 años)",
                 "Rendimiento soberano\nargentino implícito\n(Rf + EMBI+)",
                 "Costo de la deuda\nde ALUAR (antes de\nimpuestos)",
                 "Costo de la deuda\nde ALUAR (después de\nimpuestos)"]
    vals = [cc["rf"], cc["rf"] + cc["embi"], cc["kd"], cc["kd_post_tax"]]
    cols = [C["muted"], C["risk"], C["aluar"], C["value"]]
    fig, ax = marco("ALUAR se financia muy por debajo del rendimiento soberano argentino",
                    "Tasas de renta fija que alimentan el costo de capital del modelo",
                    "% anual", figsize=figsize)
    b = ax.bar(etiquetas, vals, color=cols, width=0.55)
    for r, v in zip(b, vals):
        ax.text(r.get_x() + r.get_width() / 2, v + 0.0018, f"{v:.2%}",
                ha="center", fontsize=SZ["annot"] + 1, fontweight="bold", color=C["ink"])
    _pct_y(ax)
    ax.set_ylim(0, max(vals) * 1.22)
    _grid(ax)
    return exportar(fig, "s02_renta_fija")


# ===========================================================================
# S03 / S04 — Contexto de industria (datos de la Memoria y de industria)
# ===========================================================================
def _static():
    return json.load(open(os.path.join(RAIZ, "static_inputs.json"), encoding="utf-8"))


def g_market_share(figsize):
    st = _static()["market_share_regional"]
    etiquetas = [n.replace("\n", " ") for n in st["names"]]
    valores = st["share"]
    fig, ax = marco("ALUAR concentra seis de cada diez toneladas del mercado argentino",
                    "Participación en el mercado doméstico de aluminio", "% del mercado",
                    figsize=figsize)
    ax.axis("off")
    colores = [C["navy"], C["blue_lt"], C["muted"], C["grid"]][:len(valores)]
    explode = [0.04 if i == 0 else 0 for i in range(len(valores))]
    w, t, a = ax.pie(valores, labels=etiquetas, autopct="%1.0f%%", startangle=110,
                     colors=colores, explode=explode, textprops=dict(fontsize=SZ["tick"] + 1),
                     wedgeprops=dict(edgecolor="white", linewidth=1.6))
    for x in a:
        x.set_color("white")
        x.set_fontweight("bold")
        x.set_fontsize(SZ["annot"] + 2)
    return exportar(fig, "s03_market_share")


def g_matriz_energetica(figsize):
    st = _static()["energy_mix"]
    etiquetas = [k.replace("\n", " ") for k in st]
    valores = list(st.values())
    fig, ax = marco("Más de tres cuartos de la energía es de generación propia y renovable",
                    "Matriz de abastecimiento eléctrico de la planta de Puerto Madryn",
                    "% del consumo", figsize=figsize)
    cols = [C["blue"], C["value"], C["aluar"], C["muted"]]
    b = ax.barh(etiquetas[::-1], valores[::-1], color=cols[::-1], height=0.6)
    for r, v in zip(b, valores[::-1]):
        ax.text(v + 0.012, r.get_y() + r.get_height() / 2, f"{v:.0%}",
                va="center", fontsize=SZ["annot"] + 1, fontweight="bold")
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(xmax=1, decimals=0))
    ax.set_xlim(0, max(valores) * 1.22)
    ax.tick_params(length=0)
    ax.grid(axis="x", color=C["grid"], linewidth=0.9)
    ax.set_axisbelow(True)
    return exportar(fig, "s04_matriz_energetica")


def g_curva_costos(figsize):
    st = _static()["cost_curve"]
    nombres = [n.replace("\n", " ") for n in st["names"]]
    costos = st["cash_cost"]
    orden = np.argsort(costos)
    nombres = [nombres[i] for i in orden]
    costos = [costos[i] for i in orden]
    cols = [C["aluar"] if "ALUAR" in n else C["blue_lt"] for n in nombres]
    fig, ax = marco("ALUAR opera en el tercio bajo de la curva de costos global",
                    "Cash cost C1 de productores primarios de aluminio",
                    "USD por tonelada", figsize=figsize)
    b = ax.bar(range(len(costos)), costos, color=cols, width=0.62)
    ax.set_xticks(range(len(costos)))
    ax.set_xticklabels(nombres, rotation=32, ha="right", fontsize=SZ["tick"] - 0.5)
    for r, v, n in zip(b, costos, nombres):
        ax.text(r.get_x() + r.get_width() / 2, v + 25, f"{v:,.0f}", ha="center",
                fontsize=SZ["annot"], fontweight="bold" if "ALUAR" in n else "normal",
                color=C["aluar"] if "ALUAR" in n else C["ink"])
    ax.set_ylim(0, max(costos) * 1.16)
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v, p: f"{v:,.0f}"))
    ax.tick_params(length=0)
    _grid(ax)
    return exportar(fig, "s04_curva_costos")


# ===========================================================================
# S05 — Estadística de la acción
# ===========================================================================
def g_retornos_acumulados(panel, figsize):
    d = panel.loc[panel.index >= (panel.index[-1] - pd.DateOffset(years=6))]
    series = {"ALUA": d["alua_usd"], "Merval": d["merval_usd"], "Ternium Arg.": d["txar_usd"]}
    fig, ax = marco("ALUAR supera a Ternium pero queda muy por detras del Merval",
                    "Retorno acumulado en dólares, base 100 al inicio del período",
                    "índice, base 100", figsize=figsize)
    estilos = {"ALUA": (C["navy"], LW["heavy"]), "Merval": (C["risk"], LW["regular"]),
               "Ternium Arg.": (C["value"], LW["regular"])}
    for k, s in series.items():
        s = s.dropna()
        idx = s / s.iloc[0] * 100
        col, lw = estilos[k]
        ax.plot(idx.index, idx.values, color=col, lw=lw, label=k)
        ax.annotate(f"{idx.iloc[-1]:,.0f}", xy=(idx.index[-1], idx.iloc[-1]),
                    xytext=(6, 0), textcoords="offset points", va="center",
                    fontsize=SZ["annot"], fontweight="bold", color=col)
    ax.set_yscale("log")
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v, p: f"{v:,.0f}"))
    ax.legend(loc="upper left", frameon=False, fontsize=SZ["legend"])
    ax.tick_params(length=0)
    _grid(ax)
    return exportar(fig, "s05_retornos_acumulados")


def g_distribucion(res, panel, figsize):
    m2 = res["m2_estadistica"]
    r = panel["alua_usd"].pct_change().dropna()
    fig, ax = marco("Los retornos tienen colas más pesadas que una normal",
                    "Distribución de retornos diarios en dólares y normal ajustada",
                    "frecuencia", nota=(f"Jarque-Bera = {m2['jarque_bera']:,.0f}, "
                                        f"p-value < 0,01: se rechaza la normalidad."),
                    figsize=figsize)
    ax.hist(r, bins=90, color=C["blue_lt"], edgecolor="white", linewidth=0.3, density=True)
    x = np.linspace(r.min(), r.max(), 400)
    from scipy import stats
    ax.plot(x, stats.norm.pdf(x, r.mean(), r.std(ddof=1)), color=C["risk"],
            lw=LW["bold"], label="Normal ajustada")
    v95 = res["m10_riesgo"]["var_historico_95"]
    ax.axvline(v95, color=C["navy"], ls="--", lw=LW["medium"])
    ax.annotate(f"VaR 95% histórico\n{v95:.2%}", xy=(v95, ax.get_ylim()[1] * 0.72),
                xytext=(-8, 0), textcoords="offset points", ha="right",
                fontsize=SZ["annot"], color=C["navy"], fontweight="bold")
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(xmax=1, decimals=0))
    ax.legend(loc="upper right", frameon=False, fontsize=SZ["legend"])
    ax.tick_params(length=0)
    _grid(ax)
    return exportar(fig, "s05_distribucion")


# ===========================================================================
# S06 — Creacion de valor: ROIC contra WACC
# ===========================================================================
def g_roic_wacc(res, figsize):
    rt = res["m4_estados"]["ratios"]
    wacc = res["m6_costo_capital"]["wacc"]
    anios = sorted(int(y) for y in rt)
    roic = [rt.get(y, rt.get(str(y), {})).get("roic", 0) for y in anios]
    _crea = sum(1 for v in roic if v >= wacc)
    fig, ax = marco(f"El ROIC superó al costo de capital en {_crea} de los {len(roic)} "
                    f"ejercicios del ciclo de inversión",
                    "Rendimiento sobre el capital invertido contra el WACC del modelo",
                    "% anual", figsize=figsize)
    cols = [C["value"] if v >= wacc else C["risk"] for v in roic]
    b = ax.bar([str(a) for a in anios], roic, color=cols, width=0.55)
    for r_, v in zip(b, roic):
        ax.text(r_.get_x() + r_.get_width() / 2, v + 0.004, f"{v:.1%}", ha="center",
                fontsize=SZ["annot"], fontweight="bold")
    ax.axhline(wacc, color=C["navy"], ls="--", lw=LW["bold"], zorder=5)
    ax.annotate(f"WACC {wacc:.2%}", xy=(len(anios) - 0.4, wacc), xytext=(0, 7),
                textcoords="offset points", ha="right", fontsize=SZ["annot"],
                fontweight="bold", color=C["navy"],
                bbox=dict(boxstyle="round,pad=0.28", fc="white", ec=C["navy"], lw=0.8))
    _pct_y(ax, dec=0)
    ax.set_ylim(0, max(max(roic), wacc) * 1.28)
    _grid(ax)
    return exportar(fig, "s06_roic_wacc")


# ===========================================================================
# S07 — Pipeline del beta: OLS, Blume y Hamada
# ===========================================================================
def g_pipeline_beta(res, figsize):
    cc = res["m6_costo_capital"]
    etiquetas = ["Beta OLS\ncontra el S&P 500",
                 "Beta ajustado\npor Blume",
                 "Beta desapalancado\n(Hamada, D/E hist.)",
                 "Beta apalancado\n(Hamada, D/E objetivo)"]
    vals = [cc["beta_ols"], cc["beta_blume"], cc["beta_desapalancado"], cc["beta_apalancado"]]
    cols = [C["blue"], C["blue_lt"], C["muted"], C["navy"]]
    fig, ax = marco("El beta pasa de la regresión cruda a la estructura de capital objetivo",
                    "Beta OLS, ajuste de Blume y ecuaciones de Hamada",
                    "beta", nota=(f"Blume: 2/3 x beta + 1/3. Hamada: desapalancar con "
                                  f"D/E = {cc['d_e_historico']:.3f} y reapalancar con "
                                  f"D/E objetivo = {cc['d_e_objetivo']:.3f}, con t = 35%."),
                    figsize=figsize)
    b = ax.bar(etiquetas, vals, color=cols, width=0.55)
    for r_, v in zip(b, vals):
        ax.text(r_.get_x() + r_.get_width() / 2, v + 0.012, f"{v:.3f}", ha="center",
                fontsize=SZ["annot"] + 1, fontweight="bold")
    ax.axhline(1.0, color=C["muted"], ls=":", lw=LW["medium"])
    ax.text(3.42, 1.0, "beta del mercado = 1", va="bottom", ha="right",
            fontsize=SZ["annot"] - 0.5, color=C["muted"])
    ax.set_ylim(0, 1.16)
    ax.tick_params(length=0)
    _grid(ax)
    return exportar(fig, "s07_pipeline_beta")


# ===========================================================================
# S08 — Construcción del WACC
# ===========================================================================
def g_wacc(res, figsize):
    cc = res["m6_costo_capital"]
    rf, embi = cc["rf"], cc["embi"]
    lam = cc["lambda_ar"]
    rp = lam * embi                                   # riesgo país ponderado
    berp = cc["beta_apalancado"] * cc["erp"]
    ke, wacc = cc["ke"], cc["wacc"]
    peso_rp = rp / ke
    fig, ax = marco_ppt(nota=(f"Ke = Rf + Beta x (Rm - Rf) + Lambda x EMBI+, con Lambda = {lam:.2f} "
                               f"= ventas al mercado interno sobre ventas totales (Aluar exporta "
                               f"cerca del {1-lam:.0%} de su producción y factura al precio LME en "
                               f"dólares). Con Lambda = 1, la variante pre-cargada en la plantilla, "
                               f"el Ke sube a {cc['ke_lambda_uno']:.2%}."),
                        figsize=figsize)
    ax.set_ylabel("% anual (USD)", fontsize=SZ["tick"])
    x = np.arange(5)
    bases = [0, rf, rf + rp, 0, 0]
    altos = [rf, rp, berp, ke, wacc]
    cols = [C["blue"], C["risk"], C["blue_lt"], C["navy"], C["aluar"]]
    etiquetas = ["Tasa libre\nde riesgo", f"+ Lambda x EMBI+\n({lam:.2f} x {embi:.2%})",
                 "+ Beta x ERP", "= Ke", "WACC"]
    for i in range(5):
        ax.bar(x[i], altos[i], bottom=bases[i], color=cols[i], width=0.55)
        ax.text(x[i], bases[i] + altos[i] + 0.0022, f"{altos[i]:.2%}", ha="center",
                fontsize=SZ["annot"] + 1, fontweight="bold",
                color=C["aluar"] if i == 4 else C["ink"])
    for i in range(2):
        ax.plot([x[i] + 0.275, x[i + 1] - 0.275],
                [bases[i] + altos[i]] * 2, color=C["muted"], lw=LW["thin"])
    ax.axvline(2.5, color=C["muted"], ls="--", lw=LW["medium"], alpha=0.55)
    ax.set_xticks(x)
    ax.set_xticklabels(etiquetas)
    _pct_y(ax)
    ax.set_ylim(0, ke * 1.22)
    ax.tick_params(length=0)
    _grid(ax)
    return exportar(fig, "s08_wacc")


# ===========================================================================
# S10 — Cadena del método indirecto del FCFF
# ===========================================================================
def g_cadena_fcff(res, figsize):
    p = res["m5_proyecciones"]["proyecciones"].get(2030, res["m5_proyecciones"]["proyecciones"].get("2030"))
    def col_signo(v):
        return C["risk"] if v < 0 else C["blue_lt"]

    cajas = [("EBIT", p["ebit"], C["blue"]), ("× (1 − t)", None, None),
             ("NOPAT", p["nopat"], C["navy"]), ("+ D&A", p["da"], C["blue_lt"]),
             ("− CAPEX", -p["capex"], col_signo(-p["capex"])),
             ("− Δ NWC", -p["dnwc"], col_signo(-p["dnwc"])),
             ("= FCFF", p["fcff"], C["value"])]
    fig, ax = marco("", "", "", figsize=figsize)
    ax.axis("off")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 30)
    n = len(cajas)
    ancho, hueco = 11.6, 2.6
    x0 = (100 - (n * ancho + (n - 1) * hueco)) / 2
    for i, (lbl, val, col) in enumerate(cajas):
        cx = x0 + i * (ancho + hueco)
        if val is None:
            ax.text(cx + ancho / 2, 15, lbl, ha="center", va="center",
                    fontsize=SZ["subtitle"], color=C["muted"], style="italic")
        else:
            ax.add_patch(FancyBboxPatch((cx, 6), ancho, 18,
                                        boxstyle="round,pad=0,rounding_size=1.6",
                                        fc=col, ec="none"))
            ax.text(cx + ancho / 2, 18.4, lbl, ha="center", va="center", color="white",
                    fontsize=SZ["axis"], fontweight="bold")
            ax.text(cx + ancho / 2, 11.4, f"{val:,.0f}", ha="center", va="center",
                    color="white", fontsize=SZ["title"], fontweight="bold")
        if i < n - 1 and cajas[i + 1][1] is not None and val is not None:
            ax.add_patch(FancyArrowPatch((cx + ancho + 0.3, 15),
                                         (cx + ancho + hueco - 0.3, 15),
                                         arrowstyle="-|>", mutation_scale=11,
                                         color=C["muted"], lw=1.1))
    ax.text(50, 1.6, "Flujo de fondos libre a la firma proyectado para 2030E, "
                     "en millones de dólares",
            ha="center", fontsize=SZ["source"] + 0.5, color=C["muted"])
    return exportar(fig, "s10_cadena_fcff")


# ===========================================================================
# S11 — FCFF histórico y proyectado
# ===========================================================================
def g_fcff(res, figsize):
    usd = res["m4_estados"]["usd"]
    proj = res["m5_proyecciones"]["proyecciones"]
    hist_y = sorted(int(y) for y in usd)
    hist_v = [usd.get(y, usd.get(str(y), {}))["nopat"] + usd.get(y, usd.get(str(y), {}))["da"] - usd.get(y, usd.get(str(y), {}))["capex"] for y in hist_y]
    proj_y = sorted(int(y) for y in proj)
    proj_v = [proj.get(y, proj.get(str(y), {}))["fcff"] for y in proj_y]
    anios = hist_y + proj_y
    vals = hist_v + proj_v
    cols = [C["navy"]] * len(hist_y) + [C["aluar"]] * len(proj_y)
    fig, ax = marco("Cerrado el ciclo de inversión, el flujo libre se estabiliza",
                    "Flujo de fondos libre a la firma, histórico y proyectado",
                    "USD millones",
                    nota=("Histórico sin variación de capital de trabajo, para aislar el "
                          "efecto del CAPEX. Proyectado con la alícuota estatutaria del 35%."),
                    figsize=figsize)
    b = ax.bar([str(a) for a in anios], vals, color=cols, width=0.6)
    for r_, v in zip(b, vals):
        off = 9 if v >= 0 else -15
        ax.annotate(f"{v:,.0f}", xy=(r_.get_x() + r_.get_width() / 2, v),
                    xytext=(0, off), textcoords="offset points", ha="center",
                    fontsize=SZ["annot"], fontweight="bold")
    ax.axhline(0, color=C["ink"], lw=LW["thin"])
    ax.axvline(len(hist_y) - 0.5, color=C["muted"], ls="--", lw=LW["medium"])
    ax.text(len(hist_y) - 0.42, max(vals) * 1.02, "proyectado", fontsize=SZ["annot"],
            color=C["muted"], style="italic")
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v, p: f"{v:,.0f}"))
    ax.set_ylim(min(vals) * 1.35 if min(vals) < 0 else 0, max(vals) * 1.25)
    ax.tick_params(length=0)
    _grid(ax)
    return exportar(fig, "s11_fcff")


# ===========================================================================
# S12 — Puente de valuación
# ===========================================================================
def g_puente(res, figsize):
    d = res["m7_dcf"]
    van, tv = d["van_5y"], d["valor_terminal_descontado"]
    ev, dn, eq = d["enterprise_value"], d["deuda_neta"], d["equity_value"]
    etiquetas = ["Valor presente\nde los flujos\nexplicitos",
                 "Valor presente\ndel valor\nterminal", "Enterprise\nValue",
                 "(-) Deuda\nneta", "Valor de\nlas acciones"]
    bases = [0, van, 0, eq, 0]
    altos = [van, tv, ev, dn, eq]
    cols = [C["blue"], C["blue_lt"], C["navy"], C["risk"], C["value"]]
    fig, ax = marco(f"El valor terminal explica {d['peso_valor_terminal']:.0%} del valor de la firma",
                    "Del valor presente de los flujos al valor de las acciones",
                    "USD millones",
                    nota=(f"El valor terminal pesa {d['peso_valor_terminal']:.1%} del "
                          f"Enterprise Value."), figsize=figsize)
    x = np.arange(5)
    for i in range(5):
        ax.bar(x[i], altos[i], bottom=bases[i], color=cols[i], width=0.58)
        txt = f"(-) {altos[i]:,.0f}" if i == 3 else f"{altos[i]:,.0f}"
        ax.text(x[i], bases[i] + altos[i] + ev * 0.018, txt, ha="center",
                fontsize=SZ["annot"] + 1, fontweight="bold",
                color=C["value"] if i == 4 else C["ink"])
    ax.plot([x[0] + 0.29, x[1] - 0.29], [van, van], color=C["muted"], lw=LW["thin"])
    ax.plot([x[1] + 0.29, x[2] - 0.29], [ev, ev], color=C["muted"], lw=LW["thin"])
    ax.plot([x[2] + 0.29, x[3] - 0.29], [ev, ev], color=C["muted"], lw=LW["thin"])
    ax.plot([x[3] + 0.29, x[4] - 0.29], [eq, eq], color=C["muted"], lw=LW["thin"])
    ax.set_xticks(x)
    ax.set_xticklabels(etiquetas)
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v, p: f"{v:,.0f}"))
    ax.set_ylim(0, ev * 1.18)
    ax.tick_params(length=0)
    _grid(ax)
    return exportar(fig, "s12_puente")


# ===========================================================================
# S13 — Monte Carlo y valor a riesgo
# ===========================================================================
def g_montecarlo(res, muestra, figsize):
    mc, d = res["m9_monte_carlo"], res["m7_dcf"]
    px = d["precio_mercado_ars"]
    _pr = mc.get("prob_suba", float(np.mean(muestra > px)))
    fig, ax = marco(f"La simulación deja {_pr:.0%} de probabilidad de que el valor "
                    f"fundamental supere al mercado",
                    "Distribución del precio objetivo simulado", "ARS por acción",
                    nota=(f"{mc['n_sim']:,} corridas. Normales independientes sobre WACC "
                          f"(desvío {mc['sd_wacc']:.2%}), g (desvío {mc['sd_g']:.2%}) y el "
                          f"flujo terminal."), figsize=figsize)
    m = muestra[(muestra > np.percentile(muestra, 0.5)) & (muestra < np.percentile(muestra, 99.5))]
    ax.hist(m, bins=70, color=C["blue_lt"], edgecolor="white", linewidth=0.3)
    ax.axvspan(mc["p25"], mc["p75"], color=C["blue"], alpha=0.10, zorder=0)
    _mediana_a_la_derecha = mc["mediana"] >= px
    for val, col, lbl, ha, dx in [
            (mc["mediana"], C["navy"], f"Mediana\nARS {mc['mediana']:,.0f}",
             "left" if _mediana_a_la_derecha else "right", 8 if _mediana_a_la_derecha else -8),
            (px, C["risk"], f"Mercado\nARS {px:,.0f}",
             "right" if _mediana_a_la_derecha else "left", -8 if _mediana_a_la_derecha else 8)]:
        ax.axvline(val, color=col, ls="--", lw=LW["bold"], zorder=6)
        ax.annotate(lbl, xy=(val, ax.get_ylim()[1] * 0.88), xytext=(dx, 0),
                    textcoords="offset points", ha=ha, va="top", fontsize=SZ["annot"],
                    fontweight="bold", color=col, zorder=7,
                    bbox=dict(boxstyle="round,pad=0.28", fc="white", ec=col, lw=0.9))
    ax.annotate(f"Rango intercuartil sombreado: ARS {mc['p25']:,.0f} a {mc['p75']:,.0f}",
                xy=(0.015, 0.045), xycoords="axes fraction", va="bottom", ha="left",
                fontsize=SZ["annot"] - 0.5, color=C["muted"])
    ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda v, p: f"{v:,.0f}"))
    ax.set_ylabel("")
    ax.tick_params(length=0)
    _grid(ax)
    return exportar(fig, "s13_montecarlo")


def g_var(res, figsize):
    r = res["m10_riesgo"]
    etiquetas = ["VaR 95%\nparametrico", "VaR 95%\nhistorico", "CVaR 95%\nhistorico",
                 "VaR 99%\nparametrico", "VaR 99%\nhistorico", "CVaR 99%\nhistorico"]
    vals = [r["var_parametrico_95"], r["var_historico_95"], r["cvar_historico_95"],
            r["var_parametrico_99"], r["var_historico_99"], r["cvar_historico_99"]]
    cols = [C["blue_lt"], C["blue"], C["navy"], C["blue_lt"], C["blue"], C["risk"]]
    fig, ax = marco("La pérdida esperada en la cola supera al VaR en ambos niveles",
                    "Valor a riesgo diario, metodos paramétrico e histórico",
                    "% de pérdida diaria",
                    nota=("El VaR paramétrico supone normalidad. El histórico y el CVaR "
                          "leen directamente la cola empirica de la muestra."),
                    figsize=figsize)
    b = ax.bar(etiquetas, vals, color=cols, width=0.6)
    for r_, v in zip(b, vals):
        ax.annotate(f"{v:.2%}", xy=(r_.get_x() + r_.get_width() / 2, v), xytext=(0, -14),
                    textcoords="offset points", ha="center", fontsize=SZ["annot"],
                    fontweight="bold", color="white")
    ax.axhline(0, color=C["ink"], lw=LW["thin"])
    _pct_y(ax, dec=0)
    ax.set_ylim(min(vals) * 1.20, 0)
    ax.tick_params(length=0)
    _grid(ax)
    return exportar(fig, "s13_var")


# ===========================================================================
# S14 — Valuación relativa
# ===========================================================================
def g_peers(res, figsize):
    m12 = res["m12_multiplos"]
    nombres = [n.replace("\n", " ") for n in m12["peers_nombres"]]
    vals = list(m12["peers_ev_ebitda"])
    # Reemplazo del múltiplo implícito por el calculado en este trabajo
    for i, n in enumerate(nombres):
        if "ALUAR" in n:
            nombres[i] = "ALUAR\n(a precio de mercado)"
            vals[i] = m12["ev_ebitda_fy25"]
    nombres.append("ALUAR\n(implícito en el DCF)")
    vals.append(m12["ev_ebitda_implicito_dcf"])
    orden = np.argsort(vals)
    nombres = [nombres[i] for i in orden]
    vals = [vals[i] for i in orden]
    cols = [C["aluar"] if "ALUAR" in n and "DCF" not in n else
            (C["value"] if "DCF" in n else C["blue_lt"]) for n in nombres]
    fig, ax = marco("ALUAR cotiza por encima de todos sus comparables globales",
                    "EV/EBITDA de productores de aluminio contra ALUAR", "veces EBITDA",
                    nota=("Multiplo de ALUAR calculado sobre el EBITDA auditado de FY2025 "
                          "y la deuda neta del último trimestre informado."),
                    figsize=figsize)
    b = ax.bar(range(len(vals)), vals, color=cols, width=0.62)
    ax.set_xticks(range(len(vals)))
    ax.set_xticklabels([n.replace("\n", "\n") for n in nombres], fontsize=SZ["tick"] - 0.5)
    for r_, v in zip(b, vals):
        ax.text(r_.get_x() + r_.get_width() / 2, v + max(vals) * 0.018, f"{v:.1f}x",
                ha="center", fontsize=SZ["annot"] + 1, fontweight="bold")
    mediana = float(np.median([v for n, v in zip(nombres, vals) if "ALUAR" not in n]))
    ax.axhline(mediana, color=C["muted"], ls="--", lw=LW["medium"])
    ax.annotate(f"Mediana de comparables {mediana:.1f}x", xy=(0.2, mediana), xytext=(0, 6),
                textcoords="offset points", fontsize=SZ["annot"], color=C["muted"])
    ax.set_ylim(0, max(vals) * 1.18)
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v, p: f"{v:.0f}x"))
    ax.tick_params(length=0)
    _grid(ax)
    return exportar(fig, "s14_peers")


# ===========================================================================
# S15 — Síntesis de metodologías
# ===========================================================================
def g_sintesis(res, figsize):
    d, mc, m12 = res["m7_dcf"], res["m9_monte_carlo"], res["m12_multiplos"]
    px = d["precio_mercado_ars"]
    ccl = res["m1_mercado"]["ccl"]
    acc = res["m1_mercado"]["acciones_mm"]
    est = res["m4_estados"]["usd"]
    mediana_peers = float(np.median([v for n, v in zip(m12["peers_nombres"], m12["peers_ev_ebitda"])
                                     if "ALUAR" not in n]))
    eq_peers = mediana_peers * est.get(2025, est.get("2025", {}))["ebitda"] - d["deuda_neta"]
    metodos = [
        ("Monte Carlo P5", mc["p5"], C["risk"]),
        ("Comparables\n(mediana de peers)", eq_peers / acc * ccl, C["muted"]),
        ("Monte Carlo P25", mc["p25"], C["blue_lt"]),
        ("DCF (caso base)", d["target_ars"], C["navy"]),
        ("Monte Carlo\nmediana", mc["mediana"], C["blue"]),
        ("Monte Carlo P95", mc["p95"], C["value"]),
    ]
    metodos.sort(key=lambda t: t[1])
    arriba = sum(1 for m in metodos if m[1] > px)
    titulo = (f"El descuento de flujos y la mediana de la simulación dejan al mercado "
              f"{d['upside']:.0%} por debajo del valor fundamental"
              if d["upside"] > 0 else
              f"El descuento de flujos deja al mercado {-d['upside']:.0%} por encima "
              f"del valor fundamental")
    sub = (f"Precio objetivo por metodología contra el precio de mercado. "
           f"{arriba} de {len(metodos)} superan la cotización")
    fig, ax = marco(titulo, sub, "ARS por acción", figsize=figsize)
    y = np.arange(len(metodos))
    b = ax.barh(y, [m[1] for m in metodos], color=[m[2] for m in metodos], height=0.58)
    ax.set_yticks(y)
    ax.set_yticklabels([m[0] for m in metodos], fontsize=SZ["tick"])
    for r_, m in zip(b, metodos):
        ax.text(m[1] + max(x[1] for x in metodos) * 0.012, r_.get_y() + r_.get_height() / 2,
                f"{m[1]:,.0f}", va="center", fontsize=SZ["annot"] + 1, fontweight="bold")
    ax.axvline(px, color=C["risk"], ls="--", lw=LW["bold"], zorder=6)
    ax.annotate(f"Mercado\nARS {px:,.0f}", xy=(px, 0.6), xytext=(10, 0),
                textcoords="offset points", va="center", fontsize=SZ["annot"],
                fontweight="bold", color=C["risk"], zorder=7,
                bbox=dict(boxstyle="round,pad=0.28", fc="white", ec=C["risk"], lw=0.9))
    ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda v, p: f"{v:,.0f}"))
    ax.set_xlim(0, max(x[1] for x in metodos) * 1.16)
    ax.tick_params(length=0)
    ax.grid(axis="x", color=C["grid"], linewidth=0.9)
    ax.set_axisbelow(True)
    return exportar(fig, "s15_sintesis")


# ===========================================================================
# S17 — Portafolio
# ===========================================================================
def g_frontera(res, figsize):
    pf = res["m11_portafolio"]
    fr = pf["frontera"]
    vol = [f["vol"] for f in fr]
    ret = [f["ret"] for f in fr]
    fig, ax = marco("ALUAR queda dentro de la frontera: aporta por diversificacion, no por retorno",
                    "Frontera eficiente de media-varianza sin ventas en corto",
                    "retorno anual esperado", figsize=figsize)
    ax.plot(vol, ret, color=C["navy"], lw=LW["heavy"], label="Frontera eficiente", zorder=4)
    ms, mv = pf["max_sharpe"], pf["min_varianza"]
    ax.scatter([ms["vol"]], [ms["ret"]], s=95, color=C["aluar"], zorder=6,
               label="Máximo índice de Sharpe", edgecolor="white", linewidth=1.2)
    ax.scatter([mv["vol"]], [mv["ret"]], s=85, color=C["value"], zorder=6,
               label="Mínima varianza", edgecolor="white", linewidth=1.2)
    desplaz = {"ALUA": (10, -12), "TXAR": (10, 8), "GGAL": (-12, 8), "MERVAL": (10, -14)}
    for a in pf["activos"]:
        v, r_ = pf["vol_anual"][a], pf["retorno_anual"][a]
        ax.scatter([v], [r_], s=55, color=C["muted"], zorder=5)
        ax.annotate(a, xy=(v, r_), xytext=desplaz.get(a, (8, 6)),
                    textcoords="offset points", fontsize=SZ["annot"],
                    fontweight="bold", color=C["ink"])
    _pct_y(ax, dec=0)
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(xmax=1, decimals=0))
    ax.set_xlabel("volatilidad anual", fontsize=SZ["axis"], color=C["muted"])
    ax.legend(loc="lower right", frameon=False, fontsize=SZ["legend"])
    ax.tick_params(length=0)
    _grid(ax)
    return exportar(fig, "s17_frontera")


def g_indice_unico(res, figsize):
    iu = res["m11_portafolio"]["indice_unico_sharpe"]
    activos = [a for a in iu if a != "MERVAL"] + ["MERVAL"]
    sist = [iu[a]["riesgo_sistematico"] for a in activos]
    idio = [iu[a]["riesgo_idiosincratico"] for a in activos]
    fig, ax = marco("Casi dos tercios del riesgo de ALUAR es diversificable",
                    "Descomposición de la varianza según el modelo de índice único de Sharpe",
                    "varianza anualizada",
                    nota=("Varianza total = beta al cuadrado por la varianza del Merval, "
                          "más la varianza del residuo."), figsize=figsize)
    x = np.arange(len(activos))
    ax.bar(x, sist, color=C["navy"], width=0.55, label="Riesgo sistemático")
    ax.bar(x, idio, bottom=sist, color=C["blue_lt"], width=0.55, label="Riesgo idiosincrático")
    for i, a in enumerate(activos):
        tot = sist[i] + idio[i]
        ax.text(i, tot + 0.008, f"{iu[a]['pct_sistematico']:.0%} sistemático",
                ha="center", fontsize=SZ["annot"] - 0.5, color=C["muted"])
    ax.set_xticks(x)
    ax.set_xticklabels(activos)
    ax.legend(loc="upper left", frameon=False, fontsize=SZ["legend"])
    ax.set_ylim(0, max(s + i_ for s, i_ in zip(sist, idio)) * 1.22)
    ax.tick_params(length=0)
    _grid(ax)
    return exportar(fig, "s17_indice_unico")


# ===========================================================================
# S18 — Sensibilidad
# ===========================================================================
def g_matriz_sensibilidad(res, figsize):
    s = res["m8_sensibilidad"]
    m = np.array(s["matriz_target_ars"])
    px = res["m7_dcf"]["precio_mercado_ars"]
    _n = int((m > px).sum())
    fig, ax = marco(f"El precio objetivo supera al mercado en {_n} de las {m.size} "
                    f"combinaciones de WACC y g",
                    "Precio objetivo según el costo de capital y el crecimiento perpetuo",
                    "ARS por acción", figsize=figsize)
    im = ax.imshow(m, cmap="RdYlGn", aspect="auto",
                   vmin=np.nanmin(m), vmax=np.nanmax(m))
    ax.set_xticks(range(len(s["g_valores"])))
    ax.set_xticklabels([f"{g:.2%}" for g in s["g_valores"]])
    ax.set_yticks(range(len(s["wacc_valores"])))
    ax.set_yticklabels([f"{w:.2%}" for w in s["wacc_valores"]])
    ax.set_xlabel("crecimiento perpetuo (g)", fontsize=SZ["axis"], color=C["muted"])
    ax.set_ylabel("WACC", fontsize=SZ["axis"], color=C["muted"])
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            centro = (i == m.shape[0] // 2 and j == m.shape[1] // 2)
            ax.text(j, i, f"{m[i, j]:,.0f}", ha="center", va="center",
                    fontsize=SZ["annot"], fontweight="bold" if centro else "normal",
                    color=C["ink"],
                    bbox=dict(boxstyle="round,pad=0.18", fc="white", ec=C["navy"],
                              lw=1.1) if centro else None)
    ax.grid(False)
    ax.tick_params(length=0)
    ax.text(1.02, 1.02, f"Precio de mercado: ARS {px:,.0f}", transform=ax.transAxes,
            ha="right", va="bottom", fontsize=SZ["annot"], color=C["muted"])
    return exportar(fig, "s18_matriz")


def g_tornado(res, figsize):
    s = res["m8_sensibilidad"]
    base = res["m7_dcf"]["target_ars"]
    m = np.array(s["matriz_target_ars"])
    nw, ng = m.shape
    prec = {p["shock"]: p["target_ars"] for p in s["sensibilidad_precio"]}
    variables = [
        ("Precio realizado del aluminio\n(-20% / +20%)", prec[-0.20], prec[0.20]),
        ("WACC\n(+150 pb / -150 pb)", m[-1, ng // 2], m[0, ng // 2]),
        ("Crecimiento perpetuo g\n(-100 pb / +100 pb)", m[nw // 2, 0], m[nw // 2, -1]),
    ]
    variables.sort(key=lambda v: abs(v[2] - v[1]))
    fig, ax = marco("El precio del aluminio domina la sensibilidad del precio objetivo",
                    "Impacto en el precio objetivo de mover una variable por vez",
                    "ARS por acción", figsize=figsize)
    y = np.arange(len(variables))
    for i, (lbl, bajo, alto) in enumerate(variables):
        ax.barh(i, bajo - base, left=base, color=C["risk"], height=0.5)
        ax.barh(i, alto - base, left=base, color=C["value"], height=0.5)
        ax.text(bajo - abs(alto - bajo) * 0.02, i, f"{bajo:,.0f}", va="center", ha="right",
                fontsize=SZ["annot"], fontweight="bold", color=C["risk"])
        ax.text(alto + abs(alto - bajo) * 0.02, i, f"{alto:,.0f}", va="center", ha="left",
                fontsize=SZ["annot"], fontweight="bold", color=C["value"])
    ax.set_yticks(y)
    ax.set_yticklabels([v[0] for v in variables], fontsize=SZ["tick"])
    ax.axvline(base, color=C["navy"], lw=LW["bold"], zorder=6)
    ax.set_ylim(-0.6, len(variables) - 0.15)
    lo = min(v[1] for v in variables)
    hi = max(v[2] for v in variables)
    ax.set_xlim(lo - (hi - lo) * 0.10, hi + (hi - lo) * 0.08)
    ax.annotate(f"Caso base: ARS {base:,.0f}", xy=(base, len(variables) - 0.30),
                xytext=(0, 0), textcoords="offset points", ha="center", va="center",
                fontsize=SZ["annot"], fontweight="bold", color=C["navy"], zorder=7,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=C["navy"], lw=0.9))
    ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda v, p: f"{v:,.0f}"))
    ax.tick_params(length=0)
    ax.grid(axis="x", color=C["grid"], linewidth=0.9)
    ax.set_axisbelow(True)
    return exportar(fig, "s18_tornado")


# ===========================================================================
# S9-BIS — Contexto macroeconómico y de mercado (slide nueva)
# ===========================================================================
EMBI_OBJETIVO_LP = 350.0   # pb -- nivel de referencia soberano BB, supuesto propio del modelo
EMBI_ANIOS_PROY = ["2027E", "2028E", "2029E", "2030E"]

_SZ_PPT = {k: v + 2.5 for k, v in SZ.items()}   # fuentes mas grandes para el panel compacto (1/3 de slide)


def g_embi_descompresion(res, figsize):
    m3 = res["m3_macro"]
    anios_h, vals_h = list(m3["embi_anios"]), list(m3["embi_valores"])
    pico_i = int(np.argmax(vals_h))
    caida = (vals_h[-1] - vals_h[pico_i]) / vals_h[pico_i]
    ultimo = vals_h[-1]
    n = len(EMBI_ANIOS_PROY)
    vals_p = [ultimo * (EMBI_OBJETIVO_LP / ultimo) ** (k / n) for k in range(1, n + 1)]
    anios_todos = anios_h + EMBI_ANIOS_PROY

    fig, ax = marco_ppt(nota=("2027E-2030E: convergencia propia del modelo hacia un nivel de "
                               "referencia soberano BB, no es consenso de mercado."), figsize=figsize)
    ax.plot(anios_h, vals_h, color=C["navy"], lw=LW["heavy"], marker="o", markersize=6,
            markerfacecolor="white", markeredgewidth=1.8, zorder=5)
    ax.plot([anios_h[-1]] + EMBI_ANIOS_PROY, [ultimo] + vals_p, color=C["navy"], lw=LW["heavy"],
            ls=(0, (5, 3)), marker="o", markersize=6, markerfacecolor=C["blue_lt"],
            markeredgewidth=1.8, alpha=0.85, zorder=4)
    ax.fill_between(anios_todos, vals_h + vals_p, color=C["blue_lt"], alpha=0.15, zorder=1)
    ax.annotate(f"Pico 2022\n{vals_h[pico_i]:,.0f} pb", xy=(anios_h[pico_i], vals_h[pico_i]),
                xytext=(0, 16), textcoords="offset points", ha="center", va="bottom",
                fontsize=_SZ_PPT["annot"], fontweight="bold", color=C["risk"],
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=C["risk"], lw=1.0))
    ax.annotate(f"{anios_h[-1]}: {vals_h[-1]:,.0f} pb  →  {EMBI_ANIOS_PROY[-1]}: {vals_p[-1]:,.0f} pb (proy.)",
                xy=(0.97, 0.80), xycoords="axes fraction", ha="right", va="center",
                fontsize=_SZ_PPT["annot"] - 1, fontweight="bold", color=C["value"],
                bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=C["value"], lw=1.0))
    ax.set_ylim(0, max(vals_h) * 1.22)
    ax.tick_params(length=0, labelsize=_SZ_PPT["tick"])
    ax.tick_params(axis="x", labelsize=_SZ_PPT["tick"] - 2)
    ax.set_ylabel("puntos básicos", fontsize=_SZ_PPT["axis"] - 1, color=C["ink"])
    _grid(ax)
    titulo = f"El riesgo país se comprimió {abs(caida):.0%} desde el pico de 2022"
    subtitulo = "Evolución y proyección del EMBI+ Argentina"
    return exportar_fijo(fig, "s09b_embi_descompresion"), titulo, subtitulo


def g_macro_proyeccion(res, figsize):
    m3 = res["m3_macro"]
    anios = [str(a) for a in m3["anios"]]
    pbi, inf = m3["pbi_growth"], m3["inflacion"]
    n_hist = sum(1 for a in m3["anios"] if not str(a).endswith("E"))
    fig, ax = marco_ppt(nota=(f"{m3['fuente_macro'][:120]}..."), figsize=figsize)
    fig.subplots_adjust(top=0.86)
    cols_pbi = [C["blue"] if i < n_hist else C["aluar"] for i in range(len(anios))]
    ax.bar(anios, pbi, color=cols_pbi, width=0.6, zorder=3, label="Crecimiento del PBI")
    ax.set_ylim(min(pbi) * 1.15, max(pbi) * 1.45)
    ax.set_ylabel("PBI, % anual", fontsize=_SZ_PPT["axis"] - 1, color=C["ink"])
    ax2 = ax.twinx()
    ax2.plot(anios, inf, color=C["risk"], lw=LW["bold"], marker="o", markersize=5,
             zorder=5, label="Inflación (esc. log.)")
    ax2.set_yscale("log")
    ticks_log = [5, 10, 25, 50, 100, 200]
    ax2.set_yticks(ticks_log)
    ax2.set_yticks([], minor=True)
    ax2.set_ylim(4, 260)
    ax2.tick_params(length=0, labelsize=_SZ_PPT["tick"])
    ax2.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v, p: f"{v:,.0f}%"))
    ax2.set_ylabel("Inflación, % anual (esc. log.)", fontsize=_SZ_PPT["axis"] - 1, color=C["ink"])
    ax2.grid(False)
    ax.axvline(n_hist - 0.5, color=C["muted"], ls=":", lw=LW["thin"], zorder=2)
    ax.axhline(0, color=C["ink"], lw=LW["thin"])
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    fig.legend(h1 + h2, l1 + l2, loc="upper center", bbox_to_anchor=(0.5, 0.995),
               frameon=False, fontsize=_SZ_PPT["legend"] - 1, ncol=2)
    ax.tick_params(length=0, labelsize=_SZ_PPT["tick"] - 1)
    ax.tick_params(axis="x", rotation=35)
    ax.set_axisbelow(True)
    ax.grid(axis="y", color=C["grid"], linewidth=0.9)
    titulo = "La economía converge a un crecimiento moderado con inflación a un dígito"
    subtitulo = "Proyección macroeconómica argentina: PBI e inflación"
    return exportar_fijo(fig, "s09b_macro_proyeccion"), titulo, subtitulo


def g_lme_vs_dxy(panel, figsize):
    d = panel.loc[panel.index >= (panel.index[-1] - pd.DateOffset(years=4))][["lme", "dxy"]].dropna()
    r_lme = d["lme"].pct_change().dropna()
    r_dxy = d["dxy"].pct_change().dropna()
    corr = float(r_lme.corr(r_dxy.reindex(r_lme.index)))
    fig, ax = marco_ppt(nota=(f"Correlación de retornos diarios (últimos 4 años): {corr:+.2f}."),
                         figsize=figsize)
    ax.plot(d.index, d["lme"], color=C["navy"], lw=LW["regular"], label="Aluminio LME (USD/Tn)")
    ax.set_ylabel("USD por tonelada", fontsize=_SZ_PPT["axis"] - 1, color=C["ink"])
    ax.tick_params(axis="y", labelcolor=C["ink"], labelsize=_SZ_PPT["tick"])
    ax2 = ax.twinx()
    ax2.plot(d.index, d["dxy"], color=C["risk"], lw=LW["medium"], ls="--", label="Índice DXY")
    ax2.set_ylabel("índice DXY", fontsize=_SZ_PPT["axis"] - 1, color=C["ink"])
    ax2.tick_params(axis="y", labelcolor=C["ink"], labelsize=_SZ_PPT["tick"])
    ax2.grid(False)
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="upper center", frameon=False, fontsize=_SZ_PPT["legend"] - 1,
              ncol=2, bbox_to_anchor=(0.5, 1.10))
    ax.tick_params(length=0, axis="x", labelsize=_SZ_PPT["tick"] - 1.5, rotation=35)
    ax.grid(axis="y", color=C["grid"], linewidth=0.9)
    ax.set_axisbelow(True)
    titulo = "El aluminio se mueve en sentido inverso al dólar en el mundo"
    subtitulo = "Precio del aluminio (LME) contra el índice DXY"
    return exportar_fijo(fig, "s09b_lme_vs_dxy"), titulo, subtitulo


def g_peso_riesgo_portafolio(res, figsize):
    """Peso en la cartera de máximo Sharpe vs. contribución al riesgo, por activo.
    Complementa las tarjetas KPI de S17/PORTAFOLIO (que solo muestran el dato de
    ALUA) con el desglose completo de los 4 activos."""
    pf = res["m11_portafolio"]
    activos = [a for a in pf["activos"] if a != "MERVAL"] + ["MERVAL"]
    w = [pf["max_sharpe"]["w"][pf["activos"].index(a)] for a in activos]
    ccr = [pf["max_sharpe"]["ccr"][a] for a in activos]
    fig, ax = marco_ppt(figsize=figsize)
    x = np.arange(len(activos))
    width = 0.32
    b1 = ax.bar(x - width / 2, w, width, color=C["navy"], label="Peso en la cartera")
    b2 = ax.bar(x + width / 2, ccr, width, color=C["aluar"], label="Contribución al riesgo")
    for r, v in zip(b1, w):
        ax.text(r.get_x() + r.get_width() / 2, v + 0.012, f"{v:.0%}", ha="center",
                fontsize=SZ["annot"] - 0.5, fontweight="bold", color=C["navy"])
    for r, v in zip(b2, ccr):
        ax.text(r.get_x() + r.get_width() / 2, v + 0.012, f"{v:.0%}", ha="center",
                fontsize=SZ["annot"] - 0.5, fontweight="bold", color=C["aluar"])
    ax.set_xticks(x)
    ax.set_xticklabels(activos)
    ax.set_ylabel("% de la cartera / % del riesgo total", fontsize=SZ["tick"])
    _pct_y(ax, dec=0)
    ax.set_ylim(0, max(max(w), max(ccr)) * 1.30)
    ax.legend(loc="upper right", frameon=False, fontsize=SZ["legend"])
    ax.tick_params(length=0)
    _grid(ax)
    return exportar_fijo(fig, "s22_peso_riesgo")


def g_kelly_sizing(res, figsize):
    """Dimensionamiento de la posición: sizing por VaR/ES a distintas tolerancias
    de drawdown vs. el criterio de Kelly (M12 del anexo, fuera de la bibliografía
    obligatoria pero calculado en el motor vigente)."""
    an, m10 = res["anexo"], res["m10_riesgo"]
    kelly_medio = an["kelly_medio"]
    cvar21 = abs(m10["cvar_historico_95_21d"])
    tolerancias = [0.05, 0.10, 0.15, 0.20]
    sizing = [t / cvar21 for t in tolerancias]
    recomendado = min(kelly_medio, sizing[1])

    etiquetas = [f"{int(t*100)}%" for t in tolerancias] + ["Half-Kelly"]
    valores = sizing + [kelly_medio]
    colores = [C["blue_lt"]] * len(tolerancias) + [C["value"]]
    fig, ax = marco_ppt(nota=("Recomendado = mínimo entre half-Kelly y VaR/ES a tolerancia 10%. "
                               "CVaR 95% a 21 sesiones vía raíz-de-tiempo (Jorion)."),
                        figsize=figsize)
    y = np.arange(len(etiquetas))[::-1]
    b = ax.barh(y, valores, color=colores, height=0.55)
    for r, v in zip(b, valores):
        ax.text(v + 0.012, r.get_y() + r.get_height() / 2, f"{v:.1%}", va="center",
                fontsize=SZ["annot"], fontweight="bold")
    ax.set_yticks(y)
    ax.set_yticklabels(etiquetas)
    ax.set_ylim(-0.7, y.max() + 1.1)
    ax.set_xlabel("% de la cartera (sizing por VaR/ES)", fontsize=SZ["tick"] - 1)
    ax.axvline(recomendado, color=C["risk"], ls="--", lw=LW["medium"])
    ax.annotate(f"Recomendado {recomendado:.1%}", xy=(recomendado, y.max()),
                xytext=(6, 10), textcoords="offset points", fontsize=SZ["annot"] - 0.5,
                fontweight="bold", color=C["risk"])
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(xmax=1, decimals=0))
    ax.set_xlim(0, max(valores) * 1.32)
    ax.tick_params(length=0)
    ax.grid(axis="x", color=C["grid"], linewidth=0.9)
    ax.set_axisbelow(True)
    return exportar_fijo(fig, "s22_kelly_sizing")


# ===========================================================================
# Slides nuevas -- EBITDA futuro, finanzas cuantitativas, curva de tasas
# ===========================================================================
def g_fcff_bridge_futuro(res, figsize):
    """Bridge de FCFF ano a ano (NOPAT + D&A - CAPEX - DeltaNWC): muestra por
    que el FCFF 2026E es negativo y como se estabiliza desde 2027E."""
    proy = res["m5_proyecciones"]["proyecciones"]
    anios = list(proy.keys())
    nopat = [proy[y]["nopat"] for y in anios]
    da = [proy[y]["da"] for y in anios]
    capex = [-proy[y]["capex"] for y in anios]
    dnwc = [-proy[y]["dnwc"] for y in anios]
    fcff = [proy[y]["fcff"] for y in anios]

    fig, ax = marco_ppt(nota="FCFF = NOPAT + D&A - CAPEX - DeltaNWC, motor DCF (sin hardcodeo).",
                        figsize=figsize)
    x = np.arange(len(anios))
    bottom = np.zeros(len(anios))
    for vals, color, label in [(nopat, C["value"], "+ NOPAT"), (da, C["blue_lt"], "+ D&A"),
                                (capex, C["risk"], "- CAPEX"), (dnwc, C["muted"], "- ΔNWC")]:
        ax.bar(x, vals, bottom=bottom, color=color, width=0.55, label=label, zorder=3)
        bottom += np.array(vals)
    ax.plot(x, fcff, "D-", color=C["navy"], lw=LW["bold"], ms=7, zorder=5, label="FCFF")
    for i, f in enumerate(fcff):
        ax.text(i, f + (10 if f >= 0 else -22), f"${f:,.0f}", ha="center",
                fontsize=SZ["annot"], fontweight="bold", color=C["navy"])
    ax.set_xticks(x)
    ax.set_xticklabels([f"{y}E" for y in anios], fontsize=SZ["tick"])
    ax.axhline(0, color=C["ink"], lw=LW["hairline"])
    ax.legend(frameon=False, fontsize=SZ["legend"] - 1, loc="upper left", ncol=1)
    ax.tick_params(length=0)
    _grid(ax)
    return exportar_fijo(fig, "s_fcff_bridge_futuro")


def g_rerating_ev_ebitda(res, figsize):
    """EBITDA que se modera desde el pico ciclico vs. multiplo EV/EBITDA
    implicito (EV fijo del DCF / EBITDA de cada anio) -- el re-rating mecanico."""
    proy = res["m5_proyecciones"]["proyecciones"]
    anios = list(proy.keys())
    ebitda = [proy[y]["ebitda"] for y in anios]
    ev = res["m7_dcf"]["enterprise_value"]
    multiplos = [ev / e for e in ebitda]

    fig, ax1 = marco_ppt(nota="EV fijo (motor DCF) / EBITDA de cada año. El múltiplo sube porque el EBITDA se normaliza, no porque suba el precio.",
                         figsize=figsize)
    x = np.arange(len(anios))
    b = ax1.bar(x, ebitda, color=C["blue"], width=0.45, alpha=0.65, zorder=3, label="EBITDA (USD MM)")
    ax1.bar_label(b, fmt=lambda v: f"${v:.0f}", fontsize=SZ["annot"] - 1, padding=2)
    ax1.set_ylabel("EBITDA (USD MM)", fontsize=SZ["tick"])
    ax2 = ax1.twinx()
    ax2.plot(x, multiplos, color=C["aluar"], lw=LW["bold"], marker="o", ms=7, zorder=4)
    for i, m in enumerate(multiplos):
        ax2.text(i, m + 0.15, f"{m:.1f}x", ha="center", fontsize=SZ["annot"],
                  fontweight="bold", color=C["aluar"])
    ax2.set_ylabel("EV/EBITDA implícito (x)", fontsize=SZ["tick"])
    ax1.set_xticks(x)
    ax1.set_xticklabels([f"{y}E" for y in anios], fontsize=SZ["tick"])
    ax1.tick_params(length=0)
    ax1.grid(axis="y", visible=False)
    return exportar_fijo(fig, "s_rerating_ev_ebitda")


def g_normalidad_cornish_fisher(res, figsize):
    """Contraste VaR gaussiano (parametrico) vs. VaR ajustado por asimetria y
    curtosis (Cornish-Fisher), a partir del rechazo de normalidad (Jarque-Bera)."""
    m2, r = res["m2_estadistica"], res["m10_riesgo"]
    S, K = m2["asimetria"], m2["exceso_curtosis"]

    def cornish_fisher(z, S, K):
        return z + (z**2 - 1) * S / 6 + (z**3 - 3 * z) * K / 24 - (2 * z**3 - 5 * z) * S**2 / 36

    mu, sigma = m2["retorno_diario_medio"], m2["vol_diaria"]
    z95, z99 = -1.6449, -2.3263
    var95_cf = mu + cornish_fisher(z95, S, K) * sigma
    var99_cf = mu + cornish_fisher(z99, S, K) * sigma

    etiquetas = ["VaR 95%\ngaussiano", "VaR 95%\nCornish-Fisher", "VaR 99%\ngaussiano", "VaR 99%\nCornish-Fisher"]
    vals = [r["var_parametrico_95"], var95_cf, r["var_parametrico_99"], var99_cf]
    cols = [C["blue_lt"], C["risk"], C["blue_lt"], C["risk"]]
    fig, ax = marco(f"El VaR gaussiano subestima la cola: Jarque-Bera rechaza normalidad (JB={m2['jarque_bera']:,.0f}, p<0,001)",
                    "VaR paramétrico gaussiano vs. ajustado por asimetría y curtosis (Cornish-Fisher)",
                    "% de pérdida diaria",
                    nota=(f"Asimetría={S:.2f}, exceso de curtosis={K:.2f} (colas pesadas). "
                          "Cornish-Fisher ajusta el cuantil normal por ambos momentos."),
                    figsize=figsize)
    b = ax.bar(etiquetas, vals, color=cols, width=0.55, zorder=3)
    for rct, v in zip(b, vals):
        ax.annotate(f"{v:.2%}", xy=(rct.get_x() + rct.get_width() / 2, v), xytext=(0, -14),
                    textcoords="offset points", ha="center", fontsize=SZ["annot"],
                    fontweight="bold", color="white")
    ax.axhline(0, color=C["ink"], lw=LW["thin"])
    _pct_y(ax, dec=0)
    ax.set_ylim(min(vals) * 1.25, 0)
    ax.tick_params(length=0)
    _grid(ax)
    return exportar(fig, "s_cornish_fisher")


def g_convergencia_tasas(res, figsize):
    """Curva de tasas de Argentina: convergencia del EMBI+ hacia su media de
    largo plazo, contrastando el supuesto institucional del modelo (350 pb,
    referencia BB) contra un ajuste AR(1)/Ornstein-Uhlenbeck empirico sobre
    la serie real. Incluye el rendimiento implicito del bono soberano en USD
    (Rf UST10Y + EMBI+), no solo el spread, para mostrar la curva de tasas
    completa (bono, no solo riesgo pais)."""
    m3 = res["m3_macro"]
    rf = res["m1_mercado"]["rf"]
    anios_h = [int(a) for a in m3["embi_anios"]]
    vals_h = np.array(m3["embi_valores"], dtype=float)

    x0, x1 = vals_h[:-1], vals_h[1:]
    b, a = np.polyfit(x0, x1, 1)
    theta = a / (1 - b)
    kappa = -np.log(b)
    ultimo = vals_h[-1]

    anios_p = list(range(anios_h[-1] + 1, anios_h[-1] + 6))
    ar1_path = [ultimo]
    for _ in anios_p:
        ar1_path.append(a + b * ar1_path[-1])
    ar1_path = ar1_path[1:]

    objetivo_lp = EMBI_OBJETIVO_LP
    n_sup = 4
    supuesto_path = [ultimo * (objetivo_lp / ultimo) ** (k / n_sup) for k in range(1, n_sup + 1)]

    yield_bono = lambda pb: rf * 100 + pb / 100  # Rf (UST10Y) + EMBI+ (pb->pp) = rendimiento USD del bono soberano

    fig, ax = marco(f"El EMBI+ actual ({ultimo:,.0f} pb) ya está cerca de su equilibrio estimado (~{theta:,.0f} pb)",
                    "Riesgo país y rendimiento del bono soberano en USD: AR(1) real vs. supuesto institucional",
                    "pb / % anual",
                    nota=(f"AR(1) ajustado sobre 7 obs. reales (2020-2026): kappa={kappa:.2f}/año, "
                          f"vida media ~2,5 años. Rendimiento del bono = Rf UST10Y ({rf*100:.2f}%) + EMBI+. "
                          "Advertencia: n pequeño, cota orientativa."),
                    figsize=figsize)
    ax.plot(anios_h, vals_h, color=C["navy"], lw=LW["heavy"], marker="o", ms=6,
            markerfacecolor="white", markeredgewidth=1.8, zorder=5, label="EMBI+ real (2020-2026)")
    ax.plot([anios_h[-1]] + anios_p, [ultimo] + ar1_path, color=C["risk"], lw=LW["bold"],
            ls=(0, (5, 3)), marker="o", ms=5, zorder=4, label=f"Convergencia AR(1) empírica (θ≈{theta:,.0f} pb)")
    ax.plot([anios_h[-1]] + [anios_h[-1] + k for k in range(1, n_sup + 1)], [ultimo] + supuesto_path,
            color=C["value"], lw=LW["medium"], ls=":", marker="s", ms=5, zorder=4,
            label=f"Supuesto institucional del modelo ({objetivo_lp:,.0f} pb, ref. BB)")
    ax.axhline(theta, color=C["risk"], lw=LW["hairline"], ls="--", alpha=0.5)
    ax.set_ylim(0, max(vals_h) * 1.15)
    ax.legend(frameon=False, fontsize=SZ["legend"] - 1, loc="upper right")
    ax.set_ylabel("EMBI+ (pb)", fontsize=SZ["axis"])
    ax.tick_params(length=0)
    _grid(ax)

    ax2 = ax.twinx()
    ax2.set_ylim(yield_bono(0), yield_bono(max(vals_h) * 1.15))
    ax2.set_ylabel("Rendimiento bono soberano USD (Rf+EMBI+, %)", fontsize=SZ["axis"] - 1, color=C["muted"])
    ax2.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v, _: f"{v:.1f}%"))
    ax2.tick_params(length=0, colors=C["muted"], labelsize=SZ["tick"] - 1)
    for spine in ["top"]:
        ax2.spines[spine].set_visible(False)

    return exportar(fig, "s_convergencia_tasas")


def _anillos_geometria(geom):
    """Itera los anillos exteriores de una geometria GeoJSON (Polygon o
    MultiPolygon), ignorando huecos interiores -- suficiente para una
    silueta de fondo a esta escala."""
    tipo, coords = geom["type"], geom["coordinates"]
    if tipo == "Polygon":
        yield coords[0]
    elif tipo == "MultiPolygon":
        for poligono in coords:
            yield poligono[0]


def g_mapa_productores(figsize=(10.6, 5.5)):
    """Mapa de burbujas: participación en la producción mundial de aluminio
    primario por país (mismos datos que static_inputs['market_share_pies']
    ['global'], usados también en la comparativa Latam/mundial de LA EMPRESA).
    Base cartográfica: Natural Earth 1:110m (dominio público)."""
    share = _static()["market_share_pies"]["global"]
    geo_path = os.path.join(DIR, "geo_data", "world_110m.geojson")
    geo = json.load(open(geo_path, encoding="utf-8"))

    fig, ax = marco_ppt(nota="Base cartográfica: Natural Earth, escala 1:110m (dominio público).",
                        figsize=figsize)
    ax.set_xlim(-165, 175)
    ax.set_ylim(-56, 82)
    ax.set_aspect(1.28)
    ax.axis("off")

    for feat in geo["features"]:
        for anillo in _anillos_geometria(feat["geometry"]):
            xs = [p[0] for p in anillo]
            ys = [p[1] for p in anillo]
            ax.fill(xs, ys, color=C["grid"], edgecolor="white", linewidth=0.5, zorder=1)

    # (país, lon, lat, dx/dy de la etiqueta en puntos, alineación horizontal)
    centroides = [("China", 104.5, 36.5, (0, 34), "center"),
                  ("India", 79.5, 22.5, (0, -30), "center"),
                  ("Rusia", 58.0, 61.5, (0, 26), "center"),
                  ("Canadá", -96.0, 57.5, (0, 26), "center"),
                  ("EAU", 54.0, 24.0, (30, -14), "left")]
    for pais, lon, lat, offset, ha in centroides:
        val = share[pais]
        radio = 1100 * val + 70
        ax.scatter([lon], [lat], s=radio, color=C["navy"], alpha=0.88,
                   edgecolor="white", linewidth=1.1, zorder=5)
        ax.annotate(f"{pais} {val:.1%}", xy=(lon, lat), xytext=offset,
                    textcoords="offset points", ha=ha, va="center",
                    fontsize=SZ["annot"] - 0.5, fontweight="bold", color=C["ink"], zorder=6)

    puerto_madryn = (-65.0, -42.8)
    ax.scatter([puerto_madryn[0]], [puerto_madryn[1]], s=340, color=C["aluar"],
               edgecolor="white", linewidth=1.3, zorder=6)
    ax.annotate("ALUAR, Puerto Madryn\n(Argentina, <1% global)", xy=puerto_madryn,
                xytext=(16, -4), textcoords="offset points", ha="left",
                fontsize=SZ["annot"], fontweight="bold", color=C["aluar"], zorder=6)

    ax.text(0.01, 0.03, f"Resto del mundo: {share['Otros']:.0%}. Tamaño de burbuja = "
            "% de la producción mundial.", transform=ax.transAxes,
            fontsize=SZ["annot"], color=C["muted"])
    return exportar_fijo(fig, "s_mapa_productores")


def g_resumen_valuacion(res, figsize):
    """Franja resumen Bajista(P5)-Base(DCF)-Alcista(P95) vs. Mercado, en una
    sola fila condensada. Para el cierre de la tesis (Hipótesis y recomendación
    final) -- reutiliza los mismos valores ya mostrados en SÍNTESIS, sin
    recalcular nada."""
    mc, d = res["m9_monte_carlo"], res["m7_dcf"]
    p5, p95 = mc["p5"], mc["p95"]
    base, mercado = d["target_ars"], d["precio_mercado_ars"]
    apply_aluar_theme()
    fig = plt.figure(figsize=figsize)
    fig.subplots_adjust(left=0.05, right=0.97, top=0.68, bottom=0.34)
    ax = fig.add_subplot(111)
    ax.barh([0], [p95 - p5], left=p5, height=0.45, color=C["blue_lt"], alpha=0.55, zorder=2)
    ax.scatter([base], [0], s=220, color=C["navy"], zorder=4, marker="D")
    ax.scatter([mercado], [0], s=170, color=C["risk"], zorder=4, marker="o")
    ax.annotate(f"Bajista (P5)\nARS {p5:,.0f}", xy=(p5, 0), xytext=(0, -30),
                textcoords="offset points", ha="center", fontsize=SZ["annot"] - 0.5, color=C["muted"])
    ax.annotate(f"Base (DCF)\nARS {base:,.0f}", xy=(base, 0), xytext=(0, 20),
                textcoords="offset points", ha="center", fontsize=SZ["annot"] + 0.5,
                fontweight="bold", color=C["navy"])
    ax.annotate(f"Mercado\nARS {mercado:,.0f}", xy=(mercado, 0), xytext=(0, -30),
                textcoords="offset points", ha="center", fontsize=SZ["annot"] + 0.5,
                fontweight="bold", color=C["risk"])
    ax.annotate(f"Alcista (P95)\nARS {p95:,.0f}", xy=(p95, 0), xytext=(0, 20),
                textcoords="offset points", ha="center", fontsize=SZ["annot"] - 0.5, color=C["muted"])
    ax.set_ylim(-1, 1)
    ax.set_yticks([])
    margen = (p95 - p5) * 0.14
    ax.set_xlim(p5 - margen, p95 + margen)
    ax.set_xticks([])
    for spine in ("left", "top", "right", "bottom"):
        ax.spines[spine].set_visible(False)
    return exportar_fijo(fig, "s_resumen_valuacion")


def g_badlar_local(figsize=(4.3, 1.10)):
    """Evolución mensual de la tasa BADLAR (plazo fijo > $1MM, promedio bancos
    privados) -- cubre el mercado de renta fija LOCAL en pesos que pide la
    consigna del examen, distinto del EMBI+ (spread soberano en USD) y del
    costo de deuda propio de ALUAR ya mostrados en esta misma slide. Serie
    real BCRA, últimos 12 meses (indicadores.ar, consultado 29-jul-2026)."""
    meses = ["Ago-25", "Sep-25", "Oct-25", "Nov-25", "Dic-25", "Ene-26",
              "Feb-26", "Mar-26", "Abr-26", "May-26", "Jun-26", "Jul-26"]
    valores = [58.19, 40.63, 37.19, 29.44, 26.69, 31.19,
               29.5, 25.19, 20.88, 20.81, 20.94, 20.94]
    apply_aluar_theme()
    fig = plt.figure(figsize=figsize)
    fig.subplots_adjust(left=0.11, right=0.97, top=0.66, bottom=0.20)
    fig.text(0.11, 0.94, "Tasa BADLAR (renta fija local, pesos)", ha="left", va="top",
              fontsize=SZ["annot"] + 0.5, fontweight="bold", color=C["navy"],
              fontfamily=TITLE_FONT)
    ax = fig.add_subplot(111)
    x = np.arange(len(meses))
    ax.plot(x, valores, color=C["navy"], lw=LW["regular"], marker="o", markersize=3.2)
    ax.fill_between(x, valores, min(valores) - 2, color=C["navy"], alpha=0.08)
    ax.annotate(f"{valores[0]:.0f}%", xy=(0, valores[0]), xytext=(0, 8),
                textcoords="offset points", ha="center", fontsize=SZ["annot"] - 1.5,
                fontweight="bold", color=C["muted"])
    ax.annotate(f"{valores[-1]:.0f}%", xy=(len(meses) - 1, valores[-1]), xytext=(2, -12),
                textcoords="offset points", ha="center", fontsize=SZ["annot"] - 1.5,
                fontweight="bold", color=C["aluar"])
    ax.set_xticks(x[::2])
    ax.set_xticklabels(meses[::2], fontsize=SZ["tick"] - 2.5)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=100, decimals=0))
    ax.tick_params(labelsize=SZ["tick"] - 2, length=0)
    ax.grid(axis="y", color=C["grid"], linewidth=0.7)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    return exportar_fijo(fig, "s_badlar_local")


def generar_macro_extra(res, panel):
    """Los 3 gráficos de contexto macro de la slide nueva (no reemplazan marcos existentes).
    Tamaño de salida FIJO e idéntico entre los tres (exportar_fijo, sin bbox='tight') para
    que queden simétricos al insertarse con el mismo ancho; titulo/subtitulo van como
    textbox nativo del pptx, no horneados en el PNG."""
    fs = (6.0, 6.7)
    p1 = g_embi_descompresion(res, fs)
    p2 = g_macro_proyeccion(res, fs)
    p3 = g_lme_vs_dxy(panel, fs)
    print(f"  S09B (nueva) embi_descompresion, macro_proyeccion, lme_vs_dxy")
    return p1, p2, p3


# ===========================================================================
# ORQUESTADOR — mapea cada gráfico a su marco del deck
# ===========================================================================
# (slide, shape_id) -> (funcion, ancho_pulgadas, alto_pulgadas)
MAPA = {
    (2, 10):  ("renta_fija",        7.24, 4.81),
    (3, 9):   ("market_share",      6.21, 3.90),
    (4, 5):   ("matriz_energetica", 5.84, 3.96),
    (4, 8):   ("curva_costos",      5.84, 3.70),
    (5, 16):  ("distribución",      4.94, 2.35),
    (5, 9):   ("retornos_acum",     6.78, 2.35),
    (6, 9):   ("roic_wacc",         6.06, 4.12),
    (7, 14):  ("pipeline_beta",     4.97, 3.30),
    (8, 15):  ("wacc",              5.85, 3.88),
    (10, 10): ("cadena_fcff",       6.48, 2.20),
    (11, 6):  ("fcff",              7.37, 3.81),
    (12, 6):  ("puente",            6.49, 4.28),
    (13, 6):  ("montecarlo",        5.05, 2.92),
    (13, 14): ("var",               4.52, 2.76),
    (14, 5):  ("peers",             7.44, 3.80),
    (15, 13): ("síntesis",          5.77, 3.54),
    (17, 9):  ("frontera",          5.17, 3.33),
    (17, 12): ("indice_unico",      5.45, 3.33),
    (18, 9):  ("matriz_sens",       4.41, 2.93),
    (18, 12): ("tornado",           4.85, 2.93),
}


def generar_todos(res, panel, muestra):
    rutas = {}
    for (slide, sid), (nombre, w, h) in MAPA.items():
        fs = _fs(w, h)
        if nombre == "renta_fija":
            p = g_renta_fija(res, fs)
        elif nombre == "market_share":
            p = g_market_share(fs)
        elif nombre == "matriz_energetica":
            p = g_matriz_energetica(fs)
        elif nombre == "curva_costos":
            p = g_curva_costos(fs)
        elif nombre == "distribución":
            p = g_distribucion(res, panel, fs)
        elif nombre == "retornos_acum":
            p = g_retornos_acumulados(panel, fs)
        elif nombre == "roic_wacc":
            p = g_roic_wacc(res, fs)
        elif nombre == "pipeline_beta":
            p = g_pipeline_beta(res, fs)
        elif nombre == "wacc":
            p = g_wacc(res, fs)
        elif nombre == "cadena_fcff":
            p = g_cadena_fcff(res, fs)
        elif nombre == "fcff":
            p = g_fcff(res, fs)
        elif nombre == "puente":
            p = g_puente(res, fs)
        elif nombre == "montecarlo":
            p = g_montecarlo(res, muestra, fs)
        elif nombre == "var":
            p = g_var(res, fs)
        elif nombre == "peers":
            p = g_peers(res, fs)
        elif nombre == "síntesis":
            p = g_sintesis(res, fs)
        elif nombre == "frontera":
            p = g_frontera(res, fs)
        elif nombre == "indice_unico":
            p = g_indice_unico(res, fs)
        elif nombre == "matriz_sens":
            p = g_matriz_sensibilidad(res, fs)
        elif nombre == "tornado":
            p = g_tornado(res, fs)
        else:
            continue
        rutas[(slide, sid)] = p
        print(f"  S{slide:02d} id={sid:<4d} {nombre:<20s} -> {os.path.basename(p)}")
    return rutas


if __name__ == "__main__":
    import m1_mercado as M1
    res = json.load(open(os.path.join(DIR, "resultados_original.json"), encoding="utf-8"))
    panel = M1.construir_panel(M1.cargar_series())
    muestra = np.load(os.path.join(DIR, "muestra_montecarlo.npy"))
    print("Generando gráficos...")
    generar_todos(res, panel, muestra)
    generar_macro_extra(res, panel)
    print("[OK]")
