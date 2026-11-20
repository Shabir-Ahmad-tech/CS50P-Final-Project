from project import (
    calculate_distance,
    generate_command,
    is_collision,
    is_within_bounds,
    parse_coordinations,
    parse_obstacle,
)


def test_parse_coordinations() -> None:
    assert parse_coordinations("0, 0") == (0, 0)
    assert parse_coordinations(" 3 , -2 ") == (3, -2)

    try:
        parse_coordinations("invalid")
        assert False, "Expected ValueError for invalid coordinate"
    except ValueError:
        pass


def test_parse_obstacle() -> None:
    assert parse_obstacle("") == []
    assert parse_obstacle("   ") == []
    assert parse_obstacle("2,3; 2,2; 1,3") == [(2, 3), (2, 2), (1, 3)]


def test_is_within_bounds() -> None:
    assert is_within_bounds((0, 0), 5) is True
    assert is_within_bounds((4, 4), 5) is True
    assert is_within_bounds((-1, 0), 5) is False
    assert is_within_bounds((5, 2), 5) is False


def test_calculate_distance() -> None:
    assert calculate_distance((0, 0), (3, 4)) == 5.0
    assert calculate_distance((2, 2), (2, 2)) == 0
    assert calculate_distance((-1, -1), (2, 3)) == 5.0


def test_is_collision() -> None:
    assert is_collision((0, 0), [(0, 0)]) is True
    assert is_collision((0, 0), [(0.5, 0)]) is True
    assert is_collision((0, 0), [(5, 5)]) is False
    assert is_collision((0, 0), [(1, 0)], 1.0) is True
    assert is_collision((0, 0), [(1, 0)], 0.5) is False


def test_generate_command() -> None:
    assert generate_command((0, 0), (5, 0)) == "MOVE_EAST 5.0"
    assert generate_command((5, 0), (2, 0)) == "MOVE_WEST 3.0"
    assert generate_command((0, 0), (0, 5)) == "MOVE_NORTH 5.0"
    assert generate_command((0, 5), (0, 2)) == "MOVE_SOUTH 3.0"
    assert generate_command((0, 0), (0, 0)) == "HALT"


def run_all_tests() -> None:
    test_parse_coordinations()
    test_parse_obstacle()
    test_is_within_bounds()
    test_calculate_distance()
    test_is_collision()
    test_generate_command()
    print("All function tests passed!")


if __name__ == "__main__":
    run_all_tests()