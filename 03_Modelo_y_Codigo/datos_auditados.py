# -*- coding: utf-8 -*-
"""
datos_auditados.py
==================
Estados Financieros Consolidados de ALUAR ALUMINIO ARGENTINO S.A.I.C.
FY2020 a FY2025 (ejercicios cerrados al 30 de junio), auditados por
Price Waterhouse & Co. S.R.L.

CRITERIO DE MONEDA (NIC 29)
---------------------------
Cada ejercicio se toma de la columna del ejercicio CORRIENTE de SU PROPIO
informe anual, es decir, expresado en moneda de cierre de ESE ejercicio.
No se utilizan las columnas comparativas, dado que bajo NIC 29 el comparativo se
reexpresa a la moneda de cierre del ejercicio siguiente y por lo tanto no es
homogéneo con el tipo de cambio de su propio cierre.

FUENTES
-------
  FY2020: Aluar Jun_2020 (Memoria y Estados Financieros Consolidados), pp. 47/48/51
  FY2021: Aluar Jun_2021 (Memoria y Estados Financieros Consolidados), pp. 4/5/8
  FY2022: Aluar Jun_2022 (Memoria y Estados Financieros Consolidados), pp. 3/5/8
  FY2023: Aluar Jun_2023 (Memoria y Estados Financieros Consolidados), pp. 4/5/8
  FY2024: Aluar Jun_2024 (Memoria y Estados Financieros Consolidados), pp. 4/5/8
  FY2025: Aluar Jun_2025 (Memoria y Estados Financieros Consolidados), pp. 3/4/7

Toda cifra se validó exigiendo integridad contable estricta:
- Activo Corriente + No Corriente = Total del Activo
- Pasivo + Patrimonio Neto = Total del Activo
- EBIT + Resultado Financiero + Asociadas = EBT (Resultado Antes de Impuestos)
- EBT + Impuesto a las Ganancias = Resultado del Ejercicio
- FCO + FCI + FCF = Variación Neta del Efectivo
"""

# Contado con Liquidacion de cierre de cada ejercicio (30 de junio)
CCL_CIERRE = {2020: 77.0, 2021: 165.0, 2022: 263.0, 2023: 503.0, 2024: 1350.0, 2025: 1430.0}

ACCIONES_EN_CIRCULACION = 2_800_000_000  # EEFF, Resultado por accion

