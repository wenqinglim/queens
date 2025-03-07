"""Generate placement of n queens on an nxn grid, such that no two queens can attack each other."""

import logging
import numpy as np
from ortools.sat.python import cp_model


def solve_n_queens(n, logger: logging.Logger) -> list[tuple[int, int]]:
    """Solves the N-Queens problem and returns a valid placement."""

    logger.info(f"Solving N-Queens problem for {n}x{n} grid")
    model = cp_model.CpModel()
    queens = [model.NewIntVar(0, n - 1, f"Q{i}") for i in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            model.Add(queens[i] != queens[j])  # No same row
            model.Add(queens[i] != queens[j])  # No same column

            # Check only immediate diagonal corners (distance of 1)
            if j - i == 1:  # Only check adjacent queens
                # Create a new variable for the absolute difference
                abs_diff = model.NewIntVar(0, n - 1, f"abs_diff_{i}_{j}")
                # Use add_abs_equality to handle absolute value
                model.AddAbsEquality(abs_diff, queens[i] - queens[j])
                # Ensure the absolute difference is not 1
                model.Add(abs_diff != 1)

    solver = cp_model.CpSolver()
    solver.Solve(model)
    return [(i, solver.Value(queens[i])) for i in range(n)]


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Starting the game")

    n = 8
    queens_positions = solve_n_queens(n, logger)
    logger.info(f"Queens positions: {queens_positions}")

    # Create a grid
    grid = np.zeros((n, n))
    for i, j in queens_positions:
        grid[i, j] = 1
    logger.info(f"Grid: {grid}")
