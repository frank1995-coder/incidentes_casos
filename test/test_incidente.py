import pytest
from src.incidente import (
    crear_incidencia,
    obtener_incidencia,
    actualizar_incidencia,
    eliminar_incidencia,
    listar_incidencias,
    IncidenciaNoEncontradaError
)
from src.base_datos import reiniciar_base_datos

@pytest.fixture(autouse=True)
def limpiar_base_datos():
    """Reinicia la base de datos antes de cada prueba."""
    reiniciar_base_datos()

# ---------- Unitarias y regresión ----------

@pytest.mark.regression
def test_crear_incidencia_exitoso():
    inc = crear_incidencia("Fallo en login", "No permite acceso", "alta", "Juan Pérez")
    assert inc["id"] == 1
    assert inc["titulo"] == "Fallo en login"
    assert inc["estado"] == "abierta"
    assert len(listar_incidencias()) == 1

def test_crear_incidencia_prioridad_invalida():
    with pytest.raises(ValueError, match="Prioridad no válida"):
        crear_incidencia("Título", "Desc", "urgente", "Ana")

@pytest.mark.regression
def test_obtener_incidencia_existente():
    crear_incidencia("Problema red", "Sin conexión", "crítica", "Admin")
    inc = obtener_incidencia(1)
    assert inc["prioridad"] == "crítica"

@pytest.mark.regression
def test_obtener_incidencia_no_encontrada():
    with pytest.raises(IncidenciaNoEncontradaError):
        obtener_incidencia(99)

@pytest.mark.regression
def test_actualizar_incidencia():
    crear_incidencia("Bug", "Desc", "baja", "Dev")
    actualizada = actualizar_incidencia(1, estado="cerrada", asignado_a="QA")
    assert actualizada["estado"] == "cerrada"
    assert actualizada["asignado_a"] == "QA"

def test_actualizar_incidencia_campo_invalido():
    crear_incidencia("Bug", "Desc", "baja", "Dev")
    with pytest.raises(ValueError, match="Campo no permitido"):
        actualizar_incidencia(1, no_existe="valor")

@pytest.mark.regression
def test_eliminar_incidencia():
    crear_incidencia("Test", "Desc", "media", "User")
    assert eliminar_incidencia(1) is True
    assert len(listar_incidencias()) == 0

def test_eliminar_incidencia_no_existe():
    assert eliminar_incidencia(10) is False

@pytest.mark.regression
def test_listar_incidencias_con_filtro():
    crear_incidencia("Inc1", "d", "baja", "A")
    crear_incidencia("Inc2", "d", "media", "B")
    actualizar_incidencia(1, estado="cerrada")
    resultado = listar_incidencias(estado_filtro="cerrada")
    assert len(resultado) == 1
    assert resultado[0]["id"] == 1