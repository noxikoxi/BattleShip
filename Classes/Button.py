from Settings import pygame, BLOCK_COLOR


class Button:
    def __init__(self, position, text, font):
        self.border_width = 5
        self.width = 150
        self.height = 80
        self.pos = position

        self.image = pygame.Surface((self.width - 2 * self.border_width, self.height - 2 * self.border_width))
        self.image.fill(BLOCK_COLOR)
        self.rect = self.image.get_rect(topleft=(position[0] + self.border_width, position[1] + self.border_width))

        self.font = font
        self.text = text
        self.fontColor = (45, 45, 45)

    def draw(self, surface):
        # border
        pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(self.pos, (self.width, self.height)))

        # Inside
        surface.blit(self.image, self.rect)

        # Text
        surface.blit(self.font.render(self.text, True, self.fontColor),
                     (self.pos[0] + self.width/2 - self.font.size(self.text)[0] / 2,
                      self.pos[1] + self.height/2 - self.font.size(self.text)[1] / 2))

    def hover(self, mousePos):
        if self.rect.collidepoint(mousePos):
            self.fontColor = BLOCK_COLOR
            self.image.fill((45, 45, 45))
        else:
            self.fontColor = (45, 45, 45)
            self.image.fill(BLOCK_COLOR)
