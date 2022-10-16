import csv
from threading import Thread

import pygame

import engine
from settings import *


# functions
def thread_1():
    global Knight, health_bar, world, bg, img_list, finished
    
    #load images
    pine1_img = pygame.image.load('../graphics/Characters/PNG/Background/pine1.png').convert_alpha()
    pine2_img = pygame.image.load('../graphics/Characters/PNG/Background/pine2.png').convert_alpha()
    mountain_img = pygame.image.load('../graphics/Characters/PNG/Background/mountain.png').convert_alpha()
    sky_img = pygame.image.load('../graphics/Characters/PNG/Background/sky_cloud.png').convert_alpha()
    
    bg = [sky_img, mountain_img, pine1_img, pine2_img]

    #store tiles in a list
    img_list = []
    for x in range(TILE_TYPES):
        img = pygame.image.load(f'../graphics/Characters/PNG/Tile/{x}.png')
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        img_list.append(img)
        
    #create empty tile list
    world_data = []
    for row in range(ROWS):
        r = [-1] * COLS
        world_data.append(r)
    
    #load in level data and create world
    with open(f'../Levels/level{gs.level}_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                world_data[x][y] = int(tile)
    
    world = engine.World()
    Knight, health_bar = world.process_data(world_data, img_list, gs)
    
    finished = True

def loading():
    global finished

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    
    previous_time = pygame.time.get_ticks()

    while (not finished):
        screen.fill((0, 0, 0))
        pygame.display.set_caption("loading data...!")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                
        current_time = pygame.time.get_ticks()
                
        pygame.draw.rect(screen, BLACK, (WIDTH//2 - 80, HEIGHT//2 - 2, 154, 24))
        pygame.draw.rect(screen, RED, (WIDTH//2 - 80, HEIGHT//2, 150, 20))
        pygame.draw.rect(screen, GREEN, (WIDTH//2 - 80, HEIGHT//2, 18 * current_time//previous_time, 20))
        
        engine.draw_text(screen, f'{(current_time//previous_time)*10}/{100}', WIDTH//2 - 80 + 70, HEIGHT//2 + 10, 36, colors["black"])
                
        pygame.display.update()
        clock.tick(MAX_FPS)

def main():
    global gs

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    while True:
        pygame.display.set_caption(gs.caption)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                
             # keyboard presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    gs.moving_left = True
                
                if event.key == pygame.K_RIGHT:
                    gs.moving_right = True
                
                if event.key == pygame.K_SPACE:
                    gs.attack = True
                    if Knight.character_num == 2:
                        sword_fx.play(0)
                    
                    elif Knight.character_num == 1:
                        Spear_fx.play(0)
                    
                    else:
                        AxeBattle_fx.play(0)
                
                if event.key == pygame.K_UP and Knight.alive:
                    Knight.jump = True
                
                if event.key == pygame.K_ESCAPE:
                    gs.current_state = "play menu"
                    gs.MenusLog.append(gs.current_state)
                    gs.state_index = gs.menuNames.index(gs.current_state)
                    
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    gs.moving_left = False
                
                if event.key == pygame.K_RIGHT:
                    gs.moving_right = False
                
        gs.stateManager(screen, bg, world, Knight, health_bar, clock, img_list)

        pygame.display.update()
        
        if gs.current_state == "game":
            if not gs.musicIsPlaying:
                pygame.mixer.music.load(gs.musicList[gs.music_index])
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play()
                gs.musicIsPlaying = True
                
            pygame.mixer.music.unpause()
            
            if not pygame.mixer.music.get_busy():
                gs.music_index += 1
            
                if gs.music_index >= len(gs.musicList):
                    gs.music_index = 0
                
                gs.musicIsPlaying = False  
        
        else:
            pygame.mixer.music.pause()
            
if __name__ == "__main__":
    pygame.init()  
    
    # icon
    icon = pygame.transform.scale(pygame.image.load("../graphics/icon/3.png"), (512, 512))
    pygame.display.set_icon(icon)
    
    # play menu buttons
    playMenuButtons = [engine.Button("play", 200, 40, (WIDTH//2-100, HEIGHT//2-100), 5, "play", top_color='#0c3f91', on_collide_top_color='#2167d9', bottom_color='#3a69b5'),
                       engine.Button("change", 200, 40, (WIDTH//2-100, HEIGHT//2-50), 5, "change", top_color='#0c3f91', on_collide_top_color='#2167d9', bottom_color='#3a69b5'),
                       engine.Button("back", 200, 40, (WIDTH//2-100, HEIGHT//2), 5, "back", top_color='#0c3f91', on_collide_top_color='#2167d9', bottom_color='#3a69b5')
    ]
    
    # main menu buttons
    mainMenuButtons = [engine.Button("start", 200, 40, (WIDTH//2-100, HEIGHT//2-100), 5, "start", top_color='#0c3f91', on_collide_top_color='#2167d9', bottom_color='#3a69b5'),
                       engine.Button("options", 200, 40, (WIDTH//2-100, HEIGHT//2-50), 5, "options", top_color='#0c3f91', on_collide_top_color='#2167d9', bottom_color='#3a69b5'),
                       engine.Button("exit", 200, 40, (WIDTH//2-100, HEIGHT//2), 5, "exit", top_color='#0c3f91', on_collide_top_color='#2167d9', bottom_color='#3a69b5')
    ] 
    
    # options menu buttons  
    optionsMenuButtons = [engine.Button("change", 100, 40, (WIDTH//2-50, HEIGHT//2-50), 5, "music", top_color='#0c3f91', on_collide_top_color='#2167d9', bottom_color='#3a69b5'),
                            engine.Button("back", 200, 40, (WIDTH//2-100, HEIGHT//2), 5, "backFromOptions", top_color='#0c3f91', on_collide_top_color='#2167d9', bottom_color='#3a69b5')
    ]
    
    Menus = [engine.Menu("main menu", "main menu", menuButtons = mainMenuButtons), 
             engine.Menu("play menu", "play menu", menuButtons = playMenuButtons), 
             engine.Menu("options menu", "options menu", menuButtons = optionsMenuButtons), 
             engine.Menu("game", "gameLogic", [engine.BasicTimer(5)]),
             engine.Menu("game over screen", "gameOver")
    ]
    
    menuNames = [Menu.name for Menu in Menus]

    gs = engine.GameState(menuNames, Menus)
    
    Knight = None 
    health_bar = None
    world = None
    bg = []
    img_list = []
    
    finished = False
    
    x = Thread(target = thread_1)
    
    x.start()
    
    loading()
    x.join()
    
    main()
