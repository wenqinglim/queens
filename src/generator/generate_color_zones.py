"""Generate color zones for the game.
In a game of Queens, players place N Queens in an NxN grid, and each Queen must not be able to attack each other.
Each Queen is also contained by a unique color zone, where each color zone only has one Queen.
The color zones can take up any number of adjacent tiles.
The zones force the grid to only have a single possible solution."""

from config import color_map


def generate_color_zones(queens_positions: list[tuple[int, int]]) -> list[dict]:
    """Generate color zones for the game.

    Args:
        queens_positions (list[tuple[int, int]]): The positions of the queens on the grid.

    Returns:
        list[dict]: The color zones for the game.
        E.g. [
        {"color": "red", "x": [0, 0, 0, 1], "y": [0, 1, 2, 2]},
        {"color": "blue", "x": [1, 1, 2], "y": [0, 1, 1]},
        {"color": "green", "x": [2, 3, 3], "y": [0, 0, 1]},
        {"color": "yellow", "x": [0, 1, 2, 2, 3, 3], "y": [3, 3, 2, 3, 2, 3]}
        ]
    """
    color_zones = []
    n = len(queens_positions)

    # Get the unique colors from color_map
    queen_colors = list(color_map.keys())[:n]

    # Initialize the color zones
    for color in queen_colors:
        color_zones.append(
            {
                "color": color,
                "x": [queen["x"] for queen in queens_positions],
                "y": [queen["y"] for queen in queens_positions],
            }
        )

    # Generate the color zones
    # TODO: Implement the logic to generate the color zones

    return color_zones
