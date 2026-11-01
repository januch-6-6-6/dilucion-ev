"""Registro sanitario ISP (formulario ASP.NET, 2 postbacks). tipo 0 = nombre de producto, 1 = principio activo. Solo registros vigentes."""
import re, html, urllib.request, urllib.parse, http.cookiejar, ssl
U='https://registrosanitario.ispch.gob.cl/'
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
P='ctl00$ContentPlaceHolder1$'
def _abrir():
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()),urllib.request.HTTPSHandler(context=ctx))
def _campos(h):
    return {m.group(1):html.unescape(m.group(2)) for m in re.finditer(r'<input type="hidden" name="([^"]+)" id="[^"]*" value="([^"]*)"',h)}
def _post(op,d):
    return op.open(urllib.request.Request(U,urllib.parse.urlencode(d).encode(),{'User-Agent':'Mozilla/5.0'}),timeout=90).read().decode('utf8','replace')
def _filas(h):
    out=[]
    for r in re.findall(r'<tr>(.*?)</tr>',h,re.S):
        c=re.findall(r'<span id="[^"]*lbl(Producto|Nombre|FechaRegistro|Titular|PA|Estado)">(.*?)</span>',r,re.S)
        if c: out.append({k:html.unescape(v).strip() for k,v in c})
    return out
def buscar(texto,tipo=1,maxpag=60):
    op=_abrir(); h=op.open(urllib.request.Request(U,headers={'User-Agent':'Mozilla/5.0'}),timeout=60).read().decode('utf8','replace')
    chk=f'{P}chkTipoBusqueda${tipo}'
    d=_campos(h); d.update({'__EVENTTARGET':chk,'__EVENTARGUMENT':'',chk:'on'})
    h=_post(op,d)
    campo=re.search(r'name="(ctl00\$ContentPlaceHolder1\$txt[^"]+)"',h).group(1)
    est=re.search(r'<select name="ctl00\$ContentPlaceHolder1\$ddlEstado".*?<option[^>]*value="([^"]*)"',h,re.S).group(1)
    base={chk:'on',campo:texto,f'{P}ddlEstado':est}
    d=_campos(h); d.update(base); d[f'{P}btnBuscar']='Buscar'
    h=_post(op,d); todas=_filas(h); pag=1
    while pag<maxpag:
        nxt=[int(x) for x in re.findall(r"Page\$(\d+)",h) if int(x)>pag]
        if not nxt: break
        pag=min(nxt)
        d=_campos(h); d.update(base); d.update({'__EVENTTARGET':f'{P}gvDatosBusqueda','__EVENTARGUMENT':f'Page${pag}'})
        h=_post(op,d); f=_filas(h)
        if not f: break
        todas+=f
    return todas
