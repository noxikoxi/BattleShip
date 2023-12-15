import sys
from Server import Client
import pygame
import threading
from popup import Popup

WIDTH, HEIGHT = 1100, 700
MAP_SIZE = 10
BLOCK_SIZE = int((WIDTH - 200) / 2 / MAP_SIZE)
FPS = 60


class Block(pygame.sprite.Sprite):
    def __init__(self, pos, groups, color=(200, 200, 200)):
        super().__init__(groups)
        self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)

    def updateColor(self, color):
        self.image.fill(color)


class Ship:
    def __init__(self, size, startBlock, direction):
        self.size = size
        self.startBlock = startBlock
        self.direction = direction


class Player:
    def __init__(self):
        self.ships = [Ship(4, (2, 2), (1, 0)),
                      Ship(3, (6, 6), (1, 0))]
        self.name = "Player"


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Battleships")
        self.mapSprites = pygame.sprite.Group()
        self.map = self.generateMap(offsetX=50)
        map_width = (BLOCK_SIZE + 1) * MAP_SIZE
        self.opponentMap = self.generateMap(offsetX=WIDTH - map_width - 5)
        self.clock = pygame.time.Clock()
        self.yourTurn = False

        self.opponentName = "Waiting for opponent to join..."

        # Text
        self.fontSize = 40
        self.font = pygame.font.Font(None, self.fontSize)

        # LAN
        self.lan = Client()

        # Player
        self.player = Player()
        for ship in self.player.ships:
            x, y = ship.startBlock[0], ship.startBlock[1]
            for i in range(ship.size):
                self.map[x][y].updateColor((45, 45, 120))
                x += ship.direction[0]
                y += ship.direction[1]

    def generateMap(self, offsetX=0.0, offsetY=50):
        lineSize = 1
        temp = [[None for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]

        for col in range(MAP_SIZE):
            for row in range(MAP_SIZE):
                temp[row][col] = Block((row * BLOCK_SIZE + offsetX + lineSize * row,
                                        col * BLOCK_SIZE + offsetY + lineSize * col),
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
                             (WIDTH - (BLOCK_SIZE + 1) * MAP_SIZE - 5 - 40,
                              50 + int((i - 0.5) * (BLOCK_SIZE + 1)) - self.font.size("1")[1]/2))

            self.screen.blit(self.font.render(f'{labels[i - 1]}', True, (255, 255, 255)),
                             (WIDTH - (BLOCK_SIZE + 1) * MAP_SIZE - 5 + (i - 0.5) * (BLOCK_SIZE + 1) - self.font.size(labels[i - 1])[0] / 2, 20))

        # Text
        # Turns
        self.screen.blit(
            self.font.render(f'{"YOUR TURN" if self.yourTurn else "OPPONENT TURN"}', True, (255, 255, 255)),
            (10, HEIGHT - 80))

        # Player Name
        self.screen.blit(
            self.font.render(self.player.name, True, (255, 255, 255)),
            (self.map[int(MAP_SIZE/2)][0].rect.x - self.font.size(self.player.name)[0] / 2, HEIGHT - 170))

        # Opponent Name
        self.screen.blit(
            self.font.render(self.opponentName, True, (255, 255, 255)),
            (self.opponentMap[int(MAP_SIZE / 2)][0].rect.x - self.font.size(self.opponentName)[0] / 2, HEIGHT - 170))

    def getNameAndIp(self, popup):
        self.player.name = popup.name.get()
        self.lan.updateIp(popup.ip.get())

        popup.root.destroy()

    def createPopup(self):
        popup = Popup()
        popup.updateButtonCommand(lambda: self.getNameAndIp(popup) )
        popup.run()


if __name__ == '__main__':
    game = Game()
    game.draw()
    pygame.display.update()
    game.createPopup()

    game.lan.connect_with_server()
    game.lan.sendData(game.player.name)
    threading.Thread(target=game.receiveOpponentName).start()

    # GAME LOOP
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                pygame.font.quit()
                sys.exit()

        game.draw()
        pygame.display.update()
        game.clock.tick(FPS)
