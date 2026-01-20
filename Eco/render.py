import sqlite3

DB_NAME = "ecosystem.db"
HTML_FILE = "world.html"

def render_world():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT width, height FROM world_state")
    try:
        width, height = cursor.fetchone()
    except TypeError:
        width, height = 50, 50
    cursor.execute("SELECT x, y, type, color FROM entities")
    entities = cursor.fetchall()

    entity_map = {}
    for ent in entities:
        x, y, type_name, color = ent
        entity_map[(x, y)] = color

    conn.close()
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="refresh" content="1"> 

        <style>
            body {{ background-color: #222; color: white; font-family: sans-serif; }}
            .grid-container {{
                display: grid;
                grid-template-columns: repeat({width}, 15px);
                grid-template-rows: repeat({height}, 15px);
                gap: 1px;
                width: fit-content;
                margin: 20px auto;
                border: 2px solid #555;
            }}
            .cell {{
                width: 15px;
                height: 15px;
                background-color: #1a1a1a;
            }}
            .entity {{
                width: 100%;
                height: 100%;
                border-radius: 50%;
                transition: all 0.3s; /* Makes the color change smooth */
            }}
        </style>
    </head>
    <body>
        <h2 style="text-align:center">Infection Simulation (Live)</h2>
        <div class="grid-container">
    """
    for y in range(height):
        for x in range(width):
            if (x, y) in entity_map:
                color = entity_map[(x, y)]
                html_content += f'<div class="cell"><div class="entity" style="background-color:{color}"></div></div>'
            else:
                html_content += '<div class="cell"></div>'

    html_content += """
        </div>
    </body>
    </html>
    """
    with open(HTML_FILE, "w") as f:
        f.write(html_content)
if __name__ == "__main__":
    render_world()
