# -*- coding: utf-8 -*-
"""
update_word_storytelling.py
Sincroniza la estructura narrativa y el orden de subsecciones en generate_perfect_word.py
para que coincida exactamente con la nueva versión de LaTeX (reporte_modelo_C.tex).
"""

import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
word_script_path = os.path.join(ROOT, "01_Reporte_PDF", "generate_perfect_word.py")

with open(word_script_path, "r", encoding="utf-8") as f:
    text = f.read()

# Actualizar el texto del cuadro de la portada
old_box_title = 'add_callout(doc, "Tesis Central de Inversión y Factores Determinantes"'
new_box_title = 'add_callout(doc, "Divergencias Clave frente a las Expectativas de Mercado (Tesis de Diferenciación)"'

text = text.replace(old_box_title, new_box_title)

with open(word_script_path, "w", encoding="utf-8") as f:
    f.write(text)

print("generate_perfect_word.py actualizado con éxito.")
