import random
from Settings import pygame, START_SHIPS, MAP_SIZE
from Classes.Block import Block
from Classes.Ship import Ship


class Player:
    def __init__(self):
        self.shipsGroup = pygame.sprite.Group()
        self.ships = []
        self.name = "Player"
        self.shipsDestroyed = 0

    def randomShipPlacement(self, board):
        # Ship placements starts from the biggest ship
        for ship_size in list(START_SHIPS.keys())[::-1]:
            for _ in range(START_SHIPS[ship_size]):
                ship_placed = False

                while not ship_placed:
                    board_row = random.randint(0, MAP_SIZE - 1)
                    board_col = random.randint(0, MAP_SIZE - 1)

                    # Random Start Block
                    while not Block.checkNeighbours(board, (board_row, board_col)):
                        board_row = random.randint(0, MAP_SIZE - 1)
                        board_col = random.randint(0, MAP_SIZE - 1)

                    dirs = [0, 1]
                    direction = random.choice(dirs)

                    start_pos = (board_row, board_col)

                    if ship_size > 1:
                        # Check every direction
                        while len(dirs) != 0:
                            direction = random.choice(dirs)
                            # Check if Ship can fit on the board in specific direction
                            if direction == 0:  # Horizontal
                                if board_col + ship_size > MAP_SIZE:
                                    dirs.remove(direction)
                                    continue
                            elif direction == 1:  # Vertical
                                if board_row + ship_size > MAP_SIZE:
                                    dirs.remove(direction)
                                    continue

                            board_row, board_col = start_pos
                            i = 1

                            while i != ship_size:
                                if direction == 0:  # check next columns
                                    board_col += 1
                                else:  # check next rows
                                    board_row += 1
                                if not Block.checkNeighbours(board, (board_row, board_col), direction):
                                    dirs.remove(direction)
                                    break
                                i += 1

                            if i == ship_size:  # There is no need to check other direction
                                break

                    if len(dirs) != 0:
                        self.ships.append(Ship(ship_size, start_pos, direction, self.shipsGroup))
                        for i in range(ship_size):
                            board[start_pos[0] + i if direction == 1 else start_pos[0]][
                                start_pos[1] + i if direction == 0 else start_pos[1]].ship = self.ships[-1]

                        ship_placed = True
