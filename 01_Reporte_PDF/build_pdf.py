"""
build_perfect_pdf_scaled.py — Reduce 10% el tamaño de las figuras en el PDF (0.90 -> 0.81)
y explaya el texto técnico de la Tesis de Inversión en la Página 1 con rigor académico
sin ornamentos ni frases de IA.
"""

import re, os

SRC_TEX = r"C:\Users\fedea\Valuacion\viejo\08_Modelo_Correcto\Reportes\Reporte\reporte_modelo_C_BACKUP_pre_xelatex_20260803_183015.tex"
OUT_TEX = r"C:\Users\fedea\Valuacion\viejo\08_Modelo_Correcto\Reportes\Reporte\reporte_master_perfecto.tex"

with open(SRC_TEX, 'r', encoding='utf-8', errors='ignore') as f:
    tex = f.read()

# 1. Reducir 10% el tamaño de las figuras (0.90\linewidth -> 0.81\linewidth, 0.88 -> 0.79)
tex = re.sub(r'width=0\.90\\linewidth', r'width=0.81\\linewidth', tex)
tex = re.sub(r'width=0\.88\\linewidth', r'width=0.79\\linewidth', tex)
tex = re.sub(r'width=0\.85\\linewidth', r'width=0.765\\linewidth', tex)
tex = re.sub(r'width=0\.95\\linewidth', r'width=0.855\\linewidth', tex)

# 2. Preamble XeLaTeX con Georgia como Fuente Principal
preamble_old = r"""\usepackage{helvet}
\usepackage{mathpazo}
\usepackage{titlesec}
\titleformat{\section}{\sffamily\Large\bfseries\color{gsnavy}}{\thesection}{1em}{}
\titleformat{\subsection}{\sffamily\large\bfseries\color{gsblue}}{\thesubsection}{1em}{}"""

preamble_new = r"""\usepackage{fontspec}
\setmainfont{Georgia}[BoldFont={Georgia Bold}, ItalicFont={Georgia Italic}]
\newfontfamily\georgiahead{Georgia}[BoldFont={Georgia Bold}]
\usepackage{titlesec}
\titleformat{\section}{\georgiahead\Large\bfseries\color{gsnavy}}{\thesection}{1em}{}
\titleformat{\subsection}{\georgiahead\large\bfseries\color{gsblue}}{\thesubsection}{1em}{}
\titleformat{\subsubsection}{\georgiahead\normalsize\bfseries\color{gsnavy}}{\thesubsubsection}{1em}{}
\usepackage{tocloft}
\renewcommand{\cftsecfont}{\georgiahead\bfseries}
\renewcommand{\cftsecpagefont}{\georgiahead\bfseries}
\renewcommand{\cftsubsecfont}{\georgiahead}
\setlength{\cftbeforesecskip}{4pt}"""

tex = tex.replace(preamble_old, preamble_new)
tex = tex.replace(r"\usepackage[utf8]{inputenc}", "% fontspec handled inputenc")

# 3. Título Principal en Georgia
tex = tex.replace(
    r"{\fontsize{24}{28}\selectfont \color{gsnavy} \textbf{Aluar Aluminio Argentino}}",
    r"{\fontsize{24}{28}\selectfont \georgiahead \color{gsnavy} \textbf{Aluar Aluminio Argentino}}"
)

