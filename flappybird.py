import os
import sys
import pygame 
import random 
from sys import exit

#GAME VARIABLES
WINDOW_WIDTH = 360
WINDOW_HEIGHT = 640

BIRD_WIDTH = 34
BIRD_HEIGHT = 24
BIRD_X = WINDOW_WIDTH/8
BIRD_Y = WINDOW_HEIGHT/2

PIPE_WIDTH = 64
PIPE_HEIGHT = 512
PIPE_X = WINDOW_WIDTH
PIPE_Y = 0

#IMPORTING IMAGES
def resource_path(relative_path):
  try:
    base_path = sys._MEIPASS
  except Exception:
    base_path = os.path.abspath(".")
  return os.path.join(base_path, relative_path)

def load_image(image_name,scale=None) :
    full_path = resource_path(image_name)
    image = pygame.image.load(full_path) 
    if scale is not None :
        image = pygame.transform.scale(image,scale) 
    return image

background_image = load_image("flappybirdbg.png")
bird_image = load_image("flappybird.png",(BIRD_WIDTH,BIRD_HEIGHT))
toppipe_image = load_image("toppipe.png",(PIPE_WIDTH,PIPE_HEIGHT))
bottompipe_image = load_image("bottompipe.png",(PIPE_WIDTH,PIPE_HEIGHT))

class Bird(pygame.Rect) :
    def __init__(self,img):
        pygame.Rect.__init__(self,BIRD_X,BIRD_Y,BIRD_WIDTH,BIRD_HEIGHT) 
        self.img = img

class Pipe(pygame.Rect) :
    def __init__(self,img):
        pygame.Rect.__init__(self,PIPE_X,PIPE_Y,PIPE_WIDTH,PIPE_HEIGHT) 
        self.img = img
        self.passed = False

#SETTING WINDOW
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("FLAPPY BIRD")
pygame.display.set_icon(bird_image)
clock = pygame.time.Clock()

create_pipes_timer = pygame.USEREVENT + 0
pygame.time.set_timer(create_pipes_timer,1500) #FOR EVERY 1.5 SEC

#GAME
bird = Bird(bird_image)
pipes = []
bird_velocity_y = 0
pipe_velocity_x = -2
gravity = 0.4
score = 0
game_over = False

def create_pipes() :
    random_pipe_y = PIPE_Y - PIPE_HEIGHT/4 - random.random() * (PIPE_HEIGHT/2)
    open_height = WINDOW_HEIGHT/4

    top_pipe = Pipe(toppipe_image)
    top_pipe.y = random_pipe_y
    pipes.append(top_pipe)

    bottom_pipe = Pipe(bottompipe_image)
    bottom_pipe.y = top_pipe.y + top_pipe.height + open_height
    pipes.append(bottom_pipe)

def move() :
    global bird_velocity_y,score,game_over

    bird_velocity_y += gravity
    bird.y += bird_velocity_y
    bird.y = max(bird.y,0)

    if bird.y > WINDOW_HEIGHT :
        game_over = True
        return

    for pipe in pipes :
        pipe.x += pipe_velocity_x

        if not pipe.passed and pipe.x + pipe.width < bird.x :
            score += 0.5
            pipe.passed = True

        if bird.colliderect(pipe) :
            game_over = True
            return

    while len(pipes) > 0 and pipes[0].x < - PIPE_WIDTH :
        pipes.pop(0)

def draw() :
    window.fill("black")
    window.blit(background_image,(0,0))
    window.blit(bird.img,bird)

    for pipe in pipes :
        window.blit(pipe.img,pipe)

    score_str = str(int(score))
    text_str = "Game Over : "
    def_color = "yellow"

    text_font = pygame.font.SysFont("Comic Sans MS",45)

    if game_over :
        def_color = "#f50707"
        text_render = text_font.render(text_str,True,def_color)
        window.blit(text_render,(5,0))
        def_color = "#1e72fa"
        score_render = text_font.render(score_str,True,def_color)
        window.blit(score_render,(275,0))
    else :
        score_render = text_font.render(score_str,True,def_color)
        window.blit(score_render,(5,0))

while True :
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            pygame.quit()
            exit()

        if event.type == create_pipes_timer and not game_over :
            create_pipes()

        if event.type == pygame.KEYDOWN :
            if event.key in (pygame.K_UP,pygame.K_SPACE) :
                bird_velocity_y = -6

            if game_over and event.key == pygame.K_RETURN :
                bird.y = BIRD_Y
                bird_velocity_y = -6
                pipes.clear()
                score = 0
                game_over = False

    if not game_over :
        move()
        draw()
        pygame.display.update()
        clock.tick(60) #60FPS