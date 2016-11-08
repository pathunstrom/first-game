#!/usr/bin/env python
import pygame
import random
import sys
from pygame.locals import KEYDOWN, KEYUP, QUIT
from pygame.locals import K_ESCAPE, K_RETURN
from pygame.locals import K_DOWN,K_LEFT, K_RIGHT, K_UP

import config

# set up pygame, the window, and the mouse cursor
KEEP_RUNNING = True
STOP_RUNNING = False
top_score = 0



def new_attack(new_dir, new_type, spawn_location, container):
    attack_definition = config.attacks[new_type]
    new_attack = {
        'rect': pygame.Rect(spawn_location, (attack_definition["size"], attack_definition["size"])),
        'direction': new_dir, 'life': attack_definition["life"], 'speed': attack_definition["velocity"],
    }
    container.append(new_attack)


def new_enemy(style, player, container):
    spawn = random.randint(1, config.game["spawnrate"])
    spawn_rate = {
        "z": zomSpawn,
        "s": skelSpawn
    }
    if not spawn > spawn_rate[style]:
        return
    coin = random.randint(0, 10)
    enemy = config.enemies[style].copy()
    sight = {
        "z": zomSight,
        "s": skelSight
    }
    enemy["sight"] = sight[style]
    enemy["awake"] = coin <= config.game["awareness"]
    enemy["rect"] = pygame.Rect(0, 0, enemy["size"], enemy["size"])
    enemy["rect"].topleft = (random.randint(1, config.game["width"] - enemy["size"]),
                                 random.randint(1, config.game["height"] - enemy["size"]))
    playerSafeZone.center = player["rect"].center
    if not enemy['rect'].colliderect(playerSafeZone):
        container.append(enemy)


def text_draw(text, font, surface, x, y, color):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def game_over(score):
    global top_score
    pygame.draw.rect(windowSurface, config.colors["background"],
                     pygame.Rect(100, 50, 400, 500))
    text_draw('GAME OVER', titlefont, windowSurface, 195, 60, config.colors["title"])
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


