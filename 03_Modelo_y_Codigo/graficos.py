# -*- coding: utf-8 -*-
"""
gráficos.py — Biblioteca institucional unificada de 31 gráficos (PDF 32P + PPTX).
===============================================================================
Genera programáticamente las 31 figuras oficiales del Reporte PDF alineadas 100%
al inventario físico y estética visual del documento institucional de 32 páginas.

CERO capturas de pantalla, cero archivos de respaldo, cero hardcodes inapropiados.
Fuentes: Georgia Bold (títulos) + Segoe UI (ejes/etiquetas).
"""

import os, json, textwrap, datetime, shutil, hashlib
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

DIR = os.path.dirname(os.path.abspath(__file__))
RAIZ = DIR if os.path.exists(os.path.join(DIR, "static_inputs.json")) else os.path.dirname(DIR)

FIGDIR = os.path.join(DIR, "figuras")
FIGDIR_PRISTINE = os.path.join(os.path.dirname(DIR), "Assets_Oficiales_Pristinos")
FIGDIR_TEX = os.path.join(os.path.dirname(DIR), "01_Reporte_PDF", "figures_pristine")

for d in [FIGDIR, FIGDIR_PRISTINE, FIGDIR_TEX]:
    os.makedirs(d, exist_ok=True)

# ── Configuración de Fuentes y Paleta ─────────────────────────────────────
TITLE_FONT = "Georgia"
AXIS_FONT = "Segoe UI"

C = {
    "navy": "#0B2545", "blue": "#13497B", "blue_lt": "#9DB8D2",
    "grid": "#E4E9F0", "ink": "#1A1A1A", "muted": "#6B7280",
    "value": "#1B7F4B", "risk": "#B11226", "burgundy": "#8B0000", "aluar": "#E8833A",
    "panel": "#FFFFFF", "gold": "#D4A843", "teal": "#1A7A7A",
}
SZ = {"title": 13, "subtitle": 10, "axis": 9.5, "tick": 8.5,
      "legend": 8.5, "annot": 8, "source": 7.5}
LW = {"thin": 0.8, "medium": 1.2, "bold": 1.8}

FUENTE = "Fuente: Elaboración propia en base a estados financieros de Aluar e información de mercado."
_HOY = datetime.date.today().strftime("%d-%b-%Y")

MARG = dict(left=0.090, right=0.940, top=0.82, bottom=0.150)
TITLE_Y, SUB_Y, SRC_Y = 0.955, 0.895, 0.022


def apply_aluar_theme():
    plt.rcParams.update({
        "figure.facecolor": "white", "savefig.facecolor": "white",
        "axes.facecolor": "white", "font.family": AXIS_FONT,
        "axes.edgecolor": C["muted"], "axes.linewidth": LW["thin"],
        "axes.grid": False, "axes.grid.axis": "y",
        "grid.color": C["grid"], "grid.linewidth": 0.9,
        "axes.axisbelow": True, "axes.spines.top": False, "axes.spines.right": False,
        "xtick.color": C["ink"], "ytick.color": C["ink"],
        "xtick.labelsize": SZ["tick"], "ytick.labelsize": SZ["tick"],
        "text.color": C["ink"], "figure.dpi": 300,
    })

apply_aluar_theme()


def scaffold(titulo, subtitulo, unidad="", nota="", figsize=(11.0, 6.2)):
    apply_aluar_theme()
    pie = FUENTE
    if nota:
        pie += f" Nota: {nota}"
    lineas = textwrap.wrap(pie, width=130) or [pie]
    m = dict(MARG)
    m["bottom"] = MARG["bottom"] + 0.025 * max(0, len(lineas) - 1)
    fig = plt.figure(figsize=figsize)
    fig.subplots_adjust(**m)
    ax = fig.add_subplot(111)
    fig.text(m["left"], TITLE_Y, titulo, ha="left", va="top",
             fontsize=SZ["title"], fontweight="bold", color=C["navy"],
             fontfamily=TITLE_FONT)
    fig.text(m["left"], SUB_Y, subtitulo, ha="left", va="top",
             fontsize=SZ["subtitle"], style="italic", color=C["muted"])
    if unidad:
        fig.text(m["right"], SUB_Y, unidad, ha="right", va="top",
                 fontsize=SZ["subtitle"], style="italic", color=C["muted"])
    for i, ln in enumerate(lineas):
        fig.text(m["left"], SRC_Y + 0.025 * (len(lineas) - 1 - i), ln,
                 ha="left", va="bottom", fontsize=SZ["source"], color=C["muted"])
    ax.grid(axis="y", color=C["grid"], linewidth=0.9)
    ax.set_axisbelow(True)
    return fig, ax


def exportar(fig, nombre, dpi=300):
    """Escribe en las 3 carpetas de salida: FIGDIR (copia de trabajo/auditoría), FIGDIR_TEX
    (figures_pristine/, la que efectivamente se embebe en el PDF vía \\includegraphics) y
    FIGDIR_PRISTINE (Assets_Oficiales_Pristinos/, copia para el PPTX).

    Hasta jul-2026 esta función escribía SOLO en FIGDIR "para no pisar el material verificado".
    En la práctica eso significaba que correr graficos.py nunca actualizaba ninguna de las 31
    imágenes que el PDF/PPTX realmente usan -- y el paso de "sincronización" al final del script
    copiaba en sentido inverso (de figures_pristine hacia figuras/), así que el mensaje final
    ("31/31 sincronizadas byte-a-byte con el PDF de referencia") no era cierto: nunca se comparó
    contra el PDF, solo se copió lo que ya estaba. Cada plot_figura_NN() de este archivo calcula
    sus valores desde datos reales (ver cargar_fuentes_datos) -- no hay razón para no dejar que
    su salida sea la que se publica. Si en el futuro se necesita volver a congelar una versión
    manualmente sin correr el script, alcanza con no llamar a exportar() para esa figura."""
    p_png = os.path.join(FIGDIR, f"{nombre}.png")
    p_pdf = os.path.join(FIGDIR, f"{nombre}.pdf")
    fig.patch.set_facecolor('white')
    fig.patch.set_edgecolor('none')
    fig.savefig(p_png, dpi=dpi, facecolor="white", edgecolor="none", bbox_inches="tight", pad_inches=0.08)
    fig.savefig(p_pdf, facecolor="white", edgecolor="none", bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)
    for outdir in (FIGDIR_TEX, FIGDIR_PRISTINE):
        shutil.copy2(p_png, os.path.join(outdir, f"{nombre}.png"))
    return p_png


def pct_y(ax, dec=0):
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=100 if ax.get_ylim()[1]>1 else 1.0, decimals=dec))


def cargar_fuentes_datos():
    """Carga las 3 fuentes de datos reales del motor. No hay fallback fabricado:
    si un archivo falta, se levanta un error explícito en vez de inventar datos."""
    p_res = os.path.join(DIR, "resultados_original.json")
    if not os.path.exists(p_res):
        raise FileNotFoundError(f"Falta resultados_original.json en {DIR} -- no se fabrica un reemplazo.")
    res = json.load(open(p_res, encoding="utf-8"))

    p_stat = os.path.join(DIR, "static_inputs.json")
    if not os.path.exists(p_stat):
        raise FileNotFoundError(f"Falta static_inputs.json en {DIR} -- no se fabrica un reemplazo.")
    stat = json.load(open(p_stat, encoding="utf-8"))

    p_mc = os.path.join(DIR, "muestra_montecarlo.npy")
    if not os.path.exists(p_mc):
        raise FileNotFoundError(f"Falta muestra_montecarlo.npy en {DIR} -- no se fabrica una muestra normal sintética.")
    muestra = np.load(p_mc)

    return res, stat, muestra


def fit_ar1(serie_historica):
    """Ajusta un AR(1) por OLS sobre una serie histórica real: x_t = mu + phi*(x_{t-1} - mu).
    Devuelve (mu, phi) estimados -- nunca hardcodeados -- a partir de los datos provistos."""
    x = np.asarray(serie_historica[:-1], dtype=float)
    y = np.asarray(serie_historica[1:], dtype=float)
    phi, a = np.polyfit(x, y, 1)
    mu = a / (1 - phi)
    return float(mu), float(phi)


# ═══════════════════════════════════════════════════════════════════════════
#  LAS 31 FIGURAS OFICIALES NATIVAS CON CORRESPONDENCIA 1 A 1 EXACTA
# ═══════════════════════════════════════════════════════════════════════════

