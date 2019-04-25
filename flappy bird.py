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

def terminate():
    pygame.quit()
    sys.exit()
    
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

class Bird(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.n = "1"
        self.image = load_image("bird{}.1.bmp".format(self.n), (255, 255, 255))
        self.image = pygame.transform.scale(self.image, (70, 55))
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 210
    
    def update(self):
        if self.rext.y == 655:
            all_sprites.remove(self)
            
class Tube(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image("труба.bmp", (255, 255, 255)), (100, 1010))
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = random.randint(-310, 0)
        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self, n):
        if n == 0:
            self.rect.x -= 2
            if self.rect.x < -100:
                self.kill()
            if self.rect.x == 270:
                tubes.add(Tube(all_sprites))
            if self.rect.x == 200:
                return True
            return False
        else:
            self.kill()

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
        
screen_rect = (0, 0, 500, 600)        
best_score = 0
result = 0


def beginning():
    global best_score    
    clicked = 0
    bird.rect.x = 200
    bird.rect.y = 210
    button_play = Button(buttons, 100, 300, load_image("начать.png", 0))
    button_shop = Button(buttons, 450, 10, pygame.transform.scale(load_image("магазин.png", 0), (40, 40)))
    button_exit = Button(buttons, 145, 410, pygame.transform.scale(load_image("exit.bmp", 0), (210, 75)))
    best = Button(buttons, 0, 0, pygame.transform.scale(load_image("best.bmp", (255, 255, 255)), (200, 40)))
    vy = 5
    for i in range(len(str(best_score))):
        Button(buttons, i*25, 40, pygame.transform.scale(load_image("{}.bmp".format(str(best_score)[i]), (255, 255, 255)), (25, 30)))    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == MYEVENTTYPE:
                bird.rect.y += vy/1            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:              
                if 100 < event.pos[0] < 400 and 300 < event.pos[1] < 400:
                    click()
                    buttons.empty()
                    if play():
                        return True
                if 450 < event.pos[0] < 490 and 10 < event.pos[1] < 50:
                    click()
                    if shop():
                        return True
                if 145 < event.pos[0] < 355 and 410 < event.pos[1] < 585:
                    click()
                    terminate()               
                vy = 5
            clicked += 1
            if clicked and clicked > 20:
                bird.image = load_image("bird{}.1.bmp".format(bird.n), (255, 255, 255))
                bird.image = pygame.transform.scale(bird.image, (70, 55))
                vy = 2
                if clicked == 40:
                    clicked = 0
            else:
                bird.image = load_image("bird{}.2.bmp".format(bird.n), (255, 255, 255))
                bird.image = pygame.transform.scale(bird.image, (70, 55))
                vy = -2
        screen.fill(pygame.Color('white')) 
        all_sprites.draw(screen)
        buttons.draw(screen)
        pygame.display.flip()


background = Background(all_sprites)
bird = Bird(all_sprites)           
MYEVENTTYPE = 30
pygame.time.set_timer(MYEVENTTYPE, 20)
clock = pygame.time.Clock()

while running:
    if beginning():
        pass
pygame.quit()
