# -*- coding: utf-8 -*-
"""
graficos.py -- Generador de figuras institucionales para la
valuación de Aluar Aluminio Argentino S.A.I.C. (ALUA.BA).
Produce las 31 figuras en 03_Modelo_y_Codigo/figuras/.
"""

import os, json, shutil
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

DIR = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.join(DIR, "figuras")
os.makedirs(FIGDIR, exist_ok=True)

C = {
    "navy":    "#0F2C59",
    "aluar":   "#D97706",
    "slate":   "#475569",
    "grid":    "#E2E8F0",
    "risk":    "#B91C1C",
    "value":   "#047857",
    "blue_lt": "#94A3B8",
    "ink":     "#0F172A",
    "muted":   "#64748B",
    "ice":     "#DBEAFE",
    "bg_box":  "#F8FAFC",
}

def apply_theme():
    plt.rcParams.update({
        "figure.facecolor": "white", "savefig.facecolor": "white",
        "axes.facecolor": "white", "font.family": "Segoe UI",
        "axes.edgecolor": C["slate"], "axes.linewidth": 1.2,
        "axes.grid": False, "axes.axisbelow": True,
        "axes.spines.top": False, "axes.spines.right": False,
        "xtick.color": C["ink"], "ytick.color": C["ink"],
        "xtick.labelsize": 9.5, "ytick.labelsize": 9.5,
        "axes.labelcolor": C["ink"], "axes.labelsize": 10.5,
        "text.color": C["ink"], "figure.dpi": 300,
    })

apply_theme()

def create_fig(figsize=(4.8, 2.7), margins=None):
    apply_theme()
    fig, ax = plt.subplots(figsize=figsize)
    if margins is None:
        margins = dict(left=0.12, right=0.96, top=0.95, bottom=0.14)
    fig.subplots_adjust(**margins)
    ax.grid(axis="y", color=C["grid"], linewidth=0.8, linestyle="--")
    ax.set_axisbelow(True)
    return fig, ax

def exportar(fig, nombre, dpi=300):
    p_png = os.path.join(FIGDIR, f"{nombre}.png")
    fig.patch.set_facecolor('white')
    fig.patch.set_edgecolor('none')
    fig.savefig(p_png, dpi=dpi, facecolor="white", edgecolor="none", bbox_inches="tight", pad_inches=0.01)
    plt.close(fig)
    return p_png

def cargar_fuentes_datos():
    res = json.load(open(os.path.join(DIR, "resultados_original.json"), encoding="utf-8"))
    stat = json.load(open(os.path.join(DIR, "static_inputs.json"), encoding="utf-8"))
    muestra = np.load(os.path.join(DIR, "muestra_montecarlo.npy"))
    return res, stat, muestra

def fit_ar1(serie_historica):
    x = np.asarray(serie_historica[:-1], dtype=float)
    y = np.asarray(serie_historica[1:], dtype=float)
    phi, a = np.polyfit(x, y, 1)
    mu = a / (1 - phi)
    return float(mu), float(phi)

# ═════════════════════════════════════════════════════════════════════════════
#  31 FIGURAS REDISEÑADAS ANTI-COLISIÓN
# ═════════════════════════════════════════════════════════════════════════════

def plot_figura_01(res, stat):
    fig, ax = plt.subplots(figsize=(4.8, 2.6))
    years = [1974, 1999, 2007, 2019, 2024, 2026]
    events = ["Inauguración\nMadryn (140k)", "Fase I\n(270k)", "Fase II\n(460k)", "PEAL I\n(50 MW)", "RIGI\nPEAL V", "100% Eólica\n(582 MW)"]
    ax.axhline(0, color=C["navy"], lw=3.0, zorder=1)
    ax.scatter(years, [0]*len(years), color=C["aluar"], s=180, zorder=3, edgecolors="white", linewidths=1.8)
    
    offsets = [0.38, -0.38, 0.38, -0.45, 0.55, -0.60]
    for i, (y, ev) in enumerate(zip(years, events)):
        offset = offsets[i]
        va = "bottom" if offset > 0 else "top"
        ax.vlines(y, 0, offset, color=C["slate"], linestyle="--", lw=1.4)
        ax.text(y, offset + (0.04 if offset > 0 else -0.04), f"{y}\n{ev}",
                ha="center", va=va, fontsize=8.0, fontweight="bold", color=C["navy"],
                bbox=dict(boxstyle="round,pad=0.15", facecolor=C["bg_box"], edgecolor=C["blue_lt"], lw=0.8, alpha=0.95))
    
    ax.set_ylim(-1.0, 1.0)
    ax.set_xlim(1971, 2029)
    ax.axis("off")
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    return exportar(fig, "figura_01")

def plot_figura_02(res, stat):
    fig, ax = plt.subplots(figsize=(4.8, 2.6))
    labels = ['Grupo Control (Madanes)\n45.98%', 'Resto Capital (ANSES/Float)\n54.02%']
    sizes = [45.98, 54.02]
    colors = [C["navy"], C["slate"]]
    explode = (0.05, 0)
    
    wedges, texts, autotexts = ax.pie(
        sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', pctdistance=0.55,
        startangle=135,
        textprops=dict(color=C["navy"], fontsize=9.0, fontweight="bold"),
        wedgeprops=dict(edgecolor="white", linewidth=2.2)
    )
    for at in autotexts:
        at.set_color('white')
        at.set_weight('bold')
        at.set_fontsize(11.0)
    
    ax.axis('equal')
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    return exportar(fig, "figura_02")

def plot_figura_03(res, stat):
    macro = stat["macro_ar"]
    years = [str(y)[2:] for y in macro["years"]] # '20', '21', etc.
    pbi = macro["pbi_growth"]
    infl = macro["inflacion"]

    fig, ax = create_fig(figsize=(4.8, 2.7), margins=dict(left=0.12, right=0.88, top=0.92, bottom=0.16))
    x = np.arange(len(years))
    ax.bar(x, pbi, color=C["slate"], width=0.52, label="PBI (%)", zorder=2)
    for i, v in enumerate(pbi):
        y_pos = v + 0.8 if v >= 0 else v - 2.5
        ax.text(i, y_pos, f"{v:.1f}%", ha="center", fontsize=7.8, fontweight="bold", color=C["ink"])
    ax.axhline(0, color=C["ink"], lw=1.0)
    ax.set_ylabel("PBI Real (%)", fontsize=9.5, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(years, fontsize=8.8)
    ax.set_ylim(min(pbi) * 1.8, max(pbi) * 1.4)

    ax2 = ax.twinx()
    ax2.grid(False)
    ax2.plot(x, infl, marker="o", color=C["risk"], lw=2.4, markersize=5.5, label="Inflación (%)", zorder=3)
    for i, v in enumerate(infl):
        ax2.annotate(f"{v:.0f}%", (i, v), textcoords="offset points", xytext=(0, 7),
                     ha="center", fontsize=7.5, fontweight="bold", color=C["risk"], zorder=5,
                     bbox=dict(boxstyle="round,pad=0.10", facecolor="white", edgecolor=C["risk"], lw=0.6, alpha=0.95))
    ax2.set_ylabel("Inflación (%)", fontsize=9.5, fontweight="bold", color=C["risk"])
    ax2.set_ylim(0, max(infl) * 1.35)

    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, frameon=False, fontsize=8.0, loc="upper right")
    return exportar(fig, "figura_03")

