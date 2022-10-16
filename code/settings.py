import pygame
import os

pygame.mixer.init()

WIDTH = 800
HEIGHT = int(WIDTH * 0.8)

DIMENSION_Y = 7
DIMENSION_X = 7

SQ_SIZE_Y = HEIGHT // DIMENSION_Y
SQ_SIZE_X = WIDTH // DIMENSION_X

MAX_FPS = 60

GRAVITY = 0.75
SCROLL_THRESH = 200
ROWS = 16
COLS = 150
TILE_SIZE = HEIGHT // ROWS
TILE_TYPES = int(len(os.listdir("../graphics/Characters/PNG/Tile")))
MAX_LEVELS = int(len(os.listdir("../Levels"))) - 1

#create sprite groups
enemy_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

# colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

colors = {"white":WHITE, "red":RED, "green":GREEN, "grey":GREY, "blue":BLUE, "black":BLACK, "1":(120, 100, 100), "2":(150, 80, 50), "3":(200, 50, 50), "4":(20, 120, 255)}
IMAGES = {}

# fx
# Knights
jump_fx = pygame.mixer.Sound('../audio/sfx/Knights/jump.wav')
sword_fx = pygame.mixer.Sound('../audio/sfx/Knights/sword.mp3')
AxeBattle_fx = pygame.mixer.Sound('../audio/sfx/Knights/AxeBattle.mp3')
Spear_fx = pygame.mixer.Sound('../audio/sfx/Knights/Spear.mp3')

# Zombies
Zombie_Biting_A1_fx = pygame.mixer.Sound('../audio/sfx/Zombies/Zombie-Biting-A1.mp3')
Zombie_Breathing_H1_fx = pygame.mixer.Sound('../audio/sfx/Zombies/Zombie-Breathing-H1.mp3')
Zombie_Breathing_Short_A3_fx = pygame.mixer.Sound('../audio/sfx/Zombies/Zombie-Breathing-Short-A3.mp3')
Zombie_Dying_and_Choking_A1_fx = pygame.mixer.Sound('../audio/sfx/Zombies/Zombie-Dying-and-Choking-A1.mp3')
Zombie_Growl_A7_fx = pygame.mixer.Sound('../audio/sfx/Zombies/Zombie-Growl-A7.mp3')
Zombie_Short_Attack_A1_fx = pygame.mixer.Sound('../audio/sfx/Zombies/Zombie-Short-Attack-A1.mp3')

# set volume
jump_fx.set_volume(1)
sword_fx.set_volume(1)
AxeBattle_fx.set_volume(1)
Spear_fx.set_volume(1)
Zombie_Biting_A1_fx.set_volume(0.02)
Zombie_Breathing_H1_fx.set_volume(0.02)
Zombie_Breathing_Short_A3_fx.set_volume(0.02)
Zombie_Dying_and_Choking_A1_fx.set_volume(0.05)
Zombie_Growl_A7_fx.set_volume(0.02)
Zombie_Short_Attack_A1_fx.set_volume(1)