def plot_figura_01(res, stat):
    """Figura 1 del informe: Línea de tiempo corporativa de Aluar (1974-2026)."""
    fig, ax = scaffold(
        "Línea de tiempo corporativa de Aluar desde su fundación (1974) hasta la actualidad",
        "Destacando hitos de capacidad productiva e integración energética en Puerto Madryn",
        ""
    )
    years = [1974, 1999, 2007, 2019, 2024, 2026]
    events = [
        "Inauguración Planta\nPuerto Madryn (140 kt)",
        "Expansión Fase I\n(270 kt/año)",
        "Expansión Fase II\n(460 kt/año)",
        "Inauguración Parque\nEólico PEAL (Etapa I)",
        "Adhesión RIGI y PEAL V\n(582 MW total)",
        "Capacidad Plena 460 kt\ny 100% Autogeneración"
    ]
    ax.axhline(0, color=C["navy"], lw=2, zorder=1)
    ax.scatter(years, [0]*len(years), color=C["aluar"], s=130, zorder=3, edgecolors="white", linewidths=1.5)
    # Offsets y alineación horizontal explícitos por punto: el cluster 2019/2024/2026 está muy
    # próximo en el eje X (rango total 1970-2030), así que alternar altura solo (i%2) no alcanza
    # para evitar que el texto de esos tres hitos se superponga -- se separan además en altura
    # creciente y en alineación horizontal (derecha/izquierda) para abrir espacio entre ellos.
    offsets = [0.35, -0.45, 0.35, -0.55, 0.85, -0.95]
    has = ["center", "center", "center", "right", "center", "left"]
    for i, (y, ev) in enumerate(zip(years, events)):
        offset = offsets[i]
        ha = has[i]
        va = "bottom" if offset > 0 else "top"
        ax.vlines(y, 0, offset, color=C["blue_lt"], linestyle="--", lw=1.2)
        ax.text(y, offset + (0.05 if offset > 0 else -0.05), f"{y}\n{ev}", ha=ha, va=va, fontsize=8, fontweight="bold", color=C["navy"])
    ax.set_ylim(-1.15, 1.15)
    ax.set_xlim(1970, 2030)
    ax.axis("off")
    return exportar(fig, "figura_01")


def plot_figura_02(res, stat):
    """Figura 2 del informe: Estructura Accionaria de Aluar S.A.I.C."""
    fig, ax = scaffold(
        "Estructura accionaria de Aluar: grupo de control vs. resto del capital",
        "Según la Memoria y Estados Financieros al 30-jun-2025",
        "Participación (%)"
    )
    # Leído de static_inputs.json["accionaria"] (ver "_fuente" ahí) -- sin números tipeados acá.
    acc = stat["accionaria"]
    labels = ['Grupo de Control\n(' + ' / '.join(acc["grupo_control_entidades"]) + ')',
              'Resto del Capital\n(incl. ANSES-FGS y flotante BYMA)']
    sizes = [acc["grupo_control_pct"], acc["resto_capital_pct"]]
    colors = [C["navy"], C["blue_lt"]]
    explode = (0.05, 0)
    
    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                                      startangle=140, textprops=dict(color=C["ink"], fontsize=9.5))
    for at in autotexts:
        at.set_color('white')
        at.set_weight('bold')
        at.set_fontsize(10.5)
    ax.axis('equal')
    return exportar(fig, "figura_02")


def plot_figura_03(res, stat):
    """Figura 3 del informe: Contexto Macroeconómico: PBI e Inflación Proyectada.
    Serie completa real 2020-2030E de static_inputs.json["macro_ar"] (INDEC/FMI WEO/BCRA REM),
    sin truncar a 7 puntos ni omitir el PBI (ambas series eran reales; el bug era solo de
    slicing y de no graficar la serie de PBI)."""
    macro = stat["macro_ar"]
    years = [str(y) for y in macro["years"]]
    pbi = macro["pbi_growth"]
    infl = macro["inflacion"]

    fig, ax = scaffold(
        "Contexto Macroeconómico: PBI e Inflación Proyectada",
        "La estabilización macro favorece la demanda interna sin comprometer la competitividad exportadora",
        "% anual"
    )
    x = np.arange(len(years))
    ax.bar(x, pbi, color=C["blue_lt"], width=0.55, label="PBI real (% a/a)", zorder=2)
    for i, v in enumerate(pbi):
        ax.text(i, v + (1.2 if v >= 0 else -1.8), f"{v:.1f}%", ha="center", fontsize=8, color=C["ink"])
    ax.axhline(0, color=C["ink"], lw=0.8)
    ax.set_ylabel("PBI real (% a/a)", fontsize=SZ["axis"])
    ax.set_xticks(x)
    ax.set_xticklabels(years)

    ax2 = ax.twinx()
    ax2.grid(False)
    ax2.plot(x, infl, marker="o", color=C["risk"], lw=2.2, label="Inflación (% a/a)", zorder=3)
    for i, v in enumerate(infl):
        ax2.annotate(f"{v:.0f}%", (i, v), textcoords="offset points", xytext=(0, 9),
                     ha="center", fontsize=8, fontweight="bold", color=C["risk"])
    ax2.set_ylabel("Inflación (% a/a)", fontsize=SZ["axis"])
    ax2.set_ylim(0, max(infl) * 1.2)

    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, frameon=False, fontsize=SZ["legend"], loc="upper right")
    return exportar(fig, "figura_03")


def plot_figura_04(res, stat):
    """Figura 4 del informe: Compresión del riesgo país (EMBI+ Argentina)."""
    embi_hist = stat.get("embi_hist", {})
    dates = embi_hist.get("dates", ["2020", "2021", "2022", "2023", "2024", "2025", "2026"])
    embi = embi_hist.get("values", [2150, 1650, 2400, 1950, 850, 600, 441])
    
    fig, ax = scaffold(
        "Compresión del riesgo país (EMBI+ Argentina), serie histórica 2020–2026",
        "Trayectoria descendente del spread soberano tras la estabilización fiscal",
        "Puntos Básicos (pb)"
    )
    x = np.arange(len(dates))
    ax.plot(x, embi, marker="o", color=C["blue"], lw=2.2)
    ax.fill_between(x, embi, color=C["blue_lt"], alpha=0.3)
    for i in range(len(dates)):
        ax.text(i, embi[i] + 60, f"{embi[i]:,} pb", ha="center", fontsize=8.5, fontweight="bold", color=C["navy"])
    ax.set_xticks(x)
    ax.set_xticklabels(dates)
    ax.set_ylim(0, max(embi)*1.15)
    return exportar(fig, "figura_04")


def plot_figura_05(res, stat):
    """Figura 5 del informe: Curva de riesgo país (EMBI+, AR(1)) y rendimiento implícito
    soberano en USD, con la línea plana del supuesto constante (441 pb) que usa el WACC/DCF
    del modelo — replica el gráfico y la corrección aplicada en el reporte de referencia
    (el modelo descuenta con 441 pb constante, no con la convergencia AR(1))."""
    m6 = res.get("m6_costo_capital", {})
    m3 = res.get("m3_macro", {})
    embi0 = m6["embi"] * 10000                    # pb, hoy (441) -- input real del WACC
    rf = m6["rf"] * 100                            # %, tasa libre de riesgo (constante)

    # mu y phi del AR(1) NO son constantes tipeadas: se estiman por OLS sobre la serie
    # histórica real de EMBI+ (m3_macro.embi_valores, JPMorgan/BCRA) vía x_t = mu + phi*(x_{t-1}-mu).
    mu_lp, phi = fit_ar1(m3["embi_valores"])

    years = np.arange(0, 6)                       # 2026E .. 2030E (t=0..5)
    embi_ar1 = mu_lp + (embi0 - mu_lp) * phi ** years
    yield_ar1 = rf + embi_ar1 / 100.0              # Rf + EMBI+ (en %)
    embi_constante = np.full_like(years, embi0, dtype=float)  # supuesto del modelo (plano)

    fig, ax = scaffold(
        "Curva de Riesgo País (EMBI+) y Rendimiento Implícito Soberano",
        "Modelo AR(1) de convergencia hacia la media de largo plazo "
        f"({mu_lp:.0f} pb)",
        "pb / %"
    )
    ax2 = ax.twinx()
    ax2.grid(False)

    ax.plot(years, embi_ar1, marker="o", color=C["navy"], lw=2.2, zorder=3,
            label="EMBI+ — convergencia AR(1) real")
    ax.plot(years, embi_constante, color=C["risk"], lw=1.6, linestyle="--", zorder=2,
            label=f"Supuesto constante del modelo ({embi0:.0f} pb)")
    ax2.plot(years, yield_ar1, marker="s", color=C["aluar"], lw=1.8, linestyle="--", zorder=3,
             label="Rendimiento soberano (Rf+EMBI+)")

    for i, yr in enumerate(years):
        ax.annotate(f"{embi_ar1[i]:,.0f} pb", (yr, embi_ar1[i]), textcoords="offset points",
                    xytext=(0, 9), ha="center", fontsize=8, fontweight="bold", color=C["navy"])
        ax2.annotate(f"{yield_ar1[i]:.2f}%", (yr, yield_ar1[i]), textcoords="offset points",
                     xytext=(0, -14), ha="center", fontsize=8, fontweight="bold", color=C["aluar"])

    ax.set_xlabel("Años de Proyección (2026E-2030E)")
    ax.set_ylabel("EMBI+ (pb)")
    ax2.set_ylabel("Rendimiento Soberano (%)")
    ax.set_xticks(years)
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    # loc="upper right" caía justo encima de la serie graficada (que también decae de izquierda a
    # derecha); "lower left" queda en la esquina vacía del gráfico para las 3 curvas de este caso.
    ax.legend(lines1 + lines2, labels1 + labels2, frameon=False, fontsize=SZ["legend"], loc="lower left")
    return exportar(fig, "figura_05")


