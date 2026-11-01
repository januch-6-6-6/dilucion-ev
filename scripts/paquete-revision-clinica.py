#!/usr/bin/env python3
"""Genera el HTML del paquete de revisión clínica de Oftalmología para imprimir como PDF.

Uso: python3 scripts/paquete-revision-clinica.py salida.html
Luego: chrome --headless --no-sandbox --print-to-pdf=informes/oftalmologia-paquete-revision-clinica.pdf salida.html
Todo sale de datos/oftalmo/*.yaml: lo que ve la enfermera es lo que muestra la app.
"""
import glob
import html
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
UNIDAD = {'mcg': 'µg', 'mg': 'mg', 'U': 'U', 'g': 'g', 'ml': 'ml'}


def num(n):
    return str(round(n, 4)).rstrip('0').rstrip('.').replace('.', ',') if isinstance(n, float) else str(n)


def final_texto(fin):
    c = fin['cantidad']
    u = UNIDAD.get(c['unidad'], c['unidad'])
    cant = f"{num(c['min'])} a {num(c['max'])} {u}" if 'min' in c else f"{num(c['valor'])} {u}"
    return f"{cant} en {num(fin['volumenMl'])} ml"


def corto(t, n=170):
    return t if len(t) <= n else t[: n - 1].rsplit(' ', 1)[0] + '…'


def esc(t):
    return html.escape(t)


fichas = {}
for fn in sorted(glob.glob(str(RAIZ / 'datos' / 'oftalmo' / '*.yaml'))):
    d = yaml.safe_load(open(fn, encoding='utf-8'))
    fichas[d['id']] = d

CAJAS = '<span class="cajas">☐ OK &nbsp; ☐ Corregir &nbsp; ☐ Sacar</span>'


def tabla_dosis(id_):
    f = fichas[id_]
    filas = []
    for d in f['dosis']:
        fin = f"<br><b>Concentración de referencia: {esc(final_texto(d['final']))}</b>" if d.get('final') else ''
        est = 'Autorizada' if d['estatus'] == 'autorizada' else 'Off-label'
        filas.append(f"<tr><td>{esc(corto(d['indicacion'], 90))}</td><td>{esc(corto(d['texto'], 260))}{fin}</td><td>{est}</td></tr>")
    return '<table class="datos"><tr><th>Indicación</th><th>Lo que muestra la app</th><th>Estatus</th></tr>' + ''.join(filas) + '</table>'


def resumen_ficha(f):
    ds = f['dosis']
    if not ds:
        return 'Sin cifras (ficha informativa, sin pauta en las fuentes).'
    d = ds[0]
    base = corto(d['texto'], 150)
    if d.get('final'):
        base += f" [{final_texto(d['final'])}]"
    extra = f" (+{len(ds) - 1} dosis más)" if len(ds) > 1 else ''
    return base + extra


def anexo():
    filas = []
    for id_, f in sorted(fichas.items(), key=lambda kv: kv[1]['nombre'].lower()):
        reg = 'No registrado en Chile' if f['registroChile'] == 'no_registrado' else 'ISP'
        filas.append(f"<tr><td><b>{esc(f['nombre'])}</b></td><td>{esc(resumen_ficha(f))}</td><td>{reg}</td><td class='marca'>☐ OK<br>☐ Corregir<br>☐ Sacar</td><td class='nota'></td></tr>")
    return ('<table class="anexo"><tr><th>Medicamento</th><th>Dosis que muestra la app (primera de la ficha)</th><th>Registro</th><th>Revisión</th><th>Comentario</th></tr>'
            + ''.join(filas) + '</table>')


def pregunta(texto):
    return f"<li>{texto}<div class='resp'>{CAJAS}<div class='linea'></div></div></li>"