# ---------------------------------------------------------------------------
# ESTADO DE RESULTADOS INTEGRALES CONSOLIDADO (en pesos, moneda de cierre)
# ---------------------------------------------------------------------------
ESTADO_RESULTADOS = {
    2020: dict(
        ventas_netas             =  63_409_348_048,
        costo_ventas             = -54_760_342_500,
        resultado_bruto          =   8_649_005_548,
        otros_resultados_op      =               0,
        costos_distribucion      =  -3_208_310_641,
        gastos_administracion    =  -1_706_887_987,
        otras_ganancias_perdidas =     -30_171_482,
        resultado_operativo      =   3_703_635_438,
        resultado_financiero     =  -6_566_063_005,
        resultado_asociadas      =      55_902_016,
        resultado_antes_imp      =  -2_806_525_551,
        impuesto_ganancias       =    -576_987_122,
        resultado_ejercicio      =  -3_383_512_673,
        resultado_accionistas    =  -3_657_833_689,
    ),
    2021: dict(
        ventas_netas             =  84_727_990_356,
        costo_ventas             = -68_373_389_110,
        resultado_bruto          =  16_354_601_246,
        otros_resultados_op      =               0,
        costos_distribucion      =  -3_652_477_359,
        gastos_administracion    =  -2_587_422_482,
        otras_ganancias_perdidas =       4_335_635,
        resultado_operativo      =  10_119_037_040,
        resultado_financiero     =   2_419_331_881,
        resultado_asociadas      =       8_263_359,
        resultado_antes_imp      =  12_546_632_280,
        impuesto_ganancias       =  -7_905_027_168,
        resultado_ejercicio      =   4_641_605_112,
        resultado_accionistas    =   4_872_789_993,
    ),
    2022: dict(
        ventas_netas             = 172_191_945_319,
        costo_ventas             =-117_898_237_133,
        resultado_bruto          =  54_293_708_186,
        otros_resultados_op      =               0,
        costos_distribucion      =  -7_072_608_359,
        gastos_administracion    =  -4_514_399_010,
        otras_ganancias_perdidas =     -63_699_146,
        resultado_operativo      =  42_643_001_671,
        resultado_financiero     =   9_632_037_259,
        resultado_asociadas      =    -110_423_361,
        resultado_antes_imp      =  52_164_615_569,
        impuesto_ganancias       = -21_779_035_241,
        resultado_ejercicio      =  30_385_580_328,
        resultado_accionistas    =  29_986_923_221,
    ),
    2023: dict(
        ventas_netas             = 325_816_454_929,
        costo_ventas             =-269_627_442_436,
        resultado_bruto          =  56_189_012_493,
        otros_resultados_op      =               0,
        costos_distribucion      = -14_244_626_233,
        gastos_administracion    = -10_963_048_835,
        otras_ganancias_perdidas =     187_212_424,
        resultado_operativo      =  31_168_549_849,
        resultado_financiero     =  44_564_001_050,
        resultado_asociadas      =    -109_126_134,
        resultado_antes_imp      =  75_623_424_765,
        impuesto_ganancias       =  -5_700_597_582,
        resultado_ejercicio      =  69_922_827_183,
        resultado_accionistas    =  66_183_247_107,
    ),
    2024: dict(
        ventas_netas             =1_236_401_592_941,
        costo_ventas             =-1_004_361_399_758,
        resultado_bruto          =  232_040_193_183,
        otros_resultados_op      =   69_358_315_372,
        costos_distribucion      =  -55_831_798_811,
        gastos_administracion    =  -38_755_109_755,
        otras_ganancias_perdidas =     -845_996_116,
        resultado_operativo      =  205_965_603_873,
        resultado_financiero     =    4_962_718_527,
        resultado_asociadas      =      300_555_040,
        resultado_antes_imp      =  211_228_877_440,
        impuesto_ganancias       =  -90_078_786_044,
        resultado_ejercicio      =  121_150_091_396,
        resultado_accionistas    =  122_054_902_973,
    ),
    2025: dict(
        ventas_netas             =1_562_412_110_649,
        costo_ventas             =-1_330_677_784_788,
        resultado_bruto          =  231_734_325_861,
        otros_resultados_op      =   43_157_521_696,
        costos_distribucion      =  -83_210_844_083,
        gastos_administracion    =  -60_925_022_982,
        otras_ganancias_perdidas =    1_186_589_783,
        resultado_operativo      =  131_942_570_275,
        resultado_financiero     =  -48_050_930_393,
        resultado_asociadas      =     -256_815_924,
        resultado_antes_imp      =   83_634_823_958,
        impuesto_ganancias       =  -70_518_972_115,
        resultado_ejercicio      =   13_115_851_843,
        resultado_accionistas    =    7_513_255_855,
    ),
}

