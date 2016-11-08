import random

from pygame import Rect

import config

zombie_spawn = 975
skeleton_spawn = 995
spawn_speed = 0
zombie_sight = Rect(*config.zombie_sight)
skeleton_sight = Rect(*config.skeleton_sight)
playerSafeZone = Rect(*config.safe_zone)

def update_spawners():
    global spawn_speed
    spawn_speed += 1
    if spawn_speed == config.game["spawn_increase_interval"]:
        global zombie_spawn
        zombie_spawn -= 1
        global skeleton_spawn
        skeleton_spawn -= 1


def new_attack(new_dir, new_type, spawn_location, container):
    attack_definition = config.attacks[new_type]
    attack = {
        'rect': Rect(spawn_location, (attack_definition["size"], attack_definition["size"])),
        'direction': new_dir,
        'life': attack_definition["life"],
        'speed': attack_definition["velocity"],
        'dead': False
    }
    container.append(attack)


def new_enemy(style, player, container):
    spawn = random.randint(1, config.game["spawnrate"])
    spawn_rate = {
        "z": zombie_spawn,
        "s": skeleton_spawn
    }
    if not spawn > spawn_rate[style]:
        return
    coin = random.randint(0, 10)
    enemy = config.enemies[style].copy()
    sight = {
        "z": zombie_sight,
        "s": skeleton_sight
    }
    enemy["sight"] = sight[style]
    enemy["awake"] = coin <= config.game["awareness"]
    enemy["rect"] = Rect(0, 0, enemy["size"], enemy["size"])
    enemy["rect"].topleft = (random.randint(1, config.game["width"] - enemy["size"]),
                                 random.randint(1, config.game["height"] - enemy["size"]))
    enemy["dead"] = False
    playerSafeZone.center = player["rect"].center
    if not enemy['rect'].colliderect(playerSafeZone):
        container.append(enemy)