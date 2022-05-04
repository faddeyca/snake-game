import pygame
from pathlib import Path

pygame.init()


class Sounds():
    eating_sound = pygame.mixer.Sound(Path("sounds/food.mp3"))
    hurt_sound = pygame.mixer.Sound(Path("sounds/hurt.mp3"))
    bonus_sound = pygame.mixer.Sound(Path("sounds/bonus.mp3"))
    death_sound = pygame.mixer.Sound(Path("sounds/death.mp3"))
    drink_sound = pygame.mixer.Sound(Path("sounds/drink.mp3"))