# ---------------------------------------------------------------------------
# ESTADO DE SITUACION FINANCIERA CONSOLIDADO (en pesos, moneda de cierre)
# ---------------------------------------------------------------------------
BALANCE = {
    2020: dict(
        efectivo                  =  1_839_369_042,
        cuentas_por_cobrar        =  2_963_245_410,
        inventarios               = 25_148_031_793,
        otros_creditos_c          =  2_825_305_007,
        creditos_impositivos_c    =  2_191_062_408,
        otros_activos_fin_c       =     36_642_836,
        otras_inversiones_c       =              0,
        activo_corriente          = 35_003_656_496,
        ppe                       = 44_175_210_057,
        intangibles               =  1_383_549_875,
        inversiones_asociadas     =    179_154_769,
        otros_creditos_nc         =    222_412_710,
        creditos_impositivos_nc   =     19_116_441,
        activo_imp_diferido       =     22_050_318,
        activo_no_corriente       = 46_001_494_170,
        total_activo              = 81_005_150_666,
        cuentas_por_pagar_c       =  4_615_356_124,
        deuda_financiera_c        = 11_531_280_521,
        otros_pasivos_c           =  2_337_811_076,
        pasivo_corriente          = 18_484_447_721,
        cuentas_por_pagar_nc      =    623_801_384,
        deuda_financiera_nc       = 17_358_044_398,
        otros_pasivos_nc          =  8_868_653_577,
        pasivo_no_corriente       = 26_850_499_359,
        total_pasivo              = 45_334_947_080,
        total_patrimonio          = 35_670_203_586,
    ),
    2021: dict(
        efectivo                  =  7_252_917_427,
        cuentas_por_cobrar        =  3_689_394_219,
        inventarios               = 36_480_731_995,
        otros_creditos_c          =  3_668_735_416,
        creditos_impositivos_c    =  1_399_009_335,
        otros_activos_fin_c       =        910_837,
        otras_inversiones_c       =              0,
        activo_corriente          = 52_491_699_229,
        ppe                       = 60_199_672_377,
        intangibles               =  1_690_086_480,
        inversiones_asociadas     =    277_353_962,
        otros_creditos_nc         =    314_326_591,
        creditos_impositivos_nc   =    198_624_228,
        activo_imp_diferido       =              0,
        activo_no_corriente       = 62_680_063_638,
        total_activo              =115_171_762_867,
        cuentas_por_pagar_c       =  4_789_321_872,
        deuda_financiera_c        =  6_119_068_136,
        otros_pasivos_c           =  2_990_271_080,
        pasivo_corriente          = 13_898_661_088,
        cuentas_por_pagar_nc      =              0,
        deuda_financiera_nc       = 23_811_203_685,
        otros_pasivos_nc          = 19_732_650_053,
        pasivo_no_corriente       = 43_543_853_738,
        total_pasivo              = 57_442_514_826,
        total_patrimonio          = 57_729_248_041,
    ),
    2022: dict(
        efectivo                  = 20_161_189_895,
        cuentas_por_cobrar        = 18_917_452_767,
        inventarios               = 77_031_996_402,
        otros_creditos_c          =  8_736_893_481,
        creditos_impositivos_c    =  1_104_585_898,
        otros_activos_fin_c       =      1_598_589,
        otras_inversiones_c       =              0,
        activo_corriente          =125_953_717_032,
        ppe                       = 89_916_231_377,
        intangibles               =  2_135_899_711,
        inversiones_asociadas     =    344_388_827,
        otros_creditos_nc         =    304_375_359,
        creditos_impositivos_nc   =    307_457_623,
        activo_imp_diferido       =              0,
        activo_no_corriente       = 93_008_352_897,
        total_activo              =218_962_069_929,
        cuentas_por_pagar_c       = 11_888_382_325,
        deuda_financiera_c        = 11_438_716_791,
        otros_pasivos_c           = 19_755_544_912,
        pasivo_corriente          = 43_082_644_028,
        cuentas_por_pagar_nc      =              0,
        deuda_financiera_nc       = 23_801_570_192,
        otros_pasivos_nc          = 32_016_679_052,
        pasivo_no_corriente       = 55_818_249_244,
        total_pasivo              = 98_900_893_272,
        total_patrimonio          =120_061_176_657,
    ),
    2023: dict(
        efectivo                  = 29_693_029_170,
        cuentas_por_cobrar        = 15_464_292_214,
        inventarios               =181_793_434_471,
        otros_creditos_c          =  6_533_666_474,
        creditos_impositivos_c    = 13_030_551_476,
        otros_activos_fin_c       =      4_331_815,
        otras_inversiones_c       =              0,
        activo_corriente          =246_519_305_620,
        ppe                       =207_445_737_487,
        intangibles               =  3_242_978_064,
        inversiones_asociadas     =    633_308_241,
        otros_creditos_nc         =    889_239_241,
        creditos_impositivos_nc   =    162_765_479,
        activo_imp_diferido       =     51_563_967,
        activo_no_corriente       =212_425_592_479,
        total_activo              =458_944_898_099,
        cuentas_por_pagar_c       = 29_364_578_190,
        deuda_financiera_c        = 45_532_934_684,
        otros_pasivos_c           =  9_491_032_148,
        pasivo_corriente          = 84_388_545_022,
        cuentas_por_pagar_nc      =              0,
        deuda_financiera_nc       = 69_611_275_176,
        otros_pasivos_nc          = 31_991_505_856,
        pasivo_no_corriente       =101_602_781_032,
        total_pasivo              =185_991_326_054,
        total_patrimonio          =272_953_572_045,
    ),
    2024: dict(
        efectivo                  =  266_322_192_658,
        cuentas_por_cobrar        =   88_423_622_080,
        inventarios               =  756_454_320_091,
        otros_creditos_c          =   77_810_698_453,
        creditos_impositivos_c    =   18_080_070_469,
        otros_activos_fin_c       =   11_773_861_948,
        otras_inversiones_c       =                0,
        activo_corriente          =1_218_864_765_699,
        ppe                       =  737_899_921_734,
        intangibles               =    6_926_605_491,
        inversiones_asociadas     =    2_653_483_256,
        otros_creditos_nc         =    2_808_147_415,
        creditos_impositivos_nc   =       94_863_121,
        activo_imp_diferido       =    1_079_727_342,
        activo_no_corriente       =  751_462_748_359,
        total_activo              =1_970_327_514_058,
        cuentas_por_pagar_c       =  107_703_695_971,
        deuda_financiera_c        =   83_358_417_754,
        otros_pasivos_c           =   56_316_326_894,
        pasivo_corriente          =  247_378_440_619,
        cuentas_por_pagar_nc      =                0,
        deuda_financiera_nc       =  468_120_057_201,
        otros_pasivos_nc          =  120_279_464_099,
        pasivo_no_corriente       =  588_399_521_300,
        total_pasivo              =  835_777_961_919,
        total_patrimonio          =1_134_549_552_139,
    ),
    2025: dict(
        efectivo                  =   98_947_674_124,
        cuentas_por_cobrar        =   80_168_140_299,
        inventarios               =1_142_056_656_056,
        otros_creditos_c          =   54_742_518_963,
        creditos_impositivos_c    =   42_823_904_159,
        otros_activos_fin_c       =   19_404_759_127,
        otras_inversiones_c       =   32_020_256_411,
        activo_corriente          =1_470_163_909_139,
        ppe                       =1_259_939_797_125,
        intangibles               =    2_677_009_787,
        inversiones_asociadas     =    3_442_673_667,
        otros_creditos_nc         =   21_780_377_930,
        creditos_impositivos_nc   =   53_887_418_251,
        activo_imp_diferido       =    3_831_471_042,
        activo_no_corriente       =1_345_558_747_802,
        total_activo              =2_815_722_656_941,
        cuentas_por_pagar_c       =  111_743_862_956,
        deuda_financiera_c        =  433_391_263_269,
        otros_pasivos_c           =   56_229_216_361,
        pasivo_corriente          =  601_364_342_586,
        cuentas_por_pagar_nc      =                0,
        deuda_financiera_nc       =  417_391_464_490,
        otros_pasivos_nc          =  210_646_455_799,
        pasivo_no_corriente       =  628_037_920_289,
        total_pasivo              =1_229_402_262_875,
        total_patrimonio          =1_586_320_394_066,
    ),
}

