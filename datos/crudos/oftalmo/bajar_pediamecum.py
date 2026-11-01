"""Pediamécum para los orales oftalmológicos (mismo método que tópicos: una ficha inexistente devuelve ~131 KB genéricos)."""
import subprocess, re, html, os
O = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pediamecum')
B = 'https://www.aeped.es/comites/cm/pediamecum/principios-activos'
def curl(u): return subprocess.run(['curl', '-sL', '--max-time', '60', u], capture_output=True, text=True).stdout
def texto(h):
    h = re.sub(r'(?is)<(script|style|nav|header|footer).*?</\1>', '', h); h = re.sub(r'(?i)<br\s*/?>|</p>|</li>|</h\d>|</tr>', '\n', h)
    return re.sub(r'\n\s*\n+', '\n', re.sub(r'[ \t\xa0]+', ' ', html.unescape(re.sub(r'<[^>]+>', '', h))))
for s in ['acetazolamida', 'valaciclovir', 'famciclovir', 'aciclovir', 'doxiciclina', 'minociclina', 'azitromicina', 'prednisona',
          'acido-tranexamico', 'ivermectina', 'pirimetamina', 'cotrimoxazol', 'sulfametoxazol-trimetoprim', 'trimetoprim-sulfametoxazol',
          'manitol', 'glicerol', 'alteplasa', 'vancomicina', 'ceftazidima', 'cefuroxima', 'bevacizumab', 'triamcinolona', 'bupivacaina', 'lidocaina', 'hialuronidasa']:
    out = os.path.join(O, s + '.txt')
    if os.path.exists(out) or os.path.exists(out + '.sin'): continue
    h = curl(f'{B}/{s}')
    if len(h) < 1000 or 'pediamecum/principios-activos/' + s not in h or abs(len(h) - 131000) < 3000:
        open(out + '.sin', 'w').write(str(len(h))); print('SIN', s, len(h), flush=True); continue
    t = texto(h); i = t.find('Uso clínico'); t = t[i if i > 0 else 0:]
    open(out, 'w').write(f'{B}/{s}\n' + t[:30000]); print('OK', s, len(t), flush=True)
