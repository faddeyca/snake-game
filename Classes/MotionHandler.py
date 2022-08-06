from Classes.Level_Info import Info
from Classes.Saver import save

import pygame
import sys


def read_input():
    '''
    Reads keyboard input
    '''
    keys = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            keys.append(event.key)
            if len(keys) == 2:
                break

    move_stack = []
    for key in keys:
        if key == pygame.K_UP or key == pygame.K_w:
            move_stack.append(lambda: Move_up())
        elif key == pygame.K_DOWN or key == pygame.K_s:
            move_stack.append(lambda: Move_down())
        elif key == pygame.K_LEFT or key == pygame.K_a:
            move_stack.append(lambda: Move_left())
        elif key == pygame.K_RIGHT or key == pygame.K_d:
            move_stack.append(lambda: Move_right())
        elif key == pygame.K_b:
            Info.cheatsB = (Info.cheatsB + 1) % 2
        elif key == pygame.K_k:
            Info.cheatsK = (Info.cheatsK + 1) % 2
        elif key == pygame.K_m:
            Info.score += 100
        elif key == pygame.K_ESCAPE:
            if Info.pause:
                return 0
            Info.pause = 1
            Info.d_x = 0
            Info.d_y = 0
        elif key == pygame.K_p:
            if Info.pause:
                save()
    return move_stack


def Move_up():
    '''
    If possible, changes snake direction to up
    '''
    if Info.d_y != 0 or Info.pause:
        Info.d_x = -1
        Info.d_y = 0
        return 1
    return 0


def Move_down():
    '''
    If possible, changes snake direction to down
    '''
    if Info.d_y != 0 or Info.pause:
        Info.d_x = 1
        Info.d_y = 0
        return 1
    return 0


def Move_left():
    '''
    If possible, changes snake to left
    '''
    if Info.d_x != 0 or Info.pause:
        Info.d_x = 0
        Info.d_y = -1
        return 1
    return 0


def Move_right():
    '''
    If possible, changes snake to right
    '''
    if Info.d_x != 0 or Info.pause:
        Info.d_x = 0
        Info.d_y = 1
        return 1
    return 0