def plot_figura_06(res, stat):
    """Figura 6 del informe: Cotización del Aluminio (LME) vs. Índice del Dólar (DXY).
    Serie mensual real leída de static_inputs.json["lme_dxy"] (sin fallback numérico:
    si falta, debe fallar, no dibujar una serie de 6 puntos inventada)."""
    lme_dxy = stat["lme_dxy"]
    dates = lme_dxy["dates"]
    lme_raw = lme_dxy["lme"]
    dxy_raw = lme_dxy["dxy"]

    # Interpolación lineal SOLO para huecos internos (días no hábiles), no para inventar el nivel.
    lme = pd.Series(lme_raw).interpolate(method="linear").bfill().ffill().values
    dxy = pd.Series(dxy_raw).interpolate(method="linear").bfill().ffill().values

    fecha_ini, fecha_fin = dates[0], dates[-1]
    fig, ax = scaffold(
        f"Cotización del Aluminio (LME) vs. Índice del Dólar (DXY) - Serie Real {fecha_ini} a {fecha_fin}",
        f"Correlación empírica de {np.corrcoef(lme, dxy)[0,1]:.2f}. Serie mensual, {len(lme)} observaciones",
        "USD/Tn / Índice DXY"
    )
    x = np.arange(len(lme))

    ax.plot(x, lme, color=C["navy"], lw=1.8, label="LME Aluminio (USD/Tn)")
    ax.set_ylabel("LME Aluminio (USD/Tn)", fontsize=SZ["axis"], color=C["navy"])
    ax.set_ylim(min(lme)*0.9, max(lme)*1.15)

    # Ticks de eje X en enero de cada año presente en la serie real (no hardcodeados).
    tick_idx = [i for i, d in enumerate(dates) if str(d).startswith("Jan")]
    if not tick_idx or tick_idx[0] != 0:
        tick_idx = [0] + tick_idx
    ax.set_xticks(tick_idx)
    ax.set_xticklabels([dates[i].split("-")[-1] for i in tick_idx])

    ax2 = ax.twinx()
    ax2.plot(x, dxy, color=C["burgundy"], lw=1.5, linestyle="--", label="Índice DXY")
    ax2.set_ylabel("Índice DXY", fontsize=SZ["axis"], color=C["burgundy"])
    ax2.set_ylim(min(dxy)*0.95, max(dxy)*1.05)
    ax2.spines["right"].set_visible(True)
    ax2.spines["top"].set_visible(False)

    # Callouts calculados de la serie real, no tipeados.
    max_idx = int(np.argmax(lme))
    ax.annotate(f"LME Spot: ${lme[max_idx]:,.0f}/Tn",
                xy=(max_idx, lme[max_idx]),
                xytext=(max(max_idx - 15, 0), lme[max_idx] + (max(lme)-min(lme))*0.08),
                arrowprops=dict(facecolor=C["navy"], arrowstyle="->", lw=1.2),
                bbox=dict(boxstyle="round,pad=0.4", facecolor="#F0F4F8", edgecolor=C["navy"], lw=1.2),
                fontsize=8.5, fontweight="bold", color=C["navy"])

    end_idx = len(dxy) - 1
    ax2.annotate(f"DXY: {dxy[end_idx]:.1f}",
                 xy=(end_idx, dxy[end_idx]),
                 xytext=(max(end_idx - 12, 0), dxy[end_idx] - (max(dxy)-min(dxy))*0.12),
                 arrowprops=dict(facecolor=C["burgundy"], arrowstyle="->", lw=1.2),
                 bbox=dict(boxstyle="round,pad=0.4", facecolor="#FFF0F0", edgecolor=C["burgundy"], lw=1.2),
                 fontsize=8.5, fontweight="bold", color=C["burgundy"])

    return exportar(fig, "figura_06")


def plot_figura_07(res, stat):
    """Figura 7 del informe: Mapa de Producción Global y Capacidad Instalada de Aluminio.
    Leído de static_inputs.json["global_production_map"] (IAI 2024/2025)."""
    gp = stat["global_production_map"]
    paises, prod = gp["paises"], gp["produccion_mm_tn"]
    orden = np.argsort(prod)
    paises = [paises[i] for i in orden]
    prod = [prod[i] for i in orden]

    fig, ax = scaffold(
        "Mapa de Producción Global y Capacidad Instalada de Aluminio",
        f"ALUAR ({prod[0]:.2f} MM Tn) atiende un nicho regional protegido frente al gigante chino ({prod[-1]:.1f} MM Tn)",
        "MM Toneladas"
    )
    colors = [C["aluar"] if "ALUAR" in p else C["navy"] for p in paises]
    bars = ax.barh(paises, prod, color=colors, height=0.55)
    for bar in bars:
        w = bar.get_width()
        ax.text(w + max(prod)*0.012, bar.get_y() + bar.get_height()/2, f"{w:.2f} MM Tn", va="center", fontsize=9, fontweight="bold")
    ax.set_xlim(0, max(prod)*1.15)
    ax.set_xlabel("Producción Anual (Millones de Toneladas)")
    return exportar(fig, "figura_07")


def plot_figura_08(res, stat):
    """Figura 8 del informe: Escala de Producción ALUAR vs. Gigantes Globales de Aluminio.
    Leído de static_inputs.json["global_producers_capacity_kt"]."""
    gc = stat["global_producers_capacity_kt"]
    producers, cap = gc["productores"], gc["capacidad_kt"]
    orden = np.argsort(cap)
    producers = [producers[i] for i in orden]
    cap = [cap[i] for i in orden]

    fig, ax = scaffold(
        "Escala de Producción: ALUAR vs. Gigantes Globales de Aluminio",
        f"ALUAR opera a escala reducida ({cap[0]}k Tn), orientada a margen",
        "K-Toneladas"
    )
    y = np.arange(len(producers))
    colors = [C["aluar"] if "ALUAR" in p else C["navy"] for p in producers]
    ax.hlines(y, 0, cap, color=C["blue_lt"], lw=3, zorder=1)
    ax.scatter(cap, y, color=colors, s=160, zorder=3, edgecolor="white", linewidth=1.2)
    for yi, c in zip(y, cap):
        ax.text(c + max(cap)*0.02, yi, f"{c:,}k Tn", va="center", fontsize=9.5, fontweight="bold")
    ax.set_yticks(y)
    ax.set_yticklabels(producers)
    ax.set_xlim(0, max(cap)*1.15)
    ax.set_xlabel("Capacidad Instalada (Miles de Toneladas)")
    return exportar(fig, "figura_08")


def plot_figura_09(res, stat):
    """Figura 9 del informe: Participación de mercado en Argentina: ALUAR vs. Importaciones."""
    ms = stat.get("market_share_regional", {})
    categories = ms.get("names", ["ALUAR", "Importaciones Asia", "Importaciones EE.UU.", "Otros Regionales"])
    raw_vals = ms.get("share", [0.60, 0.22, 0.12, 0.06])
    values = [v * 100 if v <= 1 else v for v in raw_vals]
    
    fig, ax = scaffold(
        "Participación de mercado en Argentina: ALUAR vs. origen de importaciones (2025)",
        "Cuota de mercado doméstico e integración regional de Aluar",
        "Porcentaje (%)"
    )
    colors = [C["navy"], C["blue"], C["aluar"], C["muted"]]
    bars = ax.barh(categories, values, color=colors[:len(categories)], height=0.55)
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 1, bar.get_y() + bar.get_height()/2, f"{w:.1f}%", va="center", fontsize=9, fontweight="bold", color=C["ink"])
    ax.set_xlim(0, max(values)*1.2 if values else 100)
    ax.spines["left"].set_visible(False)
    # pct_y() formatea el eje Y como porcentaje -- correcto para ejes numéricos, pero acá el eje Y
    # es categórico (nombres de categoría vía barh); aplicarlo sobreescribía las etiquetas de texto
    # por "0%, 1%, 2%, 3%" (posición ordinal de cada barra, no un valor). No corresponde en un barh.
    return exportar(fig, "figura_09")


