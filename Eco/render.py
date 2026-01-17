import sqlite3

DB_NAME = "ecosystem.db"
HTML_FILE = "world.html"


def render_world():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT width, height FROM world_state")
    width, height = cursor.fetchone()
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
        <style>
            body {{ background-color: #333; color: white; font-family: monospace; }}
            .grid-container {{
                display: grid;
                grid-template-columns: repeat({width}, 15px); /* 15px wide columns */
                grid-template-rows: repeat({height}, 15px);    /* 15px tall rows */
                gap: 1px;
                width: fit-content;
                margin: 20px auto;
                background-color: #222;
                border: 1px solid #555;
            }}
            .cell {{
                width: 15px;
                height: 15px;
                background-color: #1a1a1a; /* Empty cell color */
            }}
            .entity {{
                border-radius: 50%; /* Circle */
                width: 100%;
                height: 100%;
            }}
        </style>
    </head>
    <body>
        <h1 style="text-align:center">World State</h1>
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

    print(f"🖼️  Rendered {HTML_FILE}. Open it in your browser.")


if __name__ == "__main__":
    render_world()