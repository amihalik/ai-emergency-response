from typing import Optional, Tuple

from database import get_connection, init_db, seed_data
import sqlite3

INCIDENT_RESOURCE_MAP = {
    "fire": "fire",
    "medical": "hospital",
    "accident": "hospital",
    "crime": "police",
    "violence": "police",
}

SPEED_MPH = 30  # assumed average speed
MILES_PER_DEGREE = 69.0  # rough conversion for latitude/longitude degrees


def distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    return ((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2) ** 0.5


def eta_minutes(dist_deg: float) -> float:
    miles = dist_deg * MILES_PER_DEGREE
    return (miles / SPEED_MPH) * 60


def get_nearest_resource(conn: sqlite3.Connection, resource_type: str, lat: float, lon: float) -> Optional[Tuple[int, float]]:
    cur = conn.cursor()
    cur.execute(
        "SELECT id, latitude, longitude FROM resources WHERE type=? AND availability>0",
        (resource_type,),
    )
    rows = cur.fetchall()
    if not rows:
        return None
    rows.sort(key=lambda r: distance(lat, lon, r[1], r[2]))
    res_id, rlat, rlon = rows[0]
    dist = distance(lat, lon, rlat, rlon)
    return res_id, dist


def handle_incident(
    conn: sqlite3.Connection, incident_type: str, lat: float, lon: float
) -> Optional[Tuple[int, int, float]]:
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO incidents (type, latitude, longitude) VALUES (?, ?, ?)",
        (incident_type, lat, lon),
    )
    incident_id = cur.lastrowid
    resource_type = INCIDENT_RESOURCE_MAP.get(incident_type, "police")
    nearest = get_nearest_resource(conn, resource_type, lat, lon)
    if nearest is None:
        conn.commit()
        return None
    res_id, dist = nearest
    eta = eta_minutes(dist)
    cur.execute(
        "UPDATE incidents SET assigned_resource_id=?, eta_minutes=? WHERE id=?",
        (res_id, eta, incident_id),
    )
    cur.execute(
        "UPDATE resources SET availability=availability-1 WHERE id=?",
        (res_id,),
    )
    conn.commit()
    return incident_id, res_id, eta


if __name__ == "__main__":
    conn = get_connection()
    init_db(conn)
    seed_data(conn)
    result = handle_incident(conn, "fire", 40.7200, -74.0000)
    if result:
        inc_id, res_id, eta = result
        print(f"Incident {inc_id} assigned to resource {res_id} with ETA {eta:.1f} minutes")
    else:
        print("No available resource found for incident")

