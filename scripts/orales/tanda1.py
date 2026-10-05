"""Orales, tanda 1: analgésicos y antiinflamatorios (por ahora, solo paracetamol)."""
from .comun import (dosis, discrepancia, ficha_oral, fu, fuente_cima, fuente_pediamecum_oral, pres)

INF = 'CIMA-PARACETAMOL-83208'  # Antidol infantil 100 mg/ml solución oral
G1 = 'CIMA-PARACETAMOL-85780'  # Antidol 1 g comprimidos
PED = 'PEDIAMECUM-PARACETAMOL'


def fuentes():
    return [
        fuente_cima('paracetamol', '83208', 'Antidol infantil 100 mg/ml solución oral', varios=True),
        fuente_cima('paracetamol', '85780', 'Antidol 1 g comprimidos', varios=True),
        fuente_pediamecum_oral('paracetamol', 'Paracetamol (acetaminofén)', slug='paracetamol-acetaminofen'),
    ]


def paracetamol():
    presentaciones = [
        pres('jarabe-100-mg-ml', 'jarabe', mg_ml=100, fuente=fu(INF, 'Antidol infantil 100 mg/ml solución oral')),
        # La ficha de Antidol 1 g no menciona ranura ni partición; pide otra presentación para dosis <1 g.
        pres('comprimido-1-g', 'comprimido', mg=1000, partible='no', fuente=fu(G1, 'Antidol 1 g comprimidos (4.2 y 4.4)')),
    ]
    dosis_ = [
        dosis('Dolor leve-moderado y fiebre (15 mg/kg cada 6 h)', 'pediatrico', 'por_peso', 'mg/kg', base='toma', max=15,
              tomas=4, intervalo_h=6, fuente=fu(INF, '4.2: 15 mg/kg cada 6 horas; máx. 60 mg/kg/día')),
        dosis('Dolor leve-moderado y fiebre (alternativa 10 mg/kg cada 4 h)', 'pediatrico', 'por_peso', 'mg/kg', base='toma',
              max=10, tomas=6, intervalo_h=4, condicion='Si a las 3-4 h no hay efecto; intervalo mínimo de 4 h entre tomas',
              fuente=fu(PED, 'Dosis y pautas: 10 mg/kg cada 4 horas; ~60 mg/kg/día')),
        dosis('Dolor moderado y fiebre (adultos y adolescentes >16 años o >50 kg)', 'adulto', 'fija', 'mg', min=1000, max=1000,
              intervalo_h=6, tope_dia=(2600, 'mg'), texto='1 comprimido (1 g) cada 6-8 horas según necesidad',
              fuente=fu(G1, '4.2: 1 g cada 6-8 h; la ficha topa en 3 g/24 h, se muestra el tope más bajo de Pediamécum (2,6 g)')),
    ]
    disc = [
        discrepancia('Tope diario del adulto (>43 kg)',
                     [(G1, '3 g/24 h (CIMA, Antidol 1 g)'), (PED, '2,6 g/24 h (Pediamécum, >43 kg)')],
                     '2,6 g/24 h',
                     'Se muestra el valor más bajo de las dos fuentes hasta que se decida el tope.'),
    ]
    alertas = [
        'Máximo 60 mg/kg/día en niños (4 tomas de 15 mg/kg); no exceder aunque se sumen otros medicamentos con paracetamol.',
        'Pediamécum equipara 0,6 ml de solución a 15 gotas (frasco con cuentagotas); con jeringa dosificar en ml.',
        'Antidol infantil está indicado en niños de 3 a 32 kg; en menores de 2 años la dosis la establece el médico.',
        'Antidol 1 g: dosis <1 g por toma requieren otra presentación; no usar con otros medicamentos con paracetamol (máx. 3 g/día en total según CIMA).',
        'Hepatotoxicidad descrita con dosis diarias <4 g en adultos; en alcohólicos crónicos no más de 2 g/día (CIMA).',
    ]
    return ficha_oral(
        'paracetamol', 'Paracetamol (acetaminofén)', 'analgesico-no-opioide', presentaciones, dosis_,
        {
            'comida': 'indiferente',
            'texto': 'Vía oral. Comprimidos con un vaso de líquido, preferentemente agua. Solución con la jeringa oral del envase. '
                     'Pediamécum: las comidas ricas en carbohidratos pueden disminuir su absorción.',
            'fuente': fu(G1, '4.2 Forma de administración'),
        },
        comerciales=['Antidol infantil', 'Antidol 1 g'], discrepancias=disc,
        renal='Insuficiencia renal grave (aclaramiento de creatinina <10 ml/min): intervalo entre tomas de al menos 8 h.',
        hepatico='Reducir la dosis e incrementar el intervalo entre tomas.',
        fuente_ajuste=fu(INF, '4.2 Insuficiencia renal / Insuficiencia hepática'),
        alertas=alertas,
    )


def fichas():
    return {'paracetamol': paracetamol()}
