"""
Main file to run the game
"""
import logging
import argparse
import json
from game import Queens


def main(game_config_path: str, logger: logging.Logger):
    queens = Queens(logger)
    # Read the game config
    with open(game_config_path, "r") as f:
        game_config = json.load(f)
    queens.initialize_game(game_config)
    queens.run()


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Starting the game")

    # Read arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--game", type=str, default="src/game_store/game_001.json")
    args = parser.parse_args()

    # Run the game
    main(args.game, logger)


