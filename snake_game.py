# Import modules and libraries for the Snake Game
import pygame as pg
from random import randrange # for random position of snake and food

# initialize pygame
pg.init()

# Setting up the game window
width, height = 800, 600 # window size
screen = pg.display.set_mode((width, height)) # create (800 * 600) window
pg.display.set_caption('Snake Game') # set window title

# Setting up the size of the tiles
tile_size = 50 # 800/50 = 16 tiles in a row; 600/50 = 12 tiles in a column

# Function to get random position of snake and food
def get_random_position():
    item_range = (tile_size // 2, height - tile_size // 2, tile_size) # (25, 575, 50)
    return [randrange(*item_range), randrange(*item_range)]

# create an element for snake and food
element = pg.rect.Rect([0, 0, tile_size - 3, tile_size - 3]) # pg.rect.Rect(left, top, width, height), -2 is for the border
snake = element.copy() # create snake
snake.center = get_random_position() # object.center = (x, y) is a rect object method that sets the center point of the rectangle
food = element.copy() # create food
food.center = get_random_position()

# create a dictionary for snake movement, time and time_step for snake speed
snake_direction = (0, 0) # (x, y), (0, 0) means the snake is not moving, (0, -50) means the snake is moving up
time, time_step = 0, 100 # snake speed (time_step = 100 means the snake moves every 100 milliseconds)

# Snake eats food and grows in length
length = 1 # snake length
segments = [snake.copy()] # create a list for snake segments (its body)

# create a variable & font for points
points = 0
font = pg.font.SysFont('Arial', 24)

# create a game over variable
game_over = False

# infinite loop to keep the window open
while True:
    # update the screen color for erasing the footprint of the snake
    screen.fill('#343D35')

    # event listener
    for event in pg.event.get():
        # Quit game
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            exit()
        # Snake movement triggered by keyboard
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w or event.key == pg.K_UP:
                snake_direction = (0, -tile_size) # change the direction of the snake to (0, -50)
            if event.key == pg.K_s or event.key == pg.K_DOWN:
                snake_direction = (0, tile_size)
            if event.key == pg.K_a or event.key == pg.K_LEFT:
                snake_direction = (-tile_size, 0)
            if event.key == pg.K_d or event.key == pg.K_RIGHT:
                snake_direction = (tile_size, 0)

    # Draw snake body and food, the order must be between screen.fill() and pg.display.update()
    [pg.draw.rect(screen, '#A0E548', segment) for segment in segments] # draw the snake and its body
    pg.draw.rect(screen, '#E45F2B', food) # draw the food
 
    # Put the moving condition in the game_over == False condition, so that the snake will not move after the game is over
    if game_over == False:
        # Move snake
        time_now = pg.time.get_ticks() # get current time, get_ticks() returns the number of milliseconds
        if time_now - time > time_step:
            time = time_now
            snake.move_ip(snake_direction) # move_ip() is a rect object method that moves the rectangle in place
            # record the entire path of the snake
            segments.append(snake.copy()) # segments = [snake.copy(), snake.copy(), snake.copy(), ...]
            segments = segments[-length:] # keep the length of the snake
    pg.time.Clock().tick(60) # set frame rate to 60 fps (遊戲偵數)

    # Snake eats food
    if snake.center == food.center:
        food.center = get_random_position() # the food is randomly generated again
        length += 1 # the snake grows in length
        points += 1 # get 1 point
        # make the snake move faster—
        # time_step -= 5 

    # show your points on the screen
    text = font.render(f'Points: {points}', True, 'white')
    screen.blit(text, (20, 20))
        # print the text you want on the screen
        # screen.blit(font.render(f'Hello everyone', True, 'white'), (50,50))

    # Set borders and self-eating
    # define the self_eating variable
    self_eating = pg.Rect.collidelist(snake, segments[:-1]) != -1  # Rect.collidelist(list) returns the index of the first collision with the list, -1 means no collision
    # if the snake hits the border or eats itself, the game will be reset
    if snake.left < 0 or snake.right > width or snake.top < 0 or snake.bottom > height or self_eating:
        game_over = True
        # show gameover on the screen
        game_over_font = pg.font.SysFont('Arial', 60)
        game_over_text = game_over_font.render('Game Over', True, 'white')
        # show the text in the center of the screen
        screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - game_over_text.get_height() // 2))
        pg.display.update()
        
        # keydown any key to restart the game
        if pg.event.wait().type == pg.KEYDOWN:
            snake.center, food.center = get_random_position(), get_random_position() # reset the snake and food
            length, snake_direction, points = 1, (0, 0), 0 # reset the snake length, direction, and points
            segments = [snake.copy()] # reset the snake segments
            game_over = False # reset the game_over variable

    # Update the screen
    pg.display.update()