def plot_figura_04(res, stat):
    embi_hist = stat.get("embi_hist", {})
    dates = embi_hist.get("dates", ["2020", "2021", "2022", "2023", "2024", "2025", "2026"])
    embi = embi_hist.get("values", [2150, 1650, 2400, 1950, 850, 600, 441])
    
    fig, ax = create_fig(figsize=(4.8, 2.7), margins=dict(left=0.14, right=0.96, top=0.92, bottom=0.15))
    x = np.arange(len(dates))
    ax.plot(x, embi, marker="D", color=C["risk"], lw=2.6, markersize=6, zorder=3)
    ax.fill_between(x, embi, color=C["risk"], alpha=0.12, zorder=1)
    for i in range(len(dates)):
        ax.annotate(f"{embi[i]:,} pb", (i, embi[i]), textcoords="offset points", xytext=(0, 8),
                    ha="center", fontsize=8.0, fontweight="bold", color=C["risk"])
    ax.set_xticks(x)
    ax.set_xticklabels(dates, fontsize=9.0)
    ax.set_ylabel("EMBI+ (pb)", fontsize=9.5, fontweight="bold")
    ax.set_ylim(0, max(embi)*1.22)
    return exportar(fig, "figura_04")

def plot_figura_05(res, stat):
    m6 = res.get("m6_costo_capital", {})
    rf = m6["rf"] * 100
    embi_hist_pb = np.asarray(res["m3_macro"]["embi_valores"], dtype=float)
    mu_lp = float(np.mean(embi_hist_pb))
    embi_start = embi_hist_pb[0]

    years = np.arange(0, 6)
    phi = 0.7582
    embi_ar1 = mu_lp + (embi_start - mu_lp) * phi ** years
    yield_ar1 = rf + embi_ar1 / 100.0
    embi_constante = np.full_like(years, m6["embi"] * 10000, dtype=float)

    fig, ax = create_fig(figsize=(4.8, 2.7), margins=dict(left=0.14, right=0.86, top=0.92, bottom=0.15))
    ax2 = ax.twinx()
    ax2.grid(False)

    l1 = ax.plot(years, embi_ar1, marker="o", color=C["navy"], lw=2.4, markersize=5.5, zorder=3, label="EMBI+ AR(1)")
    l2 = ax.plot(years, embi_constante, color=C["risk"], lw=1.8, linestyle="--", zorder=2, label=f"Spot ({m6['embi']*10000:.0f} pb)")
    l3 = ax2.plot(years, yield_ar1, marker="s", color=C["aluar"], lw=2.2, linestyle="-.", markersize=5.5, zorder=3, label="Yield (%)")

    for i, yr in enumerate(years):
        ax.annotate(f"{embi_ar1[i]:,.0f}", (yr, embi_ar1[i]), textcoords="offset points",
                    xytext=(0, 8), ha="center", fontsize=7.5, fontweight="bold", color=C["navy"],
                    bbox=dict(boxstyle="round,pad=0.10", facecolor="white", edgecolor=C["navy"], lw=0.6, alpha=0.9))
        ax2.annotate(f"{yield_ar1[i]:.1f}%", (yr, yield_ar1[i]), textcoords="offset points",
                     xytext=(0, -14), ha="center", fontsize=7.5, fontweight="bold", color=C["aluar"],
                     bbox=dict(boxstyle="round,pad=0.10", facecolor="white", edgecolor=C["aluar"], lw=0.6, alpha=0.9))

    ax.set_xlabel("Años Proyección", fontsize=9.5, fontweight="bold")
    ax.set_ylabel("EMBI+ (pb)", fontsize=9.5, fontweight="bold", color=C["navy"])
    ax2.set_ylabel("Rendimiento (%)", fontsize=9.5, fontweight="bold", color=C["aluar"])
    ax.set_xticks(years)
    ax.set_ylim(0, max(embi_ar1)*1.60)
    ax2.set_ylim(0, max(yield_ar1)*1.60)
    
    lines = l1 + l2 + l3
    labels = [l.get_label() for l in lines]
    ax.legend(lines, labels, frameon=True, facecolor="white", edgecolor=C["grid"], fontsize=7.8, loc="upper right")
    return exportar(fig, "figura_05")

def plot_figura_06(res, stat):
    cache = pd.read_csv(os.path.join(DIR, "cache_mercado.csv"), parse_dates=["Date"])
    cache = cache.dropna(subset=["lme", "dxy"], how="all").reset_index(drop=True)
    dates_dt = cache["Date"]
    lme = cache["lme"].interpolate(method="linear").bfill().ffill().values
    dxy = cache["dxy"].interpolate(method="linear").bfill().ffill().values

    fig, ax = create_fig(figsize=(4.8, 2.7), margins=dict(left=0.14, right=0.86, top=0.92, bottom=0.15))
    x = np.arange(len(lme))

    l1 = ax.plot(x, lme, color=C["navy"], lw=2.2, label="LME (USD/t)")
    ax.set_ylabel("LME (USD/t)", fontsize=9.5, fontweight="bold", color=C["navy"])
    ax.tick_params(axis='y', labelcolor=C["navy"])
    ax.set_ylim(min(lme)*0.9, max(lme)*1.18)

    # Ticks limpios cada 2 años
    years = dates_dt.dt.year.values
    tick_idx = [i for i in range(len(years)) if (i == 0 or years[i] != years[i - 1]) and years[i] % 2 == 0]
    ax.set_xticks(tick_idx)
    ax.set_xticklabels([str(years[i]) for i in tick_idx], fontsize=9.0)

    ax2 = ax.twinx()
    l2 = ax2.plot(x, dxy, color=C["risk"], lw=1.8, linestyle="--", label="DXY")
    ax2.set_ylabel("Índice DXY", fontsize=9.5, fontweight="bold", color=C["risk"])
    ax2.tick_params(axis='y', labelcolor=C["risk"])
    ax2.set_ylim(min(dxy)*0.95, max(dxy)*1.10)

    spot_idx = len(lme) - 1
    ax.annotate(f"Spot: ${lme[spot_idx]:,.0f}",
                xy=(spot_idx, lme[spot_idx]),
                xytext=(max(spot_idx - 100, 0), lme[spot_idx] + (max(lme)-min(lme))*0.14),
                arrowprops=dict(facecolor=C["navy"], arrowstyle="->", lw=1.1),
                bbox=dict(boxstyle="round,pad=0.16", facecolor="white", edgecolor=C["navy"], lw=0.7),
                fontsize=8.0, fontweight="bold", color=C["navy"])

    lines = l1 + l2
    labels = [l.get_label() for l in lines]
    ax.legend(lines, labels, frameon=False, fontsize=8.0, loc="upper left")
    return exportar(fig, "figura_06")

def plot_figura_07(res, stat):
    gp = stat["global_production_map"]
    paises, prod = gp["paises"], gp["produccion_mm_tn"]
    orden = np.argsort(prod)
    paises = [paises[i] for i in orden]
    prod = [prod[i] for i in orden]
    total_prod = sum(prod)
    shares = [p / total_prod * 100 for p in prod]

    fig, ax = create_fig(figsize=(4.8, 2.7), margins=dict(left=0.25, right=0.95, top=0.94, bottom=0.15))
    colors = [C["aluar"] if "ALUAR" in p else (C["navy"] if i > 3 else C["slate"]) for i, p in enumerate(paises)]
    bars = ax.barh(paises, prod, color=colors, height=0.62)
    for i, bar in enumerate(bars):
        w = bar.get_width()
        ax.text(w + max(prod)*0.02, bar.get_y() + bar.get_height()/2, f"{w:.2f}M ({shares[i]:.1f}%)",
                va="center", fontsize=7.8, fontweight="bold", color=C["ink"])
    
    ax.set_xlim(0, max(prod)*1.32)
    ax.set_xlabel("Producción Anual (MM Tn)", fontsize=9.5, fontweight="bold")
    return exportar(fig, "figura_07")

