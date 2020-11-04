from ..abstract_sprite import AbstractSprite
from ...resource_manager import ResourceManager

class HudElement(AbstractSprite):
    def __init__(self, level, sprite, coord):
        AbstractSprite.__init__(self)

        self._coord = coord

        self.image = ResourceManager.load_sprite(level, sprite)
        self.rect = self.image.get_rect()

        #self.set_static_position(self._coord) # TODO Esto es un bug y debería eliminarse.
        #                                      # wip: set_static_position

    # TODO CHECK THIS
    def update(self, elapsed_time):
        pass

    def set_collision(self, coll):
        pass

    def _increase_position(self, increment):
        pass

    def draw(self, screen):
        screen.blit(self.image, self._coord)
