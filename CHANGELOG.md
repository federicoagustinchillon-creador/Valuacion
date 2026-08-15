# Historial de Versiones

## [v1.1.0] - 2026-08-15
### Paridad 1:1 Word-PDF, Configuración en Español y Depuración Forense de Clichés

- **Informe en Microsoft Word (.docx) con Paridad 1:1**:
  - Reescritura arquitectónica de `generate_master_word_report.py` con replicación exacta del diseño de portada en dos columnas (Resumen, Tesis, Cuadro de Dictamen con métricas y mini-tablas).
  - Integración nativa de las **31 figuras de alta resolución (300 DPI)** y **22 tablas estilizadas** con formato institucional Navy (`#0D233A`), sombreado zebra (`#F8FAFC`), bordes sutiles y alineación numérica a la derecha.
  - Configuración global del idioma de corrección a **Español (Argentina, `es-AR`)** a nivel de nodo XML y estilos raíz (`docDefaults`), eliminando falsos errores ortográficos en Microsoft Word.
  - Actualización automatizada de la Tabla de Contenidos (TOC) y campos dinámicos mediante Word COM Automation.

- **Depuración Forense de Muletillas y Clichés de IA**:
  - Auditoría exhaustiva en todos los archivos de texto, código fuente (`.tex`, `.py`, `.md`), eliminando frases mecánicas, conectores sobreutilizados (*«sin embargo»*, *«cabe destacar»*, *«es crucial»*, *«en este sentido»*, etc.) y reemplazándolos por prosa financiera rigurosa y directa.

- **Tratado Enciclopédico y Guía de Estudio (51 páginas)**:
  - Consolidación del módulo `05_Guia_de_Estudio` con 12 módulos analíticos, demostraciones matemáticas formales, banco de preguntas de defensa oral y diagramas conceptuales de alta resolución.

## [v1.0.0] - 2026-08-14
### Versión Final Unificada

- **Informe de Valuación (LaTeX / PDF)**:
  - Documento de 30 páginas estructurado en LaTeX con tipografía Georgia.
  - Incorporación de análisis estratégico PESTEL, FODA, Gobierno Corporativo, calificación crediticia sintética y análisis de sensibilidad multidimensional.
  - Integración completa de las 31 figuras cuantitativas.
  - Apéndice contable con Estados Financieros Auditados (FY2020–FY2025), conciliación fiscal y proyección explícita de FCFF (2026E–2030E).

- **Motor Cuantitativo (Python)**:
  - Homogeneización de series bursátiles locales a USD vía tipo de cambio implícito (CCL / ADR GGAL).
  - Estimación del Beta OLS y filtro dinámico de Kalman sobre series de retornos diarios (2016–2026).
  - Simulación estocástica de Monte Carlo con 10.000 iteraciones sobre variables operativas y macroeconómicas.
  - Modelización de riesgo de cola mediante Value at Risk (VaR), Conditional VaR (CVaR) y Teoría de Valores Extremos (EVT - Generalized Pareto Distribution).

- **Notebook Maestro (Jupyter)**:
  - Consolidación autocontenida de los módulos M0 a M13 para verificación y ejecución interactiva de extremo a extremo.

- **Modelo Financiero Dinámico (Excel)**:
  - Estructuración integral del modelo financiero en hoja de cálculo con fórmulas dinámicas de DCF, WACC, matrices WACC vs. $g$ y consolidación contable.

- **Presentación (PowerPoint)**:
  - Diapositivas de soporte para la exposición y defensa del trabajo final.