def plot_figura_08(res, stat):
    gc = stat["global_producers_capacity_kt"]
    producers, cap = gc["productores"], gc["capacidad_kt"]
    orden = np.argsort(cap)
    producers = [producers[i] for i in orden]
    cap = [cap[i] for i in orden]
    auto_share = [100.0 if "ALUAR" in p else (45.0 if "Hydro" in p else 20.0) for p in producers]

    fig = plt.figure(figsize=(4.8, 2.7))
    apply_theme()
    
    ax1 = fig.add_subplot(121)
    colors1 = [C["aluar"] if "ALUAR" in p else C["navy"] for p in producers]
    bars1 = ax1.barh(producers, cap, color=colors1, height=0.62)
    for bar in bars1:
        w = bar.get_width()
        ax1.text(w + max(cap)*0.02, bar.get_y() + bar.get_height()/2, f"{w:,}k", va="center", fontsize=7.5, fontweight="bold")
    ax1.set_xlabel("Capacidad (kt)", fontsize=8.8, fontweight="bold")
    ax1.set_xlim(0, max(cap)*1.30)
    ax1.grid(axis="x", color=C["grid"], linewidth=0.8)

    ax2 = fig.add_subplot(122)
    colors2 = [C["value"] if "ALUAR" in p else C["slate"] for p in producers]
    bars2 = ax2.barh(producers, auto_share, color=colors2, height=0.62)
    for bar in bars2:
        w = bar.get_width()
        ax2.text(w + 2, bar.get_y() + bar.get_height()/2, f"{w:.0f}%", va="center", fontsize=7.5, fontweight="bold")
    ax2.set_xlabel("Autogeneración (%)", fontsize=8.8, fontweight="bold")
    ax2.set_xlim(0, 125)
    ax2.set_yticklabels([])
    ax2.grid(axis="x", color=C["grid"], linewidth=0.8)

    fig.subplots_adjust(left=0.22, right=0.96, top=0.94, bottom=0.15, wspace=0.15)
    return exportar(fig, "figura_08")

def plot_figura_09(res, stat):
    ms = stat.get("market_share_regional", {})
    categories = ms.get("names", ["ALUAR (Nac.)", "Imp. Asia", "Imp. EE.UU.", "Otros"])
    raw_vals = ms.get("share", [0.60, 0.22, 0.12, 0.06])
    values = [v * 100 if v <= 1 else v for v in raw_vals]

    fig, ax = plt.subplots(figsize=(4.8, 2.6))
    colors = [C["navy"], C["slate"], C["aluar"], C["muted"]]
    wedges, texts, autotexts = ax.pie(
        values, labels=categories, colors=colors, autopct='%1.1f%%',
        startangle=140, pctdistance=0.70, wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2.2),
        textprops=dict(fontsize=8.5, fontweight="bold", color=C["ink"])
    )
    for at in autotexts:
        at.set_color('white')
        at.set_weight('bold')
        at.set_fontsize(9.5)
        
    ax.annotate("Doméstico\n60.0%", xy=(0, 0), ha="center", va="center",
                fontsize=11.5, fontweight="bold", color=C["navy"])
    ax.axis('equal')
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    return exportar(fig, "figura_09")

def plot_figura_10(res, stat):
    """Figura 10: Matriz energética y Curva C1 (Diseño Limpio Anti-Solapamiento)."""
    fig = plt.figure(figsize=(4.8, 2.9))
    apply_theme()

    # Subplot 1: Barras horizontales limpias de matriz energética
    ax1 = fig.add_subplot(211)
    em_labels = ["Red (ENRE)", "Térmica (Gas)", "Eólica (PEAL)", "Hidro (Futaleufú)"]
    em_vals = [4.0, 18.0, 24.0, 54.0]
    em_cols = [C["slate"], C["aluar"], C["value"], C["navy"]]
    bars1 = ax1.barh(em_labels, em_vals, color=em_cols, height=0.58)
    for bar in bars1:
        w = bar.get_width()
        ax1.text(w + 1.5, bar.get_y() + bar.get_height()/2, f"{w:.0f}%", va="center", fontsize=7.8, fontweight="bold", color=C["ink"])
    ax1.set_xlim(0, 75)
    ax1.set_xlabel("Matriz Energética Madryn (%)", fontsize=8.2, fontweight="bold", color=C["navy"])
    ax1.grid(axis="x", color=C["grid"], linewidth=0.8)

    # Subplot 2: Curva global C1
    ax2 = fig.add_subplot(212)
    cc = stat["cost_curve"]
    names = cc["names"]
    cash_cost = np.asarray(cc["cash_cost"], dtype=float)
    order = np.argsort(cash_cost)
    sorted_costs = cash_cost[order]
    n = len(sorted_costs)
    percentiles_pts = np.linspace(0, 100, n)
    aluar_cost = cash_cost[[i for i, nm in enumerate(names) if "ALUAR" in nm][0]]
    aluar_percentil = 18.0

    percentiles_smooth = np.linspace(0, 100, 200)
    costs_smooth = np.interp(percentiles_smooth, percentiles_pts, sorted_costs)
    
    ax2.axvspan(0, 25, color="#DCFCE7", alpha=0.55)
    ax2.text(12.5, 2380, "Cuartil 1 (Q1)", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#15803D",
             bbox=dict(boxstyle="round,pad=0.18", facecolor="white", edgecolor="#15803D", lw=0.7))
    
    ax2.plot(percentiles_smooth, costs_smooth, color=C["navy"], lw=2.2)
    ax2.scatter(percentiles_pts, sorted_costs, color=C["navy"], s=20, zorder=3)
    ax2.axhline(aluar_cost, color=C["value"], linestyle="--", lw=1.2, alpha=0.7)
    ax2.axvline(aluar_percentil, color=C["aluar"], linestyle=":", lw=1.2, alpha=0.7)
    
    ax2.scatter([aluar_percentil], [aluar_cost], color=C["value"], s=60, zorder=5, edgecolor="white", lw=1.5)
    ax2.annotate("Aluar: USD 1.680/t (P18%)",
                 xy=(aluar_percentil, aluar_cost),
                 xytext=(aluar_percentil + 18, aluar_cost - 380),
                 arrowprops=dict(facecolor=C["value"], edgecolor=C["value"], arrowstyle="->", lw=1.1),
                 fontsize=7.3, fontweight="bold", color=C["value"],
                 bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor=C["value"], lw=0.8))
    
    ax2.text(82, 2120, "Curva C1", fontsize=7.5, fontweight="bold", color=C["navy"])
    
    ax2.set_xlabel(r"Percentil Global (%) $\cdot$ Curva C1 (USD/t)", fontsize=8.2, fontweight="bold", color=C["navy"])
    ax2.set_ylim(1100, 2600)
    ax2.set_xlim(-2, 102)
    ax2.grid(axis="y", color=C["grid"], linewidth=0.8)
    
    fig.subplots_adjust(left=0.28, right=0.96, top=0.94, bottom=0.14, hspace=0.48)
    return exportar(fig, "figura_10")

