# -*- coding: utf-8 -*-
"""
build_master_encyclopedia.py
Compilador Maestro del Tratado Enciclopedico de Valuacion y Manual de Estudio Aluar.
Importa los modulos de contenido y compila en XeLaTeX a alta resolucion.
"""

import os
import sys
import subprocess
from modules import (
    part01_estrategico,
    part02_contabilidad,
    part03_costo_capital,
    part04_dcf_valuacion,
    part05_estocastico_copulas,
    part06_riesgo_evt,
    part07_portafolio_multiplos,
    part08_econometria,
    part09_arquitectura_software,
    part10_marco_regulatorio,
    part11_banco_preguntas,
    part12_bibliografia,
)

TEX_FILE = "GUIA_DE_ESTUDIO_ALUAR.tex"
PDF_FILE = "GUIA_DE_ESTUDIO_ALUAR.pdf"

PREAMBLE = r"""\documentclass[10pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[spanish,es-nodecimaldot]{babel}
\usepackage[margin=1.75cm,top=2.0cm,bottom=2.0cm,headheight=14pt]{geometry}
\usepackage{amsmath,amssymb,amsfonts,amsthm}
\usepackage{cancel}
\usepackage{mathrsfs}
\usepackage{fontspec}
\usepackage{tcolorbox}
\tcbuselibrary{skins,breakable}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{array}
\usepackage{longtable}
\usepackage{graphicx}
\usepackage{float}
\usepackage{caption}
\usepackage{fancyhdr}
\usepackage{setspace}
\usepackage{hyperref}
\usepackage{xcolor}

\setmainfont{Georgia}
\setsansfont{Arial}
\setmonofont{Consolas}[Scale=0.88]

\definecolor{primary}{RGB}{10, 37, 64}
\definecolor{secondary}{RGB}{0, 128, 128}
\definecolor{accent}{RGB}{200, 16, 46}
\definecolor{darkgray}{RGB}{45, 55, 72}
\definecolor{lightgray}{RGB}{247, 250, 252}
\definecolor{boxbg}{RGB}{240, 245, 250}
\definecolor{boxborder}{RGB}{10, 37, 64}
\definecolor{codegray}{RGB}{245, 247, 250}

\hypersetup{
    colorlinks=true,
    linkcolor=primary,
    citecolor=secondary,
    urlcolor=secondary
}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\color{primary}\textbf{ALUAR S.A.I.C. | Tratado Enciclopedico de Valuacion y Defensa}}
\fancyhead[R]{\small\color{darkgray}\textit{Catedra EyTB -- FCE UNCuyo}}
\fancyfoot[L]{\footnotesize\color{darkgray}Valuacion Financiera y Econometrica Avanzada}
\fancyfoot[R]{\small\thepage}
\renewcommand{\headrulewidth}{0.6pt}
\renewcommand{\footrulewidth}{0.4pt}

\setstretch{1.04}
\setlength{\parskip}{4.5pt}
\setlength{\parindent}{0pt}

\theoremstyle{definition}
\newtheorem{teorema}{\color{primary}\textbf{Teorema}}[section]
\newtheorem{proposicion}{\color{primary}\textbf{Proposicion}}[section]
\newtheorem{definicion}{\color{primary}\textbf{Definicion}}[section]

\newtcolorbox{conceptbox}[2][]{
    enhanced,
    breakable,
    colback=boxbg,
    colframe=primary,
    fonttitle=\bfseries\color{white},
    title={Fundamento y Racionalidad Economica: #2},
    coltitle=white,
    sharp corners,
    boxrule=0.8pt,
    top=3mm,bottom=3mm,left=3mm,right=3mm,
    #1
}

\newtcolorbox{examquestion}[2][]{
    enhanced,
    breakable,
    colback=lightgray,
    colframe=secondary,
    fonttitle=\bfseries\color{white},
    title={Pregunta de Mesa de Examen: #2},
    coltitle=white,
    sharp corners,
    boxrule=0.8pt,
    top=3mm,bottom=3mm,left=3mm,right=3mm,
    #1
}

\newtcolorbox{codebox}[2][]{
    enhanced,
    breakable,
    colback=codegray,
    colframe=darkgray,
    fonttitle=\bfseries\color{white},
    title={Modulo Cuantitativo: #2},
    coltitle=white,
    sharp corners,
    boxrule=0.8pt,
    top=3mm,bottom=3mm,left=3mm,right=3mm,
    #1
}

\begin{document}

\begin{titlepage}
    \centering
    \vspace*{1.0cm}
    {\Huge\textbf{\color{primary}Tratado Enciclopedico de Valuacion,}}\\[0.3cm]
    {\Huge\textbf{\color{primary}Econometria y Teoria Financiera}}\\[0.6cm]
    {\Large\textbf{\color{secondary}Manual Integral de Estudio, Demostraciones Formales y Defensa Oral de Grado}}\\[0.4cm]
    {\large\textbf{\color{darkgray}Analisis Exhaustivo de Aluar Aluminio Argentino S.A.I.C. (BYMA: ALUA)}}\\[1.5cm]

    \begin{tcolorbox}[colback=boxbg,colframe=primary,sharp corners,boxrule=1pt,width=0.92\linewidth]
        \centering
        \textbf{\color{primary}Catedra de Evaluacion y Tributacion de Bases (EyTB)}\\[0.15cm]
        \textbf{Facultad de Ciencias Economicas -- Universidad Nacional de Cuyo (UNCuyo)}\\[0.25cm]
        \textit{Estructura Curricular y Rigor Academico: Tratado Tecnico para Examen de Grado}\\[0.15cm]
        \textbf{Periodo de Cobertura:} 2026E--2030E | \textbf{Horizonte de Mercado:} 10 Anos (2016--2026)
    \end{tcolorbox}

    \vspace{1.5cm}

    \begin{minipage}[t]{0.45\linewidth}
        \textbf{\color{primary}Dictamen del Modelo DCF:} COMPRAR\\
        \textbf{\color{primary}Target Base DCF:} ARS 1.235,51 (+25,8\%)\\
        \textbf{\color{primary}Target con Opcion Real:} ARS 1.255,11 (+27,8\%)\\
        \textbf{\color{primary}Precio Spot de Mercado:} ARS 982,00\\
        \textbf{\color{primary}Costo de Capital (WACC):} 7,06\% Dolarizado
    \end{minipage}\hfill
    \begin{minipage}[t]{0.45\linewidth}
        \textbf{\color{primary}Simulacion Monte Carlo:} 20.000 Trayectorias\\
        \textbf{\color{primary}Distribucion de Retornos:} Student-$t$ ($\nu=4,2$)\\
        \textbf{\color{primary}Dependencia No Lineal:} Copula de Clayton ($\lambda_L=0,38$)\\
        \textbf{\color{primary}Riesgo Extremo:} EVT-GPD ($VaR_{99\%} = -10,44\%$)\\
        \textbf{\color{primary}Dimensionamiento:} Half-Kelly (Tope 20,0\%)
    \end{minipage}

    \vfill
    {\large\color{darkgray}\textbf{Mendoza, Republica Argentina -- Agosto de 2026}}
\end{titlepage}

\tableofcontents
\clearpage
"""