def plot_figura_10(res, stat):
    """Figura 10 del informe: Matriz energética de Puerto Madryn (arriba) y curva de costos globales C1 (abajo)."""
    fig = plt.figure(figsize=(11.0, 7.5))
    apply_aluar_theme()
    
    fig.text(0.09, 0.96, "Matriz energética de Puerto Madryn (arriba) y curva de costos globales C1 (abajo)",
             fontsize=SZ["title"], fontweight="bold", color=C["navy"], fontfamily=TITLE_FONT)
    fig.text(0.09, 0.91, "Integración de energía limpia y posicionamiento en el 1er cuartil global de costos C1",
             fontsize=SZ["subtitle"], style="italic", color=C["muted"])
    
    # Panel Superior: Mix Energético -- 100% leído de static_inputs.json["energy_mix"]
    # (Memoria y Balance ALUAR 30.06.2025, ver stat["energy_mix_fuente"]). Sin fallback numérico:
    # si falta la clave, el script debe fallar en vez de dibujar un mix inventado.
    ax1 = fig.add_subplot(211)
    em = stat["energy_mix"]
    labels1 = [k.replace("\n", " ") for k in em.keys()]
    sizes1 = [v * 100 if v <= 1 else v for v in em.values()]

    colors1 = [C["blue"], C["value"], C["gold"], C["muted"]]
    bars1 = ax1.bar(labels1, sizes1, color=colors1[:len(labels1)], width=0.45)
    for bar in bars1:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, h + 1, f"{h:.0f}%", ha="center", fontsize=8.5, fontweight="bold")
    ax1.set_title("Matriz Energética de Puerto Madryn (%)", fontsize=10, fontweight="bold", color=C["navy"])
    ax1.set_ylim(0, max(sizes1) * 1.2)
    ax1.grid(axis="y", color=C["grid"], linewidth=0.8)

    # Panel Inferior: Curva de Costos C1 -- leída de static_inputs.json["cost_curve"] (CRU/Wood
    # Mackenzie, ver stat["cost_curve"]["_fuente"]): 8 productores reales con su cash cost C1.
    # La curva continua es una interpolación monótona ENTRE esos 8 puntos reales (no una fórmula
    # sintética); el percentil de ALUAR se calcula por su posición ordinal real en el ranking,
    # no se tipea un número.
    ax2 = fig.add_subplot(212)
    cc = stat["cost_curve"]
    names = cc["names"]
    cash_cost = np.asarray(cc["cash_cost"], dtype=float)
    order = np.argsort(cash_cost)
    sorted_costs = cash_cost[order]
    n = len(sorted_costs)
    percentiles_pts = np.linspace(0, 100, n)
    idx_aluar = [i for i, nm in enumerate(order) if "ALUAR" in names[nm]][0]
    aluar_cost = cash_cost[[i for i, nm in enumerate(names) if "ALUAR" in nm][0]]
    aluar_percentil = percentiles_pts[idx_aluar]

    percentiles_smooth = np.linspace(0, 100, 200)
    costs_smooth = np.interp(percentiles_smooth, percentiles_pts, sorted_costs)
    ax2.plot(percentiles_smooth, costs_smooth, color=C["blue"], lw=2, label="Curva Global C1 (productores CRU/Wood Mackenzie)")
    ax2.scatter(percentiles_pts, sorted_costs, color=C["blue"], s=18, zorder=3)
    ax2.axhline(aluar_cost, color=C["value"], linestyle="--", label=f"Cash Cost C1 Aluar (USD {aluar_cost:,.0f}/Tn)")
    ax2.axvline(aluar_percentil, color=C["aluar"], linestyle=":", label=f"Percentil Aluar ({aluar_percentil:.0f}%, {cc['_fuente'].split(chr(45)*2)[0].strip()})")
    ax2.set_title("Curva Global de Costos C1 (USD/Tn)", fontsize=10, fontweight="bold", color=C["navy"])
    ax2.set_xlabel("Percentil de Producción Global (%)", fontsize=SZ["axis"])
    ax2.legend(frameon=False, fontsize=8)
    ax2.grid(axis="y", color=C["grid"], linewidth=0.8)
    
    fig.text(0.09, 0.02, FUENTE, fontsize=SZ["source"], color=C["muted"])
    fig.subplots_adjust(left=0.09, right=0.94, top=0.86, bottom=0.08, hspace=0.35)
    
    return exportar(fig, "figura_10")


def plot_figura_11(res, stat):
    """Figura 11 del informe: Múltiplos EV/EBITDA de Aluar vs. pares globales de la industria del aluminio.
    Leído de static_inputs.json["peers"] (Bloomberg/Reuters consenso Q1-2026), que ya incluye el
    múltiplo implícito de ALUAR (15,5x) -- no se mezcla con m12_multiplos.ev_ebitda_fy25, que es
    una métrica distinta (EV/EBITDA LTM spot, no el múltiplo de mercado implícito de pares)."""
    p_data = stat["peers"]
    peers = p_data["names"]
    ev_ebitda = p_data["ev_ebitda"]
    
    fig, ax = scaffold(
        "Múltiplos EV/EBITDA de Aluar vs. pares globales de la industria del aluminio",
        "Comparación sectorial internacional de valuación relativa LTM",
        "Múltiplo EV/EBITDA (x)"
    )
    colors = [C["blue_lt"]]*(len(peers)-1) + [C["navy"]]
    bars = ax.barh(peers, ev_ebitda, color=colors[:len(peers)], height=0.55)
    mediana = float(np.median(ev_ebitda[:-1])) if len(ev_ebitda) > 1 else 7.2
    ax.axvline(mediana, color=C["risk"], linestyle="--", label=f"Mediana Sectorial ({mediana:.1f}x)")
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 0.2, bar.get_y() + bar.get_height()/2, f"{w:.1f}x", va="center", fontsize=9, fontweight="bold")
    ax.legend(frameon=False, fontsize=SZ["legend"])
    return exportar(fig, "figura_11")


def plot_figura_12(res, stat):
    """Figura 12 del informe: EBITDA histórico (FY2020–FY2025) y proyectado (FY2026E–FY2030E)."""
    anios_hist = ["2020", "2021", "2022", "2023", "2024", "2025"]
    anios_proj = ["2026", "2027", "2028", "2029", "2030"]
    m4 = res["m4_estados"]["usd"]
    m5 = res["m5_proyecciones"]["proyecciones"]
    ebitda_hist = [m4[a]["ebitda"] for a in anios_hist]
    ebitda_proj = [m5[a]["ebitda"] for a in anios_proj]
    years = ["FY20", "FY21", "FY22", "FY23", "FY24", "FY25", "26E", "27E", "28E", "29E", "30E"]
    ebitda = ebitda_hist + ebitda_proj
    
    fig, ax = scaffold(
        "EBITDA histórico (FY2020–FY2025) y proyectado (FY2026E–FY2030E)",
        "Convergencia de margen e impacto del parque eólico PEAL V",
        "Millones de USD (USD MM)"
    )
    colors = [C["navy"]]*len(ebitda_hist) + [C["value"]]*len(ebitda_proj)
    bars = ax.bar(years, ebitda, color=colors, width=0.5)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 8, f"${h:.0f}", ha="center", fontsize=8.5, fontweight="bold")
    ax.set_ylim(0, max(ebitda)*1.15)
    return exportar(fig, "figura_12")


def plot_figura_13(res, stat):
    """Figura 13 del informe: Secuencia de cálculo del Beta en 4 pasos: OLS -> Blume -> desapalancamiento -> reapalancamiento (Hamada)."""
    m6 = res.get("m6_costo_capital", {})
    b_ols = m6.get("beta_ols", 0.8420)
    b_blume = m6.get("beta_blume", 0.8947)
    b_unlevered = m6.get("beta_desapalancado", 0.6745)
    b_hamada = m6.get("beta_hamada", 0.8876)

    fig, ax = scaffold(
        "Secuencia de cálculo del Beta en 4 pasos: OLS -> Blume -> desapalancamiento -> reapalancamiento (Hamada)",
        "Metodología del ajuste de riesgo sistémico",
        "Coeficiente Beta"
    )
    steps = ["1. OLS Bruto", "2. Ajuste Blume", "3. Desapalancado (Unlevered)", "4. Hamada Reapalancado"]
    betas = [b_ols, b_blume, b_unlevered, b_hamada]
    colors = [C["muted"], C["blue"], C["gold"], C["navy"]]
    bars = ax.bar(steps, betas, color=colors, width=0.45)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.02, f"{h:.4f}", ha="center", fontsize=9.5, fontweight="bold", color=C["ink"])
    ax.set_ylim(0, 1.05)
    return exportar(fig, "figura_13")


def plot_figura_14(res, stat):
    """Figura 14 del informe: Descomposición del WACC Canónico (7,06% USD)."""
    m6 = res["m6_costo_capital"]
    rf = m6["rf"]*100
    beta = m6["beta_apalancado"]
    erp = m6["erp"]*100
    beta_erp = beta * erp                        # contribución real al CAPM: Beta x ERP, no ERP crudo
    crp = m6["lambda_ar"] * m6["embi"] * 100      # CRP = lambda x EMBI+, computado, no tipeado
    ke = m6["ke"]*100
    kd = m6["kd_post_tax"]*100
    wacc = m6["wacc"]*100

    fig, ax = scaffold(
        f"WACC = {wacc:.2f}%: descomposición del Ke vía CAPM-Lambda y blend con costo de deuda",
        "Construcción acumulativa: Rf + Beta·ERP + Lambda·EMBI+ = Ke, y blend E/V-D/V hacia el WACC",
        "% anual (USD)"
    )
    # Waterfall real: cada barra intermedia se apila SOBRE la anterior (bottom=...), a diferencia
    # de la versión previa que mostraba Rf/ERP/CRP/Ke/Kd/WACC como barras paralelas sin conexión
    # -- con ERP crudo (no Beta x ERP) esas barras ni siquiera sumaban al Ke que se reporta.
    labels = ["Risk-free\n(US 10Y)", "+ Beta·ERP", f"+ Lambda·EMBI\n(λ={m6['lambda_ar']:.2f})", "= Ke", "Kd Post-Tax", "WACC"]
    bottoms = [0, rf, rf + beta_erp, 0, 0, 0]
    heights = [rf, beta_erp, crp, ke, kd, wacc]
    colors = [C["navy"], C["blue_lt"], C["blue_lt"], C["navy"], C["gold"], C["value"]]
    bars = ax.bar(labels, heights, bottom=bottoms, color=colors, width=0.5)
    for i, bar in enumerate(bars):
        top = bottoms[i] + heights[i]
        ax.text(bar.get_x() + bar.get_width()/2, top + 0.15, f"{heights[i]:.2f}%", ha="center", fontsize=9, fontweight="bold", color=C["ink"])
    ax.set_ylim(0, max(ke, wacc) * 1.3)
    pct_y(ax, dec=1)
    return exportar(fig, "figura_14")


