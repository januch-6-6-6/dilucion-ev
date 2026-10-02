import { randomBytes } from 'node:crypto'
import { resolve } from 'node:path'
import { createClient, type SupabaseClient } from '@supabase/supabase-js'
import { config } from 'dotenv'

// En local las claves salen de .env.supabase; en CI vienen como variables de entorno (secretos).
config({ path: resolve(__dirname, '../../.env.supabase'), quiet: true })

const requerida = (nombre: string): string => {
  const valor = process.env[nombre]
  if (!valor) throw new Error(`Falta la variable ${nombre} (ver .env.supabase.ejemplo)`)
  return valor
}

const opciones = { auth: { persistSession: false, autoRefreshToken: false } }

/** Aleatorio por archivo de prueba: evita choques entre corridas, porque nada se borra (la bitácora es inmutable). */
export const sufijo = randomBytes(3).toString('hex')

export const clienteServicio = (): SupabaseClient =>
  createClient(requerida('SUPABASE_PRUEBA_URL'), requerida('SUPABASE_PRUEBA_SERVICE_KEY'), opciones)

export const clientePublico = (): SupabaseClient =>
  createClient(requerida('SUPABASE_PRUEBA_URL'), requerida('SUPABASE_PRUEBA_ANON_KEY'), opciones)

export interface RolPrueba {
  nombre: string
  establecimiento?: string
  pais?: string
  admin?: boolean
  suspendida?: boolean
}

/** Crea el usuario, su fila en `personas` (con la clave de servicio) y devuelve un cliente con su sesión iniciada. */
export async function crearUsuario(rol: RolPrueba): Promise<{ id: string; cliente: SupabaseClient }> {
  const servicio = clienteServicio()
  const correo = `prueba+${sufijo}-${rol.nombre}@dilucion-ev.test`
  const clave = randomBytes(18).toString('base64url')
  const { data, error } = await servicio.auth.admin.createUser({ email: correo, password: clave, email_confirm: true })
  if (error || !data.user) throw new Error(`No se pudo crear a ${rol.nombre}: ${error?.message}`)
  const id = data.user.id

  const persona = await servicio.from('personas').insert({
    id,
    correo,
    nombre: rol.nombre,
    profesion: 'Persona de prueba',
    establecimiento: rol.establecimiento ?? null,
    pais_extranjero: rol.pais ?? null,
    estado: rol.suspendida ? 'suspendida' : 'activa',
  })
  if (persona.error) throw new Error(`No se pudo registrar a ${rol.nombre}: ${persona.error.message}`)
  if (rol.admin) {
    const adm = await servicio.from('administradores').insert({ persona: id })
    if (adm.error) throw new Error(`No se pudo hacer administrador a ${rol.nombre}: ${adm.error.message}`)
  }

  const cliente = clientePublico()
  const sesion = await cliente.auth.signInWithPassword({ email: correo, password: clave })
  if (sesion.error) throw new Error(`No se pudo iniciar sesión como ${rol.nombre}: ${sesion.error.message}`)
  return { id, cliente }
}

/** Inserta un establecimiento de prueba y devuelve su código. */
export async function crearHospital(nombre: string): Promise<string> {
  const codigo = `PRUEBA-${sufijo}-${nombre}`
  const { error } = await clienteServicio()
    .from('establecimientos')
    .insert({ codigo, nombre: `Hospital de prueba ${nombre}`, tipo: 'Hospital', comuna: 'Prueba', region: 'Prueba' })
  if (error) throw new Error(`No se pudo crear el hospital ${nombre}: ${error.message}`)
  return codigo
}

/** Asegura y devuelve el id del medicamento de prueba. */
export async function medicamentoDePrueba(): Promise<string> {
  const { error } = await clienteServicio().from('medicamentos').upsert({ id: 'prueba-medicamento' })
  if (error) throw new Error(`No se pudo asegurar el medicamento de prueba: ${error.message}`)
  return 'prueba-medicamento'
}
