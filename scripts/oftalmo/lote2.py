"""Oftalmología, lote 2: 16 fichas intravítreas (anti-VEGF, implante, antibióticos, antifúngicos, antivirales, otros).

Reglas del lote (ver ledger y DECISIONES.md):
- Las presentaciones que ya vienen a la concentración de uso (Lucentis, Eylia, Vabysmo, Beovu, Jetrea) son `usoDirecto`
  y no llevan protocolo: el verificador no tiene nada que comparar y el riesgo es el exceso de volumen (alerta).
- `reconstituir.volumenMl` es el volumen FINAL tras reconstituir (el polvo suma volumen); el diluyente que se agrega va en el texto.
- Donde ninguna fuente aceptable trae pasos (amikacina, anfotericina B, clindamicina, foscarnet, metotrexato) `protocolos` queda vacío.
"""
from .comun import (cargar, cima, conserv, consenso, diluir, disc, dm, dosis, ficha, final, final_rango, isp, pres,
                    ped, protocolo, reconstituir, sefh_pnt, texto, web)

PNT_BEVA = 'BEVACIZUMAB_25MG_ML_INYECCIN_INTRAVTREA_PNT'
PNT_RANI = 'RANIBIZUMAB_05MG_005ML_INYECCIN_INTRAVTREA_PNT'
PNT_AFLI = 'AFLIBERCEPT_2MG_005ML_INYECCIN_INTRAVTREA_PNT'
PNT_VANCO = 'VANCOMICINA_HIDROCLORURO_10MG_ML_INYECCIN_INTRAVTREA_PNT'
PNT_CEFTA = 'CEFTAZIDIMA'
PNT_VORI = 'VORICONAZOL_100MCG_01ML_INYECCIN_INTRAVTREA_PNT'
PNT_GANCI = 'GANCICLOVIR_20MG_ML_INYECCIN_INTRAVTREA_PNT'

EXCESO = ('La presentación trae más volumen que la dosis: elimina el exceso hasta la marca de {ml} ml antes de inyectar. '
          'Inyectar todo el contenido puede causar una sobredosis ({fuente}).')


