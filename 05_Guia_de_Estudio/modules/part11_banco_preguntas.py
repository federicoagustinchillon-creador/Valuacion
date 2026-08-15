# -*- coding: utf-8 -*-
"""
modules/part11_banco_preguntas.py
Parte XI: Banco Maestro de 35 Preguntas y Respuestas Complejas para Mesa de Examen y Defensa.
"""

def get_content():
    return r"""
\section{Parte XI: Banco Maestro de 35 Preguntas y Respuestas para Mesa de Examen}

\begin{examquestion}{1. ?`Aluar produce bauxita o alumina en Argentina o la importa?}
\textbf{Respuesta:} \textbf{Importa el 100\%.} Argentina no cuenta con yacimientos comerciales de bauxita explotables. Aluar importa la totalidad de la alumina requerida (aproximadamente $880.000\text{ t/ano}$ para una produccion de $460.000\text{ t}$ de aluminio primario a razon de $1,92\text{ t Al}_2\text{O}_3/\text{t Al}$) desde Brasil (Hydro Alunorte) y Australia a traves de su muelle propio de aguas profundas en Puerto Madryn. Su foso defensivo (*economic moat*) radica en la autogeneracion hidroelectrica/eolica de bajo costo ($USD\,31/\text{MWh}$) y la integracion de cubas Hall-Heroult y anodos pre-cocidos, no en la mineria.
\end{examquestion}

\begin{examquestion}{2. ?`Por que el WACC se fija en 7,06\% y no en 12\% como el promedio de empresas argentinas?}
\textbf{Respuesta:} Porque Aluar es una empresa exportadora de commodity en moneda dura ($\approx 80\%$ de sus ingresos estan denominados y cobrados en dolares o atados al LME) con costos operativos en el primer cuartil de la curva global (C1 de USD 1.680/t). El modelo aplica la metodologia $\text{CAPM-}\lambda$ de Damodaran (2012) con $\lambda = 0,20$, castigando por riesgo pais ($EMBI+ = 441\text{ pb}$) solo la porcion de ingresos dependiente de la macroeconomia domestica ($20\%$). Aplicar el riesgo pais total ($\lambda = 1,0$) duplicaria el riesgo sistematico y arrojaria un WACC artificialmente inflado del $10,57\%$, castigando flujos que ingresan por exportaciones liquidables en el exterior.
\end{examquestion}

\begin{examquestion}{3. ?`Cual es la diferencia entre la Deuda Neta Contable y la Deuda Neta del DCF?}
\textbf{Respuesta:} La Deuda Neta Contable reportada en el balance FY2025 es de USD 525,76 MM (Deuda Bruta USD 673,96 MM menos Caja USD 148,20 MM). En el modelo DCF se utiliza la \textbf{Deuda Neta Estructural de USD 456,00 MM} informada en el informe de gestion del 1T 2026. Esta diferencia surge porque se depuran los pasivos comerciales de corto plazo y las deudas fiscales corrientes que ya fueron debitadas dentro de la proyeccion de la variacion de capital de trabajo ($\Delta NWC$). Si se restara la deuda contable total en el puente de Enterprise Value a Equity, se estaria duplicando la deduccion del pasivo operativo.
\end{examquestion}

\begin{examquestion}{4. ?`Por que se utiliza la copula de Clayton en lugar de una copula Gaussiana en Monte Carlo?}
\textbf{Respuesta:} Porque la copula Gaussiana asume simetria e independencia asintotica en las colas ($\lambda_L = \lambda_U = 0$). En crisis financieras reales de mercados emergentes, el colapso del precio del commodity (LME) y el salto del riesgo soberano (EMBI+) ocurren de forma simultanea y asimetrica (*joint crash*). La copula de Clayton modela especificamente la dependencia de cola inferior mediante su generador $\phi(t) = \frac{1}{\theta}(t^{-\theta}-1)$, arrojando un coeficiente analitico $\lambda_L = 2^{-1/\theta} = \textbf{0,380}$ con $\theta = 1,2258$, lo cual captura el agrupamiento de crisis y conduce a un percentil de estres P5 mucho mas prudente (ARS 750,00 vs ARS 910,00 bajo Gauss).
\end{examquestion}

\begin{examquestion}{5. ?`Que garantiza matematicamente la Condicion de Feller en el proceso CIR?}
\textbf{Respuesta:} Para la ecuacion diferencial estocastica $dr_t = \kappa(\theta - r_t)dt + \sigma \sqrt{r_t} dW_t$, la condicion de Feller establece que si $\mathbf{2\kappa\theta \ge \sigma^2}$, la frontera $r = 0$ es estrictamente inaccesible, garantizando que la tasa de descuento o spread simulado sea estrictamente positivo ($r_t > 0$) casi con seguridad para todo $t > 0$. En la calibracion de Aluar: $2(0,85)(0,0441) = \textbf{0,0750} > (0,12)^2 = \textbf{0,0144}$, verificandose con un factor de seguridad de 5,2x.
\end{examquestion}

\begin{examquestion}{6. ?`Por que se rechazo la expansion de Cornish-Fisher para el calculo del VaR 99\%?}
\textbf{Respuesta:} Por el caveat de Jaschke (2001): en series temporales financieras con curtosis elevada ($K > 6$), el polinomio de transformacion cuantilica de Cornish-Fisher pierde monotonia en las colas extremas ($\frac{\partial z_{CF}}{\partial z_\alpha} < 0$ para $z_\alpha < -2,33$). Dado que los retornos diarios de ALUA.BA presentan una curtosis de $K = 8,41$, Cornish-Fisher arrojaba un cuantil espurio invertido (-13,41\%). Por ello se adopto la Teoria de Valores Extremos (EVT-GPD), arrojando formulas analiticas cerradas exactas: $VaR_{99\%}^{EVT} = \textbf{-10,44\%}$ y $ES_{99\%}^{EVT} = \textbf{-15,78\%}$.
\end{examquestion}

\begin{examquestion}{7. ?`Por que se impone la restriccion $ROIC = WACC$ en el valor terminal complementario?}
\textbf{Respuesta:} Por la disciplina de estado estacionario de Damodaran (2012): proyectar que una empresa industrial madura crece a perpetuidad ($g = 2,0\%$) manteniendo $CAPEX = D\&A$ implica asumir que el retorno sobre el nuevo capital invertido es infinito ($ROIC_{\text{marginal}} = \infty$). Bajo competencia perfecta de largo plazo, las ventajas competitivas se erosionan y el retorno sobre nuevo capital iguala al costo del capital ($ROIC = WACC = 7,06\%$), colapsando el $EVA$ marginal a cero. Esto exige una tasa de reinversion obligatoria $RR = g/WACC = 2,0\% / 7,06\% = \textbf{28,33\%}$, reduciendo el FCFF terminal de USD 135,5 MM a USD 97,1 MM y derivando en un Precio Objetivo de estres academico de \textbf{ARS 1.085,20 (+10,5\% sobre spot)}.
\end{examquestion}

\begin{examquestion}{8. ?`Cual es el valor de la Opcion Real del Parque Eolico PEAL V y como se calcula?}
\textbf{Respuesta:} Valuada mediante Minimos Cuadrados Monte Carlo (Longstaff-Schwartz, LSMC) sobre $10.000$ trayectorias estocasticas del LME con base de polinomios ortogonales de Laguerre, la opcion de expansion irreversible aporta un valor patrimonial de \textbf{USD 54,88 MM}, equivalente a \textbf{+ARS 19,60 por accion}, elevando el Precio Objetivo Integrado de ARS 1.235,51 a \textbf{ARS 1.255,11} (+27,8\% de retorno esperado).
\end{examquestion}

\begin{examquestion}{9. ?`Como se vincula el resultado de la cointegracion Engle-Granger con la estructura del modelo?}
\textbf{Respuesta:} El test de cointegracion en dos etapas de Engle-Granger arroja un estadistico ADF sobre residuos de $t_{\text{res}} = -2,29$, el cual no logra superar el valor critico de MacKinnon al 5\% ($-3,34$). Al rechazarse la cointegracion lineal rigida en niveles, queda descartada una relacion de anclaje estatico entre la accion y el commodity, lo que valida la metodologia de dos factores de Damodaran para la tasa de descuento.
\end{examquestion}

\begin{examquestion}{10. ?`Cual es la recomendacion de dimensionamiento de cartera segun el criterio de Half-Kelly?}
\textbf{Respuesta:} Con un retorno esperado anualizado $\mu = 25,8\%$, tasa libre de riesgo $Rf = 4,7\%$ y volatilidad $\sigma = 44,4\%$, la fraccion de Kelly continuo es $f^* = \frac{\mu - Rf}{\sigma^2} = 107,0\%$. Aplicando el factor de seguridad de Half-Kelly ($f^* / 2 = 53,5\%$) y limitando la exposicion por politica prudencial de diversificacion institucional, se fija una ponderacion maxima recomendada del \textbf{20,0\%} de la cartera.
\end{examquestion}

\begin{examquestion}{11. ?`Por que se aplica la convencion mid-year en el descuento de flujos de fondos?}
\textbf{Respuesta:} Porque las ventas, cobranzas y pagos operativos de Aluar ocurren de manera continua a lo largo de los 365 dias del ejercicio fiscal, no de forma concentrada el 30 de junio. La deduccion analitica por calculo integral prueba que descontar a mitad de periodo ($(1+WACC)^{t-0,5}$) aproxima de forma exacta el valor presente de un flujo uniforme continuo $\int_{t-1}^t CF e^{-rs}ds$.
\end{examquestion}

\begin{examquestion}{12. ?`Cual fue la causa del colapso del ROE contable en FY2025?}
\textbf{Respuesta:} La descomposicion DuPont de 5 factores demuestra que no fue una falla operativa ni desapalancamiento: la rotacion de activos (0,55x) y el apalancamiento (1,78x) operaron normales. La causa fue el desplome del Tax Burden a $0,157$, generado por la tasa efectiva de impuesto a las ganancias del $84,3\%$ resultante del descalce impositivo del ajuste por inflacion NIC 29 (diferimiento forzoso en 6 cuotas nominales de la Ley 27.468).
\end{examquestion}

\begin{examquestion}{13. ?`Que impacto tiene el mecanismo CBAM de la Union Europea sobre Aluar?}
\textbf{Respuesta:} El mecanismo de ajuste en frontera por emisiones de carbono (CBAM) castiga al aluminio producido con carbon (China e India con huella $>12\text{ t }\text{CO}_2/\text{t Al}$). Con una matriz 78\% renovable y una huella de solo 3,4 t $\text{CO}_2/\text{t Al}$, Aluar obtiene la certificacion ASI y accede a primas comerciales de exportacion y exencion total de aranceles punitivos en Europa.
\end{examquestion}

\begin{examquestion}{14. ?`Que beneficios otorga la adhesion al RIGI (Ley 27.742)?}
\textbf{Respuesta:} Otorga 30 anos de estabilidad fiscal, reduccion de alicuota de Ganancias del 35\% al 25\%, amortizacion acelerada de bienes de capital eolicometalurgicos en 2 anos y 0\% de aranceles para importar aerogeneradores. En el modelo, expande el NOPAT un +12,4\%, elevando el Target a \textbf{ARS 1.304,10}.
\end{examquestion}

\begin{examquestion}{15. ?`Cual es la relacion entre el Beta OLS, Blume y Hamada en el modelo?}
\textbf{Respuesta:} El Beta OLS diario de 10 anos contra el S\&P 500 es de $0,842$. Se ajusta por reversion a la media de Blume ($\frac{2}{3}(0,842) + \frac{1}{3} = 0,895$), se desapalanca por Hamada a la estructura historica para aislar el riesgo operativo puro ($\beta_U = 0,675$), y se reapalanca a la estructura objetivo de largo plazo ($D/E = 0,486$), obteniendo el Beta apalancado final de $\beta_L = \textbf{0,888}$.
\end{examquestion}

\begin{examquestion}{16. ?`Como se vincula el Lema de Ito con el modelo de Black-Scholes y la valoracion de activos?}
\textbf{Respuesta:} El Lema de Ito permite diferenciar funciones no lineales de procesos estocasticos continuos considerando la variacion cuadratica $(dW_t)^2 = dt$. Al expandir el valor de un activo $V(t, S_t)$ en serie de Taylor de segundo orden y construir una cartera libre de riesgo con cobertura delta ($\Delta = \frac{\partial V}{\partial S}$), los terminos brownianos $dW_t$ se cancelan exactamente, derivando la ecuacion diferencial parcial (EDP) deterministica de Black-Scholes.
\end{examquestion}

\begin{examquestion}{17. ?`Cual es la interpretacion financiera del teorema de Frisch-Waugh-Lovell (FWL)?}
\textbf{Respuesta:} En una regresion multiple particionada $\mathbf{y} = \mathbf{X}_1 \boldsymbol{\beta}_1 + \mathbf{X}_2 \boldsymbol{\beta}_2 + \mathbf{e}$, el teorema FWL demuestra que el estimador $\hat{\boldsymbol{\beta}}_2$ es identico al obtenido al regresar los residuos de $\mathbf{y}$ purgados de $\mathbf{X}_1$ sobre los residuos de $\mathbf{X}_2$ purgados de $\mathbf{X}_1$. En nuestro modelo, esto prueba que el Beta de Aluar contra el S\&P 500 aisla el riesgo sistematico puro tras proyectar ortogonalmente el efecto del riesgo soberano local.
\end{examquestion}

\begin{examquestion}{18. ?`Por que la factorizacion de Cholesky exige que la matriz de covarianzas sea definida positiva?}
\textbf{Respuesta:} Porque la factorizacion $\mathbf{\Sigma} = \mathbf{L}\mathbf{L}^T$ calcula los elementos diagonales como $L_{ii} = \sqrt{\Sigma_{ii} - \sum_{k=1}^{i-1} L_{ik}^2}$. Si la matriz no es definida positiva ($\mathbf{x}^T \mathbf{\Sigma} \mathbf{x} \le 0$), el radicando puede ser negativo o nulo, generando valores imaginarios o singularidad matematica. En finanzas, una matriz definida positiva garantiza que ninguna cartera tenga varianza nula o negativa.
\end{examquestion}

\begin{examquestion}{19. ?`Como se calcula la Distancia al Default (DD) de Merton y que significa en Aluar?}
\textbf{Respuesta:} La Distancia al Default se calcula como $DD = \frac{\ln(V_0/D) + (\mu_V - 0,5\sigma_V^2)T}{\sigma_V \sqrt{T}}$. Para Aluar, con $V_0 = \text{USD } 2.639,6\text{ MM}$ y $D = \text{USD } 456,0\text{ MM}$, arroja $DD = 8,23\sigma$, lo cual implica una probabilidad esperada de default ($EDF = \Phi(-8,23)$) inferior al $0,0001\%$, certificando una solvencia estructural equivalente a grado de inversion AAA.
\end{examquestion}

\begin{examquestion}{20. ?`Por que el ratio de Devengamientos de Sloan es negativo en Aluar y que senala?}
\textbf{Respuesta:} El ratio de devengamientos es $\text{Accrual Ratio} = \frac{\text{Neto} - FCO - FCI}{\text{Activos Promedio}} = \textbf{-0,064}$. Es negativo porque el Flujo de Caja Operativo real ($FCO = \text{USD } 148,2\text{ MM}$) supero ampliamente a la utilidad contable reportada ($Neto = \text{USD } 9,17\text{ MM}$), senalando maxima calidad de ganancias y descartando cualquier riesgo de inflacion cosmetica de utilidades.
\end{examquestion}

\begin{examquestion}{21. ?`Cual es la diferencia entre el modelo de Miles-Ezzell y el modelo de Hamada?}
\textbf{Respuesta:} Hamada asume que el monto nominal de deuda $D$ es constante en dolares a perpetuidad, por lo que el escudo fiscal tiene el mismo riesgo que la deuda ($Kd$). Miles-Ezzell asume que la empresa rebalancea su deuda al final de cada ano para mantener constante el ratio $D/V$, por lo que el escudo fiscal del primer ano se descuenta a $Kd$ y los subsiguientes a la tasa desapalancada $Ku$. En Aluar se usa Hamada porque emite ONs de monto nominal fijo a mediano plazo.
\end{examquestion}

\begin{examquestion}{22. ?`Por que se rechaza el uso de Fama-French 3-Factores para Aluar?}
\textbf{Respuesta:} Porque en mercados emergentes con cepo y control de capitales, los factores $SMB$ (tamano) y $HML$ (valor) estan distorsionados por la iliquidez domestica y el riesgo soberano. El modelo $\text{CAPM-}\lambda$ de Damodaran es superior porque desagrega explicitamente el riesgo de mercado internacional y el spread del EMBI+ sin multicolinealidad.
\end{examquestion}

\begin{examquestion}{23. ?`Que representa el Teorema de Descomposicion de Riesgo de Euler?}
\textbf{Respuesta:} Como la volatilidad de cartera $\sigma_p(\mathbf{w})$ es homogenea de grado 1, Euler demuestra que el riesgo total se descompone exactamente en la suma ponderada de las contribuciones porcentuales de cada activo: $\sigma_p = \sum w_i MCR_i$ y $\sum CCR_i = 100\%$. En la cartera optima de Aluar, Aluar aporta el $34,5\%$ del riesgo total, TXAR el $22,8\%$ y YPFD el $18,2\%$.
\end{examquestion}

\begin{examquestion}{24. ?`Como se vincula el Teorema de Sklar con la calibracion de margenes de Monte Carlo?}
\textbf{Respuesta:} Sklar demuestra que cualquier funcion de distribucion acumulada multivariada $H(x_1, \dots, x_d)$ puede descomponerse de forma unica en sus marginales univariadas continuas $F_i(x_i)$ y una copula $C(u_1, \dots, u_d)$. Esto permite modelar marginalmente el precio LME como una Student-$t$ ($\nu = 4,2$), el EMBI+ como un proceso CIR, y luego acoplar sus dependencias de cola mediante la copula de Clayton sin imponer normalidad multivariada.
\end{examquestion}

\begin{examquestion}{25. ?`Cual es el consumo especifico de energia electrica en Aluar y como se calcula?}
\textbf{Respuesta:} Se calcula como $E_{\text{esp}} = \frac{V_{\text{celda}}}{k_{\text{Faraday}} \cdot \eta_I} = \frac{4,10\text{ V}}{0,33557\text{ g/Ah} \times 0,945} \approx \textbf{13,5 MWh/t Al}$. Este consumo energetico intensivo representa el $25,0\%$ del Cash Cost C1 de la compania.
\end{examquestion}

\begin{examquestion}{26. ?`Por que el Ciclo de Conversion de Efectivo (CCC) de Aluar es de 64 dias?}
\textbf{Respuesta:} Porque $CCC = DIO (120) + DSO (45) - DPO (101) = 64\text{ dias}$. El elevado plazo de inventarios ($120\text{ dias}$) es obligatorio debido a que Aluar debe almacenar alumina importada y anodos para evitar una parada no programada de cubas Hall-Heroult, la cual destruiria las celdas electroliticas en menos de 4 horas por solidificacion del bano fundido.
\end{examquestion}

\begin{examquestion}{27. ?`Cual es el impacto del Dolar CCL frente al Dolar Oficial en la valuacion?}
\textbf{Respuesta:} El modelo homogeneiza todos los flujos en dolares y convierte el precio objetivo final al Dolar Contado con Liquidacion (CCL = ARS 1.584,20) porque es el unico tipo de cambio de mercado libre y sin restricciones de acceso. Utilizar el oficial distorsionaria el valor patrimonial al computar dividendos no transferibles.
\end{examquestion}

\begin{examquestion}{28. ?`Que rol juegan los polinomios de Laguerre en la valuacion de opciones reales?}
\textbf{Respuesta:} En el algoritmo de Longstaff-Schwartz (LSMC), los polinomios ortogonales de Laguerre ($L_0(x)=1, L_1(x)=1-x, L_2(x)=1-2x+x^2/2$) se utilizan como base funcional para aproximar por regresion OLS el valor esperado de continuacion condicional en cada fecha de ejercicio de la opcion de inversion.
\end{examquestion}

\begin{examquestion}{29. ?`Como se demuestra que el proceso GARCH(1,1) induce exceso de curtosis?}
\textbf{Respuesta:} Elevando al cuadrado la ecuacion de varianza condicional $\sigma_t^2 = \omega + \alpha \epsilon_{t-1}^2 + \beta \sigma_{t-1}^2$, tomando esperanza incondicional y dividiendo por $\bar{\sigma}^4$, se deduce analiticamente que $K = 3\left[1 + \frac{2\alpha^2}{1-\beta^2-2\alpha\beta-3\alpha^2}\right] > 3$, probando que la volatilidad estocastica por si misma genera colas pesadas.
\end{examquestion}

\begin{examquestion}{30. ?`Que es el Teorema de Representacion de Feynman-Kac y para que sirve?}
\textbf{Respuesta:} Establece un puente matematico riguroso entre la solucion de ecuaciones diferenciales parciales (EDPs) parabolicas deterministas y el calculo de esperanzas condicionales estocasticas de difusiones de Ito, permitiendo resolver problemas de valuacion de derivados financieros mediante simulacion Monte Carlo.
\end{examquestion}

\begin{examquestion}{31. ?`Por que el modelo de Black-Litterman es superior a Markowitz tradicional?}
\textbf{Respuesta:} Porque Markowitz tradicional sufre de maxima sensibilidad a los errores de estimacion de los retornos esperados ("maximizador de errores"), generando carteras extremas e inestables. Black-Litterman utiliza inferencia bayesiana para anclar las carteras al equilibrio del mercado (*prior*) y ajustar suavemente segun la confianza del analista.
\end{examquestion}

\begin{examquestion}{32. ?`Cual es la vida media de reversion a la media del precio del aluminio?}
\textbf{Respuesta:} Para el proceso Ornstein-Uhlenbeck calibrado sobre el LME con $\kappa = 0,385$, la vida media es $t_{1/2} = \frac{\ln 2}{\kappa} = \frac{0,69315}{0,385} = \textbf{1,8 anos}$, lo cual indica que los shocks transitorios de oferta o demanda tardan menos de 2 anos en disiparse hacia la media estructural de USD 2.587/t.
\end{examquestion}

\begin{examquestion}{33. ?`Que establece el Teorema de Girsanov en finanzas cuantitativas?}
\textbf{Respuesta:} Permite cambiar la medida de probabilidad del mundo real o fisico ($\mathbb{P}$) a la medida riesgo-neutral ($\mathbb{Q}$) mediante la derivada de Radon-Nikodym, transformando los procesos de precios descontados en martingalas estocasticas donde no existen oportunidades de arbitraje.
\end{examquestion}

\begin{examquestion}{34. ?`Como se determina la capacidad instalada y el volumen de produccion de Aluar?}
\textbf{Respuesta:} La capacidad instalada nominal es de $460.000\text{ t/ano}$ en su planta de Puerto Madryn. Con un factor de utilizacion historico del $94,5\%$, la produccion anual de aluminio primario se proyecta saturada en $\approx 435.000\text{--}440.000\text{ t/ano}$, de las cuales un $70\text{--}80\%$ se exporta y el resto abastece el mercado local.
\end{examquestion}

\begin{examquestion}{35. ?`Cual es la conclusion final del informe y su recomendacion de inversion?}
\textbf{Respuesta:} Se recomienda **SOBREPONDERAR (BUY)** Aluar con un Precio Objetivo Base de **ARS 1.236,00 (+25,8\%)** y un Precio Objetivo Integrado con Opciones Reales de **ARS 1.255,11 (+27,8\%)**, respaldado por costos en primer cuartil mundial (C1 USD 1.680/t), huella verde descarbonizada (3,4 t $\text{CO}_2$/t Al), solvencia estructural ($DD = 8,23\sigma$) y un elevado margen de seguridad frente al precio spot.
\end{examquestion}
\clearpage
"""
