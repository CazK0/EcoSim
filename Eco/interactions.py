import sqlite3

DB_NAME = "ecosystem.db"


def handle_interactions():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT x, y FROM entities GROUP BY x, y HAVING count(*) > 1")
    collision_spots = cursor.fetchall()

    for pos in collision_spots:
        x, y = pos

        cursor.execute("SELECT id, type FROM entities WHERE x = ? AND y = ?", (x, y))
        entities = cursor.fetchall()

        zombies = [e for e in entities if e[1] == 'zombie']
        victims = [e for e in entities if e[1] in ('human', 'player')]

        if zombies and victims:
            for victim in victims:
                victim_id = victim[0]
                victim_type = victim[1]

                cursor.execute("DELETE FROM entities WHERE id = ?", (victim_id,))

                if victim_type == 'player':
                    print(f" GAME OVER: The Hero was eaten at {x}, {y}")

                cursor.execute("""
                    INSERT INTO entities (x, y, type, color, energy) 
                    VALUES (?, ?, 'zombie', '#FF0000', 100)
                """, (x, y))

            for zombie in zombies:
                cursor.execute("UPDATE entities SET energy = energy + 20 WHERE id = ?", (zombie[0],))

    conn.commit()
    conn.close()
