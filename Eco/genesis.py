import sqlite3
import os

DB_NAME = "ecosystem.db"


def create_universe():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    print(f"🌌 Connecting to {DB_NAME}...")
    with open("schema.sql", "r") as f:
        schema = f.read()
    cursor.executescript(schema)
    print("📜 Tables created successfully.")
    cursor.execute("SELECT count(*) FROM world_state")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO world_state (turn_count, width, height) VALUES (0, 50, 50)")
        print("🌍 World parameters set (50x50 Grid).")
    conn.commit()
    conn.close()
    print("✅ Genesis complete. The universe is ready.")


if __name__ == "__main__":
    if os.path.exists(DB_NAME):
        print("⚠️  Warning: Database already exists.")

    create_universe()