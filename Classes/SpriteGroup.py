from Settings import pygame


# Sprite Group implementing specific draw method for group
class SpriteGroup(pygame.sprite.Group):
    def draw(self, surface, **kwargs):
        for sprite in self.sprites():
            sprite.draw(surface)
