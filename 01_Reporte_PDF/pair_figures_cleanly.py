# -*- coding: utf-8 -*-
"""
Script para emparejar figuras lado a lado de forma exacta y limpia en reporte_modelo_C.tex
"""
import re

with open("c:/Users/fedea/Valuacion/valuacion-aluar-uncuyo/01_Reporte_PDF/tex/reporte_modelo_C.tex", "r", encoding="utf-8") as f:
    text = f.read()

# Pair 1: Figures 4 and 5 in Macro Section
# Let's find figure 4 and 5 blocks
p_fig45 = r"""\begin{center}
\includegraphics[height=3.8cm, width=0.72\linewidth, keepaspectratio]{figures_pristine/figura_04.png}
\captionof{figure}{Evolución del riesgo país (EMBI+ Argentina), serie 2020–2026.}
\end{center}"""

# Pair 2: Figures 8 and 9
p_fig8 = r"""\begin{center}
\includegraphics[height=3.8cm, width=0.72\linewidth, keepaspectratio]{figures_pristine/figura_08.png}
\captionof{figure}{Escala operativa de Aluar en comparación con productores globales.}
\end{center}"""

p_fig9 = r"""\begin{center}
\includegraphics[height=3.8cm, width=0.72\linewidth, keepaspectratio]{figures_pristine/figura_09.png}
\captionof{figure}{Participación de mercado en Argentina: Aluar vs. importaciones (2025).}
\end{center}"""

pair_8_9 = r"""\noindent
\begin{minipage}[b]{0.488\linewidth}
    \centering
    \includegraphics[width=\linewidth, height=4.6cm, keepaspectratio]{figures_pristine/figura_08.png}
    \captionof{figure}{\small Escala operativa vs. productores globales.}
\end{minipage}\hfill
\begin{minipage}[b]{0.488\linewidth}
    \centering
    \includegraphics[width=\linewidth, height=4.6cm, keepaspectratio]{figures_pristine/figura_09.png}
    \captionof{figure}{\small Market share en Argentina (2025).}
\end{minipage}
\vspace{0.15cm}"""

if p_fig8 in text and p_fig9 in text:
    # Replace both with pair_8_9
    text = text.replace(p_fig8, pair_8_9)
    text = text.replace(p_fig9, "")
    print("Paired Figures 8 and 9")

# Pair 3: Figures 13 and 14 in WACC Section
p_fig13 = r"""\begin{center}
\includegraphics[height=3.8cm, width=0.72\linewidth, keepaspectratio]{figures_pristine/figura_13.png}
\captionof{figure}{Secuencia de cálculo del Beta: OLS $\rightarrow$ Blume $\rightarrow$ desapalancamiento/reapalancamiento de Hamada.}
\end{center}"""

p_fig14 = r"""\begin{center}
\includegraphics[height=3.8cm, width=0.72\linewidth, keepaspectratio]{figures_pristine/figura_14.png}
\captionof{figure}{Descomposición del WACC: Ke (con $\lambda$), Kd y ponderadores de estructura de capital.}
\end{center}"""

pair_13_14 = r"""\noindent
\begin{minipage}[b]{0.488\linewidth}
    \centering
    \includegraphics[width=\linewidth, height=4.6cm, keepaspectratio]{figures_pristine/figura_13.png}
    \captionof{figure}{\small Secuencia de cálculo del Beta (Hamada).}
\end{minipage}\hfill
\begin{minipage}[b]{0.488\linewidth}
    \centering
    \includegraphics[width=\linewidth, height=4.6cm, keepaspectratio]{figures_pristine/figura_14.png}
    \captionof{figure}{\small Descomposición del WACC (7,06\%).}
\end{minipage}
\vspace{0.15cm}"""

if p_fig13 in text and p_fig14 in text:
    text = text.replace(p_fig13, pair_13_14)
    text = text.replace(p_fig14, "")
    print("Paired Figures 13 and 14")

# Pair 4: Figures 18 and 19 in Sensitivity Section
p_fig18 = r"""\begin{center}
\includegraphics[height=3.8cm, width=0.72\linewidth, keepaspectratio]{figures_pristine/figura_18.png}
\captionof{figure}{Rangos de valuación por metodología vs. precio de mercado spot (ARS 982,50).}
\end{center}"""

