import json
from pathlib import Path


RUTA_DB = Path(__file__).resolve().parent.parent / "data" / "incidencias.json"


def inicializar_base_datos() -> None:
    """Crea el archivo JSON si todavía no existe."""
    RUTA_DB.parent.mkdir(parents=True, exist_ok=True)

    if not RUTA_DB.exists():
        datos_iniciales = {
            "incidencias": {},
            "siguiente_id": 1
        }

        guardar_base_datos(datos_iniciales)


def cargar_base_datos() -> dict:
    """Carga y retorna los datos almacenados en el archivo JSON."""
    inicializar_base_datos()

    try:
        with RUTA_DB.open("r", encoding="utf-8") as archivo:
            return json.load(archivo)

    except (json.JSONDecodeError, OSError) as error:
        raise RuntimeError(
            f"No se pudo leer la base de datos JSON: {error}"
        ) from error


def guardar_base_datos(datos: dict) -> None:
    """Guarda los datos en el archivo JSON."""
    RUTA_DB.parent.mkdir(parents=True, exist_ok=True)

    try:
        with RUTA_DB.open("w", encoding="utf-8") as archivo:
            json.dump(
                datos,
                archivo,
                ensure_ascii=False,
                indent=4
            )

    except OSError as error:
        raise RuntimeError(
            f"No se pudo guardar la base de datos JSON: {error}"
        ) from error


def obtener_siguiente_id() -> int:
    """Obtiene el siguiente ID disponible y actualiza el contador."""
    datos = cargar_base_datos()

    siguiente_id = datos["siguiente_id"]
    datos["siguiente_id"] += 1

    guardar_base_datos(datos)

    return siguiente_id


def reiniciar_base_datos() -> None:
    """
    Reinicia la base de datos.

    Esta función se utiliza principalmente durante las pruebas.
    """
    datos_iniciales = {
        "incidencias": {},
        "siguiente_id": 1
    }

    guardar_base_datos(datos_iniciales)