import pygame
import pygame_menu
import sys
from pathlib import Path

from Classes.Levels import *
from Classes.Sounds import *
from Classes.Level_Info import Info
from Classes.Saver import load_save


def start():
    '''
    Loads music, initializes menu.
    '''
    pygame.mixer.music.load(
        Path("sounds/music.mp3"))
    pygame.mixer.music.play()
    screen = build_menu()
    levels = init_levels()
    menu = pygame_menu.Menu("Menu", 300, 200,
                            theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Play', lambda: start_game(levels))
    menu.add.button('Load', lambda: load_from_save(levels))
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.set_title("Snake")
    menu.mainloop(screen)


def init_levels():
    levels = []
    levels.append(init_level_1())
    levels.append(init_level_2())
    levels.append(init_level_3())
    return levels


def load_from_save(levels):
    clean()
    res = load_save()
    if res == -1:
        return
    Info.started_from_save = True
    start_game(levels)


def clean():
    Info.snake_blocks = []
    Info.walls = []


def start_game(levels):
    '''
    Starts levels by their order.
    Ends if all levels are won or all lives are spent
    '''
    if not Info.started_from_save:
        Info.score = 0
        Info.lives = 3
        Info.current_level = 0

    for level_index in range(len(levels)):
        if Info.started_from_save and level_index < Info.current_level - 1:
            continue
        res = levels[level_index].start()
        Info.started_from_save = False
        if not res:
            break

    show_result()
    build_menu()


def build_menu():
    '''
    Rebuilds pygame display for menu
    '''
    pygame.init()
    pygame.display.set_caption("Snake")
    return pygame.display.set_mode([500, 500])


def show_result():
    '''
    Shows score in the end
    '''
    screen = pygame.display.set_mode([500, 75])
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                return
        courier = pygame.font.SysFont('courier', 25)
        text_score = courier.render(f"Result: {Info.score}", 0, Color.white)
        text_continue = courier.render("Press any key to continue",
                                       0, Color.white)
        screen.blit(text_score, (10, 10))
        screen.blit(text_continue, (10, 40))
        pygame.display.flip()


if __name__ == "__main__":
    start()
    sys.exit()
