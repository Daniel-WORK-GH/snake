import pygame
import time
import random

#game colors
player_color = (0, 0, 0)
text_color = (0, 0, 0)
food_color = (255, 0 ,0)
backgroud_color = (255, 255, 255)

#tile size
tile_width = 16
tile_height = 16

#screen size
screen_width = 640
screen_height = 480

#add two tuples element wise
def add_positions(pos_a, pos_b) -> tuple :
    return tuple(map(sum, zip(pos_a, pos_b)))

#spawn food on map - doesnt take into acount player tiles
def spawn_food() -> tuple :
    foodx = random.randrange(0, screen_width // tile_width) * tile_width
    foody = random.randrange(0, screen_height // tile_height) * tile_height
    return (foodx, foody)

#check if player lost the game
def is_lost_game() -> bool:
    lost = player_pos[0] < 0 or player_pos[1] < 0 or player_pos[0] >= screen_width or player_pos[1] >= screen_height
    lost = lost or (player_pos in player_body)
    return lost

#print msg to screen
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [screen_width / 6, screen_height / 3])

#setup screen
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

#setup game
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
game_speed = 15
is_game_over = False
is_game_close = False

#in game object positions
player_body = [] 
player_pos = spawn_food()
food_pos = spawn_food()

#player movement offset
current_direction = (0, 0) 

def game_loop():
    global player_pos, food_pos, current_direction, is_game_over, is_game_close

    while not is_game_close:
        #input update
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_game_close = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and current_direction != (0, tile_height):
                    current_direction = (0, -tile_height)
                elif event.key == pygame.K_a and current_direction != (tile_width, 0):
                    current_direction = (-tile_width, 0)
                elif event.key == pygame.K_s and current_direction != (0, -tile_height):
                    current_direction = (0, tile_height)
                elif event.key == pygame.K_d and current_direction != (-tile_width, 0):
                    current_direction = (tile_width, 0)

        #logic update
        is_game_over = is_lost_game()

        if player_pos == food_pos:
            food_pos = spawn_food()
            player_body.append(player_pos)

        if len(player_body) > 0:
            for i in range(0, len(player_body) - 1):
                player_body[i] = player_body[i + 1]
            player_body[len(player_body) - 1] = player_pos

        #draw update
        screen.fill(backgroud_color)

        player_pos = add_positions(player_pos, current_direction)
        pygame.draw.rect(screen, food_color, [food_pos[0], food_pos[1], tile_width, tile_height])
        pygame.draw.rect(screen, player_color, [player_pos[0], player_pos[1], tile_width, tile_height])
        for x in player_body:
            pygame.draw.rect(screen, player_color, [x[0], x[1], tile_width, tile_height])
        pygame.display.update()

        #wait after game over
        while is_game_over:
            screen.fill(backgroud_color)
            message("Game over, press any key to close", text_color)
 
            pygame.display.update()
 
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    is_game_close = True
                    is_game_over = False

        clock.tick(game_speed)

#start game
game_loop()