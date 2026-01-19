import time
from move import move_entities
from render import render_world
from interactions import handle_interactions
from metabolism import apply_metabolism


def run_simulation():
    turn = 1
    while True:
        print(f"--- Turn {turn} ---")

        move_entities()
        handle_interactions()
        apply_metabolism()
        render_world()
        turn += 1
        time.sleep(1)


if __name__ == "__main__":
    run_simulation()
