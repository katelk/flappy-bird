import os
import pygame
import random
import sys

pygame.init()
screen = pygame.display.set_mode([500, 600])
screen.fill(pygame.Color('blue'))


def load_image(name, colorkey):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if colorkey != 0:
        image.set_colorkey(colorkey)
    return image

def start_screen():
    intro_text = ["", "", "", "", "",
                  "           WELCOME TO FLAPPY BIRD GAME", "",
                  "                           Правила игры:",
                  "                       Они всем известны.",
                  "                Нажми, чтобы начать играть",
                  "                                 ---------->",
                  "                       P.s. пробел = пауза"]
 
    fon = pygame.transform.scale(load_image('фон.png', 0), (500, 600))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
 
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return True
        pygame.display.flip()

running = start_screen()
