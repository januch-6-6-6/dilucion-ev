#!/usr/bin/env node
/**
 * Genera las capturas de funcionamiento (estilo ficha de Google Play) y la imagen Open Graph.
 *
 * 1. Levanta `vite preview` sobre dist/ (hay que haber corrido `npm run build` antes).
 * 2. Con Playwright (Chromium) saca capturas REALES de la app en un celular de 360 px.
 * 3. Monta cada captura en un marco de teléfono con un titular corto y la guarda como
 *    public/capturas/<id>.webp (540×1080, ≤ 120 KB).
 * 4. Rehace public/og.png (1200×627) con la portada nueva.
 *
 * Uso:
 *   npm run build
 *   PLAYWRIGHT=/ruta/a/playwright/index.mjs node scripts/capturas/generar-capturas.mjs
 * (Si playwright está instalado en el proyecto basta con `node scripts/capturas/generar-capturas.mjs`.)
 * Necesita ImageMagick (`magick`) para convertir a WebP.
 *
 * Los titulares deben coincidir con src/app/capturas.ts (una prueba revisa que existan las imágenes).
 */
import { execFileSync, spawn } from 'node:child_process'
import { mkdirSync, readFileSync, statSync } from 'node:fs'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'

const RAIZ = resolve(dirname(fileURLToPath(import.meta.url)), '../..')
const SALIDA = join(RAIZ, 'public/capturas')
const TMP = join(RAIZ, 'node_modules/.cache/capturas')
const PUERTO = Number(process.env.PUERTO ?? 4179)
const BASE = `http://localhost:${PUERTO}/`
const MAX_BYTES = 120 * 1024

const { chromium } = await import(process.env.PLAYWRIGHT ? pathToFileURL(process.env.PLAYWRIGHT).href : 'playwright')

// Titulares: mismos textos que src/app/capturas.ts
const titulares = Object.fromEntries(
  [...readFileSync(join(RAIZ, 'src/app/capturas.ts'), 'utf8').matchAll(/id: '([^']+)',\s*titular: '([^']+)'/g)].map((m) => [m[1], m[2]]),
)

/** Fondo de cada lámina: variaciones del degradado de la cabecera. */
const FONDOS = {
  busqueda: 'linear-gradient(160deg, #0f766e 0%, #0e7490 55%, #2563eb 100%)',
  ficha: 'linear-gradient(160deg, #0e7490 0%, #2563eb 100%)',
  calculadora: 'linear-gradient(160deg, #1e40af 0%, #2563eb 50%, #0e7490 100%)',
  compatibilidad: 'linear-gradient(160deg, #5b21b6 0%, #4f46e5 50%, #2563eb 100%)',
  oscuro: 'linear-gradient(160deg, #0b1220 0%, #155e75 60%, #1d4ed8 100%)',
}

/** Cómo llegar a cada pantalla. */
const ESCENAS = [
  {
    id: 'busqueda',
    ruta: '#/',
    async preparar(p) {
      await p.getByRole('searchbox').fill('cef')
      await p.getByRole('searchbox').evaluate((e) => {
        e.blur()
        window.scrollTo(0, e.getBoundingClientRect().top + window.scrollY - 16)
      })
    },
  },
  { id: 'ficha', ruta: '#/m/noradrenalina' },
  {
    id: 'calculadora',
    ruta: '#/m/noradrenalina/calcular',
    async preparar(p) {
      await p.getByLabel('Peso (kg)').fill('70')
      await p.getByLabel('Dosis', { exact: true }).fill('0.1')
      await p.locator('input').last().evaluate((e) => e.blur())
      // que se vea el resultado (ml/h) abajo de la pantalla
      await p.locator('.resultado').evaluate((e) => window.scrollTo(0, e.getBoundingClientRect().bottom + window.scrollY - window.innerHeight + 140))
    },
  },
  {
    id: 'compatibilidad',
    ruta: '#/m/noradrenalina',
    async preparar(p) {
      await p.getByRole('tab', { name: 'Compatibilidad' }).click()
      await p.evaluate(() => window.scrollTo(0, 250))
    },
  },
  { id: 'oscuro', ruta: '#/m/fentanilo', tema: 'oscuro' },
]

