import pygame.draw

import config


def game(windowSurface, font, containers, top_score):
    player = containers["player"]
    attacks = containers["attacks"]
    enemies = containers["enemies"]

    windowSurface.fill(config.colors["background"])
    for a in attacks:
        pygame.draw.rect(windowSurface, config.colors["attack"], a['rect'])
    pygame.draw.rect(windowSurface, config.colors["player"], player["rect"])
    for e in enemies:
        pygame.draw.rect(windowSurface, e['color'], e['rect'])
    # Draw the score and top score.
    text_draw('Score: %s' % player["score"], font, windowSurface, 20, 620, config.colors["text"])
    text_draw('Top Score: %s' % top_score, font, windowSurface, 20, 660, config.colors["text"])

    life_block = pygame.Rect(0, 620, 30, 30)
    for x in range(1, 11):
        life_block.left = 590 - (x * 40)
        if player["life"] >= x:
            pygame.draw.rect(windowSurface, config.colors["player"], life_block)
        else:
            pygame.draw.rect(windowSurface, config.colors["player"], life_block, 2)


def text_draw(text, font, surface, x, y, color):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)