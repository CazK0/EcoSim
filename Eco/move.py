import sqlite3
import random

DB_NAME = "ecosystem.db"

def move_entities():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT id, x, y FROM entities")
    entities = cursor.fetchall()

    for entity in entities:
        ent_id, old_x, old_y = entity

        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])

        new_x = max(0, min(49, old_x + dx))
        new_y = max(0, min(49, old_y + dy))

        cursor.execute("UPDATE entities SET x = ?, y = ? WHERE id = ?", (new_x, new_y, ent_id))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    move_entities()