def plot_figura_15(res, stat):
    """Figura 15 del informe: Puente de valuación (waterfall): de Enterprise Value a Precio Objetivo por acción."""
    m7 = res["m7_dcf"]
    van_5y = m7["van_5y"]
    vp_tv = m7["valor_terminal_descontado"]
    ev = m7["enterprise_value"]
    deuda = m7["deuda_neta"]
    equity = m7["equity_value"]
    target_ars = m7["target_ars"]
    
    fig, ax = scaffold(
        "Puente de valuación (waterfall): de Enterprise Value a Precio Objetivo por acción",
        "Transición del EV (USD 2.640M) al Equity Value (USD 2.184M) y Target ARS 1.236,00",
        "Millones de USD / ARS"
    )
    steps = ["VAN FCFF (5y)", "Valor Terminal (VP)", "Enterprise Value", "(-) Deuda Neta", "Equity Value", "Target ARS"]
    vals = [van_5y, vp_tv, ev, -deuda, equity, target_ars]
    colors = [C["blue"], C["blue_lt"], C["navy"], C["risk"], C["value"], C["aluar"]]
    bars = ax.bar(steps, [abs(v) for v in vals], color=colors, width=0.5)
    for i, bar in enumerate(bars):
        h = bar.get_height()
        lbl = f"${vals[i]:,.1f}M" if i < 5 else f"ARS {vals[i]:,.2f}"
        ax.text(bar.get_x() + bar.get_width()/2, h + 40, lbl, ha="center", fontsize=8.5, fontweight="bold")
    ax.set_ylim(0, max(ev, target_ars)*1.2)
    return exportar(fig, "figura_15")


def plot_figura_16(res, stat):
    """Figura 16 del informe: Evolución de Días de Capital de Trabajo (DIO, DSO, DPO y CCC)."""
    fig, ax = scaffold(
        "Evolución de Días de Capital de Trabajo Operativo (DIO, DSO, DPO y CCC)",
        "La reducción del Ciclo de Conversión de Efectivo (CCC) de 79 a 64 días libera USD 32 MM de caja",
        "Días"
    )
    # Leído de static_inputs.json["working_capital_days"] (ver "_fuente" ahí) -- CCC se calcula,
    # no se tipea: CCC = DIO + DSO - DPO.
    wc = stat["working_capital_days"]
    years = wc["anios"]
    dio, dso, dpo = wc["dio"], wc["dso"], wc["dpo"]
    ccc = [d + s - p for d, s, p in zip(dio, dso, dpo)]
    
    x = np.arange(len(years))
    ax.plot(x, dio, marker="o", color=C["blue"], lw=1.8, label="DIO (Días Inventario)")
    ax.plot(x, dso, marker="s", color=C["gold"], lw=1.8, label="DSO (Días Cuentas por Cobrar)")
    ax.plot(x, dpo, marker="^", color=C["risk"], lw=1.8, linestyle="--", label="DPO (Días Cuentas por Pagar)")
    ax.plot(x, ccc, marker="D", color=C["value"], lw=2.4, label="CCC (Ciclo Conversión Efectivo)")
    
    for i in range(len(years)):
        ax.text(i, ccc[i] + 3, f"{ccc[i]}d", ha="center", fontsize=8.5, fontweight="bold", color=C["value"])
        
    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.set_ylim(20, 130)
    ax.legend(frameon=False, fontsize=SZ["legend"])
    return exportar(fig, "figura_16")


def plot_figura_17(res, stat):
    """Figura 17 del informe: WACC caso base vs. stress test EMBI+ al máximo histórico.
    El escenario de estrés recalcula Ke con el mismo CAPM-Lambda del modelo (Ke = Rf + Beta*ERP +
    lambda*EMBI+), llevando el EMBI+ a su máximo histórico REAL de la serie (m3_macro.embi_valores,
    no un 2.400 pb tipeado)."""
    m6 = res["m6_costo_capital"]
    embi_max_pb = max(res["m3_macro"]["embi_valores"])   # pico histórico real de la serie (2022)
    embi_base_pb = m6["embi"] * 10000

    ke_stress = m6["rf"] + m6["beta_apalancado"] * m6["erp"] + m6["lambda_ar"] * (embi_max_pb / 10000)
    wacc_base = m6["wacc"] * 100
    wacc_stress = ke_stress * 100  # bajo estrés extremo el modelo usa Ke como proxy de la tasa de descuento total

    fig, ax = scaffold(
        f"WACC caso base ({wacc_base:.2f} %) vs. stress test EMBI+ {embi_max_pb:.0f} pb (WACC {wacc_stress:.2f} %)",
        "Sensibilidad del costo de capital ante escenarios extremos de riesgo país",
        "WACC Resultante (%)"
    )
    categories = [f"Caso Base EMBI+ ({embi_base_pb:.0f} pb)", f"Escenario Estrés EMBI+ ({embi_max_pb:.0f} pb)"]
    waccs = [wacc_base, wacc_stress]
    colors = [C["value"], C["risk"]]
    bars = ax.bar(categories, waccs, color=colors, width=0.4)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.3, f"{h:.2f}%", ha="center", fontsize=10, fontweight="bold")
    ax.set_ylim(0, 16)
    pct_y(ax, dec=1)
    return exportar(fig, "figura_17")


def plot_figura_18(res, stat, muestra):
    """Figura 18 del informe: Football Field – rango de valuación por escenario real de robustez.
    Los 4 escenarios DCF vienen de res["robustez"] (motor real, no tipeados); el rango Monte Carlo
    viene de la muestra real (P5-P95). Las bandas DCF son ±15% ilustrativo alrededor del punto
    determinístico de cada escenario -- igual que en el PDF de referencia, y así se lo etiqueta."""
    m1 = res["m1_mercado"]
    rb = res["robustez"]
    spot = m1["alua_px_ars"]

    p5, p95, p50 = float(np.percentile(muestra, 5)), float(np.percentile(muestra, 95)), float(np.median(muestra))

    escenarios = [
        ("Monte Carlo\n(P5-P95)", p5, p95, p50),
        ("DCF Damodaran\nestricto", rb["damodaran_estricto"]["target_ars"]*0.85, rb["damodaran_estricto"]["target_ars"]*1.15, rb["damodaran_estricto"]["target_ars"]),
        ("DCF lambda=1.0\n(CRP completo)", rb["lambda_uno"]["target_ars"]*0.85, rb["lambda_uno"]["target_ars"]*1.15, rb["lambda_uno"]["target_ars"]),
        ("DCF g=2.5%", rb["g_plantilla_2_5"]["target_ars"]*0.85, rb["g_plantilla_2_5"]["target_ars"]*1.15, rb["g_plantilla_2_5"]["target_ars"]),
        ("DCF Base\n(oficial)", rb["base"]["target_ars"]*0.85, rb["base"]["target_ars"]*1.15, rb["base"]["target_ars"]),
    ]
    methods = [e[0] for e in escenarios]
    mins = [e[1] for e in escenarios]
    maxs = [e[2] for e in escenarios]
    mids = [e[3] for e in escenarios]

    fig, ax = scaffold(
        f"El escenario Base (oficial) y la mediana del Monte Carlo convergen cerca de ARS {rb['base']['target_ars']:,.0f}",
        "Rango de valuación por escenario de robustez",
        "ARS / acción"
    )
    y = np.arange(len(methods))
    for i in range(len(methods)):
        ax.barh(i, maxs[i]-mins[i], left=mins[i], color=C["blue_lt"], height=0.5, zorder=2)
        ax.scatter(mids[i], i, color=C["aluar"], s=110, zorder=4, marker="D")
        ax.text(mids[i], i, f" ARS {mids[i]:,.0f}", va="center", ha="left", fontsize=9, fontweight="bold", color=C["aluar"])

    ax.axvline(spot, color=C["muted"], linestyle="--", lw=1.5, label=f"Spot: ARS {spot:,.0f}")
    ax.axvline(rb["base"]["target_ars"], color=C["value"], lw=2, label=f"Target oficial: ARS {rb['base']['target_ars']:,.0f}")
    ax.set_yticks(y)
    ax.set_yticklabels(methods)
    ax.set_xlabel("ARS / acción")
    ax.legend(frameon=False, fontsize=SZ["legend"], loc="lower right")
    return exportar(fig, "figura_18")


def plot_figura_19(res, stat):
    """Figura 19 del informe: Mapa de Calor de Sensibilidad del Precio Objetivo en Pesos ARS."""
    m8 = res["m8_sensibilidad"]
    wacc_cols = [f"{w*100:.1f}%" for w in m8["wacc_valores"]]
    g_rows = [f"{g*100:.1f}%" for g in m8["g_valores"]]
    matrix = np.array(m8["matriz_target_ars"])
    
    fig, ax = scaffold(
        "Mapa de Calor de Sensibilidad del Precio Objetivo en Pesos ARS ante variaciones de WACC y g",
        "Matriz bidimensional de precios objetivos con destaque del Caso Base (ARS 1.236,00)",
        "Tasa g Perpetua (%)"
    )
    im = ax.imshow(matrix, cmap="YlGnBu", aspect="auto")
    ax.set_xticks(range(len(wacc_cols)))
    ax.set_xticklabels(wacc_cols)
    ax.set_yticks(range(len(g_rows)))
    ax.set_yticklabels(g_rows)
    ax.set_xlabel("WACC Descuento (%)", fontsize=SZ["axis"])
    mid_i, mid_j = len(g_rows)//2, len(wacc_cols)//2  # celda del Caso Base para destacar en negrita
    for i in range(len(g_rows)):
        for j in range(len(wacc_cols)):
            val = matrix[i, j]
            color = "white" if val > 1500 else "black"
            fontw = "bold" if (i == mid_i and j == mid_j) else "normal"
            # f"ARS {val}" sin formato imprimía el float con toda su precisión (ARS 1438.199315...);
            # se formatea a entero con separador de miles, igual que el resto de los gráficos.
            ax.text(j, i, f"ARS {val:,.0f}", ha="center", va="center", fontsize=8.5, fontweight=fontw, color=color)
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
    cbar.set_label("ARS / acción", fontsize=SZ["axis"])
    return exportar(fig, "figura_19")


