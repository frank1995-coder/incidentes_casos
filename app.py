"""Aplicación de consola para la gestión de incidencias."""

from src.incidente import (
    IncidenciaNoEncontradaError,
    actualizar_incidencia,
    crear_incidencia,
    eliminar_incidencia,
    listar_incidencias,
    obtener_incidencia,
)


PRIORIDADES_VALIDAS = ("baja", "media", "alta", "crítica")
ESTADOS_VALIDOS = ("abierta", "en proceso", "cerrada")


def mostrar_encabezado(titulo: str) -> None:
    """Muestra un encabezado para cada opción del menú."""
    print("\n" + "=" * 60)
    print(titulo.upper())
    print("=" * 60)


def solicitar_texto(mensaje: str) -> str:
    """Solicita un texto obligatorio."""
    while True:
        valor = input(mensaje).strip()

        if valor:
            return valor

        print("El valor no puede estar vacío.")


def solicitar_id() -> int:
    """Solicita y valida el identificador numérico de una incidencia."""
    while True:
        valor = input("Ingrese el ID de la incidencia: ").strip()

        try:
            id_incidencia = int(valor)

            if id_incidencia <= 0:
                print("El ID debe ser un número mayor que cero.")
                continue

            return id_incidencia

        except ValueError:
            print("Ingrese un identificador numérico válido.")


def seleccionar_opcion(
    titulo: str,
    opciones: tuple[str, ...],
    permitir_vacio: bool = False,
) -> str | None:
    """Permite seleccionar una opción de una lista numerada."""
    print(f"\n{titulo}:")

    for indice, opcion in enumerate(opciones, start=1):
        print(f"{indice}. {opcion.capitalize()}")

    while True:
        mensaje = "Seleccione una opción"

        if permitir_vacio:
            mensaje += " o presione Enter para conservar el valor actual"

        seleccion = input(f"{mensaje}: ").strip()

        if permitir_vacio and seleccion == "":
            return None

        try:
            indice = int(seleccion)

            if 1 <= indice <= len(opciones):
                return opciones[indice - 1]

            print("Seleccione una opción disponible.")

        except ValueError:
            print("Ingrese el número correspondiente a una opción.")


def imprimir_incidencia(incidencia: dict) -> None:
    """Muestra los datos de una incidencia."""
    print("-" * 60)
    print(f"ID          : {incidencia['id']}")
    print(f"Título      : {incidencia['titulo']}")
    print(f"Descripción : {incidencia['descripcion']}")
    print(f"Prioridad   : {incidencia['prioridad'].capitalize()}")
    print(f"Estado      : {incidencia['estado'].capitalize()}")
    print(f"Asignado a  : {incidencia['asignado_a']}")


def registrar_incidencia() -> None:
    """Registra una nueva incidencia."""
    mostrar_encabezado("Registrar incidencia")

    titulo = solicitar_texto("Título: ")
    descripcion = solicitar_texto("Descripción: ")
    prioridad = seleccionar_opcion(
        "Prioridad",
        PRIORIDADES_VALIDAS,
    )
    asignado_a = solicitar_texto("Responsable o área asignada: ")

    try:
        incidencia = crear_incidencia(
            titulo=titulo,
            descripcion=descripcion,
            prioridad=prioridad,
            asignado_a=asignado_a,
        )

        print("\nIncidencia registrada correctamente.")
        imprimir_incidencia(incidencia)

    except ValueError as error:
        print(f"\nNo se pudo registrar la incidencia: {error}")


def consultar_incidencia() -> None:
    """Consulta una incidencia mediante su identificador."""
    mostrar_encabezado("Consultar incidencia")

    id_incidencia = solicitar_id()

    try:
        incidencia = obtener_incidencia(id_incidencia)
        imprimir_incidencia(incidencia)

    except IncidenciaNoEncontradaError as error:
        print(f"\n{error}")


def listar_todas_las_incidencias() -> None:
    """Muestra todas las incidencias registradas."""
    mostrar_encabezado("Listado de incidencias")

    incidencias = listar_incidencias()

    if not incidencias:
        print("No existen incidencias registradas.")
        return

    print(f"Total de incidencias: {len(incidencias)}")

    for incidencia in incidencias:
        imprimir_incidencia(incidencia)


