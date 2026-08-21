# Cambios pendientes de sincronizar (PDF → Word → PPTX)

Valores nuevos, calculados por `modelos_estocasticos.py` (commit `e47c11e`), listos para reemplazar en el `.tex` local y luego sincronizar Word/PPTX.

**Por qué no está ya hecho:** el `.tex` del PDF vive solo en la PC del autor (está en `.gitignore`, no en este repositorio), así que no se pudo recompilar el PDF desde esta sesión. Como el Word/PPTX deben mantener paridad 1:1 con el PDF, tampoco se tocó su texto todavía — se haría desprolijo (Word/PPTX actualizados, PDF viejo). El código sí quedó actualizado y corriendo (`git log`, commit `e47c11e`).

**Checklist al volver a la PC:**
1. Aplicar los reemplazos de este archivo en el `.tex`.
2. Recompilar el PDF.
3. Pedir que se sincronicen Word y PPTX con el PDF nuevo (o pasar el `.tex` para hacerlo directamente).
4. Si se corre `python graficos.py` de nuevo en la PC local: las figuras 24, 29 y 31 en este repo se regeneraron en un entorno sin la fuente "Segoe UI" (usó una fuente de reemplazo) — al regenerarlas en la PC con esa fuente instalada, van a volver a verse iguales al resto de las 31 figuras. No es un problema de datos, solo tipografía.
5. Para la opción real de PEAL V (punto 6 más abajo): pasar el dato de S0 (o los insumos crudos) para terminar ese cálculo.

## 1. Beta dinámico (Filtro de Kalman) — Figura 24

| | Antes (texto) | Ahora (código real) |
|---|---|---|
| Beta actual | 0,764β | **0,851β** |

Aparece en: PDF (3 lugares, sección "Beta Condicional GARCH(1,1)" / Figura 24), Word (1 lugar), PPTX (diapositiva 25, KPI y tabla).

## 2. Proceso CIR del EMBI+ — Figura 29, sección 16.1

| | Antes (texto) | Ahora (código real) |
|---|---|---|
| κ | 0,7582 (en realidad era la φ del AR(1), reusada sin transformar) | **0,277** |
| θ | 0,1614 (unidades inconsistentes con "422 pb" citado en otros lados) | **422 pb** |
| σ | 0,085 | **12,84** |
| Feller 2κθ vs σ² | "0,2448 > 0,0072" (con los números viejos, mal combinados) | **233,7 > 164,9 → se cumple** |
| AIC CIR vs AR(1) | ΔAIC = -3.359,4 vs -2.894,6 (sin cálculo real detrás) | **97,30 vs 98,25 (ΔAIC=-0,95) — CIR preferido, pero por muy poco** |

La figura_29.png ya está regenerada con estos valores (κ=0,277 en vez de 0,35).

## 3. GARCH(1,1) — persistencia — Figura 30

| | Antes | Ahora (corrida real) |
|---|---|---|
| Persistencia α+β | 0,96 | **0,943** |

Diferencia menor — puede deberse a datos algo más actualizados en la caché.

## 4. Cópula de dependencia de colas — Figura 31, sección "Dependencia Asimétrica en Caídas"

**Este es el cambio más importante de contenido, no solo de número.**

| | Antes (texto) | Ahora (ajuste real por MLE) |
|---|---|---|
| θ Clayton | 1,23 | 1,09 |
| λ_L (dependencia cola inferior) | 0,38 | 0,53 |
| ΔAIC Clayton vs. Gaussiana | -88,9 (Clayton "gana") | **+161,5 (Clayton pierde)** |
| ΔAIC Clayton vs. t-Student | -34,2 (Clayton "gana") | **+207,9 (Clayton pierde)** |
| Cópula preferida por AIC | Clayton | **t-Student** (colas simétricas y pesadas, no asimetría hacia abajo) |

Ajustado sobre ALUA-USD vs. Merval-USD (el EMBI+ del repo solo tiene 6 puntos anuales, no alcanza para calibrar una cópula). Con datos reales, la historia cambia: no es que ALUA tenga colas asimétricas hacia abajo vinculadas al riesgo soberano — tiene colas simétricas y pesadas, mejor descriptas por una t-Student. Esto probablemente requiere reescribir el párrafo de la sección 15.5/16.3, no solo cambiar números.

La figura_31.png ya está regenerada (mantiene el enfoque Clayton porque el capítulo está armado alrededor de esa cópula, pero ya no tiene el corrimiento manual de -32 ARS — es una simulación real de principio a fin).

## 5. Análisis de sensibilidad de Sobol — Diapositiva 21 del PPTX

La tabla actual (Si/ST por variable: Precio Aluminio, etc.) no tiene ningún cálculo detrás. Con el nuevo `m17_sobol_sensibilidad()` corrido sobre WACC / g / shock de margen (las mismas tres fuentes de incertidumbre del Monte Carlo existente):

| Variable | Si (efecto propio) | STi (efecto total, con interacciones) |
|---|---|---|
| g (crecimiento perpetuo) | 0,165 | 0,822 |
| WACC | 0,105 | 0,515 |
| Shock de margen EBITDA | 0,013 | 0,013 |

Confirma cuantitativamente lo que el informe ya dice cualitativamente en la diapositiva 19: el modelo es más sensible a `g` que al WACC. La tabla del PPTX usa variables distintas (Precio Aluminio, WACC, EMBI+, C1) — si querés esas específicas en vez de las tres del Monte Carlo, avisame y las corro (es una sola línea de código distinta, ya con el motor armado).

## 6. Opción Real PEAL V (LSMC) — no tengo reemplazo todavía

El motor de Longstaff-Schwartz está escrito, validado (test contra Black-Scholes, pasa) y listo en `modelos_estocasticos.lsmc_opcion_americana()` / `m18_opcion_real_peal_v()`. Lo que falta es un solo número: **S0, el valor presente del beneficio incremental de PEAL V** (ahorro de energía al pasar de 200 a 582 MW eólicos). No está en ningún archivo del repositorio.

Con eso (o con el dato crudo: MW incrementales, tarifa evitada vs. PPA eólico, y a partir de qué año entra en operación) calculo el valor real de la opción y reemplazo el "+ARS 19,60" / "ARS 1.255,60" en los tres documentos.
