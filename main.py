import pygame
import pygame_menu
from pathlib import Path

from Classes.Levels import *
from Classes.Sounds import *


def start():
    pygame.mixer.music.load(
        Path("sounds/music.mp3"))
    pygame.mixer.music.play()
    screen, size = build_screen()
    menu = pygame_menu.Menu("Menu", 300, 200,
                            theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Play', lambda: start_game(screen, size))
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(screen)


def start_game(screen, size):
    res = start_level_1(screen, size)

    if res:
        Sounds.bonus_sound.play()
        res = start_level_2(screen, size)

    if res:
        Sounds.bonus_sound.play()
        res = start_level_3(screen, size)


def build_screen():
    pygame.init()
    pygame.display.set_caption("Snake")
    size = [Prop.block_size * Prop.blocks_amount +
            2 * Prop.block_size + Prop.delta * Prop.blocks_amount,
            Prop.block_size * Prop.blocks_amount +
            2 * Prop.block_size+Prop.delta * Prop.blocks_amount +
            Prop.up_length]
    return pygame.display.set_mode(size), size


if __name__ == "__main__":
    start()
    sys.exit()
