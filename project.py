import math
import sys


def parse_coordinations(coord_str: str) -> tuple[int, int]:
    """Convert a string like '0, 0' into an (x, y) integer pair."""
    parts = coord_str.split(",")
    if len(parts) != 2:
        raise ValueError("Coordinate must use 'x, y' format.")

    x = int(parts[0].strip())
    y = int(parts[1].strip())
    return (x, y)


def parse_obstacle(obstacle_str: str) -> list[tuple[int, int]]:
    """Convert '2,3; 2,2; 1,3' into a list of (x, y) obstacle coordinates."""
    if not obstacle_str.strip():
        return []

    obstacles: list[tuple[int, int]] = []
    for item in obstacle_str.split(";"):
        if item.strip():
            obstacles.append(parse_coordinations(item))
    return obstacles


def is_within_bounds(pos: tuple[int, int], arena_size: int) -> bool:
    """Check whether a coordinate sits inside the arena grid."""
    x, y = pos
    return 0 <= x < arena_size and 0 <= y < arena_size


def display_map(
    arena_size: int,
    current_pos: tuple[int, int],
    goal: tuple[int, int],
    obstacles: list[tuple[int, int]],
) -> None:
    """Print a grid view of the arena with robot, goal, and obstacles."""
    print("\n[ARENA MAP]")

    for y in range(arena_size - 1, -1, -1):
        row = f"{y:>2} "
        for x in range(arena_size):
            spot = (x, y)
            if spot == current_pos:
                row += "[R]"
            elif spot == goal:
                row += "[G]"
            elif spot in obstacles:
                row += "[X]"
            else:
                row += " . "
        print(row)

    x_axis = "   " + "".join(f" {x} " for x in range(arena_size))
    print(x_axis)


def calculate_distance(p1: tuple[int, int], p2: tuple[int, int]) -> float:
    """Find the straight-line distance between two points."""
    x1, y1 = p1
    x2, y2 = p2
    distance = math.hypot(x2 - x1, y2 - y1)
    return round(distance, 2)


def is_collision(
    robot_pos: tuple[int, int],
    obstacle_pos: list[tuple[int, int]],
    safety_margin: float = 1.0,
) -> bool:
    """Return True if the robot is inside any obstacle's safety radius."""
    for obstacle in obstacle_pos:
        dist_robot_obs = calculate_distance(robot_pos, obstacle)
        if dist_robot_obs <= safety_margin:
            return True
    return False


def generate_command(current_pos: tuple[int, int], next_pos: tuple[int, int]) -> str:
    """Turn a coordinate step into a motor command string."""
    current_x, current_y = current_pos
    next_x, next_y = next_pos

    dx = next_x - current_x
    dy = next_y - current_y

    if dx == 0 and dy == 0:
        return "HALT"
    if dx > 0:
        return f"MOVE_EAST {float(dx)}"
    if dx < 0:
        return f"MOVE_WEST {abs(float(dx))}"
    if dy > 0:
        return f"MOVE_NORTH {float(dy)}"
    return f"MOVE_SOUTH {abs(float(dy))}"


def get_neighbor_moves(pos: tuple[int, int]) -> list[tuple[int, int]]:
    """Return the four adjacent grid spots: up, down, right, and left."""
    x, y = pos
    return [
        (x, y + 1),
        (x, y - 1),
        (x + 1, y),
        (x - 1, y),
    ]


def main() -> None:
    """Run the greedy obstacle-avoidance loop from start to goal."""
    try:
        arena_size = int(input("Enter Arena size (e.g. 5 for 5x5): ").strip())
        if arena_size <= 1:
            sys.exit("Arena size can't be lower than 2.")

        start = parse_coordinations(input("Enter starting position (x,y): ").strip())
        goal = parse_coordinations(input("Enter Goal position (x,y): ").strip())
        obstacles = parse_obstacle(input("Obstacle positions (x,y; x,y...): ").strip())
    except ValueError as error:
        sys.exit(f"Invalid input: {error}")

    if not is_within_bounds(start, arena_size):
        sys.exit("Starting position is outside the arena.")
    if not is_within_bounds(goal, arena_size):
        sys.exit("Goal position is outside the arena.")

    safety_margin = 1.0
    current_pos = start
    visited: set[tuple[int, int]] = {current_pos}
    step_count = 0
    max_steps = arena_size * arena_size * 4

    display_map(arena_size, current_pos, goal, obstacles)

    while current_pos != goal:
        if step_count >= max_steps:
            print("\nRobot Trapped: No collision-free route available!")
            return

        candidates = get_neighbor_moves(current_pos)
        safe_moves: list[tuple[int, int]] = []

        for move in candidates:
            if not is_within_bounds(move, arena_size):
                continue
            if move != goal and is_collision(move, obstacles, safety_margin=safety_margin):
                continue
            safe_moves.append(move)

        if not safe_moves:
            print("\nRobot Trapped: No collision-free route available!")
            return

        unvisited_safe = [m for m in safe_moves if m not in visited]
        if not unvisited_safe:
            print("\nRobot Trapped: No collision-free route available!")
            return

        next_pos = min(unvisited_safe, key=lambda pos: calculate_distance(pos, goal))
        command = generate_command(current_pos, next_pos)

        step_count += 1
        print(f"Step {step_count}: {current_pos} -> {next_pos} | Command: {command}")

        current_pos = next_pos
        visited.add(current_pos)

    print(f"\nGoal reached at {goal} in {step_count} step(s)! Command: {generate_command(current_pos, goal)}")
    display_map(arena_size, current_pos, goal, obstacles)


if __name__ == "__main__":
    main()