game = {
    "title": "Zombie Apocalypse",
    "height": 600,
    "width": 600,
    "fps": 35,
    "spawnrate": 1001,
    "awareness": 0,
    "spawn_increase_interval": 50
}


colors = {
    "background": (0, 0, 0),
    "player": (255, 0, 0),
    "attack": (255, 255, 0),
    "zombie": (0, 255, 0),
    "skeleton": (255, 255, 255),
    "text": (255, 255, 255),
    "title": (0, 128, 0)
}

player = {
    "size": 15,
    "velocity": 3,
    "safety": 60
}

attacks = {
    "z": {
        "size": 5,
        "velocity": 5,
        "life": 2,
        "noise": 300
    },
    "x": {
        "size": 5,
        "velocity": 8,
        "life": 15,
        "noise": 200
    }
}

enemies = {
    "z": {
        "size": 17,
        "speed": 1,
        "sight": 150,
        "score": 10,
        "color": colors["zombie"]
    },
    "s": {
        "size": 13,
        "speed": 4,
        "sight": 100,
        "score": 15,
        "color": colors["skeleton"]
    }
}

scoreboard = 0, game["height"] + 1, game["width"], 100
safe_zone = 0, 0, player["safety"], player["safety"]
z_noise_rect = (0, 0), (attacks["z"]["noise"], attacks["z"]["noise"])
x_noise_rect = (0, 0), (attacks["x"]["noise"], attacks["x"]["noise"])
zombie_sight = 0, 0, enemies["z"]["sight"], enemies["z"]["sight"]
skeleton_sight = 0, 0, enemies["s"]["sight"], enemies["s"]["sight"]