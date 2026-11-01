import { alternarFavorito, leerFavoritos } from '../favoritos'
import { leerRecientes, registrarReciente } from '../recientes'

// Las fichas de pabellón se guardan como `oft:<id>` en las mismas claves que EV, orales y tópicos;
// las otras secciones descartan esos ids porque no encuentran la ficha.
const PREFIJO = 'oft:'
const conPrefijo = (id: string) => PREFIJO + id
const sinPrefijo = (lista: string[]): string[] => lista.filter((x) => x.startsWith(PREFIJO)).map((x) => x.slice(PREFIJO.length))

export const leerFavoritosOculares = (): string[] => sinPrefijo(leerFavoritos())
export const esFavoritoOcular = (id: string): boolean => leerFavoritos().includes(conPrefijo(id))
export const alternarFavoritoOcular = (id: string): void => alternarFavorito(conPrefijo(id))
export const leerRecientesOculares = (): string[] => sinPrefijo(leerRecientes())
export const registrarRecienteOcular = (id: string): void => registrarReciente(conPrefijo(id))
