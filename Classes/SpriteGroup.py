from Settings import pygame


class SpriteGroup(pygame.sprite.Group):
    def draw(self, surface, **kwargs):
        for sprite in self.sprites():
            sprite.draw(surface)
