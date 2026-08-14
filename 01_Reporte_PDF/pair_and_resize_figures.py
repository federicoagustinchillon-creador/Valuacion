# -*- coding: utf-8 -*-
"""
Formateo y escalado optimo de figuras en reporte_modelo_C.tex (Sin errores de escape en regex)
"""
import re

with open("c:/Users/fedea/Valuacion/valuacion-aluar-uncuyo/01_Reporte_PDF/tex/reporte_modelo_C.tex", "r", encoding="utf-8") as f:
    text = f.read()

def make_pair(fig1, cap1, fig2, cap2, h="4.5cm"):
    return (
        "\\noindent\n"
        "\\begin{minipage}[b]{0.488\\linewidth}\n"
        "    \\centering\n"
        f"    \\includegraphics[width=\\linewidth, height={h}, keepaspectratio]{{figures_pristine/{fig1}}}\n"
        f"    \\captionof{{figure}}{{\\small {cap1}}}\n"
        "\\end{minipage}\\hfill\n"
        "\\begin{minipage}[b]{0.488\\linewidth}\n"
        "    \\centering\n"
        f"    \\includegraphics[width=\\linewidth, height={h}, keepaspectratio]{{figures_pristine/{fig2}}}\n"
        f"    \\captionof{{figure}}{{\\small {cap2}}}\n"
        "\\end{minipage}\n"
        "\\vspace{0.15cm}"
    )

# 1. Pair Figures 4 and 5
pattern_4_5 = re.compile(r'\\begin\{center\}\s*\\includegraphics\[.*?\]\{figures_pristine/figura_04\.png\}\s*\\captionof\{figure\}\{.*?\}.*?\\begin\{center\}\s*\\includegraphics\[.*?\]\{figures_pristine/figura_05\.png\}\s*\\captionof\{figure\}\{.*?\}\\end\{center\}', re.DOTALL)
text = pattern_4_5.sub(lambda m: make_pair("figura_04.png", r"Evolución del riesgo país (EMBI+ Argentina), serie 2020–2026.", "figura_05.png", r"Curva de riesgo país (EMBI+) y rendimiento implícito soberano en USD ($Rf+EMBI+$).", "4.6cm"), text)

# 2. Pair Figures 6 and 7
pattern_6_7 = re.compile(r'\\begin\{center\}\s*\\includegraphics\[.*?\]\{figures_pristine/figura_06\.png\}\s*\\captionof\{figure\}\{.*?\}.*?\\begin\{center\}\s*\\includegraphics\[.*?\]\{figures_pristine/figura_07\.png\}\s*\\captionof\{figure\}\{.*?\}\\end\{center\}', re.DOTALL)
text = pattern_6_7.sub(lambda m: make_pair("figura_06.png", r"Cotización del aluminio (LME) vs. índice del dólar (DXY), serie diaria 2016-2026.", "figura_07.png", r"Distribución de la producción global y flujos de exportación de Aluar.", "4.6cm"), text)

# 3. Pair Figures 8 and 9
pattern_8_9 = re.compile(r'\\begin\{center\}\s*\\includegraphics\[.*?\]\{figures_pristine/figura_08\.png\}\s*\\captionof\{figure\}\{.*?\}.*?\\begin\{center\}\s*\\includegraphics\[.*?\]\{figures_pristine/figura_09\.png\}\s*\\captionof\{figure\}\{.*?\}\\end\{center\}', re.DOTALL)
text = pattern_8_9.sub(lambda m: make_pair("figura_08.png", r"Escala operativa de Aluar en comparación con productores globales.", "figura_09.png", r"Participación de mercado en Argentina: Aluar vs. importaciones (2025).", "4.6cm"), text)

# 4. Pair Figures 13 and 14
pattern_13_14 = re.compile(r'\\begin\{center\}\s*\\includegraphics\[.*?\]\{figures_pristine/figura_13\.png\}\s*\\captionof\{figure\}\{.*?\}.*?\\begin\{center\}\s*\\includegraphics\[.*?\]\{figures_pristine/figura_14\.png\}\s*\\captionof\{figure\}\{.*?\}\\end\{center\}', re.DOTALL)
text = pattern_13_14.sub(lambda m: make_pair("figura_13.png", r"Secuencia de cálculo del Beta: OLS $\rightarrow$ Blume $\rightarrow$ Hamada.", "figura_14.png", r"Descomposición del WACC: Ke (con $\lambda$), Kd y ponderadores.", "4.6cm"), text)

# 5. Pair Figures 18 and 19
pattern_18_19 = re.compile(r'\\begin\{center\}\s*\\includegraphics\[.*?\]\{figures_pristine/figura_18\.png\}\s*\\captionof\{figure\}\{.*?\}.*?\\begin\{center\}\s*\\includegraphics\[.*?\]\{figures_pristine/figura_19\.png\}\s*\\captionof\{figure\}\{.*?\}\\end\{center\}', re.DOTALL)
text = pattern_18_19.sub(lambda m: make_pair("figura_18.png", r"Rangos de valuación por metodología vs. spot.", "figura_19.png", r"Mapa de calor: sensibilidad WACC y g.", "4.7cm"), text)

# 6. Pair Figures 20 and 21
pattern_20_21 = re.compile(r'\\begin\{center\}\s*\\includegraphics\[.*?\]\{figures_pristine/figura_20\.png\}\s*\\captionof\{figure\}\{.*?\}.*?\\begin\{center\}\s*\\includegraphics\[.*?\]\{figures_pristine/figura_21\.png\}\s*\\captionof\{figure\}\{.*?\}\\end\{center\}', re.DOTALL)
text = pattern_20_21.sub(lambda m: make_pair("figura_20.png", r"Distribución estocástica Monte Carlo (N=19.995).", "figura_21.png", r"DCF Inverso: tasa de crecimiento implícita en spot.", "4.7cm"), text)

