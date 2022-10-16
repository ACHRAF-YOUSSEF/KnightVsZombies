import csv
import os
from random import randint

import pygame

from settings import *


def draw_bg(screen, gs, sky_img, mountain_img, pine1_img, pine2_img):
    screen.fill(BLACK)
    width = sky_img.get_width()
    for x in range(5):
        screen.blit(sky_img, ((x * width) - gs.bg_scroll * 0.5, 0))
        screen.blit(mountain_img, ((x * width) - gs.bg_scroll * 0.6, HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img, ((x * width) - gs.bg_scroll * 0.7, HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img, ((x * width) - gs.bg_scroll * 0.8, HEIGHT- pine2_img.get_height()))

#function to reset level
def reset_level():
    enemy_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()

	#create empty tile list
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)

    return data


def draw_text(screen, txt, x, y, police, color):
    txt_font = pygame.font.Font(None, police)
    txt = txt_font.render(txt, True, color)
    txt_rect = txt.get_rect()
    txt_rect.center =  (x, y)
    screen.blit(txt,txt_rect)


class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y, gs):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.gs = gs
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
    
    def update(self):
        self.rect.x += self.gs.screen_scroll


class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y, gs):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.gs = gs
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
    
    def update(self):
        self.rect.x += self.gs.screen_scroll


class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y, gs):
        pygame.sprite.Sprite.__init__(self)
        self.gs = gs
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
    
    def update(self):
        self.rect.x += self.gs.screen_scroll

class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y, gs):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.gs = gs
        self.image = gs.item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self, Knight):
        self.rect.x += self.gs.screen_scroll
		#check if the player has picked up the box
        if pygame.sprite.collide_rect(self, Knight):
			#check what kind of box it was
            if self.item_type == 'Health':
                Knight.health += 25
                if Knight.health > Knight.max_health:
                    Knight.health = Knight.max_health
			
            #delete the item box
            self.kill()


class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, screen, Knight, health):
		#update with new health
        self.health = health
		#calculate health ratio
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))
        img = pygame.image.load(f"../graphics/Characters/PNG/KNIGHTS/3/Head/{Knight.character_num}.png")
        img = pygame.transform.scale(img,(int(img.get_width() * 0.12),int(img.get_height()) * 0.12))
        img_rect = img.get_rect()
        img_rect.center = (45,45)
        screen.blit(img, img_rect)
        draw_text(screen, f'{Knight.health}/{Knight.max_health}', self.x + 70, self.y + 10, 36, colors["black"])


class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data, img_list, gs):
        zombies_nb = 0
        self.level_length = len(data[0])
		#iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)
                    
                    elif tile >= 9 and tile <= 10:
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE, gs)
                        water_group.add(water)
                    
                    elif tile >= 11 and tile <= 14:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE, gs)
                        decoration_group.add(decoration)
                    
                    elif tile == 15:#create player
                        Knight = Character(character_type="KNIGHTS", character_num = gs.char_num, x=x * TILE_SIZE,y=y * TILE_SIZE, scale=0.15, speed=5)
                        health_bar = HealthBar(85, 45, Knight.health, Knight.health) 
                    
                    elif tile == 16:#create enemies
                        Zombie = Character(character_type="ZOMBIES", character_num = randint(1,3), x=x * TILE_SIZE,y=y * TILE_SIZE, scale=0.2, speed=2)
                        enemy_group.add(Zombie)
                        zombies_nb += 1
                    
                    elif tile == 17:#create health box
                        item_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE, gs)
                        item_box_group.add(item_box)
                    
                    elif tile == 18:#create exit
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE, gs)
                        exit_group.add(exit)

        return Knight, health_bar

    def draw(self, screen, screen_scroll):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])


