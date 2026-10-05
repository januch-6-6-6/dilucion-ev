"""Orales, tanda 1: analgésicos y antiinflamatorios (por ahora, solo paracetamol)."""
from .comun import (dosis, discrepancia, ficha_oral, fu, fuente_cima, fuente_pediamecum_oral, pres)

INF = 'CIMA-PARACETAMOL-83208'  # Antidol infantil 100 mg/ml solución oral
G1 = 'CIMA-PARACETAMOL-85780'  # Antidol 1 g comprimidos
PED = 'PEDIAMECUM-PARACETAMOL'


def fuentes():
    return [
        fuente_cima('paracetamol', '83208', 'Antidol infantil 100 mg/ml solución oral', varios=True),
        fuente_cima('paracetamol', '85780', 'Antidol 1 g comprimidos', varios=True),
        fuente_pediamecum_oral('paracetamol', 'Paracetamol (acetaminofén)', anio=2021, slug='paracetamol-acetaminofen'),
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
              fuente=fu(INF, '4.2: 10 mg/kg cada 4 horas; "intervalo mínimo de 4 horas" entre tomas; Pediamécum coincide')),
        dosis('Dolor leve-moderado y fiebre (>43 kg, régimen de Pediamécum)', 'pediatrico', 'fija', 'mg', min=650, max=650,
              tomas=4, intervalo_h=6, tope_dia=(2600, 'mg'), condicion='>43 kg (adolescentes >13 años)',
              texto='650 mg cada 4-6 horas; máximo 2600 mg/24 h',
              fuente=fu(PED, '>43 kg (adolescentes >13 años): 650 mg/4-6 h; máximo: 2600 mg/24 h')),
        dosis('Dolor moderado y fiebre (adultos y adolescentes >16 años o >50 kg)', 'adulto', 'fija', 'mg', min=1000, max=1000,
              tomas=3, intervalo_h=8, tope_dia=(3000, 'mg'), texto='1 comprimido (1 g) cada 6-8 horas según necesidad',
              fuente=fu(G1, '4.2: 1 comprimido (1g) cada 6-8 horas, según necesidad. No se excederá de 3 g/24 horas')),
    ]
    disc = [
        discrepancia('Tope diario según régimen',
                     [(G1, 'Antidol 1 g, adultos y adolescentes >16 años o >50 kg, 1 g cada 6-8 h: máximo 3 g/24 h (CIMA)'),
                      (PED, '>43 kg (adolescentes >13 años), 650 mg cada 4-6 h: máximo 2600 mg/24 h (Pediamécum)')],
                     'Cada régimen se muestra con su propio tope',
                     'Los dos topes pertenecen a regímenes distintos (dosis por toma y población diferentes); no son un conflicto numérico.'),
    ]
    alertas = [
        'Máximo 60 mg/kg/día en niños (4 tomas de 15 mg/kg); no exceder aunque se sumen otros medicamentos con paracetamol (CIMA 83208).',
        'Antidol infantil está indicado en niños de 3 a 32 kg; en menores de 2 años la dosis la establece el médico.',
        'Antidol 1 g: dosis <1 g por toma requieren otra presentación; no usar con otros medicamentos con paracetamol (máx. 3 g/día en total según CIMA).',
        'Hepatotoxicidad descrita con dosis diarias <4 g en adultos; en alcohólicos crónicos no más de 2 g/día (CIMA).',
    ]
    return ficha_oral(
        'paracetamol', 'Paracetamol (acetaminofén)', 'analgesico-no-opioide', presentaciones, dosis_,
        {
            'comida': 'indiferente',
            'texto': 'Vía oral. Comprimidos con un vaso de líquido, preferentemente agua. '
                     'Solución con la jeringa oral del envase (ficha de Antidol infantil). '
                     'Pediamécum: las comidas ricas en carbohidratos pueden disminuir su absorción.',
            'fuente': fu(G1, '4.2 Forma de administración: comprimidos con un vaso de líquido, preferentemente agua'),
        },
        comerciales=['Antidol infantil', 'Antidol 1 g'], discrepancias=disc,
        renal='Antidol 1 g (CIMA): filtración glomerular 10-50 ml/min, 500 mg cada 6 h; <10 ml/min, 500 mg cada 8 h; '
              'la ficha añade «Debido a la dosis, este medicamento no está indicado para este grupo de pacientes» (comprimido de 1 g). '
              'Antidol infantil (CIMA): insuficiencia renal grave (aclaramiento de creatinina <10 ml/min), intervalo entre tomas de al menos 8 h.',
        hepatico='Antidol 1 g (CIMA): no se excederá de 2 g/24 horas y el intervalo mínimo entre dosis será de 8 horas. '
                 'Antidol infantil (CIMA): reducir la dosis e incrementar el intervalo entre tomas. '
                 'Ancianos (Antidol 1 g): reducir la dosis del adulto en un 25 %.',
        fuente_ajuste=fu(G1, '4.2 Pacientes con insuficiencia renal / hepática / uso en ancianos (la pauta pediátrica: ficha 83208)'),
        alertas=alertas,
    )


def fichas():
    return {'paracetamol': paracetamol()}