CSS = """
@page { size: A4; margin: 16mm 14mm; }
body { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 10.5pt; color: #1b1f24; line-height: 1.35; }
h1 { font-size: 20pt; margin: 0 0 4px; color: #0b4a6f; }
h2 { font-size: 14pt; margin: 22px 0 6px; color: #0b4a6f; border-bottom: 2px solid #0b4a6f; padding-bottom: 3px; page-break-after: avoid; }
h3 { font-size: 11.5pt; margin: 14px 0 4px; page-break-after: avoid; }
.sub { color: #555; margin: 0 0 10px; }
.aviso { background: #fff4d6; border-left: 5px solid #d99a00; padding: 7px 10px; margin: 8px 0; }
table { border-collapse: collapse; width: 100%; margin: 6px 0 10px; }
th, td { border: 1px solid #9aa5b1; padding: 4px 6px; vertical-align: top; text-align: left; }
th { background: #e8eef3; }
table.datos td:first-child { width: 22%; }
table.datos td:last-child { width: 12%; }
.datos { page-break-inside: auto; }
table.anexo { font-size: 8.8pt; }
table.anexo td:nth-child(1) { width: 17%; } table.anexo td:nth-child(3) { width: 11%; }
table.anexo td:nth-child(4) { width: 11%; white-space: nowrap; } table.anexo td:nth-child(5) { width: 15%; }
tr { page-break-inside: avoid; }
.marca { font-size: 9pt; }
.cajas { font-weight: 700; }
ol.preg li { margin: 8px 0; page-break-inside: avoid; }
.resp { margin-top: 4px; } .linea { border-bottom: 1px solid #777; height: 24px; }
.punto { border: 1px solid #c3ccd5; border-radius: 6px; padding: 6px 10px; margin: 10px 0; }
.duda { background: #eef6fb; padding: 5px 9px; border-radius: 4px; margin: 5px 0; }
.pie { color: #666; font-size: 9pt; margin-top: 18px; }
ul { margin: 4px 0 4px 18px; padding: 0; }
.salto { page-break-before: always; }
"""


def punto(titulo, intro, id_, dudas):
    d = ''.join(f'<div class="duda">❓ {x}</div>' for x in dudas)
    tabla = tabla_dosis(id_) if id_ else ''
    return f"<div class='punto'><h3>{titulo}</h3><p>{intro}</p>{tabla}{d}<div class='resp'>{CAJAS}<div class='linea'></div></div></div>"