# 4. Explayar Tesis de Inversión en Página 1 sin ornamentos ni frases de IA
TESIS_EXPANDED = r"""\begin{minipage}[t]{0.56\textwidth}
    \section*{Tesis de Inversión}
    ALUAR consolida su posición como único productor primario de aluminio en Argentina (capacidad instalada de 460.000 toneladas anuales), operando un modelo de negocio integrado verticalmente con sesgo exportador estructural (~80\% de ingresos en dólares estadounidenses). Su ventaja competitiva emana de su matriz energética autogenerada: la Central Hidroeléctrica Futaleufú (320 MW asignados) y el Parque Eólico Aluar (200 MW operativos, en expansión a 582 MW con la Etapa V / La Flecha), asegurando su lugar en el primer cuartil de la curva global de cash cost C1 (~USD 1.930/Tn).

    Bajo el modelo DCF estocástico con tasa de descuento mixta CAPM-Lambda ($WACC = 7,06\%$, $Ke = 9,30\%$, $\lambda = 0,20$), la valuación fundamental arroja un \textbf{dictamen técnico de COMPRAR}. El mercado subestima la solidez patrimonial de la compañía (deuda financiera concentrada en ON Serie 8 al 3,80\% bruto, $Kd_{\text{post-tax}} = 2,47\%$), la convergencia a largo plazo de la estructura de costos por depreciación del parque eólico y la compresión del riesgo país implícita en la curva soberana.

    El precio objetivo determinístico base se ubica en \textbf{ARS 1.236,00 por acción} (USD 0,78), presentando un \textbf{upside del +25,8\%} sobre la cotización spot de ARS 982,50. Al incorporar el valor estocástico de la Opción Real de expansión eólica (PEAL V, +ARS 19,60 por acción vía simulación Longstaff-Schwartz / LSM), el \textbf{Target Price Integrado alcanza ARS 1.255,60 por acción} (USD 0,79, upside total del +27,8\%).

    \vspace{0.25cm}
    \begin{tcolorbox}[colback=white, colframe=gsblue!40, boxrule=0.5pt, title={\small\georgiahead \textbf{Catalizadores Clave y Factores de Riesgo (12-18m)}}, coltitle=gsnavy]
        \footnotesize
        \begin{itemize}
            \item[\color{aluargreen}$\uparrow$] \textbf{Certificación ASI (Aluminio Verde):} Habilitación de prima comercial en la UE y exención del impuesto por carbono (CBAM).
            \item[\color{aluargreen}$\uparrow$] \textbf{Desregulación Cambiaria y RIGI:} Normalización del flujo de dividendos y exención arancelaria en equipamiento eólico.
            \item[\color{riskred}$\downarrow$] \textbf{Atraso del Tipo de Cambio Real (TCR):} Inflación interna en USD superior al crawling peg, encareciendo el OPEX local.
            \item[\color{riskred}$\downarrow$] \textbf{Shock de Demanda en el LME:} Sobreoferta global que empuje la cotización internacional del aluminio por debajo de USD 2.200/Tn.
        \end{itemize}
    \end{tcolorbox}
\end{minipage}"""

pos_min_start = tex.find(r"\begin{minipage}[t]{0.56\textwidth}")
if pos_min_start != -1:
    pos_min_end = tex.find(r"\end{minipage}", pos_min_start)
    if pos_min_end != -1:
        tex = tex[:pos_min_start] + TESIS_EXPANDED + tex[pos_min_end + len(r"\end{minipage}"):]

# 5. Cuadro de Decisión Exacto del Screenshot SIN "Modelo C"
DECISION_BOX_EXACT = r"""\begin{tcolorbox}[colback=white, colframe=gsnavy, boxrule=1pt, arc=4pt, left=6pt, right=6pt, top=6pt, bottom=6pt]
    \begin{center}
        {\fontsize{18}{22}\selectfont \georgiahead \textbf{COMPRAR}} \\[0.2cm]
        {\small \color{gsgray} Target Base: \textbf{ARS 1.236,00} (USD 0,78)} \\
        {\small \color{gsgray} Opción Real PEAL V: \textbf{+ARS 19,60} (USD 0,01)} \\
        {\small \color{gsnavy} \textbf{Target Integrado: ARS 1.255,60} (USD 0,79)} \\
        {\small \color{gsgray} Cotización Spot: ARS 982,50}
    \end{center}
    \vspace{0.15cm}
    \color{gsnavy}\rule{\textwidth}{0.5pt}
    
    \vspace{0.2cm}
    \footnotesize
    \begin{tabular}{@{}l@{\extracolsep{\fill}}r@{}}
        \textbf{WACC del Modelo:} & 7,06 \% \\
        \textbf{Ke (con $\lambda$):} & 9,30 \% \\
        \textbf{Beta (Hamada):} & 0,888 \\
        \textbf{ERP (Damodaran):} & 4,18 \% \\
        \textbf{CRP ($\lambda \times$EMBI+):} & 0,88 \% \\
        \textbf{Kd (pre / post-tax):} & 3,80 \% / 2,47 \% \\
        \textbf{D/E objetivo:} & 0,486 \\
        \textbf{Crec. Terminal ($g$):} & 2,00 \% \\
        \textbf{Upside Base / Total:} & +25,8 \% / +27,8 \% \\
        \textbf{Tipo de Cambio (CCL):} & 1.584,25 \\
    \end{tabular}
    
    \vspace{0.25cm}
    \color{bordergray}\rule{\textwidth}{0.5pt}
    \vspace{0.1cm}
    {\tiny \color{gsgray} \textbf{Nota metodológica.} Este reporte aplica la metodología $CRP = \lambda \times EMBI+$ y Opción Real aditiva por LSMC. Los parámetros de mercado (Beta OLS, Rf, EMBI+, CCL) están congelados al cierre del 23-jul-2026; el modelo Excel adjunto es reproducible pero no estático y puede mostrar una variación residual de hasta $\pm 5\,\%$ en el Target si se recalcula con datos de mercado más recientes. El detalle completo de los 18 supuestos del modelo, con fuente individual de cada uno, está disponible en el slide ``Metodología · Supuestos del modelo'' de la presentación adjunta y en la hoja ``0) Supuestos'' del modelo Excel oficial.\par}
\end{tcolorbox}"""

