from .base_datos import (
    cargar_base_datos,
    guardar_base_datos,
    obtener_siguiente_id,
)


class IncidenciaNoEncontradaError(Exception):
    """Excepción personalizada para incidencia no encontrada."""
    pass


def crear_incidencia(
    titulo: str,
    descripcion: str,
    prioridad: str,
    asignado_a: str
) -> dict:
    """Crea y almacena una nueva incidencia."""

    if prioridad not in ("baja", "media", "alta", "crítica"):
        raise ValueError(
            "Prioridad no válida. Use: baja, media, alta, crítica."
        )

    id_incidencia = obtener_siguiente_id()

    incidencia = {
        "id": id_incidencia,
        "titulo": titulo.strip(),
        "descripcion": descripcion.strip(),
        "prioridad": prioridad,
        "estado": "abierta",
        "asignado_a": asignado_a.strip()
    }

    datos = cargar_base_datos()

    # En JSON las claves siempre se almacenan como texto.
    datos["incidencias"][str(id_incidencia)] = incidencia

    guardar_base_datos(datos)

    return incidencia


def obtener_incidencia(id_incidencia: int) -> dict:
    """Obtiene una incidencia mediante su ID."""

    datos = cargar_base_datos()

    incidencia = datos["incidencias"].get(str(id_incidencia))

    if incidencia is None:
        raise IncidenciaNoEncontradaError(
            f"Incidencia con ID {id_incidencia} no encontrada."
        )

    return incidencia


def actualizar_incidencia(id_incidencia: int, **kwargs) -> dict:
    """Actualiza los datos permitidos de una incidencia."""

    datos = cargar_base_datos()

    incidencia = datos["incidencias"].get(str(id_incidencia))

    if incidencia is None:
        raise IncidenciaNoEncontradaError(
            f"Incidencia con ID {id_incidencia} no encontrada."
        )

    campos_permitidos = {
        "titulo",
        "descripcion",
        "prioridad",
        "estado",
        "asignado_a"
    }

    for clave, valor in kwargs.items():

        if clave not in campos_permitidos:
            raise ValueError(
                f"Campo no permitido: {clave}"
            )

        if (
            clave == "prioridad"
            and valor not in ("baja", "media", "alta", "crítica")
        ):
            raise ValueError(
                "Prioridad no válida."
            )

        incidencia[clave] = (
            valor.strip()
            if isinstance(valor, str)
            else valor
        )

    datos["incidencias"][str(id_incidencia)] = incidencia

    guardar_base_datos(datos)

    return incidencia


def eliminar_incidencia(id_incidencia: int) -> bool:
    """Elimina una incidencia mediante su ID."""

    datos = cargar_base_datos()

    clave = str(id_incidencia)

    if clave in datos["incidencias"]:

        del datos["incidencias"][clave]

        guardar_base_datos(datos)

        return True

    return False


def listar_incidencias(
    estado_filtro: str = None
) -> list:
    """Lista todas las incidencias o las filtra por estado."""

    datos = cargar_base_datos()

    incidencias = list(
        datos["incidencias"].values()
    )

    if estado_filtro:
        return [
            incidencia
            for incidencia in incidencias
            if incidencia["estado"] == estado_filtro
        ]

    return incidencias