def fichas():
    f = {}

    # ---------------------------------------------------------------- bevacizumab
    p = lambda d: sefh_pnt(PNT_BEVA, d)  # noqa: E731
    pe = lambda d: ped('bevacizumab', d)  # noqa: E731
    f['bevacizumab'] = ficha(
        'bevacizumab', 'Bevacizumab intravítreo (Avastin fraccionado)', 'anti-vegf', ['intravitreo'],
        [pres('avastin-100', 'solucion', 100, 'mg', isp('B-1862/25 Avastin concentrado 100 mg/4 mL (bevacizumab)'), volumen=4, isp_codigos=['B-1862/25'],
              nota='Frasco de uso intravenoso (25 mg/ml). El uso intravítreo es off-label y se hace fraccionando el frasco en farmacia.'),
         pres('avastin-400', 'solucion', 400, 'mg', isp('B-1863/25 Avastin concentrado 400 mg/16 mL (bevacizumab)'), volumen=16, isp_codigos=['B-1863/25'],
              nota='Mismo medicamento, frasco grande (25 mg/ml).')],
        [dosis('Degeneración macular asociada a la edad húmeda y otras indicaciones retinales', 'intravitrea',
               'Una inyección intravítrea de 1,25 mg en 0,05 ml, a intervalos regulares (cada 4 a 6 semanas) o según evolución. '
               'La jeringa se prepara en farmacia cargando 0,15 ml del frasco de 25 mg/ml (0,08 ml quedan en el espacio muerto de la aguja).',
               final(1.25, 'mg', 0.05), p('Posología: 1,25 mg/0,05 ml por inyección intravítrea cada 4 o 6 semanas; indicación off-label'),
               estatus='off_label', presentaciones=['avastin-100', 'avastin-400'],
               condicion='El PNT lo marca como «off-label»: el frasco de Avastin solo está autorizado por vía intravenosa.',
               tambien=[consenso('Tabla 4: bevacizumab 25 mg/ml (estabilidad en jeringa)')])],
        protocolos=[
            protocolo('pnt-sefh-fraccionado', 0, 'Fraccionar el frasco en jeringas de 1 ml (PNT SEFH)', 'avastin-100',
                      [texto('Desprecintar el vial de Avastin, limpiar el elastómero con alcohol de 70° y dejar secar.'),
                       cargar(0.15),
                       texto('Quitar la aguja, cerrar la jeringa con un tapón estéril, envasar de forma individual en bolsa estéril, etiquetar y proteger de la luz. '
                             'Trabajar en campana de flujo laminar con técnica aséptica.')],
                      (3.75, 'mg', 0.15), p('Método específico, pasos 1 a 5'))],
        pediatria=('no_establecida', 'Pediamécum: en retinopatía del prematuro hay datos limitados (0,625 mg en dosis única; rango 0,37 a 1,25 mg) y la dosis óptima no está establecida; '
                                      'la fuente no da el volumen de inyección, por eso no se carga como dosis.'),
        conservacion=[
            conserv('Jeringa preparada según el PNT: 9 días en refrigerador (2–8 °C), protegida de la luz. Hay datos de 3 meses; para eso o para lotes de más de 25 unidades hay que hacer control de esterilidad.',
                    p('Conservación y plazo de validez: 9 días'), horas=216),
            conserv('Consenso SEFH-SEO-SERV: 180 días de estabilidad fisicoquímica a 2–8 °C en jeringas de policarbonato o polipropileno (grado A+); el plazo real lo limitan los controles microbiológicos.',
                    consenso('Tabla 4: bevacizumab 25 mg/ml, 180 días a 2–8 °C'), horas=4320)],
        contraindicaciones=['No hay contraindicaciones propias de la vía intravítrea en las fuentes consultadas; el frasco no está autorizado para esta vía.'],
        alertas=['No agitar el vial y trasvasar con cuidado: la agitación y las burbujas agregan la proteína. Descartar la jeringa si hay turbidez (PNT SEFH).',
                 'Se han notificado casos individuales y brotes de acontecimientos adversos oculares graves tras el uso intravítreo fuera de indicación de bevacizumab (Pediamécum).',
                 'La jeringa se prepara con 0,15 ml para inyectar 0,05 ml: el resto es espacio muerto de la aguja. Inyectar solo hasta la marca de 0,05 ml (PNT SEFH).'],
    )

    # ---------------------------------------------------------------- ranibizumab
    cv = lambda d: cima('ranibizumab', '106374004', d)  # noqa: E731  Lucentis vial
    cj = lambda d: cima('ranibizumab', '106374003', d)  # noqa: E731  Lucentis jeringa precargada
    p = lambda d: sefh_pnt(PNT_RANI, d)  # noqa: E731
    f['ranibizumab'] = ficha(
        'ranibizumab', 'Ranibizumab intravítreo (Lucentis)', 'anti-vegf', ['intravitreo'],
        [pres('lucentis-vial', 'solucion', 2.3, 'mg', cv('6.5 Vial con 0,23 ml de solución estéril (10 mg/ml)'), volumen=0.23, isp_codigos=['B-1989/22'], uso_directo=True,
              nota='Lucentis 10 mg/ml. El ISP registra «solución inyectable 10 mg/mL» sin distinguir vial de jeringa. Cantidad: 10 mg/ml × 0,23 ml.'),
         pres('lucentis-jeringa', 'jeringa_precargada', 1, 'mg', cj('Volumen extraíble de la jeringa precargada: 0,1 ml'), volumen=0.1, uso_directo=True,
              nota='Jeringa precargada de 10 mg/ml; cantidad: 10 mg/ml × 0,1 ml extraíbles.')],
        [dosis('Degeneración macular neovascular, edema macular diabético, oclusión venosa retiniana y neovascularización coroidea', 'intravitrea',
               '0,5 mg (0,05 ml) en inyección intravítrea. El vial contiene 0,23 ml y la jeringa 0,1 ml extraíbles: hay que eliminar el exceso antes de inyectar.',
               final(0.5, 'mg', 0.05), cv('4.2 Posología: 0,5 mg administrados como una inyección intravítrea; volumen de inyección de 0,05 ml'), estatus='autorizada',
               presentaciones=['lucentis-vial', 'lucentis-jeringa'],
               tambien=[p('Indicaciones y posología: 0,5 mg/0,05 ml'), consenso('Tabla 4: ranibizumab 0,5 mg/0,05 ml')]),
         dosis('Retinopatía del prematuro (zona I, zona II con estadio 3+ o ROP agresiva posterior)', 'intravitrea',
               '0,2 mg (0,02 ml) en inyección intravítrea en recién nacidos pretérmino. El vial contiene 0,23 ml: se desecha el exceso antes de inyectar.',
               final(0.2, 'mg', 0.02), cv('4.2 Posología: 0,2 mg en recién nacidos pretérmino; volumen de inyección de 0,02 ml'), estatus='autorizada', poblacion='pediatrico',
               presentaciones=['lucentis-vial'],
               condicion='Solo con el vial: la jeringa precargada no sirve para esta dosis porque no permite medir 0,02 ml.')],
        pediatria=('con_dosis', 'Retinopatía del prematuro: 0,2 mg/0,02 ml (CIMA 4.2). Para las demás indicaciones no se ha establecido en menores de 18 años.'),
        conservacion=[conserv('Conservar en nevera (2–8 °C), sin congelar. Antes de usar, el vial sin abrir puede estar hasta 24 horas a 25 °C.', cv('6.3 Periodo de validez'), horas=24),
                      conserv('Alícuotas de farmacia (jeringas de 0,5 ml): 9 días refrigeradas según el PNT; el consenso da 28 días de estabilidad fisicoquímica a 2–8 °C.',
                              p('Conservación y plazo de validez: 9 días'), horas=216)],
        contraindicaciones=['Hipersensibilidad al ranibizumab o a alguno de los excipientes; infección ocular o periocular activa o sospechada; inflamación intraocular activa grave (CIMA 4.3).'],
        alertas=[EXCESO.format(ml='0,05', fuente='CIMA 4.2 y 6.6'),
                 'El PNT de la SEFH describe un fraccionamiento en alícuotas de 0,065 ml en jeringas de 0,5 ml sin espacio muerto; es una preparación de farmacia y no tiene verificador porque no hay dilución.'],
    )

    # ---------------------------------------------------------------- aflibercept
    cv = lambda d: cima('aflibercept', '112797002', d)  # noqa: E731  Eylea vial
    cj = lambda d: cima('aflibercept', '112797001', d)  # noqa: E731  Eylea jeringa
    p = lambda d: sefh_pnt(PNT_AFLI, d)  # noqa: E731
    f['aflibercept'] = ficha(
        'aflibercept', 'Aflibercept intravítreo (Eylia / Eylea)', 'anti-vegf', ['intravitreo'],
        [pres('eylia-vial', 'solucion', 4, 'mg', cv('6.5 Cada vial contiene un volumen extraíble de al menos 0,1 ml (40 mg/ml)'), volumen=0.1, isp_codigos=['B-2275/22'], uso_directo=True,
              nota='Eylia 40 mg/ml (ISP B-2275/22). Cantidad: 40 mg/ml × 0,1 ml extraíbles.'),
         pres('eylia-jeringa', 'jeringa_precargada', 3.6, 'mg', cj('Volumen extraíble de la jeringa precargada: al menos 0,09 ml (40 mg/ml)'), volumen=0.09, uso_directo=True,
              nota='Jeringa precargada. Cantidad: 40 mg/ml × 0,09 ml extraíbles.')],
        [dosis('Degeneración macular neovascular, edema macular (diabético y por oclusión venosa) y neovascularización coroidea miópica', 'intravitrea',
               '2 mg (0,05 ml) en inyección intravítrea. El vial (0,1 ml extraíbles) y la jeringa (0,09 ml extraíbles) traen más que la dosis: elimina el exceso antes de inyectar.',
               final(2, 'mg', 0.05), cv('4.2 y 6.6: la dosis recomendada es de 2 mg de aflibercept, equivalente a 0,05 ml'), estatus='autorizada',
               presentaciones=['eylia-vial', 'eylia-jeringa'],
               tambien=[p('Posología: 2 mg de aflibercept equivalentes a 50 µl'), consenso('Tabla 4: aflibercept 2 mg/0,05 ml')])],
        pediatria=('sin_datos', 'La ficha técnica española trae una dosis para recién nacidos pretérmino con retinopatía del prematuro (0,4 mg/0,01 ml con el dispositivo dosificador PICLEO); '
                                'no se carga aquí porque exige ese dispositivo y no se comprobó la indicación en Chile.'),
        conservacion=[conserv('Conservar en nevera (2–8 °C). Las alícuotas de farmacia duran 9 días refrigeradas según el PNT; el consenso da 28 días de estabilidad fisicoquímica a 2–8 °C.',
                              p('Conservación y plazo de validez: 9 días'), horas=216)],
        contraindicaciones=['Hipersensibilidad al aflibercept; infección ocular o periocular activa o sospechada; inflamación intraocular activa grave (CIMA 4.3).'],
        alertas=[EXCESO.format(ml='0,05', fuente='CIMA 4.2 y 6.6'),
                 'Cada vial o jeringa es para un solo ojo: extraer varias dosis de un mismo envase aumenta el riesgo de contaminación e infección (CIMA 4.2).',
                 'En Chile también está registrado Eylia 8 mg/0,07 mL (ISP B-3222/26). Su posología no se carga porque no se consultó su ficha técnica.'],
    )

    # ---------------------------------------------------------------- faricimab
    cv = lambda d: cima('faricimab', '1221683001', d)  # noqa: E731  vial
    cj = lambda d: cima('faricimab', '1221683002', d)  # noqa: E731  jeringa
    f['faricimab'] = ficha(
        'faricimab', 'Faricimab intravítreo (Vabysmo)', 'anti-vegf', ['intravitreo'],
        [pres('vabysmo-vial', 'solucion', 28.8, 'mg', cv('6.5 Vial con 0,24 ml de solución estéril (120 mg/ml)'), volumen=0.24, isp_codigos=['B-2970/23'], uso_directo=True,
              nota='Vabysmo 120 mg/ml. El ISP lo registra como «6 mg/0,05 mL» sin distinguir vial de jeringa. Cantidad: 120 mg/ml × 0,24 ml.'),
         pres('vabysmo-jeringa', 'jeringa_precargada', 21, 'mg', cj('6.5 Cada jeringa precargada contiene 21 mg de faricimab en 0,175 ml'), volumen=0.175, uso_directo=True)],
        [dosis('Degeneración macular neovascular, edema macular diabético y edema por oclusión venosa retiniana', 'intravitrea',
               '6 mg (0,05 ml) en inyección intravítrea. La jeringa contiene 21 mg en 0,175 ml: se elimina el exceso hasta la marca de dosis de 0,05 ml.',
               final(6, 'mg', 0.05), cj('4.2 Posología: 6 mg (0,05 ml de solución) mediante inyección intravítrea'), estatus='autorizada',
               presentaciones=['vabysmo-vial', 'vabysmo-jeringa'],
               tambien=[consenso('Tabla 4: faricimab 6 mg/0,05 ml')])],
        pediatria=('no_establecida', 'La ficha técnica no establece la seguridad ni la eficacia en menores de 18 años (CIMA).'),
        conservacion=[conserv('Conservar en nevera (2–8 °C). Antes del uso, el vial o la jeringa sin abrir pueden estar hasta 24 horas a 20–25 °C en su embalaje original.', cj('6.3 Periodo de validez'), horas=24)],
        contraindicaciones=['Hipersensibilidad al faricimab; infección ocular o periocular activa o sospechada; inflamación intraocular activa (CIMA 4.3).'],
        alertas=[EXCESO.format(ml='0,05', fuente='CIMA 4.2 y 6.6'),
                 'Cada jeringa o vial es para un solo ojo (CIMA 4.2).'],
    )

    # ---------------------------------------------------------------- brolucizumab
    c = lambda d: cima('brolucizumab', '1191417', d)  # noqa: E731
    f['brolucizumab'] = ficha(
        'brolucizumab', 'Brolucizumab intravítreo (Beovu)', 'anti-vegf', ['intravitreo'],
        [pres('beovu-jeringa', 'jeringa_precargada', 19.8, 'mg', c('6.5 Jeringa precargada con 0,165 ml de solución (120 mg/ml)'), volumen=0.165, uso_directo=True,
              nota='Beovu 120 mg/ml. Cantidad: 120 mg/ml × 0,165 ml. No aparece en el ISP (31-oct-2026).'),
         pres('beovu-vial', 'solucion', 27.6, 'mg', c('4.2 y 6.6: el vial contiene 0,23 ml (120 mg/ml)'), volumen=0.23, uso_directo=True,
              nota='Cantidad: 120 mg/ml × 0,23 ml.')],
        [dosis('Degeneración macular neovascular y edema macular diabético', 'intravitrea',
               '6 mg (0,05 ml) en inyección intravítrea. La jeringa (0,165 ml) y el vial (0,23 ml) traen más que la dosis: expulsa el exceso antes de inyectar.',
               final(6, 'mg', 0.05), c('4.2 Posología: 6 mg de brolucizumab (0,05 ml de solución) en inyección intravítrea'), estatus='autorizada',
               presentaciones=['beovu-jeringa', 'beovu-vial'], condicion='Autorizada en España (CIMA). No figura en el registro del ISP.')],
        registro='no_registrado',
        pediatria=('no_establecida', 'No se ha establecido la seguridad y eficacia en menores de 18 años; no hay datos (CIMA 4.2).'),
        conservacion=[conserv('Conservar en nevera (2–8 °C) y proteger de la luz en el blíster sellado. Antes de usar, el blíster sin abrir puede estar hasta 24 horas por debajo de 25 °C.', c('6.3 y 6.4'), horas=24)],
        contraindicaciones=['Hipersensibilidad al principio activo o a algún excipiente; infecciones oculares o perioculares activas o sospechadas; inflamación intraocular activa (CIMA 4.3).'],
        alertas=[EXCESO.format(ml='0,05', fuente='CIMA 4.2'),
                 'Si se inyecta todo el volumen de la jeringa o del vial puede haber una sobredosis (CIMA 4.2).'],
    )

    # ---------------------------------------------------------------- dexametasona (implante)
    c = lambda d: cima('dexametasona-implante', '10638001', d)  # noqa: E731
    f['dexametasona-implante'] = ficha(
        'dexametasona-implante', 'Dexametasona, implante intravítreo (Ozurdex)', 'corticoide', ['intravitreo'],
        [pres('ozurdex-700', 'implante', 700, 'mcg', isp('F-19167/22 Ozurdex implante intravítreo'), isp_codigos=['F-19167/22'],
              nota='Implante de 700 µg en un aplicador de un solo uso. No se prepara ni se diluye.')],
        [dosis('Edema macular diabético en pseudofáquicos, edema macular por oclusión venosa retiniana y uveítis no infecciosa del segmento posterior', 'intravitrea',
               'Un implante de 700 µg por vía intravítrea en el ojo afectado. No se recomienda en ambos ojos al mismo tiempo. Cada aplicador es para un solo ojo.',
               None, c('4.2 Posología: un implante OZURDEX por vía intravítrea en el ojo afectado'), estatus='autorizada')],
        modo='informativa',
        pediatria=('no_establecida', 'No se han establecido la seguridad y eficacia en la población pediátrica; no hay datos (CIMA 4.2).'),
        contraindicaciones=['Hipersensibilidad al principio activo o a algún excipiente (CIMA 4.3).'],
        alertas=['Es un implante: no hay concentración ni volumen que verificar. Solo un oftalmólogo con experiencia en inyecciones intravítreas debe aplicarlo (CIMA 4.2).',
                 'Con desgarro de la cápsula posterior o una apertura del iris al vítreo hay riesgo de que el implante se desplace a la cámara anterior y cause edema o descompensación corneal (CIMA 4.4).'],
    )

    # ---------------------------------------------------------------- vancomicina
    p = lambda d: sefh_pnt(PNT_VANCO, d)  # noqa: E731
    fen = lambda d: web('amikacina-iv', 'PMC13405202', 'Antibiotics (MDPI)', d)  # noqa: E731
    wit = lambda d: web('amikacina-iv', '28110950', 'Ophthalmology (AAO)', d)  # noqa: E731
    f['vancomicina'] = ficha(
        'vancomicina', 'Vancomicina intravítrea', 'antibiotico', ['intravitreo'],
        [pres('vial-500', 'polvo', 500, 'mg', isp('B-3218/26 Vancomicina liofilizado para solución inyectable 500 mg'), isp_codigos=['B-3218/26'],
              nota='Vial de uso intravenoso; el uso intravítreo es off-label y se prepara en farmacia.')],
        [dosis('Endoftalmitis bacteriana', 'intravitrea',
               '1 mg en 0,1 ml (10 mg/ml) en inyección intravítrea, en general dosis única. Si hay gas o aceite de silicona, reducir la dosis (1/4 a 1/10); en vitrectomía, al 50 %.',
               final(1, 'mg', 0.1), p('Composición: 5 mg de vancomicina en 0,5 ml (10 mg/ml); Posología: dosis única'), estatus='off_label',
               condicion='Preparación magistral del PNT; la vancomicina no tiene indicación intravítrea en su ficha.',
               tambien=[consenso('Tabla 4: vancomicina 1 mg/0,1 ml'), fen('Endoftalmitis: vancomicina intravítrea 1 mg/0,1 ml')])],
        protocolos=[
            protocolo('pnt-sefh-10-mg-ml', 0, 'Desde el vial de 500 mg (PNT SEFH)', 'vial-500',
                      [reconstituir('agua para inyección: agregar 10 ml (queda a 50 mg/ml)', 10),
                       diluir(2, 10, 'cloruro de sodio 0,9 %'),
                       texto('Homogeneizar la mezcla en la misma jeringa (queda a 10 mg/ml).'),
                       texto('Filtrar (0,22 µm) 0,5 ml de esta solución sobre una jeringa de insulina de 1 ml, tapar, envasar en bolsa y etiquetar. '
                             'El volumen inyectado es 0,1 ml; el resto compensa el espacio muerto de la jeringa y la aguja.')],
                      (5, 'mg', 0.5), p('Método específico, pasos 1 a 7'))],
        pediatria=('sin_datos', 'El PNT y las fuentes consultadas no traen una pauta pediátrica.'),
        conservacion=[conserv('Jeringa preparada: 9 días refrigerada (2–8 °C) y protegida de la luz; 30 horas a temperatura ambiente. Congelada, hay datos de 6 meses con ensayos de esterilidad.',
                              p('Conservación y plazo de validez: 9 días'), horas=216)],
        contraindicaciones=['Hipersensibilidad al principio activo o a algún excipiente (ficha técnica de uso intravenoso, CIMA 4.3).',
                            'La ficha de uso intravenoso prohíbe la vía intramuscular por riesgo de necrosis (CIMA 4.3).'],
        alertas=['ALERTA ROJA — La vancomicina intraocular se ha asociado a vasculitis retiniana oclusiva hemorrágica (HORV): en la serie de 36 ojos, 33 recibieron vancomicina por bolo intracameral, '
                 '22 (61 %) terminaron con visión de 20/200 o peor y 8 (22 %) sin percepción de luz (Witkin 2017). No uses esta ficha para la vía intracameral.',
                 'Reducir la dosis de los antibióticos intravítreos si se usó gas o aceite de silicona (PNT SEFH).'],
        discrepancias=[],
    )
    wit('Vancomicina intraocular y vasculitis retiniana oclusiva hemorrágica: serie de 36 ojos (alerta HORV)')

    # ---------------------------------------------------------------- ceftazidima
    p = lambda d: sefh_pnt(PNT_CEFTA, d, enlace='CEFTAZIDIMA_2MG_01ML_INYECCIN_INTRAVTREA_PNT')  # noqa: E731
    fen = lambda d: web('amikacina-iv', 'PMC13405202', 'Antibiotics (MDPI)', d)  # noqa: E731
    evi = lambda d: web('amikacina-iv', 'PMC13421665', 'Communications Medicine (Nature)', d)  # noqa: E731
    s_p = p('Composición y posología: 10 mg de ceftazidima en 0,5 ml (20 mg/ml) = 2 mg/0,1 ml')
    s_c = consenso('Tabla 4: ceftazidima 2 mg/0,1 ml')
    s_f = fen('Endoftalmitis empírica: ceftazidima 2,25 mg/0,1 ml')
    s_e = evi('Ensayo EVIAN: ceftazidima 2,25 mg/0,1 ml')
    f['ceftazidima'] = ficha(
        'ceftazidima', 'Ceftazidima intravítrea', 'antibiotico', ['intravitreo'],
        [pres('vial-1g', 'polvo', 1000, 'mg', isp('F-11944/22 Ceftazidima polvo para solución inyectable 1 g'), isp_codigos=['F-11944/22'],
              nota='Vial de uso intravenoso; el uso intravítreo es off-label y se prepara en farmacia. Al reconstituir hay un sobrevolumen de unos 0,6 ml por gramo.')],
        [dosis('Endoftalmitis bacteriana', 'intravitrea',
               '2 mg en 0,1 ml (20 mg/ml) en inyección intravítrea, en general dosis única (solo un 7 % necesita una segunda inyección a las 40–72 h). Reducir la dosis si hay gas o aceite de silicona.',
               final(2, 'mg', 0.1), s_p, estatus='off_label', condicion='Preparación magistral del PNT; la ceftazidima no tiene indicación intravítrea en su ficha.',
               tambien=[s_c])],
        protocolos=[
            protocolo('pnt-sefh-20-mg-ml', 0, 'Desde el vial de 1 g (PNT SEFH)', 'vial-1g',
                      [reconstituir('agua para inyección: agregar 9,4 ml (el polvo suma volumen y quedan 10 ml a 100 mg/ml)', 10),
                       texto('Agitar con la aguja clavada en el vial para ventilarlo y evitar la sobrepresión de dióxido de carbono, hasta disolución completa.'),
                       diluir(2, 10, 'cloruro de sodio 0,9 %'),
                       texto('Homogeneizar la mezcla en la misma jeringa (queda a 20 mg/ml). Filtrar (0,22 µm) 0,5 ml sobre una jeringa de insulina de 1 ml, tapar, envasar y etiquetar. Proteger de la luz.')],
                      (10, 'mg', 0.5), p('Método específico, pasos 1 a 7'))],
        pediatria=('sin_datos', 'El PNT y las fuentes consultadas no traen una pauta pediátrica.'),
        conservacion=[conserv('Jeringa preparada: 9 días refrigerada (2–8 °C) o 45 días congelada (−20 °C), protegida de la luz. Hay bibliografía de 6 meses congelada con control de esterilidad.',
                              p('Conservación y plazo de validez: 9 días'), horas=216)],
        contraindicaciones=['Hipersensibilidad a la ceftazidima, a otras cefalosporinas o a algún excipiente; antecedente de hipersensibilidad grave a otro betalactámico (ficha técnica de uso intravenoso, CIMA 4.3).'],
        alertas=['Desechar la solución si hay precipitado. Con aceite de silicona o gas hay que reducir la dosis (PNT SEFH).',
                 'Es una buena alternativa a los aminoglucósidos por su escasa toxicidad retiniana (PNT SEFH). Las inyecciones repetidas aumentan la toxicidad retiniana.'],
        discrepancias=[disc('Dosis intravítrea de ceftazidima por 0,1 ml',
                            [(s_p['ref'], '2 mg/0,1 ml (PNT SEFH)'), (s_c['ref'], '2 mg/0,1 ml (consenso SEFH-SEO-SERV 2025)'),
                             (s_f['ref'], '2,25 mg/0,1 ml (Fenniri 2026)'), (s_e['ref'], '2,25 mg/0,1 ml (ensayo EVIAN)')],
                            '2 mg/0,1 ml',
                            'Las fuentes españolas (PNT y consenso) dan 2 mg; las publicaciones de EE. UU. y del ensayo EVIAN dan 2,25 mg. Se muestra la cifra que trae el protocolo de preparación verificable.')],
    )

    # ---------------------------------------------------------------- amikacina
    fen = lambda d: web('amikacina-iv', 'PMC13405202', 'Antibiotics (MDPI)', d)  # noqa: E731
    evi = lambda d: web('amikacina-iv', 'PMC13421665', 'Communications Medicine (Nature)', d)  # noqa: E731
    ewi = lambda d: web('amikacina-iv', 'eyewiki.org/Endophthalmitis', 'Academia Americana de Oftalmología (EyeWiki)', d, anio=2026)  # noqa: E731
    cam = lambda d: web('amikacina-iv', '8285892', 'Archives of Ophthalmology', d)  # noqa: E731
    cam91 = lambda d: web('amikacina-iv', '2064573', 'Archives of Ophthalmology', d)  # noqa: E731
    s_f = fen('Endoftalmitis empírica: amikacina 0,4 mg/0,1 ml como alternativa a la ceftazidima')
    s_c = consenso('Tabla 4: amikacina 100–400 µg/0,1 ml')
    f['amikacina'] = ficha(
        'amikacina', 'Amikacina intravítrea', 'antibiotico', ['intravitreo'],
        [pres('amp-100', 'solucion', 100, 'mg', isp('F-7616/26 Amikacina solución inyectable 100 mg/2 mL'), volumen=2, isp_codigos=['F-7616/26'],
              nota='Ampolla de uso intravenoso (50 mg/ml). Hay otras concentraciones registradas (p. ej. F-7617/21).')],
        [dosis('Endoftalmitis bacteriana: alternativa cuando no se puede usar ceftazidima', 'intravitrea',
               '0,4 mg en 0,1 ml (4 mg/ml) en inyección intravítrea, dosis única. Evitar repetir las inyecciones por la toxicidad retiniana.',
               final(0.4, 'mg', 0.1), s_f, estatus='off_label', condicion='La ficha técnica de la amikacina no incluye la vía intravítrea.',
               tambien=[evi('Ensayo EVIAN: amikacina 0,4 mg/0,1 ml'), ewi('Amikacina 400 µg/0,1 mL (alternativa en alérgicos a penicilina)')])],
        sin_pauta=None,
        protocolos=[],
        pediatria=('sin_datos', 'Las fuentes consultadas no traen una pauta pediátrica.'),
        alertas=['RIESGO DE INFARTO MACULAR: la amikacina y la gentamicina en dosis bajas pueden causar infarto macular (Campochiaro y Lim 1994); en la encuesta de 1991 hubo 5 casos atribuidos a amikacina.',
                 'Evitar las inyecciones repetidas de amikacina por la toxicidad retiniana (Fenniri 2026).',
                 'Una dosis mal diluida es el riesgo central: las dosis las prepara el farmacéutico con protocolos escritos para prevenir errores de dilución (Campochiaro y Lim 1994).',
                 'Esta ficha no trae pasos de preparación: ninguna fuente aceptable los describe paso a paso.'],
        discrepancias=[disc('Dosis intravítrea de amikacina por 0,1 ml',
                            [(s_f['ref'], '0,4 mg/0,1 ml (Fenniri 2026)'), (s_c['ref'], '100 a 400 µg/0,1 ml (tabla 4 del consenso, concentraciones estudiadas)')],
                            '0,4 mg/0,1 ml', 'La tabla del consenso es de estabilidad y lista un rango; las publicaciones clínicas usan 0,4 mg.')],
    )
    cam('Amikacina y gentamicina en dosis bajas pueden causar infarto macular (estudio de 1994)')
    cam91('Encuesta de especialistas de retina: 5 casos de infarto macular atribuidos a amikacina (1991)')

    # ---------------------------------------------------------------- anfotericina B
    ewi = lambda d: web('anfotericina-iv', 'eyewiki.org/Endophthalmitis', 'Academia Americana de Oftalmología (EyeWiki)', d, anio=2026)  # noqa: E731
    leu = lambda d: web('anfotericina-iv', 'PMC6907248', 'International Journal of Retina and Vitreous', d)  # noqa: E731
    kan = lambda d: web('anfotericina-iv', 'PMC13676249', 'Investigative Ophthalmology & Visual Science', d)  # noqa: E731
    s_e = ewi('Anfotericina B 5–10 µg/0,1 mL')
    s_l = leu('Anfotericina B en dextrosa al 5 % (5 µg/0,1 ml)')
    s_k = kan('Aspergillus: anfotericina B 10 µg/0,1 ml')
    f['anfotericina-b'] = ficha(
        'anfotericina-b', 'Anfotericina B intravítrea', 'antifungico', ['intravitreo'],
        [pres('vial-50', 'polvo', 50, 'mg', dm('anfotericina-b', 'Vial con 50 mg de anfotericina B (etiqueta de la forma liposomal, uso intravenoso)'),
              nota='La etiqueta consultada es de la forma liposomal de uso intravenoso. La dosis intravítrea publicada es de anfotericina B convencional '
                   'diluida en dextrosa al 5 %; confirma con farmacia qué forma se usa en el pabellón. No hay registro en el ISP (31-oct-2026).')],
        [dosis('Endoftalmitis fúngica', 'intravitrea',
               '5 a 10 µg en 0,1 ml en inyección intravítrea, diluida en dextrosa al 5 %, en general combinada con voriconazol.',
               final_rango(5, 10, 'mcg', 0.1), s_e, estatus='off_label', condicion='La ficha técnica no incluye la vía intravítrea.',
               tambien=[s_l, s_k])],
        registro='no_registrado',
        protocolos=[],
        pediatria=('sin_datos', 'Las fuentes consultadas no traen una pauta pediátrica.'),
        alertas=['La anfotericina B puede causar toxicidad retiniana (EyeWiki).',
                 'Un error de unidades es posible: 5 µg/0,1 ml no es 0,5 mg/0,1 ml (Leung 2019 cita ambas cifras). Esta ficha no trae pasos de preparación: se descartaron las recetas de fuentes con errores de unidades.',
                 'Con aceite de silicona no se recuperó la anfotericina B a las concentraciones intravítreas (Leung 2019, estudio in vitro).'],
        discrepancias=[disc('Dosis intravítrea de anfotericina B por 0,1 ml',
                            [(s_e['ref'], '5 a 10 µg/0,1 ml'), (s_l['ref'], '5 µg/0,1 ml'), (s_k['ref'], '10 µg/0,1 ml')],
                            '5 a 10 µg/0,1 ml', 'Cada estudio usó una cifra distinta dentro del mismo rango; no hay guía que fije una sola.')],
    )

    # ---------------------------------------------------------------- voriconazol
    p = lambda d: sefh_pnt(PNT_VORI, d)  # noqa: E731
    kan = lambda d: web('anfotericina-iv', 'PMC13676249', 'Investigative Ophthalmology & Visual Science', d)  # noqa: E731
    s_p = p('Posología: 100 microgramos/0,1 ml por vía intravítrea')
    s_k = kan('Aspergillus: voriconazol 50 µg/0,1 mL')
    f['voriconazol'] = ficha(
        'voriconazol', 'Voriconazol intravítreo', 'antifungico', ['intravitreo'],
        [pres('vial-200', 'polvo', 200, 'mg', isp('F-22354/25 Fusitop liofilizado para solución inyectable 200 mg (voriconazol)'), isp_codigos=['F-22354/25'],
              nota='Vial de uso intravenoso; el uso intravítreo es off-label. Medicamento peligroso (lista NIOSH 3).')],
        [dosis('Endoftalmitis fúngica', 'intravitrea',
               '100 µg en 0,1 ml (1 mg/ml) en inyección intravítrea.',
               final(100, 'mcg', 0.1), s_p, estatus='off_label', condicion='Preparación magistral del PNT; el voriconazol no tiene indicación intravítrea en su ficha.',
               tambien=[s_k])],
        protocolos=[
            protocolo('pnt-sefh-1-mg-ml', 0, 'Desde el vial de 200 mg (PNT SEFH)', 'vial-200',
                      [reconstituir('agua para inyección: agregar 19 ml, a través de un filtro de sistema cerrado (quedan 20 ml a 10 mg/ml)', 20),
                       texto('Agitar suavemente hasta que la solución esté libre de partículas visibles.'),
                       diluir(1, 10, 'cloruro de sodio 0,9 %'),
                       texto('Queda a 1 mg/ml (1000 µg/ml). Filtrar (0,22 µm) 0,5 ml sobre jeringas de 1 ml a través de su cono y tapar con tapón estéril.')],
                      (500, 'mcg', 0.5), p('Método específico, pasos 1 a 6'))],
        pediatria=('sin_datos', 'El PNT cita un caso pediátrico en su bibliografía, pero no da una pauta; no se carga.'),
        conservacion=[conserv('Jeringa preparada: 9 días refrigerada (2–8 °C) o 45 días congelada (−20 °C), protegida de la luz y la humedad.', p('Conservación y plazo de validez: 9 días'), horas=216)],
        contraindicaciones=['Hipersensibilidad al principio activo o a algún excipiente (ficha técnica de uso intravenoso, CIMA 4.3).'],
        alertas=['Desechar si hay partículas, precipitado o color amarillo oscuro (PNT SEFH).',
                 'Medicamento peligroso (NIOSH 3): preparar en campana de flujo laminar y valorar con el servicio de prevención si hace falta cabina de seguridad biológica (PNT SEFH).'],
        discrepancias=[disc('Dosis intravítrea de voriconazol por 0,1 ml',
                            [(s_p['ref'], '100 µg/0,1 ml (PNT SEFH)'), (s_k['ref'], '50 µg/0,1 ml (Kang 2026, Aspergillus)')],
                            '100 µg/0,1 ml', 'El PNT fija 100 µg; una serie clínica de endoftalmitis por Aspergillus usó 50 µg.')],
    )

    # ---------------------------------------------------------------- ganciclovir
    p = lambda d: sefh_pnt(PNT_GANCI, d)  # noqa: E731
    su = lambda d: web('foscarnet-iv', 'PMC13665908', 'Journal (revisión narrativa)', d, anio=2026)  # noqa: E731
    s_p = p('Composición: 10 mg de ganciclovir en 0,5 ml (20 mg/ml) = 2 mg/0,1 ml')
    s_c = consenso('Tabla 4: ganciclovir 200 µg/0,1 ml y 400 µg/0,1 ml (periodo de validez)')
    f['ganciclovir'] = ficha(
        'ganciclovir', 'Ganciclovir intravítreo', 'antiviral', ['intravitreo'],
        [pres('vial-500', 'polvo', 500, 'mg', isp('F-27539/23 Cymevene liofilizado para solución inyectable 500 mg (ganciclovir)'), isp_codigos=['F-27539/23'],
              nota='Vial de uso intravenoso; el uso intravítreo es off-label. Medicamento peligroso (lista NIOSH 2).')],
        [dosis('Retinitis por citomegalovirus y otras infecciones intraoculares por CMV', 'intravitrea',
               '2 mg en 0,1 ml (20 mg/ml) en inyección intravítrea: dos dosis semanales durante tres semanas como inducción y luego una inyección semanal de mantenimiento. '
               'Se han descrito dosis de hasta 3000 µg/0,1 ml.',
               final(2, 'mg', 0.1), s_p, estatus='off_label', condicion='Preparación magistral del PNT (2017); el ganciclovir no tiene indicación intravítrea en su ficha.',
               tambien=[su('Guía NIH citada por Su 2026: ganciclovir intravítreo 2 mg por inyección')])],
        protocolos=[
            protocolo('pnt-sefh-20-mg-ml', 0, 'Desde el vial de 500 mg (PNT SEFH)', 'vial-500',
                      [reconstituir('agua para inyección: agregar 10 ml (queda a 50 mg/ml)', 10),
                       diluir(2, 5, 'cloruro de sodio 0,9 %'),
                       texto('Homogeneizar la mezcla en la misma jeringa de 5 ml (queda a 20 mg/ml).'),
                       texto('Filtrar (0,22 µm) 0,5 ml sobre una jeringa de insulina de 1 ml, tapar, envasar y etiquetar. No usar agua bacteriostática con parabenos: precipita.')],
                      (10, 'mg', 0.5), p('Método específico, pasos 1 a 5'))],
        pediatria=('sin_datos', 'El PNT y las fuentes consultadas no traen una pauta pediátrica.'),
        conservacion=[conserv('Jeringa preparada: 9 días refrigerada (2–8 °C) o 45 días congelada (−20 °C), protegida de la luz y la humedad. No usar si hay partículas, precipitado u oscurecimiento.',
                              p('Conservación y plazo de validez: 9 días'), horas=216)],
        contraindicaciones=['Hipersensibilidad al ganciclovir, al valganciclovir o a algún excipiente (ficha técnica de uso intravenoso, CIMA 4.3).'],
        alertas=['Potencial mutagénico y carcinogénico: medicamento peligroso (NIOSH 2). Preparar en cabina de seguridad biológica con doble guante, bata y mascarilla FFP3 (PNT SEFH).',
                 'No usar agua bacteriostática con parabenos: son incompatibles con el ganciclovir y producen precipitación (PNT SEFH).'],
        discrepancias=[disc('Dosis intravítrea de ganciclovir por 0,1 ml',
                            [(s_p['ref'], '2 mg/0,1 ml (20 mg/ml, PNT SEFH)'), (s_c['ref'], '200 y 400 µg/0,1 ml (tabla 4 del consenso, estudios de estabilidad)')],
                            '2 mg/0,1 ml',
                            'La tabla del consenso es de periodos de validez: lista las concentraciones de los estudios de estabilidad, que no coinciden con la dosis del PNT ni con la guía NIH citada. '
                            'Se muestra la dosis del PNT; confirma con tu servicio de farmacia.')],
    )

    # ---------------------------------------------------------------- foscarnet
    ami = lambda d: web('foscarnet-iv', 'PMC13087365', 'Journal of Ophthalmic Inflammation and Infection', d, anio=2026)  # noqa: E731
    su = lambda d: web('foscarnet-iv', 'PMC13665908', 'Journal (revisión narrativa)', d, anio=2026)  # noqa: E731
    tho = lambda d: web('foscarnet-iv', 'PMC13283819', 'Journal (serie de casos)', d, anio=2026)  # noqa: E731
    s_a = ami('Foscarnet intravítreo 1,2 mg/0,05 mL bajo anestesia y luego en consulta')
    s_s = su('Guía NIH citada: foscarnet 2,4 mg por inyección, semanal en la inducción')
    s_t = tho('Necrosis retinal aguda: foscarnet 1,2–2,4 mg/0,1 mL dos veces por semana')
    f['foscarnet'] = ficha(
        'foscarnet', 'Foscarnet intravítreo', 'antiviral', ['intravitreo'],
        [pres('sol-24', 'solucion', 24, 'mg', isp('F-27647/23 Foscarnet sódico hexahidrato solución inyectable 24 mg/mL'), volumen=1, isp_codigos=['F-27647/23'], uso_directo=True,
              nota='Solución de uso intravenoso a 24 mg/ml. El ISP no informa el contenido del envase: se modela por 1 ml para expresar la concentración. '
                   'La dosis intravítrea publicada tiene la misma concentración (24 mg/ml), por eso se usa sin diluir.')],
        [dosis('Retinitis por citomegalovirus y necrosis retinal aguda: complemento del tratamiento sistémico', 'intravitrea',
               '2,4 mg en 0,1 ml (24 mg/ml) en inyección intravítrea; algunas series usan 1,2 mg en 0,05 ml (misma concentración). La frecuencia varía entre las fuentes (semanal o dos veces por semana).',
               final(2.4, 'mg', 0.1), s_s, estatus='off_label', condicion='La ficha técnica del foscarnet no incluye la vía intravítrea.',
               presentaciones=['sol-24'], tambien=[s_a, s_t])],
        protocolos=[],
        pediatria=('sin_datos', 'Las fuentes consultadas no traen una pauta pediátrica.'),
        alertas=['Esta ficha no trae pasos de preparación: ninguna fuente aceptable los describe paso a paso. La guía NIH/CDC/IDSA no se pudo leer directamente (403); se cita a través de Su 2026.',
                 'Con 1,2 mg en 0,05 ml y 2,4 mg en 0,1 ml la concentración es la misma (24 mg/ml): confirma el volumen que se va a inyectar antes de cargar la jeringa.'],
        discrepancias=[disc('Frecuencia de las inyecciones intravítreas de foscarnet',
                            [(s_s['ref'], 'Una vez por semana durante la inducción (guía NIH, citada por Su 2026)'),
                             (s_a['ref'], 'Dos veces por semana (Amiri 2026)'), (s_t['ref'], 'Dos veces por semana (Thompson 2026)')],
                            'La frecuencia la fija el oftalmólogo tratante',
                            'Las series clínicas usan dos veces por semana y la guía citada una vez por semana; no se muestra una pauta única.')],
    )

    # ---------------------------------------------------------------- clindamicina
    soh = lambda d: web('clindamicina-iv', '20708269', 'Ophthalmology', d)  # noqa: E731
    cas = lambda d: web('clindamicina-iv', 'PMC12277979', 'Romanian Journal of Ophthalmology', d)  # noqa: E731
    hos = lambda d: web('clindamicina-iv', 'PMC4329957', 'Journal of Ophthalmic & Vision Research', d, anio=2015)  # noqa: E731
    s_s = soh('Ensayo aleatorizado: 1 mg de clindamicina intravítrea y 400 µg de dexametasona')
    s_c = cas('Protocolo más usado: clindamicina 1,0 mg/0,1 ml con dexametasona 0,4 mg/0,1 ml')
    s_h = hos('Clindamicina 1,5 mg/0,1 mL semanal o cada 4 semanas en el embarazo')
    f['clindamicina'] = ficha(
        'clindamicina', 'Clindamicina intravítrea', 'antibiotico', ['intravitreo'],
        [pres('amp-600', 'solucion', 600, 'mg', isp('F-16339/22 Clindamicina solución inyectable 600 mg/4 mL'), volumen=4, isp_codigos=['F-16339/22'],
              nota='Ampolla de uso intravenoso (150 mg/ml). El uso intravítreo es off-label.')],
        [dosis('Retinocoroiditis toxoplásmica', 'intravitrea',
               '1 mg en 0,1 ml (10 mg/ml) en inyección intravítrea, una a tres inyecciones, habitualmente junto con dexametasona 0,4 mg/0,1 ml.',
               final(1, 'mg', 0.1), s_c, estatus='off_label', condicion='La ficha técnica de la clindamicina no incluye la vía intravítrea.', tambien=[s_s])],
        protocolos=[],
        pediatria=('sin_datos', 'Las fuentes consultadas no traen una pauta pediátrica.'),
        alertas=['Esta ficha no trae pasos de preparación: ninguna fuente aceptable los describe. La concentración de la ampolla (150 mg/ml) es 15 veces la de la dosis (10 mg/ml): '
                 'no la inyectes sin diluir y deja la dilución a farmacia.',
                 'Se reserva para embarazadas y para quienes no toleran el tratamiento oral (Gupta 2026).'],
        discrepancias=[disc('Dosis intravítrea de clindamicina por 0,1 ml',
                            [(s_c['ref'], '1,0 mg/0,1 ml (protocolo más usado)'), (s_s['ref'], '1 mg (ensayo aleatorizado)'), (s_h['ref'], '1,5 mg/0,1 ml (un estudio citado)')],
                            '1 mg/0,1 ml', 'La dosis de 1 mg es la mayoritaria; un estudio citado usó 1,5 mg.')],
    )

    # ---------------------------------------------------------------- metotrexato
    fre = lambda d: web('metotrexato-iv', '18303160', 'British Journal of Ophthalmology', d)  # noqa: E731
    cio = lambda d: web('metotrexato-iv', 'PMC13565040', 'Cancers (MDPI)', d)  # noqa: E731
    lira = lambda d: web('metotrexato-iv', 'PMC12997583', 'Arquivos Brasileiros de Oftalmologia', d)  # noqa: E731
    s_f = fre('Protocolo: 400 µg/0,1 ml dos veces por semana por 4 semanas, luego semanal por 8 y mensual por 9 meses')
    s_c = cio('Metotrexato 400 µg/0,1 mL en protocolos de inducción, consolidación y mantenimiento')
    s_l = lira('Metotrexato intravítreo habitualmente a 400 µg/0,1 mL')
    f['metotrexato'] = ficha(
        'metotrexato', 'Metotrexato intravítreo', 'antimetabolito', ['intravitreo'],
        [pres('amp-50', 'solucion', 50, 'mg', isp('F-19444/22 Metotrexato solución inyectable 50 mg/2 mL'), volumen=2, isp_codigos=['F-19444/22'],
              nota='Ampolla de uso intravenoso (25 mg/ml). El uso intravítreo es off-label. Medicamento peligroso.')],
        [dosis('Linfoma vitreorretinal primario; uveítis y otras indicaciones', 'intravitrea',
               '400 µg en 0,1 ml (4 mg/ml) en inyección intravítrea. Los esquemas varían: 25 inyecciones en 12 meses (Frenkel) o una fase inicial de 7 inyecciones; '
               'la frecuencia y la cantidad total las define el oncólogo y el oftalmólogo.',
               final(400, 'mcg', 0.1), s_f, estatus='off_label', condicion='La ficha técnica del metotrexato no incluye la vía intravítrea.', tambien=[s_c, s_l])],
        protocolos=[],
        pediatria=('sin_datos', 'Las fuentes consultadas no traen una pauta pediátrica.'),
        alertas=['Esta ficha no trae pasos de preparación: ninguna fuente aceptable los describe. La ampolla (25 mg/ml) es unas 60 veces la concentración de la dosis (4 mg/ml): deja la dilución a farmacia.',
                 'La queratopatía es el efecto adverso más frecuente y se relaciona con la frecuencia de las inyecciones y la dosis acumulada (Cioboată 2026).',
                 'Dosis más altas pueden causar toxicidad ocular (Lira 2025).'],
        discrepancias=[],
    )

    # ---------------------------------------------------------------- ocriplasmina
    c = lambda d: cima('ocriplasmina', '113819002', d)  # noqa: E731
    f['ocriplasmina'] = ficha(
        'ocriplasmina', 'Ocriplasmina intravítrea (Jetrea)', 'enzima', ['intravitreo'],
        [pres('jetrea-0-375', 'solucion', 0.375, 'mg', c('6.5 Jetrea 0,375 mg/0,3 ml: formulación lista para inyectar'), volumen=0.3, uso_directo=True,
              nota='Formulación lista para inyectar, que no requiere dilución. No aparece en el ISP (31-oct-2026).')],
        [dosis('Tracción vitreomacular, incluso con agujero macular de diámetro menor o igual a 400 micrones', 'intravitrea',
               '0,125 mg en 0,1 ml en inyección intravítrea única. Solo se inyectan 0,1 ml de los 0,3 ml del vial; el resto se descarta.',
               final(0.125, 'mg', 0.1), c('4.2 Posología: 0,125 mg en 0,1 ml de la solución administrados mediante inyección intravítrea'), estatus='autorizada',
               condicion='Autorizada en España (CIMA). No figura en el registro del ISP.', presentaciones=['jetrea-0-375'])],
        registro='no_registrado',
        pediatria=('no_establecida', 'No hay recomendación de uso específica en menores de 18 años para la tracción vitreomacular (CIMA 4.2).'),
        conservacion=[conserv('Se conserva congelado (−20 °C) hasta 3 años. Ya descongelado: en nevera (2–8 °C) hasta 1 semana, o por debajo de 25 °C hasta 8 horas. No volver a congelar.', c('6.3 Periodo de validez'), horas=8)],
        contraindicaciones=['Hipersensibilidad al principio activo o a algún excipiente; infecciones oculares o perioculares activas o sospechadas (CIMA 4.3).'],
        alertas=['Solo se inyectan 0,1 ml del total de 0,3 ml del vial: descarta el resto antes de inyectar (CIMA 4.2).',
                 'Se notificó un caso de subluxación o facodonesis del cristalino en ensayos clínicos en adultos, posiblemente relacionado con el tratamiento (CIMA 4.4).'],
    )

    return f
