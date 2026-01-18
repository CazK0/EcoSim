import sqlite3

DB_NAME = "ecosystem.db"


def apply_metabolism():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE entities SET energy = energy - 1")
    cursor.execute("SELECT count(*) FROM entities WHERE energy <= 0")
    deaths = cursor.fetchone()[0]

    if deaths > 0:
        cursor.execute("DELETE FROM entities WHERE energy <= 0")
        print(f"⚰️  {deaths} entities starved to death.")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    apply_metabolism()