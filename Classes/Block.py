from Settings import pygame, BLOCK_SIZE, MAP_SIZE, BLOCK_COLOR, SHOT_CIRCLE_COLOR


# A class representing one block on a game board
class Block(pygame.sprite.Sprite):
    def __init__(self, position, *groups, color=BLOCK_COLOR):
        super().__init__(*groups)
        self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=position)

        # If Block can be shot (enemy board)
        self.canShoot = True
        # If Block has a ship
        self.ship = None
        # If Block was shot (player board)
        self.wasShot = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

        if self.wasShot:
            pygame.draw.circle(surface, SHOT_CIRCLE_COLOR, self.rect.center, BLOCK_SIZE / 3)

    def updateColor(self, color):
        self.image.fill(color)

    @classmethod
    def isOnBoard(cls, pos):
        if 0 <= pos[0] < MAP_SIZE and 0 <= pos[1] < MAP_SIZE:
            return True
        return False

    @classmethod
    def checkNeighbours(cls, board, position, direction=-1):
        """
        Check if any neighbour lock has a ship.

        :param direction: Check block only in specific direction (0 - Horizontal, 1 - Vertical)
        :param board: Game Board
        :param position: Block position (row, col)
        :return: True if ship can be placed, False if not
        """
        if direction == 0:  # Only blocks on the right
            for i in range(-1, 2):
                if Block.isOnBoard((position[0] + i, position[1] + 1)):
                    if board[position[0] + i][position[1] + 1].ship is not None:
                        return False
        elif direction == 1:  # Only blocks on the bottom
            for i in range(-1, 2):
                if Block.isOnBoard((position[0] + 1, position[1] + i)):
                    if board[position[0] + 1][position[1] + i].ship is not None:
                        return False
        else:  # Every neighbour block
            for row in range(-1, 2):
                for col in range(-1, 2):
                    if Block.isOnBoard((position[0] + row, position[1] + col)):
                        if board[position[0] + row][position[1] + col].ship is not None:
                            return False

        return True
