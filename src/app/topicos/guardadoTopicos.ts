import { alternarFavorito, leerFavoritos } from '../favoritos'
import { leerRecientes, registrarReciente } from '../recientes'

// Los tópicos se guardan como `top:<id>` en las mismas claves que EV y orales; las otras
// secciones descartan esos ids porque no encuentran la ficha.
const PREFIJO = 'top:'
const conPrefijo = (id: string) => PREFIJO + id
const sinPrefijo = (lista: string[]): string[] => lista.filter((x) => x.startsWith(PREFIJO)).map((x) => x.slice(PREFIJO.length))

export const leerFavoritosTopicos = (): string[] => sinPrefijo(leerFavoritos())
export const esFavoritoTopico = (id: string): boolean => leerFavoritos().includes(conPrefijo(id))
export const alternarFavoritoTopico = (id: string): void => alternarFavorito(conPrefijo(id))
export const leerRecientesTopicos = (): string[] => sinPrefijo(leerRecientes())
export const registrarRecienteTopico = (id: string): void => registrarReciente(conPrefijo(id))
