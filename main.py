import pygame
import pygame_menu
from pathlib import Path

from Classes.Level import *


def start():
    screen, size = build_window()
    menu = pygame_menu.Menu("Menu", 300, 200,
                            theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Play', lambda: start_game(screen, size))
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(screen)


def start_game(screen, size):
    lvl = Level(screen, size)
    lvl.start()


def build_window():
    pygame.init()
    pygame.mixer.music.load(
        Path("sounds/music.mp3"))
    pygame.mixer.music.play()
    size = [Prop.block_size * Prop.blocks_amount +
            2 * Prop.block_size + Prop.delta * Prop.blocks_amount,
            Prop.block_size * Prop.blocks_amount +
            2 * Prop.block_size+Prop.delta * Prop.blocks_amount +
            Prop.up_length]
    pygame.display.set_caption("Snake")
    screen = pygame.display.set_mode(size)
    return screen, size


if __name__ == "__main__":
    start()
    sys.exit()
