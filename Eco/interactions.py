import sqlite3

DB_NAME = "ecosystem.db"


def handle_interactions():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT x, y FROM entities GROUP BY x, y HAVING count(*) > 1")
    collision_spots = cursor.fetchall()

    for pos in collision_spots:
        x, y = pos

        cursor.execute("SELECT id, type, energy FROM entities WHERE x = ? AND y = ?", (x, y))
        entities_at_spot = cursor.fetchall()

        wolves = [e for e in entities_at_spot if e[1] == 'wolf']
        rabbits = [e for e in entities_at_spot if e[1] == 'rabbit']

        if wolves and rabbits:
            for rabbit in rabbits:
                rabbit_id = rabbit[0]
                cursor.execute("DELETE FROM entities WHERE id = ?", (rabbit_id,))
                print(f"💀 Rabbit {rabbit_id} was eaten at {x}, {y}")

            for wolf in wolves:
                wolf_id = wolf[0]
                cursor.execute("UPDATE entities SET energy = energy + 20 WHERE id = ?", (wolf_id,))

    conn.commit()
    conn.close()