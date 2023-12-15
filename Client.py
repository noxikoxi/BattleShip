import sys

import pygame

WIDTH, HEIGHT = 1100, 700
MAP_SIZE = 10
BLOCK_SIZE = int((WIDTH-200) / 2 / MAP_SIZE)
FPS = 60


class Block(pygame.sprite.Sprite):
    def __init__(self, pos, groups, color=(200, 200, 200)):
        super().__init__(groups)
        self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Battleships")
        self.mapSprites = pygame.sprite.Group()
        self.map = self.generateMap(offsetX=50)
        map_width = (BLOCK_SIZE+1) * MAP_SIZE
        self.opponentMap = self.generateMap(offsetX=WIDTH - map_width-5)
        self.clock = pygame.time.Clock()

        # Text
        self.font = pygame.font.Font(None, 40)

    def generateMap(self, offsetX=0.0, offsetY=50):
        lineSize = 1
        temp = [[None for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]

        for col in range(MAP_SIZE):
            for row in range(MAP_SIZE):
                temp[row][col] = Block((row * BLOCK_SIZE + offsetX + lineSize * row,
                                        col * BLOCK_SIZE + offsetY + lineSize * col),
                                       self.mapSprites)

        return temp

    def draw(self):
        self.screen.fill((60, 60, 60))

        border_line_wdith = 5

        # Border around maps
        pygame.draw.rect(self.screen, (0, 0, 0),
                         pygame.Rect((self.map[0][0].rect.left - border_line_wdith,
                                      self.map[0][0].rect.top - border_line_wdith),
                                     ((BLOCK_SIZE+1) * MAP_SIZE + 2 * border_line_wdith,
                                      (BLOCK_SIZE+1) * MAP_SIZE + 2 * border_line_wdith)))

        pygame.draw.rect(self.screen, (0, 0, 0),
                         pygame.Rect((self.opponentMap[0][0].rect.left - border_line_wdith,
                                      self.opponentMap[0][0].rect.top - border_line_wdith),
                                     ((BLOCK_SIZE + 1) * MAP_SIZE + 2 * border_line_wdith,
                                      (BLOCK_SIZE + 1) * MAP_SIZE + 2 * border_line_wdith)))

        self.mapSprites.draw(self.screen)

        labels = "ABCDEFGHIJKLMNOPRSTWXYZ"[:MAP_SIZE]
        # Text
        for i in range(1, MAP_SIZE+1):
            # Board
            self.screen.blit(self.font.render(f'{i}', True, (255, 255, 255)),
                             (10, 35 + int((i-0.5) * (BLOCK_SIZE+1))))

            self.screen.blit(self.font.render(f'{labels[i-1]}', True, (255, 255, 255)),
                             (65 + (i-1) * (BLOCK_SIZE+1), 20))

            # Opponent Board
            self.screen.blit(self.font.render(f'{i}', True, (255, 255, 255)),
                             (WIDTH - (BLOCK_SIZE+1) * MAP_SIZE - 5 - 40, 35 + int((i - 0.5) * (BLOCK_SIZE + 1))))

            self.screen.blit(self.font.render(f'{labels[i - 1]}', True, (255, 255, 255)),
                             (WIDTH - (BLOCK_SIZE+1) * MAP_SIZE + 10 + (i - 1) * (BLOCK_SIZE + 1), 20))




game = Game()
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
