from .base_datos import db, get_next_id

class IncidentNotFoundError(Exception):
    """Excepción personalizada para incidencia no encontrada."""
    pass

def create_incident(title: str, description: str, priority: str, assigned_to: str) -> dict:
    """Crea una nueva incidencia y la almacena."""
    if priority not in ("baja", "media", "alta", "crítica"):
        raise ValueError("Prioridad no válida. Use: baja, media, alta, crítica.")

    incident_id = get_next_id()
    incident = {
        "id": incident_id,
        "title": title.strip(),
        "description": description.strip(),
        "priority": priority,
        "status": "abierta",
        "assigned_to": assigned_to.strip()
    }
    db["incidents"][incident_id] = incident
    return incident

def get_incident(incident_id: int) -> dict:
    """Obtiene una incidencia por ID. Lanza IncidentNotFoundError si no existe."""
    incident = db["incidents"].get(incident_id)
    if incident is None:
        raise IncidentNotFoundError(f"Incidencia con ID {incident_id} no encontrada.")
    return incident

def update_incident(incident_id: int, **kwargs) -> dict:
    """Actualiza campos de una incidencia existente."""
    incident = get_incident(incident_id)
    allowed_fields = {"title", "description", "priority", "status", "assigned_to"}
    for key, value in kwargs.items():
        if key not in allowed_fields:
            raise ValueError(f"Campo no permitido: {key}")
        if key == "priority" and value not in ("baja", "media", "alta", "crítica"):
            raise ValueError("Prioridad no válida.")
        incident[key] = value.strip() if isinstance(value, str) else value
    db["incidents"][incident_id] = incident
    return incident

def delete_incident(incident_id: int) -> bool:
    """Elimina una incidencia. Retorna True si existía, False si no."""
    if incident_id in db["incidents"]:
        del db["incidents"][incident_id]
        return True
    return False

def list_incidents(filter_status: str = None) -> list:
    """Lista todas las incidencias, opcionalmente filtradas por estado."""
    if filter_status:
        return [inc for inc in db["incidents"].values() if inc["status"] == filter_status]
    return list(db["incidents"].values())