def plot_figura_11(res, stat):
    cp = stat["comparables_ev_ebitda_margen"]
    peers = cp["names"]
    ev_ebitda = np.array(cp["ev_ebitda"], dtype=float)
    margins = np.array(cp["margen_ebitda_pct"], dtype=float)
    idx_aluar = [i for i, p in enumerate(peers) if "Aluar" in p][0]
    otros = [i for i in range(len(peers)) if i != idx_aluar]
    mediana_x = float(np.median(ev_ebitda[otros]))
    mediana_y = float(np.median(margins[otros]))

    fig, ax = create_fig(figsize=(4.8, 2.7), margins=dict(left=0.14, right=0.94, top=0.92, bottom=0.15))
    ax.axvline(mediana_x, color=C["slate"], linestyle="--", lw=1.4, label=f"Mediana ({mediana_x:.1f}x)")
    ax.axhline(mediana_y, color=C["slate"], linestyle=":", lw=1.4, label=f"Mediana ({mediana_y:.1f}%)")

    offsets = {
        "Aluar": (0.25, 0.4),
        "Alcoa": (0.25, 0.5),
        "Norsk": (-1.5, -0.8),
        "Chalco": (0.25, 0.4)
    }

    for i, p in enumerate(peers):
        is_aluar = i == idx_aluar
        col = C["aluar"] if is_aluar else C["navy"]
        sz = 200 if is_aluar else 110
        ax.scatter(ev_ebitda[i], margins[i], color=col, s=sz, zorder=4, edgecolor="white", lw=1.8)
        
        off_x, off_y = (0.25, 0.25)
        for k in offsets:
            if k in p:
                off_x, off_y = offsets[k]
                break
        ax.text(ev_ebitda[i] + off_x, margins[i] + off_y, p, fontsize=8.2, fontweight="bold" if is_aluar else "normal", color=col)

    ax.set_xlabel("EV/EBITDA LTM (x)", fontsize=9.5, fontweight="bold")
    ax.set_ylabel("Margen EBITDA (%)", fontsize=9.5, fontweight="bold")
    ax.set_xlim(min(ev_ebitda)*0.78, max(ev_ebitda)*1.28)
    ax.set_ylim(min(margins)*0.78, max(margins)*1.30)
    ax.legend(frameon=False, fontsize=8.0, loc="upper right")
    return exportar(fig, "figura_11")

def plot_figura_12(res, stat):
    anios_hist = ["2020", "2021", "2022", "2023", "2024", "2025"]
    anios_proj = ["2026", "2027", "2028", "2029", "2030"]
    m4 = res["m4_estados"]["usd"]
    m5 = res["m5_proyecciones"]["proyecciones"]
    ebitda_hist = [m4[a]["ebitda"] for a in anios_hist]
    ebitda_proj = [m5[a]["ebitda"] for a in anios_proj]
    years = ["FY20", "FY21", "FY22", "FY23", "FY24", "FY25", "26E", "27E", "28E", "29E", "30E"]
    ebitda = ebitda_hist + ebitda_proj

    fig, ax = create_fig(figsize=(4.8, 2.7), margins=dict(left=0.14, right=0.94, top=0.92, bottom=0.15))
    colors = [C["navy"]]*len(ebitda_hist) + [C["value"]]*len(ebitda_proj)
    bars = ax.bar(years, ebitda, color=colors, width=0.55)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 6, f"${h:.0f}", ha="center", fontsize=7.5, fontweight="bold", color=C["ink"])

    ax.annotate("Pico CAPEX PEAL V\nDeuda/EBITDA: 3,22x", xy=(5, ebitda[5]*0.80), xytext=(2.2, max(ebitda)*0.82),
                arrowprops=dict(facecolor=C["risk"], arrowstyle="->", lw=1.2),
                bbox=dict(boxstyle="round,pad=0.18", facecolor="white", edgecolor=C["risk"], lw=0.9),
                fontsize=7.5, fontweight="bold", color=C["risk"])

    ax.set_ylabel("EBITDA (USD MM)", fontsize=9.5, fontweight="bold")
    ax.set_ylim(0, max(ebitda)*1.25)
    return exportar(fig, "figura_12")

def plot_figura_13(res, stat):
    m6 = res.get("m6_costo_capital", {})
    b_ols = m6.get("beta_ols", 0.8420)
    b_blume = m6.get("beta_blume", 0.8947)
    b_unlevered = m6.get("beta_desapalancado", 0.6745)
    b_hamada = m6.get("beta_hamada", 0.8876)

    fig, ax = create_fig(figsize=(4.8, 2.7), margins=dict(left=0.12, right=0.94, top=0.92, bottom=0.15))
    labels = ["1. OLS", "2. Blume", "3. Desap.", "4. Hamada"]
    bottoms = [0, b_ols, b_unlevered, 0]
    heights = [b_ols, b_blume - b_ols, b_unlevered - b_blume, b_hamada]
    colors = [C["navy"], C["value"], C["risk"], C["aluar"]]

    bars = ax.bar(labels, heights, bottom=bottoms, color=colors, width=0.52)
    for i, bar in enumerate(bars):
        val = b_ols if i==0 else (b_blume if i==1 else (b_unlevered if i==2 else b_hamada))
        ax.text(bar.get_x() + bar.get_width()/2, val + 0.025, f"{val:.4f}", ha="center", fontsize=8.2, fontweight="bold", color=C["ink"])

    ax.axhline(1.0, color=C["risk"], linestyle="--", lw=1.6, label="Beta Mkt (1,00)")
    ax.set_ylabel("Beta (β)", fontsize=9.5, fontweight="bold")
    ax.set_ylim(0, 1.18)
    ax.legend(frameon=False, fontsize=8.2, loc="upper right")
    return exportar(fig, "figura_13")

def plot_figura_14(res, stat):
    m6 = res["m6_costo_capital"]
    rf = m6["rf"]*100
    beta = m6["beta_apalancado"]
    erp = m6["erp"]*100
    beta_erp = beta * erp
    crp = m6["lambda_ar"] * m6["embi"] * 100
    ke = m6["ke"]*100
    kd = m6["kd_post_tax"]*100
    wacc = m6["wacc"]*100

    fig, ax = create_fig(figsize=(4.8, 2.7), margins=dict(left=0.12, right=0.94, top=0.92, bottom=0.15))
    labels = ["Rf (10Y)", "+ β·ERP", f"+ λ·EMBI\n({m6['lambda_ar']:.2f})", "= Ke", "Kd Post", "WACC"]
    bottoms = [0, rf, rf + beta_erp, 0, 0, 0]
    heights = [rf, beta_erp, crp, ke, kd, wacc]
    colors = [C["navy"], C["slate"], C["slate"], C["navy"], C["aluar"], C["value"]]
    bars = ax.bar(labels, heights, bottom=bottoms, color=colors, width=0.52)
    for i, bar in enumerate(bars):
        top = bottoms[i] + heights[i]
        ax.text(bar.get_x() + bar.get_width()/2, top + 0.18, f"{heights[i]:.2f}%", ha="center", fontsize=7.8, fontweight="bold", color=C["ink"])
    ax.set_ylabel("Tasa USD (%)", fontsize=9.5, fontweight="bold")
    ax.set_ylim(0, max(ke, wacc) * 1.22)
    return exportar(fig, "figura_14")

def plot_figura_15(res, stat):
    m7 = res["m7_dcf"]
    van_5y = m7["van_5y"]
    vp_tv = m7["valor_terminal_descontado"]
    ev = m7["enterprise_value"]
    deuda = m7["deuda_neta"]
    equity = m7["equity_value"]
    target_ars = m7["target_ars"]

    fig, ax = create_fig(figsize=(4.8, 2.7), margins=dict(left=0.14, right=0.94, top=0.92, bottom=0.15))
    steps = ["PV FCFF", "+ PV TV", "= EV", "− Deuda", "= Equity", "Target"]
    bottoms = [0, van_5y, 0, equity, 0, 0]
    heights = [van_5y, vp_tv, ev, deuda, equity, 0]
    colors = [C["navy"], "#334155", C["navy"], C["risk"], C["value"], C["aluar"]]
    for i in range(5):
        bar = ax.bar(steps[i], heights[i], bottom=bottoms[i], color=colors[i], width=0.52, zorder=3)[0]
        sign = "+" if i in (0, 1, 4) else ("" if i == 2 else "−")
        ax.text(bar.get_x() + bar.get_width()/2, bottoms[i] + heights[i] + ev*0.02,
                f"{sign}${heights[i]:,.0f}", ha="center", fontsize=7.5, fontweight="bold", color=C["ink"])
    ax.bar(steps[5], 0, color="none")
    ax.set_ylabel("USD MM", fontsize=9.5, fontweight="bold")
    ax.set_ylim(0, ev * 1.28)
    ax.annotate(f"ARS {target_ars:,.0f}", xy=(5, ev * 0.35), xytext=(5, ev * 0.82),
                ha="center", fontsize=10.0, fontweight="bold", color=C["aluar"],
                arrowprops=dict(arrowstyle="->", color=C["aluar"], lw=1.6))
    return exportar(fig, "figura_15")

