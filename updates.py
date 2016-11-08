import random

import config
from create import new_enemy, update_spawners

VECTORS = [
    (0, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
    (-1, 0),
    (0, 0),
    (1, 0),
    (-1, -1),
    (0, -1),
    (1, -1)
]


def clamp_to_play_space(rect):
    rect.top = rect.top if rect.top > 0 else 0
    rect.bottom = rect.bottom if rect.bottom < config.game["height"] else config.game["height"]
    rect.left = rect.left if rect.left > 0 else 0
    rect.right = rect.right if rect.right < config.game["width"] else config.game["width"]


def move_object(direction, rect, velocity):
    vector = VECTORS[direction]
    rect.move_ip(vector[0] * velocity, vector[1] * velocity)


def calculate_direction(up, down, left, right):
    up *= 3
    down *= -3
    left *= -1
    right *= 1
    return 5 + up + down + left + right


def player_update(player):
    rect = player["rect"]
    move = player["move"]

    move["last"] = move["direction"] if move["direction"] != 5 else move["last"]
    print("Last valid move: {}".format(move["last"]))
    player["move"]["direction"] = calculate_direction(move["up"],
                                                      move["down"],
                                                      move["left"],
                                                      move["right"])

    move_object(move["direction"], rect, player["velocity"])

    clamp_to_play_space(rect)


def enemy_update(enemy, containers):
    player = containers["player"]
    enemies = containers["enemies"]
    attacks = containers["attacks"]

    if not enemy['awake']:
        shuffle = random.randint(1, 9)

        move_object(shuffle, enemy["rect"], 1)

        enemy["sight"].center = enemy["rect"].center
        if enemy["sight"].colliderect(player["rect"]):
            enemy["awake"] = True
        for other in enemies:
            if other["awake"] and enemy["rect"].colliderect(other["rect"]):
                enemy["awake"] = True
    elif enemy['awake']:
        up = enemy["rect"].top > player["rect"].centery
        down = enemy["rect"].bottom < player["rect"].centery
        left = enemy["rect"].left > player["rect"].centerx
        right = enemy["rect"].right < player["rect"].centerx
        move_object(calculate_direction(up, down, left, right),
                    enemy['rect'],
                    enemy['speed'])

    clamp_to_play_space(enemy["rect"])
    if player["rect"].colliderect(enemy['rect']):
        player["life"] -= 1
        enemy["dead"] = True
    for attack in attacks:
        if attack['rect'].colliderect(enemy['rect']):
            player["score"] += enemy['score']
            enemy["dead"] = True
            attack["dead"] = True


def attack_update(attack):
    move_object(attack["direction"], attack["rect"], attack["speed"])

    if (attack['life'] < 0
        or attack['rect'].bottom < 0
        or attack['rect'].top > config.game["height"]
        or attack['rect'].left > config.game["width"]
        or attack['rect'].right < 0):
        attack["dead"] = True
    attack['life'] -= 1


def game_update(containers):
    player = containers["player"]
    player_update(player)
    for attack in containers["attacks"]:
        attack_update(attack)
    for enemy in containers["enemies"]:
        enemy_update(enemy, containers)
    containers["attacks"] = list(filter(lambda x: not x["dead"], containers["attacks"]))
    containers["enemies"] = list(filter(lambda x: not x["dead"], containers["enemies"]))
    new_enemy("s", player, containers["enemies"])
    new_enemy("z", player, containers["enemies"])
    update_spawners()