from database import get_connection, init_db, seed_data
from resource_management import handle_incident


def main():
    conn = get_connection()
    init_db(conn)
    seed_data(conn)
    # Example incident
    result = handle_incident(conn, "medical", 40.7210, -74.0040)
    if result:
        inc_id, res_id, eta = result
        print(
            f"Incident {inc_id} assigned to resource {res_id} with ETA {eta:.1f} minutes"
        )
    else:
        print("No available resource found")


if __name__ == "__main__":
    main()