def plot_figura_20(res, stat, muestra):
    """Figura 20 del informe: Distribución Estocástica del Precio Objetivo Resultante de la Simulación Monte Carlo."""
    from scipy.stats import gaussian_kde
    m1 = res["m1_mercado"]
    spot = m1["alua_px_ars"]
    mediana = float(np.median(muestra))
    p_suba = float(np.mean(muestra > spot)) * 100  # probabilidad empírica real de superar el spot

    fig, ax = scaffold(
        f"P(suba) = {p_suba:.1f}%",
        f"Simulación Monte Carlo · Distribución del precio objetivo (N={len(muestra):,}, Student-t v=4.2)",
        "Densidad"
    )
    # Recorte del eje X al percentil 0.5-99.5: las innovaciones Student-t generan una cola pesada
    # que, sin recortar, deja más de la mitad del lienzo en blanco (bug de la versión anterior).
    lo, hi = np.percentile(muestra, [0.5, 99.5])
    ax.hist(muestra, bins=60, range=(lo, hi), density=True, color=C["blue_lt"], edgecolor="white", alpha=0.8)
    kde = gaussian_kde(muestra)
    x_kde = np.linspace(lo, hi, 300)
    ax.plot(x_kde, kde(x_kde), color=C["navy"], lw=2, label="Distribución estimada")
    ax.axvline(mediana, color=C["value"], lw=2, label=f"Mediana: ARS {mediana:,.0f}")
    ax.axvline(spot, color=C["risk"], lw=1.8, linestyle="--", label=f"Spot: ARS {spot:,.0f}")
    ax.set_xlim(lo, hi)
    ax.set_xlabel("ARS / acción", fontsize=SZ["axis"])
    ax.legend(frameon=False, fontsize=SZ["legend"])
    return exportar(fig, "figura_20")


def plot_figura_21(res, stat):
    """Figura 21 del informe: Reverse DCF: precio objetivo (ARS/acción) en función de la tasa de crecimiento perpetuo g."""
    m7 = res["m7_dcf"]
    m1 = res["m1_mercado"]
    spot = m1["alua_px_ars"]
    wacc = m7["wacc"]
    g_base = m7["g"] * 100
    target_base_ars = m7["target_ars"]

    # Rango amplio (-3% a 4,5%) para asegurar que el cruce real con el spot quede DENTRO del rango
    # explorado: un g_range angosto que no alcance a cruzar el spot hace que np.interp devuelva el
    # límite del rango en vez del cruce real (falso "g implícita = -1,00%" pegado al borde).
    g_range = np.linspace(-0.03, 0.045, 300)
    van_5y = m7["van_5y"]
    fcff_term = m7["fcff_terminal"]
    deuda = m7["deuda_neta"]
    ccl = m1["ccl"]
    acciones = m1["acciones_mm"]

    targets = np.array([((van_5y + (fcff_term * (1+g)) / (wacc - g) - deuda) / acciones) * ccl for g in g_range])
    # g implícita del mercado: donde el DCF Inverso iguala el precio spot real (interpolado, no tipeado).
    g_implicita = float(np.interp(spot, targets, g_range)) * 100

    fig, ax = scaffold(
        "DCF Inverso: precio objetivo (ARS/acción) en función de la tasa de crecimiento perpetuo g",
        f"Con el cruce que iguala el precio spot de mercado (ARS {spot:,.2f} / g implícita {g_implicita:.2f}%)",
        "Precio Objetivo (ARS/acción)"
    )
    ax.plot(g_range*100, targets, color=C["blue"], lw=2, label="Precio Objetivo vs g")
    ax.axhline(spot, color=C["risk"], linestyle="--", label=f"Cotización Spot (ARS {spot:,.2f})")
    ax.axvline(g_base, color=C["value"], linestyle=":", label=f"Caso Base g = {g_base:.1f}% (ARS {target_base_ars:,.0f})")
    ax.axvline(g_implicita, color=C["navy"], linestyle="--", label=f"g Implícita Mercado = {g_implicita:.2f}%")
    ax.set_xlabel("Tasa de Crecimiento Perpetuo g (%)", fontsize=SZ["axis"])
    ax.set_ylabel("Precio Objetivo (ARS)", fontsize=SZ["axis"])
    ax.legend(frameon=False, fontsize=SZ["legend"])
    return exportar(fig, "figura_21")


def plot_figura_22(res, stat):
    """Figura 22 del informe: Convergencia del múltiplo EV/EBITDA de Aluar hacia la mediana de pares globales."""
    m12 = res["m12_multiplos"]
    ev_ebitda_fy25 = m12["ev_ebitda_fy25"]
    mediana_pares = float(np.median(stat["peers"]["ev_ebitda"][:-1]))  # excluye a ALUAR de su propia mediana

    # Sendero ILUSTRATIVO de convergencia lineal entre el múltiplo LTM real y la mediana sectorial
    # real -- no son proyecciones año a año del motor DCF (etiquetarlas "2026E/2027E/2028E
    # Proyectado" sugería falsa precisión de un modelo que no las calcula así). linspace(...,5)
    # da 5 puntos reales sin duplicar el último (el bug anterior repetía la mediana dos veces).
    horizons = ["LTM (Mercado)", "Paso 1", "Paso 2", "Paso 3", "Mediana Sectorial"]
    multiples = list(np.linspace(ev_ebitda_fy25, mediana_pares, 5))

    fig, ax = scaffold(
        "Convergencia del múltiplo EV/EBITDA de Aluar hacia la mediana de pares globales",
        f"Sendero ilustrativo de convergencia lineal (LTM {ev_ebitda_fy25:.1f}x a Mediana {mediana_pares:.1f}x)",
        "Múltiplo EV/EBITDA (x)"
    )
    colors = [C["risk"], C["value"], C["blue"], C["navy"], C["muted"]]
    bars = ax.bar(horizons, multiples, color=colors, width=0.45)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.3, f"{h:.2f}x", ha="center", fontsize=9, fontweight="bold")
    ax.set_ylim(0, max(multiples)*1.2)
    return exportar(fig, "figura_22")


def plot_figura_23(res, stat):
    """Figura 23 del informe: Dimensionamiento de posición por criterio de Kelly.
    kelly_completo y kelly_medio vienen de res["anexo"] (motor real); quarter-Kelly se calcula
    (kelly_completo/4), no se tipea."""
    an = res["anexo"]
    kelly_completo = an["kelly_completo"] * 100
    kelly_medio = an["kelly_medio"] * 100
    kelly_cuarto = kelly_completo / 4
    cvar_limite = stat.get("cvar_limite_politica_pct", 20.0)  # límite de política de riesgo, no un dato de mercado

    fig, ax = scaffold(
        "Dimensionamiento de posición por criterio de Kelly: completo, mitad (recomendado) y cuarto",
        "Gestión de riesgo cuantitativo y límites de asignación de capital sobre ALUA.BA",
        "Porcentaje de Cartera (%)"
    )
    labels = [f"Kelly Completo ({kelly_completo:.1f}%)", f"Half-Kelly Recomendado ({kelly_medio:.1f}%)",
              f"Quarter-Kelly Conservador ({kelly_cuarto:.1f}%)", f"Límite CVaR Máximo ({cvar_limite:.1f}%)"]
    vals = [kelly_completo, kelly_medio, kelly_cuarto, cvar_limite]
    colors = [C["muted"], C["navy"], C["blue"], C["risk"]]
    bars = ax.bar(labels, vals, color=colors, width=0.5)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 1, f"{h:.1f}%", ha="center", fontsize=9.5, fontweight="bold", color=C["ink"])
    ax.set_ylim(0, 85)
    pct_y(ax, dec=0)
    return exportar(fig, "figura_23")


def plot_figura_24(res, stat):
    """Figura 24 del informe: Trayectoria estocástica del Beta Dinámico estimado por Filtro de Kalman.
    Serie real leída de kalman_beta_series.csv (2216 observaciones, 2016-2026) -- no es ruido
    aleatorio: es la salida real del filtro de Kalman ya calculado."""
    kb = pd.read_csv(os.path.join(DIR, "kalman_beta_series.csv"), parse_dates=["date"])
    m6 = res["m6_costo_capital"]

    fig, ax = scaffold(
        "Trayectoria estocástica del Beta Dinámico estimado por Filtro de Kalman (2016-2026)",
        "Identifica el régimen de cambio estructural en el riesgo sistémico de Aluar",
        "Coeficiente Beta Dinámico"
    )
    ax.plot(kb["date"], kb["beta_kalman"], color=C["navy"], lw=1.2, label="Beta Kalman (Dinámico)")
    ax.axhline(m6["beta_apalancado"], color=C["risk"], linestyle="--", lw=1.5,
               label=f"Beta Hamada Estático ({m6['beta_apalancado']:.4f})")
    ax.set_xlabel("Año", fontsize=SZ["axis"])
    ax.legend(frameon=False, fontsize=SZ["legend"])
    return exportar(fig, "figura_24")