def listar_incidencias_por_estado() -> None:
    """Muestra las incidencias filtradas por estado."""
    mostrar_encabezado("Filtrar incidencias por estado")

    estado = seleccionar_opcion(
        "Estado",
        ESTADOS_VALIDOS,
    )

    incidencias = listar_incidencias(estado_filtro=estado)

    if not incidencias:
        print(f"\nNo existen incidencias con estado '{estado}'.")
        return

    print(
        f"\nTotal de incidencias con estado "
        f"'{estado}': {len(incidencias)}"
    )

    for incidencia in incidencias:
        imprimir_incidencia(incidencia)


def modificar_incidencia() -> None:
    """Actualiza los datos de una incidencia existente."""
    mostrar_encabezado("Actualizar incidencia")

    id_incidencia = solicitar_id()

    try:
        incidencia_actual = obtener_incidencia(id_incidencia)

    except IncidenciaNoEncontradaError as error:
        print(f"\n{error}")
        return

    print("\nDatos actuales:")
    imprimir_incidencia(incidencia_actual)

    print(
        "\nIngrese los nuevos valores. "
        "Presione Enter para conservar el valor actual."
    )

    titulo = input(
        f"Título [{incidencia_actual['titulo']}]: "
    ).strip()

    descripcion = input(
        f"Descripción [{incidencia_actual['descripcion']}]: "
    ).strip()

    prioridad = seleccionar_opcion(
        f"Prioridad actual: {incidencia_actual['prioridad']}",
        PRIORIDADES_VALIDAS,
        permitir_vacio=True,
    )

    estado = seleccionar_opcion(
        f"Estado actual: {incidencia_actual['estado']}",
        ESTADOS_VALIDOS,
        permitir_vacio=True,
    )

    asignado_a = input(
        f"Asignado a [{incidencia_actual['asignado_a']}]: "
    ).strip()

    cambios = {}

    if titulo:
        cambios["titulo"] = titulo

    if descripcion:
        cambios["descripcion"] = descripcion

    if prioridad:
        cambios["prioridad"] = prioridad

    if estado:
        cambios["estado"] = estado

    if asignado_a:
        cambios["asignado_a"] = asignado_a

    if not cambios:
        print("\nNo se realizaron cambios.")
        return

    try:
        incidencia_actualizada = actualizar_incidencia(
            id_incidencia,
            **cambios,
        )

        print("\nIncidencia actualizada correctamente.")
        imprimir_incidencia(incidencia_actualizada)

    except (ValueError, IncidenciaNoEncontradaError) as error:
        print(f"\nNo se pudo actualizar la incidencia: {error}")


def borrar_incidencia() -> None:
    """Elimina una incidencia después de solicitar confirmación."""
    mostrar_encabezado("Eliminar incidencia")

    id_incidencia = solicitar_id()

    try:
        incidencia = obtener_incidencia(id_incidencia)

    except IncidenciaNoEncontradaError as error:
        print(f"\n{error}")
        return

    imprimir_incidencia(incidencia)

    confirmacion = input(
        "\n¿Está seguro de eliminar esta incidencia? (s/n): "
    ).strip().lower()

    if confirmacion not in ("s", "si", "sí"):
        print("Eliminación cancelada.")
        return

    if eliminar_incidencia(id_incidencia):
        print("\nIncidencia eliminada correctamente.")
    else:
        print("\nNo fue posible eliminar la incidencia.")


def mostrar_menu() -> None:
    """Muestra el menú principal."""
    print("\n" + "=" * 60)
    print("SISTEMA DE GESTIÓN DE INCIDENCIAS")
    print("=" * 60)
    print("1. Registrar incidencia")
    print("2. Consultar incidencia por ID")
    print("3. Listar todas las incidencias")
    print("4. Filtrar incidencias por estado")
    print("5. Actualizar incidencia")
    print("6. Eliminar incidencia")
    print("0. Salir")
    print("=" * 60)


def main() -> None:
    """Ejecuta el menú principal de la aplicación."""
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_incidencia()

        elif opcion == "2":
            consultar_incidencia()

        elif opcion == "3":
            listar_todas_las_incidencias()

        elif opcion == "4":
            listar_incidencias_por_estado()

        elif opcion == "5":
            modificar_incidencia()

        elif opcion == "6":
            borrar_incidencia()

        elif opcion == "0":
            print("\nGracias por utilizar el sistema.")
            break

        else:
            print("\nOpción no válida. Intente nuevamente.")


if __name__ == "__main__":
    main()