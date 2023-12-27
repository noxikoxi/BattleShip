from Settings import BLOCK_SIZE, OFFSET_X, OFFSET_Y, pygame


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