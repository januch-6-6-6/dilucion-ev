import { existsSync, readdirSync, readFileSync } from 'node:fs'
import { join } from 'node:path'
import { parse } from 'yaml'
import { validarDatos } from '../src/esquema/validar'
import { validarOrales } from '../src/esquema/validar-orales'

const raiz = join(import.meta.dirname, '..', 'datos')
const dirMed = join(raiz, 'medicamentos')
const archivoFuentes = join(raiz, 'fuentes.yaml')

const archivos = existsSync(dirMed) ? readdirSync(dirMed).filter((a) => a.endsWith('.yaml')).sort() : []
const fichas = archivos.map((a) => {
  const ficha = parse(readFileSync(join(dirMed, a), 'utf8'))
  const esperado = a.replace(/\.yaml$/, '')
  if (ficha?.id !== esperado) console.error(`${a}: el id "${ficha?.id}" no coincide con el nombre del archivo`)
  return ficha
})
const fuentes = existsSync(archivoFuentes) ? (parse(readFileSync(archivoFuentes, 'utf8')) ?? []) : []

const errores = validarDatos(fichas, fuentes)
const idMalos = fichas.filter((f, i) => f?.id !== archivos[i].replace(/\.yaml$/, '')).length
if (errores.length || idMalos) {
  for (const e of errores) console.error(`✗ ${e}`)
  console.error(`\n${errores.length + idMalos} errores en ${fichas.length} fichas.`)
  process.exit(1)
}
console.log(`${fichas.length} fichas validadas, ${fuentes.length} fuentes.`)

// Orales (datos/orales/*.yaml + datos/fuentes-orales.yaml); ambos opcionales.
const dirOrales = join(raiz, 'orales')
const archivoFuentesOrales = join(raiz, 'fuentes-orales.yaml')
const archivosOrales = existsSync(dirOrales) ? readdirSync(dirOrales).filter((a) => a.endsWith('.yaml')).sort() : []
const orales = archivosOrales.map((a) => parse(readFileSync(join(dirOrales, a), 'utf8')))
const fuentesOrales = existsSync(archivoFuentesOrales) ? (parse(readFileSync(archivoFuentesOrales, 'utf8')) ?? []) : []
const erroresOrales = validarOrales(orales, fuentesOrales)
orales.forEach((f, i) => {
  const esperado = archivosOrales[i].replace(/\.yaml$/, '')
  if (f?.id !== esperado) erroresOrales.push(`${archivosOrales[i]}: el id "${f?.id}" no coincide con el nombre del archivo`)
})
if (erroresOrales.length) {
  for (const e of erroresOrales) console.error(`✗ ${e}`)
  console.error(`\n${erroresOrales.length} errores en ${orales.length} fichas orales.`)
  process.exit(1)
}
console.log(`${orales.length} fichas orales validadas, ${fuentesOrales.length} fuentes orales.`)
