# -*- coding: utf-8 -*-
"""
perfect_latex_report.py
Limpia y perfecciona tex/reporte_modelo_C.tex con:
- \texorpdfstring en títulos para eliminar advertencias de hyperref.
- CO\textsubscript{2} y delimitadores matemáticos limpios.
- Compilación de 3 pasadas sin errores ni warnings.
- Sincronización de Informe_Valuacion_Institucional_Aluar_UNCuyo.pdf e Informe_Valuacion_Aluar_VISTA_PREVIA.pdf.
"""

import os, re, subprocess, shutil

DIR = os.path.dirname(os.path.abspath(__file__))
SRC_CAMBIADO = os.path.join(DIR, "reporte_modelo_C_cambiado.tex")
DEST_TEX = os.path.join(DIR, "tex", "reporte_modelo_C.tex")

def clean_and_perfect():
    with open(SRC_CAMBIADO, "r", encoding="utf-8") as f:
        text = f.read()

    # 1. Fix titles with math for hyperref
    text = text.replace(r"\section{Supuestos Macroeconómicos, Commodity (LME) y Mecánica Operativa de Proyección ($P\times Q$)}",
                        r"\section{Supuestos Macroeconómicos, Commodity (LME) y Mecánica Operativa de Proyección \texorpdfstring{($P\times Q$)}{(P x Q)}}")
    
    text = text.replace(r"\section{Costo de Capital (WACC), Beta y Factor $\lambda$}",
                        r"\section{Costo de Capital (WACC), Beta y Factor \texorpdfstring{$\lambda$}{lambda}}")
    
    text = text.replace(r"\subsection{Fundamentación Económica del Factor $\lambda = 0,20$}",
                        r"\subsection{Fundamentación Económica del Factor \texorpdfstring{$\lambda = 0,20$}{lambda = 0,20}}")
    
    text = text.replace(r"\subsection{Secuencia del Beta en Cuatro Pasos (OLS $\to$ Blume $\to$ Hamada)}",
                        r"\subsection{Secuencia del Beta en Cuatro Pasos (OLS \texorpdfstring{$\to$}{->} Blume \texorpdfstring{$\to$}{->} Hamada)}")
    
    text = text.replace(r"\subsection{Distribución Empírica con Innovaciones t-Student ($\nu=4,2$)}",
                        r"\subsection{Distribución Empírica con Innovaciones t-Student \texorpdfstring{($\nu=4,2$)}{(nu=4,2)}}")
    
    text = text.replace(r"\subsection{Análisis de Expectativas Implícitas: Tasa Implícita del DCF Inverso (Reverse DCF) ($g^* = 0,69\%$)}",
                        r"\subsection{Análisis de Expectativas Implícitas: Tasa Implícita del DCF Inverso (Reverse DCF) \texorpdfstring{($g^* = 0,69\%$)}{(g* = 0,69\%)}}")

    # 2. Fix CO2 and math expressions inside ESG table and text
    text = text.replace(r"Huella $<4$ t CO$_2$/t Al.", r"Huella $<$\,4 t CO\textsubscript{2}/t Al.")
    text = text.replace(r"($>6.200$ empleos directos e indirectos)", r"($>$\,6.200 empleos directos e indirectos)")
    text = text.replace(r"($<4\text{ t CO}_2/\text{t Al}$)", r"($<$\,4 t CO\textsubscript{2}/t Al)")
    text = text.replace(r"($\sim 11\text{ t CO}_2/\text{t}$)", r"($\sim$\,11 t CO\textsubscript{2}/t)")
    text = text.replace(r"($>$\,USD 2.500 MM para un nuevo smelter)", r"($>$\,USD 2.500 MM para un nuevo smelter)")

    # 3. Ensure proper includegraphics relative path for tex/reporte_modelo_C.tex
    # In tex/reporte_modelo_C.tex, figure paths like ../03_Modelo_y_Codigo/figuras/figura_01.png work when compiled from 01_Reporte_PDF
    
    with open(DEST_TEX, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Estructura perfeccionada escrita en {DEST_TEX}")

    # Also update reporte_modelo_C_cambiado.tex so both are identical
    with open(SRC_CAMBIADO, "w", encoding="utf-8") as f:
        f.write(text)

    # 4. Compile with build_pdf.py
    print("Compilando con build_pdf.py (3 pasadas XeLaTeX)...")
    res = subprocess.run(["python", "build_pdf.py"], cwd=DIR, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    print(res.stdout)
    if res.returncode != 0:
        print("Error en build_pdf.py:")
        print(res.stderr)
        raise SystemExit("Fallo en compilación XeLaTeX")

    # 5. Sincronizar copias VISTA_PREVIA
    pdf_main = os.path.join(DIR, "Informe_Valuacion_Institucional_Aluar_UNCuyo.pdf")
    pdf_vista = os.path.join(DIR, "Informe_Valuacion_Aluar_VISTA_PREVIA.pdf")
    shutil.copy2(pdf_main, pdf_vista)
    print(f"Copia VISTA_PREVIA sincronizada ({os.path.getsize(pdf_vista)/1e6:.1f} MB)")

if __name__ == "__main__":
    clean_and_perfect()
