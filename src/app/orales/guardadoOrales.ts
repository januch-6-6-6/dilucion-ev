import { alternarFavorito, leerFavoritos } from '../favoritos'
import { leerRecientes, registrarReciente } from '../recientes'

// Los orales se guardan como `oral:<id>` en las mismas claves que los EV; la UI de EV
// descarta esos ids porque obtenerFicha('oral:x') es undefined.
const PREFIJO = 'oral:'
const conPrefijo = (id: string) => PREFIJO + id
const sinPrefijo = (lista: string[]): string[] =>
  lista.filter((x) => x.startsWith(PREFIJO)).map((x) => x.slice(PREFIJO.length))

export const leerFavoritosOrales = (): string[] => sinPrefijo(leerFavoritos())
export const esFavoritoOral = (id: string): boolean => leerFavoritos().includes(conPrefijo(id))
export const alternarFavoritoOral = (id: string): void => alternarFavorito(conPrefijo(id))
export const leerRecientesOrales = (): string[] => sinPrefijo(leerRecientes())
export const registrarRecienteOral = (id: string): void => registrarReciente(conPrefijo(id))
