"""Tabla de compatibilidad en Y de Stabilis («AVEC solvants usuels») leída por color de celda.

Uso: python3 scripts/stabilis_matriz.py ID [ID ...] --salida X.json [--pdf existente.pdf]
Pide el PDF por POST, lo convierte a PNG (pdftoppm) y detecta la grilla buscando las líneas oscuras.
Salida: {fila: {columna: 'G'|'R'|'Y'|'.'|'-'}} con los nombres en inglés que imprime Stabilis.
"""
import argparse
import json
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

URL = 'https://www.stabilis.org/TableIncompatibilitesSolvants-pdf.php'
SOLVENTES = ['Chlorure de sodium 0,9%', 'Glucose 5%', 'Nutrition parentérale (mélange binaire', 'Nutrition parentérale (mélange ternair', 'Ringer lactate']


def pedir_pdf(ids, destino):
    datos = 'hopital=Formacion&service=Dilucion+EV&choix_molecule=%d&' % ids[0] + '&'.join(f'idmolecule[]={i}' for i in ids)
    subprocess.run(['curl', '-sL', '-m', '180', '-A', 'Mozilla/5.0', URL, '--data', datos, '-o', str(destino)], check=True)


def nombres(pdf):
    """Nombres de columnas (5 solventes + moléculas) en el orden del PDF."""
    texto = subprocess.run(['pdftotext', '-layout', str(pdf), '-'], capture_output=True, text=True, check=True).stdout
    lineas = [l.strip() for l in texto.splitlines() if l.strip()]
    i = lineas.index(SOLVENTES[0])
    cols = []
    for l in lineas[i:]:
        if len(cols) > 5 and l == cols[5]:  # empieza la lista de filas
            break
        cols.append(l)
    return cols


def lineas_oscuras(valores, umbral=60):
    """Centros de las rachas de píxeles oscuros."""
    res, ini = [], None
    for k, v in enumerate(valores + [255]):
        if v < umbral and ini is None:
            ini = k
        elif v >= umbral and ini is not None:
            res.append((ini + k - 1) / 2)
            ini = None
    return res


def clasificar(c):
    r, g, b = c[:3]
    if r > 200 and g < 80 and b < 80:
        return 'R'
    if g > 150 and r < 80:
        return 'G'
    if r > 220 and g > 180 and b < 80:
        return 'Y'
    if abs(r - g) < 12 and abs(g - b) < 12 and r < 170:
        return '-'
    return '.'


def leer(pdf, n_filas):
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(['pdftoppm', '-r', '300', '-png', '-singlefile', str(pdf), f'{d}/t'], check=True)
        im = Image.open(f'{d}/t.png').convert('RGB')
    w, h = im.size
    gris = im.convert('L')
    # Fila de referencia: en la mitad inferior de la página (zona de celdas), barrer horizontalmente.
    y_ref = int(h * 0.62)
    xs = lineas_oscuras([gris.getpixel((x, y_ref)) for x in range(w)])
    x_ref = int((xs[-2] + xs[-1]) / 2)  # dentro de la última columna
    ys = lineas_oscuras([gris.getpixel((x_ref, y)) for y in range(h)])
    # Las filas de celdas son la racha más larga de líneas equiespaciadas (descarta texto del pie y encabezado).
    ys = racha_regular(ys)
    assert len(ys) == n_filas + 1, f'{len(ys) - 1} filas detectadas, se esperaban {n_filas}'
    return im, xs, ys


def racha_regular(pos, tolerancia=0.35):
    mejor, actual = [], pos[:1]
    for a, b in zip(pos, pos[1:]):
        paso = b - a
        if len(actual) >= 2 and abs(paso - (actual[1] - actual[0])) > tolerancia * (actual[1] - actual[0]):
            mejor = max(mejor, actual, key=len)
            actual = [a, b]
        else:
            actual.append(b)
    return max(mejor, actual, key=len)


def matriz(pdf):
    cols = nombres(pdf)
    filas = cols[5:]
    im, xs, ys = leer(pdf, len(filas))
    xs = racha_regular(xs)
    assert len(xs) == len(cols) + 1, f'{len(xs) - 1} columnas detectadas, se esperaban {len(cols)}'
    res = {}
    for i, f in enumerate(filas):
        cy = int((ys[i] + ys[i + 1]) / 2)
        res[f] = {c: clasificar(im.getpixel((int((xs[j] + xs[j + 1]) / 2), cy))) for j, c in enumerate(cols)}
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('ids', nargs='+', type=int)
    ap.add_argument('--salida', required=True)
    ap.add_argument('--pdf')
    a = ap.parse_args()
    pdf = Path(a.pdf) if a.pdf else Path(tempfile.mkdtemp()) / 'stabilis.pdf'
    if not a.pdf:
        pedir_pdf(a.ids, pdf)
    m = matriz(pdf)
    diag = sum(1 for f in m if m[f].get(f) == '-')
    print(f'{len(m)} filas; diagonal gris en {diag}')
    Path(a.salida).write_text(json.dumps(m, ensure_ascii=False, indent=0))


if __name__ == '__main__':
    main()
