import os
import pygame
import random
import sys

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode([500, 600])
screen.fill(pygame.Color('blue'))
particles = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
buttons = pygame.sprite.Group()
tubes = pygame.sprite.Group()


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

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, dx, dy):
        super().__init__(particles)
        self.fire = [load_image(random.choice(["хлопушка1.bmp", "хлопушка2.bmp", "хлопушка3.bmp"]), (255, 255, 255))]
        for scale in (5, 10, 20):
            self.fire.append(pygame.transform.scale(self.fire[0], (scale, scale)))        
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        self.gravity = 0.2

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()
            
def create_particles(position):
    particle_count = 50
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers)) 

class Background(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image("фон.png", 0)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        
def click():
    pygame.mixer.music.load(os.path.join('data', 'click.mp3'))
    pygame.mixer.music.play()    

def fly():
    pygame.mixer.music.load(os.path.join('data', 'fly.mp3'))
    pygame.mixer.music.play() 
    
class Button(pygame.sprite.Sprite):
    def __init__(self, group, x, y, image):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        self.kill()  
