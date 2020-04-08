from map import *
from car import *
from world import *
import time

#TODO: For whatever reason, you cannot start a TrackBoundry on an Arc
#TODO: Observation State

WINDOW_SIZE = (750,750)
WHITE = (255, 255, 255)
GREEN = (21.2, 46.7, 17.6)

trackMap = loadTrack()
# trackMap.shift(Point(-64,-50))
trackMap.scaleToWindowSize(WINDOW_SIZE, 50)
trackMap.shift(Point(150,0))


racecar = Car()
world = World(True, WINDOW_SIZE, trackMap, racecar)


ThrottleForward = False
ThrottleBackward = False
SteerRight = False
SteerLeft = False
Throttle = 0
Steer = 0
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
			Steer=0
	if(not ThrottleBackward and not ThrottleForward):
			Throttle=0
	if(SteerLeft):
			Steer =-1
	if(SteerRight):
			Steer =1
	if(ThrottleForward):
			Throttle=1
	if(ThrottleBackward):
			Throttle=-1

	start = time.time()
	racecar.drive(Throttle, Steer)
	world.update()
	world.DisplayWindow.Draw(0)
	end = time.time()
	print(end-start)