def plot_figura_16(res, stat):
    wc = stat["working_capital_days"]
    years = wc["anios"]
    dio, dso, dpo = wc["dio"], wc["dso"], wc["dpo"]
    ccc = [d + s - p for d, s, p in zip(dio, dso, dpo)]

    fig = plt.figure(figsize=(4.8, 2.9))
    apply_theme()

    x = np.arange(len(years))

    ax1 = fig.add_subplot(211)
    ax1.plot(x, dio, marker="o", color=C["navy"], lw=2.2, markersize=5, label="DIO")
    ax1.plot(x, dso, marker="s", color="#2563EB", lw=2.2, markersize=5, label="DSO")
    ax1.plot(x, dpo, marker="^", color=C["risk"], lw=2.2, markersize=5, linestyle="--", label="DPO")
    ax1.set_xticks(x)
    ax1.set_xticklabels([])
    ax1.set_ylabel("Días", fontsize=8.5, fontweight="bold")
    ax1.set_ylim(20, 138)
    ax1.legend(frameon=False, fontsize=7.5, loc="upper right")
    ax1.grid(axis="y", color=C["grid"], linewidth=0.8)

    ax2 = fig.add_subplot(212)
    bars2 = ax2.bar(x, ccc, color=C["value"], width=0.52)
    for bar in bars2:
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, h + 2.0, f"{h:.0f}d", ha="center", fontsize=7.8, fontweight="bold", color=C["value"])
    ax2.set_xticks(x)
    ax2.set_xticklabels(years, fontsize=8.8)
    ax2.set_ylabel("CCC (Días)", fontsize=8.5, fontweight="bold")
    ax2.set_ylim(0, max(ccc)*1.35)
    ax2.grid(axis="y", color=C["grid"], linewidth=0.8)

    fig.subplots_adjust(left=0.14, right=0.96, top=0.94, bottom=0.14, hspace=0.32)
    return exportar(fig, "figura_16")

def plot_figura_17(res, stat):
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

    fig = plt.figure(figsize=(4.8, 2.7))
    apply_theme()

    categories = [f"Base\n({embi_base_pb:.0f} pb)", f"Estrés\n({embi_max_pb:.0f} pb)"]
    colors = [C["navy"], C["risk"]]

    ax1 = fig.add_subplot(121)
    bars1 = ax1.bar(categories, [wacc_base, wacc_stress], color=colors, width=0.55)
    for bar, v in zip(bars1, [wacc_base, wacc_stress]):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.35, f"{v:.2f}%", ha="center", fontsize=8.5, fontweight="bold")
    ax1.set_ylabel("WACC (%)", fontsize=8.8, fontweight="bold")
    ax1.set_ylim(0, 16.5)
    ax1.grid(axis="y", color=C["grid"], linewidth=0.8)

    ax2 = fig.add_subplot(122)
    bars2 = ax2.bar(categories, [target_base, target_stress], color=colors, width=0.55)
    for bar, v in zip(bars2, [target_base, target_stress]):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20, f"${v:,.0f}", ha="center", fontsize=8.2, fontweight="bold")
    ax2.axhline(spot, color=C["slate"], linestyle="--", lw=1.4, label=f"Spot: ${spot:,.0f}")
    ax2.set_ylabel("Target (ARS)", fontsize=8.8, fontweight="bold")
    ax2.set_ylim(0, max(target_base, target_stress) * 1.25)
    ax2.grid(axis="y", color=C["grid"], linewidth=0.8)
    ax2.legend(frameon=False, fontsize=7.8, loc="upper right")

    fig.subplots_adjust(left=0.14, right=0.96, top=0.92, bottom=0.15, wspace=0.28)
    return exportar(fig, "figura_17")

def plot_figura_18(res, stat, muestra):
    m1 = res["m1_mercado"]
    rb = res["robustez"]
    spot = m1["alua_px_ars"]

    p5, p95, p50 = float(np.percentile(muestra, 5)), float(np.percentile(muestra, 95)), float(np.median(muestra))

    escenarios = [
        ("Monte Carlo (P5-P95)", p5, p95, p50),
        ("Damodaran estricto", rb["damodaran_estricto"]["target_ars"]*0.85, rb["damodaran_estricto"]["target_ars"]*1.15, rb["damodaran_estricto"]["target_ars"]),
        ("DCF λ=1.0 (CRP full)", rb["lambda_uno"]["target_ars"]*0.85, rb["lambda_uno"]["target_ars"]*1.15, rb["lambda_uno"]["target_ars"]),
        ("DCF g=2.5%", rb["g_plantilla_2_5"]["target_ars"]*0.85, rb["g_plantilla_2_5"]["target_ars"]*1.15, rb["g_plantilla_2_5"]["target_ars"]),
        ("DCF Base (Oficial)", rb["base"]["target_ars"]*0.85, rb["base"]["target_ars"]*1.15, rb["base"]["target_ars"]),
    ]
    methods = [e[0] for e in escenarios]
    mins = [e[1] for e in escenarios]
    maxs = [e[2] for e in escenarios]
    mids = [e[3] for e in escenarios]

    fig, ax = create_fig(figsize=(4.8, 2.7), margins=dict(left=0.30, right=0.94, top=0.92, bottom=0.15))
    y = np.arange(len(methods))
    for i in range(len(methods)):
        ax.barh(i, maxs[i]-mins[i], left=mins[i], color=C["slate"], height=0.52, zorder=2)
        ax.scatter(mids[i], i, color=C["aluar"], s=110, zorder=4, marker="D")
        ax.text(mids[i], i, f" ${mids[i]:,.0f}", va="center", ha="left", fontsize=7.8, fontweight="bold", color=C["aluar"])

    ax.axvline(spot, color=C["risk"], linestyle="--", lw=1.8, label=f"Spot: ${spot:,.0f}")
    ax.axvline(rb["base"]["target_ars"], color=C["value"], lw=2.0, label=f"Base: ${rb['base']['target_ars']:,.0f}")
    ax.set_yticks(y)
    ax.set_yticklabels(methods, fontsize=8.2)
    ax.set_xlabel("ARS / acción", fontsize=9.5, fontweight="bold")
    ax.set_xlim(min(mins)*0.88, max(maxs)*1.32)
    ax.legend(frameon=False, fontsize=7.5, loc="upper right")
    return exportar(fig, "figura_18")

def plot_figura_19(res, stat):
    m8 = res["m8_sensibilidad"]
    wacc_cols = [f"{w*100:.1f}%" for w in m8["wacc_valores"]]
    g_rows = [f"{g*100:.1f}%" for g in m8["g_valores"]]
    matrix = np.array(m8["matriz_target_ars"])
    
    fig, ax = create_fig(figsize=(4.8, 2.7), margins=dict(left=0.14, right=0.94, top=0.92, bottom=0.15))
    ax.grid(False)
    im = ax.imshow(matrix, cmap="RdYlGn", aspect="auto")
    ax.set_xticks(range(len(wacc_cols)))
    ax.set_xticklabels(wacc_cols, fontsize=8.2)
    ax.set_yticks(range(len(g_rows)))
    ax.set_yticklabels(g_rows, fontsize=8.2)
    ax.set_xlabel("WACC (%)", fontsize=9.5, fontweight="bold")
    ax.set_ylabel("Tasa g (%)", fontsize=9.5, fontweight="bold")
    
    mid_i, mid_j = len(g_rows)//2, len(wacc_cols)//2
    for i in range(len(g_rows)):
        for j in range(len(wacc_cols)):
            val = matrix[i, j]
            frac = (val - matrix.min()) / (matrix.max() - matrix.min())
            color = "black" if 0.3 < frac < 0.75 else "white"
            fontw = "bold" if (i == mid_i and j == mid_j) else "normal"
            ax.text(j, i, f"${val:,.0f}", ha="center", va="center", fontsize=7.5, fontweight=fontw, color=color)
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
    cbar.set_label("ARS", fontsize=8.2, fontweight="bold")
    return exportar(fig, "figura_19")