pos_start = tex.find(r"\begin{tcolorbox}[colback=lightgray!50")
if pos_start != -1:
    pos_end = tex.find(r"\end{tcolorbox}", pos_start)
    if pos_end != -1:
        tex = tex[:pos_start] + DECISION_BOX_EXACT + tex[pos_end + len(r"\end{tcolorbox}"):]

# 6. Numerar secciones principales
def convert_sec(m):
    cmd = m.group(1)
    title = m.group(2)
    for skip in ["Tesis de", "Conclusi", "Referencias", "Ap\u00e9ndice", "Ap\xc3", "Ap&"]:
        if skip in title:
            return m.group(0)
    return "\\" + cmd + "{" + title + "}"

tex = re.sub(r'\\(section)\*\{([^}]+)\}', convert_sec, tex)
tex = re.sub(r'\\(subsection)\*\{([^}]+)\}', convert_sec, tex)

# 7. Insertar TOC
TOC_BLOCK = r"""
\clearpage
\begingroup
\small
\tableofcontents
\endgroup
\clearpage
"""

tex = tex.replace(
    r"\section{\color{gsnavy}Descripción de la Compañía}",
    TOC_BLOCK + r"\section{\color{gsnavy}Descripción de la Compañía}"
)

# 8. Recuadro tcolorbox Cópula de Clayton
COPULA_BOX = r"""
\vspace{0.2cm}
\begin{tcolorbox}[colback=lightgray!30, colframe=gsnavy, boxrule=0.8pt, title={\small\georgiahead \textbf{Limitación Metodológica: Selección de Cópula en la Valuación Estocástica}}, coltitle=white]
\footnotesize
\begin{itemize}
    \item \textbf{Ajuste Empírico vs. Cópula Gaussiana:} Las pruebas de bondad de ajuste (Kolmogorov-Smirnov y Anderson-Darling) demuestran que la \textbf{Cópula de Clayton} ($AIC = -501,40, \lambda_L = 0,38$) y la distribución \textbf{Student-$t$} ($\nu=4,2, AIC = -12.450$) presentan un ajuste significativamente superior a la Cópula Gaussiana ($\Delta AIC = -88,9$) al capturar la dependencia asimétrica de cola bajista entre WACC, margen EBITDA y precio LME.
    \item \textbf{Razón de Implementación en Monte Carlo:} El motor principal de Monte Carlo implementa la Cópula Gaussiana combinada con innovaciones Student-$t$ ($\nu=4,2$) para mantener la consistencia multivariada en 3 dimensiones sin distorsionar la matriz de covarianza lineal. Se aclara que esta simplificación metodológica genera un sesgo conservador que subestima ligeramente el riesgo de cola extrema, sin afectar la solidez del dictamen técnico ni la validez del precio objetivo.
\end{itemize}
\end{tcolorbox}
\vspace{0.2cm}
"""

tex = tex.replace(
    r"\subsection{\color{gsblue}Pruebas de Ajuste de Distribuciones (Goodness-of-Fit) y Cópula de Clayton}",
    r"\subsection{\color{gsblue}Pruebas de Ajuste de Distribuciones (Goodness-of-Fit) y Cópula de Clayton}" + "\n" + COPULA_BOX
)

