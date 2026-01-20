import sqlite3
import threading
import os
from flask import Flask, request, jsonify
from genesis import create_universe
from spawn import spawn_life
from main import run_simulation

app = Flask(__name__)
DB_NAME = "ecosystem.db"


def initialize_world():
    if not os.path.exists(DB_NAME):
        create_universe()
        spawn_life(num_humans=100, num_zombies=1)


def get_db_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/move_player', methods=['POST'])
def move_player():
    data = request.json
    direction = data.get('direction')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, x, y FROM entities WHERE type='player'")
    player = cursor.fetchone()

    if player:
        p_id, x, y = player['id'], player['x'], player['y']

        if direction == 'w':
            y -= 1
        elif direction == 's':
            y += 1
        elif direction == 'a':
            x -= 1
        elif direction == 'd':
            x += 1

        cursor.execute("SELECT width, height FROM world_state")
        w, h = cursor.fetchone()
        x = max(0, min(w - 1, x))
        y = max(0, min(h - 1, y))

        cursor.execute("UPDATE entities SET x=?, y=? WHERE id=?", (x, y, p_id))
        conn.commit()

    conn.close()
    return jsonify(success=True)


@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT width, height FROM world_state")
    try:
        width, height = cursor.fetchone()
    except TypeError:
        width, height = 50, 50

    cursor.execute("SELECT x, y, type FROM entities")
    entities = cursor.fetchall()
    conn.close()

    entity_map = {}
    human_count = 0
    zombie_count = 0
    player_alive = False

    for ent in entities:
        x, y, type_name = ent[0], ent[1], ent[2]

        if type_name == 'zombie':
            symbol = "Z"
            color = "#FF0000"  # Red
            zombie_count += 1
        elif type_name == 'human':
            symbol = "H"
            color = "#44aaff"  # Blue
            human_count += 1
        elif type_name == 'player':
            symbol = "P"
            color = "#00FF00"  # Green
            player_alive = True
        else:
            symbol = "?"
            color = "#888"

        entity_map[(x, y)] = (symbol, color)

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="refresh" content="0.5">
        <title>Zombie Survival</title>
        <style>
            body {{ background-color: #1a1a1a; color: white; font-family: 'Courier New', monospace; text-align: center; }}
            .grid-container {{
                display: grid;
                grid-template-columns: repeat({width}, 20px);
                grid-template-rows: repeat({height}, 20px);
                gap: 1px;
                width: fit-content; margin: 0 auto;
                background-color: #000; border: 4px solid #444;
            }}
            .cell {{
                width: 20px; height: 20px; background-color: #222;
                display: flex; align-items: center; justify-content: center;
                font-size: 16px; font-weight: bold;
            }}
        </style>
        <script>
            document.addEventListener('keydown', function(event) {{
                const key = event.key.toLowerCase();
                if (['w', 'a', 's', 'd'].includes(key)) {{
                    fetch('/move_player', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify({{direction: key}})
                    }}).then(() => {{
                        window.location.reload(); 
                    }});
                }}
            }});
        </script>
    </head>
    <body>
        <h1>STATUS: {'ALIVE' if player_alive else 'DEAD'}</h1>
        <h3>H: {human_count} | Z: {zombie_count}</h3>

        <div class="grid-container">
    """

    for y in range(height):
        for x in range(width):
            if (x, y) in entity_map:
                symbol, color = entity_map[(x, y)]
                html_content += f'<div class="cell" style="color:{color}">{symbol}</div>'
            else:
                html_content += '<div class="cell"></div>'

    html_content += "</div></body></html>"
    return html_content


if __name__ == '__main__':
    initialize_world()

    simulation_thread = threading.Thread(target=run_simulation)
    simulation_thread.daemon = True
    simulation_thread.start()

    app.run(debug=True, use_reloader=False, port=5000)