import pygame
import pygame_menu
from pathlib import Path

from Classes.Levels import *
from Classes.Sounds import *
from Classes.Level_Info import Info


def start():
    '''
    Loads music, initializes menu.
    '''
    pygame.mixer.music.load(
        Path("sounds/music.mp3"))
    pygame.mixer.music.play()
    screen = build_menu()
    menu = pygame_menu.Menu("Menu", 300, 200,
                            theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Play', start_game)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.set_title("Snake")
    menu.mainloop(screen)


def start_game():
    '''
    Starts levels by their order. Ends if all levels are won or all lives are spent
    '''
    Info.score = 0
    Info.lives = 3
    res = start_level_1()

    if res:
        Sounds.bonus_sound.play()
        res = start_level_2()

    if res:
        Sounds.bonus_sound.play()
        res = start_level_3()

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