def game():
    running = True
    player = {
        "rect": pygame.Rect(0, 0, config.player["size"], config.player["size"]),
        "move": {
            "left": False,
            "right": False,
            "up": False,
            "down": False,
            "last": 0
        },
        "score": 0,
        "life": 10
    }
    player["rect"].center = ((config.game["width"] / 2), (config.game["height"] / 2))
    attacks = []
    enemies = []
    spawn_speed = 0

    # main loop
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                return STOP_RUNNING

            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    player["move"]["right"] = False
                    player["move"]["left"] = True
                if event.key == K_RIGHT:
                    player["move"]["left"] = False
                    player["move"]["right"] = True
                if event.key == K_UP:
                    player["move"]["down"] = False
                    player["move"]["up"] = True
                if event.key == K_DOWN:
                    player["move"]["up"] = False
                    player["move"]["down"] = True

                # Z attack creation
                if event.key == ord('z'):
                    z_noise.center = player["rect"].center
                    for e in enemies:
                        if not e['awake']:
                            if z_noise.colliderect(e['rect']):
                                e['awake'] = True
                    if player["move"]["up"]:
                        if player["move"]["left"]:
                            new_attack(4, 'z', player["rect"].topleft, attacks)
                            new_attack(7, 'z', player["rect"].topleft, attacks)
                            new_attack(8, 'z', player["rect"].topleft, attacks)
                        elif player["move"]["right"]:
                            new_attack(8, 'z', player["rect"].topright, attacks)
                            new_attack(9, 'z', player["rect"].topright, attacks)
                            new_attack(6, 'z', player["rect"].topright, attacks)
                        else:
                            new_attack(7, 'z', player["rect"].midtop, attacks)
                            new_attack(8, 'z', player["rect"].midtop, attacks)
                            new_attack(9, 'z', player["rect"].midtop, attacks)
                    elif player["move"]["down"]:
                        if player["move"]["left"]:
                            new_attack(4, 'z', player["rect"].bottomleft, attacks)
                            new_attack(1, 'z', player["rect"].bottomleft, attacks)
                            new_attack(2, 'z', player["rect"].bottomleft, attacks)
                        elif player["move"]["right"]:
                            new_attack(6, 'z', player["rect"].bottomright, attacks)
                            new_attack(3, 'z', player["rect"].bottomright, attacks)
                            new_attack(2, 'z', player["rect"].bottomright, attacks)
                        else:
                            new_attack(3, 'z', player["rect"].midbottom, attacks)
                            new_attack(2, 'z', player["rect"].midbottom, attacks)
                            new_attack(1, 'z', player["rect"].midbottom, attacks)
                    elif player["move"]["left"]:
                        new_attack(7, 'z', player["rect"].midleft, attacks)
                        new_attack(4, 'z', player["rect"].midleft, attacks)
                        new_attack(1, 'z', player["rect"].midleft, attacks)
                    elif player["move"]["right"]:
                        new_attack(9, 'z', player["rect"].midright, attacks)
                        new_attack(6, 'z', player["rect"].midright, attacks)
                        new_attack(3, 'z', player["rect"].midright, attacks)
                    else:
                        if last_move == 2:
                            new_attack(3, 'z', player["rect"].midbottom, attacks)
                            new_attack(2, 'z', player["rect"].midbottom, attacks)
                            new_attack(1, 'z', player["rect"].midbottom, attacks)
                        elif last_move == 4:
                            new_attack(7, 'z', player["rect"].midleft, attacks)
                            new_attack(4, 'z', player["rect"].midleft, attacks)
                            new_attack(1, 'z', player["rect"].midleft, attacks)
                        elif last_move == 6:
                            new_attack(9, 'z', player["rect"].midright, attacks)
                            new_attack(6, 'z', player["rect"].midright, attacks)
                            new_attack(3, 'z', player["rect"].midright, attacks)
                        elif last_move == 8:
                            new_attack(7, 'z', player["rect"].midtop, attacks)
                            new_attack(8, 'z', player["rect"].midtop, attacks)
                            new_attack(9, 'z', player["rect"].midtop, attacks)

                # X Attack Creation
                if event.key == ord('x'):
                    x_noise.center = player["rect"].center
                    for e in enemies:
                        if e['awake'] == False:
                            if x_noise.colliderect(e['rect']):
                                e['awake'] = True
                    if player["move"]["up"]:
                        if player["move"]["left"]:
                            new_attack(7, 'x', player["rect"].topleft, attacks)
                        elif player["move"]["right"]:
                            new_attack(9, 'x', player["rect"].topright, attacks)
                        else:
                            new_attack(8, 'x', player["rect"].midtop, attacks)
                    elif player["move"]["down"]:
                        if player["move"]["left"]:
                            new_attack(1, 'x', player["rect"].bottomleft, attacks)
                        elif player["move"]["right"]:
                            new_attack(3, 'x', player["rect"].bottomright, attacks)
                        else:
                            new_attack(2, 'x', player["rect"].midbottom, attacks)
                    elif player["move"]["left"]:
                        new_attack(4, 'x', player["rect"].midleft, attacks)
                    elif player["move"]["right"]:
                        new_attack(6, 'x', player["rect"].midright, attacks)
                    else:
                        if last_move == 2:
                            new_attack(2, 'x', player["rect"].midbottom, attacks)
                        elif last_move == 4:
                            new_attack(4, 'x', player["rect"].midleft, attacks)
                        elif last_move == 6:
                            new_attack(6, 'x', player["rect"].midright, attacks)
                        elif last_move == 8:
                            new_attack(8, 'x', player["rect"].midtop, attacks)

            # Deactivate player movement and save last direction
            if event.type == KEYUP:
                if event.key == K_LEFT or event.key == ord('a'):
                    player["move"]["left"] = False
                    last_move = 4
                if event.key == K_RIGHT or event.key == ord('d'):
                    player["move"]["right"] = False
                    last_move = 6
                if event.key == K_UP or event.key == ord('w'):
                    player["move"]["up"] = False
                    last_move = 8
                if event.key == K_DOWN or event.key == ord('s'):
                    player["move"]["down"] = False
                    last_move = 2
                # Close game if escape key is pressed
                if event.key == K_ESCAPE:
                    return STOP_RUNNING

        # Move the player around.
        if player["move"]["left"] and player["rect"].left > 0:
            player["rect"].move_ip(-1 * config.player["velocity"], 0)
        if player["move"]["right"] and player["rect"].right < config.game["width"]:
            player["rect"].move_ip(config.player["velocity"], 0)
        if player["move"]["up"] and player["rect"].top > 0:
            player["rect"].move_ip(0, -1 * config.player["velocity"])
        if player["move"]["down"] and player["rect"].bottom < config.game["height"]:
            player["rect"].move_ip(0, config.player["velocity"])

        # Move Attacks
        for a in attacks:
            if a['direction'] == 9:
                a['rect'].move_ip(a['speed'], - a['speed'])
            elif a['direction'] == 8:
                a['rect'].move_ip(0, - a['speed'])
            elif a['direction'] == 7:
                a['rect'].move_ip(- a['speed'], - a['speed'])
            elif a['direction'] == 6:
                a['rect'].move_ip(a['speed'], 0)
            elif a['direction'] == 4:
                a['rect'].move_ip(- a['speed'], 0)
            elif a['direction'] == 3:
                a['rect'].move_ip(a['speed'], a['speed'])
            elif a['direction'] == 2:
                a['rect'].move_ip(0, a['speed'])
            elif a['direction'] == 1:
                a['rect'].move_ip(- a['speed'], a['speed'])

        # Move enemies
        for e in enemies:
            if e['awake'] == False:
                shuffle = random.randint(1, 10)
                if shuffle == 1 and e['rect'].left > 0 and e[
                    'rect'].bottom < config.game["height"]:
                    e['rect'].move_ip(-1, 1)
                elif shuffle == 2 and e['rect'].bottom < config.game["height"]:
                    e['rect'].move_ip(0, 1)
                elif shuffle == 3 and e['rect'].right < config.game["width"] and e[
                    'rect'].bottom < config.game["height"]:
                    e['rect'].move_ip(1, 1)
                elif shuffle == 4 and e['rect'].left > 0:
                    e['rect'].move_ip(-1, 0)
                elif shuffle == 6 and e['rect'].right < config.game["width"]:
                    e['rect'].move_ip(1, 0)
                elif shuffle == 7 and e['rect'].left > 0 and e['rect'].top > 0:
                    e['rect'].move_ip(-1, -1)
                elif shuffle == 8 and e['rect'].top > 0:
                    e['rect'].move_ip(0, -1)
                elif shuffle == 9 and e['rect'].right < config.game["width"] and e[
                    'rect'].top > 0:
                    e['rect'].move_ip(1, 1)
            elif e['awake'] == True:
                if player["rect"].centerx > e['rect'].centerx:
                    if player["rect"].centery > e['rect'].centery:
                        e['rect'].move_ip(e['speed'], e['speed'])
                    elif player["rect"].centery < e['rect'].centery:
                        e['rect'].move_ip(e['speed'], - e['speed'])
                    else:
                        e['rect'].move_ip(e['speed'], 0)
                elif player["rect"].centerx < e['rect'].centerx:
                    if player["rect"].centery > e['rect'].centery:
                        e['rect'].move_ip(- e['speed'], e['speed'])
                    elif player["rect"].centery < e['rect'].centery:
                        e['rect'].move_ip(- e['speed'], - e['speed'])
                    else:
                        e['rect'].move_ip(- e['speed'], 0)
                elif player["rect"].centery > e['rect'].centery:
                    e['rect'].move_ip(0, e['speed'])
                elif player["rect"].centery < e['rect'].centery:
                    e['rect'].move_ip(0, - e['speed'])

        # Collision checks
        # Attacks against Enemies
        for a in attacks[:]:
            for e in enemies[:]:
                if a['rect'].colliderect(e['rect']) == True:
                    player["score"] += e['score']
                    enemies.remove(e)
                    attacks.remove(a)
                    break
        # Player Against Enemies
        for e in enemies[:]:
            if player["rect"].colliderect(e['rect']) == True:
                player["life"] -= 1
                enemies.remove(e)
        # Wake zones
        for e in enemies:
            if e['awake'] == False:
                e['sight'].center = e['rect'].center
            if e['sight'].colliderect(player["rect"]) == True:
                e['awake'] = True
            for e2 in enemies:
                if e2['awake'] == True:
                    e['sight'].center = e['rect'].center
                    if e['sight'].colliderect(e2['rect']):
                        e['awake'] = True

        # Spawn
        # Enemies
        new_enemy("s", player, enemies)
        new_enemy("z", player, enemies)

        # Draw frame
        windowSurface.fill(config.colors["background"])
        for a in attacks:
            pygame.draw.rect(windowSurface, config.colors["attack"], a['rect'])
        pygame.draw.rect(windowSurface, config.colors["player"], player["rect"])
        for e in enemies:
            pygame.draw.rect(windowSurface, e['color'], e['rect'])
        # Score area
        pygame.draw.rect(windowSurface, config.colors["background"], SCOREBOARD)
        # Draw the score and top score.
        text_draw('Score: %s' % player["score"], font, windowSurface, 20, 620, config.colors["text"])
        text_draw('Top Score: %s' % top_score, font, windowSurface, 20, 660, config.colors["text"])
        if player["life"] >= 1:
            pygame.draw.rect(windowSurface, config.colors["player"],
                             pygame.Rect(550, 620, 30, 30))
        else:
            pygame.draw.rect(windowSurface, config.colors["player"],
                             pygame.Rect(550, 620, 30, 30), 2)
        if player["life"] >= 2:
            pygame.draw.rect(windowSurface, config.colors["player"],
                             pygame.Rect(510, 620, 30, 30))
        else:
            pygame.draw.rect(windowSurface, config.colors["player"],
                             pygame.Rect(510, 620, 30, 30), 2)
        if player["life"] >= 3:
            pygame.draw.rect(windowSurface, config.colors["player"],
                             pygame.Rect(470, 620, 30, 30))
        else:
            pygame.draw.rect(windowSurface, config.colors["player"],
                             pygame.Rect(470, 620, 30, 30), 2)
        if player["life"] >= 4:
            pygame.draw.rect(windowSurface, config.colors["player"],
                             pygame.Rect(430, 620, 30, 30))
        else:
            pygame.draw.rect(windowSurface, config.colors["player"],
                             pygame.Rect(430, 620, 30, 30), 2)
        if player["life"] >= 5:
            pygame.draw.rect(windowSurface, config.colors["player"],
                             pygame.Rect(390, 620, 30, 30))
        else:
            pygame.draw.rect(windowSurface, config.colors["player"],
                             pygame.Rect(390, 620, 30, 30), 2)
        if player["life"] >= 6:
            pygame.draw.rect(windowSurface, config.colors["player"],
                             pygame.Rect(350, 620, 30, 30))
        else:
            pygame.draw.rect(windowSurface, config.colors["player"],
                             pygame.Rect(350, 620, 30, 30), 2)
        if player["life"] >= 7:
            pygame.draw.rect(windowSurface, config.colors["player"],
                             pygame.Rect(310, 620, 30, 30))
        else:
            pygame.draw.rect(windowSurface, config.colors["player"],
                             pygame.Rect(310, 620, 30, 30), 2)
        if player["life"] >= 8:
            pygame.draw.rect(windowSurface, config.colors["player"],
                             pygame.Rect(270, 620, 30, 30))
        else:
            pygame.draw.rect(windowSurface, config.colors["player"],
                             pygame.Rect(270, 620, 30, 30), 2)
        if player["life"] >= 9:
            pygame.draw.rect(windowSurface, config.colors["player"],
                             pygame.Rect(230, 620, 30, 30))
        else:
            pygame.draw.rect(windowSurface, config.colors["player"],
                             pygame.Rect(230, 620, 30, 30), 2)
        if player["life"] >= 10:
            pygame.draw.rect(windowSurface, config.colors["player"],
                             pygame.Rect(190, 620, 30, 30))
        else:
            pygame.draw.rect(windowSurface, config.colors["player"],
                             pygame.Rect(190, 620, 30, 30), 2)

        # Age and remove attacks
        for a in attacks[:]:
            if (a['life'] < 0
                or a['rect'].bottom < 0
                or a['rect'].top > config.game["height"]
                or a['rect'].left > config.game["width"]
                or a['rect'].right < 0):
                attacks.remove(a)
            a['life'] -= 1

        # Break loop if player is dead.
        if player["life"] <= 0:
            return game_over(player["score"])

        spawn_speed += 1
        if spawn_speed == config.game["spawn_increase_interval"]:
            global zomSpawn
            zomSpawn -= 1
            global skelSpawn
            skelSpawn -= 1

        # Update screen
        pygame.display.update()
        mainClock.tick(config.game["fps"])


def main_menu():
    running = True
    while running:
        pygame.draw.rect(windowSurface, config.colors["background"],
                         pygame.Rect(100, 50, 400, 500))
        text_draw(' %s ' % (config.game["title"]), titlefont, windowSurface, 135, 60, config.colors["title"])
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
                    running = game()


if __name__ == "__main__":
    pygame.init()
    mainClock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)
    titlefont = pygame.font.SysFont(None, 48)
    SCOREBOARD = pygame.Rect(*config.scoreboard)
    playerSafeZone = pygame.Rect(*config.safe_zone)
    z_noise = pygame.Rect(*config.z_noise_rect)
    x_noise = pygame.Rect(*config.x_noise_rect)
    zomSight = pygame.Rect(*config.zombie_sight)
    skelSight = pygame.Rect(*config.skeleton_sight)
    zomSpawn = 975
    skelSpawn = 995
    windowSurface = pygame.display.set_mode((config.game["width"],
                                             config.game["height"] + SCOREBOARD.height))
    pygame.display.set_caption(config.game["title"])
    pygame.mouse.set_visible(False)
    main_menu()
    pygame.quit()
    sys.exit()
