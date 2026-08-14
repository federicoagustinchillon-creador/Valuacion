# -*- coding: utf-8 -*-
"""
Script de actualizacion de figuras y enriquecimiento de analisis institucional en reporte_modelo_C.tex
"""
import re

with open("c:/Users/fedea/Valuacion/valuacion-aluar-uncuyo/01_Reporte_PDF/tex/reporte_modelo_C.tex", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Enrich Section 2 with PESTEL analysis
pestel_block = r"""
\subsubsection{Matriz PESTEL del Contexto Operativo}
\begin{table}[H]
\centering
\caption{\textbf{Resumen PESTEL: Factores Macro y de Entorno}}
\small
\begin{tabular}{p{2.5cm}p{12.0cm}}
\toprule
\textbf{Dimensión} & \textbf{Factores Clave e Implicancia para Aluar} \\
\midrule
\textbf{Político} & Ley 27.742 (RIGI) con estabilidad fiscal a 30 años y beneficios tributarios para expansiones eólicas. \\
\textbf{Económico} & Compresión del EMBI+ (441 pb), desinflación y unificación cambiaria gradual que abarata el WACC. \\
\textbf{Social} & Principal empleador privado de Puerto Madryn y motor de desarrollo de la provincia del Chubut. \\
\textbf{Tecnológico} & Digitalización de celdas electrolíticas y aerogeneradores patagónicos con factor de planta $>50\%$. \\
\textbf{Ambiental} & Certificación ASI frente al arancel europeo CBAM ($3,4\text{ t }\text{CO}_2/\text{t}$ vs $11,5\text{ t}$ promedio mundial). \\
\textbf{Legal} & Cumplimiento de normativas CNV, BYMA, estados auditados bajo IFRS/NIIF y acuerdos CAMMESA. \\
\bottomrule
\end{tabular}
\end{table}
"""

# 2. Enrich Section 3 with Porter's 5 Forces
porter_block = r"""
\subsubsection{Análisis de las Cinco Fuerzas de Porter}
\begin{table}[H]
\centering
\caption{\textbf{Evaluación Estructural de las Cinco Fuerzas de Porter en la Industria del Aluminio}}
\small
\begin{tabular}{p{3.8cm}cp{9.5cm}}
\toprule
\textbf{Fuerza Competitiva} & \textbf{Intensidad} & \textbf{Justificación Estratégica} \\
\midrule
\textbf{Poder de Proveedores} & Medio-Bajo & Alúmina contratada a largo plazo (Platts PAX). 96\% de energía propia cautiva y ánodos in situ. \\
\textbf{Poder de Compradores} & Bajo/Medio & Monopolio local en Argentina (20\% de ventas). En exportaciones (80\%) es tomador de precio LME. \\
\textbf{Amenaza de Entrantes} & Muy Baja & Barrera de capital ($>\text{USD 3.500 MM}$), falta de bloques energéticos y acceso portuario. \\
\textbf{Amenaza de Sustitutos} & Baja & Sustitutos (fibra de carbono, titanio) triplican el costo; el acero triplica el peso. \\
\textbf{Rivalidad de la Industria} & Media & Competencia global mitigada por cash cost C1 en primer cuartil mundial (USD 1.680/t). \\
\bottomrule
\end{tabular}
\end{table}
"""

# 3. Enrich Section 5 with DuPont 5-factor and Sloan Accrual
dupont_block = r"""
\subsubsection{Descomposición DuPont de 5 Factores y Calidad de Ganancias}
\begin{table}[H]
\centering
\caption{\textbf{Descomposición DuPont de 5 Factores (FY2021--FY2025)}}
\small
\begin{tabular}{lccccc}
\toprule
\textbf{Factor DuPont} & \textbf{FY2021} & \textbf{FY2022} & \textbf{FY2023} & \textbf{FY2024} & \textbf{FY2025} \\
\midrule
1. Tax Burden (Neto / EBT) & 0,652 & 0,668 & 0,731 & 0,685 & \textbf{0,157} \\
2. Interest Burden (EBT / EBIT) & 0,914 & 0,942 & 0,968 & 0,912 & \textbf{0,633} \\
3. Margen Operativo (EBIT / Ventas) & 0,092 & 0,281 & 0,303 & 0,157 & \textbf{0,084} \\
4. Rotación de Activos (Ventas / Activos) & 0,74x & 0,79x & 0,71x & 0,63x & \textbf{0,55x} \\
5. Apalancamiento (Activo / PN) & 2,00x & 1,82x & 1,68x & 1,74x & \textbf{1,78x} \\
\midrule
\textbf{ROE Resultante} & \textbf{8,04\%} & \textbf{25,31\%} & \textbf{25,62\%} & \textbf{10,68\%} & \textbf{0,83\%} \\
\bottomrule
\end{tabular}
\end{table}
\noindent
\textbf{Calidad de Ganancias (Ratio de Devengamientos de Sloan):} El ratio de devengamientos sobre flujo de caja de Aluar en FY2025 es negativo (\textbf{-0,064}), demostrando que el bajo resultado contable reportado (\$9,17 MM) respondió al ajuste impositivo no monetario de NIC 29 y no a una pérdida de generación real de flujo operativo (\$148,2 MM de FCO).
"""

# Insert institutional blocks if not already present
if "Matriz PESTEL del Contexto Operativo" not in text:
    text = text.replace(r"\section{Dinámica Global del Mercado de Aluminio (LME)}", pestel_block + "\n" + r"\section{Dinámica Global del Mercado de Aluminio (LME)}")

if "Análisis de las Cinco Fuerzas de Porter" not in text:
    text = text.replace(r"\section{Operaciones, Costos C1 y Matriz Energética}", porter_block + "\n" + r"\section{Operaciones, Costos C1 y Matriz Energética}")

if "Descomposición DuPont de 5 Factores" not in text:
    text = text.replace(r"\section{Modelo WACC y Descomposición del Beta}", dupont_block + "\n" + r"\section{Modelo WACC y Descomposición del Beta}")

with open("c:/Users/fedea/Valuacion/valuacion-aluar-uncuyo/01_Reporte_PDF/tex/reporte_modelo_C.tex", "w", encoding="utf-8") as f:
    f.write(text)

print("Actualizado reporte_modelo_C.tex con bloques de analisis institucional.")
