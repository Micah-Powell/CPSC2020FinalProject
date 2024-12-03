import pygame
from random import randint


def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score_surf = font.render(f"Score: {current_time/1000:.0f}", False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    if current_time//1000 % 25 == 0:
            levelsfx.play()
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            if obstacle_rect.bottom == 300:
                obstacle_type = snail_surf
            else:
                obstacle_type = fly_surf
            obstacle_rect.x -= 5       
            screen.blit(obstacle_type,obstacle_rect)
            
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        
        return obstacle_list
    else:
        return []
   
def collisions(player,obstacles):
    if obstacles: 
        for rect in obstacles:
            if player.colliderect(rect):
                return False
    return True
        
def player_animation():
    global player_surf, player_index
    
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]
    

pygame.init()

screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Micah's game")
clock = pygame.time.Clock()
font = pygame.font.Font("Fonts/Pixeltype.ttf", 50)
game_active = False
start_time = 0
score = 0
highscore = 0

#background images
sky_surf = pygame.image.load("Graphics/Sky.png").convert()
ground_surf = pygame.image.load("Graphics/ground.png").convert()

#sounds

jumpsfx = pygame.mixer.Sound("Audio/jump.wav")
levelsfx = pygame.mixer.Sound("Audio/level.wav")

#music

pygame.mixer.music.load("Audio/lobby.mp3")
pygame.mixer.music.play(-1, 0.0)

#obstacles

snail_frame_1 = pygame.image.load("Graphics/Snail/snail1.png").convert_alpha()
snail_frame_2 = pygame.image.load("Graphics/Snail/snail2.png").convert_alpha()
snail_frames = [snail_frame_1,snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

fly_frame_1 = pygame.image.load("Graphics/Fly/Fly1.png").convert_alpha()
fly_frame_2 = pygame.image.load("Graphics/Fly/Fly2.png").convert_alpha()
fly_frames = [fly_frame_1,fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []

#Player

player_walk_1 = pygame.image.load("Graphics/Player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("Graphics/Player/player_walk_2.png").convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0

player_surf = player_walk[player_index]
player_jump = pygame.image.load("Graphics/Player/jump.png").convert_alpha()

player_rect = player_surf.get_rect(midbottom = (100,300))
player_gravity = 0

player_stand_surf = pygame.image.load("Graphics/Player/player_stand.png").convert_alpha()
player_stand_surf = pygame.transform.rotozoom(player_stand_surf,0,2)
player_stand_rect = player_stand_surf.get_rect(center = (400,200))

#menu screen

game_name_surf = font.render("Alien Run", False, "blue")
game_name_rect = game_name_surf.get_rect(center = (400,50))

directions_surf = font.render("Press the spacebar to start", False, "blue")
directions_rect = directions_surf.get_rect(center = (400,340))

#timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

#game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active == True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom > 299:
                    player_gravity = -19
                    jumpsfx.play()
            
            if event.type == obstacle_timer:
                if randint(0,2) == 1:
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900,1100), 190)))
                else:    
                    obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,1100), 300)))
                    
            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]
                
            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]    
                
        if game_active == False:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()
        
                    
    if game_active == True:   
        screen.blit(sky_surf, (0,0))
        screen.blit(ground_surf, (0,300))
        
        #Player
        
        player_gravity += .8
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf, player_rect)
       
        #obstacle movement
        
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #collision
        
        game_active = collisions(player_rect,obstacle_rect_list)
        
        score = display_score()
    
    else:
        #menu screen
        
        screen.fill(("grey"))
        screen.blit(player_stand_surf, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.bottom = 300
        player_gravity = 0        
        if score > highscore:
            highscore = score
        score_message_surf = font.render(f"Previous Score {score/1000:.0f}", False,"blue")
        score_rect = score_message_surf.get_rect(center = (300,80))
        highscore_surf = font.render(f"High Score {highscore/1000:.0f}", False,"blue")
        highscore_rect = score_message_surf.get_rect(center = (600,80))
        
        
        screen.blit(score_message_surf,score_rect)
        screen.blit(highscore_surf, highscore_rect)
        screen.blit(game_name_surf, game_name_rect)
        screen.blit(directions_surf, directions_rect)
      
    #frame rate limiter
        
    pygame.display.update()
    clock.tick(60)