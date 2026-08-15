# -*- coding: utf-8 -*-
"""
build_pdf.py -- Compila tex/reporte_valuacion.tex a Informe_Valuacion_Aluar_UNCuyo.pdf
con XeLaTeX, 3 pasadas (necesarias para resolver el índice y las referencias cruzadas).

El documento usa \\usepackage{fontspec} con Georgia (vía \\setmainfont) para los títulos y el
cuerpo con tipografía profesional. Requiere una instalación de XeLaTeX en PATH (MiKTeX o TeX Live).

Uso:
    python build_pdf.py
"""
import os
import subprocess
import shutil
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
TEX_DIR = os.path.join(DIR, "tex")
TEX_FILE = os.path.join("tex", "reporte_valuacion.tex")
OUTPUT_NAME = "Informe_Valuacion_Aluar_UNCuyo.pdf"


def run_pass(n):
    print(f"[xelatex] pasada {n}/3...")
    result = subprocess.run(
        ["xelatex", "-interaction=nonstopmode", "-halt-on-error",
         f"-output-directory={TEX_DIR}", TEX_FILE],
        cwd=DIR, capture_output=True, text=True
    )
    if result.returncode != 0:
        print(result.stdout[-3000:])
        print(result.stderr[-2000:])
        raise SystemExit(f"[ERROR] xelatex falló en la pasada {n} (exit {result.returncode}).")


def main():
    if shutil.which("xelatex") is None:
        raise SystemExit("[ERROR] xelatex no está en PATH. Instalá MiKTeX o TeX Live.")

    for n in (1, 2, 3):
        run_pass(n)

    compiled = os.path.join(TEX_DIR, "reporte_valuacion.pdf")
    if not os.path.exists(compiled):
        raise SystemExit("[ERROR] xelatex terminó sin errores pero no generó el PDF esperado.")

    final_path = os.path.join(DIR, OUTPUT_NAME)
    shutil.copy2(compiled, final_path)
    size_mb = os.path.getsize(final_path) / 1e6
    print(f"[EXITO] {OUTPUT_NAME} generado ({size_mb:.1f} MB).")


if __name__ == "__main__":
    main()

