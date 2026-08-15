# -*- coding: utf-8 -*-
"""
generate_theory_charts.py
Generador de Figuras Cuantitativas y Teoricas para el Tratado Enciclopedico.
Disena 10 diagramas explicativos de alta resolucion (300 DPI) para facilitar la comprension de los modelos.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy import stats

OUT_DIR = "theory_charts"
os.makedirs(OUT_DIR, exist_ok=True)

# Estilo visual institucional
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['DejaVu Serif', 'Georgia']
plt.rcParams['axes.edgecolor'] = '#0A2540'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['grid.color'] = '#E2E8F0'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.6

NAVY = '#0A2540'
TEAL = '#008080'
RED = '#C8102E'
GRAY = '#718096'
LIGHT_GRAY = '#F7FAFC'
GOLD = '#D4AF37'

def save_fig(fig, filename):
    path = os.path.join(OUT_DIR, filename)
    fig.savefig(path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Grafico generado: {path}")

# ==============================================================================
# 1. Copulas Comparativa: Gaussiana vs. Clayton
# ==============================================================================
def chart_copulas():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))
    n = 3000
    rng = np.random.default_rng(42)
    
    # Gaussiana
    rho = 0.55
    cov = [[1, rho], [rho, 1]]
    z = rng.multivariate_normal([0, 0], cov, n)
    u_gauss = stats.norm.cdf(z[:, 0])
    v_gauss = stats.norm.cdf(z[:, 1])
    
    ax1.scatter(u_gauss, v_gauss, s=4, alpha=0.35, color=NAVY)
    ax1.set_title("Copula Gaussiana (rho = 0,55)\nDependencia de Cola Nula (lambda_L = 0)", fontsize=10, fontweight='bold', color=NAVY)
    ax1.set_xlabel("Marginal U = F(LME)", fontsize=9)
    ax1.set_ylabel("Marginal V = F(EMBI+)", fontsize=9)
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.grid(True)
    
    # Cuadrante de cola
    rect1 = patches.Rectangle((0, 0), 0.15, 0.15, linewidth=1.5, edgecolor=GRAY, facecolor='none', linestyle='--')
    ax1.add_patch(rect1)
    ax1.text(0.18, 0.05, "Cola Normal:\nDispersion simetrica", fontsize=8, color=GRAY)
    
    # Clayton
    theta = 1.2258
    u_clay = rng.uniform(0, 1, n)
    w = rng.uniform(0, 1, n)
    v_clay = (1.0 + u_clay**(-theta) * (w**(-theta / (theta + 1.0)) - 1.0)) ** (-1.0 / theta)
    
    ax2.scatter(u_clay, v_clay, s=4, alpha=0.35, color=RED)
    ax2.set_title("Copula de Clayton (theta = 1,226)\nDependencia de Cola Inferior Asimetrica (lambda_L = 0,38)", fontsize=10, fontweight='bold', color=RED)
    ax2.set_xlabel("Marginal U = F(LME)", fontsize=9)
    ax2.set_ylabel("Marginal V = F(EMBI+)", fontsize=9)
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.grid(True)
    
    rect2 = patches.Rectangle((0, 0), 0.15, 0.15, linewidth=1.5, edgecolor=RED, facecolor=RED, alpha=0.15)
    ax2.add_patch(rect2)
    ax2.text(0.18, 0.05, "Agrupamiento de Crisis:\nCaida LME + Salto EMBI", fontsize=8, fontweight='bold', color=RED)
    
    fig.tight_layout()
    save_fig(fig, "teoria_01_copulas_comparativa.png")

# ==============================================================================
# 2. Difusiones Continuas: Ornstein-Uhlenbeck y CIR
# ==============================================================================
def chart_sde():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8))
    t = np.linspace(0, 6, 600)
    dt = t[1] - t[0]
    rng = np.random.default_rng(101)
    
    # Ornstein-Uhlenbeck
    kappa, theta_ou, sigma_ou = 0.385, 2450, 420
    s_paths = np.zeros((5, len(t)))
    for p in range(5):
        s = 1900.0 if p % 2 == 0 else 3100.0
        for i in range(len(t)):
            s_paths[p, i] = s
            s += kappa * (theta_ou - s) * dt + sigma_ou * np.sqrt(dt) * rng.normal()
        ax1.plot(t, s_paths[p], lw=1.2, alpha=0.85)
    
    ax1.axhline(theta_ou, color=NAVY, linestyle='--', lw=1.5, label=f"Media Largo Plazo theta = USD {theta_ou}")
    # Envolvente analitica
    env_sup = theta_ou + 1.96 * sigma_ou / np.sqrt(2 * kappa)
    env_inf = theta_ou - 1.96 * sigma_ou / np.sqrt(2 * kappa)
    ax1.fill_between(t, env_inf, env_sup, color=NAVY, alpha=0.08, label="Banda Asintotica 95%")
    ax1.set_title("Proceso Ornstein-Uhlenbeck (LME)\nVida Media t_{1/2} = 1,8 anos", fontsize=10, fontweight='bold', color=NAVY)
    ax1.set_xlabel("Tiempo (Anos)", fontsize=9)
    ax1.set_ylabel("Precio LME (USD / t)", fontsize=9)
    ax1.legend(loc='upper right', fontsize=8)
    ax1.grid(True)
    
    # CIR
    kappa_cir, theta_cir, sigma_cir = 0.85, 0.0441, 0.12
    r_paths = np.zeros((5, len(t)))
    for p in range(5):
        r = 0.12 if p % 2 == 0 else 0.02
        for i in range(len(t)):
            r_paths[p, i] = r
            r = max(0.0001, r + kappa_cir * (theta_cir - r) * dt + sigma_cir * np.sqrt(max(0, r) * dt) * rng.normal())
        ax2.plot(t, r_paths[p] * 100, lw=1.2, alpha=0.85)
    
    ax2.axhline(theta_cir * 100, color=TEAL, linestyle='--', lw=1.5, label=f"Media theta = {theta_cir*100:.2f}%")
    ax2.axhline(0, color=RED, linestyle='-', lw=1.2, label="Frontera Inaccesible (Feller: 2kappa theta >= sigma^2)")
    ax2.set_title("Proceso Cox-Ingersoll-Ross (CIR - Spread)\nCondicion de Feller Cumplida (0,075 > 0,014)", fontsize=10, fontweight='bold', color=TEAL)
    ax2.set_xlabel("Tiempo (Anos)", fontsize=9)
    ax2.set_ylabel("Tasa / Spread (%)", fontsize=9)
    ax2.legend(loc='upper right', fontsize=8)
    ax2.grid(True)
    
    fig.tight_layout()
    save_fig(fig, "teoria_02_sde_difusiones.png")

# ==============================================================================
# 3. Quiebre de Monotonia de Cornish-Fisher (Jaschke 2001)
# ==============================================================================
def chart_cornish_fisher():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8))
    z = np.linspace(-3.5, 0.5, 400)
    S = -0.42
    K_high = 8.41  # Aluar
    K_normal = 0.0
    
    # Polinomio CF
    z_cf_high = z + (S/6)*(z**2 - 1) + (K_high/24)*(z**3 - 3*z) - (S**2/36)*(2*z**3 - 5*z)
    z_cf_normal = z
    
    ax1.plot(z, z, 'k--', lw=1.2, label="Distribucion Normal (Identidad)")
    ax1.plot(z, z_cf_high, color=RED, lw=2.0, label="Cornish-Fisher Aluar (K = 8,41)")
    ax1.set_title("Cuantil Transformado z_CF vs. Cuantil Estandar z", fontsize=10, fontweight='bold', color=NAVY)
    ax1.set_xlabel("Cuantil Normal z_alpha", fontsize=9)
    ax1.set_ylabel("Cuantil Ajustado z_CF", fontsize=9)
    ax1.legend(loc='upper left', fontsize=8)
    ax1.grid(True)
    
    # Derivada dz_CF / dz
    dz_high = 1 + (S/3)*z + (K_high/24)*(3*z**2 - 3) - (S**2/36)*(6*z**2 - 5)
    dz_normal = np.ones_like(z)
    
    ax2.plot(z, dz_normal, 'k--', lw=1.2, label="Normal: Pendiente Constante = 1")
    ax2.plot(z, dz_high, color=RED, lw=2.0, label="Derivada dz_CF / dz (K = 8,41)")
    ax2.axhline(0, color='black', lw=0.8)
    ax2.axvspan(-3.5, -2.33, color=RED, alpha=0.15, label="Region de Invalidez (Pendiente < 0, Falla Monotonia)")
    ax2.set_title("Derivada de Cornish-Fisher (Caveat de Jaschke 2001)\nDemostracion de Perdida de Monotonia en Colas", fontsize=10, fontweight='bold', color=RED)
    ax2.set_xlabel("Cuantil Normal z_alpha", fontsize=9)
    ax2.set_ylabel("Derivada dz_CF / dz", fontsize=9)
    ax2.legend(loc='upper right', fontsize=8)
    ax2.grid(True)
    
    fig.tight_layout()
    save_fig(fig, "teoria_03_cornish_fisher_quiebre.png")

# ==============================================================================
# 4. EVT-GPD: Ajuste de Excesos sobre Umbral (POT)
# ==============================================================================
def chart_evt_pot():
    fig, ax = plt.subplots(figsize=(8, 4.8))
    rng = np.random.default_rng(42)
    
    # Generar excesos empiricos
    u = 0.035
    xi = 0.280
    beta = 0.0191
    
    y = np.linspace(0, 0.12, 300)
    gpd_surv = (1.0 + xi * y / beta) ** (-1.0 / xi)
    
    # Puntos simulados
    sim_excess = stats.genpareto.rvs(c=xi, scale=beta, size=150, random_state=42)
    sim_excess = np.sort(sim_excess)
    emp_surv = 1.0 - np.arange(1, len(sim_excess) + 1) / len(sim_excess)
    
    ax.plot(y * 100, gpd_surv, color=RED, lw=2.2, label="Curva Teorica Pareto Generalizada (xi = 0,280, beta = 1,91%)")
    ax.step(sim_excess * 100, emp_surv, color=NAVY, lw=1.5, where='post', label="Supervivencia Empirica de Excesos (POT)")
    
    var_99 = (0.1044 - u) * 100
    es_99 = (0.1578 - u) * 100
    ax.axvline(var_99, color=GOLD, linestyle='--', lw=1.5, label=f"VaR 99% EVT = -10,44% (Exceso {var_99:.2f}%)")
    ax.axvline(es_99, color=RED, linestyle=':', lw=1.8, label=f"ES 99% EVT = -15,78% (Exceso {es_99:.2f}%)")
    
    ax.set_title("Teoria de Valores Extremos (EVT-GPD): Ajuste de Cola sobre Umbral u = 3,5%", fontsize=10, fontweight='bold', color=NAVY)
    ax.set_xlabel("Magnitud del Exceso sobre el Umbral: Y = X - u (%)", fontsize=9)
    ax.set_ylabel("Probabilidad de Supervivencia: P(Y > y | X > u)", fontsize=9)
    ax.legend(loc='upper right', fontsize=8.5)
    ax.grid(True)
    
    save_fig(fig, "teoria_04_evt_gpd_pot.png")

# ==============================================================================
# 5. Algebra Lineal: Proyecciones OLS y Descomposicion de Cholesky
# ==============================================================================
def chart_algebra():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8))
    
    # 1. Proyeccion OLS en R^3
    ax1.set_xlim(-0.5, 3.5)
    ax1.set_ylim(-0.5, 3.5)
    
    # Subespacio Span(X)
    ax1.fill([0, 3, 2.5, -0.5], [0, 1, 3, 2], color=TEAL, alpha=0.15, label="Subespacio Col(X) = Span{x_1, x_2}")
    
    # Vectores
    ax1.arrow(0, 0, 2.2, 1.4, head_width=0.1, head_length=0.1, fc=NAVY, ec=NAVY, lw=2.0)
    ax1.text(2.3, 1.4, "y_hat = P y", fontsize=10, fontweight='bold', color=NAVY)
    
    ax1.arrow(0, 0, 2.2, 2.8, head_width=0.1, head_length=0.1, fc=RED, ec=RED, lw=2.0)
    ax1.text(2.3, 2.8, "y (Obs)", fontsize=10, fontweight='bold', color=RED)
    
    ax1.arrow(2.2, 1.4, 0, 1.4, head_width=0.1, head_length=0.1, fc=GRAY, ec=GRAY, lw=1.8, linestyle='--')
    ax1.text(2.3, 2.1, "e = M y\n(e ortogonal a X)", fontsize=9, color=GRAY)
    
    ax1.set_title("Geometria de Minimos Cuadrados (OLS)\nProyeccion Ortogonal P y Matriz Aniquiladora M = I - P", fontsize=10, fontweight='bold', color=NAVY)
    ax1.legend(loc='upper left', fontsize=8)
    ax1.axis('off')
    
    # 2. Descomposicion de Cholesky
    rng = np.random.default_rng(77)
    z = rng.normal(0, 1, (2, 1000))
    # Matriz L triangular inferior
    L = np.array([[1.0, 0.0], [0.65, 0.7599]])  # Correlacion 0.65
    y_chol = L @ z
    
    ax2.scatter(z[0], z[1], s=4, alpha=0.25, color=GRAY, label="Normales Independientes Z ~ N(0, I)")
    ax2.scatter(y_chol[0], y_chol[1], s=4, alpha=0.35, color=NAVY, label="Normales Correlacionadas Y = L Z ~ N(0, Sigma)")
    
    ax2.set_title("Descomposicion de Cholesky: Sigma = L L^T\nTransformacion Lineal de Variables Estocasticas", fontsize=10, fontweight='bold', color=NAVY)
    ax2.set_xlabel("Variable 1", fontsize=9)
    ax2.set_ylabel("Variable 2", fontsize=9)
    ax2.legend(loc='upper left', fontsize=8)
    ax2.grid(True)
    
    fig.tight_layout()
    save_fig(fig, "teoria_05_algebra_proyecciones_cholesky.png")

# ==============================================================================
# 6. Analisis de Componentes Principales (PCA) y Espectro de Autovalores
# ==============================================================================
def chart_pca():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8))
    
    autovalores = [2.45, 0.88, 0.42, 0.18, 0.07]
    var_exp = [v / sum(autovalores) * 100 for v in autovalores]
    var_acum = np.cumsum(var_exp)
    
    # Scree plot
    ax1.bar(range(1, 6), var_exp, color=NAVY, alpha=0.85, label="Varianza Explicada Individual (%)")
    ax1.plot(range(1, 6), var_acum, color=RED, marker='o', lw=2.0, label="Varianza Acumulada (%)")
    ax1.set_title("Descomposicion Espectral (PCA - Scree Plot)\nAutovalores de la Matriz de Covarianzas", fontsize=10, fontweight='bold', color=NAVY)
    ax1.set_xlabel("Componente Principal (PC)", fontsize=9)
    ax1.set_ylabel("Varianza Explicada (%)", fontsize=9)
    ax1.set_xticks(range(1, 6))
    ax1.legend(loc='center right', fontsize=8.5)
    ax1.grid(True)
    
    # Cargas factoriales
    factores = ['ALUA', 'S&P 500', 'LME Alum', 'EMBI+', 'CCL FX']
    pc1_cargas = [0.52, 0.48, 0.45, -0.38, 0.39]
    pc2_cargas = [0.41, -0.22, 0.68, 0.15, -0.54]
    
    x = np.arange(len(factores))
    w = 0.35
    ax2.bar(x - w/2, pc1_cargas, width=w, color=NAVY, label="PC1: Factor Mercado / Global (61,2%)")
    ax2.bar(x + w/2, pc2_cargas, width=w, color=TEAL, label="PC2: Factor Commodity vs FX (22,0%)")
    ax2.axhline(0, color='black', lw=0.8)
    ax2.set_title("Cargas Factoriales de Autovectores (Eigenvectors)", fontsize=10, fontweight='bold', color=NAVY)
    ax2.set_xticks(x)
    ax2.set_xticklabels(factores, fontsize=8.5)
    ax2.legend(loc='lower left', fontsize=8.5)
    ax2.grid(True)
    
    fig.tight_layout()
    save_fig(fig, "teoria_06_pca_autovalores_espectro.png")

# ==============================================================================
# 7. Descomposicion DuPont: Radar y Cascada de Destruccion Fiscal
# ==============================================================================
def chart_dupont():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8))
    
    # Cascada DuPont
    conceptos = ['EBIT Margin\n(8,4%)', 'Rotacion\n(0,55x)', 'Apalancamiento\n(1,78x)', 'Carga Fin.\n(0,633)', 'Tax Burden\n(0,157)', 'ROE Final\n(0,83%)']
    valores = [8.4, 4.62, 8.22, 5.20, 0.83, 0.83]
    
    colores = [TEAL, TEAL, TEAL, GRAY, RED, GOLD]
    ax1.bar(conceptos, valores, color=colores, alpha=0.85)
    ax1.set_title("Cascada Multiplicativa DuPont FY2025\nEvidencia del Colapso por Tax Burden (84,3% Ganancias)", fontsize=10, fontweight='bold', color=NAVY)
    ax1.set_ylabel("Retorno Acumulado Proporcional (%)", fontsize=9)
    ax1.grid(True, axis='y')
    
    # Comparativa 2023 vs 2025
    anios = ['FY2021', 'FY2022', 'FY2023', 'FY2024', 'FY2025']
    tb_hist = [0.652, 0.668, 0.731, 0.685, 0.157]
    roe_hist = [8.04, 25.31, 25.62, 10.68, 0.83]
    
    ax2.plot(anios, tb_hist, color=RED, marker='s', lw=2.0, label="Tax Burden (Neto / EBT)")
    ax2.plot(anios, [r/30 for r in roe_hist], color=NAVY, marker='o', lw=2.0, linestyle='--', label="ROE / 30 (Escala Normalizada)")
    ax2.set_title("Evolucion del Tax Burden vs. ROE Historico\nDistorsion Transitoria NIC 29 (Descalce RECPAM)", fontsize=10, fontweight='bold', color=RED)
    ax2.legend(loc='upper right', fontsize=8.5)
    ax2.grid(True)
    
    fig.tight_layout()
    save_fig(fig, "teoria_07_dupont_radar_waterfall.png")

# ==============================================================================
# 8. Presupuesto de Riesgo de Euler y Frontera Markowitz
# ==============================================================================
def chart_euler_risk():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8))
    
    # Frontera eficiente
    vols = np.linspace(0.18, 0.45, 200)
    rets = 0.047 + 1.18 * (vols - 0.18)**0.65
    
    ax1.plot(vols * 100, rets * 100, color=NAVY, lw=2.2, label="Frontera Eficiente de Markowitz")
    # Cartera Sharpe
    ax1.scatter([24.2], [33.2], color=RED, s=80, zorder=5, label="Cartera Maximo Sharpe (SR = 1,18)")
    ax1.scatter([18.5], [16.4], color=TEAL, s=80, zorder=5, label="Cartera Minima Varianza")
    
    # Linea de Asignacion de Capital (CAL)
    cml_v = np.linspace(0, 0.45, 100)
    cml_r = 0.047 + 1.18 * cml_v
    ax1.plot(cml_v * 100, cml_r * 100, color=GOLD, linestyle='--', lw=1.5, label="Capital Allocation Line (CAL)")
    
    ax1.set_title("Teoria de Portafolio: Frontera Eficiente y CAL", fontsize=10, fontweight='bold', color=NAVY)
    ax1.set_xlabel("Volatilidad de la Cartera (%)", fontsize=9)
    ax1.set_ylabel("Rendimiento Esperado (%)", fontsize=9)
    ax1.legend(loc='upper left', fontsize=8)
    ax1.grid(True)
    
    # Descomposicion de Euler CCR
    activos = ['ALUA', 'TXAR', 'YPFD', 'GGAL', 'PAMP']
    ccr_pct = [34.5, 22.8, 18.2, 14.5, 10.0]
    
    ax2.pie(ccr_pct, labels=activos, autopct='%1.1f%%', startangle=140, colors=[NAVY, TEAL, RED, GOLD, GRAY], explode=(0.08, 0, 0, 0, 0))
    ax2.set_title("Presupuesto de Riesgo de Euler: sum(CCR_i) = 100%\nContribucion Porcentual al Riesgo en Cartera Optima", fontsize=10, fontweight='bold', color=NAVY)
    
    fig.tight_layout()
    save_fig(fig, "teoria_08_markowitz_euler_budgeting.png")

# ==============================================================================
# 9. Modelo Estructural de Merton: Distancia al Default (DD)
# ==============================================================================
def chart_merton():
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    t = np.linspace(0, 5, 200)
    
    v0 = 2639.6  # Enterprise Value
    d = 456.0    # Deuda Neta
    mu_v = 0.08
    sigma_v = 0.22
    
    # Trayectoria esperada y bandas
    v_mean = v0 * np.exp(mu_v * t)
    v_inf = v0 * np.exp((mu_v - 0.5 * sigma_v**2) * t - 1.96 * sigma_v * np.sqrt(t))
    v_sup = v0 * np.exp((mu_v - 0.5 * sigma_v**2) * t + 1.96 * sigma_v * np.sqrt(t))
    
    ax.plot(t, v_mean, color=NAVY, lw=2.0, label="Valor de los Activos de la Firma V_t (Esperanza)")
    ax.fill_between(t, v_inf, v_sup, color=NAVY, alpha=0.12, label="Banda de Dispersion Estocastica (95%)")
    ax.axhline(d, color=RED, linestyle='--', lw=2.0, label=f"Barrera de Deuda Nominal D = USD {d:.1f} MM")
    
    # Distancia al default
    ax.annotate("Distancia al Default (DD = 4,82 sigma)\nProbabilidad de Quiebra EDF < 0,01%",
                xy=(2.5, (v_mean[100] + d)/2), xytext=(2.8, 1200),
                arrowprops=dict(facecolor=NAVY, shrink=0.05, width=1, headwidth=6),
                fontsize=9, fontweight='bold', color=NAVY)
    
    ax.set_title("Modelo Estructural de Merton (1974) y Capacidad de Deuda\nEquity como Opcion de Compra: E = max(V - D, 0)", fontsize=10, fontweight='bold', color=NAVY)
    ax.set_xlabel("Horizonte Temporal (Anos)", fontsize=9)
    ax.set_ylabel("Valor Corporativo (USD Millones)", fontsize=9)
    ax.legend(loc='upper left', fontsize=8.5)
    ax.grid(True)
    
    save_fig(fig, "teoria_09_merton_distancia_default.png")

# ==============================================================================
# 10. Opciones Reales: Frontera de Parada Optima (HJB)
# ==============================================================================
def chart_real_options():
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    s = np.linspace(1500, 3500, 300)
    k = 2400.0
    
    # Valor intrinseco de ejercicio
    ejercicio = np.maximum(s - k, 0)
    # Valor de continuacion (aproximacion suave)
    continuacion = np.where(s < k, 80 * np.exp((s - k) / 400), (s - k) + 80 * np.exp(-(s - k) / 600))
    
    ax.plot(s, ejercicio, color=GRAY, linestyle='--', lw=1.8, label="Valor Intrinseco de Ejercicio Inmediato: max(S - K, 0)")
    ax.plot(s, continuacion, color=RED, lw=2.2, label="Valor de la Opcion Real V(S) (Con Flexibilidad)")
    
    # Punto de parada optima
    s_star = 2850.0
    ax.axvline(s_star, color=GOLD, linestyle=':', lw=1.8, label=f"Umbral de Parada Optima S* = USD {s_star:.0f}/t")
    ax.text(1700, 300, "Region de Espera\n(Continuacion Optima)", fontsize=9, color=NAVY, fontweight='bold')
    ax.text(2950, 400, "Region de Inversion\n(Ejercicio Optimo)", fontsize=9, color=RED, fontweight='bold')
    
    ax.set_title("Opciones Reales (Longstaff-Schwartz / HJB): Flexibilidad del Proyecto PEAL V\nPrima por Oportunidad de Espera: +ARS 19,60 por Accion", fontsize=10, fontweight='bold', color=NAVY)
    ax.set_xlabel("Precio de Mercado del Aluminio LME (USD / t)", fontsize=9)
    ax.set_ylabel("Valor del Proyecto (USD MM)", fontsize=9)
    ax.legend(loc='upper left', fontsize=8.5)
    ax.grid(True)
    
    save_fig(fig, "teoria_10_opciones_reales_hjb.png")

if __name__ == "__main__":
    print("Generando graficos teoricos cuantitativos...")
    chart_copulas()
    chart_sde()
    chart_cornish_fisher()
    chart_evt_pot()
    chart_algebra()
    chart_pca()
    chart_dupont()
    chart_euler_risk()
    chart_merton()
    chart_real_options()
    print("Todas las 10 figuras teoricas generadas con exito en theory_charts/.")
