from map import *
from car import *
from world import *
import pygame
import time

#TODO: For whatever reason, you cannot start a TrackBoundry on an Arc
#TODO: Observation State

WINDOW_SIZE = (750,750)
WHITE = (255, 255, 255)
GREEN = (21.2, 46.7, 17.6)

#Initialize PyGame
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()

# trackMap.shift(Point(-64,-50))
trackMap.scaleToWindowSize(WINDOW_SIZE, 50)
trackMap.shift(Point(150,0))

print(trackMap.Objectives.Segments)

racecar = Car()
world = World(screen, trackMap, racecar)



pygame.display.flip()

ThrottleForward = False
ThrottleBackward = False
SteerRight = False
SteerLeft = False
Throttle = 0
Steer = 0
Direction = 0
while True:


	events = pygame.event.get()
	for event in events:
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				SteerLeft = True
			if event.key == pygame.K_RIGHT:
				SteerRight = True
			if event.key == pygame.K_DOWN:
				ThrottleForward = True
			elif event.key == pygame.K_UP:
				ThrottleBackward = True
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				SteerLeft = False
			if event.key == pygame.K_RIGHT:
				SteerRight = False
			if event.key == pygame.K_DOWN:
				ThrottleForward = False
			elif event.key == pygame.K_UP:
				ThrottleBackward = False
	#Not holding both down
	if(SteerLeft and SteerRight): 
		SteerLeft = False
		SteerRight = False
	#Not holding both down
	if(ThrottleBackward and ThrottleForward):
		ThrottleForward=False
		ThrottleBackward=False
	if(not SteerLeft and not SteerRight):
		if(Steer>0):
			Steer-=1
		elif(Steer<0):
			Steer+=1
	if(not ThrottleBackward and not ThrottleForward):
		if(Throttle>0):
			Throttle-=1
		elif(Throttle<0):
			Throttle+=1
	if(SteerLeft):
		if (Steer>-8):
			Steer -=1
	if(SteerRight):
		if (Steer<8):
			Steer +=1
	if(ThrottleForward):
		if(Throttle<8):
			Throttle+=1
	if(ThrottleBackward):
		if(Throttle>-8):
			Throttle-=1
	if(Throttle>0):
		Direction = 1
	elif(Throttle<0):
		Direction=-1
	else:
		Direction=0

	racecar.drive(Throttle, Steer, Direction)
	world.update()


	pygame.display.flip()
	clock.tick(30)