# 7. Pair Figures 23 and 24
pattern_23_24 = re.compile(r'\\begin\{center\}\s*\\includegraphics\[.*?\]\{figures_pristine/figura_23\.png\}\s*\\captionof\{figure\}\{.*?\}.*?\\begin\{center\}\s*\\includegraphics\[.*?\]\{figures_pristine/figura_24\.png\}\s*\\captionof\{figure\}\{.*?\}\\end\{center\}', re.DOTALL)
text = pattern_23_24.sub(lambda m: make_pair("figura_23.png", r"Dimensionamiento por criterio de Kelly y límite de política.", "figura_24.png", r"Trayectoria del Beta Dinámico estimado por Filtro de Kalman.", "4.6cm"), text)

# 8. Pair Figures 26 and 27
pattern_26_27 = re.compile(r'\\begin\{center\}\s*\\includegraphics\[.*?\]\{figures_pristine/figura_26\.png\}\s*\\captionof\{figure\}\{.*?\}.*?\\begin\{center\}\s*\\includegraphics\[.*?\]\{figures_pristine/figura_27\.png\}\s*\\captionof\{figure\}\{.*?\}\\end\{center\}', re.DOTALL)
text = pattern_26_27.sub(lambda m: make_pair("figura_26.png", r"Simulación estocástica LME (Ornstein-Uhlenbeck).", "figura_27.png", r"Distribución del Precio Objetivo mediante DCF Estocástico Continuo.", "4.6cm"), text)

# 9. Pair Figures 29 and 30
pattern_29_30 = re.compile(r'\\begin\{center\}\s*\\includegraphics\[.*?\]\{figures_pristine/figura_29\.png\}\s*\\captionof\{figure\}\{.*?\}.*?\\begin\{center\}\s*\\includegraphics\[.*?\]\{figures_pristine/figura_30\.png\}\s*\\captionof\{figure\}\{.*?\}\\end\{center\}', re.DOTALL)
text = pattern_29_30.sub(lambda m: make_pair("figura_29.png", r"Simulación estocástica soberana (proceso CIR).", "figura_30.png", r"Evolución del Beta dinámico condicional (GARCH).", "4.6cm"), text)

# 10. Scale up standalone figures
text = re.sub(r'\\includegraphics\[height=3\.\d+cm, width=0\.\d+\\linewidth, keepaspectratio\]\{figures_pristine/figura_01\.png\}', r'\\includegraphics[width=0.88\\linewidth, height=4.8cm, keepaspectratio]{figures_pristine/figura_01.png}', text)
text = re.sub(r'\\includegraphics\[height=3\.\d+cm, width=0\.\d+\\linewidth, keepaspectratio\]\{figures_pristine/figura_02\.png\}', r'\\includegraphics[width=0.88\\linewidth, height=4.8cm, keepaspectratio]{figures_pristine/figura_02.png}', text)
text = re.sub(r'\\includegraphics\[height=3\.\d+cm, width=0\.\d+\\linewidth, keepaspectratio\]\{figures_pristine/figura_10\.png\}', r'\\includegraphics[width=0.92\\linewidth, height=5.4cm, keepaspectratio]{figures_pristine/figura_10.png}', text)
text = re.sub(r'\\includegraphics\[height=3\.\d+cm, width=0\.\d+\\linewidth, keepaspectratio\]\{figures_pristine/figura_15\.png\}', r'\\includegraphics[width=0.88\\linewidth, height=4.9cm, keepaspectratio]{figures_pristine/figura_15.png}', text)
text = re.sub(r'\\includegraphics\[height=3\.\d+cm, width=0\.\d+\\linewidth, keepaspectratio\]\{figures_pristine/figura_16\.png\}', r'\\includegraphics[width=0.88\\linewidth, height=4.8cm, keepaspectratio]{figures_pristine/figura_16.png}', text)
text = re.sub(r'\\includegraphics\[height=3\.\d+cm, width=0\.\d+\\linewidth, keepaspectratio\]\{figures_pristine/figura_22\.png\}', r'\\includegraphics[width=0.88\\linewidth, height=4.8cm, keepaspectratio]{figures_pristine/figura_22.png}', text)
text = re.sub(r'\\includegraphics\[height=3\.\d+cm, width=0\.\d+\\linewidth, keepaspectratio\]\{figures_pristine/figura_25\.png\}', r'\\includegraphics[width=0.88\\linewidth, height=4.8cm, keepaspectratio]{figures_pristine/figura_25.png}', text)
text = re.sub(r'\\includegraphics\[height=3\.\d+cm, width=0\.\d+\\linewidth, keepaspectratio\]\{figures_pristine/figura_28\.png\}', r'\\includegraphics[width=0.88\\linewidth, height=4.8cm, keepaspectratio]{figures_pristine/figura_28.png}', text)
text = re.sub(r'\\includegraphics\[height=3\.\d+cm, width=0\.\d+\\linewidth, keepaspectratio\]\{figures_pristine/figura_31\.png\}', r'\\includegraphics[width=0.88\\linewidth, height=4.8cm, keepaspectratio]{figures_pristine/figura_31.png}', text)

with open("c:/Users/fedea/Valuacion/valuacion-aluar-uncuyo/01_Reporte_PDF/tex/reporte_modelo_C.tex", "w", encoding="utf-8") as f:
    f.write(text)

print("Actualizado correctamente reporte_modelo_C.tex con figuras pareadas.")
