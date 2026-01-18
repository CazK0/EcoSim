import time
import sqlite3  # <--- Need this to check the count
from move import move_entities
from render import render_world
from interactions import handle_interactions
from metabolism import apply_metabolism

DB_NAME = "ecosystem.db"


def run_simulation():
    turn = 1

    while True:
        print(f"--- Turn {turn} ---")
        move_entities()
        handle_interactions()
        apply_metabolism()
        render_world()
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("SELECT count(*) FROM entities WHERE type='rabbit'")
        rabbits_left = cursor.fetchone()[0]
        conn.close()

        print(f"🐰 Rabbits Remaining: {rabbits_left}")

        if rabbits_left == 0:
            print("\n" + "=" * 40)
            print(f"💀 GAME OVER: EXTINCTION EVENT")
            print(f"The colony survived for {turn} turns.")
            print("=" * 40 + "\n")
            break  

        turn += 1
        time.sleep(1)


if __name__ == "__main__":
    run_simulation()