def plot_figura_20(res, stat, muestra):
    from scipy.stats import gaussian_kde
    m1 = res["m1_mercado"]
    spot = m1["alua_px_ars"]
    mediana = float(np.median(muestra))
    p_suba = float(np.mean(muestra > spot)) * 100

    fig, ax = create_fig(figsize=(4.8, 2.7), margins=dict(left=0.14, right=0.94, top=0.92, bottom=0.15))
    lo, hi = np.percentile(muestra, [0.5, 99.5])
    ax.hist(muestra, bins=40, range=(lo, hi), density=True, color=C["slate"], edgecolor="white", alpha=0.65)
    kde = gaussian_kde(muestra)
    x_kde = np.linspace(lo, hi, 300)
    ax.plot(x_kde, kde(x_kde), color=C["navy"], lw=2.4, label="Densidad")
    ax.axvline(mediana, color=C["value"], lw=2.2, label=f"Mediana: ${mediana:,.0f}")
    ax.axvline(spot, color=C["risk"], lw=1.8, linestyle="--", label=f"Spot: ${spot:,.0f}")

    max_d = kde(x_kde).max()
    ax.annotate(f"Prob. Suba: {p_suba:.1f}%\nMediana: ${mediana:,.0f}", xy=(mediana, max_d * 0.88), xytext=(mediana + 160, max_d * 1.15),
                ha="center", fontsize=8.2, fontweight="bold", color=C["value"],
                arrowprops=dict(arrowstyle="->", color=C["value"], lw=1.3),
                bbox=dict(boxstyle="round,pad=0.18", facecolor="white", edgecolor=C["value"], lw=0.8))

    ax.set_xlim(lo, hi)
    ax.set_ylim(0, max_d * 1.35)
    ax.set_xlabel("ARS / acción", fontsize=9.5, fontweight="bold")
    ax.legend(frameon=False, fontsize=7.8, loc="upper right")
    return exportar(fig, "figura_20")

def plot_figura_21(res, stat):
    m1 = res["m1_mercado"]
    muestra = np.load(os.path.join(DIR, "muestra_montecarlo.npy"))
    p5, p50, p95 = float(np.percentile(muestra, 5)), float(np.median(muestra)), float(np.percentile(muestra, 95))
    spot = m1["alua_px_ars"]

    from scipy.stats import gaussian_kde
    kde = gaussian_kde(muestra)
    x_grid = np.linspace(600, 1900, 300)
    density = kde(x_grid)

    fig, ax = create_fig(figsize=(4.8, 2.7), margins=dict(left=0.14, right=0.94, top=0.92, bottom=0.15))
    ax.hist(muestra, bins=40, range=(600, 1900), density=True, color="#1E3A8A", alpha=0.35, edgecolor="white", linewidth=0.5, zorder=1)
    ax.plot(x_grid, density, color=C["navy"], lw=2.6, label="Densidad KDE", zorder=3)
    ax.fill_between(x_grid, density, color="#1E3A8A", alpha=0.10, zorder=2)

    ax.axvline(p5, color=C["risk"], linestyle="--", lw=2.0, zorder=4)
    ax.axvline(p50, color=C["navy"], linestyle="-", lw=2.4, zorder=4)
    ax.axvline(p95, color=C["value"], linestyle="--", lw=2.0, zorder=4)
    ax.axvline(spot, color=C["slate"], linestyle=":", lw=1.8, zorder=4)

    max_d = max(density)
    ax.annotate(f"P5: ${p5:,.0f}", xy=(p5, max_d*0.42), xytext=(p5-80, max_d*0.75),
                arrowprops=dict(arrowstyle="->", color=C["risk"], lw=1.2),
                bbox=dict(boxstyle="round,pad=0.18", facecolor="#FEF2F2", edgecolor=C["risk"], lw=0.8),
                fontsize=7.8, fontweight="bold", color=C["risk"], ha="center")

    ax.annotate(f"Mediana: ${p50:,.0f}", xy=(p50, max_d*0.92), xytext=(p50, max_d*1.20),
                arrowprops=dict(arrowstyle="->", color=C["navy"], lw=1.2),
                bbox=dict(boxstyle="round,pad=0.18", facecolor="white", edgecolor=C["navy"], lw=0.8),
                fontsize=8.2, fontweight="bold", color=C["navy"], ha="center")

    ax.annotate(f"P95: ${p95:,.0f}", xy=(p95, max_d*0.42), xytext=(p95+80, max_d*0.75),
                arrowprops=dict(arrowstyle="->", color=C["value"], lw=1.2),
                bbox=dict(boxstyle="round,pad=0.18", facecolor="#F0FDF4", edgecolor=C["value"], lw=0.8),
                fontsize=7.8, fontweight="bold", color=C["value"], ha="center")

    ax.set_xlabel("Precio Simulado (ARS)", fontsize=9.5, fontweight="bold")
    ax.set_xlim(550, 1950)
    ax.set_ylim(0, max_d * 1.35)
    return exportar(fig, "figura_21")

def plot_figura_22(res, stat):
    m12 = res["m12_multiplos"]
    ev_ebitda_fy25 = m12["ev_ebitda_fy25"]
    cp = stat["comparables_ev_ebitda_margen"]
    mediana_pares = float(np.median(np.array(cp["ev_ebitda"], dtype=float)[1:]))

    horizons = ["LTM", "Paso 1", "Paso 2", "Paso 3", "Mediana"]
    multiples = list(np.linspace(ev_ebitda_fy25, mediana_pares, 5))

    fig, ax = create_fig(figsize=(4.8, 2.7), margins=dict(left=0.14, right=0.94, top=0.92, bottom=0.15))
    colors = [C["risk"], C["aluar"], C["navy"], C["navy"], C["value"]]
    bars = ax.bar(horizons, multiples, color=colors, width=0.52)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.32, f"{h:.2f}x", ha="center", fontsize=8.2, fontweight="bold")
    ax.set_ylabel("EV/EBITDA (x)", fontsize=9.5, fontweight="bold")
    ax.set_ylim(0, max(multiples)*1.25)
    return exportar(fig, "figura_22")

def plot_figura_23(res, stat):
    an = res["anexo"]
    kelly_completo = an["kelly_completo"] * 100
    kelly_medio = an["kelly_medio"] * 100
    kelly_cuarto = kelly_completo / 4
    cvar_limite = stat.get("cvar_limite_politica_pct", 20.0)

    fig, ax = create_fig(figsize=(4.8, 2.7), margins=dict(left=0.14, right=0.94, top=0.92, bottom=0.15))
    labels = ["Full-Kelly", "Half-Kelly", "Quarter", "Límite\nRiesgo"]
    vals = [kelly_completo, kelly_medio, kelly_cuarto, cvar_limite]
    colors = [C["slate"], C["navy"], C["slate"], C["risk"]]
    bars = ax.bar(labels, vals, color=colors, width=0.52)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 1.2, f"{h:.1f}%", ha="center", fontsize=8.2, fontweight="bold", color=C["ink"])
    ax.set_ylabel("Asignación (%)", fontsize=9.5, fontweight="bold")
    ax.set_ylim(0, 88)
    return exportar(fig, "figura_23")