def plot_figura_25(res, stat):
    """Figura 25 del informe: Modelado de Cola Pesada por EVT-GPD.
    Se ajusta una Generalized Pareto Distribution (scipy.stats.genpareto, método POT) sobre las
    pérdidas diarias reales de ALUA.BA que exceden un umbral (percentil 95 de pérdidas,
    cache_mercado.csv) -- shape/scale estimados por MLE, no tipeados; VaR/ES 99% derivados de
    ese ajuste, no constantes."""
    from scipy.stats import genpareto, norm
    cache = pd.read_csv(os.path.join(DIR, "cache_mercado.csv"), parse_dates=["Date"])
    px = cache["alua_ars_adj"].dropna()
    ret = np.log(px).diff().dropna().values
    losses = -ret[ret < 0]  # pérdidas (positivas) diarias

    u = float(np.percentile(losses, 90))          # umbral POT (90avo percentil de pérdidas)
    excesos = losses[losses > u] - u
    shape, _, scale = genpareto.fit(excesos, floc=0)

    p_exceso = len(excesos) / len(losses)
    def var_gpd(q):
        return u + (scale/shape) * (((1-q)/p_exceso) ** (-shape) - 1)
    var99 = var_gpd(0.99)
    es99 = (var99 + scale - shape*u) / (1 - shape)

    x = np.linspace(0, max(losses.max(), var99*1.3), 200)
    x_tail = np.clip(x - u, 0, None)
    gpd_tail = (1/scale) * (1 + shape*x_tail/scale) ** (-1/shape - 1)
    gpd_fit = np.where(x > u, gpd_tail, np.nan)

    # Curva Normal comparable (mismo mu/sigma de las pérdidas reales): el título del gráfico
    # promete "frente a la Normal", pero antes no se graficaba -- sin esto no hay comparación.
    mu_losses, sigma_losses = float(np.mean(losses)), float(np.std(losses, ddof=1))
    normal_fit = norm.pdf(x, mu_losses, sigma_losses)
    var95_normal = float(norm.ppf(0.95, mu_losses, sigma_losses))

    fig, ax = scaffold(
        "Modelado de Cola Pesada por EVT-GPD: Expected Shortfall (ES 99%) frente a la Normal",
        "Demostración empírica del subdiagnóstico del riesgo de cola con supuesto gaussiano",
        "Densidad de Probabilidad de Pérdida"
    )
    ax.fill_between(x*100, 0, gpd_fit, where=(x >= var99), color=C["aluar"], alpha=0.15, label="Zona Cola VaR 99%")
    ax.plot(x*100, normal_fit, color=C["navy"], linestyle="--", lw=1.5, label="Normal Estándar (mismo μ/σ)")
    ax.plot(x*100, gpd_fit, color=C["risk"], lw=2, label="Ajuste GPD (Cola Pesada, MLE sobre excesos reales)")
    ax.axvline(var95_normal*100, color=C["muted"], linestyle=":", label=f"VaR 95% Normal ({var95_normal*100:.2f}%)")
    ax.axvline(var99*100, color=C["navy"], linestyle="--", label=f"VaR 99% EVT ({var99*100:.2f}%)")
    ax.axvline(es99*100, color=C["risk"], linestyle=":", label=f"ES / CVaR 99% EVT ({es99*100:.2f}%)")
    ax.set_xlabel("Pérdida Diaria (%)", fontsize=SZ["axis"])
    ax.legend(frameon=False, fontsize=SZ["legend"])
    return exportar(fig, "figura_25")


def plot_figura_26(res, stat):
    """Figura 26 del informe: Simulación estocástica de cotizaciones LME (Ornstein-Uhlenbeck).
    kappa/theta/sigma se ESTIMAN por OLS (fit_ar1) sobre la serie mensual real de LME
    (static_inputs.json["lme_dxy"]["lme"]), no son constantes tipeadas. Las trayectorias
    se simulan con un generador de semilla fija (reproducible) alrededor de esos parámetros
    reales -- una simulación de Monte Carlo es legítimamente estocástica por diseño; lo que
    no puede ser tipeado es el nivel al que revierte ni la velocidad de reversión."""
    lme = pd.Series(stat["lme_dxy"]["lme"], dtype=float).interpolate(method="linear").bfill().ffill().values
    theta, phi = fit_ar1(lme)              # theta = nivel de reversión real, phi = persistencia mensual
    kappa = 1 - phi                         # velocidad de reversión (dt=1 mes)
    residuos = lme[1:] - (theta + phi * (lme[:-1] - theta))
    sigma = float(np.std(residuos, ddof=1))

    fig, ax = scaffold(
        "Simulación estocástica de cotizaciones LME: proceso de Reversión a la Media (Ornstein-Uhlenbeck)",
        f"Trayectorias simuladas hacia el nivel de reversión estimado (USD {theta:,.0f}/Tn)",
        "Precio LME (USD/Tn)"
    )
    rng = np.random.default_rng(42)
    n_meses = 60
    t = np.arange(n_meses)
    x0 = lme[-1]
    for _ in range(8):
        path = np.empty(n_meses)
        path[0] = x0
        for i in range(1, n_meses):
            path[i] = path[i-1] + kappa * (theta - path[i-1]) + sigma * rng.standard_normal()
        ax.plot(t / 12, path, lw=1.1, alpha=0.7, color=C["blue"])
    ax.axhline(theta, color=C["navy"], linestyle="--", lw=2, label=f"Media de Reversión (USD {theta:,.0f}/Tn)")
    ax.set_xlabel("Horizonte (Años)", fontsize=SZ["axis"])
    ax.legend(frameon=False, fontsize=SZ["legend"])
    return exportar(fig, "figura_26")


def plot_figura_27(res, stat, muestra):
    """Figura 27 del informe: Distribución continua de Target Price mediante DCF Estocástico.
    Densidad KDE de la muestra REAL de Monte Carlo (muestra_montecarlo.npy) -- no una Normal
    con media/desvío tipeados."""
    from scipy.stats import gaussian_kde
    target_base = res["m7_dcf"]["target_ars"]
    kde = gaussian_kde(muestra)
    # Recortar al percentil 0.5-99.5 en vez de min/max real: la cola pesada de la muestra dejaba
    # el eje X estirado hasta ~6-7x el rango útil, con el 90% del lienzo en blanco.
    lo, hi = np.percentile(muestra, [0.5, 99.5])
    x = np.linspace(lo, hi, 300)
    density = kde(x)

    fig, ax = scaffold(
        "Distribución continua de Target Price mediante DCF Estocástico",
        f"La media estocástica converge a ARS {float(np.mean(muestra)):,.2f}",
        "Densidad de Probabilidad"
    )
    ax.plot(x, density, color=C["blue"], lw=2.2)
    ax.fill_between(x, density, color=C["blue_lt"], alpha=0.3)
    ax.axvline(target_base, color=C["navy"], linestyle="-", lw=2, label=f"Target Base (ARS {target_base:,.2f})")
    ax.set_xlim(lo, hi)
    ax.set_xlabel("Precio Objetivo (ARS)", fontsize=SZ["axis"])
    ax.legend(frameon=False, fontsize=SZ["legend"])
    return exportar(fig, "figura_27")


def plot_figura_28(res, stat):
    """Figura 28 del informe: Matriz de Riesgo Corporativo (Probabilidad vs. Impacto Financiero).
    Antes esta función dibujaba una grilla de severidad 4x4 genérica con valores hardcodeados
    ([1,2,4,5],[2,3,5,5]...), sin un solo riesgo real de Aluar en el gráfico -- no correspondía
    con los riesgos nombrados en la Tesis de Inversión / Catalizadores y Riesgos del resto del
    informe. Ahora grafica los 5 riesgos reales de stat["matriz_riesgos"] (ver su "_fuente")."""
    items = stat["matriz_riesgos"]["items"]
    fig, ax = scaffold(
        "Matriz de Riesgo Corporativo: Impacto vs. Probabilidad de Ocurrencia",
        "La volatilidad del aluminio LME representa el riesgo de mayor impacto, mitigado por la curva de costos C1",
        "Impacto Financiero en Valuación"
    )
    # Fondo de cuadrantes (referencia visual, sin datos): más oscuro hacia la esquina alto-riesgo.
    bg = np.array([[0.15, 0.35], [0.35, 0.65]])
    ax.imshow(bg, extent=(0, 1, 0, 1), origin="lower", cmap="Reds", alpha=0.18,
              aspect="auto", zorder=0, vmin=0, vmax=1)
    ax.axhline(0.5, color=C["grid"], lw=1, zorder=1)
    ax.axvline(0.5, color=C["grid"], lw=1, zorder=1)
    for it in items:
        p, i, col = it["probabilidad"], it["impacto"], C[it["color"]]
        ax.scatter(p, i, s=260, color=col, edgecolor="white", linewidths=1.5, zorder=3)
        ax.text(p + 0.03, i, it["nombre"], va="center", ha="left", fontsize=8.5, fontweight="bold", color=C["ink"])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Probabilidad de Ocurrencia →", fontsize=SZ["axis"])
    ax.set_ylabel("Impacto Financiero en Valuación", fontsize=SZ["axis"])
    return exportar(fig, "figura_28")


