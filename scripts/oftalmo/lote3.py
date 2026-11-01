"""Oftalmología, lote 3: bloqueos y perioculares (9 fichas informativas) y antifibróticos y toxina (3 fichas de alto riesgo).

Reglas del lote (ver ledger y DECISIONES.md):
- Las fichas `informativa` (bloqueos y subconjuntivales) muestran volúmenes y dosis como texto: no tienen verificador.
- Antifibróticos y toxina botulínica van como `intraocular` para poder verificar la concentración, siempre con la alerta
  «La dosis y el tiempo de aplicación los define el cirujano».
- Si una fuente no sostiene una dosis, la ficha queda `sinPauta` con su motivo (mepivacaína). No se inventa.
"""
from .comun import (cargar, cima, conserv, consenso, diluir, disc, dm, dosis, ficha, final, final_rango, isp, pres,
                    protocolo, reconstituir, texto, web)

CIRUJANO = 'La dosis y el tiempo de aplicación los define el cirujano; esta ficha solo muestra lo que publican las fuentes.'
NO_SISTEMICA = 'La ficha técnica consultada es la de uso sistémico o general y no incluye esta vía.'
EW = 'American Academy of Ophthalmology (EyeWiki)'


def fichas():
    f = {}
    rco = lambda t: web('bloqueos', 'ophthalmic-surgery-2012', 'Royal College of Anaesthetists y Royal College of Ophthalmologists', t, anio=2012)  # noqa: E731
    ewr = lambda t: web('bloqueos', 'eyewiki.org/Retrobulbar', EW, t, anio=2026)  # noqa: E731
    ewo = lambda t: web('bloqueos', 'eyewiki.org/Ocular_Anesthesia', EW, t, anio=2026)  # noqa: E731
    ews = lambda t: web('bloqueos', 'eyewiki.org/Sub-Tenon', EW, t, anio=2026)  # noqa: E731
    loh = lambda t: web('bloqueos', 'PMC10614322', 'European Journal of Medical Research', t)  # noqa: E731
    cao = lambda t: web('bloqueos', 'PMC12771858', 'BMC Ophthalmology', t)  # noqa: E731
    moh = lambda t: web('bloqueos', 'PMC10491076', 'Indian Journal of Ophthalmology', t)  # noqa: E731

    # ---------------------------------------------------------------- bupivacaína
    c = lambda d: cima('bupivacaina', '57110', d)  # noqa: E731  Bupivacaína Physan 5 mg/ml
    f['bupivacaina'] = ficha(
        'bupivacaina', 'Bupivacaína en bloqueos oculares', 'anestesico-local', ['bloqueo'],
        [pres('bupivacaina-0-5', 'solucion', 50, 'mg', isp('F-3026/25 Bupivacaína clorhidrato solución inyectable 50 mg/10 mL'), volumen=10, isp_codigos=['F-3026/25'], uso_directo=True,
              nota='Bupivacaína al 0,5 % (5 mg/ml), la concentración de la tabla de la ficha técnica. Hay otras solicitudes registradas (F-10858/21).'),
         pres('bupivacaina-0-75', 'solucion', 7.5, 'mg', isp('F-28146/24 Bupivacaína clorhidrato solución inyectable 0,75 %'), volumen=1, isp_codigos=['F-28146/24'], uso_directo=True,
              nota='Bupivacaína al 0,75 % (7,5 mg/ml), expresada por 1 ml: el ISP no informa el contenido del envase. Es la concentración de la mezcla más usada en el bloqueo retrobulbar.')],
        [dosis('Bloqueo retrobulbar en cirugía ocular', 'retrobulbar',
               'Ficha técnica (bupivacaína 5 mg/ml): 2 a 4 ml (10 a 20 mg), con inicio de acción en 5 minutos y duración de 4 a 8 horas. '
               'En la práctica se usa mezclada con lidocaína al 2 % (la combinación más usada lleva bupivacaína al 0,75 %). Sin vasoconstrictor.',
               None, c('4.2 Posología, tabla de dosis: bloqueo retrobulbar 2–4 ml, 10–20 mg, inicio 5 min, duración 4–8 h; indicación cirugía ocular'), estatus='autorizada',
               condicion='Autorizada en la ficha de referencia (Bupivacaína Physan, CIMA). Confirma la indicación en la ficha del producto chileno.',
               presentaciones=['bupivacaina-0-5', 'bupivacaina-0-75'],
               tambien=[ewr('Mezcla: lidocaína 2 % con bupivacaína 0,75 %; «Slowly inject 2 to 4 ml of anesthetic»')]),
         dosis('Bloqueo peribulbar en cirugía ocular', 'peribulbar',
               'Ficha técnica (bupivacaína 5 mg/ml): 6 a 10 ml (30 a 50 mg), con inicio de acción en 10 minutos y duración de 4 a 8 horas.',
               None, c('4.2 Posología, tabla de dosis: bloqueo peribulbar 6–10 ml, 30–50 mg, inicio 10 min, duración 4–8 h; indicación cirugía ocular'), estatus='autorizada',
               condicion='Autorizada en la ficha de referencia (Bupivacaína Physan, CIMA). Confirma la indicación en la ficha del producto chileno.',
               presentaciones=['bupivacaina-0-5'],
               tambien=[ewo('Peribulbar: «commonly 6-10mL»; la combinación de lidocaína y bupivacaína es la más popular')]),
         dosis('Anestesia subtenoniana', 'subtenoniana',
               'Lidocaína 2 %, sola o mezclada con igual volumen de bupivacaína 0,5 o 0,75 %, en 2 a 5 ml. Evitar el vasoconstrictor.',
               None, ews('Lidocaína 2 %, sola o con igual volumen de bupivacaína 0,5 o 0,75 %, 2-5 ml'), estatus='off_label',
               condicion='Técnica descrita en EyeWiki; la ficha técnica no menciona la vía subtenoniana.', presentaciones=['bupivacaina-0-5', 'bupivacaina-0-75'],
               tambien=[loh('Mezcla subtenoniana: 2,0 ml de lidocaína 20 mg/ml y 2,0 ml de bupivacaína 2,5 mg/ml')])],
        modo='informativa',
        pediatria=('sin_datos', 'Las fuentes consultadas no traen una pauta pediátrica de bloqueos oculares.'),
        contraindicaciones=['Hipersensibilidad a la bupivacaína o a otros anestésicos locales de tipo amida (CIMA 4.3).'],
        alertas=['La administración retrobulbar puede alcanzar de forma ocasional el espacio subaracnoideo y causar ceguera temporal, colapso cardiovascular, apnea y convulsiones: hay que diagnosticarlo y tratarlo rápido (CIMA 4.4).',
                 'Anestesia del tronco cerebral con bloqueos retrobulbar, peribulbar y subtenoniano: los síntomas aparecen dentro de 10 minutos (RCoA/RCOphth 2012).',
                 'Todos los anestésicos locales son miotóxicos: evitar inyectarlos dentro de un músculo (RCoA/RCOphth 2012).',
                 'Agujas finas y cortas, no más de 25 G ni de 25 mm (RCoA/RCOphth 2012). La guía RCoA/RCOphth 2012 no trae dosis.'],
        discrepancias=[disc('Concentración de la bupivacaína en la mezcla con lidocaína',
                            [(ewr('Retrobulbar: bupivacaína 0,75 %')['ref'], '0,75 % (retrobulbar)'), (ews('Subtenoniana: bupivacaína 0,5 o 0,75 %')['ref'], '0,5 o 0,75 % (subtenoniana)')],
                            '0,5 o 0,75 % según la técnica',
                            'EyeWiki da 0,75 % para el bloqueo retrobulbar y 0,5 o 0,75 % para el subtenoniano; la ficha técnica usa la de 5 mg/ml (0,5 %).')],
    )
    rco('Perforación del globo, anestesia del tronco cerebral y miotoxicidad de los anestésicos locales')

    # ---------------------------------------------------------------- ropivacaína
    c = lambda d: cima('ropivacaina', '73054', d)  # noqa: E731  Ropivacaína Kabi
    f['ropivacaina'] = ficha(
        'ropivacaina', 'Ropivacaína en bloqueos oculares', 'anestesico-local', ['bloqueo'],
        [pres('ropivacaina-7-5', 'solucion', 7.5, 'mg', c('Ropivacaína Kabi 7,5 mg/ml solución inyectable'), volumen=1, uso_directo=True,
              nota='Ropivacaína al 0,75 % (7,5 mg/ml), expresada por 1 ml. No aparece en el ISP (31-oct-2026). La ficha técnica española es de uso epidural y perineural.'),
         pres('ropivacaina-10', 'solucion', 10, 'mg', c('Ropivacaína Kabi 10 mg/ml solución inyectable'), volumen=1, uso_directo=True,
              nota='Ropivacaína al 1 % (10 mg/ml), expresada por 1 ml.')],
        [dosis('Anestesia subtenoniana en cirugía vitreorretinal y de catarata', 'subtenoniana',
               'Publicado: 2 a 4 ml de ropivacaína al 1 % (estudio citado por Lohmann 2023), o 4 ml al 0,75 % sin hialuronidasa (reporte de caso, que describe un síndrome transitorio del ápex orbitario).',
               None, loh('Estudio citado: 2,0–4,0 ml de ropivacaína 1,0 % en el espacio subtenoniano'), estatus='off_label',
               condicion='Sin guía de sociedad: solo un estudio citado y un reporte de caso. La ficha técnica consultada no incluye vías oculares.',
               presentaciones=['ropivacaina-7-5', 'ropivacaina-10'], tambien=[cao('4 ml de ropivacaína 0,75 % sin hialuronidasa, sin compresión ocular posterior')])],
        modo='informativa', registro='no_registrado',
        pediatria=('sin_datos', 'Las fuentes consultadas no traen una pauta pediátrica de bloqueos oculares.'),
        alertas=['Se describió un síndrome transitorio del ápex orbitario, con evidencia en resonancia, tras 4 ml de ropivacaína al 0,75 % en el espacio subtenoniano durante una cirugía combinada (Cao 2026, reporte de caso).',
                 'Anestesia del tronco cerebral con bloqueos retrobulbar, peribulbar y subtenoniano: los síntomas aparecen dentro de 10 minutos (RCoA/RCOphth 2012).'],
    )

    # ---------------------------------------------------------------- mepivacaína
    f['mepivacaina'] = ficha(
        'mepivacaina', 'Mepivacaína en bloqueos oculares', 'anestesico-local', ['bloqueo'],
        [pres('mepivacaina-3', 'solucion', 30, 'mg', isp('F-29363/25 y F-29940/26: mepivacaína clorhidrato solución inyectable 3 %'), volumen=1,
              isp_codigos=['F-29363/25', 'F-29940/26'], uso_directo=True,
              nota='Mepivacaína al 3 % (30 mg/ml), expresada por 1 ml. El ISP no distingue si es de uso dental ni informa el envase.')],
        [],
        modo='informativa',
        sin_pauta='Ninguna fuente consultada trae una dosis oftálmica de mepivacaína: la ficha técnica revisada (Mepivacaína Physan 20 mg/ml, infiltración) no incluye vías oculares '
                  'y ni la guía RCoA/RCOphth 2012 ni las páginas de EyeWiki sobre bloqueos la mencionan.',
        pediatria=('sin_datos', 'No se recomienda en menores de 4 años (ficha técnica CIMA); no hay pauta oftálmica.'),
        alertas=['No uses esta ficha para dosificar: no hay una dosis oftálmica respaldada. Consulta el protocolo de anestesia de tu pabellón.'],
    )

    # ---------------------------------------------------------------- hialuronidasa
    d = lambda t: dm('hialuronidasa', t)  # noqa: E731
    s_e = ewr('Hialuronidasa como adyuvante a 50 UI por ml')
    s_m = moh('Rango publicado de 0,75 a 300 UI/ml; peribulbar de 12,5 a 50 UI/ml')
    s_d = d('Aumento de la dispersión de otros fármacos: 50 a 300 unidades, lo más típico 150 USP')
    f['hialuronidasa'] = ficha(
        'hialuronidasa', 'Hialuronidasa como coadyuvante de bloqueos', 'enzima', ['bloqueo'],
        [pres('hylase-150', 'polvo', 150, 'UI', isp('B-2256/22 Hylase Dessau liofilizado para solución inyectable 150 U.I.'), isp_codigos=['B-2256/22'],
              nota='Liofilizado de 150 UI. La etiqueta de referencia (DailyMed) es la de Hylenex recombinante, de 150 unidades/ml: son productos distintos.')],
        [dosis('Coadyuvante del bloqueo peribulbar o retrobulbar', 'peribulbar',
               'Se agrega al anestésico para que se disperse mejor: 50 UI por ml de mezcla (EyeWiki). La etiqueta FDA de Hylenex indica 50 a 300 unidades, lo más típico 150 USP, antes o junto con el fármaco. '
               'El rango publicado es muy amplio: de 0,75 a 300 UI/ml, y en bloqueo peribulbar de 12,5 a 50 UI/ml.',
               None, s_e, estatus='autorizada',
               condicion='La etiqueta FDA de Hylenex incluye las vías peribulbar y retrobulbar. Hylase Dessau es otro producto: confirma su ficha en Chile.',
               presentaciones=['hylase-150'], tambien=[s_d, s_m])],
        modo='informativa',
        pediatria=('sin_datos', 'Las fuentes consultadas no traen una pauta pediátrica en bloqueos oculares.'),
        alertas=['No aplicar directamente sobre la córnea: no es de uso tópico (etiqueta FDA, 5.2).',
                 'La hialuronidasa acelera la dispersión y el inicio del bloqueo, pero la dosis no está estandarizada: confirma la del protocolo de tu pabellón.'],
        discrepancias=[disc('Concentración de la hialuronidasa en la mezcla anestésica',
                            [(s_e['ref'], '50 UI/ml'), (s_m['ref'], '0,75 a 300 UI/ml (peribulbar 12,5 a 50)'), (s_d['ref'], '50 a 300 unidades por administración (típico 150)')],
                            '50 UI/ml (EyeWiki), con el rango publicado como referencia',
                            'No hay una guía que fije la dosis; los estudios usan desde 0,75 hasta 300 UI/ml.')],
    )

    # ---------------------------------------------------------------- cefazolina
    pan = lambda t: web('subconjuntivales', 'PMC4255380', 'Jundishapur Journal of Microbiology', t)  # noqa: E731
    hos = lambda t: web('subconjuntivales', 'PMC9768931', 'International Journal of Retina and Vitreous', t)  # noqa: E731
    mak = lambda t: web('subconjuntivales', '29121356', 'Ophthalmic Surgery, Lasers and Imaging Retina', t)  # noqa: E731
    esc = lambda t: web('subconjuntivales', 'PMC13528843', 'Journal of Cataract & Refractive Surgery (guía ESCRS)', t)  # noqa: E731
    sur = lambda t: web('subconjuntivales', 'PMC12577578', 'Clinical Ophthalmology', t)  # noqa: E731
    ku = lambda t: web('subconjuntivales', 'PMC8841617', 'American Journal of Ophthalmology Case Reports', t)  # noqa: E731
    rah = lambda t: web('subconjuntivales', 'PMC9092187', 'American Journal of Ophthalmology Case Reports', t)  # noqa: E731
    s_p = pan('50 mg de cefazolina (0,5 cc de 100 mg/ml) bajo la conjuntiva')
    s_h = hos('Al final de la cirugía: cefazolina subconjuntival 50 mg y betametasona 2 mg')
    s_k = mak('0,3 ml de cefazolina + 0,2 ml de BSS (0,5 ml) subconjuntival')
    f['cefazolina'] = ficha(
        'cefazolina', 'Cefazolina subconjuntival', 'antibiotico', ['periocular'],
        [pres('vial-1g', 'polvo', 1000, 'mg', isp('F-13893/24 Cefazolina polvo para solución inyectable 1 g'), isp_codigos=['F-13893/24'],
              nota='Vial de uso intravenoso e intramuscular; el uso subconjuntival es off-label. Hay otras solicitudes registradas.')],
        [dosis('Profilaxis de endoftalmitis al final de la cirugía', 'subconjuntival',
               '50 mg bajo la conjuntiva (0,5 ml a 100 mg/ml en el estudio de Panahibazaz). Otra serie la combina con betametasona 2 mg; '
               'en cirugía retiniana se usó 0,3 ml de cefazolina con 0,2 ml de BSS, sin ventaja analgésica al mezclarla con lidocaína.',
               None, s_p, estatus='off_label', condicion=NO_SISTEMICA, presentaciones=['vial-1g'], tambien=[s_h, s_k])],
        modo='informativa',
        pediatria=('sin_datos', 'Las fuentes consultadas no traen una pauta pediátrica.'),
        alertas=['La guía ESCRS recomienda un antibiótico intracameral (p. ej. cefuroxima 1 mg/0,1 ml) al final de la cirugía de catarata; los antibióticos subconjuntivales adicionales los respalda una sola guía (Surawatsatien 2025).',
                 'Con cefuroxima subconjuntival se describió toxicidad retinal por sobredosis y por penetración escleral accidental (Ku 2022; Raharja 2022): el mismo riesgo vale para cualquier antibiótico subconjuntivo si hay error de dilución.',
                 'Ninguna guía de sociedad fija la dosis subconjuntival de antibióticos: las cifras salen de estudios aislados. Verifica el protocolo de tu pabellón.'],
    )
    esc('Intracameral cefuroxima 1 mg/0,1 ml al final de la cirugía de catarata (GRADE +++)')
    sur('Antibióticos subconjuntivales adicionales respaldados por una sola guía')
    ku('Toxicidad por cefuroxima con dosis estándar y altas por vía subconjuntival')
    rah('Toxicidad retinal por cefuroxima subconjuntival: sobredosis y penetración escleral')

    # ---------------------------------------------------------------- gentamicina
    ay = lambda t: web('subconjuntivales', 'PMC13417846', 'BMC Ophthalmology', t)  # noqa: E731
    cam91 = lambda t: web('amikacina-iv', '2064573', 'Archives of Ophthalmology', t)  # noqa: E731
    s_a = ay('Gentamicina subconjuntival 40 mg/ml, 0,5 ml (20 mg) y dexametasona 4 mg/ml, 0,5 ml (2 mg)')
    f['gentamicina'] = ficha(
        'gentamicina', 'Gentamicina subconjuntival', 'antibiotico', ['periocular'],
        [pres('amp-80', 'solucion', 80, 'mg', isp('B-1988/22 Gentamicina solución inyectable 80 mg/2 mL'), volumen=2, isp_codigos=['B-1988/22'],
              nota='Ampolla de uso intravenoso e intramuscular (40 mg/ml); el uso subconjuntival es off-label.')],
        [dosis('Profilaxis tras cirugía de catarata', 'subconjuntival',
               '20 mg (0,5 ml de la ampolla de 40 mg/ml) bajo la conjuntiva, junto con dexametasona 2 mg, al final de la cirugía.',
               None, s_a, estatus='off_label', condicion=NO_SISTEMICA, presentaciones=['amp-80'])],
        modo='informativa',
        pediatria=('sin_datos', 'Las fuentes consultadas no traen una pauta pediátrica.'),
        alertas=['RIESGO DE INFARTO MACULAR: se notificaron 23 casos tras inyecciones subconjuntivas profilácticas de aminoglucósidos después de cirugía ocular de rutina; 93 casos se atribuyeron a gentamicina (Campochiaro y Conway 1991).',
                 'Una sola serie respalda esta dosis; ninguna guía de sociedad fija la dosis subconjuntival de antibióticos. Verifica el protocolo de tu pabellón.'],
    )
    cam91('93 casos de infarto macular atribuidos a gentamicina; 23 tras inyecciones subconjuntivas profilácticas de aminoglucósidos')

    # ---------------------------------------------------------------- corticoides subconjuntivales
    bir = lambda t: web('subconjuntivales', 'PMC13415846', 'Eye (Londres)', t)  # noqa: E731
    f['metilprednisolona'] = ficha(
        'metilprednisolona', 'Metilprednisolona subconjuntival', 'corticoide', ['periocular'],
        [pres('vial-40', 'polvo', 40, 'mg', isp('F-23536/22 Metilprednisolona polvo para solución inyectable 40 mg'), isp_codigos=['F-23536/22'],
              nota='Vial de uso intravenoso e intramuscular. La fuente no precisa la sal (acetato o succinato) ni el producto usado.')],
        [dosis('Alternativa a los corticoides tópicos tras cirugía de catarata', 'subconjuntival',
               '20 mg bajo la conjuntiva (ensayo clínico citado por Birtel 2026, frente a corticoides tópicos).',
               None, bir('Metilprednisolona subconjuntival 20 mg frente a esquemas tópicos'), estatus='off_label', condicion=NO_SISTEMICA, presentaciones=['vial-40'])],
        modo='informativa',
        pediatria=('sin_datos', 'Las fuentes consultadas no traen una pauta pediátrica.'),
        alertas=['Dosis tomada de una revisión que cita un ensayo, sin guía de sociedad: las dosis subconjuntivales de corticoides son muy variables (triamcinolona de 1 a 20 mg). Verifica el protocolo de tu pabellón.'],
    )
    hos_b = hos('Al final de la cirugía: cefazolina 50 mg y betametasona 2 mg subconjuntivales')
    bir_b = bir('Betametasona acetato subconjuntival 5,7 mg frente a esquemas tópicos')
    f['betametasona'] = ficha(
        'betametasona', 'Betametasona subconjuntival', 'corticoide', ['periocular'],
        [pres('amp-4', 'solucion', 4, 'mg', isp('F-7623/26 Betametasona sodio fosfato solución inyectable 4 mg/1 mL'), volumen=1, isp_codigos=['F-7623/26'],
              nota='Betametasona fosfato 4 mg/ml. La serie de 5,7 mg usó el acetato, que no es esta presentación.')],
        [dosis('Corticoide al final de la cirugía ocular', 'subconjuntival',
               '2 mg junto con cefazolina 50 mg al final de la vitrectomía (Hosseini 2022). Un ensayo citado usó betametasona acetato 5,7 mg.',
               None, hos_b, estatus='off_label', condicion=NO_SISTEMICA, presentaciones=['amp-4'], tambien=[bir_b])],
        modo='informativa',
        pediatria=('sin_datos', 'Las fuentes consultadas no traen una pauta pediátrica.'),
        alertas=['Las dosis subconjuntivales de corticoides son muy variables entre series: verifica el protocolo de tu pabellón.'],
        discrepancias=[disc('Dosis subconjuntival de betametasona',
                            [(hos_b['ref'], '2 mg (betametasona)'), (bir_b['ref'], '5,7 mg (betametasona acetato)')],
                            '2 mg',
                            'Las dos cifras corresponden a sales y esquemas distintos; no hay una guía que fije una sola.')],
    )
    f['dexametasona'] = ficha(
        'dexametasona', 'Dexametasona subconjuntival', 'corticoide', ['periocular'],
        [pres('amp-4', 'solucion', 4, 'mg', isp('F-27214/22 Dexametasona fosfato solución inyectable 4 mg/1 mL'), volumen=1, isp_codigos=['F-27214/22'],
              nota='Dexametasona fosfato 4 mg/ml, de uso intravenoso e intramuscular.')],
        [dosis('Corticoide tras cirugía de catarata', 'subconjuntival',
               '2 mg (0,5 ml de la ampolla de 4 mg/ml) bajo la conjuntiva, junto con gentamicina 20 mg, al final de la cirugía.',
               None, s_a, estatus='off_label', condicion=NO_SISTEMICA, presentaciones=['amp-4'])],
        modo='informativa',
        pediatria=('sin_datos', 'Las fuentes consultadas no traen una pauta pediátrica.'),
        alertas=['Una sola serie respalda esta dosis (cirugía de catarata manual en una misión humanitaria). Verifica el protocolo de tu pabellón.',
                 'No confundir con el implante intravítreo de dexametasona (Ozurdex), que es otra ficha.'],
    )

    # ---------------------------------------------------------------- mitomicina C
    coc = lambda t: web('antifibroticos', '16235305', 'Cochrane Database of Systematic Reviews', t)  # noqa: E731
    ewt = lambda t: web('antifibroticos', 'eyewiki.org/Trabeculectomy', EW, t, anio=2026)  # noqa: E731
    gaz = lambda t: web('antifibroticos', 'PMC12989694', 'Clinical Ophthalmology', t)  # noqa: E731
    ahm = lambda t: web('antifibroticos', 'PMC13627763', 'Clinical Ophthalmology', t)  # noqa: E731
    tah = lambda t: web('antifibroticos', 'PMC9684179', 'Frontiers in Medicine', t)  # noqa: E731
    sin = lambda t: web('antifibroticos', 'PMC12013292', 'Indian Journal of Ophthalmology', t)  # noqa: E731
    s_a = ahm('Esponjas con mitomicina C de 0,1 a 0,5 mg/ml durante 1 a 5 minutos; inyección de 0,1 ml de una solución de 0,1 a 0,4 mg/ml')
    s_g = gaz('Mínimo 0,4 mg/ml durante 3 minutos en poblaciones de ascendencia africana; hasta 1,0 mg/ml en los casos más difíciles')
    s_t = tah('Pterigión: mitomicina C al 0,02 % durante 1 a 3 minutos')
    f['mitomicina'] = ficha(
        'mitomicina', 'Mitomicina C (antifibrótico)', 'antimetabolito', ['antifibrotico'],
        [pres('vial-20', 'polvo', 20, 'mg', isp('F-19531/22 Mitomicina liofilizado para solución inyectable 20 mg'), isp_codigos=['F-19531/22'],
              nota='Vial de uso intravenoso e intravesical; el uso ocular es off-label. Hay también el de 5 mg (F-19530/22). Medicamento peligroso. No se halló receta de reconstitución en fuentes aceptables.')],
        [dosis('Trabeculectomía (prevención de la cicatrización)', 'topica_intraoperatoria',
               'Esponjas empapadas con 0,1 a 0,5 mg/ml bajo la conjuntiva durante 1 a 5 minutos (EyeWiki: de 30 segundos a 5 minutos). '
               'En poblaciones de ascendencia africana, al menos 0,4 mg/ml durante 3 minutos y hasta 1,0 mg/ml en los casos difíciles.',
               final_rango(0.1, 0.5, 'mg', 1), s_a, estatus='off_label', condicion=NO_SISTEMICA + ' ' + CIRUJANO, presentaciones=['vial-20'],
               tambien=[ewt('Tiempo de esponja con mitomicina C o 5-FU: de 30 segundos a 5 minutos'), s_g]),
         dosis('Pterigión', 'topica_intraoperatoria',
               'Mitomicina C al 0,02 % (0,2 mg/ml), aplicación única durante la cirugía de 1 a 3 minutos, seguida de lavado con suero fisiológico.',
               final(0.2, 'mg', 1), s_t, estatus='off_label', condicion=NO_SISTEMICA + ' ' + CIRUJANO, presentaciones=['vial-20']),
         dosis('Inyección subconjuntival antes o después de la trabeculectomía o del implante XEN', 'subconjuntival',
               '0,1 ml de una solución de 0,1 a 0,4 mg/ml (10 a 40 µg); un experto describe 0,1 ml a 0,2 mg/ml (0,02 %). Para el needling de ampollas, 20 µg o 40 a 60 µg según la serie.',
               final_rango(0.01, 0.04, 'mg', 0.1), s_a, estatus='off_label', condicion=NO_SISTEMICA + ' ' + CIRUJANO, presentaciones=['vial-20'],
               tambien=[sin('Needling: 60 µg (0,15 ml de 0,4 mg/ml con lidocaína) o 20 µg (0,1 ml de 0,2 mg/ml con lidocaína)')])],
        protocolos=[],
        pediatria=('sin_datos', 'Las fuentes consultadas no traen una pauta pediátrica.'),
        conservacion=[conserv('La mitomicina C no es estable a temperatura ambiente una vez preparada (EyeWiki): prepararla justo antes de usar.', ewt('Mitomicina C: no estable a temperatura ambiente'))],
        alertas=[CIRUJANO,
                 'ALTO RIESGO: una concentración o un tiempo de aplicación mal calculados dañan el tejido ocular. No hay una guía de sociedad que fije la concentración oficial (nota de la búsqueda).',
                 'En trabeculectomía reduce el riesgo relativo de fracaso (RR 0,32 en ojos de alto riesgo; 0,29 en primera cirugía) sin aumento significativo de complicaciones permanentes que amenacen la visión (Cochrane).'],
        discrepancias=[disc('Concentración de mitomicina C en esponja para trabeculectomía',
                            [(s_a['ref'], '0,1 a 0,5 mg/ml durante 1 a 5 minutos'), (s_g['ref'], 'mínimo 0,4 mg/ml durante 3 minutos; hasta 1,0 mg/ml en casos difíciles'),
                             (ewt('Tiempo de esponja: de 30 segundos a 5 minutos')['ref'], '30 segundos a 5 minutos')],
                            '0,1 a 0,5 mg/ml',
                            'Cada autor fija su propia concentración y tiempo según el riesgo del paciente; se muestra el rango de la fuente principal (0,1 a 0,5 mg/ml), que incluye todo lo que otros usan salvo los casos difíciles, y la dosis la define el cirujano.')],
    )
    coc('La mitomicina C reduce el riesgo relativo de fracaso de la trabeculectomía')

    # ---------------------------------------------------------------- 5-fluorouracilo
    gre = lambda t: web('antifibroticos', '24554410', 'Cochrane Database of Systematic Reviews', t)  # noqa: E731
    s_s = sin('5-FU recién preparado: 0,5 ml de 10 mg/ml o 0,1 ml de 50 mg/ml; dosis total 5 mg')
    s_a2 = ahm('5-FU postoperatorio: 0,1 ml de 50 mg/ml cada 2 días según necesidad')
    f['fluorouracilo'] = ficha(
        'fluorouracilo', '5-fluorouracilo subconjuntival (antifibrótico)', 'antimetabolito', ['antifibrotico'],
        [pres('fu-500', 'solucion', 500, 'mg', isp('F-27364/23 Fluorouracilo solución inyectable 500 mg/10 mL'), volumen=10, isp_codigos=['F-27364/23'],
              nota='Vial de uso intravenoso (50 mg/ml); el uso subconjuntival es off-label. Medicamento peligroso.')],
        [dosis('Antifibrótico tras cirugía de glaucoma (inyección subconjuntival)', 'subconjuntival',
               '5 mg en total: 0,1 ml del vial de 50 mg/ml, o 0,5 ml de una solución de 10 mg/ml recién preparada. Un experto describe 0,1 ml de 50 mg/ml cada 2 días según necesidad.',
               final(5, 'mg', 0.1), s_s, estatus='off_label', condicion=NO_SISTEMICA + ' ' + CIRUJANO, presentaciones=['fu-500'], tambien=[s_a2]),
         dosis('Antifibrótico tras cirugía de glaucoma (solución de 10 mg/ml)', 'subconjuntival',
               '0,5 ml de una solución de 10 mg/ml recién preparada (5 mg en total). La fuente no describe cómo se diluye el vial.',
               final(5, 'mg', 0.5), s_s, estatus='off_label', condicion=NO_SISTEMICA + ' ' + CIRUJANO, presentaciones=['fu-500'])],
        protocolos=[
            protocolo('vial-sin-diluir', 0, 'Vial de 50 mg/ml sin diluir', 'fu-500',
                      [texto('Usar el vial tal como viene, sin diluir.'), cargar(0.1)],
                      (5, 'mg', 0.1), s_s)],
        pediatria=('sin_datos', 'Las fuentes consultadas no traen una pauta pediátrica.'),
        conservacion=[conserv('Preparar recién antes de usar (Singh 2025).', s_s)],
        alertas=[CIRUJANO,
                 'ALTO RIESGO: con 5-FU hay una alta incidencia de toxicidad corneal (EyeWiki).',
                 'Una dosis total baja se define como menos de 19 mg; las demás complicaciones son más frecuentes tras las inyecciones de 5-FU, sin aumento de las que amenazan la visión (Cochrane 2014).',
                 'Hoy se usa de forma ad hoc y casi no como esquema rutinario posoperatorio (Cochrane 2014).'],
        discrepancias=[disc('Concentración de la inyección de 5-FU',
                            [(s_s['ref'], '0,5 ml de 10 mg/ml o 0,1 ml de 50 mg/ml (5 mg)'), (s_a2['ref'], '0,1 ml de 50 mg/ml cada 2 días según necesidad')],
                            '5 mg por inyección', 'Las dos concentraciones dan la misma dosis total de 5 mg; la frecuencia la decide el cirujano.')],
    )
    gre('Dosis baja de 5-FU: menos de 19 mg en total; hoy casi no se usa como esquema rutinario')

    # ---------------------------------------------------------------- toxina botulínica
    bt = lambda t: web('toxina-botulinica', 'setid=33d066a9', 'U.S. National Library of Medicine — DailyMed (FDA)', t, anio=2026)  # noqa: E731
    s_dil = bt('Tabla 1: vial de 100 U con 1, 2, 4, 8 o 10 ml de diluyente da 10, 5, 2,5, 1,25 o 1 U por 0,1 ml')
    s_ble = bt('Blefaroespasmo: dosis inicial de 1,25 a 2,5 U (0,05 a 0,1 ml) por sitio')
    s_est = bt('Estrabismo: 0,05 a 0,15 ml por músculo; 1,25–2,5 U en músculos verticales y desviaciones horizontales de menos de 20 dioptrías prismáticas')
    s_est2 = bt('Estrabismo: 2,5 a 5 U en desviaciones horizontales de 20 a 50 dioptrías prismáticas')
    pasos_comunes = [texto('Inyectar el diluyente lentamente en el vial. Descartar el vial si el vacío no lo aspira.'),
                     texto('Mezclar con suavidad rotando el vial y anotar la fecha y hora de la reconstitución en la etiqueta.')]
    pasos_carga = texto('Cargar en una jeringa estéril una cantidad ligeramente mayor que la dosis, expulsar las burbujas de aire y colocar la aguja.')
    f['toxina-botulinica'] = ficha(
        'toxina-botulinica', 'Toxina botulínica A (Botox) en estrabismo y blefaroespasmo', 'toxina', ['antifibrotico'],
        [pres('botox-100', 'polvo', 100, 'U', isp('B-1397/26 Botox polvo para solución inyectable 100 U (onabotulinumtoxinA)'), isp_codigos=['B-1397/26'],
              nota='Botox de 100 U. También están registrados el de 50 U (B-2175/26) y el de 200 U (B-2176/26). Solo se documentó onabotulinumtoxinA: las unidades de otras toxinas no son equivalentes.')],
        [dosis('Blefaroespasmo esencial benigno y trastornos del nervio VII', 'intramuscular',
               'Dosis inicial de 1,25 a 2,5 U (0,05 a 0,1 ml) por sitio, en el orbicular preseptal medial y lateral del párpado superior y lateral del inferior. '
               'Aguja de 27 a 30 G. En sesiones siguientes puede aumentar hasta el doble; más de 5 U por sitio aporta poco beneficio. Máximo 200 U acumuladas en 30 días.',
               None, s_ble, estatus='autorizada',
               condicion='Autorizada en la etiqueta FDA de Botox para mayores de 12 años. ' + CIRUJANO, presentaciones=['botox-100'], tambien=[s_dil]),
         dosis('Estrabismo vertical o horizontal de menos de 20 dioptrías prismáticas, y parálisis persistente del nervio VI', 'intramuscular',
               '1,25 a 2,5 U en cualquier músculo, con 0,05 a 0,15 ml por músculo. No inyectar sin exposición quirúrgica ni guía electromiográfica. '
               'Las dosis siguientes pueden subir hasta el doble.',
               None, s_est, estatus='autorizada',
               condicion='Autorizada en la etiqueta FDA de Botox para mayores de 12 años. ' + CIRUJANO, presentaciones=['botox-100']),
         dosis('Estrabismo horizontal de 20 a 50 dioptrías prismáticas', 'intramuscular',
               '2,5 a 5 U en cualquier músculo, con 0,05 a 0,15 ml por músculo. Tenga a mano instrumentos para descomprimir la órbita.',
               None, s_est2, estatus='autorizada',
               condicion='Autorizada en la etiqueta FDA de Botox para mayores de 12 años. ' + CIRUJANO, presentaciones=['botox-100']),
         *[dosis('Diluciones de la etiqueta (tabla 1): lo que queda en el vial de 100 U según el diluyente agregado', 'intramuscular',
                 f'Vial de 100 U con {ml} ml de cloruro de sodio 0,9 % inyectable sin conservantes: {u} U por 0,1 ml. '
                 'Es la concentración de la etiqueta, no la dosis: las U por sitio y el volumen por músculo están en las indicaciones de arriba.',
                 final(float(u.replace(',', '.')), 'U', 0.1), s_dil, estatus='autorizada',
                 condicion=CIRUJANO, presentaciones=['botox-100'])
           for ml, u in ((8, '1,25'), (4, '2,5'), (2, '5'))]],
        protocolos=[
            protocolo('botox-100-8ml', 3, 'Vial de 100 U con 8 ml (1,25 U por 0,1 ml)', 'botox-100',
                      [reconstituir('cloruro de sodio 0,9 % inyectable SIN conservantes (solo ese diluyente)', 8), *pasos_comunes, pasos_carga],
                      (1.25, 'U', 0.1), s_dil),
            protocolo('botox-100-4ml', 4, 'Vial de 100 U con 4 ml (2,5 U por 0,1 ml)', 'botox-100',
                      [reconstituir('cloruro de sodio 0,9 % inyectable SIN conservantes (solo ese diluyente)', 4), *pasos_comunes, pasos_carga],
                      (2.5, 'U', 0.1), s_dil),
            protocolo('botox-100-2ml', 5, 'Vial de 100 U con 2 ml (5 U por 0,1 ml)', 'botox-100',
                      [reconstituir('cloruro de sodio 0,9 % inyectable SIN conservantes (solo ese diluyente)', 2), *pasos_comunes, pasos_carga],
                      (5, 'U', 0.1), s_dil)],
        pediatria=('no_establecida', 'La indicación de la etiqueta FDA para estrabismo y blefaroespasmo es para pacientes de 12 años o más; no hay pauta en menores.'),
        conservacion=[conserv('Usar dentro de las 24 horas posteriores a la reconstitución; mientras tanto, guardar el sobrante en refrigerador (2–8 °C). El vial es de una sola dosis: descartar lo que no se use.',
                              bt('Conservación: administrar dentro de 24 horas tras reconstituir, 2–8 °C, vial de una sola dosis'), horas=24)],
        alertas=[CIRUJANO,
                 'El verificador compara solo con las diluciones de la etiqueta (1,25; 2,5 y 5 U por 0,1 ml). La dosis en U por sitio y el volumen por músculo no se verifican: los define el cirujano.',
                 'ALTO RIESGO: las unidades de Botox NO son intercambiables con las de otras toxinas botulínicas (Dysport, Xeomin y otras); no conviertas unidades entre marcas.',
                 'Reconstituir SOLO con cloruro de sodio al 0,9 % inyectable sin conservantes (etiqueta FDA).',
                 'En el tratamiento del estrabismo se han producido hemorragias retrobulbares capaces de comprometer la circulación de la retina; hay que tener a mano instrumentos para descomprimir la órbita (etiqueta FDA).',
                 'En el blefaroespasmo puede haber ptosis (evitar el elevador del párpado), diplopía (evitar inyecciones mediales en el párpado inferior) y exposición corneal por disminución del parpadeo (etiqueta FDA).'],
    )
    return f
