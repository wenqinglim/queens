"""
This module contains the main game logic for the game.

In a game of Queens, players place N Queens in an NxN grid, and each Queen must not be able to attack each other. 
Each Queen is also contained by a unique color zone, where each color zone only has one Queen. 
The color zones can take up any number of adjacent tiles.
The zones force the grid to only have a single possible solution.
"""
import pygame
import logging


class Queens:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.n = None
        self.grid = []
        self.queens = []
        self.color_zones = []
        self.color_zone_queens = {}
        self.queen_image = pygame.image.load("assets/images/queen_icon.jpg") # Default queen image


    def initialize_game(self, game_config: dict):
        """
        Initialize the game with the given game config

        Args:
            game_config (dict): The game config. Example: game_store/game_001.py
        """
        self.n = game_config["n"]

        # Initialize the grid
        self.grid = [[0 for _ in range(self.n)] for _ in range(self.n)]
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
        # Check if the queen is in the same row as another queen
        for i in range(self.n):
            if self.grid[x][i] == 1:
                checks["row"] = False

        # Check if the queen is in the same column as another queen
        for i in range(self.n):
            if self.grid[i][y] == 1:
                checks["column"] = False

        # Check if the queen is in the same color zone as another queen
        for color_zone in self.color_zones:
            if x in color_zone["x"] and y in color_zone["y"]:
                if color_zone["color"] in self.color_zone_queens:
                    checks["color_zone"] = False
                else:
                    self.color_zone_queens[color_zone["color"]] = (x, y)

        # Check if the queen is in the corner of another queen
        # Check each diagonal direction only if within grid bounds
        corners = []
        if x > 0 and y > 0:  # Top-left corner
            corners.append(self.grid[x-1][y-1])
        if x > 0 and y < self.n-1:  # Top-right corner
            corners.append(self.grid[x-1][y+1])
        if x < self.n-1 and y > 0:  # Bottom-left corner
            corners.append(self.grid[x+1][y-1])
        if x < self.n-1 and y < self.n-1:  # Bottom-right corner
            corners.append(self.grid[x+1][y+1])
        
        if 1 in corners:  # If any corner has a queen
            checks["corner"] = False

        return checks
                
    

    def run(self):
        # Display the grid
        pygame.init()
        screen = pygame.display.set_mode((self.n * 100, self.n * 100))
        pygame.display.set_caption("Queens")
        clock = pygame.time.Clock()

        n_valid_queens = 0

        # while True:
        # Display the grid
        for i in range(self.n):
            for j in range(self.n):
                pygame.draw.rect(screen, (0, 0, 0), (i * 100, j * 100, 100, 100))

        # self.logger.info(f"Grid: {self.grid}")
        color_map = {
            "red": (255, 200, 200),
            "blue": (200, 200, 255),
            "green": (200, 255, 200),
            "yellow": (255, 255, 200),
        }
        # Display color zones
        for color_zone in self.color_zones:
            color = color_zone["color"]
            for x in color_zone["x"]:
                for y in color_zone["y"]:
                    pygame.draw.rect(screen, color_map[color], (x * 100, y * 100, 100, 100))

        while True:

            # self.logger.info(f"Grid: {self.grid}")
            # Update the display when user places a queen
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    x //= 100
                    y //= 100

                    # Check if the user has clicked on a queen
                    if self.grid[x][y] == 1:
                        self.grid[x][y] = 0
                        n_valid_queens -= 1

                        for color_zone in self.color_zones:
                            if x in color_zone["x"] and y in color_zone["y"]:
                                del self.color_zone_queens[color_zone["color"]]

                        # Remove the queen image from the screen
                        screen.blit(pygame.Surface((100, 100)), (x * 100, y * 100))

                    else:
                        # Check if queen placement adheres to game rules
                        checks = self.is_queen_correct(x, y)
                        if all(checks.values()):
                            print("Queen placement is valid")
                            self.grid[x][y] = 1
                            n_valid_queens += 1
                            # Resize queen image to fit grid cell (100x100)
                            scaled_queen = pygame.transform.scale(self.queen_image, (100, 100))
                            screen.blit(scaled_queen, (x * 100, y * 100))
                        else:
                            print("Queen placement is invalid")
                            for key, value in checks.items():
                                if not value:
                                    print(f"There is another queen in the same {key}.")

                # Check if the user has placed all queens
                if n_valid_queens == self.n:
                    print("All queens are placed correctly!")
                    pygame.quit()

                if event.type == pygame.QUIT:
                    pygame.quit()

                # Update the display
                pygame.display.update()
                clock.tick(60)