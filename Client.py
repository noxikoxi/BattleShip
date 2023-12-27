import sys
import threading

from Settings import *
from Server import Client
from Classes.Popup import Popup
from Classes.Button import Button
from Classes.Block import Block
from Classes.Player import Player
from Classes.SpriteGroup import SpriteGroup


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Battleships")

        self.mapSprites = SpriteGroup()
        self.buttonSprites = pygame.sprite.GroupSingle()
        self.shipBlocks = pygame.sprite.Group()

        # Map[ROW][COL]
        self.map = self.generateMap(OFFSET_X)
        self.opponentMap = self.generateMap(offsetX=OPPONENT_MAP_OFFSET_X)

        self.clock = pygame.time.Clock()
        self.yourTurn = False
        self.selectedBlock = None
        self.selectedBlockPosition = (None, None)
        self.gameOver = False
        self.gameOverStatus = None
        self.lastEnemyMove = None

        self.opponentName = "Waiting for opponent to join..."

        # Text
        self.fontSize = 40
        self.font = pygame.font.Font(None, self.fontSize)

        # LAN
        self.lan = Client()

        # Player
        self.player = Player()
        self.player.randomShipPlacement(self.map)

        # Buttons
        self.shootButton = Button((WIDTH / 2 - 40, HEIGHT - 120), "Shoot", self.font)

    def generateMap(self, offsetX=0.0) -> [[Block]]:
        lineSize = 1
        temp = [[] for _ in range(MAP_SIZE)]

        for col in range(MAP_SIZE):
            for row in range(MAP_SIZE):
                temp[row].append(Block((col * BLOCK_SIZE + offsetX + lineSize * col,
                                        row * BLOCK_SIZE + OFFSET_Y + lineSize * row),
                                       self.mapSprites))

        return temp

    def draw(self):
        self.screen.fill((60, 60, 60))

        border_line_width = 5

        # Border around maps
        pygame.draw.rect(self.screen, (0, 0, 0),
                         pygame.Rect((self.map[0][0].rect.left - border_line_width,
                                      self.map[0][0].rect.top - border_line_width),
                                     ((BLOCK_SIZE + 1) * MAP_SIZE + 2 * border_line_width,
                                      (BLOCK_SIZE + 1) * MAP_SIZE + 2 * border_line_width)))

        pygame.draw.rect(self.screen, (0, 0, 0),
                         pygame.Rect((self.opponentMap[0][0].rect.left - border_line_width,
                                      self.opponentMap[0][0].rect.top - border_line_width),
                                     ((BLOCK_SIZE + 1) * MAP_SIZE + 2 * border_line_width,
                                      (BLOCK_SIZE + 1) * MAP_SIZE + 2 * border_line_width)))

        self.mapSprites.draw(self.screen)
        self.player.shipsGroup.draw(self.screen)

        # Blocks representing damage to ships
        self.shipBlocks.draw(self.screen)

        # Button
        self.shootButton.draw(self.screen)

        # Board Labels
        for i in range(1, MAP_SIZE + 1):
            # Board
            self.screen.blit(self.font.render(f'{i}', True, TEXT_COLOR),
                             (10, 50 + int((i - 0.5) * (BLOCK_SIZE + 1)) - self.font.size(str(i))[1] / 2))

            self.screen.blit(self.font.render(f'{ALPHABET[i - 1]}', True, TEXT_COLOR),
                             (50 + (i - 0.5) * (BLOCK_SIZE + 1) - self.font.size(ALPHABET[i - 1])[0] / 2, 20))

            # Opponent Board
            self.screen.blit(self.font.render(f'{i}', True, TEXT_COLOR),
                             (OPPONENT_MAP_OFFSET_X - 40,
                              50 + int((i - 0.5) * (BLOCK_SIZE + 1)) - self.font.size("1")[1] / 2))

            self.screen.blit(self.font.render(f'{ALPHABET[i - 1]}', True, TEXT_COLOR),
                             (WIDTH - (BLOCK_SIZE + 1) * MAP_SIZE - 5 + (i - 0.5) * (BLOCK_SIZE + 1) -
                              self.font.size(ALPHABET[i - 1])[0] / 2, 20))

        # Text
        # Turns
        self.screen.blit(
            self.font.render(f'{"YOUR TURN" if self.yourTurn else "OPPONENT TURN"}', True, (255, 255, 255)),
            (self.map[0][int(MAP_SIZE / 2)].rect.x -
             self.font.size(f'{"YOUR TURN" if self.yourTurn else "OPPONENT TURN"}')[0] / 2, HEIGHT - 80))

        # Player Name
        self.screen.blit(
            self.font.render(self.player.name, True, TEXT_COLOR),
            (self.map[0][int(MAP_SIZE / 2)].rect.x - self.font.size(self.player.name)[0] / 2, HEIGHT - 170))

        # Opponent Name
        self.screen.blit(
            self.font.render(self.opponentName, True, TEXT_COLOR),
            (self.opponentMap[0][int(MAP_SIZE / 2)].rect.x - self.font.size(self.opponentName)[0] / 2, HEIGHT - 170))

        # Game over message
        if self.gameOver:
            self.screen.blit(
                self.font.render(f'YOU {self.gameOverStatus}', True, TEXT_COLOR),
                (self.opponentMap[0][int(MAP_SIZE / 2)].rect.x - self.font.size(f'YOU {self.gameOverStatus}')[0] / 2,
                 HEIGHT - 80))
        else:  # last enemy move message
            self.screen.blit(
                self.font.render(f'Opponent move: {self.lastEnemyMove}', True, TEXT_COLOR),
                (self.opponentMap[0][int(MAP_SIZE / 2)].rect.x - self.font.size(f'Opponent move: {self.lastEnemyMove}')[
                    0] / 2,
                 HEIGHT - 80))

    def mouseOnEnemyBoard(self, position):
        return (self.opponentMap[0][0].rect.left < position[0] < self.opponentMap[0][MAP_SIZE - 1].rect.right and
                self.opponentMap[0][0].rect.top < position[1] < self.opponentMap[MAP_SIZE - 1][0].rect.bottom)

    def selectBlock(self, position):
        board_x = (position[0] - OPPONENT_MAP_OFFSET_X - 1) // (BLOCK_SIZE + 1)
        board_y = (position[1] - OFFSET_Y - 1) // (BLOCK_SIZE + 1)

        if self.opponentMap[board_y][board_x].canShoot:
            if self.selectedBlock is not None:
                self.selectedBlock.updateColor(BLOCK_COLOR)

            self.selectedBlock = self.opponentMap[board_y][board_x]
            self.selectedBlockPosition = (board_y, board_x)
            self.selectedBlock.updateColor(SELECTED_BLOCK_COLOR)

    def getNameAndIp(self, popup):
        self.player.name = popup.name.get()
        if popup.ip.get() != "":
            self.lan.updateIp(popup.ip.get())

        popup.root.destroy()

    def createPopup(self):
        popup = Popup()
        popup.updateButtonCommand(lambda: self.getNameAndIp(popup))
        popup.run()

    def receiveOpponentName(self):
        self.opponentName = self.lan.waitForData()

    def handleShot(self, shoot):
        shoot = shoot.split(':')
        row = int(shoot[0])
        col = LETTER_TO_DECIMAL[shoot[1]]

        self.lastEnemyMove = f'{shoot[1]}{row + 1}'

        if self.map[row][col].ship is not None:
            ship = self.map[row][col].ship
            ship.shots += 1

            self.shipBlocks.add(Block(position=self.map[row][col].rect.topleft, color=(255, 0, 0, 100)))

            if ship.shots == ship.size:
                self.lan.sendData(f"SHIP_SUNK {ship.startBlock[0]},{ship.startBlock[1]}:{ship.direction}:{ship.size}")
            else:
                self.lan.sendData(f'SHIP {row}:{DECIMAL_TO_LETTER[col]}')
        else:
            self.map[row][col].wasShot = True
            self.lan.sendData(f'WATER {row}:{DECIMAL_TO_LETTER[col]}')

    def applyShotOnEnemyBoard(self, position, ship=False, sunk=False):
        position = position.split(':')

        if sunk:  # Different message
            row = int(position[0].split(",")[0][0])
            col = int(position[0].split(",")[1][0])
            direction = int(position[1])
            size = int(position[2])

            for _ in range(size):
                self.opponentMap[row][col].updateColor((0, 0, 0))
                if direction == 0:  # Horizontal
                    col += 1
                else:  # Vertical
                    row += 1

            self.player.shipsDestroyed += 1

            if self.player.shipsDestroyed == len(self.player.ships):
                self.lan.sendData(f'GAME_OVER')
                self.gameOver = True
                self.gameOverStatus = 'WON'
        else:
            row = int(position[0])
            col = LETTER_TO_DECIMAL[position[1]]

            if ship:
                self.opponentMap[row][col].updateColor((255, 0, 0))
            else:
                self.opponentMap[row][col].wasShot = True

    def handleLanGame(self):
        while not self.gameOver:
            message = self.lan.waitForData()

            if message == "TURN":
                self.yourTurn = True
            elif message.split(" ")[0] == "SHOOT":
                self.handleShot(message.split(" ")[1])
            elif message.split(" ")[0] == "SHIP":
                self.applyShotOnEnemyBoard(message.split(" ")[1], True)
            elif message.split(" ")[0] == 'SHIP_SUNK':
                print(message.split(" "))
                self.applyShotOnEnemyBoard(message.split(" ")[1], True, True)
            elif message.split(" ")[0] == "WATER":
                self.applyShotOnEnemyBoard(message.split(" ")[1], False)
            elif message.split(" ")[0] == "GAME_OVER":
                self.gameOver = True
                self.gameOverStatus = 'LOST'


if __name__ == '__main__':
    game = Game()
    game.draw()
    pygame.display.update()
    game.createPopup()

    game.lan.connect_with_server()
    game.lan.sendData(game.player.name)
    threading.Thread(daemon=True, target=game.receiveOpponentName).start()
    threading.Thread(daemon=True, target=game.handleLanGame).start()

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

            if game.selectedBlock is not None:
                game.shootButton.hover(pos)

                if game.shootButton.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
                    game.lan.sendData(
                        f'SHOOT {game.selectedBlockPosition[0]}:{DECIMAL_TO_LETTER[game.selectedBlockPosition[1]]}')
                    game.yourTurn = False
                    game.selectedBlock.updateColor(BLOCK_COLOR)
                    game.selectedBlock.canShoot = False
                    game.selectedBlock = None

        game.draw()
        pygame.display.update()
        game.clock.tick(FPS)
