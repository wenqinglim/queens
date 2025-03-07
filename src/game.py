"""
This module contains the main game logic for the game.

In a game of Queens, players place N Queens in an NxN grid, and each Queen must not be able to attack each other.
Each Queen is also contained by a unique color zone, where each color zone only has one Queen.
The color zones can take up any number of adjacent tiles.
The zones force the grid to only have a single possible solution.
"""

import pygame
import logging
import numpy as np
from config import color_map


class Queens:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.n = None
        self.grid = np.array([])
        self.queens = []
        self.color_zones = []
        self.color_zone_queens = {}
        self.queen_image = pygame.image.load(
            "assets/images/queen_icon.jpg"
        )  # Default queen image

    def initialize_game(self, game_config: dict):
        """
        Initialize the game with the given game config

        Args:
            game_config (dict): The game config. Example: game_store/game_001.py
        """
        self.n = game_config["n"]

        # Initialize the grid
        self.grid = np.zeros((self.n, self.n))
        self.logger.info(f"Initialized {self.n}x{self.n} grid")

        # Initialize the color zones from game config
        self.color_zones = game_config["color_zones"]
        self.logger.info(f"Initialized {len(self.color_zones)} color zones")

        # Store the queen positions from game config
        self.queens = game_config["queens"]
        self.logger.info(f"Stored {len(self.queens)} queens")

        # Load the queen image
        if game_config.get("queen_image"):
            self.queen_image = pygame.image.load(game_config["queen_image"])

        # Print grid
        self.logger.info(f"Grid: {self.grid}")

    def is_queen_same_column(self, x: int) -> bool:
        """Check if the queen is in the same column as another queen"""
        if self.grid[x].sum() == 1:
            return True
        return False

    def is_queen_same_row(self, y: int) -> bool:
        """Check if the queen is in the same row as another queen"""
        if self.grid[:, y].sum() == 1:
            return True
        return False

    def get_color_zone(self, x: int, y: int) -> bool:
        """Get the color zone of the coordinates"""
        for color_zone in self.color_zones:
            x_coords = color_zone["x"]
            y_coords = color_zone["y"]
            for x_coord, y_coord in zip(x_coords, y_coords):
                if x == x_coord and y == y_coord:
                    return color_zone["color"]
        return None

    def is_queen_same_color_zone(self, x: int, y: int) -> bool:
        """Check if the queen is in the same color zone as another queen"""
        queen_color_zone = self.get_color_zone(x, y)
        if queen_color_zone is not None:
            return queen_color_zone in self.color_zone_queens.keys()
        return False

    def is_queen_same_corner(self, x: int, y: int) -> bool:
        """Check if the queen is in the corner of another queen"""
        corners = []
        if x > 0 and y > 0:  # Top-left corner
            corners.append(self.grid[x - 1][y - 1])
        if x > 0 and y < self.n - 1:  # Top-right corner
            corners.append(self.grid[x - 1][y + 1])
        if x < self.n - 1 and y > 0:  # Bottom-left corner
            corners.append(self.grid[x + 1][y - 1])
        if x < self.n - 1 and y < self.n - 1:  # Bottom-right corner
            corners.append(self.grid[x + 1][y + 1])

        if 1 in corners:
            return True
        return False

    def is_queen_correct(self, x: int, y: int) -> dict:
        """Check if queen placement adheres to game rules:
        1. No two queens can be in the same row
        2. No two queens can be in the same column
        3. No two queens can be in the same color zone
        4. No two queens can be in the corner of another queen
        """
        checks = {
            "row": True,
            "column": True,
            "color_zone": True,
            "corner": True,
        }
        checks["row"] = not self.is_queen_same_row(y)
        checks["column"] = not self.is_queen_same_column(x)
        checks["color_zone"] = not self.is_queen_same_color_zone(x, y)
        checks["corner"] = not self.is_queen_same_corner(x, y)

        self.logger.info(f"Checks: {checks}")

        return checks

    def display_title(
        self,
        screen: pygame.Surface,
        title_font: pygame.font.Font,
        WINDOW_WIDTH: int,
        TITLE_HEIGHT: int,
    ):
        # Draw title
        title_text = title_font.render("Queens", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, TITLE_HEIGHT // 2))
        screen.blit(title_text, title_rect)

    def display_frame(
        self,
        screen: pygame.Surface,
        GRID_SIZE: int,
        TITLE_HEIGHT: int,
        FRAME_PADDING: int,
    ):
        frame_rect = pygame.Rect(
            FRAME_PADDING - 2,
            TITLE_HEIGHT + FRAME_PADDING - 2,
            self.n * GRID_SIZE + 4,
            self.n * GRID_SIZE + 4,
        )
        pygame.draw.rect(screen, (0, 0, 0), frame_rect, 2)  # Black frame

    def display_grid(
        self,
        screen: pygame.Surface,
        GRID_SIZE: int,
        TITLE_HEIGHT: int,
        FRAME_PADDING: int,
    ):
        # Draw grid and color zones
        for i in range(self.n):
            for j in range(self.n):
                cell_x = FRAME_PADDING + (i * GRID_SIZE)
                cell_y = TITLE_HEIGHT + FRAME_PADDING + (j * GRID_SIZE)
                pygame.draw.rect(
                    screen, (255, 255, 255), (cell_x, cell_y, GRID_SIZE, GRID_SIZE)
                )

    def display_color_zones(
        self,
        screen: pygame.Surface,
        GRID_SIZE: int,
        TITLE_HEIGHT: int,
        FRAME_PADDING: int,
    ):
        ## Display color zones
        for color_zone in self.color_zones:
            color = color_zone["color"]
            x_coords = color_zone["x"]
            y_coords = color_zone["y"]
            for x_coord, y_coord in zip(x_coords, y_coords):
                cell_x = FRAME_PADDING + (x_coord * GRID_SIZE)
                cell_y = TITLE_HEIGHT + FRAME_PADDING + (y_coord * GRID_SIZE)
                pygame.draw.rect(
                    screen, color_map[color], (cell_x, cell_y, GRID_SIZE, GRID_SIZE)
                )

    def run(self):
        # Constants for UI layout
        GRID_SIZE = 100  # Size of each cell
        FRAME_PADDING = 40  # Padding around the grid
        TITLE_HEIGHT = 60  # Height for title area

        # Calculate total window size
        WINDOW_WIDTH = self.n * GRID_SIZE + (FRAME_PADDING * 2)
        WINDOW_HEIGHT = self.n * GRID_SIZE + (FRAME_PADDING * 2) + TITLE_HEIGHT

        # Display the grid
        pygame.init()
        # screen = pygame.display.set_mode((self.n * 100, self.n * 100))
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        pygame.display.set_caption("Queens")
        clock = pygame.time.Clock()

        # Initialize fonts
        title_font = pygame.font.Font(None, 48)
        clock_font = pygame.font.Font(None, 30)

        start_time = pygame.time.get_ticks()
        n_valid_queens = 0
        running = True

        # Display the grid
        screen.fill((255, 255, 255))  # White background

        self.display_title(screen, title_font, WINDOW_WIDTH, TITLE_HEIGHT)
        self.display_frame(screen, GRID_SIZE, TITLE_HEIGHT, FRAME_PADDING)
        self.display_grid(screen, GRID_SIZE, TITLE_HEIGHT, FRAME_PADDING)
        self.display_color_zones(screen, GRID_SIZE, TITLE_HEIGHT, FRAME_PADDING)

        while running:
            # Calculate elapsed time
            elapsed_time = (
                pygame.time.get_ticks() - start_time
            ) // 1000  # Convert to seconds
            minutes = elapsed_time // 60
            seconds = elapsed_time % 60

            # Clear previous time text area with background color
            time_rect = pygame.Rect(
                FRAME_PADDING, FRAME_PADDING // 2, 130, 30
            )  # Width=150 to fit time text
            pygame.draw.rect(
                screen, (255, 255, 255), time_rect
            )  # Fill with white background

            time_text = clock_font.render(
                f"Time: {minutes:02d}:{seconds:02d}", True, (0, 0, 0)
            )
            screen.blit(time_text, (FRAME_PADDING, FRAME_PADDING // 2))

            # Update the display when user places a queen
            for event in pygame.event.get():
                # If it is a left click, place or remove a queen
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    x = (x - FRAME_PADDING) // GRID_SIZE
                    y = (y - (TITLE_HEIGHT + FRAME_PADDING)) // GRID_SIZE

                    # If the cell is already a queen, remove it
                    if self.grid[x][y] == 1:
                        self.grid[x][y] = 0
                        n_valid_queens -= 1

                        queen_color_zone = self.get_color_zone(x, y)
                        if queen_color_zone in self.color_zone_queens.keys():
                            del self.color_zone_queens[queen_color_zone]

                        # Remove the queen image from the screen
                        screen.blit(pygame.Surface((100, 100)), (x * 100, y * 100))
                        # Add color zone back to the screen
                        color = color_map[queen_color_zone]
                        pygame.draw.rect(screen, color, (x * 100, y * 100, 100, 100))

                    # If the cell is not a queen, place a queen (if valid)
                    else:
                        # Check if queen placement adheres to game rules
                        checks = self.is_queen_correct(x, y)
                        if all(checks.values()):
                            self.logger.info("Queen placement is valid")
                            self.grid[x][y] = 1
                            n_valid_queens += 1

                            # Add queen to color zone
                            queen_color_zone = self.get_color_zone(x, y)
                            self.color_zone_queens[queen_color_zone] = (x, y)
                            self.logger.info(
                                f"Added queen to color zone {queen_color_zone}: {self.color_zone_queens[queen_color_zone]}"
                            )

                            # Resize queen image to fit grid cell (100x100)
                            scaled_queen = pygame.transform.scale(
                                self.queen_image, (100, 100)
                            )
                            cell_x = FRAME_PADDING + (x * GRID_SIZE)
                            cell_y = TITLE_HEIGHT + FRAME_PADDING + (y * GRID_SIZE)
                            screen.blit(scaled_queen, (cell_x, cell_y))
                        else:
                            self.logger.info("Queen placement is invalid")
                            for key, value in checks.items():
                                if not value:
                                    self.logger.info(
                                        f"There is another queen in the same {key}."
                                    )

                #  If it is a right click, add or remove a cross to the cell
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    x, y = pygame.mouse.get_pos()
                    x = (x - FRAME_PADDING) // GRID_SIZE
                    y = (y - (TITLE_HEIGHT + FRAME_PADDING)) // GRID_SIZE
                    cell_x = FRAME_PADDING + (x * GRID_SIZE)
                    cell_y = TITLE_HEIGHT + FRAME_PADDING + (y * GRID_SIZE)
                    if self.grid[x][y] == 0:
                        # Add a cross to the cell
                        pygame.draw.line(
                            screen,
                            (0, 0, 0),
                            (cell_x, cell_y),
                            (cell_x + GRID_SIZE, cell_y + GRID_SIZE),
                            5,
                        )
                        pygame.draw.line(
                            screen,
                            (0, 0, 0),
                            (cell_x + GRID_SIZE, cell_y),
                            (cell_x, cell_y + GRID_SIZE),
                            5,
                        )
                        self.grid[x][y] = -1

                    elif self.grid[x][y] == -1:
                        # Remove the cross from the cell
                        queen_color_zone = self.get_color_zone(x, y)
                        color = color_map.get(queen_color_zone)

                        pygame.draw.line(
                            screen,
                            color,
                            (cell_x, cell_y),
                            (cell_x + GRID_SIZE, cell_y + GRID_SIZE),
                            5,
                        )
                        pygame.draw.line(
                            screen,
                            color,
                            (cell_x + GRID_SIZE, cell_y),
                            (cell_x, cell_y + GRID_SIZE),
                            5,
                        )
                        self.grid[x][y] = 0

                if event.type == pygame.QUIT:
                    pygame.quit()

                # Check if the user has placed all queens
                if n_valid_queens == self.n:
                    self.logger.info("All queens are placed correctly!")
                    running = False
                    break

            # Update the display
            pygame.display.update()
            clock.tick(60)

        # Display the final time
        final_time_text = clock_font.render(
            f"Solved! Time taken: {minutes:02d}:{seconds:02d}", True, (0, 0, 0)
        )
        screen.blit(final_time_text, (FRAME_PADDING, WINDOW_HEIGHT - FRAME_PADDING))
        pygame.display.update()
        pygame.time.wait(3000)
        pygame.quit()
