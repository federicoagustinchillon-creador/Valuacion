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

import fitz  # PyMuPDF

DIR = os.path.dirname(os.path.abspath(__file__))
TEX_DIR = os.path.join(DIR, "tex")
TEX_FILE = os.path.join("tex", "reporte_valuacion.tex")
OUTPUT_NAME = "Informe_Valuacion_Aluar_UNCuyo.pdf"


def fix_tounicode_semicolon(path):
    """dvipdfmx mapea el punto y coma de Georgia a U+037E (signo griego visualmente
    identico). Corrige solo el CMap ToUnicode para que el texto extraido/copiado
    use U+003B; los glifos y el render no cambian."""
    doc = fitz.open(path)
    seen = set()
    for i in range(doc.page_count):
        for f in doc.get_page_fonts(i, full=True):
            xref = f[0]
            if xref in seen:
                continue
            seen.add(xref)
            tu = doc.xref_get_key(xref, "ToUnicode")
            if tu[0] != "xref":
                continue
            tux = int(tu[1].split()[0])
            data = doc.xref_stream(tux)
            new = data.replace(b" <037E>", b" <003B>")
            if new != data:
                doc.update_stream(tux, new)
    tmp = path + ".tmp"
    doc.save(tmp, garbage=0, deflate=True)
    doc.close()
    shutil.move(tmp, path)


def run_pass(n):
    print(f"[xelatex] pasada {n}/3...")
    result = subprocess.run(
        ["xelatex", "-interaction=batchmode", "-halt-on-error",
         f"-output-directory={TEX_DIR}", TEX_FILE],
        cwd=DIR, capture_output=False
    )
    if result.returncode != 0:
        raise SystemExit(f"[ERROR] xelatex falló en la pasada {n} (exit {result.returncode}).")


def main():
    if shutil.which("xelatex") is None:
        raise SystemExit("[ERROR] xelatex no está en PATH. Instalá MiKTeX o TeX Live.")

    # Limpiar auxiliares previos tanto en DIR como en TEX_DIR para sincronizar TOC de forma limpia
    for d in (DIR, TEX_DIR):
        for ext in (".toc", ".aux", ".out", ".log", ".synctex.gz"):
            p = os.path.join(d, "reporte_valuacion" + ext)
            if os.path.exists(p):
                try:
                    os.remove(p)
                except OSError:
                    pass

    for n in (1, 2, 3):
        run_pass(n)

    compiled = os.path.join(TEX_DIR, "reporte_valuacion.pdf")
    if not os.path.exists(compiled):
        raise SystemExit("[ERROR] xelatex terminó sin errores pero no generó el PDF esperado.")

    final_path = os.path.join(DIR, OUTPUT_NAME)
    shutil.copy2(compiled, final_path)
    fix_tounicode_semicolon(final_path)
    size_mb = os.path.getsize(final_path) / 1e6
    print(f"[EXITO] {OUTPUT_NAME} generado ({size_mb:.1f} MB).")


if __name__ == "__main__":
    main()