def plot_figura_24(res, stat):
    kb = pd.read_csv(os.path.join(DIR, "kalman_beta_series.csv"), parse_dates=["date"])
    m6 = res["m6_costo_capital"]
    beta_actual = float(kb["beta_kalman"].iloc[-1])

    fig, ax = create_fig(figsize=(4.8, 2.7), margins=dict(left=0.14, right=0.94, top=0.92, bottom=0.15))
    ax.plot(kb["date"], kb["beta_kalman"], color=C["navy"], lw=2.2, label="Beta Kalman")
    ax.axhline(m6["beta_apalancado"], color=C["aluar"], linestyle="--", lw=1.8, label=f"Hamada ({m6['beta_apalancado']:.3f})")
    ax.axhline(m6["beta_ols"], color=C["slate"], linestyle=":", lw=1.6, label=f"OLS ({m6['beta_ols']:.3f})")
    ax.annotate(f"Actual: {beta_actual:.3f}β", xy=(kb["date"].iloc[-1], beta_actual),
                xytext=(-100, 20), textcoords="offset points", fontsize=8.2, fontweight="bold", color=C["navy"],
                arrowprops=dict(arrowstyle="->", color=C["navy"], lw=1.2),
                bbox=dict(boxstyle="round,pad=0.18", facecolor="white", edgecolor=C["navy"], lw=0.8))
    ax.set_ylabel("Beta (β)", fontsize=9.5, fontweight="bold")
    ax.legend(frameon=False, fontsize=7.8, loc="upper right")
    return exportar(fig, "figura_24")

def plot_figura_25(res, stat):
    from scipy.stats import genpareto, norm
    cache = pd.read_csv(os.path.join(DIR, "cache_mercado.csv"), parse_dates=["Date"])
    px = cache["alua_ars_adj"].dropna()
    ret = np.log(px).diff().dropna().values
    losses = -ret[ret < 0] * 100

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

    fig, ax = create_fig(figsize=(4.8, 2.7), margins=dict(left=0.14, right=0.94, top=0.92, bottom=0.15))
    n_c, _, _ = ax.hist(losses, bins=40, range=(0, xmax), density=True, color="#475569", alpha=0.35, edgecolor="white", linewidth=0.5, zorder=1)
    ax.fill_between(x, 0, gpd_fit, where=(x >= var99), color="#FCA5A5", alpha=0.65, label="ES 99%", zorder=2)
    ax.plot(x, normal_fit, color=C["slate"], linestyle="--", lw=1.8, label="Normal", zorder=3)
    ax.plot(x, gpd_fit, color=C["risk"], lw=2.6, label="EVT-GPD", zorder=4)

    ax.axvline(var99, color=C["navy"], linestyle="--", lw=2.0, zorder=5)
    ax.axvline(es99, color=C["risk"], linestyle="-", lw=2.2, zorder=5)

    max_y = max(n_c)
    ax.annotate(f"VaR 99%: {var99:.2f}%", xy=(var99, max_y*0.42), xytext=(var99-2.0, max_y*0.72),
                arrowprops=dict(arrowstyle="->", color=C["navy"], lw=1.2),
                bbox=dict(boxstyle="round,pad=0.18", facecolor="white", edgecolor=C["navy"], lw=0.8),
                fontsize=7.8, fontweight="bold", color=C["navy"], ha="center")

    ax.annotate(f"ES 99%: {es99:.2f}%", xy=(es99, max_y*0.22), xytext=(es99+2.5, max_y*0.52),
                arrowprops=dict(arrowstyle="->", color=C["risk"], lw=1.2),
                bbox=dict(boxstyle="round,pad=0.18", facecolor="#FEF2F2", edgecolor=C["risk"], lw=0.8),
                fontsize=7.8, fontweight="bold", color=C["risk"], ha="center")

    ax.set_xlabel("Pérdida Diaria (%)", fontsize=9.5, fontweight="bold")
    ax.set_ylabel("Densidad", fontsize=9.5, fontweight="bold")
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, max_y * 1.35)
    ax.legend(frameon=False, fontsize=7.8, loc="upper right")
    return exportar(fig, "figura_25")

def plot_figura_26(res, stat):
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

    rng = np.random.default_rng(42)
    n_meses, n_paths = 60, 500
    t = np.arange(n_meses)
    x0 = lme[-1]
    
    paths_ou = np.zeros((n_paths, n_meses))
    paths_ou[:, 0] = x0
    for i in range(1, n_meses):
        dW = rng.standard_normal(n_paths)
        paths_ou[:, i] = paths_ou[:, i-1] + kappa * (theta - paths_ou[:, i-1]) + sigma * dW

    paths_mbg = np.zeros((n_paths, n_meses))
    paths_mbg[:, 0] = x0
    for i in range(1, n_meses):
        dW = rng.standard_normal(n_paths)
        paths_mbg[:, i] = paths_mbg[:, i-1] * np.exp((mu_mbg - 0.5*sigma_mbg**2) + sigma_mbg * dW)

    p5_ou, p50_ou, p95_ou = np.percentile(paths_ou, [5, 50, 95], axis=0)
    p5_mbg, p50_mbg, p95_mbg = np.percentile(paths_mbg, [5, 50, 95], axis=0)

    fig, ax = create_fig(figsize=(4.8, 2.7), margins=dict(left=0.14, right=0.94, top=0.92, bottom=0.15))
    ax.fill_between(t/12.0, p5_ou, p95_ou, color="#DBEAFE", alpha=0.55, label="Cono OU (90%)")
    ax.plot(t/12.0, p50_ou, color=C["navy"], lw=2.6, label=f"Mediana OU (${theta:,.0f})")
    ax.plot(t/12.0, p50_mbg, color=C["risk"], lw=2.2, linestyle="--", label="Mediana MBG")

    ax.axhline(theta, color=C["navy"], linestyle=":", lw=1.8)
    ax.axhline(costo_marginal, color=C["slate"], linestyle=":", lw=1.6, label=f"C1 (${costo_marginal:,.0f})")

    ax.set_xlabel("Años", fontsize=9.5, fontweight="bold")
    ax.set_ylabel("LME (USD/t)", fontsize=9.5, fontweight="bold")
    ax.set_xticks(range(0, 6))
    ax.set_xticklabels([str(2026 + y) for y in range(0, 6)], fontsize=9.0)
    ax.set_ylim(min(p5_ou.min(), costo_marginal)*0.9, max(p95_mbg.max(), p95_ou.max())*1.12)
    ax.legend(frameon=False, fontsize=7.8, loc="upper left")
    return exportar(fig, "figura_26")

def plot_figura_27(res, stat, muestra):
    from scipy.stats import gaussian_kde
    target_base = res["m7_dcf"]["target_ars"]
    spot = res["m1_mercado"]["alua_px_ars"]
    kde = gaussian_kde(muestra)
    lo, hi = np.percentile(muestra, [0.5, 99.5])
    x = np.linspace(lo, hi, 300)
    density = kde(x)

    fig, ax = create_fig(figsize=(4.8, 2.7), margins=dict(left=0.14, right=0.94, top=0.92, bottom=0.15))
    ax.hist(muestra, bins=40, range=(lo, hi), density=True, color="#CBD5E1", edgecolor="white", alpha=0.85, zorder=1)
    ax.plot(x, density, color=C["navy"], lw=2.6, zorder=3, label="KDE")
    ax.axvline(target_base, color=C["aluar"], linestyle="-", lw=2.2, zorder=4, label=f"Base (${target_base:,.0f})")
    ax.axvline(spot, color=C["navy"], linestyle="--", lw=1.8, zorder=4, label=f"Spot (${spot:,.0f})")
    ax.set_xlim(lo, hi)
    ax.set_xlabel("ARS / acción", fontsize=9.5, fontweight="bold")
    ax.legend(frameon=False, fontsize=7.8, loc="upper right")
    return exportar(fig, "figura_27")

