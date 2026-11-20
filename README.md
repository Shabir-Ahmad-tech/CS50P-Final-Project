# Autonomous Robot Navigation (Greedy Obstacle Avoidance)

A terminal-based Python navigation simulator where a robot moves through a 2D grid arena from a start point to a goal while avoiding obstacles and walls.

## How It Works

The program uses a simple **greedy avoidance loop**:

1. Check the four neighboring spots (`UP`, `DOWN`, `LEFT`, `RIGHT`) around the robot.
2. Skip spots outside the arena grid.
3. Skip spots inside an obstacle's `safety_margin` (unless the spot is the goal).
4. Skip spots the robot has already visited so it does not loop back and forth.
5. Pick the remaining safe spot closest to the goal using straight-line (`math.hypot`) distance.
6. Translate the move into a motor command (`MOVE_NORTH`, `MOVE_SOUTH`, `MOVE_EAST`, `MOVE_WEST`, or `HALT`).

If no unvisited safe move is available, the robot stops and prints a warning that it is trapped.

## Project Structure

- `project.py` — Main navigation program, map display, input parsers, and helper functions.
- `tests_manual.py` — Manual `assert` test script for checking helper functions without `pytest`.
- `requirements.txt` — Dependency notes (standard library only).

## Requirements

- Python 3.10 or higher

## How to Run

Run the main program from your terminal:

```bash
python project.py

