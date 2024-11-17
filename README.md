# Snake Game by Pygame
**Pygame** is a set of [Python](http://www.python.org/) modules designed for writing video games. Pygame adds functionality on top of the excellent [SDL](http://www.libsdl.org/) library.  Here are the steps to create a Snake Game in Python:

### Install Pygame

```python
python3 pip install pygame
```

PyGame is a module for Python to create games. It allows developers to add elements such as text, graphics, sound, etc. in a simpler way and to handle events to develop games.

### **Pygame Module used in Snake Game**

`pygame.display` : pygame module to control the display window and screen module
`pygame.Rect` : Rect data type, used to locate the position of the rectangular space and can be used to detect whether the object collides
`pygame.event` : event module, used to handle user-triggered events, including custom events

`pygame.draw` : pygame module for drawing shapes on the screen
`pygame.font` : text module, used to display text, can be used to display dashboard data
`pygame.time` : time module, including controlling the iteration rate of the game loop to ensure that the feedback will not disappear too fast

### Import Module

```python
# import the module and libraries for the Snake Game
import pygame as pg
from random import randrange # for random position of snake and food
```

### 1. Create the game screen, use infinite loop running the game, track event

```python
##### Start of data layer #####

# create the game screen
width, height = 800, 600
screen = pg.display.set_mode((width, height)) # create (800 * 600) window
pg.display.set_caption('Snake Game') # set window title

##### End of data layer #####

# infinite loop to keep window running and tracking
while True:
	# event listener
	for event in pg.event.get():
		# Press ESC and [X] to quit game
		if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
			exit()
```
![Untitled](https://github.com/jy09567824/snake-game-pygame/blob/main/images/img_07.png)

### 2. Create grid system

Due to the game mechanism of Snake Game, we need to create a grid system on the screen:
![Untitled](https://github.com/jy09567824/snake-game-pygame/blob/main/images/img_01.png)

In data layer:

```python
# Setting up the size of the tiles
tile_size = 50 

# Why choose 50? 
# 800/50 = 16 tiles in a row; 
# 600/50 = 12 tiles in a column
```

### 3. Create the main elements of the game: snake, food

In data layer:

```python
# pg.rect.Rect(left, top, width, height). -3 is for the border
element = pg.rect.Rect([0, 0, tile_size - 3, tile_size - 3])

# Function to get random position of snake and food
def get_random_position():
    range = (tile_size // 2, height - tile_size // 2, tile_size) # (25, 575, 50)
    return [randrange(*range), randrange(*range)]

# create snake
snake = element.copy()
# object.center = (x, y) is a rect object method that sets the center point of the rectangle
snake.center = get_random_position()

# create food
food = element.copy() 
food.center = get_random_position()
```

Then add the following code into the While Loop created at the beginning

```python
# add the following code within the While Loop created at the beginning
while True:
	...
	...
	# Draw snake and food, the order must be between screen.fill() and pg.display.update()
  pg.draw.rect(screen, '#A0E548', snake)
  pg.draw.rect(screen, '#E45F2B', food)
	# update the screen
  pg.display.update()
```

![Untitled](https://github.com/jy09567824/snake-game-pygame/blob/main/images/img_02.png)

### 4. Set the snake movement: up, down, left, right

In data layer:

```python
# create a dictionary for snake movement, time and time_step for snake speed
snake_direction = (0, 0) # (x, y), (0, 0) means the snake is not moving, (0, -50) means the snake is moving up
time, time_step = 0, 100 # snake speed (time_step = 100 means the snake moves every 100 milliseconds)
```

In while loop and fop loop:

```python
# add the following code within the While & For Loops created at the beginning
while True:
	...
	...
	...
	# update the screen color for erasing the footprint of the snake
  screen.fill('#343D35')
	for event in pg.event.get():
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
	# set the tasks to be executed every time milliseconds
    time_now = pg.time.get_ticks() # get the time, get_ticks() returns the number of milliseconds
    if time_now - time > time_step:
        time = time_now
        snake.move_ip(snake_direction) # move_ip() is a rect object method that moves the rectangle in place
		pg.time.Clock().tick(60) # set the frame rate to 60 frames per second
```

![Now you can move the snake by keydown up, down, left, right](https://github.com/jy09567824/snake-game-pygame/blob/main/images/img_03.png)

Now you can move the snake by keydown up, down, left, right

If there is any element want to show on the screen, you must put it between `screen.fill()` and `pg.display.update()`

### 4. Add the points system

Add pg.init() above the data layer:

```python
# initialize pygame
pg.init()
```

In data layer:

```python
# create a variable & font for points
points = 0
font = pg.font.SysFont('Arial', 24)
```

In while loop:

```python
# add the following code within the While Loop created at the beginning
while True:
	...
	...
	...
	# show your points on the screen
	text = font.render(f'Points: {points}', True, 'white')
	screen.blit(text, (20, 20))
```

![Points show on the left-top](https://github.com/jy09567824/snake-game-pygame/blob/main/images/img_04.png)

Points show on the left-top

### 5. Set when the snake eats food

There are following 3 parts we need to set:

1. When the snake eats the food (position of snake the same as food)
2. food is randomly generated again
3. snake grows in length (points + 1 as well)

In data layer:

```python
# Snake eats food and grows in length
length = 1 # snake length
segments = [element.copy()] # create a list for snake segments (its body)
```

In While Loop:

```python
while True:
	...
	...
	...
	# Snake eats food
	if snake.center == food.center:
		food.center = get_random_position() # the food is randomly generated again
    length += 1 # the snake grows in length
    points += 1 # get 1 point
```

To record the entire path of the snake, add the following,  bolding code into if condition:

```python
if time_now - time > time_step: 
	time = time_now
	snake.move_ip(snake_direction) # move_ip() is a rect object method that moves the rectangle in place
	
	**# record the entire path of the snake by appending the snake.copy() to the segments list
  segments.append(snake.copy()) # segments = [snake.copy(), snake.copy(), snake.copy(), ...]
  segments = segments[-length:] # keep the length of the snake**
```

![Untitled](https://github.com/jy09567824/snake-game-pygame/blob/main/images/img_05.png)

### 6. Set Game Over condition

1. Snake self-eating, we can use `Rect.collidelist(a, b)` to check the collision between a, b
2. Snake hits the borders
3. Show the Game Over Text
4. Press any button to reset the game

In While Loop:

```python
# create a game over variable
**game_over = False**

while True:
	...
	...
	...
	**# Put the moving condition in the game_over == False condition, so that the snake will not move after the game is over
	if game_over == False:**
		# Move snake
	  time_now = pg.time.get_ticks() # get the time, get_ticks() returns the number of milliseconds
    if time_now - time > time_step:
        time = time_now
        snake.move_ip(snake_direction) # move_ip() is a rect object method that moves the rectangle in place
        # record the entire path of the snake
        segments.append(snake.copy()) # segments = [snake.copy(), snake.copy(), snake.copy(), ...]
        segments = segments[-length:] # keep the length of the snake
	...
	...
	# Set borders and self-eating
	# define the self_eating variable
	self_eating = pg.Rect.collidelist(snake, segments[:-1]) != -1  # Rect.collidelist(list) returns the index of the first collision with the list, -1 means no collision
    
	# if the snake hits the border or eats itself, the game will be reset
	if snake.left < 0 or snake.right > width or snake.top < 0 or snake.bottom > height or self_eating:
		**game_over = True**
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
      **game_over = False # reset the game_over variable**
```

![Finished!](https://github.com/jy09567824/snake-game-pygame/blob/main/images/img_06.png)

Finished!
