from .base_datos import db, obtener_siguiente_id

class IncidenciaNoEncontradaError(Exception):
    """Excepción personalizada para incidencia no encontrada."""
    pass

def crear_incidencia(titulo: str, descripcion: str, prioridad: str, asignado_a: str) -> dict:
    """Crea una nueva incidencia y la almacena."""
    if prioridad not in ("baja", "media", "alta", "crítica"):
        raise ValueError("Prioridad no válida. Use: baja, media, alta, crítica.")

    id_incidencia = obtener_siguiente_id()
    incidencia = {
        "id": id_incidencia,
        "titulo": titulo.strip(),
        "descripcion": descripcion.strip(),
        "prioridad": prioridad,
        "estado": "abierta",
        "asignado_a": asignado_a.strip()
    }
    db["incidencias"][id_incidencia] = incidencia
    return incidencia

def obtener_incidencia(id_incidencia: int) -> dict:
    """Obtiene una incidencia por ID. Lanza IncidenciaNoEncontradaError si no existe."""
    incidencia = db["incidencias"].get(id_incidencia)
    if incidencia is None:
        raise IncidenciaNoEncontradaError(f"Incidencia con ID {id_incidencia} no encontrada.")
    return incidencia

def actualizar_incidencia(id_incidencia: int, **kwargs) -> dict:
    """Actualiza campos de una incidencia existente."""
    incidencia = obtener_incidencia(id_incidencia)
    campos_permitidos = {"titulo", "descripcion", "prioridad", "estado", "asignado_a"}
    for clave, valor in kwargs.items():
        if clave not in campos_permitidos:
            raise ValueError(f"Campo no permitido: {clave}")
        if clave == "prioridad" and valor not in ("baja", "media", "alta", "crítica"):
            raise ValueError("Prioridad no válida.")
        incidencia[clave] = valor.strip() if isinstance(valor, str) else valor
    db["incidencias"][id_incidencia] = incidencia
    return incidencia

def eliminar_incidencia(id_incidencia: int) -> bool:
    """Elimina una incidencia. Retorna True si existía, False si no."""
    if id_incidencia in db["incidencias"]:
        del db["incidencias"][id_incidencia]
        return True
    return False

def listar_incidencias(estado_filtro: str = None) -> list:
    """Lista todas las incidencias, opcionalmente filtradas por estado."""
    if estado_filtro:
        return [inc for inc in db["incidencias"].values() if inc["estado"] == estado_filtro]
    return list(db["incidencias"].values())