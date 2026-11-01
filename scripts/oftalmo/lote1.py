"""Oftalmología, lote 1: intracamerales (cefuroxima y moxifloxacino piloto; el resto se agrega en la Tarea 6)."""
from .comun import (cant, cargar, cima, conserv, consenso, diluir, disc, dosis, ficha, final, isp, pres, protocolo,
                    reconstituir, sefh_pnt, texto, web)

PNT = 'PN_CEFUROXIMA_INTRACAMERULAR'
J_CRS = 'J Cataract Refract Surg (ASCRS)'


def fichas():
    f = {}

    # ---------------------------------------------------------------- cefuroxima
    c = lambda d: cima('cefuroxima', '76098', d)  # noqa: E731  Prokam 50 mg (equivalente español de Aprokam)
    p = lambda d: sefh_pnt(PNT, d)  # noqa: E731
    f['cefuroxima'] = ficha(
        'cefuroxima', 'Cefuroxima intracameral', 'antibiotico', ['intracameral'],
        [pres('aprokam-50', 'polvo', 50, 'mg', isp('F-25555/25 Aprokam polvo para solución inyectable 50 mg'), isp_codigos=['F-25555/25'],
              nota='Vial de un solo uso. La ficha técnica de referencia es la de Prokam/Ximaract (CIMA), el mismo medicamento en España.'),
         pres('vial-750', 'polvo', 750, 'mg', p('Composición y método: reconstituir un vial de cefuroxima 750 mg'),
              nota='Vial de cefuroxima de uso sistémico. No aparece en el ISP (búsqueda por principio activo, 31-oct-2026): '
                   'el PNT español parte de él y en Chile solo está registrada la presentación de 50 mg.')],
        [dosis('Profilaxis de endoftalmitis tras cirugía de catarata', 'intracameral',
               'Inyectar lentamente 0,1 ml (1 mg) en la cámara anterior al final de la cirugía. No inyectar más de la dosis recomendada.',
               final(1, 'mg', 0.1), c('4.2.1 Posología: 0,1 ml de solución reconstituida, es decir, 1 mg de cefuroxima'),
               estatus='autorizada',
               condicion='Autorizada con Aprokam (ficha técnica). Con el vial de 750 mg es una preparación magistral del PNT de la SEFH.',
               tambien=[p('Indicaciones y posología: 1 mg (0,1 ml) intracameral al final de la cirugía'),
                        consenso('Tabla 4: cefuroxima 1 mg/0,1 ml')])],
        protocolos=[
            protocolo('aprokam-ficha-tecnica', 0, 'Aprokam: reconstitución de la ficha técnica', 'aprokam-50',
                      [reconstituir('cloruro de sodio 9 mg/ml (0,9 %)', 5),
                       texto('Agitar suavemente hasta que la solución esté libre de partículas visibles.'),
                       texto('Con una jeringa de 1 ml y una aguja con filtro de 5 micras, aspirar al menos 0,1 ml de la solución.')],
                      (1, 'mg', 0.1), c('6.6 Instrucciones de reconstitución (pasos 3 a 6)')),
            protocolo('pnt-sefh-750', 0, 'Desde el vial de 750 mg (PNT SEFH)', 'vial-750',
                      [reconstituir('agua para inyección', 7.5),
                       diluir(1, 10, 'cloruro de sodio 0,9 %'),
                       texto('Homogeneizar la mezcla en la misma jeringa (queda a 10 mg/ml).'),
                       texto('Filtrar (5 µm) 0,2 ml de esta solución sobre una jeringa de insulina de 1 ml, tapar, envasar y etiquetar. '
                             'Trabajar en campana de flujo laminar con técnica aséptica.')],
                      (1, 'mg', 0.1), p('Método específico, pasos 1 a 6'))],
        pediatria=('no_establecida', 'La ficha técnica no establece la dosis óptima ni la seguridad en población pediátrica.'),
        conservacion=[
            conserv('Aprokam, ya reconstituido: usar inmediatamente y no volver a usar. Un vial por paciente.', c('6.3 Periodo de validez')),
            conserv('Jeringa preparada según el PNT: 7 días en refrigerador (2–8 °C) o 4 meses congelada (−21 °C).', p('Plazo de validez'), horas=168),
            conserv('Jeringa preparada en farmacia: 120 días a −21 °C (categoría A+ del consenso).', consenso('Tabla de estabilidad: cefuroxima 1 mg/0,1 ml'))],
        contraindicaciones=['Hipersensibilidad a la cefuroxima o a las cefalosporinas (CIMA 4.3).'],
        alertas=['NO INYECTAR MÁS DE LA DOSIS RECOMENDADA. Un error de dilución que dio 40 a 50 veces la dosis causó inflamación grave '
                 'del segmento anterior y mala agudeza visual en 6 pacientes (CIMA 4.9).',
                 'Reacción anafiláctica: muy rara, menos de 1 en 10.000 (CIMA 4.8).',
                 'Pegar la etiqueta desprendible del vial en la historia clínica del paciente (CIMA 6.6).'],
    )

    # ---------------------------------------------------------------- moxifloxacino
    arsh = lambda d: web('moxifloxacino-ic', '28007104', J_CRS, d)  # noqa: E731  Arshinoff 2016
    myers = lambda d: web('moxifloxacino-ic', '37290753', J_CRS, d)  # noqa: E731  ASCRS 2023
    sura = lambda d: web('moxifloxacino-ic', 'PMC12577578', 'Clinical Ophthalmology (Dove Medical Press)', d)  # noqa: E731
    abuz = lambda d: web('moxifloxacino-ic', 'PMC12823917', 'Frontiers in Medicine', d)  # noqa: E731
    fenn = lambda d: web('moxifloxacino-ic', 'PMC13405202', 'Antibiotics (MDPI)', d)  # noqa: E731
    f['moxifloxacino'] = ficha(
        'moxifloxacino', 'Moxifloxacino intracameral', 'antibiotico', ['intracameral'],
        [pres('oftalmica-0-5', 'solucion', 15, 'mg', isp('F-21130/24 Megrelan solución oftálmica 0,5 %'), volumen=3, isp_codigos=['F-21130/24'],
              nota='Solución oftálmica al 0,5 % (5 mg/ml), registrada en Chile para uso tópico: el uso intracameral es off-label. '
                   'Cantidad y volumen corresponden a los 3 ml que usa el protocolo de Arshinoff; el ISP no informa el contenido del envase.')],
        [dosis('Profilaxis de endoftalmitis tras cirugía de catarata', 'intracameral',
               'ASCRS 2023: 0,5 mg en total, que se logra con 0,1 ml de la solución al 0,5 % sin diluir (o con 0,5 ml de una al 0,1 %).',
               final(0.5, 'mg', 0.1), sura('Dosis ASCRS: 0,5 mg con 0,1 ml de solución al 0,5 % o 0,5 ml de una al 0,1 %'),
               estatus='off_label',
               condicion='La recomendación de la ASCRS se leyó de forma secundaria: su texto completo es solo para socios.',
               tambien=[abuz('Tabla del ECA de Egipto 2022: 0,1 ml (0,5 mg) de moxifloxacino al 0,5 % sin diluir')]),
         dosis('Profilaxis de endoftalmitis tras cirugía de catarata', 'intracameral',
               'Arshinoff 2016: 3 ml de moxifloxacino al 0,5 % + 7 ml de BSS (1,5 mg/ml = 150 µg/0,1 ml). Se inyectan 0,3 a 0,4 ml '
               '(450 a 600 µg) por el puerto lateral al final de la cirugía, con la incisión principal sellada e hidratada.',
               final(150, 'mcg', 0.1), arsh('Resumen: dilución de 3 cc de Vigamox 0,5 % con 7 cc de BSS y 0,3 a 0,4 cc (450 a 600 mcg)'),
               estatus='off_label',
               condicion='Los 150 µg/0,1 ml son la concentración de la mezcla; la dosis que se inyecta es de 450 a 600 µg.')],
        protocolos=[
            protocolo('ascrs-sin-diluir', 0, 'ASCRS: solución al 0,5 % sin diluir', 'oftalmica-0-5',
                      [texto('Usar la solución al 0,5 % tal como viene, sin diluir.'), cargar(0.1)],
                      (0.5, 'mg', 0.1), abuz('Tabla del ECA de Egipto 2022: 0,1 ml (0,5 mg) de moxifloxacino al 0,5 % sin diluir')),
            protocolo('arshinoff-3-7', 1, 'Arshinoff: 3 ml de moxifloxacino 0,5 % + 7 ml de BSS', 'oftalmica-0-5',
                      [diluir(3, 10, 'solución salina balanceada (BSS)'),
                       texto('Inyectar 0,3 a 0,4 ml (450 a 600 µg) por el puerto lateral como último paso de la cirugía.')],
                      (150, 'mcg', 0.1), arsh('Resumen: dilución de 3 cc de Vigamox 0,5 % con 7 cc de BSS'))],
        pediatria=('sin_datos', 'Las fuentes consultadas no traen una pauta pediátrica.'),
        alertas=['La concentración y el volumen van juntos: 0,1 ml si es al 0,5 % y 0,5 ml si es al 0,1 %. Un error de dosis aumenta el riesgo '
                 'de síndrome tóxico del segmento anterior (TASS) o de endoftalmitis (ASCRS 2023).',
                 'La FDA publicó una alerta sobre eventos adversos del moxifloxacino intraocular preparado fuera de la industria (ASCRS 2023).',
                 'Preparar la mezcla en el pabellón preocupa por contaminación bacteriana, errores de dilución y TASS (Surawatsatien 2025).',
                 'Los 160 µg/0,1 ml de la tabla 4 del consenso SEFH-SEO-SERV 2025 (y de Fenniri 2026) son una dosis INTRAVÍTREA, no intracameral.',
                 'Con 100 µg/0,1 ml hubo una infección por un estafilococo resistente en 3.430 casos; por eso Arshinoff subió la dosis (Arshinoff 2016).'],
        discrepancias=[disc('Dosis intracameral por inyección',
                            [(sura('Dosis ASCRS: 0,5 mg')['ref'], '0,5 mg en total (ASCRS 2023, leída de forma secundaria)'),
                             (arsh('Resumen: 0,3 a 0,4 cc (450 a 600 mcg)')['ref'], '450 a 600 µg (0,3 a 0,4 ml de una mezcla de 1,5 mg/ml)'),
                             (abuz('La dosis varió de 150 a 500 μg por inyección')['ref'], 'Rango publicado de 150 a 500 µg por inyección'),
                             (consenso('Tabla 4: moxifloxacino 160 μg/0,1 ml (preparaciones intravítreas)')['ref'],
                              '160 µg/0,1 ml: preparación intravítrea, no intracameral'),
                             (fenn('Tabla 4: moxifloxacino 160 μg por 0,1 ml, dosis intravítrea')['ref'],
                              '160 µg/0,1 ml: dosis intravítrea, no intracameral')],
                            'Los dos protocolos citados (ASCRS y Arshinoff)',
                            'No hay una dosis única aceptada: el rango publicado va de 150 a 500 µg. Se muestran los dos protocolos con su fuente '
                            'y el verificador acepta cualquiera de los dos. Verifica el protocolo de tu pabellón.')],
    )
    return f