# ---------------------------------------------------------------------------
# ESTADO DE FLUJO DE EFECTIVO CONSOLIDADO (en pesos, moneda de cierre)
# ---------------------------------------------------------------------------
FLUJO_EFECTIVO = {
    2020: dict(
        depreciacion       =  5_008_516_569,
        amortizacion       =    258_001_370,
        fco                = 18_920_408_390,
        capex              = -7_931_457_989,
        altas_intangibles  =              0,
        otros_inversion    =     65_838_537,
        fci                = -7_865_619_452,
        altas_deuda        = 18_779_900_162,
        cancelacion_deuda  =-26_448_369_650,
        intereses_pagados  =  2_044_293_453,
        dividendos_pagados = -5_519_136_360,
        fcf                =-15_231_899_301,
        variacion_efectivo = -4_177_110_363,
    ),
    2021: dict(
        depreciacion       =  7_680_589_089,
        amortizacion       =    388_006_517,
        fco                = 16_892_256_112,
        capex              = -1_555_450_901,
        altas_intangibles  =              0,
        otros_inversion    =              0,
        fci                = -1_555_450_901,
        altas_deuda        =  7_469_764_735,
        cancelacion_deuda  =-12_192_743_745,
        intereses_pagados  =  2_456_308_232,
        dividendos_pagados =   -265_084_677,
        fcf                = -7_444_371_919,
        variacion_efectivo =  7_892_433_292,
    ),
    2022: dict(
        depreciacion       = 11_638_889_080,
        amortizacion       =    635_547_731,
        fco                = 23_470_364_498,
        capex              = -2_921_329_114,
        altas_intangibles  =              0,
        otros_inversion    =              0,
        fci                = -2_921_329_114,
        altas_deuda        =  5_690_458_302,
        cancelacion_deuda  = -8_342_977_824,
        intereses_pagados  =  1_504_095_316,
        dividendos_pagados = -4_882_984_193,
        fcf                = -9_039_599_031,
        variacion_efectivo = 11_509_436_353,
    ),
    2023: dict(
        depreciacion       = 19_503_234_438,
        amortizacion       =  1_371_786_355,
        fco                = 57_135_968_178,
        capex              =-33_141_554_950,
        altas_intangibles  =    -10_185_981,
        otros_inversion    =              0,
        fci                =-33_151_740_931,
        altas_deuda        = 89_023_959_113,
        cancelacion_deuda  =-60_949_912_278,
        intereses_pagados  =  8_060_216_409,
        dividendos_pagados =-55_603_571_486,
        fcf                =-35_589_741_060,
        variacion_efectivo =-11_605_513_813,
    ),
    2024: dict(
        depreciacion       =  65_258_463_496,
        amortizacion       =   5_123_435_428,
        fco                = 106_907_787_111,
        capex              = -34_543_200_226,
        altas_intangibles  =      -1_414_203,
        otros_inversion    =               0,
        fci                = -34_544_614_429,
        altas_deuda        = 402_325_708_771,
        cancelacion_deuda  =-258_529_327_981,
        intereses_pagados  =  17_707_792_075,
        dividendos_pagados =  -3_133_677_232,
        fcf                = 122_954_911_483,
        variacion_efectivo = 195_318_084_165,
    ),
    2025: dict(
        depreciacion       =  94_401_647_331,
        amortizacion       =   7_109_275_850,
        fco                =  43_951_466_473,
        capex              =-348_821_496_391,
        altas_intangibles  =    -129_203_516,
        otros_inversion    =               0,
        fci                =-348_950_700_207,
        altas_deuda        = 533_524_217_717,
        cancelacion_deuda  =-458_075_268_932,
        intereses_pagados  =  37_426_104_537,
        dividendos_pagados =  -9_059_413_297,
        fcf                =  28_963_430_951,
        variacion_efectivo =-276_035_802_783,
    ),
}