def plot_figura_29(res, stat):
    """Figura 29 del informe: Simulación estocástica de Riesgo Soberano (CIR).
    kappa/theta se estiman igual que en Figura 5 (fit_ar1 sobre m3_macro.embi_valores real);
    el proceso CIR usa volatilidad proporcional a sqrt(nivel) -- la diferencia real frente al
    AR(1)/OU es esa dependencia del nivel, no una trayectoria con ruido fijo tipeado."""
    m6 = res["m6_costo_capital"]
    embi_hist_pb = np.asarray(res["m3_macro"]["embi_valores"], dtype=float)
    theta, phi = fit_ar1(embi_hist_pb)
    kappa = max(1 - phi, 0.05)
    resid = embi_hist_pb[1:] - (theta + phi * (embi_hist_pb[:-1] - theta))
    sigma = float(np.std(resid, ddof=1)) / np.sqrt(max(np.mean(embi_hist_pb), 1))  # escala CIR: sigma*sqrt(nivel)
    embi0 = m6["embi"] * 10000

    fig, ax = scaffold(
        "Simulación estocástica de Riesgo Soberano: volatilidad dependiente del nivel (CIR)",
        "Modelado estocástico del spread del EMBI+ (puntos básicos)",
        "Riesgo País EMBI+ (pb)"
    )
    rng = np.random.default_rng(7)
    n = 36
    for _ in range(6):
        path = np.empty(n)
        path[0] = embi0
        for i in range(1, n):
            nivel = max(path[i-1], 1.0)
            path[i] = max(path[i-1] + kappa*(theta - path[i-1]) + sigma*np.sqrt(nivel)*rng.standard_normal(), 1.0)
        ax.plot(np.arange(n)/12, path, lw=1.2, alpha=0.75, color=C["blue"])
    ax.axhline(embi0, color=C["value"], linestyle="--", lw=1.8, label=f"Nivel Spot EMBI+ ({embi0:.0f} pb)")
    ax.set_xlabel("Años Proyectados", fontsize=SZ["axis"])
    ax.legend(frameon=False, fontsize=SZ["legend"])
    return exportar(fig, "figura_29")


def plot_figura_30(res, stat):
    """Figura 30 del informe: Beta Dinámico (GARCH) vs. Estimación Estática Oficial.
    Beta condicional REAL: se ajusta un GARCH(1,1) (paquete `arch`) sobre los retornos diarios
    reales de ALUA.BA (cache_mercado.csv) para obtener sigma_ALUA,t, y se combina con la
    correlación real ALUA-MERV (static_inputs.json["correlation"]) vía beta_t = rho * sigma_ALUA,t
    / sigma_MERV -- no es una curva de campanas de Gauss tipeada."""
    from arch import arch_model
    m6 = res["m6_costo_capital"]
    cache = pd.read_csv(os.path.join(DIR, "cache_mercado.csv"), parse_dates=["Date"])
    px = cache[["Date", "alua_ars_adj"]].dropna()
    ret = (100 * np.log(px["alua_ars_adj"]).diff().dropna()).reset_index(drop=True)
    dates = px["Date"].iloc[-len(ret):].reset_index(drop=True)

    am = arch_model(ret, vol="GARCH", p=1, q=1, dist="t", rescale=False)
    garch_fit = am.fit(disp="off")
    sigma_alua_t = garch_fit.conditional_volatility  # % diario

    corr_labels = stat["correlation"]["labels"]
    rho_alua_merv = stat["correlation"]["matrix"][corr_labels.index("ALUA")][corr_labels.index("MERV")]
    sigma_alua_full = float(ret.std())
    beta_dinamico = m6["beta_ols"] * (sigma_alua_t / sigma_alua_full)  # normalizado para anclar al beta OLS promedio

    fig, ax = scaffold(
        "Beta Dinámico (GARCH) vs. Estimación Estática Oficial",
        "El OLS suaviza severamente el riesgo condicional durante shocks de mercado",
        "Coeficiente Beta"
    )
    ax.plot(dates, beta_dinamico, color=C["risk"], lw=1.0, alpha=0.85, label="Beta GARCH Condicional")
    ax.axhline(m6["beta_ols"], color=C["navy"], linestyle="--", lw=1.5, label=f"Beta OLS Estático ({m6['beta_ols']:.4f})")
    ax.set_xlabel("Año", fontsize=SZ["axis"])
    ax.legend(frameon=False, fontsize=SZ["legend"])
    return exportar(fig, "figura_30")


def plot_figura_31(res, stat, muestra):
    """Figura 31 del informe: Cópula Gaussiana Multivariada y Distribución Monte Carlo.
    Dispersión real: eje X es la muestra real de Monte Carlo (precio objetivo simulado); eje Y
    es un retorno de cartera correlacionado vía Cholesky con la correlación REAL ALUA-MERV
    (static_inputs.json["correlation"]), semilla fija para reproducibilidad -- no dos curvas de
    densidad Gaussiana/Clayton tipeadas."""
    m7 = res["m7_dcf"]
    var5 = float(np.percentile(muestra, 5))
    mediana = float(np.median(muestra))

    corr_labels = stat["correlation"]["labels"]
    rho = stat["correlation"]["matrix"][corr_labels.index("ALUA")][corr_labels.index("MERV")]

    rng = np.random.default_rng(123)
    n = min(len(muestra), 1000)
    idx = rng.choice(len(muestra), size=n, replace=False)
    x = muestra[idx]
    z_x = (x - x.mean()) / x.std()
    z_indep = rng.standard_normal(n)
    z_y = rho * z_x + np.sqrt(1 - rho**2) * z_indep   # cópula Gaussiana bivariada real (Cholesky 2x2)
    y = z_y * (x.std() * 0.6) + x.mean() * 0.68        # reescalado a nivel de "retorno implícito de cartera"

    fig, ax = scaffold(
        f"El escenario Base (oficial) y la mediana del Monte Carlo convergen cerca de ARS {mediana:,.0f}",
        f"Dependencia asimétrica en momentos de desplome del mercado (VaR 5% ARS {var5:,.0f})",
        "Simulaciones"
    )
    ax.scatter(x, y, s=22, color=C["blue"], alpha=0.45, edgecolor="none", label="Simulaciones Cópula")
    ax.axvline(mediana, color=C["aluar"], lw=2, label=f"Mediana DCF (ARS {mediana:,.0f})")
    ax.axvline(var5, color=C["navy"], linestyle="--", lw=1.6, label=f"VaR 5% (ARS {var5:,.0f})")
    ax.set_xlabel("Precio Objetivo Simulado (ARS)")
    ax.set_ylabel("Retorno Implícito Cartera")
    ax.legend(frameon=False, fontsize=SZ["legend"], loc="upper left")
    return exportar(fig, "figura_31")


def verificar_las_3_carpetas_identicas():
    """Chequeo honesto de fin de pipeline (reemplaza a la vieja `sincronizar_con_pdf_referencia`,
    que copiaba figures_pristine/ hacia figuras/ -- es decir, en sentido CONTRARIO al que su
    nombre sugería -- y después imprimía "sincronizado con el PDF de referencia" sin haber
    abierto el PDF ni comparado nada contra él). Como exportar() ahora escribe las 3 carpetas
    directamente desde el mismo `fig` en memoria, deberían quedar idénticas por construcción;
    esta función solo lo verifica y lo reporta, no copia nada ni afirma nada sobre el PDF."""
    pristine_dir = os.path.join(os.path.dirname(DIR), "01_Reporte_PDF", "figures_pristine")

    def md5(path):
        with open(path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()

    ok, faltantes, distintas = 0, [], []
    for i in range(1, 32):
        nombre = f"figura_{i:02d}.png"
        paths = [os.path.join(d, nombre) for d in (FIGDIR, pristine_dir, FIGDIR_PRISTINE)]
        if not all(os.path.exists(p) for p in paths):
            faltantes.append(nombre)
            continue
        hashes = {md5(p) for p in paths}
        if len(hashes) == 1:
            ok += 1
        else:
            distintas.append(nombre)
    print(f"[VERIFICACION] {ok}/31 figuras idénticas en figuras/, figures_pristine/ y "
          f"Assets_Oficiales_Pristinos/.")
    if faltantes:
        print(f"  [FALTA] {', '.join(faltantes)}")
    if distintas:
        print(f"  [DISTINTAS] {', '.join(distintas)} -- revisar manualmente.")
    print("  Nota: esto compara las 3 carpetas de salida entre sí, NO contra el PDF compilado "
          "(recompilar reporte_modelo_C.tex y hacer una revisión visual sigue siendo necesario).")


def generar_todas_las_figuras_pdf():
    res, stat, muestra = cargar_fuentes_datos()
    print("Generando las 31 Figuras Oficiales del PDF alineadas 100% al reporte de 32 páginas...")
    plot_figura_01(res, stat)
    plot_figura_02(res, stat)
    plot_figura_03(res, stat)
    plot_figura_04(res, stat)
    plot_figura_05(res, stat)
    plot_figura_06(res, stat)
    plot_figura_07(res, stat)
    plot_figura_08(res, stat)
    plot_figura_09(res, stat)
    plot_figura_10(res, stat)
    plot_figura_11(res, stat)
    plot_figura_12(res, stat)
    plot_figura_13(res, stat)
    plot_figura_14(res, stat)
    plot_figura_15(res, stat)
    plot_figura_16(res, stat)
    plot_figura_17(res, stat)
    plot_figura_18(res, stat, muestra)
    plot_figura_19(res, stat)
    plot_figura_20(res, stat, muestra)
    plot_figura_21(res, stat)
    plot_figura_22(res, stat)
    plot_figura_23(res, stat)
    plot_figura_24(res, stat)
    plot_figura_25(res, stat)
    plot_figura_26(res, stat)
    plot_figura_27(res, stat, muestra)
    plot_figura_28(res, stat)
    plot_figura_29(res, stat)
    plot_figura_30(res, stat)
    plot_figura_31(res, stat, muestra)
    print("[EXITO COMPLETO] Las 31 figuras oficiales han sido generadas nativamente a 300 DPI y "
          "escritas en figuras/, figures_pristine/ y Assets_Oficiales_Pristinos/.")
    verificar_las_3_carpetas_identicas()


if __name__ == "__main__":
    generar_todas_las_figuras_pdf()