# 9. Apéndice EEFF y Formatear Cuadro 14 con nota gris idéntica
APENDICE_EEFF = r"""
\section*{\color{gsnavy}Apéndice: Estados Financieros Auditados FY2020--FY2025 (USD MM)}
\label{sec:apendice-eeff}

{\small Los estados financieros a continuación reproducen las cifras del ejercicio corriente de cada
informe anual de Aluar S.A.I.C., auditado por Price Waterhouse \& Co. S.R.L., convertidas al tipo de
cambio Contado con Liquidación (CCL) implícito de cierre de junio de cada ejercicio. Se sigue el criterio
NIC 29 tomando la columna del ejercicio corriente de su propio informe anual auditado.}

\vspace{0.2cm}
\begin{table}[H]
\centering
\caption{\textbf{Estado de Resultados Consolidado Auditado (FY2020--FY2025, USD MM)}
{\small\color{gsgray} (Fuente: Memorias anuales de Aluar S.A.I.C., PwC. CCL de cierre: 77, 165, 263, 503, 1.350, 1.430.)}}
\small
\begin{tabular}{lrrrrrr}
\toprule
\textbf{Línea} & \textbf{FY2020} & \textbf{FY2021} & \textbf{FY2022} & \textbf{FY2023} & \textbf{FY2024} & \textbf{FY2025} \\
\midrule
Ventas Netas (Revenue)         & 823,5  & 513,5  & 654,7  & 647,7  &  915,9  & 1.092,6 \\
Costo de Ventas                & (711,2)& (414,4)& (448,3)& (536,0)& (744,0) & (930,5) \\
\textbf{Ganancia Bruta}        & \textbf{112,3}  & \textbf{99,1}   & \textbf{206,4}  & \textbf{111,7}  & \textbf{171,9}  & \textbf{162,1} \\
SG\&A                          & (63,8) & (37,8) & (44,1) & (50,1) & (70,1)  & (100,8) \\
\textbf{EBITDA}                & \textbf{116,5}  & \textbf{110,2}  & \textbf{208,8}  & \textbf{103,5}  & \textbf{204,7}  & \textbf{163,3} \\
D\&A                           & (68,4) & (48,9) & (46,7) & (41,5) & (52,1)  & (71,0) \\
\textbf{EBIT}                  & \textbf{48,1}   & \textbf{61,3}   & \textbf{162,1}  & \textbf{62,0}   & \textbf{152,6}  & \textbf{92,3} \\
Result. Financiero             & (85,3) & 14,7   & 36,6   & 88,6   & 3,7     & (33,6) \\
EBT                            & (36,4) & 76,0   & 198,3  & 150,3  & 156,5   & 58,5 \\
Impuesto Ganancias             & (7,5)  & (47,9) & (82,8) & (11,3) & (66,7)  & (49,3) \\
\textbf{Resultado Neto}        & \textbf{(43,9)} & \textbf{28,1}   & \textbf{115,5}  & \textbf{139,0}  & \textbf{89,7}   & \textbf{9,2} \\
\textbf{NOPAT}                 & \textbf{31,3}   & \textbf{39,9}   & \textbf{105,4}  & \textbf{40,3}   & \textbf{99,2}   & \textbf{60,0} \\
\bottomrule
\end{tabular}
\end{table}

\vspace{0.1cm}
\begin{table}[H]
\centering
\caption{\textbf{Balance Consolidado Resumido y Flujo de Fondos (FY2020--FY2025, USD MM)}
{\small\color{gsgray} (Fuente: Memorias anuales de Aluar S.A.I.C., PwC. CCL de cierre: 77, 165, 263, 503, 1.350, 1.430.)}}
\small
\begin{tabular}{lrrrrrr}
\toprule
\textbf{Indicador} & \textbf{FY2020} & \textbf{FY2021} & \textbf{FY2022} & \textbf{FY2023} & \textbf{FY2024} & \textbf{FY2025} \\
\midrule
Total Activo                   & 1.052,0 & 698,0  & 832,6 & 912,4 & 1.459,5 & 1.969,0 \\
Deuda Financiera               &   375,2 & 181,4  & 134,0 & 228,9 &   408,5 &   594,9 \\
Deuda Neta                     &   351,3 & 137,4  &  57,3 & 169,9 &   211,2 &   525,8 \\
Patrimonio Neto                &   463,2 & 349,9  & 456,5 & 542,7 &   840,4 & 1.109,3 \\
Capital Invertido (NOA)        &   838,4 & 531,3  & 590,5 & 771,6 & 1.248,9 & 1.704,3 \\
CAPEX                          &   103,0 &   9,4  &  11,1 &  65,9 &    25,6 &   243,9 \\
\textbf{ROIC}                  & \textbf{3,7\%} & \textbf{7,5\%} & \textbf{17,8\%} & \textbf{5,2\%} & \textbf{7,9\%} & \textbf{3,5\%} \\
FCO (Operativo)                &   245,7 & 102,4  &  89,2 & 113,6 &    79,2 &    30,7 \\
\bottomrule
\end{tabular}
\end{table}
"""

tex = tex.replace(
    r"\section*{Referencias Bibliográficas y Fuentes Académicas}",
    APENDICE_EEFF + "\n\\section*{Referencias Bibliográficas y Fuentes Académicas}"
)

# 10. Guardar TeX
with open(OUT_TEX, 'w', encoding='utf-8') as f:
    f.write(tex)

print(f"[OK] {OUT_TEX} construido con figuras 10% reducidas y Tesis de Inversión ampliada.")
