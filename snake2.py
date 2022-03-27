# Author: Eric Romano
# Snake game built with pygame

import pygame, time, random

class Player(object):
	def __init__(self,grid_x, grid_y):
		self.body = []
		self.head = [grid_x, grid_y]
		self.body.append(self.head)

	def draw(self, square, color):
		'''draws the squares to the screen by converting the grid location to the pixels location'''
		(pix_y, pix_x) = grid[square[1]][square[0]]
		rect = pygame.Rect(pix_x, pix_y, 30, 30)
		pygame.draw.rect(screen, color, rect)

	def move(self, direction):
		'''moves the squares that make up the body of the player'''
		for square in self.body[::-1]:
			if square != self.head:
				index = self.body.index(square)
				square[0] = self.body[index-1][0]
				square[1] = self.body[index-1][1]

				self.draw(square, blue)

		if direction == 'up':
			self.head[1] -= 1
		if direction == 'down':
			self.head[1] += 1
		if direction == 'left':
			self.head[0] -= 1
		if direction == 'right':
			self.head[0] += 1

		if self.head[0] > 16 or self.head[0] < 0:
			self.game_over()
		if self.head[1] > 14 or self.head[1] < 0:
			self.game_over()
		if self.head in self.body[1:]:
			self.game_over()

		self.draw(self.head, maroon)

		key = pygame.key.get_pressed()

		if key[pygame.K_UP] and direction != 'down':
			direction = 'up'
		if key[pygame.K_DOWN] and direction != 'up':
			direction = 'down'
		if key[pygame.K_LEFT] and direction != 'right':
			direction = 'left'
		if key[pygame.K_RIGHT] and direction != 'left':
			direction = 'right'

		return direction

	def get_direction(self, direction):
		self.direction = direction
		#print(self.direction)
		return direction

	def add_square(self):
		'''Adds a square to the snake body if the snake eats food'''
		self.body.append([0,0])
		self.body[-1][0] = self.body[-2][0]
		self.body[-1][1] = self.body[-2][1]
				
		if self.direction == 'up': # head touches food coming up
			self.body[-1][1] += 1
		if self.direction == 'down': # head touchs food coming down
			self.body[-1][1] -= 1
		if self.direction == 'left':
			self.body[-1][0] += 1
		if self.direction == 'right':
			self.body[-1][0] -= 1

	def game_over(self):
		print('Game Over')
		print('Player score: ', len(player.body))
		pygame.quit()
		quit()

class Food(object):
	def __init__(self, grid_x, grid_y):
		self.grid_x = grid_x
		self.grid_y = grid_y
	
	def draw(self, surface):
		(self.pix_y, self.pix_x) = grid[self.grid_y][self.grid_x]
		self.rect = pygame.Rect(self.pix_x, self.pix_y, 30, 30)
		pygame.draw.rect(surface, red, self.rect)

	def move(self, body):
		'''relocates the food to a new location on the grid'''
		x = random.randint(0,16)
		y = random.randint(0,14)
		if [x,y] not in body and [x,y] != [self.grid_x,self.grid_y]:
			self.grid_x = x
			self.grid_y = y

pygame.init()

screen_width = 510
screen_height = 450

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
light_green = (0,255,0)
green = (0,210,0)
maroon = (128,0,0)
blue = (0,0,255)

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('snake')
clock = pygame.time.Clock()

columns = 17
rows = 15
cell_width = 30
cell_height = 30

grid = []
for row in range(rows):
	grid.append([])
	for col in range(columns):
		grid[row].append((int(row*(screen_height/rows)), int(col*(screen_width/columns))))

# grid_x corresponds to col
# grid_y corresponds to row
player = Player(2,6) # starting grid position (grid_x, grid_y)
food = Food(8,6)

game_over = False
direction = 'right'


# Main Game Loop
while not game_over:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game_over = True
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				game_over = True

	for row in range(len(grid)):
		for col in range(len(grid[row])):
			cell = pygame.Rect(col*(screen_width/columns),row*(screen_height/rows),cell_width,cell_height)
			if row % 2 == 0:
				if col % 2 == 0:
					cell_color = light_green
				else:
					cell_color = green
			elif row % 2 != 0:
				if col % 2 == 0:
					cell_color = green
				else:
					cell_color = light_green
			pygame.draw.rect(screen, cell_color, cell)
	

	direction = player.get_direction(direction)
	new_direction = player.move(direction)
	direction = new_direction

	food.draw(screen)

	if (player.head[0], player.head[1]) == (food.grid_x, food.grid_y):
		player.add_square()
		food.move(player.body)

	pygame.display.update()
	pygame.time.delay(100)
	clock.tick(60)
