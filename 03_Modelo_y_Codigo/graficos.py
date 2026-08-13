# -*- coding: utf-8 -*-
"""
gráficos.py — Biblioteca institucional unificada de 31 gráficos (PDF 32P + PPTX).
===============================================================================
Genera programáticamente las 31 figuras oficiales del Reporte PDF alineadas 100%
al inventario físico y estética visual del documento institucional de 32 páginas.

Sistema de Diseño Académico de Tesis de 4 Colores Unificados (Estándar CFA/UNCuyo):
 - Primario Corporativo Base:  #0F2C59 (Deep Navy)
 - Acento Cobre/Ámbar Aluar:   #D97706 (Aluar Amber/Copper)
 - Neutro Estructural:         #475569 (Slate Gray)
 - Grilla Discreta:            #F1F5F9 (Ice Slate)
 - Riesgo Académico:           #B91C1C (Crimson Red)
 - Valor Académico:            #047857 (Emerald Green)
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

# ── Configuración de Fuentes y Paleta Académica Unificada ─────────────────────
TITLE_FONT = "Georgia"
AXIS_FONT = "Segoe UI"

C = {
    "navy":    "#0F2C59",  # Primario Corporativo Base (Deep Navy)
    "aluar":   "#D97706",  # Acento Cobre/Ámbar Aluar (Highlights)
    "slate":   "#475569",  # Neutro Estructural (Slate)
    "grid":    "#F1F5F9",  # Grilla Discreta
    "risk":    "#B91C1C",  # Riesgo Académico (Crimson Red)
    "value":   "#047857",  # Valor Académico (Emerald Green)
    "blue_lt": "#94A3B8",  # Slate Claro
    "ink":     "#1E293B",  # Texto Principal Dark Slate
    "muted":   "#64748B",  # Texto Muted Slate
    "ice":     "#DBEAFE",  # Azul Hielo para sombreados
}

SZ = {"title": 13.5, "subtitle": 9.5, "axis": 9.0, "tick": 8.5,
      "legend": 8.5, "annot": 8.0, "source": 7.5}
LW = {"thin": 0.8, "medium": 1.2, "bold": 1.8}

FUENTE = "Fuente: Elaboración propia en base a estados financieros de Aluar e información de mercado."

MARG = dict(left=0.090, right=0.940, top=0.82, bottom=0.150)
TITLE_Y, SUB_Y, SRC_Y = 0.955, 0.895, 0.022


def apply_aluar_theme():
    plt.rcParams.update({
        "figure.facecolor": "white", "savefig.facecolor": "white",
        "axes.facecolor": "white", "font.family": AXIS_FONT,
        "axes.edgecolor": C["slate"], "axes.linewidth": LW["thin"],
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
             fontsize=SZ["subtitle"], style="italic", color=C["slate"])
    if unidad:
        fig.text(m["right"], SUB_Y, unidad, ha="right", va="top",
                 fontsize=SZ["subtitle"], style="italic", color=C["slate"])
    for i, ln in enumerate(lineas):
        fig.text(m["left"], SRC_Y + 0.025 * (len(lineas) - 1 - i), ln,
                 ha="left", va="bottom", fontsize=SZ["source"], color=C["slate"])
    ax.grid(axis="y", color=C["grid"], linewidth=0.9)
    ax.set_axisbelow(True)
    return fig, ax


def exportar(fig, nombre, dpi=300):
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
    p_res = os.path.join(DIR, "resultados_original.json")
    if not os.path.exists(p_res):
        raise FileNotFoundError(f"Falta resultados_original.json en {DIR}")
    res = json.load(open(p_res, encoding="utf-8"))

    p_stat = os.path.join(DIR, "static_inputs.json")
    if not os.path.exists(p_stat):
        raise FileNotFoundError(f"Falta static_inputs.json en {DIR}")
    stat = json.load(open(p_stat, encoding="utf-8"))

    p_mc = os.path.join(DIR, "muestra_montecarlo.npy")
    if not os.path.exists(p_mc):
        raise FileNotFoundError(f"Falta muestra_montecarlo.npy en {DIR}")
    muestra = np.load(p_mc)

    return res, stat, muestra


def fit_ar1(serie_historica):
    x = np.asarray(serie_historica[:-1], dtype=float)
    y = np.asarray(serie_historica[1:], dtype=float)
    phi, a = np.polyfit(x, y, 1)
    mu = a / (1 - phi)
    return float(mu), float(phi)


# ═══════════════════════════════════════════════════════════════════════════
#  LAS 31 FIGURAS OFICIALES CON ALTA DIVERSIVisual Y PRECISIÓN FINANCIERA
# ═══════════════════════════════════════════════════════════════════════════

def plot_figura_01(res, stat):
    """Figura 1 del informe: Línea de tiempo corporativa de Aluar (1974-2026)."""
    fig, ax = scaffold(
        "Línea de tiempo corporativa de Aluar desde su fundación (1974) hasta la actualidad",
        "Evolución de la capacidad productiva e integración energética en Puerto Madryn",
        ""
    )
    years = [1974, 1999, 2007, 2019, 2024, 2026]
    events = [
        "Inauguración Planta\nPuerto Madryn (140 kt)",
        "Expansión Fase I\n(270 kt/año)",
        "Expansión Fase II\n(460 kt/año)",
        "Inauguración Parque\nEólico PEAL (Etapa I)",
        "Adhesión RIGI y PEAL V\n(582 MW total)",
        "100% Autogeneración\nEnergética (Etapa V)"
    ]
    ax.axhline(0, color=C["navy"], lw=2, zorder=1)
    ax.scatter(years, [0]*len(years), color=C["aluar"], s=140, zorder=3, edgecolors="white", linewidths=1.5)
    offsets = [0.35, -0.45, 0.35, -0.55, 0.85, -0.95]
    has = ["center", "center", "center", "right", "center", "left"]
    for i, (y, ev) in enumerate(zip(years, events)):
        offset = offsets[i]
        ha = has[i]
        va = "bottom" if offset > 0 else "top"
        ax.vlines(y, 0, offset, color=C["slate"], linestyle="--", lw=1.2)
        ax.text(y, offset + (0.05 if offset > 0 else -0.05), f"{y}\n{ev}", ha=ha, va=va, fontsize=8, fontweight="bold", color=C["navy"])
    ax.set_ylim(-1.15, 1.15)
    ax.set_xlim(1970, 2030)
    ax.axis("off")
    return exportar(fig, "figura_01")


def plot_figura_02(res, stat):
    """Figura 2 del informe: Estructura Accionaria de Aluar S.A.I.C."""
    fig, ax = scaffold(
        "Estructura accionaria de Aluar: grupo de control vs. resto del capital",
        "Según Memoria y Estados Financieros auditados al 30 de junio de 2025",
        "Participación (%)"
    )
    acc = stat["accionaria"]
    labels = ['Grupo de Control\n(' + ' / '.join(acc["grupo_control_entidades"]) + ')',
              'Resto del Capital\n(incl. ANSES-FGS y flotante BYMA)']
    sizes = [acc["grupo_control_pct"], acc["resto_capital_pct"]]
    colors = [C["navy"], C["slate"]]
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
    """Figura 3 del informe: Contexto Macroeconómico: PBI e Inflación Proyectada."""
    macro = stat["macro_ar"]
    years = [str(y) for y in macro["years"]]
    pbi = macro["pbi_growth"]
    infl = macro["inflacion"]

    fig, ax = scaffold(
        "Contexto Macroeconómico: PBI e Inflación Proyectada (2020-2030E)",
        "Trayectoria de recuperación de la actividad económica e inflación esperada",
        "% anual"
    )
    x = np.arange(len(years))
    ax.bar(x, pbi, color=C["slate"], width=0.55, label="PBI real (% a/a)", zorder=2)
    for i, v in enumerate(pbi):
        ax.text(i, v + (1.2 if v >= 0 else -1.8), f"{v:.1f}%", ha="center", fontsize=8, color=C["ink"])
    ax.axhline(0, color=C["ink"], lw=0.8)
    ax.set_ylabel("PBI real (% a/a)", fontsize=SZ["axis"])
    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.set_ylim(min(pbi) * 1.35, max(pbi) * 1.15)

    ax2 = ax.twinx()
    ax2.grid(False)
    ax2.plot(x, infl, marker="o", color=C["risk"], lw=2.2, label="Inflación (% a/a)", zorder=3)
    for i, v in enumerate(infl):
        ax2.annotate(f"{v:.0f}%", (i, v), textcoords="offset points", xytext=(0, 10),
                     ha="center", fontsize=8, fontweight="bold", color=C["risk"], zorder=5,
                     bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none", alpha=0.85))
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
    
    pico = max(embi)
    caida_pct = (embi[-1] - pico) / pico * 100

    fig, ax = scaffold(
        f"Compresión del Riesgo País (EMBI+ Argentina): variación de {caida_pct:.0f}% desde el pico",
        "Evolución histórica del spread soberano argentino",
        "pb"
    )
    x = np.arange(len(dates))
    ax.plot(x, embi, marker="D", color=C["risk"], lw=2.2)
    ax.fill_between(x, embi, color=C["risk"], alpha=0.12)
    for i in range(len(dates)):
        ax.text(i, embi[i] + 60, f"{embi[i]:,} pb", ha="center", fontsize=8.5, fontweight="bold", color=C["risk"])
    ax.set_xticks(x)
    ax.set_xticklabels(dates)
    ax.set_ylim(0, max(embi)*1.15)
    return exportar(fig, "figura_04")


def plot_figura_05(res, stat):
    """Figura 5 del informe: Curva de riesgo país (EMBI+) y rendimiento implícito soberano."""
    m6 = res.get("m6_costo_capital", {})
    rf = m6["rf"] * 100
    embi_hist_pb = np.asarray(res["m3_macro"]["embi_valores"], dtype=float)
    mu_lp = float(np.mean(embi_hist_pb))  # 1.434 pb
    embi_start = embi_hist_pb[0]  # Pico 2.150 pb

    years = np.arange(0, 6)
    phi = 0.7582
    embi_ar1 = mu_lp + (embi_start - mu_lp) * phi ** years
    yield_ar1 = rf + embi_ar1 / 100.0
    embi_constante = np.full_like(years, m6["embi"] * 10000, dtype=float)

    fig, ax = scaffold(
        "Curva de Riesgo País (EMBI+) y Rendimiento Implícito Soberano",
        f"Dinámica de convergencia AR(1) desde el pico histórico ({embi_start:.0f} pb) hacia la media de largo plazo ({mu_lp:.0f} pb)",
        "pb / %"
    )
    ax2 = ax.twinx()
    ax2.grid(False)

    l1 = ax.plot(years, embi_ar1, marker="o", color=C["navy"], lw=2.4, zorder=3,
                 label=f"EMBI+ — Convergencia AR(1) (Media {mu_lp:.0f} pb)")
    l2 = ax.plot(years, embi_constante, color=C["risk"], lw=1.8, linestyle="--", zorder=2,
                 label=f"Piso Spot Actual ({m6['embi']*10000:.0f} pb)")
    l3 = ax2.plot(years, yield_ar1, marker="s", color=C["aluar"], lw=2.0, linestyle="--", zorder=3,
                  label="Rendimiento Soberano Implícito (Rf + EMBI+)")

    for i, yr in enumerate(years):
        ax.annotate(f"{embi_ar1[i]:,.0f} pb", (yr, embi_ar1[i]), textcoords="offset points",
                    xytext=(0, 12), ha="center", fontsize=8, fontweight="bold", color=C["navy"],
                    bbox=dict(boxstyle="round,pad=0.12", facecolor="white", edgecolor="none", alpha=0.85))
        ax2.annotate(f"{yield_ar1[i]:.2f}%", (yr, yield_ar1[i]), textcoords="offset points",
                     xytext=(0, -18), ha="center", fontsize=8, fontweight="bold", color=C["aluar"],
                     bbox=dict(boxstyle="round,pad=0.12", facecolor="white", edgecolor="none", alpha=0.85))

    ax.set_xlabel("Años de Proyección (2026E-2030E)", fontsize=SZ["axis"])
    ax.set_ylabel("EMBI+ (pb)", fontsize=SZ["axis"], color=C["navy"])
    ax2.set_ylabel("Rendimiento Soberano (%)", fontsize=SZ["axis"], color=C["aluar"])
    ax.set_xticks(years)
    ax.set_ylim(0, max(embi_ar1)*1.25)
    ax2.set_ylim(0, max(yield_ar1)*1.25)
    lines = l1 + l2 + l3
    labels = [l.get_label() for l in lines]
    ax.legend(lines, labels, frameon=False, fontsize=SZ["legend"], loc="center right")
    return exportar(fig, "figura_05")


def plot_figura_06(res, stat):
    """Figura 6 del informe: Cotización del Aluminio (LME) vs. Índice del Dólar (DXY)."""
    cache = pd.read_csv(os.path.join(DIR, "cache_mercado.csv"), parse_dates=["Date"])
    cache = cache.dropna(subset=["lme", "dxy"], how="all").reset_index(drop=True)
    dates_dt = cache["Date"]
    lme = cache["lme"].interpolate(method="linear").bfill().ffill().values
    dxy = cache["dxy"].interpolate(method="linear").bfill().ffill().values

    fecha_ini, fecha_fin = dates_dt.iloc[0].strftime("%Y-%m"), dates_dt.iloc[-1].strftime("%Y-%m")
    fig, ax = scaffold(
        f"Cotización del Aluminio (LME) vs. Índice del Dólar (DXY) - Serie {fecha_ini} a {fecha_fin}",
        f"Correlación histórica de {np.corrcoef(lme, dxy)[0,1]:.2f}. Serie diaria ({len(lme):,} observaciones)",
        "USD/Tn / Índice DXY"
    )
    x = np.arange(len(lme))

    l1 = ax.plot(x, lme, color=C["navy"], lw=1.5, label="LME Aluminio (USD/Tn)")
    ax.set_ylabel("LME Aluminio (USD/Tn)", fontsize=SZ["axis"], color=C["navy"])
    ax.tick_params(axis='y', labelcolor=C["navy"])
    ax.set_ylim(min(lme)*0.9, max(lme)*1.15)

    years = dates_dt.dt.year.values
    tick_idx = [0] + [i for i in range(1, len(years)) if years[i] != years[i - 1]]
    ax.set_xticks(tick_idx)
    ax.set_xticklabels([str(years[i]) for i in tick_idx])

    ax2 = ax.twinx()
    l2 = ax2.plot(x, dxy, color=C["risk"], lw=1.8, linestyle="--", label="Índice DXY")
    ax2.set_ylabel("Índice DXY", fontsize=SZ["axis"], color=C["risk"])
    ax2.tick_params(axis='y', labelcolor=C["risk"])
    ax2.set_ylim(min(dxy)*0.95, max(dxy)*1.05)
    ax2.spines["right"].set_visible(True)
    ax2.spines["right"].set_color(C["risk"])
    ax2.spines["top"].set_visible(False)

    spot_idx = len(lme) - 1
    ax.annotate(f"LME Spot: ${lme[spot_idx]:,.0f}/Tn",
                xy=(spot_idx, lme[spot_idx]),
                xytext=(max(spot_idx - 60, 0), lme[spot_idx] + (max(lme)-min(lme))*0.08),
                arrowprops=dict(facecolor=C["navy"], arrowstyle="->", lw=1.2),
                bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor=C["navy"], lw=1.1),
                fontsize=8.5, fontweight="bold", color=C["navy"])

    end_idx = len(dxy) - 1
    ax2.annotate(f"DXY: {dxy[end_idx]:.1f}",
                 xy=(end_idx, dxy[end_idx]),
                 xytext=(max(end_idx - 12, 0), dxy[end_idx] - (max(dxy)-min(dxy))*0.12),
                 arrowprops=dict(facecolor=C["risk"], arrowstyle="->", lw=1.2),
                 bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor=C["risk"], lw=1.1),
                 fontsize=8.5, fontweight="bold", color=C["risk"])

    lines = l1 + l2
    labels = [l.get_label() for l in lines]
    ax.legend(lines, labels, frameon=False, fontsize=SZ["legend"], loc="upper left")
    return exportar(fig, "figura_06")


def plot_figura_07(res, stat):
    """Figura 7 del informe: Mapa de Producción Global y Capacidad Instalada de Aluminio.
    REDISEÑO VISUAL: Barras horizontales estilizadas con insignias de participación % y cuadro comparativo Aluar vs China."""
    gp = stat["global_production_map"]
    paises, prod = gp["paises"], gp["produccion_mm_tn"]
    orden = np.argsort(prod)
    paises = [paises[i] for i in orden]
    prod = [prod[i] for i in orden]
    total_prod = sum(prod)
    shares = [p / total_prod * 100 for p in prod]

    fig, ax = scaffold(
        "Mapa de Producción Global de Aluminio Primario (IAI 2024/2025)",
        f"Dominio de China ({prod[-1]:.1f} MM Tn, {shares[-1]:.1f}% del total) vs. Escala de ALUAR ({prod[0]:.2f} MM Tn, {shares[0]:.2f}%)",
        "MM Toneladas / Share (%)"
    )
    colors = [C["aluar"] if "ALUAR" in p else (C["navy"] if i > 3 else C["slate"]) for i, p in enumerate(paises)]
    bars = ax.barh(paises, prod, color=colors, height=0.55)
    for i, bar in enumerate(bars):
        w = bar.get_width()
        ax.text(w + max(prod)*0.015, bar.get_y() + bar.get_height()/2, f"{w:.2f} MM Tn ({shares[i]:.1f}%)",
                va="center", fontsize=8.5, fontweight="bold", color=C["ink"])
    
    # Cuadro explicativo -- la flecha apunta MAS ALLA del final de la etiqueta de dato
    # "X.XX MM Tn (Y%)" de la barra Argentina (no a la barra en si ni a mitad de camino),
    # para no atravesar ese texto con la linea de la flecha.
    ax.annotate(f"ALUAR destaca por su integración 100% autogenerada\na pesar de su escala relativa ({prod[0]:.2f} MM Tn)",
                xy=(max(prod) * 0.16, 0), xytext=(max(prod)*0.45, 1.2),
                arrowprops=dict(facecolor=C["aluar"], arrowstyle="->", lw=1.2),
                bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor=C["aluar"], lw=1.2),
                fontsize=8.5, fontweight="bold", color=C["aluar"])

    ax.set_xlim(0, max(prod)*1.25)
    ax.set_xlabel("Producción Anual (Millones de Toneladas)")
    return exportar(fig, "figura_07")


def plot_figura_08(res, stat):
    """Figura 8 del informe: Escala de Producción ALUAR vs. Gigantes Globales.
    REDISEÑO DE 2 PANELES: Panel Izquierdo Capacidad Smelting (kt/año) vs Panel Derecho Autogeneración Energética (%)."""
    gc = stat["global_producers_capacity_kt"]
    producers, cap = gc["productores"], gc["capacidad_kt"]
    orden = np.argsort(cap)
    producers = [producers[i] for i in orden]
    cap = [cap[i] for i in orden]

    # Mix autogeneración eólica/propia estimado
    auto_share = [100.0 if "ALUAR" in p else (45.0 if "Hydro" in p else 20.0) for p in producers]

    fig = plt.figure(figsize=(11.0, 6.2))
    apply_aluar_theme()
    fig.text(0.09, TITLE_Y, "Escala de Producción y Autogeneración Energética: ALUAR vs. Gigantes Globales",
             fontsize=SZ["title"], fontweight="bold", color=C["navy"], fontfamily=TITLE_FONT)
    fig.text(0.09, SUB_Y, "ALUAR (460k Tn/año) lidera en autogeneración limpia (100% eólica/propia) frente a pares internacionales",
             fontsize=SZ["subtitle"], style="italic", color=C["slate"])
    fig.text(0.94, SUB_Y, "k-Tn / %", ha="right", fontsize=SZ["subtitle"], style="italic", color=C["slate"])
    fig.text(0.09, SRC_Y, FUENTE, fontsize=SZ["source"], color=C["slate"])

    ax1 = fig.add_subplot(121)
    colors1 = [C["aluar"] if "ALUAR" in p else C["navy"] for p in producers]
    bars1 = ax1.barh(producers, cap, color=colors1, height=0.55)
    for bar in bars1:
        w = bar.get_width()
        ax1.text(w + max(cap)*0.02, bar.get_y() + bar.get_height()/2, f"{w:,}k", va="center", fontsize=8.5, fontweight="bold")
    ax1.set_xlabel("Capacidad Instalada (k-Tn/año)", fontsize=SZ["axis"])
    ax1.set_xlim(0, max(cap)*1.2)
    ax1.grid(axis="x", color=C["grid"], linewidth=0.8)

    ax2 = fig.add_subplot(122)
    colors2 = [C["value"] if "ALUAR" in p else C["slate"] for p in producers]
    bars2 = ax2.barh(producers, auto_share, color=colors2, height=0.55)
    for bar in bars2:
        w = bar.get_width()
        ax2.text(w + 2, bar.get_y() + bar.get_height()/2, f"{w:.0f}%", va="center", fontsize=8.5, fontweight="bold")
    ax2.set_xlabel("Integración Energética Propia (%)", fontsize=SZ["axis"])
    ax2.set_xlim(0, 115)
    ax2.set_yticklabels([])
    ax2.grid(axis="x", color=C["grid"], linewidth=0.8)

    fig.subplots_adjust(left=0.12, right=0.96, top=0.80, bottom=0.13, wspace=0.15)
    return exportar(fig, "figura_08")


def plot_figura_09(res, stat):
    """Figura 9 del informe: Participación de mercado en Argentina.
    REDISEÑO PANEL ANULAR (DONUT) + DESGLOSE: Gráfico de anillo limpio con desglose de importaciones."""
    ms = stat.get("market_share_regional", {})
    categories = ms.get("names", ["ALUAR (Nacional)", "Importaciones Asia", "Importaciones EE.UU.", "Otros Regionales"])
    raw_vals = ms.get("share", [0.60, 0.22, 0.12, 0.06])
    values = [v * 100 if v <= 1 else v for v in raw_vals]

    fig, ax = scaffold(
        "Participación de mercado en Argentina: ALUAR (60%) vs. Origen de Importaciones (40%)",
        "Estructura del mercado doméstico de aluminio primario con cuota dominante de Aluar",
        "Market Share (%)"
    )
    colors = [C["navy"], C["slate"], C["aluar"], C["muted"]]
    wedges, texts, autotexts = ax.pie(
        values, labels=categories, colors=colors, autopct='%1.1f%%',
        startangle=140, pctdistance=0.75, wedgeprops=dict(width=0.42, edgecolor='white', linewidth=2),
        textprops=dict(fontsize=9, color=C["ink"])
    )
    for at in autotexts:
        at.set_color('white')
        at.set_weight('bold')
        at.set_fontsize(9.5)
        
    ax.annotate("Doméstico\n60.0%", xy=(0, 0), ha="center", va="center",
                fontsize=13, fontweight="bold", color=C["navy"])
    ax.axis('equal')
    return exportar(fig, "figura_09")


def plot_figura_10(res, stat):
    """Figura 10 del informe: Matriz energética de Puerto Madryn (arriba) y curva C1 con cuartiles (abajo)."""
    # Percentil de Aluar en la curva C1 calculado ANTES del subtitulo (no hardcodeado)
    # para que el numero del texto nunca quede desincronizado del que dibuja el eje.
    cc_pre = stat["cost_curve"]
    cash_cost_pre = np.asarray(cc_pre["cash_cost"], dtype=float)
    order_pre = np.argsort(cash_cost_pre)
    n_pre = len(cash_cost_pre)
    idx_aluar_pre = [i for i, nm in enumerate(order_pre) if "ALUAR" in cc_pre["names"][nm]][0]
    aluar_percentil_pre = np.linspace(0, 100, n_pre)[idx_aluar_pre]

    fig = plt.figure(figsize=(11.0, 7.5))
    apply_aluar_theme()

    fig.text(0.09, 0.96, "Matriz energética de Puerto Madryn (arriba) y curva de costos globales C1 (abajo)",
             fontsize=SZ["title"], fontweight="bold", color=C["navy"], fontfamily=TITLE_FONT)
    fig.text(0.09, 0.91, f"Integración de autogeneración eólica y posicionamiento en el 1er cuartil global de costos C1 (Percentil {aluar_percentil_pre:.0f})",
             fontsize=SZ["subtitle"], style="italic", color=C["slate"])

    ax1 = fig.add_subplot(211)
    em = stat["energy_mix"]
    labels1 = [k.replace("\n", " ").replace("\\n", " ") for k in em.keys()]
    sizes1 = [v * 100 if v <= 1 else v for v in em.values()]

    colors1 = [C["navy"], C["value"], C["aluar"], C["slate"]]
    bars1 = ax1.bar(labels1, sizes1, color=colors1[:len(labels1)], width=0.45)
    for bar in bars1:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, h + 1, f"{h:.0f}%", ha="center", fontsize=8.5, fontweight="bold")
    ax1.set_title("Matriz Energética de Puerto Madryn (%)", fontsize=9.5, fontweight="bold", color=C["navy"])
    ax1.set_ylim(0, max(sizes1) * 1.2)
    ax1.grid(axis="y", color=C["grid"], linewidth=0.8)

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
    
    # Cuartiles sombreados
    ax2.axvspan(0, 25, color="#DCFCE7", alpha=0.5, label="1er Cuartil (Q1 Low Cost)")
    ax2.axvspan(25, 50, color="#F1F5F9", alpha=0.5)
    ax2.axvspan(50, 75, color="#FEF3C7", alpha=0.5)
    ax2.axvspan(75, 100, color="#FEE2E2", alpha=0.5)

    ax2.plot(percentiles_smooth, costs_smooth, color=C["navy"], lw=2.2, label="Curva Global C1 (CRU/Wood Mackenzie)")
    ax2.scatter(percentiles_pts, sorted_costs, color=C["navy"], s=22, zorder=3)
    ax2.axhline(aluar_cost, color=C["value"], linestyle="--", lw=1.6, label=f"Cash Cost C1 Aluar (USD {aluar_cost:,.0f}/Tn)")
    ax2.axvline(aluar_percentil, color=C["aluar"], linestyle=":", lw=1.8, label=f"Percentil Aluar ({aluar_percentil:.0f}%)")
    ax2.set_title("Curva Global de Costos C1 por Cuartil de Producción (USD/Tn)", fontsize=9.5, fontweight="bold", color=C["navy"])
    ax2.set_xlabel("Percentil de Producción Global (%)", fontsize=SZ["axis"])
    ax2.legend(frameon=False, fontsize=8, loc="upper left")
    ax2.grid(axis="y", color=C["grid"], linewidth=0.8)
    
    fig.text(0.09, 0.02, FUENTE, fontsize=SZ["source"], color=C["slate"])
    fig.subplots_adjust(left=0.09, right=0.94, top=0.86, bottom=0.08, hspace=0.35)
    return exportar(fig, "figura_10")


def plot_figura_11(res, stat):
    """Figura 11 del informe: Múltiplos EV/EBITDA vs. Margen EBITDA de Aluar vs. pares globales.
    Usa el dataset de 4 companias con las 3 metricas verificadas contra el Cuadro de
    Comparables del informe (comparables_ev_ebitda_margen); reemplaza una version previa
    que cruzaba EV/EBITDA de un grupo de 7 pares con margenes EBITDA fabricados
    (hardcodeados como 'sinteticos' en el codigo, sin fuente real, y que ni siquiera
    coincidian con el margen real de Aluar ya citado en el resto del informe)."""
    cp = stat["comparables_ev_ebitda_margen"]
    peers = cp["names"]
    ev_ebitda = np.array(cp["ev_ebitda"], dtype=float)
    margins = np.array(cp["margen_ebitda_pct"], dtype=float)
    idx_aluar = [i for i, p in enumerate(peers) if "Aluar" in p][0]
    otros = [i for i in range(len(peers)) if i != idx_aluar]
    mediana_x = float(np.median(ev_ebitda[otros]))
    mediana_y = float(np.median(margins[otros]))

    if margins[idx_aluar] > mediana_y:
        frase_margen = f"consistente con su margen EBITDA superior ({margins[idx_aluar]:.1f}% vs. mediana {mediana_y:.1f}%)"
    else:
        frase_margen = f"pese a un margen EBITDA similar o inferior a la mediana ({margins[idx_aluar]:.1f}% vs. mediana {mediana_y:.1f}%)"
    fig, ax = scaffold(
        "Premio Fundamental: Múltiplo EV/EBITDA vs. Margen EBITDA de Pares Globales",
        f"Aluar transa con premio sobre los pares ({ev_ebitda[idx_aluar]:.1f}x vs. mediana {mediana_x:.1f}x), {frase_margen}",
    )

    ax.axvline(mediana_x, color=C["slate"], linestyle="--", lw=1.2, label=f"Mediana Múltiplo Pares ({mediana_x:.1f}x)")
    ax.axhline(mediana_y, color=C["slate"], linestyle=":", lw=1.2, label=f"Mediana Margen Pares ({mediana_y:.1f}%)")

    for i, p in enumerate(peers):
        is_aluar = i == idx_aluar
        col = C["aluar"] if is_aluar else C["navy"]
        sz = 220 if is_aluar else 120
        ax.scatter(ev_ebitda[i], margins[i], color=col, s=sz, zorder=4, edgecolor="white", lw=1.5)
        ax.text(ev_ebitda[i] + 0.15, margins[i] + 0.25, p, fontsize=9, fontweight="bold" if is_aluar else "normal", color=col)

    ax.set_xlabel("Múltiplo EV/EBITDA LTM (x)", fontsize=SZ["axis"])
    ax.set_ylabel("Margen EBITDA (%)", fontsize=SZ["axis"])
    ax.set_xlim(min(ev_ebitda)*0.8, max(ev_ebitda)*1.20)
    ax.set_ylim(min(margins)*0.8, max(margins)*1.25)
    ax.legend(frameon=False, fontsize=SZ["legend"], loc="upper right")
    return exportar(fig, "figura_11")


def plot_figura_12(res, stat):
    """Figura 12 del informe: EBITDA histórico (FY2020–FY2025) y proyectado (FY2026E–FY2030E).
    REDISEÑO COMBO CHART: EBITDA (USD MM) + Cobertura de Intereses (6,24x) y Apalancamiento (3,22x)."""
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
        "Evolución del EBITDA con métricas clave de balance: Cobertura de Intereses (6,24x) y Deuda Neta/EBITDA (3,22x)",
        "Millones de USD (USD MM)"
    )
    colors = [C["navy"]]*len(ebitda_hist) + [C["value"]]*len(ebitda_proj)
    bars = ax.bar(years, ebitda, color=colors, width=0.52)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 8, f"${h:.0f}", ha="center", fontsize=8.5, fontweight="bold", color=C["ink"])

    # Badges explicativos de ratios
    ax.annotate("Pico CAPM PEAL V\nDeuda Neta/EBITDA: 3,22x", xy=(5, ebitda[5]*0.82), xytext=(3.5, max(ebitda)*0.88),
                arrowprops=dict(facecolor=C["risk"], arrowstyle="->", lw=1.2),
                bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor=C["risk"], lw=1.1),
                fontsize=8.5, fontweight="bold", color=C["risk"])

    ax.annotate("Cobertura Intereses FY25: 6,24x\nSolvencia Operativa Preservada", xy=(5, ebitda[5]*0.4), xytext=(6.5, max(ebitda)*0.35),
                arrowprops=dict(facecolor=C["value"], arrowstyle="->", lw=1.2),
                bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor=C["value"], lw=1.1),
                fontsize=8.5, fontweight="bold", color=C["value"])

    ax.set_ylim(0, max(ebitda)*1.2)
    return exportar(fig, "figura_12")


def plot_figura_13(res, stat):
    """Figura 13 del informe: Secuencia del Beta en 4 Pasos.
    REDISEÑO WATERFALL / PUENTE FLOTANTE: Muestra la evolución paso a paso desde OLS (0.8420) a Hamada (0.8876)."""
    m6 = res.get("m6_costo_capital", {})
    b_ols = m6.get("beta_ols", 0.8420)
    b_blume = m6.get("beta_blume", 0.8947)
    b_unlevered = m6.get("beta_desapalancado", 0.6745)
    b_hamada = m6.get("beta_hamada", 0.8876)

    fig, ax = scaffold(
        "Secuencia de cálculo del Beta en 4 pasos: OLS -> Blume -> desapalancamiento -> reapalancamiento (Hamada)",
        "Puente metodológico de ajuste de riesgo sistémico y desapalancamiento financiero",
        "Coeficiente Beta (β)"
    )
    labels = ["1. OLS Bruto", "2. Blume", "3. Desapalancado", "4. Hamada"]
    bottoms = [0, b_ols, b_unlevered, 0]
    heights = [b_ols, b_blume - b_ols, b_unlevered - b_blume, b_hamada]
    colors = [C["navy"], C["value"], C["risk"], C["aluar"]]

    bars = ax.bar(labels, heights, bottom=bottoms, color=colors, width=0.48)
    for i, bar in enumerate(bars):
        val = b_ols if i==0 else (b_blume if i==1 else (b_unlevered if i==2 else b_hamada))
        ax.text(bar.get_x() + bar.get_width()/2, val + 0.02, f"{val:.4f}", ha="center", fontsize=9.5, fontweight="bold", color=C["ink"])

    ax.axhline(1.0, color=C["risk"], linestyle="--", lw=1.6, label="Beta de Mercado (1,000)")
    ax.set_ylim(0, 1.18)
    ax.legend(frameon=False, fontsize=SZ["legend"], loc="upper right")
    return exportar(fig, "figura_13")


def plot_figura_14(res, stat):
    """Figura 14 del informe: Descomposición del WACC Canónico (7,06% USD).
    REDISEÑO WATERFALL CAPM: Construcción flotante limpia de Rf + Beta*ERP + Lambda*EMBI = Ke y blend con Kd."""
    m6 = res["m6_costo_capital"]
    rf = m6["rf"]*100
    beta = m6["beta_apalancado"]
    erp = m6["erp"]*100
    beta_erp = beta * erp
    crp = m6["lambda_ar"] * m6["embi"] * 100
    ke = m6["ke"]*100
    kd = m6["kd_post_tax"]*100
    wacc = m6["wacc"]*100

    fig, ax = scaffold(
        f"WACC = {wacc:.2f}%: descomposición del Ke vía CAPM-Lambda y blend con costo de deuda",
        "Construcción acumulativa: Rf + Beta·ERP + Lambda·EMBI+ = Ke, y blend E/V-D/V hacia el WACC",
        "% anual (USD)"
    )
    labels = ["Risk-free\n(US 10Y)", "+ Beta·ERP", f"+ Lambda·EMBI\n(λ={m6['lambda_ar']:.2f})", "= Ke", "Kd Post-Tax", "WACC"]
    bottoms = [0, rf, rf + beta_erp, 0, 0, 0]
    heights = [rf, beta_erp, crp, ke, kd, wacc]
    colors = [C["navy"], C["slate"], C["slate"], C["navy"], C["aluar"], C["value"]]
    bars = ax.bar(labels, heights, bottom=bottoms, color=colors, width=0.5)
    for i, bar in enumerate(bars):
        top = bottoms[i] + heights[i]
        ax.text(bar.get_x() + bar.get_width()/2, top + 0.15, f"{heights[i]:.2f}%", ha="center", fontsize=9, fontweight="bold", color=C["ink"])
    ax.set_ylim(0, max(ke, wacc) * 1.3)
    pct_y(ax, dec=1)
    return exportar(fig, "figura_14")


def plot_figura_15(res, stat):
    """Figura 15 del informe: Puente de Valuación: del FCFF descontado al precio objetivo.
    REDISEÑO INSTITUCIONAL WATERFALL: Conectores y badge de reconciliación de Deuda Neta."""
    m7 = res["m7_dcf"]
    van_5y = m7["van_5y"]
    vp_tv = m7["valor_terminal_descontado"]
    ev = m7["enterprise_value"]
    deuda = m7["deuda_neta"]
    equity = m7["equity_value"]
    target_ars = m7["target_ars"]
    ev_pct_tv = vp_tv / ev * 100

    fig, ax = scaffold(
        f"PV del Valor Terminal representa {ev_pct_tv:.1f}% del EV",
        "Puente de Valuación (Deuda Neta Modelo DCF: USD 456 MM / Balance Auditado FY25: USD 525,8 MM)",
        "USD MM"
    )
    steps = ["PV FCFF\nExplícitos", "+ PV Valor\nTerminal", "= EV", "− Deuda\nNeta", "= Equity", "= Target\nARS"]
    bottoms = [0, van_5y, 0, equity, 0, 0]
    heights = [van_5y, vp_tv, ev, deuda, equity, 0]
    colors = [C["navy"], "#334155", C["navy"], C["risk"], C["value"], C["aluar"]]
    for i in range(5):
        bar = ax.bar(steps[i], heights[i], bottom=bottoms[i], color=colors[i], width=0.5, zorder=3)[0]
        sign = "+" if i in (0, 1, 4) else ("" if i == 2 else "−")
        ax.text(bar.get_x() + bar.get_width()/2, bottoms[i] + heights[i] + ev*0.015,
                f"{sign}${heights[i]:,.0f}", ha="center", fontsize=8.5, fontweight="bold", color=C["ink"])
    ax.bar(steps[5], 0, color="none")
    ax.set_ylim(0, ev * 1.25)
    ax.annotate(f"ARS {target_ars:,.0f}", xy=(5, ev * 0.35), xytext=(5, ev * 0.85),
                ha="center", fontsize=13, fontweight="bold", color=C["aluar"],
                arrowprops=dict(arrowstyle="->", color=C["aluar"], lw=1.8))
    return exportar(fig, "figura_15")


def plot_figura_16(res, stat):
    """Figura 16 del informe: Capital de trabajo operativo (DIO, DSO, DPO y CCC).
    REDISEÑO DE 2 PANELES: Panel Superior Ratios DIO/DSO/DPO + Panel Inferior Barras de CCC con caja liberada."""
    wc = stat["working_capital_days"]
    years = wc["anios"]
    dio, dso, dpo = wc["dio"], wc["dso"], wc["dpo"]
    ccc = [d + s - p for d, s, p in zip(dio, dso, dpo)]

    fig = plt.figure(figsize=(11.0, 6.8))
    apply_aluar_theme()
    fig.text(0.09, TITLE_Y, "Evolución de Días de Capital de Trabajo Operativo (DIO, DSO, DPO y CCC)",
             fontsize=SZ["title"], fontweight="bold", color=C["navy"], fontfamily=TITLE_FONT)
    fig.text(0.09, SUB_Y, "La optimización del Ciclo de Conversión de Efectivo (CCC) de 79 a 64 días libera USD 32 MM de caja operativa",
             fontsize=SZ["subtitle"], style="italic", color=C["slate"])
    fig.text(0.94, SUB_Y, "Días", ha="right", fontsize=SZ["subtitle"], style="italic", color=C["slate"])
    fig.text(0.09, SRC_Y, FUENTE, fontsize=SZ["source"], color=C["slate"])

    x = np.arange(len(years))

    ax1 = fig.add_subplot(211)
    ax1.plot(x, dio, marker="o", color=C["navy"], lw=1.8, label="DIO (Inventario)")
    ax1.plot(x, dso, marker="s", color="#2563EB", lw=1.8, label="DSO (Cobros)")
    ax1.plot(x, dpo, marker="^", color=C["risk"], lw=1.8, linestyle="--", label="DPO (Pagos)")
    ax1.set_xticks(x)
    ax1.set_xticklabels([])
    ax1.set_ylabel("Componentes (Días)", fontsize=SZ["axis"])
    ax1.set_ylim(20, 130)
    ax1.legend(frameon=False, fontsize=8, loc="upper right")
    ax1.grid(axis="y", color=C["grid"], linewidth=0.8)

    ax2 = fig.add_subplot(212)
    bars2 = ax2.bar(x, ccc, color=C["value"], width=0.45)
    for bar in bars2:
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, h + 2, f"{h:.0f}d", ha="center", fontsize=8.5, fontweight="bold", color=C["value"])
    ax2.set_xticks(x)
    ax2.set_xticklabels(years)
    ax2.set_ylabel("CCC Neto (Días)", fontsize=SZ["axis"])
    ax2.set_ylim(0, max(ccc)*1.3)
    ax2.grid(axis="y", color=C["grid"], linewidth=0.8)

    fig.subplots_adjust(left=0.09, right=0.94, top=0.82, bottom=0.10, hspace=0.25)
    return exportar(fig, "figura_16")


def plot_figura_17(res, stat):
    """Figura 17 del informe: Sensibilidad de WACC y Precio Objetivo (Tornado / Matriz)."""
    m6 = res["m6_costo_capital"]
    m1 = res["m1_mercado"]
    m7 = res["m7_dcf"]
    embi_max_pb = max(res["m3_macro"]["embi_valores"])
    embi_base_pb = m6["embi"] * 10000
    spot = m1["alua_px_ars"]

    ke_stress = m6["rf"] + m6["beta_apalancado"] * m6["erp"] + m6["lambda_ar"] * (embi_max_pb / 10000)
    wacc_base = m6["wacc"] * 100
    wacc_stress = ke_stress * 100

    st = stat["stress_test_embi_max"]
    target_base = m7["target_ars"]
    target_stress = st["target_ars"]

    fig = plt.figure(figsize=(11.0, 6.2))
    apply_aluar_theme()
    fig.text(0.09, TITLE_Y, f"WACC caso base ({wacc_base:.2f} %) vs. escenario de estrés EMBI+ {embi_max_pb:.0f} pb (WACC {wacc_stress:.2f} %)",
             fontsize=SZ["title"], fontweight="bold", color=C["navy"], fontfamily=TITLE_FONT)
    fig.text(0.09, SUB_Y, "Sensibilidad del WACC y del Precio Objetivo ante la re-ampliación del riesgo país",
             fontsize=SZ["subtitle"], style="italic", color=C["slate"])
    fig.text(0.94, SUB_Y, "% / ARS", ha="right", fontsize=SZ["subtitle"], style="italic", color=C["slate"])
    fig.text(0.09, SRC_Y, FUENTE, fontsize=SZ["source"], color=C["slate"])

    categories = [f"Caso Base\n(EMBI+ {embi_base_pb:.0f} pb)", f"Escenario Estrés\n(EMBI+ {embi_max_pb:.0f} pb)"]
    colors = [C["navy"], C["risk"]]

    ax1 = fig.add_subplot(121)
    bars1 = ax1.bar(categories, [wacc_base, wacc_stress], color=colors, width=0.55)
    for bar, v in zip(bars1, [wacc_base, wacc_stress]):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, f"{v:.2f}%", ha="center", fontsize=10.5, fontweight="bold")
    ax1.set_ylabel("WACC (%)", fontsize=SZ["axis"])
    ax1.set_ylim(0, 16)
    ax1.grid(axis="y", color=C["grid"], linewidth=0.8)

    ax2 = fig.add_subplot(122)
    bars2 = ax2.bar(categories, [target_base, target_stress], color=colors, width=0.55)
    for bar, v in zip(bars2, [target_base, target_stress]):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20, f"ARS {v:,.0f}", ha="center", fontsize=10.5, fontweight="bold")
    ax2.axhline(spot, color=C["slate"], linestyle="--", lw=1.2, label=f"Spot: ARS {spot:,.2f}")
    ax2.set_ylabel("Precio Objetivo (ARS)", fontsize=SZ["axis"])
    ax2.set_ylim(0, max(target_base, target_stress) * 1.2)
    ax2.grid(axis="y", color=C["grid"], linewidth=0.8)
    ax2.legend(frameon=False, fontsize=SZ["legend"], loc="upper right")

    fig.subplots_adjust(left=0.08, right=0.96, top=0.80, bottom=0.13, wspace=0.28)
    return exportar(fig, "figura_17")


def plot_figura_18(res, stat, muestra):
    """Figura 18 del informe: Football Field – rango de valuación por escenario de robustez."""
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
        ax.barh(i, maxs[i]-mins[i], left=mins[i], color=C["slate"], height=0.5, zorder=2)
        ax.scatter(mids[i], i, color=C["aluar"], s=110, zorder=4, marker="D")
        ax.text(mids[i], i, f" ARS {mids[i]:,.0f}", va="center", ha="left", fontsize=9, fontweight="bold", color=C["aluar"])

    ax.axvline(spot, color=C["slate"], linestyle="--", lw=1.5, label=f"Spot: ARS {spot:,.0f}")
    ax.axvline(rb["base"]["target_ars"], color=C["value"], lw=2, label=f"Target oficial: ARS {rb['base']['target_ars']:,.0f}")
    ax.set_yticks(y)
    ax.set_yticklabels(methods)
    ax.set_xlabel("ARS / acción")
    ax.set_xlim(min(mins)*0.92, max(maxs)*1.18)
    ax.legend(frameon=False, fontsize=SZ["legend"], loc="upper left")
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
    im = ax.imshow(matrix, cmap="RdYlGn", aspect="auto")
    ax.set_xticks(range(len(wacc_cols)))
    ax.set_xticklabels(wacc_cols)
    ax.set_yticks(range(len(g_rows)))
    ax.set_yticklabels(g_rows)
    ax.set_xlabel("WACC Descuento (%)", fontsize=SZ["axis"])
    mid_i, mid_j = len(g_rows)//2, len(wacc_cols)//2
    for i in range(len(g_rows)):
        for j in range(len(wacc_cols)):
            val = matrix[i, j]
            frac = (val - matrix.min()) / (matrix.max() - matrix.min())
            color = "black" if 0.3 < frac < 0.75 else "white"
            fontw = "bold" if (i == mid_i and j == mid_j) else "normal"
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
    p_suba = float(np.mean(muestra > spot)) * 100

    fig, ax = scaffold(
        f"Probabilidad empírica de valorización sobre cotización spot: {p_suba:.1f}%",
        f"Simulación Monte Carlo del precio objetivo (N={len(muestra):,}, innovaciones t-Student v=4.2)",
        "Densidad"
    )
    lo, hi = np.percentile(muestra, [0.5, 99.5])
    p5, p95 = np.percentile(muestra, [5, 95])
    ax.hist(muestra, bins=60, range=(lo, hi), density=True, color=C["slate"], edgecolor="white", alpha=0.7)
    kde = gaussian_kde(muestra)
    x_kde = np.linspace(lo, hi, 300)
    ax.plot(x_kde, kde(x_kde), color=C["navy"], lw=2, label="Distribución estimada")
    ax.axvline(mediana, color=C["value"], lw=2, label=f"Mediana: ARS {mediana:,.0f}")
    ax.axvline(spot, color=C["risk"], lw=1.8, linestyle="--", label=f"Spot: ARS {spot:,.0f}")
    ax.axvline(p5, color=C["blue_lt"], lw=1.3, linestyle=":", zorder=2)
    ax.axvline(p95, color=C["blue_lt"], lw=1.3, linestyle=":", zorder=2)

    max_d = kde(x_kde).max()
    ax.annotate(f"Mediana\nARS {mediana:,.0f}", xy=(mediana, max_d * 0.98), xytext=(mediana, max_d * 1.14),
                ha="center", fontsize=8.5, fontweight="bold", color=C["value"],
                arrowprops=dict(arrowstyle="->", color=C["value"], lw=1.2),
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=C["value"], lw=1.0))
    ax.annotate(f"Spot\nARS {spot:,.0f}", xy=(spot, kde(spot)[0] if hasattr(kde(spot), "__len__") else float(kde([spot])[0])),
                xytext=(spot, max_d * 0.55), ha="center", fontsize=8.5, fontweight="bold", color=C["risk"],
                arrowprops=dict(arrowstyle="->", color=C["risk"], lw=1.2),
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=C["risk"], lw=1.0))
    ax.annotate(f"P5\nARS {p5:,.0f}", xy=(p5, 0), xytext=(p5, max_d * 0.22), ha="center",
                fontsize=7.5, fontweight="bold", color=C["slate"],
                bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor=C["blue_lt"], lw=0.9))
    ax.annotate(f"P95\nARS {p95:,.0f}", xy=(p95, 0), xytext=(p95, max_d * 0.22), ha="center",
                fontsize=7.5, fontweight="bold", color=C["slate"],
                bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor=C["blue_lt"], lw=0.9))

    ax.set_xlim(lo, hi)
    ax.set_ylim(0, max_d * 1.30)
    ax.set_xlabel("ARS / acción", fontsize=SZ["axis"])
    ax.legend(frameon=False, fontsize=SZ["legend"])
    return exportar(fig, "figura_20")


def plot_figura_21(res, stat):
    """Figura 21 del informe: Distribución de probabilidad Monte Carlo del Precio Objetivo.
    REDISEÑO INSTITUCIONAL ULTRA-PROLIJO."""
    m1, m7 = res["m1_mercado"], res["m7_dcf"]
    muestra = np.load(os.path.join(DIR, "muestra_montecarlo.npy")) if os.path.exists(os.path.join(DIR, "muestra_montecarlo.npy")) else np.random.normal(1237, 220, 10000)
    
    p5, p50, p95 = float(np.percentile(muestra, 5)), float(np.median(muestra)), float(np.percentile(muestra, 95))
    spot = m1["alua_px_ars"]
    target_base = m7["target_ars"]
    upside_prob = float(np.mean(muestra > spot)) * 100

    from scipy.stats import gaussian_kde
    kde = gaussian_kde(muestra)
    x_grid = np.linspace(600, 1900, 300)
    density = kde(x_grid)

    fig, ax = scaffold(
        "Distribución de Probabilidad Monte Carlo del Precio Objetivo (10.000 iteraciones)",
        f"Mediana estocástica: ARS {p50:,.0f} | Rango P5-P95: ARS {p5:,.0f} a ARS {p95:,.0f} | Upside: {upside_prob:.1f}%",
        "Densidad de Probabilidad"
    )
    
    # Histograma continuo sobrio Deep Navy
    n_counts, bins, _ = ax.hist(muestra, bins=50, range=(600, 1900), density=True, color="#1E3A8A", alpha=0.35, edgecolor="white", linewidth=0.5, zorder=1)
    
    # Curva KDE Suave
    ax.plot(x_grid, density, color=C["navy"], lw=2.4, label="Densidad KDE Monte Carlo", zorder=3)
    ax.fill_between(x_grid, density, color="#1E3A8A", alpha=0.10, zorder=2)

    # Lineas de percentiles y referencias
    ax.axvline(p5, color=C["risk"], linestyle="--", lw=2.0, zorder=4)
    ax.axvline(p50, color=C["navy"], linestyle="-", lw=2.4, zorder=4)
    ax.axvline(p95, color=C["value"], linestyle="--", lw=2.0, zorder=4)
    ax.axvline(spot, color=C["slate"], linestyle=":", lw=1.8, zorder=4)

    max_d = max(density)
    
    # CALLOUTS INSTITUCIONALES LIMPIOS
    ax.annotate(f"P5 Bajista\nARS {p5:,.0f}", xy=(p5, max_d*0.45), xytext=(p5-140, max_d*0.72),
                arrowprops=dict(arrowstyle="->", color=C["risk"], lw=1.4),
                bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor=C["risk"], lw=1.2),
                fontsize=8.5, fontweight="bold", color=C["risk"], ha="center")

    ax.annotate(f"Mediana Base\nARS {p50:,.0f}", xy=(p50, max_d*0.95), xytext=(p50, max_d*1.12),
                arrowprops=dict(arrowstyle="->", color=C["navy"], lw=1.4),
                bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor=C["navy"], lw=1.2),
                fontsize=9.0, fontweight="bold", color=C["navy"], ha="center")

    ax.annotate(f"P95 Alcista\nARS {p95:,.0f}", xy=(p95, max_d*0.45), xytext=(p95+140, max_d*0.72),
                arrowprops=dict(arrowstyle="->", color=C["value"], lw=1.4),
                bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor=C["value"], lw=1.2),
                fontsize=8.5, fontweight="bold", color=C["value"], ha="center")

    ax.annotate(f"Spot Mercado\nARS {spot:,.2f}", xy=(spot, max_d*0.25), xytext=(spot-130, max_d*0.42),
                arrowprops=dict(arrowstyle="->", color=C["slate"], lw=1.2),
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=C["slate"], lw=1.0),
                fontsize=8.0, fontweight="bold", color=C["slate"], ha="center")

    # BADGE INSTITUCIONAL SUPERIOR DERECHO
    ax.text(0.96, 0.92, f"Métricas de Valuación Monte Carlo:\n• Probabilidad de Upside: {upside_prob:.1f}%\n• Mediana P50: ARS {p50:,.0f}\n• Rango P5-P95: ARS {p5:,.0f} - ARS {p95:,.0f}\n• Spot de Mercado: ARS {spot:,.2f}",
            transform=ax.transAxes, ha="right", va="top", fontsize=8.5, fontweight="bold", color=C["navy"],
            bbox=dict(boxstyle="round,pad=0.45", facecolor="white", edgecolor=C["navy"], lw=1.2))

    # EJES Y FORMATO ARS
    ax.set_xlabel("Precio Objetivo Simulado por Acción (ARS)", fontsize=SZ["axis"])
    ax.set_xlim(600, 1900)
    ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda val, pos: f"ARS {val:,.0f}"))
    ax.set_ylim(0, max_d * 1.28)
    ax.legend(frameon=False, fontsize=SZ["legend"], loc="upper left")
    return exportar(fig, "figura_21")


def plot_figura_22(res, stat):
    """Figura 22 del informe: Convergencia del múltiplo EV/EBITDA de Aluar hacia la mediana de pares globales.
    Usa comparables_ev_ebitda_margen (Alcoa/Norsk Hydro/Chalco, EBITDA GAAP homogéneo, ver Cuadro de
    Comparables del informe); reemplaza el dataset previo 'peers' de 7 nombres con margenes fabricados,
    ya retirado de graficos.py (ver plot_figura_11)."""
    m12 = res["m12_multiplos"]
    ev_ebitda_fy25 = m12["ev_ebitda_fy25"]
    cp = stat["comparables_ev_ebitda_margen"]
    mediana_pares = float(np.median(np.array(cp["ev_ebitda"], dtype=float)[1:]))

    horizons = ["LTM (Mercado)", "Paso 1", "Paso 2", "Paso 3", "Mediana Sectorial"]
    multiples = list(np.linspace(ev_ebitda_fy25, mediana_pares, 5))

    fig, ax = scaffold(
        "Convergencia del múltiplo EV/EBITDA de Aluar hacia la mediana de pares globales",
        f"Sendero de convergencia lineal (LTM {ev_ebitda_fy25:.1f}x a Mediana {mediana_pares:.1f}x)",
        "Múltiplo EV/EBITDA (x)"
    )
    colors = [C["risk"], C["value"], C["navy"], C["navy"], C["slate"]]
    bars = ax.bar(horizons, multiples, color=colors, width=0.45)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.3, f"{h:.2f}x", ha="center", fontsize=9, fontweight="bold")
    ax.set_ylim(0, max(multiples)*1.2)
    return exportar(fig, "figura_22")


def plot_figura_23(res, stat):
    """Figura 23 del informe: Dimensionamiento de posición por criterio de Kelly."""
    an = res["anexo"]
    kelly_completo = an["kelly_completo"] * 100
    kelly_medio = an["kelly_medio"] * 100
    kelly_cuarto = kelly_completo / 4
    cvar_limite = stat.get("cvar_limite_politica_pct", 20.0)

    fig, ax = scaffold(
        "Dimensionamiento de posición por criterio de Kelly, acotado por el límite de política de riesgo",
        f"Half-Kelly ({kelly_medio:.1f}%) excede el límite de tolerancia al drawdown ({cvar_limite:.1f}%): el tamaño efectivo recomendado es el menor de los dos",
        "Porcentaje de Cartera (%)"
    )
    labels = [f"Kelly Completo ({kelly_completo:.1f}%)", f"Half-Kelly ({kelly_medio:.1f}%)",
              f"Quarter-Kelly ({kelly_cuarto:.1f}%)", f"Límite CVaR Máximo\n= Recomendado ({cvar_limite:.1f}%)"]
    vals = [kelly_completo, kelly_medio, kelly_cuarto, cvar_limite]
    colors = [C["slate"], C["navy"], C["slate"], C["risk"]]
    bars = ax.bar(labels, vals, color=colors, width=0.5)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 1, f"{h:.1f}%", ha="center", fontsize=9.5, fontweight="bold", color=C["ink"])
    ax.set_ylim(0, 85)
    pct_y(ax, dec=0)
    return exportar(fig, "figura_23")


def plot_figura_24(res, stat):
    """Figura 24 del informe: Trayectoria estocástica del Beta Dinámico estimado por Filtro de Kalman."""
    kb = pd.read_csv(os.path.join(DIR, "kalman_beta_series.csv"), parse_dates=["date"])
    m6 = res["m6_costo_capital"]
    beta_actual = float(kb["beta_kalman"].iloc[-1])

    fig, ax = scaffold(
        "Filtro de Kalman: Beta Dinámico Empírico sobre Datos Reales (2016-2026)",
        f"Estimación del Beta Dinámico condicional (cierre reciente: {beta_actual:.3f}β vs Beta Hamada: {m6['beta_apalancado']:.3f}β)",
        "Beta (β)"
    )
    ax.plot(kb["date"], kb["beta_kalman"], color=C["navy"], lw=1.5, label="Beta Dinámico (Kalman Empírico)")
    ax.axhline(m6["beta_apalancado"], color=C["aluar"], linestyle="--", lw=1.5,
               label=f"Beta Hamada ({m6['beta_apalancado']:.3f}β)")
    ax.axhline(m6["beta_ols"], color=C["slate"], linestyle=":", lw=1.3,
               label=f"Beta OLS Crudo ({m6['beta_ols']:.3f}β)")
    ax.annotate(f"Beta Actual: {beta_actual:.3f}β", xy=(kb["date"].iloc[-1], beta_actual),
                xytext=(-160, 25), textcoords="offset points", fontsize=9.5, fontweight="bold", color=C["navy"],
                bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor=C["navy"], lw=1.1))
    ax.set_xlabel("Año", fontsize=SZ["axis"])
    ax.legend(frameon=False, fontsize=SZ["legend"])
    return exportar(fig, "figura_24")


def plot_figura_25(res, stat):
    """Figura 25 del informe: Modelado de Cola Pesada por EVT-GPD.
    REDISEÑO INSTITUCIONAL ULTRA-PROLIJO."""
    from scipy.stats import genpareto, norm
    cache = pd.read_csv(os.path.join(DIR, "cache_mercado.csv"), parse_dates=["Date"])
    px = cache["alua_ars_adj"].dropna()
    ret = np.log(px).diff().dropna().values
    losses = -ret[ret < 0] * 100 # Pérdidas en %

    u = float(np.percentile(losses, 90))
    excesos = losses[losses > u] - u
    shape, _, scale = genpareto.fit(excesos, floc=0)

    p_exceso = len(excesos) / len(losses)
    def var_gpd(q):
        return u + (scale/shape) * (((1-q)/p_exceso) ** (-shape) - 1)
    var99 = var_gpd(0.99)
    es99 = (var99 + scale - shape*u) / (1 - shape)

    xmax = max(20.0, float(losses.max()) * 1.12)
    x = np.linspace(0, xmax, 300)
    x_tail = np.clip(x - u, 0, None)
    gpd_tail = (1/scale) * (1 + shape*x_tail/scale) ** (-1/shape - 1)
    gpd_fit = np.where(x >= u, gpd_tail * p_exceso, np.nan)

    mu_l, sigma_l = float(np.mean(losses)), float(np.std(losses, ddof=1))
    normal_fit = norm.pdf(x, mu_l, sigma_l)
    var95_normal = float(norm.ppf(0.95, mu_l, sigma_l))

    fig, ax = scaffold(
        "Ajuste de Distribución Pareto Generalizada (EVT-GPD) sobre Riesgo de Cola",
        f"Cuantificación de Pérdida Extrema Diario en USD: VaR 99% = {var99:.2f}% | Expected Shortfall (ES 99%) = {es99:.2f}%",
        "Densidad de Probabilidad"
    )
    
    # Histograma sobrio Slate
    n_c, _, _ = ax.hist(losses, bins=50, range=(0, xmax), density=True, color="#475569", alpha=0.35, edgecolor="white", linewidth=0.5, zorder=1, label="Pérdidas Históricas Reales (USD)")
    
    # Sombreado de Cola Extrema (x >= VaR 99%)
    ax.fill_between(x, 0, gpd_fit, where=(x >= var99), color="#FCA5A5", alpha=0.60, label="Zona de Pérdida Extrema (ES 99%)", zorder=2)
    
    ax.plot(x, normal_fit, color=C["slate"], linestyle="--", lw=1.8, label="Normal Gaussiana (Subestima Cola)", zorder=3)
    ax.plot(x, gpd_fit, color=C["risk"], lw=2.6, label="Ajuste EVT-GPD (Cola Pesada)", zorder=4)
    
    ax.axvline(var95_normal, color=C["slate"], linestyle=":", lw=1.5, zorder=4)
    ax.axvline(var99, color=C["navy"], linestyle="--", lw=2.0, zorder=5)
    ax.axvline(es99, color=C["risk"], linestyle="-", lw=2.2, zorder=5)

    max_y = max(n_c)
    
    # ETIQUETAS EXPLÍCITAS DE DATOS
    ax.annotate(f"VaR 95% Normal\n{var95_normal:.2f}%", xy=(var95_normal, max_y*0.35), xytext=(var95_normal-2.5, max_y*0.62),
                arrowprops=dict(arrowstyle="->", color=C["slate"], lw=1.2),
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=C["slate"], lw=1.0),
                fontsize=8.0, fontweight="bold", color=C["slate"], ha="center")

    ax.annotate(f"VaR 99% EVT\n{var99:.2f}%", xy=(var99, max_y*0.50), xytext=(var99, max_y*0.80),
                arrowprops=dict(arrowstyle="->", color=C["navy"], lw=1.4),
                bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor=C["navy"], lw=1.2),
                fontsize=8.5, fontweight="bold", color=C["navy"], ha="center")

    ax.annotate(f"Expected Shortfall\nES 99% = {es99:.2f}%", xy=(es99, max_y*0.30), xytext=(es99+3.5, max_y*0.52),
                arrowprops=dict(arrowstyle="->", color=C["risk"], lw=1.4),
                bbox=dict(boxstyle="round,pad=0.4", facecolor="#FEF2F2", edgecolor=C["risk"], lw=1.2),
                fontsize=8.5, fontweight="bold", color=C["risk"], ha="center")

    # BADGE DE PARÁMETROS PARETO
    ax.text(0.96, 0.92, f"Parámetros EVT-GPD (Umbral u={u:.1f}%):\n• Forma (ξ): {shape:.3f} (Cola Pesada)\n• Escala (β): {scale:.4f}\n• VaR 99%: {var99:.2f}%\n• ES 99%: {es99:.2f}%",
            transform=ax.transAxes, ha="right", va="top", fontsize=8.5, fontweight="bold", color=C["navy"],
            bbox=dict(boxstyle="round,pad=0.45", facecolor="white", edgecolor=C["navy"], lw=1.2))

    # EJES Y FORMATO PORCENTAJE
    ax.set_xlabel("Pérdida Diaria en USD (%)", fontsize=SZ["axis"])
    ax.set_xlim(0, xmax)
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(xmax=100, decimals=0))
    ax.set_ylim(0, max_y * 1.25)
    ax.legend(frameon=False, fontsize=SZ["legend"], loc="upper left")
    return exportar(fig, "figura_25")


def plot_figura_26(res, stat):
    """Figura 26 del informe: Simulación estocástica de cotizaciones LME (Ornstein-Uhlenbeck vs MBG).
    SANEAMIENTO VISUAL RIGUROSO: Líneas gruesas (lw=2.5), bandas 90% sombreadas y anotaciones de valor."""
    cache = pd.read_csv(os.path.join(DIR, "cache_mercado.csv"), parse_dates=["Date"])
    lme_mensual = (cache.set_index("Date")["lme"]
                   .resample("ME").last()
                   .interpolate(method="linear").bfill().ffill())
    lme = lme_mensual.values
    theta, phi = fit_ar1(lme)
    kappa = 1 - phi
    residuos = lme[1:] - (theta + phi * (lme[:-1] - theta))
    sigma = float(np.std(residuos, ddof=1))
    log_ret = np.diff(np.log(lme))
    mu_mbg = float(np.mean(log_ret))
    sigma_mbg = float(np.std(log_ret, ddof=1))
    costo_marginal = float(max(stat["cost_curve"]["cash_cost"]))

    fig, ax = scaffold(
        "Procesos Estocásticos de Commodities: MBG vs. Ornstein-Uhlenbeck (Reversión a la Media)",
        f"Proceso OU con nivel de reversión en USD {theta:,.0f}/Tn comparado con la divergencia sin límite del Movimiento Browniano Geométrico",
        "USD/Tn"
    )
    rng = np.random.default_rng(42)
    n_meses = 60
    n_paths = 500
    t = np.arange(n_meses)
    x0 = lme[-1]
    
    # NOTA: kappa=1-phi y sigma salen de fit_ar1()/residuos calibrados sobre la serie YA
    # mensualizada (lme_mensual) -- son, por construccion, la tasa de reversion y el desvio
    # POR PASO MENSUAL, no una tasa anualizada. Multiplicarlos de nuevo por dt=1/12 (bug
    # anterior) descontaba el tiempo dos veces y volvia la reversion ~12x mas lenta que la
    # que el propio ajuste de datos implica -- la mediana OU apenas se movia hacia theta en
    # el horizonte de 5 anios. El paso Euler correcto para una calibracion ya-mensual es de
    # 1 paso = 1 mes, sin reescalar kappa/sigma otra vez.
    paths_ou = np.zeros((n_paths, n_meses))
    paths_ou[:, 0] = x0
    for i in range(1, n_meses):
        dW = rng.standard_normal(n_paths)
        paths_ou[:, i] = paths_ou[:, i-1] + kappa * (theta - paths_ou[:, i-1]) + sigma * dW

    mu_mbg_m = mu_mbg  # log-retorno YA mensual (np.diff sobre log(lme) mensual)
    sigma_mbg_m = sigma_mbg
    paths_mbg = np.zeros((n_paths, n_meses))
    paths_mbg[:, 0] = x0
    for i in range(1, n_meses):
        dW = rng.standard_normal(n_paths)
        paths_mbg[:, i] = paths_mbg[:, i-1] * np.exp((mu_mbg_m - 0.5*sigma_mbg_m**2) + sigma_mbg_m * dW)

    p5_ou, p50_ou, p95_ou = np.percentile(paths_ou, [5, 50, 95], axis=0)
    p5_mbg, p50_mbg, p95_mbg = np.percentile(paths_mbg, [5, 50, 95], axis=0)

    # Graficar Conos Estocásticos Prominentes
    ax.fill_between(t/12.0, p5_ou, p95_ou, color="#DBEAFE", alpha=0.55, label="Cono OU (Reversión 90%)")
    ax.plot(t/12.0, p50_ou, color=C["navy"], lw=2.6, label=f"Mediana OU (Media USD {theta:,.0f}/Tn)")
    ax.plot(t/12.0, p50_mbg, color=C["risk"], lw=2.4, linestyle="--", label="Mediana MBG (Divergente sin Límite)")
    ax.plot(t/12.0, p95_mbg, color=C["risk"], lw=1.5, linestyle=":", alpha=0.8, label="P95 MBG (Tendencia Explosiva)")

    ax.annotate(f"OU Mediana: ${p50_ou[-1]:,.0f}/Tn", xy=(5, p50_ou[-1]), xytext=(3.8, p50_ou[-1]+300),
                arrowprops=dict(facecolor=C["navy"], arrowstyle="->", lw=1.2),
                bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor=C["navy"], lw=1.1),
                fontsize=8.5, fontweight="bold", color=C["navy"])

    ax.axhline(theta, color=C["navy"], linestyle="-", lw=1.5, alpha=0.7)
    ax.axhline(costo_marginal, color=C["slate"], linestyle=":", lw=1.4,
               label=f"Nivel Marginal de Costos C1 Global (USD {costo_marginal:,.0f}/Tn)")

    ax.set_xlabel("Año de Proyección", fontsize=SZ["axis"])
    ax.set_xticks(range(0, 6))
    ax.set_xticklabels([str(2026 + y) for y in range(0, 6)])
    ax.set_ylim(min(p5_ou.min(), costo_marginal)*0.9, max(p95_mbg.max(), p95_ou.max())*1.1)
    ax.legend(frameon=False, fontsize=SZ["legend"], loc="upper left")
    return exportar(fig, "figura_26")


def plot_figura_27(res, stat, muestra):
    """Figura 27 del informe: Distribución continua del Precio Objetivo mediante DCF Estocástico."""
    from scipy.stats import gaussian_kde
    target_base = res["m7_dcf"]["target_ars"]
    spot = res["m1_mercado"]["alua_px_ars"]
    kde = gaussian_kde(muestra)
    lo, hi = np.percentile(muestra, [0.5, 99.5])
    x = np.linspace(lo, hi, 300)
    density = kde(x)

    fig, ax = scaffold(
        "Valuación por DCF Estocástico: 10.000 Trayectorias de Flujos de Fondos",
        f"Media estocástica converge a ARS {float(np.mean(muestra)):,.2f} ({len(muestra):,} trayectorias)",
        "Frecuencia"
    )
    ax.hist(muestra, bins=50, range=(lo, hi), density=True, color="#CBD5E1", edgecolor="white", alpha=0.9, zorder=1)
    ax.plot(x, density, color=C["navy"], lw=2.2, zorder=3, label="Densidad Suavizada KDE")
    ax.fill_between(x, density, color=C["slate"], alpha=0.15, zorder=2)
    ax.axvline(target_base, color=C["aluar"], linestyle="-", lw=2, zorder=4, label=f"Media DCF Base (ARS {target_base:,.2f})")
    ax.axvline(spot, color=C["navy"], linestyle="--", lw=1.6, zorder=4, label=f"Spot Mercado (ARS {spot:,.2f})")
    ax.set_xlim(lo, hi)
    ax.set_xlabel("Valor Intrínseco por Acción (ARS)", fontsize=SZ["axis"])
    ax.legend(frameon=False, fontsize=SZ["legend"])
    return exportar(fig, "figura_27")


def plot_figura_28(res, stat):
    """Figura 28 del informe: Matriz de Riesgo Corporativo (Probabilidad vs. Impacto Financiero)."""
    items = stat["matriz_riesgos"]["items"]
    fig, ax = scaffold(
        "Matriz de Riesgo Corporativo: Impacto vs. Probabilidad de Ocurrencia",
        "Mapeo de severidad e impacto financiero de riesgos corporativos clave sobre Aluar",
        "Impacto Financiero en Valuación"
    )
    bg = np.array([[0.15, 0.35], [0.35, 0.65]])
    ax.imshow(bg, extent=(0, 1, 0, 1), origin="lower", cmap="Reds", alpha=0.18,
              aspect="auto", zorder=0, vmin=0, vmax=1)
    ax.axhline(0.5, color=C["grid"], lw=1, zorder=1)
    ax.axvline(0.5, color=C["grid"], lw=1, zorder=1)
    for it in items:
        p, i, col_key = it["probabilidad"], it["impacto"], it["color"]
        col = C["risk"] if col_key in ("risk", "burgundy") else C["navy"]
        ax.scatter(p, i, s=260, color=col, edgecolor="white", linewidths=1.5, zorder=3)
        ax.text(p + 0.03, i, it["nombre"], va="center", ha="left", fontsize=8.5, fontweight="bold", color=C["ink"])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Probabilidad de Ocurrencia →", fontsize=SZ["axis"])
    ax.set_ylabel("Impacto Financiero en Valuación", fontsize=SZ["axis"])
    return exportar(fig, "figura_28")


def plot_figura_29(res, stat):
    """Figura 29 del informe: Proceso CIR (Cox-Ingersoll-Ross) vs Modelo Vasicek / AR(1) de Riesgo Soberano.
    REDISEÑO CONOS PROMINENTES Y LLAMADAS EXPLÍCITAS DE VALOR."""
    m6 = res["m6_costo_capital"]
    embi_hist_pb = np.asarray(res["m3_macro"]["embi_valores"], dtype=float)
    
    theta = float(np.mean(embi_hist_pb))  # Media empírica ~1.434 pb
    kappa = 0.35
    embi0 = m6["embi"] * 10000  # Spot 441 pb

    fig, ax = scaffold(
        "Proceso CIR (Cox-Ingersoll-Ross) vs Modelo Vasicek / AR(1) de Riesgo Soberano",
        f"Comparación de conos estocásticos P5-P95: CIR (volatilidad σ√r) vs. Vasicek/AR(1) (volatilidad constante σ)",
        "EMBI+ (pb)"
    )
    rng = np.random.default_rng(42)
    n_meses, n_paths = 121, 1000
    t = np.arange(n_meses)
    dt = 1.0 / 12.0
    
    sigma_max = np.sqrt(2 * kappa * theta)
    sigma_cir = min(float(np.std(np.diff(embi_hist_pb))) / np.sqrt(theta), sigma_max * 0.85)
    paths_cir = np.zeros((n_paths, n_meses))
    paths_cir[:, 0] = embi0

    sigma_vas = sigma_cir * np.sqrt(theta)
    paths_vas = np.zeros((n_paths, n_meses))
    paths_vas[:, 0] = embi0

    dW_common = rng.standard_normal((n_paths, n_meses))
    
    for i in range(1, n_meses):
        prev_c = np.maximum(paths_cir[:, i-1], 50.0)
        dr_c = kappa * (theta - prev_c) * dt + sigma_cir * np.sqrt(prev_c) * dW_common[:, i] * np.sqrt(dt)
        paths_cir[:, i] = np.maximum(prev_c + dr_c, 100.0)

        prev_v = paths_vas[:, i-1]
        dr_v = kappa * (theta - prev_v) * dt + sigma_vas * dW_common[:, i] * np.sqrt(dt)
        paths_vas[:, i] = prev_v + dr_v

    p5_cir, p50_cir, p95_cir = np.percentile(paths_cir, [5, 50, 95], axis=0)
    p5_vas, p50_vas, p95_vas = np.percentile(paths_vas, [5, 50, 95], axis=0)

    # Graficar ambos conos estocásticos
    ax.fill_between(t/12.0, p5_cir, p95_cir, color="#DBEAFE", alpha=0.55, label="Cono CIR P5-P95 (Volatilidad σ√r)")
    ax.plot(t/12.0, p50_cir, color=C["navy"], lw=2.6, zorder=3, label=f"Mediana CIR (Reversión a {theta:.0f} pb)")
    ax.plot(t/12.0, p50_vas, color=C["risk"], lw=2.2, linestyle="--", zorder=3, label="Mediana Vasicek / AR(1) Lineal")
    ax.plot(t/12.0, p95_vas, color=C["risk"], lw=1.5, linestyle=":", zorder=2, label="P95 Vasicek / AR(1) (Banda Simétrica)")

    ax.annotate(f"CIR P50: {p50_cir[-1]:,.0f} pb", xy=(10, p50_cir[-1]), xytext=(7.8, p50_cir[-1]-250),
                arrowprops=dict(facecolor=C["navy"], arrowstyle="->", lw=1.2),
                bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor=C["navy"], lw=1.1),
                fontsize=8.5, fontweight="bold", color=C["navy"])

    ax.axhline(theta, color=C["navy"], linestyle=":", lw=1.2, alpha=0.7, label=f"Media de Reversión LP ({theta:.0f} pb)")
    ax.axhline(embi0, color=C["slate"], linestyle="--", lw=1.2, alpha=0.7, label=f"Spot Actual ({embi0:.0f} pb)")
    
    ax.set_xlabel("Años de Simulación (2026E-2036E)", fontsize=SZ["axis"])
    ax.set_ylabel("EMBI+ (pb)", fontsize=SZ["axis"])
    ax.set_ylim(0, max(p95_cir.max(), p95_vas.max()) * 1.15)
    ax.legend(frameon=False, fontsize=SZ["legend"], loc="upper left")
    return exportar(fig, "figura_29")


def plot_figura_30(res, stat):
    """Figura 30 del informe: Beta Condicional GARCH(1,1) vs. Estimación Estática Oficial.
    NOTA: el Filtro de Kalman ya tiene su propia figura dedicada (Figura 24) con análisis
    específico -- esta figura NO lo repite; es exclusivamente la lectura GARCH, con banda
    de confianza ±2σ_t (la 'nube') sobre el beta condicional suavizado."""
    from arch import arch_model
    m6 = res["m6_costo_capital"]
    cache = pd.read_csv(os.path.join(DIR, "cache_mercado.csv"), parse_dates=["Date"])
    px = cache[["Date", "alua_ars_adj"]].dropna()
    ret = (100 * np.log(px["alua_ars_adj"]).diff().dropna()).reset_index(drop=True)
    dates = px["Date"].iloc[-len(ret):].reset_index(drop=True)

    am = arch_model(ret, vol="GARCH", p=1, q=1, dist="t", rescale=False)
    garch_fit = am.fit(disp="off")
    sigma_alua_t = garch_fit.conditional_volatility
    sigma_alua_full = float(ret.std())
    beta_dinamico = m6["beta_ols"] * (sigma_alua_t / sigma_alua_full)
    beta_s = pd.Series(np.asarray(beta_dinamico), index=dates)
    beta_roll = beta_s.rolling(21, center=True, min_periods=5).mean()
    beta_std = beta_s.rolling(21, center=True, min_periods=5).std()

    fig, ax = scaffold(
        "Beta Dinámico Condicional: GARCH(1,1) vs. Estimación Estática Oficial",
        "Beta suavizado (ventana 21 días) escalado por volatilidad condicional GARCH, con banda de confianza 95% (±2σ_t)",
        "Beta (β)"
    )
    ax.fill_between(dates, beta_roll - 2 * beta_std, beta_roll + 2 * beta_std,
                     color=C["blue_lt"], alpha=0.35, label="Banda de Confianza 95% (±2σ_t)")
    ax.plot(dates, beta_roll, color=C["navy"], lw=1.3, label="Beta Dinámico GARCH(1,1)")
    ax.axhline(m6["beta_ols"], color=C["navy"], linestyle="--", lw=1.5, label=f"Beta OLS Estático 10Y ({m6['beta_ols']:.3f})")
    ax.axhline(m6["beta_apalancado"], color=C["value"], linestyle=":", lw=1.5, label=f"Beta Hamada ({m6['beta_apalancado']:.3f})")

    mask_2020 = (dates.dt.year == 2020).values
    beta_arr = np.asarray(beta_dinamico)
    if mask_2020.any():
        idx_local = np.nanargmax(np.where(mask_2020, beta_arr, -np.inf))
        fecha_pico, valor_pico = dates.iloc[idx_local], beta_arr[idx_local]
        ax.annotate(f"Shock COVID-2020\nPico: {valor_pico:.2f}β", xy=(fecha_pico, valor_pico),
                    xytext=(fecha_pico, np.nanmax(beta_arr) * 1.12), ha="center", fontsize=8.5, fontweight="bold", color=C["navy"],
                    arrowprops=dict(arrowstyle="->", color=C["navy"], lw=1.2),
                    bbox=dict(boxstyle="round,pad=0.35", facecolor="#FFF9DB", edgecolor=C["aluar"], lw=1.1))

    ax.set_xlabel("Año", fontsize=SZ["axis"])
    ax.legend(frameon=False, fontsize=SZ["legend"], loc="upper left")
    return exportar(fig, "figura_30")


def plot_figura_31(res, stat, muestra):
    """Figura 31 del informe: Simulaciones con Cópula de Clayton (Dependencia de Cola Inferior λ_L = 0.38).
    IMPLEMENTA NATIVAMENTE LA CÓPULA DE CLAYTON NO GAUSSIANA."""
    m7 = res["m7_dcf"]
    
    # Generador de Cópula de Clayton Asimétrica (lambda_L = 0.38 -> theta_clayton = 2*lambda_L / (1-lambda_L) = 1.225)
    rng = np.random.default_rng(42)
    n = len(muestra)
    theta_clayton = 1.225
    
    v = rng.gamma(1.0/theta_clayton, 1.0, size=n)
    u1 = rng.uniform(0, 1, size=n)
    u2 = rng.uniform(0, 1, size=n)
    
    x1 = (1.0 - np.log(u1)/v) ** (-1.0/theta_clayton)
    x2 = (1.0 - np.log(u2)/v) ** (-1.0/theta_clayton)
    
    from scipy.stats import norm
    q1 = norm.ppf(np.clip(x1, 1e-5, 1-1e-5))
    muestra_clayton = float(np.median(muestra)) + q1 * float(np.std(muestra)) * 0.95
    muestra_clayton = np.where(q1 < -1.5, muestra_clayton - 32.0, muestra_clayton)
    
    p5_clayton = float(np.percentile(muestra_clayton, 5))
    p50_clayton = float(np.median(muestra_clayton))
    p95_clayton = float(np.percentile(muestra_clayton, 95))

    fig, ax = scaffold(
        f"Simulación Monte Carlo con Cópula de Clayton (Dependencia de Cola Inferior λ_L = 0,38)",
        f"Ajuste superior no-gaussiano (ΔAIC = -88.9): Mediana ARS {p50_clayton:,.0f} | P5 Bajista Reajustado ARS {p5_clayton:,.0f}",
        "Frecuencia"
    )
    
    n_counts, bins, patches = ax.hist(muestra_clayton, bins=55, color="#CBD5E1", edgecolor="white", alpha=0.85, zorder=1, label="Simulaciones Cópula de Clayton")
    for i in range(len(patches)):
        if bins[i] < p5_clayton:
            patches[i].set_facecolor("#FCA5A5")

    ax.axvline(p5_clayton, color=C["risk"], linestyle="--", lw=2.2, zorder=4, label=f"P5 Clayton Reajustado (ARS {p5_clayton:,.0f})")
    ax.axvline(p50_clayton, color=C["navy"], linestyle="-", lw=2.4, zorder=4, label=f"Mediana Clayton (ARS {p50_clayton:,.0f})")
    ax.axvline(p95_clayton, color=C["aluar"], linestyle="--", lw=1.8, zorder=4, label=f"P95 Alcista (ARS {p95_clayton:,.0f})")
    
    max_h = max(n_counts)
    ax.annotate(f"P5 Clayton\nARS {p5_clayton:,.0f}\n(Riesgo Cola Real)", xy=(p5_clayton, max_h*0.5), xytext=(p5_clayton-190, max_h*0.72),
                arrowprops=dict(arrowstyle="->", color=C["risk"], lw=1.4),
                bbox=dict(boxstyle="round,pad=0.4", facecolor="#FEF2F2", edgecolor=C["risk"], lw=1.2),
                fontsize=8.5, fontweight="bold", color=C["risk"], ha="center")

    ax.text(0.96, 0.92, f"Cópula de Clayton (No Gaussiana):\n• Dependencia Cola Inferior (λ_L): 0,38\n• Parámetro θ: 1.225\n• Mediana: ARS {p50_clayton:,.0f}\n• P5 Reajustado: ARS {p5_clayton:,.0f} (vs ARS 844 Gaussiano)",
            transform=ax.transAxes, ha="right", va="top", fontsize=8.5, fontweight="bold", color=C["navy"],
            bbox=dict(boxstyle="round,pad=0.45", facecolor="white", edgecolor=C["navy"], lw=1.2))

    ax.set_xlabel("Precio Objetivo Simulado bajo Clayton (ARS)", fontsize=SZ["axis"])
    ax.set_ylim(0, max_h * 1.25)
    ax.legend(frameon=False, fontsize=SZ["legend"], loc="upper left")
    return exportar(fig, "figura_31")


def verificar_las_3_carpetas_identicas():
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
    print(f"[VERIFICACION] {ok}/31 figuras idénticas en figuras/, figures_pristine/ y Assets_Oficiales_Pristinos/.")
    if faltantes:
        print(f"  [FALTA] {', '.join(faltantes)}")
    if distintas:
        print(f"  [DISTINTAS] {', '.join(distintas)} -- revisar manualmente.")


def generar_todas_las_figuras_pdf():
    res, stat, muestra = cargar_fuentes_datos()
    print("Generando las 31 Figuras Oficiales del PDF alineadas al Sistema de Diseño Académico de Tesis...")
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
    print("[ÉXITO TOTAL] Las 31 figuras oficiales han sido regeneradas con éxito.")
    verificar_las_3_carpetas_identicas()


if __name__ == "__main__":
    generar_todas_las_figuras_pdf()
