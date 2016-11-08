import pygame.event
from pygame import KEYDOWN, KEYUP, QUIT
from pygame import K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_x, K_z
from create import new_attack

import config

z_noise = pygame.Rect(*config.z_noise_rect)
x_noise = pygame.Rect(*config.x_noise_rect)


def center(rect):
    return rect.center


def bottomleft(rect):
    return rect.bottomleft


def midbottom(rect):
    return rect.midbottom


def bottomright(rect):
    return rect.bottomright


def midleft(rect):
    return rect.midleft


def midright(rect):
    return rect.midright


def topleft(rect):
    return rect.topleft


def midtop(rect):
    return rect.midtop


def topright(rect):
    return rect.topright

origins = [
    center,
    bottomleft,
    midbottom,
    bottomright,
    midleft,
    center,
    midright,
    topleft,
    midtop,
    topright
]


def rotate(direction, clockwise=True):
    values = [8, 9, 6, 3, 2, 1, 4, 7, 8]
    if not clockwise:
        values = values[::-1]
    for i, value in enumerate(values):
        if value == direction:
            return values[i + 1]


class StopGameError(Exception):
    pass


def k_left(event, containers):
    player = containers["player"]
    player["move"]["left"] = event.type == KEYDOWN
    if event.type == KEYUP:
        player["move"]["last"] = 4


def k_right(event, containers):
    player = containers["player"]
    player["move"]["right"] = event.type == KEYDOWN
    if event.type == KEYUP:
        player["move"]["last"] = 6


def k_up(event, containers):
    player = containers["player"]
    player["move"]["up"] = event.type == KEYDOWN
    if event.type == KEYUP:
        player["move"]["last"] = 8


def k_down(event, containers):
    player = containers["player"]
    player["move"]["down"] = event.type == KEYDOWN
    if event.type == KEYUP:
        player["move"]["last"] = 2


def k_z_pressed(event, containers):
    player = containers["player"]
    enemies = containers["enemies"]
    attacks = containers["attacks"]
    z_noise.center = player["rect"].center
    for e in enemies:
        if not e['awake']:
            if z_noise.colliderect(e['rect']):
                e['awake'] = True
    direction = player["move"]["direction"]
    direction = direction if direction != 5 and direction != 0 else player["move"]["last"]
    origin = origins[direction](player["rect"])
    print(direction)
    new_attack(direction, 'z', origin, attacks)
    print(rotate(direction))
    new_attack(rotate(direction), 'z', origin, attacks)
    print(rotate(direction, False))
    new_attack(rotate(direction, False), 'z', origin, attacks)


def k_x_pressed(_, containers):
    player = containers["player"]
    enemies = containers["enemies"]
    attacks = containers["attacks"]

    x_noise.center = player["rect"].center
    for e in enemies:
        if e['awake']:
            if x_noise.colliderect(e['rect']):
                e['awake'] = True
    direction = player["move"]["direction"]
    direction = direction if direction != 5 and direction != 0 else player["move"]["last"]
    origin = origins[direction](player["rect"])
    new_attack(direction, 'x', origin, attacks)


def handle_keyup(event, containers):
    key_callbacks = {
        K_LEFT: k_left,
        K_RIGHT: k_right,
        K_UP: k_up,
        K_DOWN: k_down,
        K_ESCAPE: handle_quit
    }
    key_callbacks.get(event.key, blank_handle)(event, containers)


def handle_keydown(event, containers):
    key_callbacks = {
        K_UP: k_up,
        K_DOWN: k_down,
        K_RIGHT: k_right,
        K_LEFT: k_left,
        K_z: k_z_pressed,
        K_x: k_x_pressed
    }
    key_callbacks.get(event.key, blank_handle)(event, containers)


def blank_handle(*_):
    pass


def handle_quit(event, containers):
    _ = event
    _ = containers
    raise StopGameError


def game_input(containers):
    event_callbacks = {
        KEYDOWN: handle_keydown,
        KEYUP: handle_keyup,
        QUIT: handle_quit
    }

    for event in pygame.event.get():
        event_callbacks.get(event.type, blank_handle)(event, containers)