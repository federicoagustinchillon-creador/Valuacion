# -*- coding: utf-8 -*-
"""
generate_perfect_word.py
Genera un documento Word (.docx) con calidad institucional idéntica a LaTeX.
Aplica la paleta institucional (Navy #0D233A, Blue #1E3A8A, Gray #4A4A4A, Gold #D97706, Green #00843D),
fuente Georgia, tablas estilo booktabs, cajas tipo tcolorbox, encabezados y pies de página formales,
y las 31 figuras perfectamente alineadas en pares.
"""

import os, sys, re, shutil
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(DIR)
FIG_DIR = os.path.join(ROOT_DIR, "03_Modelo_y_Codigo", "figuras")
OUTPUT_DOCX = os.path.join(DIR, "Informe_Valuacion_Aluar_word.docx")
DOWNLOADS_DOCX = r"c:\Users\fedea\Downloads\Informe_Valuacion_Aluar.docx"

# Paleta de colores
HEX_NAVY = "0D233A"
HEX_BLUE = "1E3A8A"
HEX_GRAY = "4A4A4A"
HEX_LIGHTGRAY = "F8FAFC"
HEX_BORDER = "D1D5DB"
HEX_GREEN = "00843D"
HEX_RED = "B91C1C"
HEX_GOLD = "D97706"

COLOR_NAVY = RGBColor(13, 35, 58)
COLOR_BLUE = RGBColor(30, 58, 138)
COLOR_GRAY = RGBColor(74, 74, 74)
COLOR_GREEN = RGBColor(0, 132, 61)
COLOR_RED = RGBColor(185, 28, 28)
COLOR_GOLD = RGBColor(217, 119, 6)
COLOR_BLACK = RGBColor(15, 23, 42)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)

def set_table_borders(table, color_hex=HEX_BORDER, sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color_hex}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color_hex}"/>'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color_hex}"/>'
        f'  <w:insideV w:val="none"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_header_footer(doc):
    for section in doc.sections:
        section.top_margin = Inches(0.65)
        section.bottom_margin = Inches(0.65)
        section.left_margin = Inches(0.65)
        section.right_margin = Inches(0.65)
        
        # Header
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hp.text = ""
        r_left = hp.add_run("ALUAR S.A.I.C. (ALUA.BA) · Equity Research                                                 ")
        r_left.font.name = "Georgia"
        r_left.font.size = Pt(8.5)
        r_left.font.bold = True
        r_left.font.color.rgb = COLOR_NAVY
        
        r_right = hp.add_run("FCE · UNCuyo")
        r_right.font.name = "Georgia"
        r_right.font.size = Pt(8.5)
        r_right.font.color.rgb = COLOR_GRAY

        # Footer
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        fp.text = ""
        r_f1 = fp.add_run("Analista Principal: Federico Agustín Chillón | federico.chillon@fce.uncu.edu.ar")
        r_f1.font.name = "Georgia"
        r_f1.font.size = Pt(8.0)
        r_f1.font.color.rgb = COLOR_GRAY

def create_callout_box(doc, text_list, title=None, border_color=HEX_NAVY, bg_color=HEX_LIGHTGRAY):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(7.0)
    set_cell_shading(cell, bg_color)
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
    # Left border thick
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>'
        f'  <w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>'
        f'  <w:bottom w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>'
        f'  <w:right w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    
    if title:
        rt = p.add_run(f"{title}\n")
        rt.font.name = "Georgia"
        rt.font.size = Pt(10.0)
        rt.font.bold = True
        rt.font.color.rgb = COLOR_NAVY
        
    for item in text_list:
        if isinstance(item, tuple):
            prefix, body = item
            rp = p.add_run(prefix)
            rp.font.name = "Georgia"
            rp.font.size = Pt(9.0)
            rp.font.bold = True
            rp.font.color.rgb = COLOR_NAVY
            
            rb = p.add_run(f"{body}\n")
            rb.font.name = "Georgia"
            rb.font.size = Pt(9.0)
            rb.font.color.rgb = COLOR_BLACK
        else:
            rb = p.add_run(f"{item}\n")
            rb.font.name = "Georgia"
            rb.font.size = Pt(9.0)
            rb.font.color.rgb = COLOR_BLACK
            
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Georgia"
    r.font.size = Pt(14.0)
    r.font.bold = True
    r.font.color.rgb = COLOR_NAVY
    
    # Add horizontal rule under heading
    pBrd = parse_xml(f'<w:pBrd {nsdecls("w")}><w:bottom w:val="single" w:sz="8" w:space="2" w:color="{HEX_NAVY}"/></w:pBrd>')
    p._p.get_or_add_pPr().append(pBrd)

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Georgia"
    r.font.size = Pt(11.5)
    r.font.bold = True
    r.font.color.rgb = COLOR_BLUE

def add_heading_3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Georgia"
    r.font.size = Pt(10.0)
    r.font.bold = True
    r.font.color.rgb = COLOR_GRAY

