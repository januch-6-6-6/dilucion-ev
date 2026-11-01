"""Oftalmología, lote 1: intracamerales (cefuroxima y moxifloxacino piloto; el resto se agrega en la Tarea 6)."""
from .comun import (cargar, cima, conserv, consenso, diluir, disc, dm, dosis, ficha, final, final_rango, isp, pres,
                    ped, protocolo, reconstituir, sefh_pnt, texto, web)

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
               'ASCRS 2023, alternativa: 0,5 ml de una solución al 0,1 % (1 mg/ml), que también da 0,5 mg en total. '
               'Se obtiene, por ejemplo, diluyendo la solución al 0,5 % de 1 ml a 5 ml.',
               final(0.5, 'mg', 0.5), sura('Dosis ASCRS: 0,5 mg con 0,1 ml de solución al 0,5 % o 0,5 ml de una al 0,1 %'),
               estatus='off_label',
               condicion='Misma recomendación ASCRS leída de forma secundaria. Solo cambia la concentración y el volumen; la dosis total es la misma.'),
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
            protocolo('arshinoff-3-7', 2, 'Arshinoff: 3 ml de moxifloxacino 0,5 % + 7 ml de BSS', 'oftalmica-0-5',
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

    # ---------------------------------------------------------------- carbacol (Miostat)
    d = lambda t: dm('carbacol', t)  # noqa: E731
    f['carbacol'] = ficha(
        'carbacol', 'Carbacol intracameral (Miostat)', 'miotico', ['intracameral'],
        [pres('miostat-1-5ml', 'solucion', 150, 'mcg', d('How supplied: vial de 2,0 mL con 1,5 mL de llenado; carbacol 0,01 %'), volumen=1.5,
              uso_directo=True, nota='Carbacol 0,01 % (0,1 mg/ml), listo para usar. Sin registro en el ISP.')],
        [dosis('Miosis durante la cirugía (y menor alza de la presión intraocular en las primeras 24 h tras catarata)', 'intracameral',
               'Instilar suavemente en la cámara anterior no más de 0,5 ml (50 µg), antes o después de asegurar las suturas. La miosis es máxima a los 2 a 5 minutos.',
               final(50, 'mcg', 0.5), d('Dosage and administration: no más de medio mililitro; usual dosage 0,5 mL'), estatus='autorizada',
               condicion='Autorizada por la FDA (etiqueta de DailyMed). No está registrada en Chile.')],
        registro='no_registrado',
        pediatria=('sin_datos', 'La etiqueta consultada no trae una pauta pediátrica.'),
        conservacion=[conserv('Guardar a 15–30 °C. Dosis única: desechar lo que sobre.', d('Storage: 15° a 30 °C; single-dose'))],
        contraindicaciones=['Hipersensibilidad a cualquier componente (FDA).'],
        alertas=['Retirar el contenido con una jeringa seca y reemplazar la aguja por una cánula atraumática antes de instilar (FDA).',
                 'Precaución en insuficiencia cardíaca aguda, asma bronquial, úlcera péptica, hipertiroidismo, espasmo gastrointestinal, '
                 'obstrucción urinaria y enfermedad de Parkinson (FDA).'],
    )

    # ---------------------------------------------------------------- acetilcolina (Miochol-E)
    d = lambda t: dm('acetilcolina', t)  # noqa: E731
    c = lambda t: cima('acetilcolina', '58154', t)  # noqa: E731  Acetilcolina 10 mg/ml Cusí
    f['acetilcolina'] = ficha(
        'acetilcolina', 'Acetilcolina intracameral (Miochol-E)', 'miotico', ['intracameral'],
        [pres('miochol-20', 'polvo', 20, 'mg', d('Kit: vial de 20 mg de acetilcolina + ampolla de diluyente; 20 mg/2 mL (10 mg/mL)'),
              nota='Kit con vial de polvo, ampolla de diluyente y filtro de 0,2 µm. Sin registro en el ISP.')],
        [dosis('Miosis rápida tras sacar el cristalino, en queratoplastia penetrante, iridectomía y otra cirugía del segmento anterior', 'intracameral',
               'Instilar suavemente en la cámara anterior, paralelo a la cara del iris y tangencial al borde pupilar. En la mayoría de los casos bastan 0,5 a 2 ml '
               'de la solución de 10 mg/ml. La miosis dura 10 a 20 minutos y la aplicación puede repetirse.',
               final(10, 'mg', 1), d('Dosage and administration: 0,5 a 2 mL producen miosis satisfactoria'), estatus='autorizada',
               condicion='Autorizada por la FDA y por la AEMPS (Acetilcolina 10 mg/ml Cusí). No está registrada en Chile.',
               tambien=[c('4.2.1 Posología: 0,5 a 2 ml; el efecto se mantiene 10-20 minutos')])],
        protocolos=[protocolo('miochol-kit', 0, 'Miochol-E: disolver el vial con el diluyente del kit', 'miochol-20',
                              [reconstituir('diluyente del kit (2 ml)', 2),
                               texto('Agitar suavemente hasta disolver, aspirar la solución, retirar la aguja y acoplar el filtro de 0,2 µm y luego una cánula roma.'),
                               texto('No aspirar e inyectar por el mismo filtro y no reutilizarlo.')],
                              (10, 'mg', 1), d('Directions for preparing Miochol-E, pasos 1 a 9 (20 mg/2 mL = 10 mg/mL)'))],
        registro='no_registrado',
        pediatria=('no_establecida', 'La seguridad y eficacia en pacientes pediátricos no se han establecido (FDA y CIMA).'),
        conservacion=[conserv('Las soluciones acuosas de acetilcolina son inestables: preparar justo antes de usar y desechar lo que sobre. '
                              'Guardar el kit a 4–25 °C.', d('Warnings y Storage: 4 °C a 25 °C'))],
        contraindicaciones=['Hipersensibilidad a cualquier componente (FDA y CIMA).'],
        alertas=['No usar la solución si no está clara e incolora (FDA).',
                 'En cirugía de catarata, usarla solo después de sacar el cristalino; antes hay que liberar las sinequias que impidan la miosis (FDA).',
                 'El filtro del kit tiene un volumen muerto de unos 0,6 ml (FDA).',
                 'Una sobredosis se parece a la absorción sistémica: bradicardia, hipotensión, rubor, disnea e hiperhidrosis (CIMA 4.9).'],
    )

    # ---------------------------------------------------------------- Omidria (fenilefrina + ketorolaco)
    d = lambda t: dm('fenilefrina-ketorolaco', t)  # noqa: E731
    f['fenilefrina-ketorolaco'] = ficha(
        'fenilefrina-ketorolaco', 'Fenilefrina + ketorolaco intraocular (Omidria)', 'midriatico', ['intracameral'],
        [pres('omidria-4ml', 'solucion', 40.64, 'mg', d('How supplied: vial de 5 mL con 4 mL; fenilefrina 10,16 mg/mL y ketorolaco 2,88 mg/mL'), volumen=4,
              nota='Concentrado de 4 ml. La cantidad corresponde a la fenilefrina (10,16 mg/ml); lleva además ketorolaco 2,88 mg/ml. Sin registro en el ISP.')],
        [dosis('Mantener la midriasis y reducir el dolor posoperatorio en cirugía de catarata o cambio de lente', 'topica_intraoperatoria',
               'Se agrega a la solución de irrigación ocular: 4 ml de Omidria en 500 ml de solución de irrigación, que se usa según se necesite en la cirugía '
               '(fenilefrina 0,081 mg/ml y ketorolaco 0,023 mg/ml).',
               final(40.64, 'mg', 500), d('Dosage and administration: 4 mL de Omidria diluidos en 500 mL de solución de irrigación'), estatus='autorizada',
               condicion='Autorizada por la FDA. No está registrada en Chile. La cantidad es la de fenilefrina.')],
        protocolos=[protocolo('omidria-4-en-500', 0, 'Diluir un vial en 500 ml de irrigación', 'omidria-4ml',
                              [diluir(4, 500, 'solución de irrigación ocular'),
                               texto('Un vial por paciente; no sobrar para otro paciente.')],
                              (40.64, 'mg', 500), d('Dosage and administration 2.1: dilute 4 mL of OMIDRIA in 500 mL'))],
        registro='no_registrado',
        pediatria=('con_dosis', 'La FDA establece seguridad y eficacia desde neonatos hasta adolescentes.'),
        conservacion=[conserv('El producto diluido dura como máximo 4 horas a temperatura ambiente o 24 horas refrigerado.', d('Dosage and administration: storage of diluted product'),
                              horas=4)],
        contraindicaciones=['Hipersensibilidad a cualquiera de sus componentes (FDA).'],
        alertas=['Debe diluirse antes de usarlo en el ojo; no se inyecta puro (FDA).'],
    )
    f['fenilefrina-ketorolaco']['dosis'].append(dosis(
        'Mantener la midriasis y reducir el dolor posoperatorio en cirugía de catarata o cambio de lente', 'topica_intraoperatoria',
        'Misma dilución que en adultos (4 ml en 500 ml); la etiqueta no da otra pauta pediátrica.', final(40.64, 'mg', 500),
        d('Pediatric use 8.4: seguridad y eficacia establecidas desde neonatos hasta adolescentes'), estatus='autorizada', poblacion='pediatrico',
        condicion='La etiqueta no distingue una dosis pediátrica distinta.'))

    # ---------------------------------------------------------------- azul tripano (VisionBlue)
    d = lambda t: dm('azul-tripano', t)  # noqa: E731
    f['azul-tripano'] = ficha(
        'azul-tripano', 'Azul tripano (VisionBlue)', 'colorante', ['intracameral'],
        [pres('visionblue-0-5ml', 'jeringa_precargada', 0.3, 'mg', d('How supplied: jeringa de 2,25 mL llenada a 0,5 mL; azul tripano 0,06 %'), volumen=0.5,
              uso_directo=True, nota='Azul tripano 0,06 % (0,6 mg/ml), jeringa de un solo paciente. Sin registro en el ISP (los colorantes pueden entrar como dispositivo).')],
        [dosis('Teñir la cápsula anterior del cristalino en cirugía de catarata', 'intracameral',
               'Inyectar una burbuja de aire en la cámara anterior para que el humor acuoso no diluya el colorante; aplicar el colorante sobre la cápsula con una cánula roma; '
               'la tinción es suficiente apenas el colorante toca la cápsula. Luego irrigar la cámara con BSS para sacar todo el exceso.',
               final(0.3, 'mg', 0.5), d('Dosage and administration: jeringa de 0,5 mL; aire, aplicar sobre la cápsula, irrigar con BSS'), estatus='autorizada',
               condicion='Autorizada por la FDA. No está registrada en Chile. La cantidad es el contenido de la jeringa.'),
         dosis('Teñir la cápsula anterior del cristalino en cirugía de catarata', 'intracameral',
               'La etiqueta no distingue una dosis pediátrica: misma jeringa y técnica.', final(0.3, 'mg', 0.5),
               d('Pediatric use: seguridad y eficacia establecidas en pacientes pediátricos'), estatus='autorizada', poblacion='pediatrico')],
        registro='no_registrado',
        pediatria=('con_dosis', 'La etiqueta indica que la seguridad y eficacia están establecidas; no da otra dosis.'),
        contraindicaciones=['No usar si se va a implantar un lente acrílico hidrofílico no hidratado (seco): el colorante puede teñir el lente (FDA).'],
        alertas=['Retirar de inmediato todo el exceso con irrigación profusa de la cámara anterior (FDA).',
                 'Puede teñir sin querer la cápsula posterior y la cara del vítreo; suele ceder en una semana (FDA).'],
    )

    # ---------------------------------------------------------------- azul brillante (TissueBlue)
    d = lambda t: dm('azul-brillante', t)  # noqa: E731
    f['azul-brillante'] = ficha(
        'azul-brillante', 'Azul brillante G (TissueBlue)', 'colorante', ['intracameral', 'intravitreo'],
        [pres('tissueblue-0-5ml', 'jeringa_precargada', 0.125, 'mg', d('How supplied: jeringa de 2,25 mL llenada a 0,5 mL; azul brillante G 0,025 %'), volumen=0.5,
              uso_directo=True, nota='Azul brillante G 0,025 % (0,25 mg/ml), jeringa de dosis única. Sin registro en el ISP.')],
        [dosis('Teñir la membrana limitante interna (MLI) en cirugía vítrea', 'intravitrea',
               'Inyectar con una cánula roma dentro de la cavidad vítrea llena de BSS, sin que la cánula toque la retina y sin dejar que el colorante pase bajo ella. '
               'Retirar el exceso de inmediato después de teñir.',
               final(0.125, 'mg', 0.5), d('Dosage and administration: inyectar en la cavidad vítrea llena de BSS con cánula roma'), estatus='autorizada',
               condicion='Autorizada por la FDA. No está registrada en Chile. La cantidad es el contenido de la jeringa.')],
        registro='no_registrado',
        pediatria=('no_establecida', 'La seguridad y eficacia en pacientes pediátricos no se han establecido (FDA).'),
        alertas=['Comprobar que el émbolo se mueva con suavidad antes de inyectar; si no se mueve con suavidad, no usar el producto (FDA).',
                 'Las complicaciones notificadas suelen asociarse a la cirugía: desgarro, hemorragia y desprendimiento de retina, y cataratas (FDA).'],
    )

    # ---------------------------------------------------------------- verde de indocianina
    d = lambda t: dm('verde-indocianina', t)  # noqa: E731
    f['verde-indocianina'] = ficha(
        'verde-indocianina', 'Verde de indocianina', 'colorante', ['intracameral', 'intravitreo'],
        [pres('icg-25', 'polvo', 25, 'mg', isp('F-22619/26 Verde de indocianina liofilizado para solución inyectable 25 mg'), isp_codigos=['F-22619/26'],
              nota='Registrado en Chile como inyectable; el uso para teñir la membrana limitante interna es off-label.')],
        [],
        sin_pauta='La única etiqueta consultada (DailyMed) es de uso intravenoso e intersticial. Ninguna fuente consultada trae la concentración ni los pasos '
                  'para teñir la membrana limitante interna.',
        pediatria=('sin_datos', 'Sin fuente para el uso ocular.'),
        alertas=['Uso ocular off-label sin una fuente publicada en este material: usa el protocolo de tu pabellón.'],
    )

    # ---------------------------------------------------------------- Mydrane (tropicamida + fenilefrina + lidocaína)
    c = lambda t: cima('fenilefrina-tropicamida-lidocaina', '80177', t)  # noqa: E731  Fydrane (= Mydrane)
    f['fenilefrina-tropicamida-lidocaina'] = ficha(
        'fenilefrina-tropicamida-lidocaina', 'Tropicamida + fenilefrina + lidocaína intracameral (Mydrane)', 'midriatico', ['intracameral'],
        [pres('mydrane-0-6ml', 'solucion', 6, 'mg', isp('F-25730/25 Mydrane solución inyectable'), volumen=0.6, isp_codigos=['F-25730/25'], uso_directo=True,
              nota='Ampolla de 0,6 ml con tropicamida 0,2 mg/ml, fenilefrina 3,1 mg/ml y lidocaína 10 mg/ml. La cantidad corresponde a la lidocaína. '
                   'La ficha técnica de referencia es la de Fydrane (CIMA), el mismo medicamento en España.')],
        [dosis('Midriasis intraoperatoria y anestesia en cirugía de catarata', 'intracameral',
               'Inyectar lentamente 0,2 ml en una sola inyección intracameral al inicio de la cirugía, por el puerto lateral o el principal. No inyectar dosis adicionales.',
               final(2, 'mg', 0.2), c('4.2.1 Posología: 0,2 ml en una única inyección al inicio del procedimiento'), estatus='autorizada',
               condicion='Autorizada. La cantidad es la de lidocaína (2 mg en 0,2 ml); además lleva 0,04 mg de tropicamida y 0,62 mg de fenilefrina.')],
        componentes=['Tropicamida', 'Fenilefrina', 'Lidocaína'],
        pediatria=('no_establecida', 'No se ha establecido la seguridad ni la eficacia en niños de 0 a 18 años (CIMA).'),
        conservacion=[conserv('No requiere condiciones especiales de conservación.', c('6.4 Precauciones especiales de conservación'))],
        contraindicaciones=['Véase la sección 4.3 de la ficha técnica (hipersensibilidad a los principios activos o excipientes).'],
        alertas=['No inyectar dosis adicionales a los 0,2 ml: no hay efecto acumulativo significativo y aumenta la pérdida de células endoteliales (CIMA 4.4 y 4.9).',
                 'No se recomienda con cámara anterior poco profunda ni antecedente de glaucoma agudo de ángulo cerrado: aumenta el riesgo de iridocele y de síndrome del iris flácido (CIMA 4.4).',
                 'Usar la aguja con filtro de 5 µm que viene con la ampolla y expulsar el aire de la jeringa hasta ajustar 0,2 ml (CIMA 6.6).'],
    )

    # ---------------------------------------------------------------- alteplasa (Actilyse, off-label)
    e = lambda t: web('eyewiki-tpa', 'eyewiki.org/Tissue', 'American Academy of Ophthalmology (EyeWiki)', t, anio=2026)  # noqa: E731
    c = lambda t: cima('alteplasa', '59494', t)  # noqa: E731
    f['alteplasa'] = ficha(
        'alteplasa', 'Alteplasa (Actilyse) de uso ocular', 'fibrinolitico', ['intracameral', 'intravitreo'],
        [pres('actilyse-50', 'polvo', 50, 'mg', isp('B-936/25 Actilyse, activador del plasminógeno tisular humano recombinante, liofilizado'), isp_codigos=['B-936/25'],
              nota='En el ISP figura como «activador del plasminógeno tisular humano recombinante» y no informa el tamaño del vial; se toma el de 50 mg como ejemplo. '
                   'Todo uso ocular es off-label y se prepara en condiciones estériles.')],
        [dosis('Fibrina en cámara anterior, obstrucción de un dispositivo de drenaje', 'intracameral',
               '6 a 25 µg en 0,1 ml. Fibrina ya establecida: 10 a 25 µg (empezar con menos para reducir el riesgo de sangrado). Administrar después de 5 a 9 días del posoperatorio se asocia con menos complicaciones.',
               final_rango(6, 25, 'mcg', 0.1), e('Intracameral: «Dose: 6-25 µg in 0.1 mL»; fibrina establecida 10-25 µg'), estatus='off_label'),
         dosis('Endoftalmitis o TASS con fibrina', 'intravitrea',
               'Unos 25 µg en 0,05 a 0,1 ml. En endoftalmitis mejora la visualización (la fibrina se despeja en 2 a 14 horas); en TASS, cerca del 80 % de la fibrina se resuelve en 24 horas.',
               final(25, 'mcg', 0.1), e('Intravítrea/intracameral: «Dose: ~25 µg in 0.05-0.1 mL»'), estatus='off_label',
               tambien=[consenso('Tabla 4: alteplasa intravítrea 25 µg/0,1 ml')]),
         dosis('Hemorragia submacular', 'intravitrea', '12,5 a 25 µg en 0,1 ml inyectados en el vítreo.', final_rango(12.5, 25, 'mcg', 0.1),
               e('Subretiniana: «12.5-25 µg in 0.1 mL injected intravitreally»'), estatus='off_label'),
         dosis('Hemorragia submacular', 'subretiniana', '25 a 50 µg en 0,1 a 0,2 ml directamente al espacio subretiniano con una cánula de 41 G.', None,
               e('Subretiniana: «25-50 µg in 0.1-0.2 mL injected directly into the subretinal space through a 41-gauge cannula»'), estatus='off_label'),
         dosis('Profilaxis de fibrina en cirugía pediátrica', 'intracameral', 'Unos 20 µg al terminar la cirugía reducen la fibrina posoperatoria precoz.', None,
               e('Intracameral: «Pediatric Prophylaxis: ~20 µg at the conclusion of surgery reduces early postoperative fibrin formation»'),
               estatus='off_label', poblacion='pediatrico')],
        pediatria=('con_dosis', 'EyeWiki trae una dosis de profilaxis pediátrica (~20 µg).'),
        conservacion=[conserv('Usar inmediatamente después de prepararla.', e('Preparación: «Use immediately after preparation»')),
                      conserv('Preparación intravítrea de 25 µg/0,1 ml: 365 días congelada a −70 °C.', consenso('Tabla 4: alteplasa intravítrea, 365 días a −70 °C'), horas=8760)],
        alertas=['El riesgo principal es el sangrado intraocular (hipema o resangrado), que depende de la dosis: sobre todo con más de 25 µg o en los primeros 5 a 9 días (EyeWiki).',
                 'Toxicidad retiniana a dosis altas: evitar más de 50 µg por vía intravítrea (EyeWiki).',
                 'Toxicidad endotelial dependiente de la dosis in vitro; el efecto clínico es mínimo con 25 µg/0,1 ml (EyeWiki).',
                 'Preparación según EyeWiki: reconstituir a 1 mg/ml y diluir con suero sin conservantes hasta la concentración deseada, con técnica estéril estricta. '
                 'La fuente no da los volúmenes de la dilución final (solo el valor deseado); el vial de 50 mg se reconstituye con los 50 ml de agua que trae (CIMA 6.6).'],
        discrepancias=[],
    )

    # ---------------------------------------------------------------- adrenalina intracameral (off-label)
    adr = lambda clave, inst, t, **kw: web('adrenalina-ic', clave, inst, t, **kw)  # noqa: E731
    myers09 = lambda t: adr('19185242', J_CRS, t)  # noqa: E731
    shugar = lambda t: adr('crstoday.com', 'Cataract & Refractive Surgery Today (no revisada por pares)', t, anio=2006)  # noqa: E731
    nuzzi = lambda t: adr('PMC5897993', 'Open Ophthalmology Journal', t)  # noqa: E731
    jun = lambda t: adr('PMC6081127', 'Medicine (Baltimore)', t)  # noqa: E731
    yu = lambda t: adr('PMC4745390', 'Journal of Ophthalmology (Hindawi)', t)  # noqa: E731
    kaur = lambda t: adr('PMC10491068', 'Indian Journal of Ophthalmology', t)  # noqa: E731
    f['adrenalina'] = ficha(
        'adrenalina', 'Adrenalina intracameral (sin bisulfito)', 'midriatico', ['intracameral'],
        [pres('ampolla-1mg', 'solucion', 1, 'mg', isp('F-28164/24 Epinefrina solución inyectable 1 mg/1 mL'), volumen=1, isp_codigos=['F-28164/24'],
              nota='Ampolla de 1 mg/ml (1:1000). El ISP no informa si lleva bisulfito: para el ojo debe ser sin bisulfito, confírmalo en el rótulo.')],
        [dosis('Midriasis intraoperatoria y prevención del síndrome del iris flácido (IFIS)', 'intracameral',
               'epi-Shugarcaine: adrenalina 0,025 % con lidocaína 0,75 % en BSS Plus. Se inyecta una primera dosis de cerca de 1 ml antes del viscoelástico.',
               final(0.25, 'mg', 1), shugar('Receta epi-Shugarcaine: 9 ml de BSS Plus + 3 ml de lidocaína 4 % + 4 ml de adrenalina 1:1000; inyección inicial de ~1 ml'),
               estatus='off_label', condicion='La fuente principal es una revista profesional, no revisada por pares.',
               tambien=[myers09('Composición epi-Shugarcaine: adrenalina 0,025 % y lidocaína 0,75 % en BSS Plus')]),
         dosis('Miosis intraoperatoria durante cirugía de catarata con láser de femtosegundo', 'intracameral',
               'Adrenalina 0,015 %: unos 0,1 ml (15 µg) en la cámara anterior.', final(15, 'mcg', 0.1),
               jun('Preparación 0,015 %: 0,3 ml de adrenalina 1:1000 en 1,7 ml de BSS; unos 0,1 ml inyectados'), estatus='off_label',
               condicion='Estos autores usaron adrenalina con bisulfito porque en su país no había una sin él.'),
         dosis('Dilatación pupilar en facoemulsificación', 'intracameral', 'Adrenalina 0,001 % (1:100.000): 1 ml en la cámara anterior (10 µg).',
               final(10, 'mcg', 1), yu('Preparación 1:100.000: 0,1 ml de adrenalina 0,01 % en 0,9 ml de BSS Plus; 1 ml de 0,001 % intracameral'), estatus='off_label',
               condicion='Parte de adrenalina al 0,01 %; en Chile solo figura la ampolla de 1 mg/ml, así que esta pauta no tiene protocolo.')],
        protocolos=[
            protocolo('shugar-epi-shugarcaine', 0, 'epi-Shugarcaine (receta de mezcla)', 'ampolla-1mg',
                      [texto('Mezclar 9 ml de BSS Plus, 3 ml de lidocaína al 4 % sin conservantes y 4 ml de adrenalina 1:1000 sin bisulfito (16 ml en total).'),
                       texto('Esta receta usa 4 ml de adrenalina, es decir 4 ampollas de 1 ml: no se puede comprobar con el verificador de una sola ampolla.')],
                      (0.25, 'mg', 1), shugar('Receta epi-Shugarcaine')),
            protocolo('jun-0-015', 1, 'Adrenalina 0,015 % (0,3 ml en 2 ml)', 'ampolla-1mg',
                      [diluir(0.3, 2, 'BSS')], (15, 'mcg', 0.1), jun('Preparación 0,015 %: 0,3 ml de 1:1000 diluidos en 1,7 ml de BSS'))],
        pediatria=('sin_datos', 'Las fuentes consultadas no traen una pauta pediátrica intracameral.'),
        alertas=['Las concentraciones publicadas NO son equivalentes: 0,025 % (≈1:4000, epi-Shugarcaine), 1:3000 (≈0,033 %, Nuzzi), 0,015 % (Jun) y 0,001 % (1:100.000, Yu). '
                 'No se encontró una guía de AAO, ESCRS o RCOphth con una receta propia.',
                 'Usar adrenalina sin bisulfito: el bisulfito es tóxico para el endotelio corneal (Jun 2018, Myers 2009).',
                 'El uso de adrenalina en la irrigación es off-label (Kaur 2023).',
                 'La receta epi-Shugarcaine pide lidocaína al 4 % sin conservantes; en el ISP solo aparecen ampollas de lidocaína al 1 % y 2 %.',
                 'Shugar midió un pH de 3,13 para la adrenalina sola y de 6,90 para la mezcla con BSS Plus; el BSS simple sirve de diluyente si no hay BSS Plus.'],
        discrepancias=[disc('Concentración de adrenalina intracameral',
                            [(shugar('Receta epi-Shugarcaine')['ref'], '0,025 % (≈1:4000)'),
                             (nuzzi('Preparación 1:3000 en lidocaína 2 % y BSS Plus')['ref'], '1:3000 (≈0,033 %)'),
                             (jun('Preparación 0,015 %')['ref'], '0,015 %'),
                             (yu('Preparación 1:100.000')['ref'], '0,001 % (1:100.000)')],
                            'Las tres pautas con volumen publicado (0,025 %, 0,015 % y 0,001 %)',
                            'Cada autor usa una concentración distinta y no hay una guía de sociedad que elija una. Nuzzi (1:3000) no informa el volumen inyectado, '
                            'por eso no se muestra como pauta. Verifica el protocolo de tu pabellón.')],
    )

    # ---------------------------------------------------------------- lidocaína (intracameral y bloqueos)
    lun03 = lambda t: web('lidocaina-ic', '14709298', J_CRS, t)  # noqa: E731
    esh = lambda t: web('lidocaina-ic', 'PMC4881198', 'Journal of Current Ophthalmology', t)  # noqa: E731
    moh = lambda t: web('lidocaina-ic', 'PMC6034170', 'Journal of Current Ophthalmology', t)  # noqa: E731
    rco = lambda t: web('lidocaina-ic', 'curriculum.rcophth', 'Royal College of Anaesthetists y Royal College of Ophthalmologists', t, anio=2012)  # noqa: E731
    ewr = lambda t: web('bloqueos', 'eyewiki.org/Retrobulbar', 'American Academy of Ophthalmology (EyeWiki)', t, anio=2026)  # noqa: E731
    ewo = lambda t: web('bloqueos', 'eyewiki.org/Ocular_Anesthesia', 'American Academy of Ophthalmology (EyeWiki)', t, anio=2026)  # noqa: E731
    ews = lambda t: web('bloqueos', 'eyewiki.org/Sub-Tenon', 'American Academy of Ophthalmology (EyeWiki)', t, anio=2026)  # noqa: E731
    loh = lambda t: web('bloqueos', 'PMC10614322', 'European Journal of Medical Research', t)  # noqa: E731
    sinc = 'Para uso intracameral debe ser lidocaína SIN conservantes; el ISP no informa si las ampollas de Chile los llevan: confírmalo en el rótulo.'
    f['lidocaina'] = ficha(
        'lidocaina', 'Lidocaína intracameral y de bloqueos', 'anestesico-local', ['intracameral', 'bloqueo'],
        [pres('lidocaina-1', 'solucion', 10, 'mg', isp('F-28110/24 Xylestesin solución inyectable 1 % (lidocaína clorhidrato)'), volumen=1, isp_codigos=['F-28110/24'],
              uso_directo=True, nota=f'Lidocaína al 1 % (10 mg/ml), expresada por 1 ml: el ISP no informa el contenido de la ampolla. {sinc}'),
         pres('lidocaina-2', 'solucion', 20, 'mg', isp('F-6160/25, F-28109/24 y F-29966/26: lidocaína clorhidrato 2 % solución inyectable'), volumen=1,
              isp_codigos=['F-6160/25', 'F-28109/24', 'F-29966/26'], uso_directo=True,
              nota='Lidocaína al 2 % (20 mg/ml), expresada por 1 ml: el ISP no informa el contenido de la ampolla. Es la concentración de los bloqueos.')],
        [dosis('Anestesia intracameral en cirugía de catarata', 'intracameral',
               'Lidocaína al 1 % sin conservantes: 0,15 ml (150 µl) en la técnica de Lundberg, o 0,5 ml en los casos publicados. Las inyecciones intracamerales no son totalmente seguras: se describe toxicidad epitelial y endotelial.',
               final(10, 'mg', 1), lun03('Dosis/volumen: 150 microL de lidocaína 1 % (Xylocaine) intracameral'), estatus='off_label',
               condicion='La ficha técnica de lidocaína consultada (B. Braun, CIMA) no incluye la vía intracameral.', presentaciones=['lidocaina-1'],
               tambien=[moh('Volumen: 0,5 ml de lidocaína 1 % sin conservantes y sin adrenalina intracameral')]),
         dosis('Bloqueo retrobulbar', 'retrobulbar',
               'La mezcla más usada es lidocaína 2 % con bupivacaína 0,75 %. Inyectar lentamente 2 a 4 ml (EyeWiki, retrobulbar); otra página de EyeWiki dice cerca de 5 ml. No usar vasoconstrictor.',
               None, ewr('Mezcla: lidocaína 2 % con bupivacaína 0,75 %; «Slowly inject 2 to 4 ml of anesthetic»'), estatus='off_label',
               condicion='Técnica descrita en guías; la ficha técnica de lidocaína consultada no incluye vías oculares.', presentaciones=['lidocaina-2'],
               tambien=[ewo('Retrobulbar: «usually at a volume near 5mL»')]),
         dosis('Bloqueo peribulbar', 'peribulbar', 'Lidocaína con bupivacaína, comúnmente 6 a 10 ml.', None,
               ewo('Peribulbar: «commonly 6-10mL»; la combinación de lidocaína y bupivacaína es la más popular'), estatus='off_label',
               condicion='Técnica descrita en guías; la ficha técnica de lidocaína consultada no incluye vías oculares.', presentaciones=['lidocaina-2']),
         dosis('Anestesia subtenoniana', 'subtenoniana',
               'Lidocaína 2 %, sola o mezclada con igual volumen de bupivacaína 0,5 o 0,75 %, en 2 a 5 ml. Con 2 ml suele bastar para analgesia; para acinesia se necesitan 3 a 5 ml o más. Evitar el vasoconstrictor.',
               None, ews('Lidocaína 2 %, sola o con igual volumen de bupivacaína 0,5 o 0,75 %, 2-5 ml'), estatus='off_label',
               condicion='Técnica descrita en guías; la ficha técnica de lidocaína consultada no incluye vías oculares.', presentaciones=['lidocaina-2'],
               tambien=[loh('Mezcla subtenoniana: 2,0 ml de lidocaína 20 mg/ml y 2,0 ml de bupivacaína 2,5 mg/ml')])],
        pediatria=('sin_datos', 'Las fuentes consultadas no traen una pauta pediátrica.'),
        alertas=[sinc,
                 'No repetir la lidocaína intracameral si hubo ruptura de la cápsula posterior: riesgo de toxicidad retiniana (Eshraghi 2015).',
                 'Se han descrito pérdida visual completa y transitoria tras la lidocaína intracameral, y edema macular quístico después (Eshraghi 2015; Mohammadpour 2018).',
                 'Agujas finas y cortas, no más de 25 G ni de 25 mm. Perforación del globo: 1 de cada 874 a más de 16.000 bloqueos con aguja afilada; el riesgo sube en ojos miopes con longitud axial sobre 26 mm (RCoA/RCOphth 2012).',
                 'Todos los anestésicos locales son miotóxicos: evitar inyectarlos dentro de un músculo (RCoA/RCOphth 2012).',
                 'Anestesia del tronco cerebral con bloqueos retrobulbar, peribulbar y subtenoniano: los síntomas aparecen dentro de 10 minutos (RCoA/RCOphth 2012).'],
        discrepancias=[disc('Volumen del bloqueo retrobulbar',
                            [(ewr('Retrobulbar: 2 a 4 ml')['ref'], '2 a 4 ml'), (ewo('Retrobulbar: cerca de 5 ml')['ref'], 'cerca de 5 ml')],
                            '2 a 4 ml (retrobulbar) con la otra cifra citada', 'Dos páginas de EyeWiki dan volúmenes distintos; la guía RCoA/RCOphth 2012 no trae dosis.')],
    )

    # ---------------------------------------------------------------- triamcinolona
    c = lambda t: cima('triamcinolona', '74673', t)  # noqa: E731  Triesence 40 mg/ml
    d = lambda t: dm('triamcinolona', t)  # noqa: E731
    pe = lambda t: ped('triamcinolona', t)  # noqa: E731
    f['triamcinolona'] = ficha(
        'triamcinolona', 'Triamcinolona intravítrea (Triesence)', 'corticoide', ['intracameral', 'intravitreo'],
        [pres('triesence-40', 'suspension', 40, 'mg', d('How supplied: vial de un solo uso de 1 mL con 40 mg/mL de acetónido de triamcinolona'), volumen=1, uso_directo=True,
              nota='Triesence 40 mg/ml. No está registrado en el ISP.'),
         pres('triamcinolona-40-chile', 'suspension', 40, 'mg', isp('F-20727/23, F-28605/24, F-29905/26 y F-28322/24: triamcinolona acetónido 40 mg/1 mL'), volumen=1,
              isp_codigos=['F-20727/23', 'F-28605/24', 'F-29905/26', 'F-28322/24'], uso_directo=True,
              nota='Registrada en Chile (40 mg/ml). El uso intravítreo es off-label y la preparación inyectable corriente contiene alcohol bencílico (Pediamécum).')],
        [dosis('Visualización durante la vitrectomía', 'intravitrea',
               '1 a 4 mg (25 a 100 µl de la suspensión de 40 mg/ml) por vía intravítrea. Agitar el vial con fuerza 10 segundos y revisar que no esté aglomerada. '
               'Se puede diluir con BSS, comúnmente 1:10 o 1:20 según el cirujano.',
               final(40, 'mg', 1), c('4.2.1 Posología: entre 1 y 4 mg (25 a 100 µl de suspensión de 40 mg/ml) por vía intravítrea'), estatus='autorizada',
               condicion='Autorizada con Triesence (AEMPS y FDA). No está registrada en Chile; con el frasco chileno es off-label. Cada vial es para un solo ojo.',
               tambien=[d('Dosage for visualization: 1 a 4 mg (25 a 100 microliters of 40 mg/mL) intravitreally')]),
         dosis('Uveítis y otras inflamaciones oculares que no responden a corticoides tópicos', 'intravitrea',
               'Dosis inicial de 4 mg (100 µl de la suspensión de 40 mg/ml), con dosis posteriores según la necesidad.', final(40, 'mg', 1),
               d('Dosage: initial recommended dose for all indications except visualization: 4 mg (100 microliters of 40 mg/mL)'), estatus='autorizada',
               condicion='Indicación de la etiqueta FDA de Triesence (oftalmia simpática, arteritis temporal, uveítis). No figura en la ficha técnica europea ni está registrada en Chile.',
               tambien=[pe('Vía intralesional e intraocular (acetónido): uveítis refractaria, off-label; sin dosis ocular')])],
        pediatria=('no_establecida', 'La ficha técnica no establece la seguridad ni la eficacia en menores de 18 años (CIMA).'),
        conservacion=[conserv('Una vez abierto el vial, usar la suspensión de inmediato. No congelar y proteger de la luz.', c('6.3 y 6.4'))],
        alertas=['Control de la presión intraocular tras la inyección; el riesgo de alza es mayor en pacientes predispuestos, como los diabéticos (CIMA 4.4).',
                 'La presión intraocular elevada, la endoftalmitis y las cataratas son más frecuentes cuando se usa con fines terapéuticos que para visualizar (CIMA 4.8).',
                 'Inyectar en el vítreo cuanto antes tras extraerla para que no se deposite en la jeringa; una congelación puede aglomerarla y entonces no debe usarse (CIMA 4.2).',
                 'La preparación inyectable corriente lleva alcohol bencílico y no debe usarse en recién nacidos ni prematuros (Pediamécum).'],
    )
    return f