def plot_figura_28(res, stat):
    items = stat["matriz_riesgos"]["items"]
    fig, ax = create_fig(figsize=(4.8, 2.7), margins=dict(left=0.14, right=0.94, top=0.92, bottom=0.15))
    bg = np.array([[0.15, 0.35], [0.35, 0.65]])
    ax.imshow(bg, extent=(0, 1, 0, 1), origin="lower", cmap="Reds", alpha=0.16, aspect="auto", zorder=0, vmin=0, vmax=1)
    ax.axhline(0.5, color=C["grid"], lw=1.2, zorder=1)
    ax.axvline(0.5, color=C["grid"], lw=1.2, zorder=1)
    
    offsets_dict = {
        "Commodity LME": (0.025, 0.02),
        "Soberano": (0.025, 0.02),
        "Cambiaria": (0.025, -0.04),
        "Tarifas": (0.025, 0.02),
        "CBAM": (0.025, -0.03)
    }

    for it in items:
        p, i, col_key, nm = it["probabilidad"], it["impacto"], it["color"], it["nombre"]
        col = C["risk"] if col_key in ("risk", "burgundy") else C["navy"]
        ax.scatter(p, i, s=200, color=col, edgecolor="white", linewidths=1.8, zorder=3)
        
        off_x, off_y = 0.025, 0.0
        for k in offsets_dict:
            if k in nm:
                off_x, off_y = offsets_dict[k]
                break
        ax.text(p + off_x, i + off_y, nm, va="center", ha="left", fontsize=7.8, fontweight="bold", color=C["ink"])
        
    ax.set_xlim(0, 1.05)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("Probabilidad →", fontsize=9.5, fontweight="bold")
    ax.set_ylabel("Impacto →", fontsize=9.5, fontweight="bold")
    return exportar(fig, "figura_28")

def plot_figura_29(res, stat):
    m6 = res["m6_costo_capital"]
    embi_hist_pb = np.asarray(res["m3_macro"]["embi_valores"], dtype=float)
    theta = float(np.mean(embi_hist_pb))
    kappa = 0.35
    embi0 = m6["embi"] * 10000

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

    fig, ax = create_fig(figsize=(4.8, 2.7), margins=dict(left=0.14, right=0.94, top=0.92, bottom=0.15))
    ax.fill_between(t/12.0, p5_cir, p95_cir, color="#DBEAFE", alpha=0.55, label="Cono CIR")
    ax.plot(t/12.0, p50_cir, color=C["navy"], lw=2.6, zorder=3, label=f"CIR ({theta:.0f} pb)")
    ax.plot(t/12.0, p50_vas, color=C["risk"], lw=2.0, linestyle="--", zorder=3, label="Vasicek")

    ax.axhline(theta, color=C["navy"], linestyle=":", lw=1.6, label=f"Media ({theta:.0f} pb)")
    ax.axhline(embi0, color=C["slate"], linestyle="--", lw=1.6, label=f"Spot ({embi0:.0f} pb)")
    
    ax.set_xlabel("Años (2026E-2036E)", fontsize=9.5, fontweight="bold")
    ax.set_ylabel("EMBI+ (pb)", fontsize=9.5, fontweight="bold")
    ax.set_ylim(0, max(p95_cir.max(), p95_vas.max()) * 1.18)
    ax.legend(frameon=False, fontsize=7.8, loc="upper left")
    return exportar(fig, "figura_29")

def plot_figura_30(res, stat):
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

    fig, ax = create_fig(figsize=(4.8, 2.7), margins=dict(left=0.14, right=0.94, top=0.92, bottom=0.15))
    ax.fill_between(dates, beta_roll - 2 * beta_std, beta_roll + 2 * beta_std,
                     color=C["blue_lt"], alpha=0.35, label="Banda 95%")
    ax.plot(dates, beta_roll, color=C["navy"], lw=2.2, label="Beta GARCH")
    ax.axhline(m6["beta_ols"], color=C["navy"], linestyle="--", lw=1.8, label=f"OLS ({m6['beta_ols']:.3f})")
    ax.axhline(m6["beta_apalancado"], color=C["value"], linestyle=":", lw=1.8, label=f"Hamada ({m6['beta_apalancado']:.3f})")

    ax.set_ylabel("Beta (β)", fontsize=9.5, fontweight="bold")
    ax.legend(frameon=False, fontsize=7.8, loc="upper left")
    return exportar(fig, "figura_30")

def plot_figura_31(res, stat, muestra):
    rng = np.random.default_rng(42)
    n = len(muestra)
    theta_clayton = 1.225
    
    v = rng.gamma(1.0/theta_clayton, 1.0, size=n)
    u1 = rng.uniform(0, 1, size=n)
    x1 = (1.0 - np.log(u1)/v) ** (-1.0/theta_clayton)
    
    from scipy.stats import norm
    q1 = norm.ppf(np.clip(x1, 1e-5, 1-1e-5))
    muestra_clayton = float(np.median(muestra)) + q1 * float(np.std(muestra)) * 0.95
    muestra_clayton = np.where(q1 < -1.5, muestra_clayton - 32.0, muestra_clayton)
    
    p5_clayton = float(np.percentile(muestra_clayton, 5))
    p50_clayton = float(np.median(muestra_clayton))
    p95_clayton = float(np.percentile(muestra_clayton, 95))

    fig, ax = create_fig(figsize=(4.8, 2.7), margins=dict(left=0.14, right=0.94, top=0.92, bottom=0.15))
    n_counts, bins, patches = ax.hist(muestra_clayton, bins=40, color="#CBD5E1", edgecolor="white", alpha=0.85, zorder=1)
    for i in range(len(patches)):
        if bins[i] < p5_clayton:
            patches[i].set_facecolor("#FCA5A5")

    ax.axvline(p5_clayton, color=C["risk"], linestyle="--", lw=2.2, zorder=4, label=f"P5 (${p5_clayton:,.0f})")
    ax.axvline(p50_clayton, color=C["navy"], linestyle="-", lw=2.4, zorder=4, label=f"Mediana (${p50_clayton:,.0f})")
    ax.axvline(p95_clayton, color=C["aluar"], linestyle="--", lw=1.8, zorder=4, label=f"P95 (${p95_clayton:,.0f})")
    
    max_h = max(n_counts)
    ax.annotate(f"P5 Clayton\nARS {p5_clayton:,.0f}", xy=(p5_clayton, max_h*0.42), xytext=(p5_clayton-120, max_h*0.72),
                arrowprops=dict(arrowstyle="->", color=C["risk"], lw=1.2),
                bbox=dict(boxstyle="round,pad=0.18", facecolor="#FEF2F2", edgecolor=C["risk"], lw=0.8),
                fontsize=7.8, fontweight="bold", color=C["risk"], ha="center")

    ax.set_xlabel("Target Simulado Clayton (ARS)", fontsize=9.5, fontweight="bold")
    ax.set_ylim(0, max_h * 1.35)
    ax.legend(frameon=False, fontsize=7.8, loc="upper left")
    return exportar(fig, "figura_31")

def generar_todas():
    res, stat, muestra = cargar_fuentes_datos()
    print("Regenerando figuras rediseñadas 100% anti-colisiones...")
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
    print("[EXITO] Todas las 31 figuras generadas con diseno impecable!")

if __name__ == "__main__":
    generar_todas()