function servidor() {
  const vite = join(RAIZ, 'node_modules/.bin/vite')
  const proc = spawn(vite, ['preview', '--port', String(PUERTO), '--strictPort'], { cwd: RAIZ, stdio: 'pipe' })
  return new Promise((ok, mal) => {
    proc.stdout.on('data', (d) => d.toString().includes(String(PUERTO)) && ok(proc))
    proc.on('exit', (c) => mal(new Error(`vite preview terminó con código ${c}`)))
  })
}

async function contexto(navegador, { tema, ancho = 360, alto = 760 } = {}) {
  const ctx = await navegador.newContext({ viewport: { width: ancho, height: alto }, deviceScaleFactor: 2, locale: 'es-CL', colorScheme: 'light' })
  // Sin contador de visitas, sin aviso inicial (ya aceptado) y con el tema pedido
  await ctx.route(/gc\.zgo\.at|goatcounter/, (r) => r.abort())
  await ctx.addInitScript((t) => {
    localStorage.setItem('dilucion-ev:aviso-aceptado', '1')
    if (t) localStorage.setItem('dilucion-ev:tema', t)
  }, tema ?? null)
  return ctx
}

const aDataUrl = (buf) => `data:image/png;base64,${buf.toString('base64')}`

/** Lámina 540×1080: titular arriba, teléfono con la captura abajo (cortado por el borde, como en Play). */
function lamina(titular, fondo, captura) {
  return `<!doctype html><meta charset="utf-8"><style>
  *{box-sizing:border-box;margin:0}
  body{width:540px;height:1080px;overflow:hidden;background:${fondo};font-family:Ubuntu,'Segoe UI',Roboto,system-ui,sans-serif;color:#fff}
  h1{position:absolute;top:58px;left:40px;right:40px;font-size:42px;line-height:1.12;font-weight:800;letter-spacing:-.02em;text-align:center;text-wrap:balance}
  .tel{position:absolute;top:230px;left:60px;width:420px;height:900px;border-radius:56px;background:#0b1220;padding:40px 14px 14px;
       box-shadow:0 30px 60px rgb(2 6 23/.45),inset 0 0 0 2px #334155}
  .tel img{display:block;width:392px;height:827px;object-fit:cover;object-position:top;border-radius:10px 10px 0 0}
  .isla{position:absolute;top:16px;left:50%;transform:translateX(-50%);width:72px;height:10px;border-radius:5px;background:#334155}
  </style><h1>${titular}</h1><div class="tel"><img src="${captura}"><div class="isla"></div></div>`
}

function aWebp(png, destino) {
  for (const calidad of [90, 85, 80, 74, 68, 60]) {
    execFileSync('magick', [png, '-strip', '-quality', String(calidad), '-define', 'webp:method=6', destino])
    const bytes = statSync(destino).size
    if (bytes <= MAX_BYTES) return { bytes, calidad }
  }
  throw new Error(`${destino} supera ${MAX_BYTES} bytes`)
}

