import pygame
from .abstract_scene import AbstractScene
from game.entities import Platform, Player
from .backgrounds import MainBackground
from game import Configuration
from .pause_menu import PauseMenu
from ..entities.hud import Hud, HudHeart
from ..entities.hud.hud_elements.hud_mask import HudMask
from ..player_repository import PlayerRepository
from ..util.log import Clog
from pygame.locals import *

class AbstractHorizontalScene(AbstractScene):
    MIN_X = 100
    MAX_X = 300

    def __init__(self, director):
        AbstractScene.__init__(self, director)
        self.log = Clog(__name__)
        self._scroll_x = 0

        self._hud = Hud()
        self._hud.create_hud_group(PlayerRepository.ATTR_HEALTH, HudHeart, (0,0), Hud.GROW_RIGHT, 100)
        self._hud.create_hud_group(PlayerRepository.ATTR_MASKS, HudMask, (80, 0), Hud.GROW_LEFT, 100)

    def update(self, elapsed_time):
        for enemy in iter(self._enemies):
            enemy.move_cpu()

        self._static_sprites.update(elapsed_time)
        self._dynamic_sprites.update(elapsed_time)
        # TODO revisar
        #self._overlay_sprites.update(elapsed_time)

        self._hud.update()


        if self._update_scroll():
            self._background.update(self._scroll_x)
            for sprite in iter(self._static_sprites):
                sprite.set_position((self._scroll_x, 0))
            for sprite in iter(self._dynamic_sprites):
                sprite.set_position((self._scroll_x, 0))

    def events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self._director.quit_game()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self._director.push_scene(PauseMenu(self._director))
        keys_pressed = pygame.key.get_pressed()
        self._player.move(keys_pressed, K_UP, K_DOWN, K_LEFT, K_RIGHT)

    def draw(self):
        self._background.draw(self._screen)
        self._static_sprites.draw(self._screen)
        self._dynamic_sprites.draw(self._screen)
        # TODO quitamos esto de aquí
        #self._overlay_sprites.draw(self._screen)
        # llamar al draw() del HUD (?)

        self._hud.draw(self._screen)

    def _update_scroll(self):
        player = self._player
        resolution = Configuration().get_resolution()

        if player.rect.right > AbstractHorizontalScene.MAX_X:
            displ = player.rect.right - AbstractHorizontalScene.MAX_X

            if self._scroll_x + resolution[0] >= self._background.rect.right:
                if player.rect.right >= resolution[0]:
                    player.set_global_position((self._background.rect.right - player.rect.width, player._position[1]))
                return False

            self._scroll_x = min(self._scroll_x + displ, self._background.rect.right - resolution[0])
            return True

        if player.rect.left < AbstractHorizontalScene.MIN_X:
            displ = AbstractHorizontalScene.MIN_X - player.rect.left
            self._scroll_x = max(self._scroll_x - displ, 0)

            if self._scroll_x == 0 and player.rect.left < 0:
                player.set_global_position((0, player._position[1]))
                return False

            return True

        return False
