# -*- coding: utf-8 -*-
"""
forensic_scan.py
Escaneo forense de emojis, palabras cliché de IA, placeholders y consistencia en el reporte.
"""

import os, sys, re, docx

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run_scan():
    print("================================================================================")
    print(" ESCANEO FORENSE DE CALIDAD, EMOJIS, RASTROS DE IA Y PLACEHOLDERS")
    print("================================================================================\n")
    
    emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)
    
    ai_cliches = [
        'como modelo de lenguaje', 'como ia', 'inteligencia artificial', 'chatgpt', 'openai',
        'iniciamos cobertura', 'holístico', 'sinérgico', 'de clase mundial',
        'en conclusión', 'cabe destacar que', 'es importante mencionar',
        'todo', 'tbd', 'placeholder', 'lorem ipsum', 'xxx', 'revisar aquí'
    ]
    
    files_to_check = [
        ("01_Reporte_PDF/tex/reporte_modelo_C.tex", "LaTeX Report Source"),
        ("01_Reporte_PDF/generate_perfect_word.py", "Word Generator Script"),
        ("01_Reporte_PDF/audit_and_fix.py", "Audit Script"),
        ("01_Reporte_PDF/verify_full_synchronization.py", "Verification Script"),
        ("README.md", "README Principal"),
        ("CHANGELOG.md", "CHANGELOG")
    ]
    
    total_issues = 0
    
    for rel_path, desc in files_to_check:
        full_p = os.path.join(ROOT, rel_path)
        if not os.path.exists(full_p):
            continue
        with open(full_p, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        emojis = emoji_pattern.findall(content)
        if emojis:
            print(f"[ALERTA EMOJIS] {desc} ({rel_path}): {len(emojis)} encontrados -> {set(emojis)}")
            total_issues += len(emojis)
        else:
            print(f"[LIMPIO] {desc}: 0 emojis.")
            
        content_lower = content.lower()
        for kw in ai_cliches:
            # Word boundary check
            matches = len(re.findall(r'\b' + re.escape(kw) + r'\b', content_lower))
            if matches > 0:
                print(f"  [AVISO CLICHÉ] {desc}: \"{kw}\" aparece {matches} veces.")
                total_issues += matches

    # Check Word Document (.docx)
    docx_path = os.path.join(ROOT, "01_Reporte_PDF", "Informe_Valuacion_Aluar_word.docx")
    if os.path.exists(docx_path):
        doc = docx.Document(docx_path)
        word_text = " ".join([p.text for p in doc.paragraphs] + [c.text for t in doc.tables for r in t.rows for c in r.cells])
        emojis_docx = emoji_pattern.findall(word_text)
        if emojis_docx:
            print(f"[ALERTA EMOJIS] Word DOCX: {len(emojis_docx)} encontrados -> {set(emojis_docx)}")
            total_issues += len(emojis_docx)
        else:
            print(f"[LIMPIO] Word DOCX: 0 emojis.")
            
        docx_lower = word_text.lower()
        for kw in ai_cliches:
            matches = len(re.findall(r'\b' + re.escape(kw) + r'\b', docx_lower))
            if matches > 0:
                print(f"  [AVISO CLICHÉ] Word DOCX: \"{kw}\" aparece {matches} veces.")
                total_issues += matches

    print("\n--------------------------------------------------------------------------------")
    print(f"RESULTADO: {total_issues} anomalías detectadas.")
    if total_issues == 0:
        print("ESTADO: 100% LIMPIO, CERO EMOJIS, CERO RASTROS DE IA, CERO PLACEHOLDERS.")
    print("--------------------------------------------------------------------------------")

if __name__ == "__main__":
    run_scan()