mkdirSync(SALIDA, { recursive: true })
mkdirSync(TMP, { recursive: true })
const vite = await servidor()
const navegador = await chromium.launch()
const crudas = {}
try {
  for (const e of ESCENAS) {
    const ctx = await contexto(navegador, { tema: e.tema })
    const p = await ctx.newPage()
    await p.goto(BASE + e.ruta)
    await p.waitForLoadState('networkidle')
    if (e.preparar) await e.preparar(p)
    await p.waitForTimeout(300)
    crudas[e.id] = await p.screenshot()
    await ctx.close()
  }

  // Láminas estilo Play Store
  const ctx = await navegador.newContext({ viewport: { width: 540, height: 1080 }, deviceScaleFactor: 1 })
  const p = await ctx.newPage()
  for (const e of ESCENAS) {
    const titular = titulares[e.id]
    if (!titular) throw new Error(`Falta el titular de ${e.id} en src/app/capturas.ts`)
    await p.setContent(lamina(titular, FONDOS[e.id], aDataUrl(crudas[e.id])))
    await p.waitForLoadState('load')
    const png = join(TMP, `${e.id}.png`)
    await p.screenshot({ path: png })
    const r = aWebp(png, join(SALIDA, `${e.id}.webp`))
    console.log(`capturas/${e.id}.webp  ${(r.bytes / 1024).toFixed(1)} KB (calidad ${r.calidad})`)
  }
  await ctx.close()

  // Portada nueva en celular (para la imagen OG)
  const ctxPortada = await contexto(navegador)
  const pp = await ctxPortada.newPage()
  await pp.goto(BASE + '#/')
  await pp.waitForLoadState('networkidle')
  await pp.getByRole('searchbox').evaluate((el) => el.blur())
  const portada = await pp.screenshot()
  await ctxPortada.close()

  // Open Graph 1200×627
  const og = await navegador.newContext({ viewport: { width: 1200, height: 627 }, deviceScaleFactor: 1 })
  const po = await og.newPage()
  await po.setContent(`<!doctype html><meta charset="utf-8"><style>
    *{box-sizing:border-box;margin:0}
    body{width:1200px;height:627px;overflow:hidden;background:linear-gradient(135deg,#0f766e 0%,#0e7490 45%,#2563eb 100%);
         font-family:Ubuntu,'Segoe UI',Roboto,system-ui,sans-serif;color:#fff;position:relative}
    .txt{position:absolute;left:64px;top:70px;width:600px}
    .chip{display:inline-block;font-size:21px;font-weight:700;padding:6px 16px;border-radius:999px;background:rgb(15 23 42/.22);border:1px solid rgb(255 255 255/.3)}
    h1{font-size:84px;font-weight:800;letter-spacing:-.03em;margin:18px 0 8px}
    p.lema{font-size:30px;line-height:1.25;font-weight:700;text-wrap:balance}
    ul{list-style:none;padding:0;margin:26px 0 0;font-size:24px;line-height:1.6}
    li::before{content:'✓  '}
    .autor{position:absolute;left:64px;bottom:44px;font-size:20px;opacity:.9}
    .tel{position:absolute;width:300px;height:640px;border-radius:44px;background:#0b1220;padding:11px;box-shadow:0 24px 50px rgb(2 6 23/.45),inset 0 0 0 2px #334155}
    .tel img{display:block;width:278px;height:587px;object-fit:cover;object-position:top;border-radius:34px}
    .t1{left:860px;top:40px}
    .t2{left:690px;top:110px;transform:rotate(-4deg)}
  </style>
  <div class="txt"><span class="chip">Material de formación · gratis y sin internet</span>
  <h1>Dilución EV</h1>
  <p class="lema">Prepara y administra medicamentos endovenosos con la fuente a la vista.</p>
  <ul><li>89 medicamentos EV usados en Chile</li><li>Dilución, ml/h, gotas/min y dosis por peso</li><li>Compatibilidad en Y con su fuente</li></ul></div>
  <p class="autor">Héctor Salvo Agüero · TENS e Ingeniero en Informática</p>
  <div class="tel t2"><img src="${aDataUrl(crudas.ficha)}"></div>
  <div class="tel t1"><img src="${aDataUrl(portada)}"></div>`)
  await po.waitForLoadState('load')
  const ogPng = join(TMP, 'og.png')
  await po.screenshot({ path: ogPng })
  execFileSync('magick', [ogPng, '-strip', '-colors', '256', '-define', 'png:compression-level=9', join(RAIZ, 'public/og.png')])
  console.log(`og.png  ${(statSync(join(RAIZ, 'public/og.png')).size / 1024).toFixed(1)} KB`)
  await og.close()
} finally {
  await navegador.close()
  vite.kill()
}
