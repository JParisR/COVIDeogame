from game import ResourceManager
from .abstract_screen import AbstractScreen
from game.gui import PlayButton, ExitButton, TextGUI

class EndScreen(AbstractScreen):
    def __init__(self, menu):
        AbstractScreen.__init__(self, menu, "backgrounds/main_menu.jpg")

        self._gui_elements.append(ExitButton(self, (400, 270)))

        white = (255, 255, 255)
        font_64 = ResourceManager.load_font_asset("8bit.ttf", 64)
        font_32 = ResourceManager.load_font_asset("8bit.ttf", 32)

        title = TextGUI(self, font_64, white, "Has perdido", (400, 120))
        exit = TextGUI(self, font_32, white, "Salir", (400, 270))

        self._gui_elements.append(title)
        self._gui_elements.append(exit)