p_fig19 = r"""\begin{center}
\includegraphics[height=3.8cm, width=0.72\linewidth, keepaspectratio]{figures_pristine/figura_19.png}
\captionof{figure}{Mapa de calor: sensibilidad del precio objetivo ante variaciones de WACC y g.}
\end{center}"""

pair_18_19 = r"""\noindent
\begin{minipage}[b]{0.488\linewidth}
    \centering
    \includegraphics[width=\linewidth, height=4.7cm, keepaspectratio]{figures_pristine/figura_18.png}
    \captionof{figure}{\small Rangos de valuación vs. spot.}
\end{minipage}\hfill
\begin{minipage}[b]{0.488\linewidth}
    \centering
    \includegraphics[width=\linewidth, height=4.7cm, keepaspectratio]{figures_pristine/figura_19.png}
    \captionof{figure}{\small Mapa de calor de sensibilidad WACC y g.}
\end{minipage}
\vspace{0.15cm}"""

if p_fig18 in text and p_fig19 in text:
    text = text.replace(p_fig18, pair_18_19)
    text = text.replace(p_fig19, "")
    print("Paired Figures 18 and 19")

# Pair 5: Figures 20 and 21 in Monte Carlo Section
p_fig20 = r"""\begin{center}
\includegraphics[height=3.8cm, width=0.72\linewidth, keepaspectratio]{figures_pristine/figura_20.png}
\captionof{figure}{Distribución estocástica del precio objetivo (Monte Carlo, N=19.995 corridas válidas).}
\end{center}"""

p_fig21 = r"""\begin{center}
\includegraphics[height=3.8cm, width=0.72\linewidth, keepaspectratio]{figures_pristine/figura_21.png}
\captionof{figure}{DCF Inverso: tasa de crecimiento perpetuo implícita en la cotización spot.}
\end{center}"""

pair_20_21 = r"""\noindent
\begin{minipage}[b]{0.488\linewidth}
    \centering
    \includegraphics[width=\linewidth, height=4.7cm, keepaspectratio]{figures_pristine/figura_20.png}
    \captionof{figure}{\small Distribución estocástica Monte Carlo.}
\end{minipage}\hfill
\begin{minipage}[b]{0.488\linewidth}
    \centering
    \includegraphics[width=\linewidth, height=4.7cm, keepaspectratio]{figures_pristine/figura_21.png}
    \captionof{figure}{\small DCF Inverso: crecimiento implícito en spot.}
\end{minipage}
\vspace{0.15cm}"""

if p_fig20 in text and p_fig21 in text:
    text = text.replace(p_fig20, pair_20_21)
    text = text.replace(p_fig21, "")
    print("Paired Figures 20 and 21")

# Pair 6: Figures 26 and 27 in Stochastic DCF Section
p_fig26 = r"""\begin{center}
\includegraphics[height=3.8cm, width=0.72\linewidth, keepaspectratio]{figures_pristine/figura_26.png}
\captionof{figure}{Simulación estocástica de precios LME mediante proceso Ornstein-Uhlenbeck.}
\end{center}"""

p_fig27 = r"""\begin{center}
\includegraphics[height=3.8cm, width=0.72\linewidth, keepaspectratio]{figures_pristine/figura_27.png}
\captionof{figure}{Distribución del Precio Objetivo mediante DCF Estocástico (media: ARS 1.235,51).}
\end{center}"""

pair_26_27 = r"""\noindent
\begin{minipage}[b]{0.488\linewidth}
    \centering
    \includegraphics[width=\linewidth, height=4.6cm, keepaspectratio]{figures_pristine/figura_26.png}
    \captionof{figure}{\small Simulación LME Ornstein-Uhlenbeck.}
\end{minipage}\hfill
\begin{minipage}[b]{0.488\linewidth}
    \centering
    \includegraphics[width=\linewidth, height=4.6cm, keepaspectratio]{figures_pristine/figura_27.png}
    \captionof{figure}{\small Target DCF Estocástico Continuo.}
\end{minipage}
\vspace{0.15cm}"""

if p_fig26 in text and p_fig27 in text:
    text = text.replace(p_fig26, pair_26_27)
    text = text.replace(p_fig27, "")
    print("Paired Figures 26 and 27")

with open("c:/Users/fedea/Valuacion/valuacion-aluar-uncuyo/01_Reporte_PDF/tex/reporte_modelo_C.tex", "w", encoding="utf-8") as f:
    f.write(text)

print("Actualizado reporte_modelo_C.tex con figuras pareadas.")
