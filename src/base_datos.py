# Simulación de base de datos en memoria
db = {
    "incidents": {},
    "next_id": 1
}

def get_next_id():
    current = db["next_id"]
    db["next_id"] += 1
    return current