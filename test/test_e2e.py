import pytest
from src.incidente import (
    crear_incidencia,
    obtener_incidencia,
    actualizar_incidencia,
    eliminar_incidencia,
    listar_incidencias,
)
from src.base_datos import db

@pytest.fixture(autouse=True)
def limpiar_base_datos():
    """Limpia la base de datos antes de cada prueba."""
    db["incidencias"].clear()
    db["siguiente_id"] = 1

def test_flujo_completo_e2e():

    inc1 = crear_incidencia("Caída del sistema", "No responde", "crítica", "Soporte")
    inc2 = crear_incidencia("Error en reporte", "PDF no se genera", "alta", "Finanzas")
    inc3 = crear_incidencia("Lentitud en consulta", "Demora 10s", "media", "IT")


    assert len(listar_incidencias()) == 3
    assert inc1["estado"] == "abierta"
    assert inc2["estado"] == "abierta"
    assert inc3["estado"] == "abierta"


    actualizada = actualizar_incidencia(inc2["id"], estado="cerrada")
    assert actualizada["estado"] == "cerrada"


    abiertas = listar_incidencias(estado_filtro="abierta")
    assert len(abiertas) == 2
    ids_abiertas = {inc["id"] for inc in abiertas}
    assert inc1["id"] in ids_abiertas
    assert inc3["id"] in ids_abiertas


    assert eliminar_incidencia(inc3["id"]) is True
    assert len(listar_incidencias()) == 2
    with pytest.raises(Exception): 
        obtener_incidencia(inc3["id"])


    assert eliminar_incidencia(inc3["id"]) is False

  
    inc = obtener_incidencia(inc1["id"])
    assert inc["titulo"] == "Caída del sistema"