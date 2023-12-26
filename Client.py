import random
import sys
from Server import Client
import pygame
import threading
from popup import Popup

WIDTH, HEIGHT = 1100, 700
MAP_SIZE = 10
BLOCK_SIZE = int((WIDTH - 200) / 2 / MAP_SIZE)
FPS = 60

OFFSET_X = 50
OFFSET_Y = 50

OPPONENT_MAP_OFFSET_X = WIDTH - (BLOCK_SIZE + 1) * MAP_SIZE - 5

SELECTED_BLOCK_COLOR = (255, 70, 0)
BLOCK_COLOR = (200, 200, 200)

START_SHIPS = {1: 4, 2: 3, 3: 2, 4: 1}


class Block(pygame.sprite.Sprite):
    def __init__(self, pos, *groups, color=BLOCK_COLOR):
        super().__init__(*groups)
        self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)
        self.canShoot = True
        self.hasShip = False

    def updateColor(self, color):
        self.image.fill(color)

    @classmethod
    def isOnBoard(cls, pos):
        if 0 <= pos[0] < MAP_SIZE and 0 <= pos[1] < MAP_SIZE:
            return True
        return False

    @classmethod
    def checkNeighbours(cls, board, pos, dir=-1):
        """
        Check if any neighbour lock has a ship.

        :param board: Game Board
        :param pos: Block position (row, col)
        :return: True if ship can be placed, False if not
        """
        if dir == 0:  # Only blocks on the right
            for i in range(-1, 2):
                if Block.isOnBoard((pos[0] + i, pos[1] + 1)):
                    if board[pos[0] + i][pos[1] + 1].hasShip:
                        return False

        elif dir == 1:  # Only blocks on the bottom
            for i in range(-1, 2):
                if Block.isOnBoard((pos[0] + 1, pos[1] + i)):
                    if board[pos[0] + 1][pos[1] + i].hasShip:
                        return False

        else:  # Every neighbour block
            for row in range(-1, 2):
                for col in range(-1, 2):
                    if Block.isOnBoard((pos[0] + row, pos[1] + col)):
                        if board[pos[0] + row][pos[1] + col].hasShip:
                            return False

        return True


class Ship(pygame.sprite.Sprite):
    def __init__(self, size, startBlock, direction, *groups):
        """

        :param size: Ship Size
        :param startBlock: Ship Start Block
        :param direction: Ship Direction (0 - horizontal, 1 - vertical)
        :param groups: Pygame Group
        """
        super().__init__(*groups)
        self.size = size
        self.startBlock = startBlock
        self.direction = direction
        asset_name = "PatrolBoat1.png"

        if size == 2:
            asset_name = "Cruiser1.png"
        elif size == 3:
            asset_name = "BattleShip.png"
        elif size == 4:
            asset_name = "AircraftCarrier1.png"

        self.image = pygame.transform.scale(pygame.image.load(f'Assets/{asset_name}').convert_alpha(),
                                            (BLOCK_SIZE * size + (size - 1), BLOCK_SIZE))
        if direction == 1:  # vertical
            self.image = pygame.transform.rotate(self.image, 90)

        self.rect = self.image.get_rect(
            topleft=(startBlock[1] * (BLOCK_SIZE + 1) + OFFSET_X, startBlock[0] * (BLOCK_SIZE + 1) + OFFSET_Y))

    def __repr__(self):
        return f'Ship(size: {self.size}, StartBlock: {self.startBlock}, Direction: {self.direction})'


