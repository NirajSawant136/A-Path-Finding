import pygame
import random
import time

pygame.init()

global size
size = 30
cell_size = 20
WIDTH, HEIGTH = size*cell_size, size*cell_size

MAZE = pygame.display.set_mode((WIDTH, HEIGTH))
pygame.display.set_caption("A* Path-Finding Algorithm")

WHITE = (255, 255, 255)
BLACK = (0,0,0)

class cell(object):
	"""docstring for cell"""
	def __init__(self, pos, f):
		self.pos = pos
		self.f = f
		self.g = 0
		self.h = 0
		self.source = pos
		self.unblocked = True

	def setg(self, g):
		self.g = g

	def g(self):
		return self.g

	def seth(self, target):
		return abs(self.pos[0] - target[0]) + abs(self.pos[1] - target[1])

	def setf(self):
		self.f = self.g + self.h

	def isUnblocked(self, unblocked):
		self.unblocked = unblocked

def index(pos):
	return pos[0]*size + pos[1]

def pos(index):
	y = index % size
	x = (index - y)//size
	return (x, y)

def Successors(pos):
	pos1, pos2, pos3, pos4 = None, None, None, None

	if pos[0] + 1 < size:
		pos1 = (pos[0] + 1, pos[1])

	if pos[0] - 1 >= 0:
		pos2 = (pos[0] - 1, pos[1])

	if pos[1] + 1 < size:
		pos3 = (pos[0], pos[1] + 1)

	if pos[1] - 1 >= 0:
		pos4 = (pos[0], pos[1] - 1)

	return [pos1, pos2, pos3, pos4]

def dist(pos1, pos2):
	return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

global cells

cells = []
for i in range(size):
	for j in range(size):
		cells.append(cell((i, j), 100))

source = (0, 0)
target = (size-1, size-1)
# cells[index(target)].source = (4,1)

global openList, closedList

openList = []
closedList = []

# blockedCells = [(1, 0), (0, 2), (1, 2), (3, 0), (7, 2), (7, 1), (8, 4), (5, 2), (4, 2), (2, 4)]
blockedCells = []

Cell = [cell.pos for cell in cells]
if source in Cell:
	Cell.remove(source)
if target in Cell:
	Cell.remove(target)

for i in range(300):
	blockedCells.append(random.choice(Cell))

for cell in blockedCells:
	cells[index(cell)].isUnblocked(False)

MAZE.fill(WHITE)
pygame.draw.rect(MAZE, (50,250,50), (source[1]*cell_size, source[0]*cell_size, cell_size, cell_size), 0)
pygame.draw.rect(MAZE, (250,50,50), (target[1]*cell_size, target[0]*cell_size, cell_size, cell_size), 0)
pygame.display.update()

for cell in blockedCells:
	pygame.draw.rect(MAZE, (50, 50, 50), (cell[1]*cell_size, cell[0]*cell_size, cell_size, cell_size), 0)
	pygame.display.update()

for i in range(size):
	pygame.draw.line(MAZE, (0,0,0), (0, i*cell_size), (size*cell_size, i*cell_size))
	pygame.draw.line(MAZE, (0,0,0), (i*cell_size, 0), (i*cell_size, size*cell_size))
	pygame.display.update()

openList.append(cells[index(source)])
openList[0].f = 0

search = True
while len(openList) > 0 and search:

	q = next(cell.pos for cell in openList if cell.f == min(cell.f for cell in openList))

	openList.remove(cells[index(q)])

	successors = Successors(q)

	found = False
	for successor in successors:
		
		if successor != None:
			
			cells[index(successor)].g = cells[index(q)].g + dist(successor, q)
			cells[index(successor)].seth(target)
			
			f_old = cells[index(successor)].f
			cells[index(successor)].f = cells[index(successor)].g + cells[index(successor)].h
			f_new = cells[index(successor)].f
			if f_new < f_old:
				cells[index(successor)].source = q

			if cells[index(successor)].unblocked:
				
				if successor == target:
					search = False
					found = True

				else:
					notSkipped = True
					for cell in openList:
						if cell.pos == successor and cell.f < cells[index(successor)].f:
							notSkipped = False

					if notSkipped:
						notSkipped = True
						for cell in closedList:
							if cell.pos == successor and cell.f < cells[index(successor)].f:
								notSkipped = False

						if notSkipped and cells[index(successor)] not in openList:
							openList.append(cells[index(successor)])

	closedList.append(cells[index(q)])
	if found:
		closedList.append(cells[index(target)])

src = closedList[len(closedList)-1].source
print(src)
path = []

while src != source:
	path.append(src)
	src = cells[index(src)].source

print("path -> {}".format(path))
print("Length -> {}".format(len(path)))
print("openList -> {}".format(len(openList)))

# MAZE.fill((255, 255, 255))
# pygame.draw.rect(MAZE, (50,250,50), (source[1]*cell_size, source[0]*cell_size, cell_size, cell_size), 0)
# pygame.draw.rect(MAZE, (250,50,50), (target[1]*cell_size, target[0]*cell_size, cell_size, cell_size), 0)
# pygame.display.update()

for cell in path:
	time.sleep(0.05)
	pygame.draw.rect(MAZE, (50,50,250), (cell[1]*cell_size, cell[0]*cell_size, cell_size, cell_size), 0)
	pygame.draw.rect(MAZE, BLACK, (cell[1]*cell_size, cell[0]*cell_size, cell_size, cell_size), 1)
	pygame.display.update()

# for cell in blockedCells:
# 	pygame.draw.rect(MAZE, (50, 50, 50), (cell[1]*cell_size, cell[0]*cell_size, cell_size, cell_size), 0)
# 	pygame.display.update()

for i in range(size):
	pygame.draw.line(MAZE, (0,0,0), (0, i*cell_size), (size*cell_size, i*cell_size))
	pygame.draw.line(MAZE, (0,0,0), (i*cell_size, 0), (i*cell_size, size*cell_size))
	pygame.display.update()

run = True
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			run = False