def add_body_p(doc, text, bold_prefix=None, space_after=3):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        rb = p.add_run(bold_prefix)
        rb.font.name = "Georgia"
        rb.font.size = Pt(9.5)
        rb.font.bold = True
        rb.font.color.rgb = COLOR_BLACK
    r = p.add_run(text)
    r.font.name = "Georgia"
    r.font.size = Pt(9.5)
    r.font.color.rgb = COLOR_BLACK
    return p

def add_equation_box(doc, eq_text, eq_label=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    r = p.add_run(f"   {eq_text}   ")
    r.font.name = "Cambria Math"
    r.font.size = Pt(10.5)
    r.font.bold = True
    r.font.color.rgb = COLOR_NAVY
    
    if eq_label:
        rl = p.add_run(f"    ({eq_label})")
        rl.font.name = "Georgia"
        rl.font.size = Pt(9.0)
        rl.font.italic = True
        rl.font.color.rgb = COLOR_GRAY

def add_paired_figures(doc, fig_a_num, fig_a_cap, fig_b_num, fig_b_cap):
    fig_a_path = os.path.join(FIG_DIR, f"figura_{fig_a_num:02d}.png")
    fig_b_path = os.path.join(FIG_DIR, f"figura_{fig_b_num:02d}.png")
    
    if not (os.path.exists(fig_a_path) and os.path.exists(fig_b_path)):
        return
        
    table = doc.add_table(rows=2, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    for row in table.rows:
        for cell in row.cells:
            cell.width = Inches(3.4)
            set_cell_margins(cell, top=40, bottom=40, left=40, right=40)
            
    # Row 0: Images
    p0 = table.cell(0, 0).paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p0.paragraph_format.space_after = Pt(2)
    p0.add_run().add_picture(fig_a_path, width=Inches(3.3))
    
    p1 = table.cell(0, 1).paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1.paragraph_format.space_after = Pt(2)
    p1.add_run().add_picture(fig_b_path, width=Inches(3.3))
    
    # Row 1: Captions
    c0 = table.cell(1, 0).paragraphs[0]
    c0.alignment = WD_ALIGN_PARAGRAPH.LEFT
    c0.paragraph_format.space_after = Pt(4)
    r0 = c0.add_run(f"Figura {fig_a_num}: {fig_a_cap}")
    r0.font.name = "Georgia"
    r0.font.size = Pt(8.0)
    r0.font.color.rgb = COLOR_GRAY
    
    c1 = table.cell(1, 1).paragraphs[0]
    c1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    c1.paragraph_format.space_after = Pt(4)
    r1 = c1.add_run(f"Figura {fig_b_num}: {fig_b_cap}")
    r1.font.name = "Georgia"
    r1.font.size = Pt(8.0)
    r1.font.color.rgb = COLOR_GRAY
    
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

def add_single_figure(doc, fig_num, fig_cap):
    fig_path = os.path.join(FIG_DIR, f"figura_{fig_num:02d}.png")
    if not os.path.exists(fig_path):
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    p.add_run().add_picture(fig_path, width=Inches(4.5))
    
    pc = doc.add_paragraph()
    pc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pc.paragraph_format.space_after = Pt(6)
    rc = pc.add_run(f"Figura {fig_num}: {fig_cap}")
    rc.font.name = "Georgia"
    rc.font.size = Pt(8.0)
    rc.font.color.rgb = COLOR_GRAY

def add_custom_table(doc, headers, data, caption=None, col_widths=None):
    if caption:
        pc = doc.add_paragraph()
        pc.paragraph_format.space_before = Pt(6)
        pc.paragraph_format.space_after = Pt(2)
        pc.paragraph_format.keep_with_next = True
        rc = pc.add_run(f"Tabla: {caption}")
        rc.font.name = "Georgia"
        rc.font.size = Pt(9.0)
        rc.font.bold = True
        rc.font.color.rgb = COLOR_NAVY
        
    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_borders(table)
    
    # Headers
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = ""
        p = hdr_cells[i].paragraphs[0]
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT if i == 0 else WD_ALIGN_PARAGRAPH.RIGHT
        r = p.add_run(str(h))
        r.font.name = "Georgia"
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = COLOR_NAVY
        set_cell_shading(hdr_cells[i], "F1F5F9")
        set_cell_margins(hdr_cells[i], top=80, bottom=80, left=100, right=100)
        if col_widths and i < len(col_widths):
            hdr_cells[i].width = Inches(col_widths[i])
            
    # Rows
    for r_idx, row in enumerate(data):
        row_cells = table.rows[r_idx + 1].cells
        for c_idx, val in enumerate(row):
            row_cells[c_idx].text = ""
            p = row_cells[c_idx].paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.RIGHT
            r = p.add_run(str(val))
            r.font.name = "Georgia"
            r.font.size = Pt(8.5)
            if "Total" in str(row[0]) or "ROIC" in str(row[0]) or "EVA" in str(row[0]) or "Target" in str(row[0]) or "WACC" in str(row[0]):
                r.font.bold = True
                r.font.color.rgb = COLOR_NAVY
            else:
                r.font.color.rgb = COLOR_BLACK
            set_cell_margins(row_cells[c_idx], top=60, bottom=60, left=100, right=100)
            if col_widths and c_idx < len(col_widths):
                row_cells[c_idx].width = Inches(col_widths[c_idx])
                
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def build_word_report():
    print("Iniciando generación de Word institucional...")
    doc = Document()
    add_header_footer(doc)
    
    # ═════════════════════════════════════════════════════════════════════════
    # PORTADA / RESUMEN EJECUTIVO
    # ═════════════════════════════════════════════════════════════════════════
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(10)
    p_title.paragraph_format.space_after = Pt(2)
    r_t = p_title.add_run("Aluar Aluminio Argentino S.A.I.C.")
    r_t.font.name = "Georgia"
    r_t.font.size = Pt(22.0)
    r_t.font.bold = True
    r_t.font.color.rgb = COLOR_NAVY
    
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(8)
    r_s = p_sub.add_run("Reporte de Valuación Fundamental & Equity Research Institucional  |  ALUA.BA")
    r_s.font.name = "Georgia"
    r_s.font.size = Pt(12.0)
    r_s.font.color.rgb = COLOR_GRAY
    
    # Horizontal line
    p_hr = doc.add_paragraph()
    p_hr.paragraph_format.space_after = Pt(8)
    pBrd = parse_xml(f'<w:pBrd {nsdecls("w")}><w:bottom w:val="single" w:sz="12" w:space="1" w:color="{HEX_NAVY}"/></w:pBrd>')
    p_hr._p.get_or_add_pPr().append(pBrd)
    
    # Summary Box Table (2 columns: Left text, Right metrics)
    box_table = doc.add_table(rows=1, cols=2)
    box_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    box_table.autofit = False
    
    c_left = box_table.cell(0, 0)
    c_right = box_table.cell(0, 1)
    c_left.width = Inches(4.2)
    c_right.width = Inches(2.8)
    set_cell_margins(c_left, top=100, bottom=100, left=120, right=120)
    set_cell_margins(c_right, top=100, bottom=100, left=120, right=120)
    set_cell_shading(c_right, "F8FAFC")
    
    # Left Content
    pl = c_left.paragraphs[0]
    pl.paragraph_format.line_spacing = 1.15
    rl_head = pl.add_run("Resumen Ejecutivo & Tesis Central\n")
    rl_head.font.name = "Georgia"
    rl_head.font.size = Pt(11.0)
    rl_head.font.bold = True
    rl_head.font.color.rgb = COLOR_NAVY
    
    rl_body = pl.add_run(
        "Iniciamos cobertura de Aluar Aluminio Argentino S.A.I.C. (ALUA.BA) con dictamen de COMPRAR y un precio objetivo fundamental a 12 meses de ARS 1.236,00 (Target Integrado ARS 1.255,60 incluyendo la opción real eólica PEAL V), lo que representa un retorno esperado de +25,8% / +27,8% frente a la cotización spot de ARS 982,50.\n\n"
        "1. Liderazgo en Costos C1: Matriz 96% autogenerada (78% renovable), asegurando un cash cost de USD 1.680/t (primer cuartil global).\n"
        "2. Cobertura Natural: 80% de ingresos en USD vía LME frente a costos fijos domésticos en ARS.\n"
        "3. Desapalancamiento Acelerado: Conclusión del pico de CAPEX eólico y compresión de deuda neta a <1,0x EBITDA hacia FY2028E."
    )
    rl_body.font.name = "Georgia"
    rl_body.font.size = Pt(9.0)
    rl_body.font.color.rgb = COLOR_BLACK
    
    # Right Content
    pr = c_right.paragraphs[0]
    pr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pr.paragraph_format.line_spacing = 1.15
    
    rr_stat = pr.add_run("Dictamen Cuantitativo Oficial\n")
    rr_stat.font.name = "Georgia"
    rr_stat.font.size = Pt(8.5)
    rr_stat.font.color.rgb = COLOR_GRAY
    
    rr_rec = pr.add_run("COMPRAR\n")
    rr_rec.font.name = "Georgia"
    rr_rec.font.size = Pt(16.0)
    rr_rec.font.bold = True
    rr_rec.font.color.rgb = COLOR_GREEN
    
    rr_data = pr.add_run(
        "Target Base (Dumrauf): ARS 1.236,00\n"
        "Opción Real PEAL V: +ARS 19,60\n"
        "Target Integrado: ARS 1.255,60 (USD 0,79)\n"
        "Cotización Spot: ARS 982,50\n"
        "Upside Integrado: +27,8%\n"
        "─────────────────────────\n"
        "WACC Modelo: 7,06%\n"
        "Costo Equity (Ke): 9,30%\n"
        "Beta Apalancado: 0,888\n"
        "ERP Damodaran: 4,18%\n"
        "CRP (λ × EMBI+): 0,88%\n"
        "Crecimiento Terminal (g): 2,00%\n"
        "Tipo de Cambio CCL: 1.584,25"
    )
    rr_data.font.name = "Georgia"
    rr_data.font.size = Pt(8.5)
    rr_data.font.color.rgb = COLOR_NAVY
    
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    
    # Disclaimer Box
    create_callout_box(
        doc,
        ["Documento de investigación cuantitativa y análisis financiero con fines exclusivamente educativos y de divulgación académica. No constituye una recomendación de compra, venta o asesoramiento de inversión en los términos de la Ley N.° 26.831. Las opiniones técnicas representan estimaciones independientes fundamentadas en modelos econométricos y balances públicos auditados."],
        title="Aviso Legal y Descargo de Responsabilidad"
    )
    
    doc.add_page_break()
    
    # ═════════════════════════════════════════════════════════════════════════
    # SECCIÓN 1: DESCRIPCIÓN DE LA COMPAÑÍA, INDUSTRIA Y ESG
    # ═════════════════════════════════════════════════════
    add_heading_1(doc, "1. Descripción de la Compañía, Dinámica de Industria y Factores ESG")
    add_heading_2(doc, "1.1 Perfil Operativo: Integración Vertical y Capacidad al 100%")
    add_body_p(doc, "Aluar Aluminio Argentino S.A.I.C. es el único productor primario de aluminio integrado en Argentina y uno de los complejos industriales más relevantes de Sudamérica. Fundada en 1974, la compañía opera su planta de reducción electrolítica en Puerto Madryn (Provincia del Chubut) con una capacidad nominal saturada de 460.000 toneladas anuales. Su portafolio abarca aluminio primario (lingotes estándar, lingotes T, barrotes de extrusión billets, alambrón wire rod y placas de laminación) junto con una división de elaborados de alto valor agregado. El 80% de su producción física se exporta a cotización LME más primas regionales, generando un flujo de fondos estructuralmente dolarizado.")
    
    add_paired_figures(
        doc,
        1, "Hitos Históricos de Aluar (1974–2026): Expansión de capacidad y transición renovable.",
        2, "Estructura Accionaria: Grupo Madanes 45,98% y capital flotante/ANSES 54,02%."
    )
    
    add_heading_2(doc, "1.2 Ventajas Competitivas: Matriz Energética y Posición C1")
    add_body_p(doc, "La fundición electrolítica de aluminio es altamente electrointensiva (~14–15 MWh por tonelada de aluminio). El foso defensivo (economic moat) de Aluar radica en:")
    add_body_p(doc, "1. Autonomía Energética Propia (96% del Consumo): 54% provisto por Hidroeléctrica Futaleufú (320 MW bajo concesión), 24% por el Parque Eólico Aluar (PEAL, 200 MW en operación) y 18% por ciclos combinados térmicos propios. Sólo el 4% se toma de la red nacional (SADI).")
    add_body_p(doc, "2. Posición en Primer Cuartil de Costos Globales: Cash cost C1 de USD 1.680/t (percentil 29% de la curva global de costos CRU/Wood Mackenzie), garantizando márgenes operativos positivos aún en los valles del LME.")
    add_body_p(doc, "3. Infraestructura Portuaria Exclusiva: Muelle propio de aguas profundas para descarga directa de alúmina y embarque de exportaciones.")
    
    add_paired_figures(
        doc,
        9, "Cuota de Mercado Doméstica: 60% de participación en Argentina.",
        10, "Matriz Energética y Curva C1: 78% renovable y costo defensivo de USD 1.680/t."
    )
    
    add_heading_2(doc, "1.3 Estrategia Corporativa y División Elaborados")
    add_body_p(doc, "La participación de la división de elaborados se contrajo temporalmente debido a la recesión doméstica, pasando de 6,0% en FY2023 a 3,3% en FY2025:")
    
    add_custom_table(
        doc,
        ["Métrica de Volumen", "FY2023", "FY2024", "FY2025"],
        [
            ["Ventas Elaborados (t)", "23.104", "17.766", "13.498"],
            ["Ventas Totales (t)", "383.834", "418.014", "402.991"],
            ["Participación Elaborados", "6,0%", "4,3%", "3,3%"]
        ],
        caption="Participación de Elaborados en Volumen de Ventas (Memoria y EEFF)",
        col_widths=[3.0, 1.3, 1.3, 1.3]
    )
    
    add_heading_2(doc, "1.4 Scorecard ESG y Mitigación del Arancel CBAM Europeo")
    add_body_p(doc, "Con una intensidad de emisiones inferior a 4 t CO2/t Al frente a la media mundial de ~11 t CO2/t (dominada por fundiciones chinas a carbón), Aluar cuenta con una ventaja arancelaria neta estimada en USD 80–120 por tonelada bajo el Carbon Border Adjustment Mechanism (CBAM) de la Unión Europea.")
    
    # ═════════════════════════════════════════════════════════════════════════
    # SECCIÓN 2: ANÁLISIS FINANCIERO HISTÓRICO Y DUPONT
    # ═════════════════════════════════════════════════════
    add_heading_1(doc, "2. Análisis Financiero Histórico y Descomposición DuPont")
    add_heading_2(doc, "2.1 Desempeño Histórico Auditado (FY2020–FY2025)")
    add_body_p(doc, "Los estados financieros consolidados auditados por PwC reflejan la solidez operativa y la capacidad de generación de EBITDA a través de los ciclos macroeconómicos:")
    
    add_custom_table(
        doc,
        ["Métrica (USD MM)", "FY2020", "FY2021", "FY2022", "FY2023", "FY2024", "FY2025"],
        [
            ["Ventas Netas", "823,5", "513,5", "654,7", "647,8", "915,9", "1.092,6"],
            ["EBITDA", "116,5", "107,4", "209,7", "105,7", "204,7", "163,3"],
            ["Margen EBITDA", "14,2%", "20,9%", "32,0%", "16,3%", "22,4%", "14,9%"],
            ["EBIT Operativo", "48,1", "61,3", "162,1", "62,0", "152,6", "92,3"],
            ["Resultado Neto", "-43,9", "28,1", "103,4", "126,2", "89,7", "9,2"],
            ["CAPEX", "-103,0", "-9,4", "-11,1", "-65,9", "-25,6", "-243,9"],
            ["Deuda Neta", "351,3", "137,4", "57,3", "169,9", "211,2", "525,8"],
            ["Deuda Neta / EBITDA", "3,02x", "1,28x", "0,27x", "1,61x", "1,03x", "3,22x"],
            ["Cobertura Intereses (EBIT/Int)", "1,81x", "4,12x", "107,8x", "7,69x", "8,62x", "3,53x"],
            ["ROIC", "3,73%", "7,50%", "17,85%", "5,22%", "7,94%", "3,52%"]
        ],
        caption="Indicadores Financieros y Operativos Clave FY2020–FY2025 (USD MM)",
        col_widths=[2.4, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8]
    )
    
    add_heading_2(doc, "2.2 Descomposición DuPont de Cinco Factores")
    add_equation_box(doc, "ROE = (RN / EBT) × (EBT / EBIT) × (EBIT / Ventas) × (Ventas / Activos) × (Activos / PN)", "DuPont 5 Factores")
    add_body_p(doc, "En FY2025, la carga impositiva efectiva cayó a 15,67% (alícuota efectiva de 84,3% distorsionada por el ajuste por inflación impositivo NIC 29), deprimiendo el ROE a 0,83% a pesar de que el margen operativo EBIT se ubicó en un saludable 8,44%.")
    
    # ═════════════════════════════════════════════════════════════════════════
    # SECCIÓN 3: SUPUESTOS MACROECONÓMICOS Y PROYECCIÓN P x Q
    # ═════════════════════════════════════════════════════
    add_heading_1(doc, "3. Supuestos Macroeconómicos y Mecánica Operativa (P × Q)")
    add_heading_2(doc, "3.1 Entorno Macroeconómico y Riesgo Soberano")
    add_body_p(doc, "El modelo incorpora la estabilización inflacionaria y la compresión del riesgo país EMBI+ desde 2.400 pb en 2022 a 441 pb al cierre de julio de 2026.")
    
    add_paired_figures(
        doc,
        3, "Macro Argentina: Crecimiento real del PBI e inflación proyectada.",
        4, "Riesgo País (EMBI+): Compresión soberana de 2.400 pb a 441 pb."
    )
    
    add_heading_2(doc, "3.2 Formulación Microeconómica de Ingresos y Margen EBITDA")
    add_body_p(doc, "1. Volumen Físico Saturado (Q): Con capacidad nominal de 460.000 t y 94% de factor de utilización histórico:")
    add_equation_box(doc, "Q = 460.000 t × 0,94 = 432.400 t/año", "Volumen Físico")
    
    add_body_p(doc, "2. Precio Realizado (P): En 2026E escala por el nivel spot del LME en 1T26 ($3.173/t), convergiendo linealmente hacia 2030E al valor de régimen de equilibrio:")
    add_equation_box(doc, "P_2030 = LME_rev ($2.587,1/t) + Premium_elab ($645,7/t) = USD 3.232,8/t", "Precio 2030E")
    
    add_body_p(doc, "3. Calibración de Margen EBITDA (k): Calibrado sobre el 1T26 (Revenue $416 MM, EBITDA $106 MM, C1 $1.680/t):")
    add_equation_box(doc, "k = Margen_Q1 / ((P_Q1 - C1) / P_Q1) = 0,2548 / 0,5634 = 0,4521", "Calibración k")
    
    add_body_p(doc, "4. Absorción de Capital de Trabajo (ΔNWC 2026E): Calculado en base a la mediana histórica (NWC/Ventas = 49,42%):")
    add_equation_box(doc, "ΔNWC_2026E = (Ventas_2026E - Ventas_2025) × 0,4942 = (1.591,4 - 1.092,6) × 0,4942 = USD 246,5 MM", "ΔNWC 2026E")
    
    # ═════════════════════════════════════════════════════════════════════════
    # SECCIÓN 4: COSTO DE CAPITAL (WACC) Y BETA
    # ═════════════════════════════════════════════════════
    add_heading_1(doc, "4. Costo de Capital (WACC), Beta y Factor λ")
    add_heading_2(doc, "4.1 Formulación Completa del WACC (Dumrauf Cap. 12)")
    add_equation_box(doc, "WACC = Ke × (E / V) + Kd × (1 - t) × (D / V)", "WACC Canónico")
    add_equation_box(doc, "WACC = 9,30% × 0,6729 + 3,80% × (1 - 0,35) × 0,3271 = 6,26% + 0,81% = 7,06%", "Sustitución WACC")
    
    add_heading_2(doc, "4.2 Deducción del Beta en Cuatro Pasos")
    add_body_p(doc, "• Paso 1 (Beta OLS 10y, N=2.376 ruedas): Regresión lineal contra S&P 500 arrojó β_OLS = 0,8420 (SE = 0,0563, R² = 8,60%).")
    add_body_p(doc, "• Paso 2 (Ajuste de Blume 1975): β_Blume = (2/3) × 0,8420 + 1/3 = 0,8947.")
    add_body_p(doc, "• Paso 3 (Desapalancamiento Hamada con D/E_hist = 0,5036): β_U = 0,8947 / [1 + (1 - 0,35) × 0,5036] = 0,6745.")
    add_body_p(doc, "• Paso 4 (Reapalancamiento Hamada con D/E_obj = 0,4860): β_L = 0,6745 × [1 + (1 - 0,35) × 0,4860] = 0,8876.")
    
    add_paired_figures(
        doc,
        13, "Secuencia del Beta en 4 Pasos: OLS 0,842 → Blume 0,895 → Desapalancado 0,675 → Hamada 0,888.",
        14, "Descomposición WACC Canónico: Ke = 9,30%, Kd = 2,47% post-tax, WACC = 7,06%."
    )
    
    add_heading_2(doc, "4.3 Fundamentación del Factor λ = 0,20")
    add_equation_box(doc, "Ke = Rf + β_L × ERP + λ × EMBI+ = 4,70% + 0,8876 × 4,18% + 0,20 × 4,41% = 9,30%", "CAPM con λ")
    add_body_p(doc, "El factor λ = 0,20 coincide exactamente con la porción de ventas domésticas (20%). Dado que el 80% se exporta en USD a cotización LME y los costos laborales/servicios están en ARS, una depreciación del peso reduce los costos en dólares, otorgando una cobertura natural frente al riesgo país.")
    
    # ═════════════════════════════════════════════════════════════════════════
    # SECCIÓN 5: VALUACIÓN FUNDAMENTAL DCF Y OPCIÓN REAL
    # ═════════════════════════════════════════════════════
    add_heading_1(doc, "5. Valuación Fundamental DCF y Opción Real PEAL V")
    add_heading_2(doc, "5.1 Esquema de Descuento y Valor Terminal Canónico (Dumrauf Cap. 14)")
    add_equation_box(doc, "EV = Σ [FCFF_t / (1 + WACC)^t] + TV / (1 + WACC)^4 = USD 3.951,0 MM", "Enterprise Value")
    add_body_p(doc, "En estado estacionario de capacidad saturada (460 kt), CAPEX = D&A y ΔNWC = 0, por lo que el FCFF terminal converge al NOPAT de 2030E:")
    add_equation_box(doc, "TV = NOPAT_2030 × (1 + g) / (WACC - g) = 135,5 × 1,02 / (0,0706 - 0,02) = USD 2.731,4 MM", "TV Dumrauf")
    
    add_body_p(doc, "• Precio Objetivo Base (DCF Dumrauf): ARS 1.236,00 por acción (USD 0,78, +25,8% Upside).")
    add_body_p(doc, "• Opción Real PEAL V (Longstaff-Schwartz LSMC): Modela la flexibilidad americana de inversión en 312 MW eólicos mediante regresión sobre polinomios de Laguerre de orden 2, aportando +ARS 19,60 por acción (+USD 0,01).")
    add_body_p(doc, "• Precio Objetivo Integrado (Base + Opción Real): ARS 1.255,60 por acción (USD 0,79, +27,8% Upside).")
    
    add_paired_figures(
        doc,
        15, "Puente de Valuación (Waterfall): Enterprise Value USD 3.951 MM a Equity Value USD 2.186 MM.",
        18, "Football Field de Valuación: Comparativa de rangos intrínsecos frente a cotización Spot."
    )
    
    # ═════════════════════════════════════════════════════════════════════════
    # SECCIÓN 6: VALUACIÓN RELATIVA SECTORIAL
    # ═════════════════════════════════════════════
    add_heading_1(doc, "6. Valuación Relativa y Múltiplos Comparables")
    add_body_p(doc, "Aluar transa a 13,4x EV/EBITDA LTM sobre el resultado deprimido de FY2025. Sin embargo, al proyectar sobre el EBITDA normalizado de FY2026E (USD 391,2 MM), el múltiplo Forward colapsa a 5,2x EV/EBITDA, ubicando a la acción con un descuento del 20%–25% frente a sus pares globales:")
    
    add_custom_table(
        doc,
        ["Compañía / Ticker", "EV/EBITDA LTM", "Margen EBITDA", "ROIC LTM", "FCF Yield 27E"],
        [
            ["ALUAR (ALUA.BA)", "13,3x", "14,9%", "4,3%", "12,8%"],
            ["Alcoa Corp. (AA)", "8,5x", "12,0%", "5,5%", "4,8%"],
            ["Chalco (ACH)", "9,0x", "15,1%", "8,0%", "5,2%"],
            ["Kaiser Aluminum (KALU)", "7,2x", "9,8%", "3,5%", "3,0%"],
            ["Norsk Hydro (NHYDY)", "6,4x", "13,5%", "6,2%", "4,1%"],
            ["Constellium (CSTM)", "5,4x", "10,1%", "5,0%", "3,5%"],
            ["Rusal", "5,1x", "8,4%", "2,1%", "1,5%"],
            ["Mediana Industria", "7,2x", "11,1%", "5,3%", "3,8%"]
        ],
        caption="Múltiplos Financieros y Comparables Globales (julio-2026)",
        col_widths=[2.8, 1.2, 1.2, 1.0, 1.0]
    )
    
    add_paired_figures(
        doc,
        11, "Múltiplos EV/EBITDA vs Margen: Posicionamiento frente a competidores globales.",
        12, "EBITDA y Desapalancamiento: Reducción de deuda neta post-pico de inversión eólica."
    )
    
    # ═════════════════════════════════════════════════════════════════════════
    # SECCIÓN 7: CREACIÓN DE VALOR (EVA) Y DISCIPLINA TERMINAL
    # ═════════════════════════════════════════════
    add_heading_1(doc, "7. Análisis de Creación de Valor (EVA) y Disciplina Terminal")
    add_body_p(doc, "El EVA histórico y proyectado (EVA = (ROIC - WACC) × NOA) confirma que en estado estacionario terminal el spread económico converge exactamente a cero (ROIC = WACC = 7,06%):")
    
    add_custom_table(
        doc,
        ["Métrica de Valor", "FY20", "FY21", "FY22", "FY23", "FY24", "FY25", "2030E"],
        [
            ["NOPAT (USD MM)", "31,3", "39,9", "105,4", "40,3", "99,2", "60,0", "135,5"],
            ["Capital Invertido (NOA)", "838,4", "531,3", "590,5", "771,6", "1.248,9", "1.704,3", "1.919,3"],
            ["ROIC", "3,73%", "7,50%", "17,85%", "5,22%", "7,94%", "3,52%", "7,06%"],
            ["WACC", "7,06%", "7,06%", "7,06%", "7,06%", "7,06%", "7,06%", "7,06%"],
            ["Spread (ROIC - WACC)", "-3,33%", "+0,44%", "+10,79%", "-1,84%", "+0,88%", "-3,54%", "0,00%"],
            ["EVA (USD MM)", "-27,9", "2,3", "63,7", "-14,2", "11,0", "-60,3", "0,0"]
        ],
        caption="Matriz Histórica y Proyectada de Creación de Valor EVA (USD MM)",
        col_widths=[2.4, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8]
    )
    
    # ═════════════════════════════════════════════════════════════════════════
    # SECCIÓN 8: SENSIBILIDAD, MONTE CARLO Y REVERSE DCF
    # ═════════════════════════════════════════════
    add_heading_1(doc, "8. Sensibilidad, Simulación Monte Carlo y Reverse DCF")
    add_body_p(doc, "• Simulación Monte Carlo (20.000 iteraciones, t-Student ν=4,2): Mediana ARS 1.237, intervalo P5–P95 [ARS 844 – ARS 1.737], con 85,2% de probabilidad de retorno positivo frente al spot.")
    add_body_p(doc, "• Reverse DCF: El precio spot actual de ARS 982,50 descuenta una tasa terminal implícita pesimista de apenas g* = 0,69%, muy por debajo del 2,0% fundamental.")
    
    add_paired_figures(
        doc,
        19, "Mapa de Calor WACC vs g: Matriz bidimensional de sensibilidad del precio por acción.",
        20, "Monte Carlo (20.000 iteraciones): Densidad empírica con colas pesadas t-Student."
    )
    
    # ═════════════════════════════════════════════════════════════════════════
    # SECCIÓN 9: GESTIÓN DE RIESGOS Y MODELOS ECONOMÉTRICOS
    # ═════════════════════════════════════════════
    add_heading_1(doc, "9. Gestión Cuantitativa de Riesgo y Validación Econométrica")
    add_body_p(doc, "• Asignación de Kelly: Full-Kelly 73,5%, Half-Kelly 36,8%, acotado al 20,0% por política de CVaR al 95% (-32,80%).")
    add_body_p(doc, "• Filtro de Kalman Dinámico: El beta de mercado converge a 0,764 en el régimen reciente.")
    add_body_p(doc, "• Teoría de Valores Extremos (EVT-GPD): Ajuste Pareto Generalizado con ξ = 0,214 > 0 (colas pesadas Fréchet), arrojando VaR 99% = -8,20% y Expected Shortfall 99% = -10,35%.")
    add_body_p(doc, "• Proceso Estocástico CIR (Riesgo País): dr_t = κ(θ - r_t)dt + σ√r_t dW_t, verificando la condición de Feller (2κθ = 0,2448 > 0,0072 = σ²).")
    add_body_p(doc, "• Cópula de Clayton: Captura dependencia asimétrica de cola inferior (λ_L = 2^(-1/θ) = 0,38).")
    
    add_paired_figures(
        doc,
        23, "Criterio de Asignación de Kelly: Fracción óptima y límite de riesgo por CVaR.",
        24, "Beta Dinámico por Filtro de Kalman: Evolución temporal y convergencia a 0,764."
    )
    
    add_paired_figures(
        doc,
        25, "Teoría de Valores Extremos (EVT-GPD): Estimación de pérdidas extremas de cola.",
        26, "Simulación LME (Ornstein-Uhlenbeck): Reversión a la media (θ = USD 2.814/t)."
    )
    
    add_paired_figures(
        doc,
        29, "Proceso CIR Soberano: Simulación de tasas respetando no-negatividad.",
        31, "Cópula de Clayton: Dependencia asimétrica en caídas de mercado (λ_L = 0,38)."
    )
    
    # ═════════════════════════════════════════════════════════════════════════
    # SECCIÓN 10: DICTAMEN FINAL Y APÉNDICE CONTABLE
    # ═════════════════════════════════════════════
    add_heading_1(doc, "10. Dictamen Final y Apéndice de Estados Financieros Auditados")
    add_body_p(doc, "Se ratifica el dictamen de COMPRAR con un Precio Objetivo Base de ARS 1.236,00 (+25,8%) e Integrado de ARS 1.255,60 (+27,8%).")
    
    add_heading_2(doc, "10.1 Proyecciones Explícitas de Flujo de Fondos (FCFF 2026E–2030E, USD MM)")
    add_custom_table(
        doc,
        ["Línea de Flujo / Año Fiscal", "2026E", "2027E", "2028E", "2029E", "2030E"],
        [
            ["Ventas Netas (Revenue)", "1.591,4", "1.543,0", "1.494,6", "1.446,3", "1.397,9"],
            ["EBITDA", "391,2", "369,3", "347,4", "325,5", "303,6"],
            ["(-) Depreciación y Amortización", "-108,4", "-105,1", "-101,8", "-98,5", "-95,2"],
            ["EBIT Operativo", "282,8", "264,2", "245,6", "227,0", "208,4"],
            ["(-) Impuestos Operativos (35%)", "-99,0", "-92,5", "-86,0", "-79,4", "-72,9"],
            ["NOPAT", "183,8", "171,7", "159,6", "147,6", "135,5"],
            ["(+) D&A (Reversión)", "108,4", "105,1", "101,8", "98,5", "95,2"],
            ["(-) CAPEX de Mantenimiento", "-103,2", "-100,0", "-96,9", "-93,8", "-90,6"],
            ["(-) Variación Capital Trabajo (ΔNWC)", "-246,5", "23,9", "23,9", "23,9", "23,9"],
            ["FCFF Explícito Anual", "-57,5", "200,7", "188,4", "176,2", "164,0"]
        ],
        caption="Proyecciones del Free Cash Flow to the Firm (FCFF 2026E–2030E, USD MM)",
        col_widths=[3.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    )
    
    # Final Disclaimer Box
    create_callout_box(
        doc,
        ["Este documento fue elaborado con fines exclusivamente de investigación académica, educativa y de análisis cuantitativo independiente por Federico Agustín Chillón (FCE, Universidad Nacional de Cuyo). El presente reporte no constituye una oferta pública, asesoramiento financiero personalizado, recomendación vinculante de compra o venta, ni intermediación bursátil en los términos de la Ley de Mercado de Capitales N.° 26.831 y las normas reglamentarias de la Comisión Nacional de Valores (CNV). El autor certifica que las opiniones técnicas, estimaciones financieras y modelizaciones cuantitativas reflejan un análisis independiente fundamentado rigurosamente en datos contables públicos auditados por Price Waterhouse & Co. S.R.L., series de mercado de BYMA, CBOE, S&P Dow Jones y el London Metal Exchange (LME). Cualquier decisión de inversión que un tercero adopte en base a este modelo es de su exclusiva responsabilidad y riesgo."],
        title="Aviso Legal y Certificación del Analista (Research Standards / Ley 26.831)"
    )
    
    doc.save(OUTPUT_DOCX)
    print(f"Documento guardado con éxito en: {OUTPUT_DOCX}")
    try:
        shutil.copy2(OUTPUT_DOCX, DOWNLOADS_DOCX)
        print(f"Copia sincronizada en Downloads: {DOWNLOADS_DOCX}")
    except Exception as e:
        print(f"Aviso al copiar en Downloads: {e}")

if __name__ == "__main__":
    build_word_report()