class Player:
    def __init__(self):
        self.shipsGroup = pygame.sprite.Group()
        self.ships = []
        self.name = "Player"

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
                            board[start_pos[0] + i if direction == 1 else start_pos[0]][start_pos[1] + i if direction == 0 else start_pos[1]].hasShip = True

                        ship_placed = True


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Battleships")
        self.mapSprites = pygame.sprite.Group()

        # Map[ROW][COL]
        self.map = self.generateMap(OFFSET_X)
        self.opponentMap = self.generateMap(offsetX=OPPONENT_MAP_OFFSET_X)

        self.clock = pygame.time.Clock()
        self.yourTurn = True
        self.selectedBlock = None

        self.opponentName = "Waiting for opponent to join..."

        # Text
        self.fontSize = 40
        self.font = pygame.font.Font(None, self.fontSize)

        # LAN
        self.lan = Client()

        # Player
        self.player = Player()
        self.player.randomShipPlacement(self.map)

        # self.player.ships = [Ship(4, (5, 5), 3, self.player.shipsGroup)]

        print(self.player.ships)

    def generateMap(self, offsetX=0.0) -> [[Block]]:
        lineSize = 1
        temp = [[None for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]

        for col in range(MAP_SIZE):
            for row in range(MAP_SIZE):
                temp[row][col] = Block((col * BLOCK_SIZE + offsetX + lineSize * col,
                                        row * BLOCK_SIZE + OFFSET_Y + lineSize * row),
                                       self.mapSprites)

        return temp

    def receiveOpponentName(self):
        self.opponentName = self.lan.waitForData()

    def draw(self):
        self.screen.fill((60, 60, 60))

        border_line_wdith = 5

        # Border around maps
        pygame.draw.rect(self.screen, (0, 0, 0),
                         pygame.Rect((self.map[0][0].rect.left - border_line_wdith,
                                      self.map[0][0].rect.top - border_line_wdith),
                                     ((BLOCK_SIZE + 1) * MAP_SIZE + 2 * border_line_wdith,
                                      (BLOCK_SIZE + 1) * MAP_SIZE + 2 * border_line_wdith)))

        pygame.draw.rect(self.screen, (0, 0, 0),
                         pygame.Rect((self.opponentMap[0][0].rect.left - border_line_wdith,
                                      self.opponentMap[0][0].rect.top - border_line_wdith),
                                     ((BLOCK_SIZE + 1) * MAP_SIZE + 2 * border_line_wdith,
                                      (BLOCK_SIZE + 1) * MAP_SIZE + 2 * border_line_wdith)))

        self.mapSprites.draw(self.screen)
        self.player.shipsGroup.draw(self.screen)

        labels = "ABCDEFGHIJKLMNOPRSTWXYZ"[:MAP_SIZE]
        # Board Labels
        for i in range(1, MAP_SIZE + 1):
            # Board
            self.screen.blit(self.font.render(f'{i}', True, (255, 255, 255)),
                             (10, 50 + int((i - 0.5) * (BLOCK_SIZE + 1)) - self.font.size(str(i))[1] / 2))

            self.screen.blit(self.font.render(f'{labels[i - 1]}', True, (255, 255, 255)),
                             (50 + (i - 0.5) * (BLOCK_SIZE + 1) - self.font.size(labels[i - 1])[0] / 2, 20))

            # Opponent Board
            self.screen.blit(self.font.render(f'{i}', True, (255, 255, 255)),
                             (OPPONENT_MAP_OFFSET_X - 40,
                              50 + int((i - 0.5) * (BLOCK_SIZE + 1)) - self.font.size("1")[1] / 2))

            self.screen.blit(self.font.render(f'{labels[i - 1]}', True, (255, 255, 255)),
                             (WIDTH - (BLOCK_SIZE + 1) * MAP_SIZE - 5 + (i - 0.5) * (BLOCK_SIZE + 1) -
                              self.font.size(labels[i - 1])[0] / 2, 20))

        # Text
        # Turns
        self.screen.blit(
            self.font.render(f'{"YOUR TURN" if self.yourTurn else "OPPONENT TURN"}', True, (255, 255, 255)),
            (10, HEIGHT - 80))

        # Player Name
        self.screen.blit(
            self.font.render(self.player.name, True, (255, 255, 255)),
            (self.map[int(MAP_SIZE / 2)][0].rect.x - self.font.size(self.player.name)[0] / 2, HEIGHT - 170))

        # Opponent Name
        self.screen.blit(
            self.font.render(self.opponentName, True, (255, 255, 255)),
            (self.opponentMap[int(MAP_SIZE / 2)][0].rect.x - self.font.size(self.opponentName)[0] / 2, HEIGHT - 170))

    def getNameAndIp(self, popup):
        self.player.name = popup.name.get()
        if popup.ip.get() != "":
            self.lan.updateIp(popup.ip.get())

        popup.root.destroy()

    def createPopup(self):
        popup = Popup()
        popup.updateButtonCommand(lambda: self.getNameAndIp(popup))
        popup.run()

    def mouseOnEnemyBoard(self, pos):
        return (self.opponentMap[0][0].rect.left < pos[0] < self.opponentMap[MAP_SIZE - 1][0].rect.right and
                self.opponentMap[0][0].rect.top < pos[1] < self.opponentMap[0][MAP_SIZE - 1].rect.bottom)

    def selectBlock(self, pos):
        map_x = (pos[0] - OPPONENT_MAP_OFFSET_X - 1) // (BLOCK_SIZE + 1)
        map_y = (pos[1] - OFFSET_Y - 1) // (BLOCK_SIZE + 1)

        if self.selectedBlock is not None:
            self.selectedBlock.updateColor(BLOCK_COLOR)

        if self.opponentMap[map_x][map_y].canShoot:
            self.selectedBlock = self.opponentMap[map_x][map_y]
            self.selectedBlock.updateColor(SELECTED_BLOCK_COLOR)


if __name__ == '__main__':
    game = Game()
    game.draw()
    pygame.display.update()
    # game.createPopup()

    # game.lan.connect_with_server()
    # game.lan.sendData(game.player.name)
    # threading.Thread(target=game.receiveOpponentName).start()

    # GAME LOOP
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                pygame.quit()
                pygame.font.quit()
                sys.exit()

        if game.yourTurn:
            pos = pygame.mouse.get_pos()
            if game.mouseOnEnemyBoard(pos) and pygame.mouse.get_pressed()[0]:
                game.selectBlock(pos)

        game.draw()
        pygame.display.update()
        game.clock.tick(FPS)