# ---------------------------------------------------------------------------
# VOLUMEN FISICO — Memoria Anual, Planta de Puerto Madryn (Division Primario)
# "Total solidificado mas despacho de aluminio liquido", en toneladas.
# Es la magnitud que alimenta el modelo de Ingresos = Precio x Cantidad.
# ---------------------------------------------------------------------------
VOLUMEN_TN = {
    2020: 389_696,   # 376.085 solidificado + 13.611 liquido — Memoria 2020, p.2
    2021: 302_735,   # 287.051 solidificado + 15.684 liquido — Memoria 2021, p.2
    2022: 355_817,   # 338.929 solidificado + 16.888 liquido — Memoria 2022, p.2
    2023: 423_709,   # total informado                        — Memoria 2023, p.2
    2024: 443_425,   # 424.537 solidificado + 18.888 liquido — Memoria 2024, p.2
    2025: 442_437,   # 425.409 solidificado + 17.028 liquido — Memoria 2025, p.4
}

# Utilizacion media de la capacidad instalada informada en cada Memoria
UTILIZACION_INFORMADA = {2020: 0.8441, 2021: 0.6832, 2022: 0.7940,
                         2023: 0.9450, 2024: 0.9640, 2025: 0.9680}

CAPACIDAD_INSTALADA_TN = 460_000   # Memoria Anual — capacidad nominal de la planta

