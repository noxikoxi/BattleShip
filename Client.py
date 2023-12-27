import sys

from Settings import *
from Server import Client
from Classes.Popup import Popup
from Classes.Button import Button
from Classes.Block import Block
from Classes.Player import Player


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Battleships")

        self.mapSprites = pygame.sprite.Group()
        self.buttonSprites = pygame.sprite.GroupSingle()

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

        # Buttons
        self.shootButton = Button((WIDTH/2 - 100, HEIGHT-120), "Shoot", self.font)

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

        # Button
        self.shootButton.draw(self.screen)

        labels = "ABCDEFGHIJKLMNOPRSTWXYZ"[:MAP_SIZE]
        # Board Labels
        for i in range(1, MAP_SIZE + 1):
            # Board
            self.screen.blit(self.font.render(f'{i}', True, TEXT_COLOR),
                             (10, 50 + int((i - 0.5) * (BLOCK_SIZE + 1)) - self.font.size(str(i))[1] / 2))

            self.screen.blit(self.font.render(f'{labels[i - 1]}', True, TEXT_COLOR),
                             (50 + (i - 0.5) * (BLOCK_SIZE + 1) - self.font.size(labels[i - 1])[0] / 2, 20))

            # Opponent Board
            self.screen.blit(self.font.render(f'{i}', True, TEXT_COLOR),
                             (OPPONENT_MAP_OFFSET_X - 40,
                              50 + int((i - 0.5) * (BLOCK_SIZE + 1)) - self.font.size("1")[1] / 2))

            self.screen.blit(self.font.render(f'{labels[i - 1]}', True, TEXT_COLOR),
                             (WIDTH - (BLOCK_SIZE + 1) * MAP_SIZE - 5 + (i - 0.5) * (BLOCK_SIZE + 1) -
                              self.font.size(labels[i - 1])[0] / 2, 20))

        # Text
        # Turns
        self.screen.blit(
            self.font.render(f'{"YOUR TURN" if self.yourTurn else "OPPONENT TURN"}', True, (255, 255, 255)),
            (10, HEIGHT - 80))

        # Player Name
        self.screen.blit(
            self.font.render(self.player.name, True, TEXT_COLOR),
            (self.map[0][int(MAP_SIZE / 2)].rect.x - self.font.size(self.player.name)[0] / 2, HEIGHT - 170))

        # Opponent Name
        self.screen.blit(
            self.font.render(self.opponentName, True, TEXT_COLOR),
            (self.opponentMap[0][int(MAP_SIZE / 2)].rect.x - self.font.size(self.opponentName)[0] / 2, HEIGHT - 170))

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
        return (self.opponentMap[0][0].rect.left < pos[0] < self.opponentMap[0][MAP_SIZE - 1].rect.right and
                self.opponentMap[0][0].rect.top < pos[1] < self.opponentMap[MAP_SIZE - 1][0].rect.bottom)

    def selectBlock(self, pos):
        map_x = (pos[0] - OPPONENT_MAP_OFFSET_X - 1) // (BLOCK_SIZE + 1)
        map_y = (pos[1] - OFFSET_Y - 1) // (BLOCK_SIZE + 1)

        if self.selectedBlock is not None:
            self.selectedBlock.updateColor(BLOCK_COLOR)

        if self.opponentMap[map_y][map_x].canShoot:
            self.selectedBlock = self.opponentMap[map_y][map_x]
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

            game.shootButton.hover(pos)

        game.draw()
        pygame.display.update()
        game.clock.tick(FPS)
