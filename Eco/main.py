import time
from move import move_entities
from render import render_world


def run_simulation():
    turn = 1
    while True:
        print(f"Processing Turn {turn}...")

        move_entities()
        render_world()

        turn += 1
        time.sleep(1)


if __name__ == "__main__":
    run_simulation()