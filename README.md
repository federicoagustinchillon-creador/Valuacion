# Valuación Institucional de Aluar Aluminio Argentino S.A.I.C.

**Trabajo Final de Grado / Evaluación Institucional**  
*Universidad Nacional de Cuyo (UNCuyo)*  
**Autor:** Federico Chillón  

---

## 📌 Descripción del Proyecto

Este repositorio contiene la **valuación financiera institucional unificada** de **Aluar Aluminio Argentino S.A.I.C. (BCBA: ALUA)**. El proyecto combina un enfoque riguroso de finanzas corporativas con modelización cuantitativa avanzada en Python y Excel.

El modelo incluye:
- **Flujos de Fondos Descontados (DCF)**: Modelo de dos etapas con simulación de curvas de costo operativo (LME, alúmina, energía) y costo de capital (WACC = 7.06%) ajustado por riesgo país ($\lambda \times \text{EMBI+}$).
- **Simulación Monte Carlo**: Evaluación probabilística de variaciones en variables macroeconómicas y commoditarias clave (10,000 iteraciones).
- **Valuación por Múltiples Comparables**: Análisis de múltiplos de pares regionales e internacionales ($EV/EBITDA$, $P/E$, $P/BV$).
- **Reverse DCF & Análisis de Sensibilidad**: Descomposición de expectativas implícitas en el precio de mercado.

---

## 📁 Estructura del Repositorio

```text
valuacion-aluar-uncuyo/
├── README.md                                  # Presentación ejecutiva y documentación
├── 01_Reporte_PDF/
│   └── Informe_Valuacion_Institucional_Aluar_UNCuyo.pdf  # Informe oficial de 27 páginas
├── 02_Presentacion_PPTX/
│   └── TrabajoFinalEyTBChillonFedericoAluar_HOMOGENEO.pptx # Presentación ejecutiva oficial
├── 03_Modelo_y_Codigo/
│   ├── ValuacionAluar_M1-13_MASTER.ipynb     # Notebook Máster autónomo
│   ├── engine_valuacion.py                    # Motor cuantitativo principal (standalone)
│   ├── datos_auditados.py                     # Dataset financiero y contable auditado
│   ├── m1_mercado.py                          # Módulo de series de mercado y retornos
│   └── static_inputs.json                     # Parámetros canónicos e insumos de la industria
├── 04_Modelo_Excel/
│   └── Valuacion_Aluar_Modelo_Oficial.xlsx  # Planilla financiera oficial dinámica
└── Assets_Oficiales_Pristinos/                # Ilustraciones y gráficos oficiales
```

---

## 🛠️ Requisitos e Instalación

Para ejecutar y reproducir el modelo cuantitativo autónomo:

```bash
pip install pandas numpy matplotlib seaborn scipy openpyxl jupyter
```

Para ejecutar el notebook maestro:
```bash
jupyter notebook 03_Modelo_y_Codigo/ValuacionAluar_M1-13_MASTER.ipynb
```

---

## 📑 Resumen de Entregables Clave

1. **Informe PDF Oficial**: [01_Reporte_PDF/Informe_Valuacion_Institucional_Aluar_UNCuyo.pdf](01_Reporte_PDF/Informe_Valuacion_Institucional_Aluar_UNCuyo.pdf)
2. **Presentación Ejecutiva (Diapositivas)**: [02_Presentacion_PPTX/TrabajoFinalEyTBChillonFedericoAluar_HOMOGENEO.pptx](02_Presentacion_PPTX/TrabajoFinalEyTBChillonFedericoAluar_HOMOGENEO.pptx)
3. **Modelo Financiero Cuantitativo**: [03_Modelo_y_Codigo/ValuacionAluar_M1-13_MASTER.ipynb](03_Modelo_y_Codigo/ValuacionAluar_M1-13_MASTER.ipynb)
4. **Modelo Financiero en Excel**: [04_Modelo_Excel/Valuacion_Aluar_Modelo_Oficial.xlsx](04_Modelo_Excel/Valuacion_Aluar_Modelo_Oficial.xlsx)

---
© 2026 Federico Chillón - UNCuyo. Todos los derechos reservados.
