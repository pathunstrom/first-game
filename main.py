#!/usr/bin/env python
import pygame
import random
import sys
from pygame.locals import KEYDOWN, QUIT
from pygame.locals import K_ESCAPE, K_RETURN

import config
from controller import game_input, StopGameError
import create
import draw
from draw import text_draw
from updates import game_update


# set up pygame, the window, and the mouse cursor
KEEP_RUNNING = True
STOP_RUNNING = False
top_score = 0


def game_over(score):
    global top_score
    pygame.draw.rect(windowSurface, config.colors["background"],
                     pygame.Rect(100, 50, 400, 500))
    text_draw('GAME OVER', title_font, windowSurface, 195, 60, config.colors["title"])
    text_draw('Press Enter to continue', font, windowSurface, 220, 500,
              config.colors["text"])
    if score > top_score:
        top_score = score
        text_draw('New High Score!: %s' % top_score, font, windowSurface, 245,
                  470, config.colors["text"])
    else:
        text_draw('Top Score: %s' % top_score, font, windowSurface, 250, 470,
                  config.colors["text"])
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                return STOP_RUNNING
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return STOP_RUNNING
                if event.key == K_RETURN:
                    return KEEP_RUNNING
        pygame.display.update()


def _game():
    containers = {
        "enemies": [],
        "attacks": [],
        "player": {
            "rect": pygame.Rect(0, 0, config.player["size"], config.player["size"]),
            "move": {
                "left": False,
                "right": False,
                "up": False,
                "down": False,
                "last": 8,
                "direction": 8
            },
            "score": 0,
            "life": 10,
            "velocity": config.player["velocity"]
        }
    }
    containers["player"]["rect"].center = windowSurface.get_rect().center
    create.spawn = 0
    running = True
    while running:
        try:
            game_input(containers)
        except StopGameError:
            return STOP_RUNNING
        game_update(containers)
        draw.game(windowSurface, font, containers, top_score)
        if containers["player"]["life"] <= 0:
            return game_over(containers["player"]["score"])
        pygame.display.update()
        mainClock.tick(config.game["fps"])


def main_menu():
    running = True
    while running:
        pygame.draw.rect(windowSurface, config.colors["background"],
                         pygame.Rect(100, 50, 400, 500))
        text_draw(' %s ' % (config.game["title"]), title_font, windowSurface, 135, 60, config.colors["title"])
        text_draw('Press Enter to start', font, windowSurface, 220, 500, config.colors["text"])
        text_draw('Top Score: %s' % top_score, font, windowSurface, 250, 470, config.colors["text"])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                if event.key == K_RETURN:
                    running = _game()


if __name__ == "__main__":
    pygame.init()
    mainClock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)
    title_font = pygame.font.SysFont(None, 48)
    SCOREBOARD = pygame.Rect(*config.scoreboard)

    windowSurface = pygame.display.set_mode((config.game["width"],
                                             config.game["height"] + SCOREBOARD.height))
    pygame.display.set_caption(config.game["title"])
    pygame.mouse.set_visible(False)
    main_menu()
    pygame.quit()
    sys.exit()