def main(salida):
    nreg = sum(1 for f in fichas.values() if f['registroChile'] == 'no_registrado')
    noreg = ', '.join(sorted(f['nombre'].split(' (')[0].split(' intr')[0].split(' en ')[0] for f in fichas.values() if f['registroChile'] == 'no_registrado'))
    partes = [f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>"]
    partes.append("<h1>Revisión clínica — Oftalmología (Dilución EV)</h1>")
    partes.append("<p class='sub'>Para la enfermera/o de pabellón oftalmológico · Material de formación, no de prescripción</p>")
    partes.append("<div class='aviso'><b>Qué te pedimos:</b> leer cada punto y marcar <b>OK</b>, <b>Corregir</b> (y escribir qué) o <b>Sacar</b>. "
                  "No hace falta revisar todo: el punto 1 al 6 son lo más delicado; el anexo es la lista completa por si quieres mirarla. "
                  "Tu experiencia manda sobre lo que dice una fuente.</div>")
    partes.append("<h2>Qué es esta herramienta</h2><ul>"
                  f"<li>Una app de consulta con <b>{len(fichas)} fichas de pabellón</b> (intracamerales, intravítreas, bloqueos, perioculares, antifibróticos y toxina) y 11 medicamentos orales de uso oftálmico.</li>"
                  "<li>Cada ficha <b>muestra lo que dice una fuente publicada</b> (ficha técnica, protocolo de farmacia hospitalaria, consenso de sociedades) con su cita. <b>No propone preparaciones.</b></li>"
                  "<li>Un <b>verificador</b> compara lo que preparaste (volumen tras disolver, cuánto tomaste, a cuánto llevaste) con la concentración de la fuente. Si no coincide dice «NO coincide… No administres; revisa los pasos».</li>"
                  "<li>Toda ficha lleva «Alto riesgo» y «Verifica el protocolo de tu pabellón». Aún no está publicada.</li></ul>")
    partes.append("<h2>Lo más delicado, por prioridad</h2>")
    partes.append(punto('1. Toxina botulínica (Botox 100 U)',
                        'Ficha de una sola fuente (etiqueta FDA). El verificador compara solo con las <b>diluciones de la etiqueta</b>: vial de 100 U con 8, 4 o 2 ml = 1,25, 2,5 o 5 U por 0,1 ml. '
                        'Las dosis por sitio (U) y el volumen por músculo quedan como texto, sin verificar.',
                        'toxina-botulinica',
                        ['¿Son esas las diluciones que se usan en tu pabellón? ¿Falta alguna (por ejemplo 10 U por 0,1 ml, con 1 ml)?',
                         '¿Se usa otra marca o se reconstituye distinto?']))
    partes.append(punto('2. Moxifloxacino intracameral — no hay una dosis única aceptada',
                        'Se muestran dos protocolos (ASCRS 2023 y Arshinoff). El rango publicado va de 150 a 500 µg por inyección. '
                        'El verificador acepta cualquiera de los protocolos mostrados (incluida la solución al 0,1 % de la ASCRS).',
                        'moxifloxacino',
                        ['¿Cuál de los dos usa tu pabellón? ¿Se muestran bien ambos?',
                         'El envase modelado es Megrelan 0,5 % de 3 ml (15 mg): el ISP no informa el contenido real. ¿Es ese el envase?']))
    partes.append(punto('3. Mitomicina C — alto riesgo, «según el protocolo del cirujano»',
                        'No hay pasos de preparación (ninguna fuente aceptable los da). El verificador solo compara concentraciones.',
                        'mitomicina',
                        ['¿Las concentraciones y tiempos coinciden con lo que se usa? ¿Falta alguna indicación (por ejemplo dacriocistorrinostomía)?']))
    partes.append(punto('4. 5-fluorouracilo subconjuntival — alto riesgo',
                        'Misma lógica: solo muestra lo publicado; el cirujano define dosis y tiempo.',
                        'fluorouracilo',
                        ['¿La preparación de 10 mg/ml a partir del vial de 50 mg/ml es la que usan? La fuente no describe cómo se diluye.']))
    partes.append("<div class='punto'><h3>5. Dosis «off-label»</h3>"
                  "<p>36 dosis en 23 fichas están marcadas «Off-label» (la indicación no está en la ficha técnica). Las más delicadas:</p><ul>"
                  "<li><b>Adrenalina intracameral:</b> tres autores con concentraciones distintas (registrado como discrepancia).</li>"
                  "<li><b>Lidocaína intracameral</b> (4 dosis) y <b>alteplasa</b> (5 dosis).</li>"
                  "<li><b>Ganciclovir / foscarnet:</b> 2 mg en 0,1 ml (protocolo de farmacia hospitalaria) frente a 200/400 µg de una tabla de estabilidad del consenso.</li>"
                  "<li><b>Voriconazol y ceftazidima:</b> la fuente indica agregar 19 ml y 9,4 ml de agua para que queden 20 ml y 10 ml en total.</li></ul>"
                  f"<div class='duda'>❓ ¿Hay alguna cifra que te suene fuera de lo habitual?</div><div class='resp'>{CAJAS}<div class='linea'></div></div></div>")
    partes.append(f"<div class='punto'><h3>6. Productos sin registro en Chile ({nreg})</h3>"
                  "<p>Se muestran con el aviso «No registrado en Chile (puede usarse por importación o uso compasivo)».</p>"
                  f"<p><b>Son:</b> {esc(noreg)}.</p>"
                  f"<div class='duda'>❓ ¿Alguno se usa de verdad en tu pabellón? ¿Alguno sobra?</div><div class='resp'>{CAJAS}<div class='linea'></div></div></div>")
    partes.append("<h2>Preguntas generales</h2><ol class='preg'>"
                  + pregunta('¿Falta algún medicamento de pabellón que uses a menudo?')
                  + pregunta('Las fichas de <b>mepivacaína</b> y <b>verde de indocianina</b> no traen cifras (ninguna fuente aceptable). ¿Las dejamos como ficha informativa o las sacamos?')
                  + pregunta('¿El verificador te parece útil, o riesgoso por dar una sensación de seguridad? (Si lo ves riesgoso, se deja solo la ficha.)')
                  + pregunta('¿Los avisos y alertas se entienden bien para una pabellonera o un TENS?')
                  + "</ol>")
    partes.append("<div class='salto'></div><h2>Anexo: las 41 fichas</h2>"
                  "<p>La columna «Dosis» es la primera dosis de la ficha tal como la muestra la app (puede haber más). Marca solo lo que quieras comentar.</p>")
    partes.append(anexo())
    partes.append("<p class='pie'>Devuelve este documento marcado (foto o PDF) a Héctor. Las fuentes de cada cifra están en la app y en el informe técnico (informes/oftalmologia-revision.md). "
                  "Mientras no firmes, las fichas dicen «Revisión clínica: pendiente».</p></body></html>")
    Path(salida).write_text('\n'.join(partes), encoding='utf-8')


if __name__ == '__main__':
    main(sys.argv[1])