ANIOS = [2020, 2021, 2022, 2023, 2024, 2025]


def verificar():
    """Chequeos de integridad contable. Falla ruidosamente si algo no cierra."""
    errores = []
    for y in ANIOS:
        b, r, f = BALANCE[y], ESTADO_RESULTADOS[y], FLUJO_EFECTIVO[y]

        def chk(nombre, a, b_, tol=1):
            if abs(a - b_) > tol:
                errores.append(f"FY{y} {nombre}: {a:,} != {b_:,} (dif {a - b_:,})")

        chk("activo = corriente + no corriente",
            b["total_activo"], b["activo_corriente"] + b["activo_no_corriente"])
        chk("pasivo = corriente + no corriente",
            b["total_pasivo"], b["pasivo_corriente"] + b["pasivo_no_corriente"])
        chk("activo = pasivo + patrimonio",
            b["total_activo"], b["total_pasivo"] + b["total_patrimonio"])
        chk("resultado bruto", r["resultado_bruto"], r["ventas_netas"] + r["costo_ventas"])
        chk("EBIT", r["resultado_operativo"],
            r["resultado_bruto"] + r["otros_resultados_op"] + r["costos_distribucion"]
            + r["gastos_administracion"] + r["otras_ganancias_perdidas"])
        chk("resultado antes de impuestos", r["resultado_antes_imp"],
            r["resultado_operativo"] + r["resultado_financiero"] + r["resultado_asociadas"])
        chk("resultado del ejercicio", r["resultado_ejercicio"],
            r["resultado_antes_imp"] + r["impuesto_ganancias"])
        chk("variacion del efectivo", f["variacion_efectivo"], f["fco"] + f["fci"] + f["fcf"])
    return errores


if __name__ == "__main__":
    errs = verificar()
    if errs:
        print("FALLAS DE INTEGRIDAD:")
        for e in errs:
            print("  -", e)
        raise SystemExit(1)
    print("[OK] Los 6 ejercicios cierran contablemente (balance, resultados y flujo de efectivo).")
    print()
    print(f"{'Ejercicio':>10} {'CCL':>8} {'Ventas ARS':>22} {'Ventas USD MM':>15} {'EBIT USD MM':>13}")
    for y in ANIOS:
        v = ESTADO_RESULTADOS[y]["ventas_netas"]
        e = ESTADO_RESULTADOS[y]["resultado_operativo"]
        c = CCL_CIERRE[y]
        print(f"{'FY'+str(y):>10} {c:>8,.0f} {v:>22,} {v / c / 1e6:>15,.1f} {e / c / 1e6:>13,.1f}")