class Character(pygame.sprite.Sprite):
    def __init__(self, character_type, character_num, x=0, y=0, scale=0, speed=0):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.scale = scale
        self.character_type = character_type
        self.character_num = character_num - 1 
        self.speed = speed
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.got_hit = False
        self.animations_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        
        #ai specific variables
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 60, 20)
        self.idling = False
        self.idling_counter = 0
        
        self.timer1 = BasicTimer(10)

        animations = ['1','2','3']
        animation_types = ['Idle','Run','Jump','Attack','Die']
        for j in animations:
            animation_list = []
            for animation in animation_types:
                temp_list = []
                num_of_frames = len(os.listdir(f"../graphics/Characters/PNG/{self.character_type}/{j}/{animation}"))
                for i in range(num_of_frames):
                    img = pygame.image.load(f"../graphics/Characters/PNG/{self.character_type}/{j}/{animation}/{i}.png").convert_alpha()
                    img = pygame.transform.scale(img,(int(img.get_width() * self.scale),int(img.get_height()) * self.scale))
                    temp_list.append(img)
                animation_list.append(temp_list)
            self.animations_list.append(animation_list)
        
        self.image = self.animations_list[self.character_num][self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def move(self, gs, world, moving_left, moving_right):
        screen_scroll = 0
        dx,dy = 0,0

        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1 

        # jump
        if self.jump and not self.in_air:
            jump_fx.play()
            self.vel_y -= 15
            self.jump = False
            self.in_air = True
        
        # gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        #check for collision
        for tile in world.obstacle_list:
			#check collision in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                #if the ai has hit a wall then make it turn around
                if self.character_type == 'ZOMBIES':
                    self.direction *= -1
                    self.move_counter = 0
			
            #check for collision in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				#check if below the ground, i.e. jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
				
                #check if above the ground, i.e. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        #check for collision with water
        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0
        
        #check for collision with exit
        level_complete = False

        if pygame.sprite.spritecollide(self, exit_group, False) and len(enemy_group) <= 0:
            gs.zombies_nb = 0
            level_complete = True

		#check if fallen off the map
        if self.rect.bottom > HEIGHT:
            self.health = 0

        #check if going off the edges of the screen
        if self.character_type == 'KNIGHTS':
            if self.rect.left + dx < 0 or self.rect.right + dx > WIDTH:
                dx = 0

        # update rect position
        self.rect.x += dx
        self.rect.y += dy

        #update scroll based on player position
        if self.character_type == 'KNIGHTS':
            if (self.rect.right > WIDTH - SCROLL_THRESH and gs.bg_scroll < (world.level_length * TILE_SIZE) - WIDTH) or (self.rect.left < SCROLL_THRESH and gs.bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll, level_complete

    def update(self, screen, gs, Knight):
        self.update_animation(screen, gs, Knight)
        self.check_alive()

    def update_animation(self, screen, gs, Knight):
        ANIMATION_COOLDOWN = 100

        self.image = self.animations_list[self.character_num][self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        
        if self.frame_index >= len(self.animations_list[self.character_num][self.action]):
            if self.action == 3:
                gs.attack = False
                self.update_action(0)
                if self.character_type == "KNIGHTS":
                    for enemy in enemy_group: 
                        enemy.got_hit = False
                
                else:
                    Knight.got_hit = False
            
            elif self.action == 4:
                self.frame_index = len(self.animations_list[self.character_num][self.action])-1
                self.timer1.do_Function(screen, self, -1, -1)
            
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action: 
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
    
    def Attack(self, gs, Knight):
        if self.character_type == "KNIGHTS":
            Knight.update_action(3)
            for enemy in enemy_group: 
                if pygame.sprite.collide_rect(Knight, enemy):
                    if Knight.alive:
                        if enemy.alive:
                            if not enemy.got_hit:
                                enemy.health -= 25
                                enemy.got_hit = True           
                        
                        else:
                            enemy.update_action(4)
                            Zombie_Dying_and_Choking_A1_fx.play()
                            enemy.rect.y += 1
                            gs.zombies_nb -= 1
                    
                    else:
                        Knight.update_action(4)
       
        else:
            self.update_action(3)
            if pygame.sprite.collide_rect(Knight, self):
                if Knight.alive:
                    if self.alive:
                        if self.action == 3:
                            if not Knight.got_hit:
                                if self.character_num == 1:
                                    Knight.health -= 5
                                
                                elif self.character_num == 2:
                                    Knight.health -= 10
                                
                                else:
                                    Knight.health -= 15
                                Knight.got_hit = True          
                    else:
                        self.update_action(4)
                        Zombie_Dying_and_Choking_A1_fx.play()
                        self.rect.y += 1
                        gs.zombies_nb -= 1
                
                else:
                    Knight.update_action(4)
    
    def ai(self, gs, world, Knight):
        if self.alive and Knight.alive:
            if not self.idling and randint(1, 200) == 1:
                self.update_action(0)#0: idle
                Zombie_Breathing_H1_fx.play()
                self.idling = True
                self.idling_counter = 40
			
            #check if the ai in near the player
            if self.vision.colliderect(Knight.rect):
                if self.rect.colliderect(Knight.rect):
                    Zombie_Short_Attack_A1_fx.play()
                    self.Attack(gs, Knight)
                
                else:
                    if self.rect.x != Knight.rect.x :
                        if self.direction == 1:
                            ai_moving_right = True
                        
                        else:
                            ai_moving_right = False
                        ai_moving_left = not ai_moving_right
                        
                        self.move(gs, world, ai_moving_left, ai_moving_right)
                        self.update_action(1)
                        self.move_counter += 1
            
            else:
                if not self.idling:
                    if self.direction == 1:
                        ai_moving_right = True
                    
                    else:
                        ai_moving_right = False
                    
                    ai_moving_left = not ai_moving_right
                    self.move(gs, world, ai_moving_left, ai_moving_right)
                    self.update_action(1)#1: run
                    self.move_counter += 1
					
                    #update ai vision as the enemy moves
                    self.vision.center = (self.rect.centerx +60 * self.direction, self.rect.centery)

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False
        
        # scroll
        self.rect.x += gs.screen_scroll

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(4)

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image,self.flip,False),self.rect)


class GameState:
    def __init__(self, menuNames, states):
        self.state_index = 0
        self.states = states
        self.menuNames = menuNames
        self.current_state = self.menuNames[self.state_index]
        
        self.MenusLog = ["main menu"]
        
        self.caption = self.current_state
        
        self.musicListNames = os.listdir("../audio/8bit-music")
        self.musicListLength = int(len(self.musicListNames))
        self.musicList = [f"../audio/8bit-music/{song}" for song in self.musicListNames]
        self.music_index = randint(0, self.musicListLength - 1)
        self.musicIsPlaying = False
        
        self.screen_scroll = 0
        self.bg_scroll = 0
        self.level = 0
        self.moving_left = False
        self.moving_right = False
        self.attack = False
        self.char_num = 1
        self.zombies_nb = 0
        
        #pick up boxes
        self.health_box_img = pygame.image.load('../graphics/Characters/PNG/Health/health_box.png')

        self.item_boxes = {
            'Health': self.health_box_img
        }
        
        # character changer images
        img_1 = pygame.image.load("../graphics/Characters/PNG/KNIGHTS/1/Idle/0.png")
        img_2 = pygame.image.load("../graphics/Characters/PNG/KNIGHTS/2/Idle/0.png")
        img_3 = pygame.image.load("../graphics/Characters/PNG/KNIGHTS/3/Idle/0.png")

        img_1 = pygame.transform.scale(img_1, (int(img_1.get_width() * 0.2), int(img_1.get_height()) * 0.2))
        img_2 = pygame.transform.scale(img_2, (int(img_2.get_width() * 0.2), int(img_2.get_height()) * 0.2))
        img_3 = pygame.transform.scale(img_3, (int(img_3.get_width() * 0.2), int(img_3.get_height()) * 0.2))

        rect_1 = img_1.get_rect()
        rect_2 = img_2.get_rect()
        rect_3 = img_3.get_rect()

        rect_1.center = (WIDTH//2 + 20, HEIGHT//2-200)
        rect_2.center = (WIDTH//2 + 20, HEIGHT//2-200)
        rect_3.center = (WIDTH//2 + 20, HEIGHT//2-200)
        
        self.img = [img_1, img_2, img_3]
        self.rect = [rect_1, rect_2, rect_3]
        
    def stateManager(self, screen, bg, world, Knight, health_bar, clock, img_list):
        if len(self.states) != 0:
            self.caption = self.menuNames[self.state_index]
            self.states[self.state_index].draw(screen, self, bg, world, Knight, health_bar, clock, img_list)
        

class Move:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        
        self.color = color


class Button:
    def __init__(self, text, width, height, pos, elevation, task, top_color = '#475F77', on_collide_top_color = '#D74B4B', bottom_color = '#354B5E'):
        # Core attributes
        self.task = task
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.default_top_color = top_color
        self.on_collide_top_color = on_collide_top_color
        self.top_color = top_color

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = bottom_color

        # text
        self.text_surf = pygame.font.Font(None, 30).render(text, True, BLACK)
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self, screen, gs):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=12)
        screen.blit(self.text_surf, self.text_rect)
        
        self.check_click(gs)

    def check_click(self, gs):
        mouse_pos = pygame.mouse.get_pos()
        
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = self.on_collide_top_color
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed:
                    self.do_function(gs)
                    self.pressed = False
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = self.default_top_color
            
    def do_function(self, gs):
        if self.task == "play":
            print("beginning...!")
            gs.current_state = "game"
            gs.MenusLog.append(gs.current_state)
            gs.state_index = gs.menuNames.index(gs.current_state)
            
        if self.task == "start":
            print("starting...!")
            gs.current_state = "play menu"
            gs.MenusLog.append(gs.current_state)
            gs.state_index = gs.menuNames.index(gs.current_state)
            
        if self.task == "exit":
            print("exiting...!")
            quit()
            
        if self.task == "options":
            print("opening options menu...!")
            gs.current_state = "options menu"
            gs.MenusLog.append(gs.current_state)
            gs.state_index = gs.menuNames.index(gs.current_state)
        
        if self.task == "backFromOptions":
            gs.MenusLog = gs.MenusLog[:-1]
            gs.state_index = gs.menuNames.index(gs.MenusLog[-1])
            gs.current_state = gs.menuNames[gs.state_index]
            
        if self.task == "back":
            gs.MenusLog = gs.MenusLog[:-1]
            gs.state_index = gs.menuNames.index(gs.MenusLog[-1])
            gs.current_state = gs.menuNames[gs.state_index]
            
        if self.task == "music":
            print("changing...!")
            
            gs.music_index += 1
            
            if gs.music_index >= len(gs.musicList):
                gs.music_index = 0
                
                
        if self.task == "change":
            print("changing...!")
            
            gs.char_num += 1
            
            if gs.char_num >= 4:
                gs.char_num = 1
                
        if self.task == "replay":
            print("restarting...!")
            
            gs.current_state = "game"
            gs.MenusLog = ["main menu", "play menu", "game"]
            gs.state_index = gs.menuNames.index(gs.current_state)


class BasicTimer:
    def __init__(self, time_to_wait = 2):
        self.time_to_wait = time_to_wait
        self.current_time = 0
        self.start_time = pygame.time.get_ticks()
        
    def do_Function_case_1(self, screen, character, x=0):
        if x == -1:
            pass
    
    def do_Function_case_2(self, screen, character, x=0):
        if x == -1:
            character.kill()
    
    def do_Function(self, screen, character, x1, x2):
        self.current_time = pygame.time.get_ticks()
        
        if self.current_time - self.start_time < self.time_to_wait * 1000:
            self.do_Function_case_1(screen, character, x1)
            
        else:
            self.do_Function_case_2(screen, character, x2)

class Menu:
    def __init__(self, name, task, Timers = [], menuButtons = []):
        self.name = name
        self.task = task
        self.buttons = menuButtons
        self.Timers = Timers
    
    def draw(self, screen, gs, bg, world, Knight, health_bar, clock, img_list):
        screen.fill(BLACK)
        
        self.doFunction(screen, gs, clock, self.Timers, bg, world, Knight, health_bar, img_list)

        for button in self.buttons:
            button.draw(screen, gs)
            
        clock.tick(MAX_FPS)
    
    def doFunction(self, screen, gs, clock, basicTimer, bg, world, Knight, health_bar, img_list):
        if self.task == "gameLogic":  
            Knight.character_num = gs.char_num - 1
            draw_bg(screen, gs, bg[0], bg[1], bg[2], bg[3])
            world.draw(screen, gs.screen_scroll)
            
            # update animation
            Knight.update(screen, gs, Knight)
            
            # draw player
            Knight.draw(screen)

            #show player health
            health_bar.draw(screen, Knight, Knight.health)

            #update and draw groups
            item_box_group.update(Knight)
            decoration_group.update()
            water_group.update()
            exit_group.update()
            item_box_group.draw(screen)
            decoration_group.draw(screen)
            water_group.draw(screen)
            exit_group.draw(screen)
            
            for enemy in enemy_group:
                if enemy.alive:
                    draw_text(screen, f'{enemy.health}', enemy.rect.x + 15, enemy.rect.y - 20, 40, colors["green"])
                    
                enemy.ai(gs, world, Knight)
                enemy.update(screen, gs, Knight)
                enemy.draw(screen)

            if Knight.alive:
                if gs.attack:
                    Knight.Attack(gs, Knight)
                
                elif Knight.in_air:
                    Knight.update_action(2)
                
                elif gs.moving_left or gs.moving_right:
                    Knight.update_action(1)
                
                else:
                    Knight.update_action(0)

                gs.screen_scroll, level_complete = Knight.move(gs, world, gs.moving_left, gs.moving_right)
                gs.bg_scroll -= gs.screen_scroll
                
                if level_complete:
                    gs.level += 1
                    gs.bg_scroll = 0
                    world_data = reset_level()
                    if gs.level <= MAX_LEVELS:
                        #load in level data and create world
                        with open(f'../Levels/level{gs.level}_data.csv', newline='') as csvfile:
                            reader = csv.reader(csvfile, delimiter=',')
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)
                        
                        world = World()
                        Knight, health_bar = world.process_data(world_data, img_list, gs)	
                    
                    else:
                        pygame.mixer.music.pause()
                        gs.current_state = "game over screen"
                        gs.MenusLog.append(gs.current_state)
                        gs.state_index = gs.menuNames.index(gs.current_state)

            else:
                pygame.mixer.music.pause()
                gs.current_state = "game over screen"
                gs.MenusLog.append(gs.current_state)
                gs.state_index = gs.menuNames.index(gs.current_state)
            
            draw_text(screen, f"fps = {int(clock.get_fps())}", WIDTH-60, HEIGHT-620, 40, colors["red"])
            
        if self.task == "main menu":
            pass
        
        if self.task == "play menu":
            draw_text(screen, f'{gs.char_num}', WIDTH//2, HEIGHT//2-300, 50, colors["white"])
            screen.blit(gs.img[gs.char_num-1], gs.rect[gs.char_num-1])

        if self.task == "options menu":
            temp = gs.musicList[gs.music_index].split("/")

            txt = f"{temp[3]}"
            
            draw_text(screen, txt, WIDTH//2, HEIGHT//2-100, 50, colors["white"])

        if self.task == "gameOver":
            draw_text(screen, "Game Over", WIDTH//2, HEIGHT//2-100, 50, colors["red"])
