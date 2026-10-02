"""Crea a Héctor como persona y administrador en el proyecto REAL (sin enviar correo; entrará con enlace mágico en la Etapa 2)."""
import json, os, urllib.request, urllib.error
from pathlib import Path
for l in (Path.home()/'dilucion-ev'/'.env.supabase').read_text().splitlines():
    if '=' in l: k, v = l.split('=', 1); os.environ.setdefault(k, v)
URL, KEY = os.environ['SUPABASE_REAL_URL'], os.environ['SUPABASE_REAL_SERVICE_KEY']
CORREO = 'hectorsalvo32@gmail.com'
def llamar(m, ruta, cuerpo=None, extra=None):
    h = {'apikey': KEY, 'Authorization': f'Bearer {KEY}', 'Content-Type': 'application/json', 'User-Agent': 'dilucion-ev-admin/1.0'}; h.update(extra or {})
    r = urllib.request.Request(URL + ruta, data=json.dumps(cuerpo).encode() if cuerpo is not None else None, headers=h, method=m)
    try:
        with urllib.request.urlopen(r, timeout=60) as x: b = x.read(); return x.status, (json.loads(b) if b else None)
    except urllib.error.HTTPError as e: return e.code, e.read().decode()[:300]
st, u = llamar('POST', '/auth/v1/admin/users', {'email': CORREO, 'email_confirm': True})
if st >= 300:
    st2, lista = llamar('GET', '/auth/v1/admin/users?per_page=50')
    u = next(x for x in lista['users'] if x['email'] == CORREO); print('el usuario ya existía')
uid = u['id']
print('persona:', llamar('POST', '/rest/v1/personas?on_conflict=id', {'id': uid, 'correo': CORREO, 'nombre': 'Héctor Salvo Agüero', 'profesion': 'TENS e Ingeniero en Informática (administrador)', 'estado': 'activa'}, {'Prefer': 'resolution=merge-duplicates,return=minimal'})[0])
print('administrador:', llamar('POST', '/rest/v1/administradores?on_conflict=persona', {'persona': uid}, {'Prefer': 'resolution=merge-duplicates,return=minimal'})[0])
