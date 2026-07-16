import pytest
from src.incidente import (
    create_incident,
    get_incident,
    update_incident,
    delete_incident,
    list_incidents,
)
from src.base_datos import db

@pytest.fixture(autouse=True)
def clean_db():
    db["incidents"].clear()
    db["next_id"] = 1

def test_full_workflow_e2e():
    # 1. Crear incidencias
    inc1 = create_incident("Caída del sistema", "No responde", "crítica", "Soporte")
    inc2 = create_incident("Error en reporte", "PDF no se genera", "alta", "Finanzas")
    inc3 = create_incident("Lentitud en consulta", "Demora 10s", "media", "IT")

    # 2. Verificar que se crearon correctamente
    assert len(list_incidents()) == 3
    assert inc1["status"] == "abierta"
    assert inc2["status"] == "abierta"
    assert inc3["status"] == "abierta"

    # 3. Actualizar estado de una incidencia (simular cierre)
    updated = update_incident(inc2["id"], status="cerrada")
    assert updated["status"] == "cerrada"

    # 4. Listar solo las abiertas
    abiertas = list_incidents(filter_status="abierta")
    assert len(abiertas) == 2
    ids_abiertas = {inc["id"] for inc in abiertas}
    assert inc1["id"] in ids_abiertas
    assert inc3["id"] in ids_abiertas

    # 5. Eliminar una incidencia
    assert delete_incident(inc3["id"]) is True
    assert len(list_incidents()) == 2
    with pytest.raises(Exception):  # get_incident lanza IncidentNotFoundError
        get_incident(inc3["id"])

    # 6. Intento de eliminar una incidencia ya borrada
    assert delete_incident(inc3["id"]) is False

    # 7. Verificar que la incidencia restante se puede leer
    inc = get_incident(inc1["id"])
    assert inc["title"] == "Caída del sistema"