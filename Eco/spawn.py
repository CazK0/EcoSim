import sqlite3
import random

DB_NAME = "ecosystem.db"

def spawn_life(num_humans, num_zombies):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    print(f"Spawning {num_humans} Humans, {num_zombies} Zombies, and 1 Hero...")

    for i in range(num_humans):
        rand_x = random.randint(0, 49)
        rand_y = random.randint(0, 49)
        cursor.execute("INSERT INTO entities (x, y, type, color, energy) VALUES (?, ?, 'human', '#0000FF', 100)", (rand_x, rand_y))

    for i in range(num_zombies):
        rand_x = random.randint(0, 49)
        rand_y = random.randint(0, 49)
        cursor.execute("INSERT INTO entities (x, y, type, color, energy) VALUES (?, ?, 'zombie', '#FF0000', 100)", (rand_x, rand_y))

    cursor.execute("INSERT INTO entities (x, y, type, color, energy) VALUES (0, 0, 'player', '#00FF00', 100)")

    conn.commit()
    conn.close()
    print(" Outbreak started.")

if __name__ == "__main__":
    spawn_life(num_humans=80, num_zombies=1)
