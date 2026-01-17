import sqlite3
import random

DB_NAME = "ecosystem.db"


def spawn_life(num_rabbits, num_wolves):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    print(f"🧬 Spawning {num_rabbits} Rabbits and {num_wolves} Wolves...")

    for i in range(num_rabbits):
        rand_x = random.randint(0, 49)
        rand_y = random.randint(0, 49)
        cursor.execute("""
            INSERT INTO entities (x, y, type, color, energy)
            VALUES (?, ?, 'rabbit', 'white', 50)
        """, (rand_x, rand_y))

    for i in range(num_wolves):
        rand_x = random.randint(0, 49)
        rand_y = random.randint(0, 49)
        cursor.execute("""
            INSERT INTO entities (x, y, type, color, energy)
            VALUES (?, ?, 'wolf', 'red', 100)
        """, (rand_x, rand_y))

    conn.commit()
    print("✅ Life added successfully.")

    cursor.execute("SELECT type, count(*) FROM entities GROUP BY type")
    stats = cursor.fetchall()
    print("\n📊 Current Population:")
    for stat in stats:
        print(f"   {stat[0].capitalize()}s: {stat[1]}")

    conn.close()


if __name__ == "__main__":
    spawn_life(num_rabbits=10, num_wolves=2)