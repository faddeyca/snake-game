import pygame
import pygame_menu
from pathlib import Path

from Classes.Levels import *
from Classes.Sounds import *


def start():
    pygame.mixer.music.load(
        Path("sounds/music.mp3"))
    pygame.mixer.music.play()
    screen = build_menu()
    menu = pygame_menu.Menu("Menu", 300, 200,
                            theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Play', start_game)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(screen)


def start_game():
    res = start_level_1()

    if res:
        Sounds.bonus_sound.play()
        res = start_level_2()

    if res:
        Sounds.bonus_sound.play()
        res = start_level_3()

    build_menu()


def build_menu():
    pygame.init()
    pygame.display.set_caption("Snake")
    return pygame.display.set_mode([500, 500])


if __name__ == "__main__":
    start()
    sys.exit()
