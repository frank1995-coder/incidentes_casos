import pytest
from src.incidente import (
    create_incident,
    get_incident,
    update_incident,
    delete_incident,
    list_incidents,
    IncidentNotFoundError
)
from src.base_datos import db

@pytest.fixture(autouse=True)
def clean_db():
    """Limpia la base de datos antes de cada prueba."""
    db["incidents"].clear()
    db["next_id"] = 1

# ---------- Unitarias y regresión ----------

@pytest.mark.regression
def test_create_incident_success():
    inc = create_incident("Fallo en login", "No permite acceso", "alta", "Juan Pérez")
    assert inc["id"] == 1
    assert inc["title"] == "Fallo en login"
    assert inc["status"] == "abierta"
    assert len(db["incidents"]) == 1

def test_create_incident_invalid_priority():
    with pytest.raises(ValueError, match="Prioridad no válida"):
        create_incident("Título", "Desc", "urgente", "Ana")

@pytest.mark.regression
def test_get_incident_existing():
    create_incident("Problema red", "Sin conexión", "crítica", "Admin")
    inc = get_incident(1)
    assert inc["priority"] == "crítica"

@pytest.mark.regression
def test_get_incident_not_found():
    with pytest.raises(IncidentNotFoundError):
        get_incident(99)

@pytest.mark.regression
def test_update_incident():
    create_incident("Bug", "Desc", "baja", "Dev")
    updated = update_incident(1, status="cerrada", assigned_to="QA")
    assert updated["status"] == "cerrada"
    assert updated["assigned_to"] == "QA"

def test_update_incident_invalid_field():
    create_incident("Bug", "Desc", "baja", "Dev")
    with pytest.raises(ValueError, match="Campo no permitido"):
        update_incident(1, no_existe="valor")

@pytest.mark.regression
def test_delete_incident():
    create_incident("Test", "Desc", "media", "User")
    assert delete_incident(1) is True
    assert len(db["incidents"]) == 0

def test_delete_incident_not_exist():
    assert delete_incident(10) is False

@pytest.mark.regression
def test_list_incidents_with_filter():
    create_incident("Inc1", "d", "baja", "A")
    create_incident("Inc2", "d", "media", "B")
    update_incident(1, status="cerrada")
    result = list_incidents(filter_status="cerrada")
    assert len(result) == 1
    assert result[0]["id"] == 1