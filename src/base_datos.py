# Simulación de base de datos en memoria
db = {
    "incidencias": {},
    "siguiente_id": 1
}

def obtener_siguiente_id():
    actual = db["siguiente_id"]
    db["siguiente_id"] += 1
    return actual