POSTAMBLE = r"""
\end{document}
"""

def generate_tex():
    parts = [
        part01_estrategico.get_content(),
        part02_contabilidad.get_content(),
        part03_costo_capital.get_content(),
        part04_dcf_valuacion.get_content(),
        part05_estocastico_copulas.get_content(),
        part06_riesgo_evt.get_content(),
        part07_portafolio_multiplos.get_content(),
        part08_econometria.get_content(),
        part09_arquitectura_software.get_content(),
        part10_marco_regulatorio.get_content(),
        part11_banco_preguntas.get_content(),
        part12_bibliografia.get_content(),
    ]
    
    full_content = PREAMBLE + "\n".join(parts) + POSTAMBLE
    with open(TEX_FILE, "w", encoding="utf-8") as f:
        f.write(full_content)
    print(f"[1/2] Archivo {TEX_FILE} generado exitosamente ({len(full_content)} bytes).")

def compile_pdf():
    print("[2/2] Compilando 2 pasadas de XeLaTeX...")
    for p in range(1, 3):
        res = subprocess.run(
            ["xelatex", "-interaction=nonstopmode", TEX_FILE],
            capture_output=True,
            text=True
        )
        if res.returncode != 0:
            print(f"Error en pasada {p}: {res.stderr[:500]}")
            # print stdout tail
            tail = "\n".join(res.stdout.splitlines()[-30:])
            print(f"Stdout tail:\n{tail}")
            sys.exit(1)
        print(f"  Pasada {p}/2 completada.")
    
    if os.path.exists(PDF_FILE):
        size_mb = os.path.getsize(PDF_FILE) / (1024 * 1024)
        print(f"[EXITO] PDF compilado: {PDF_FILE} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    generate_tex()
    compile_pdf()
