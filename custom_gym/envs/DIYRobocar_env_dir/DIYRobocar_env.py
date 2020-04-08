#Gym Imports
import gym
from gym import spaces

#Custom Classes and Helpers Import
from envs.DIYRobocar_env_dir.map import *
from envs.DIYRobocar_env_dir.car import *
from envs.DIYRobocar_env_dir.world import *

#External Libs Imports
import numpy as np
import pygame
import time

WINDOW_SIZE = (750,750)

class DIYRobocarEnv(gym.Env):
	def __init__(self):
		#Initialize PyGame
		# pygame.init()
		# self.clock = pygame.time.Clock()
		# self.screen = pygame.display.set_mode(WINDOW_SIZE)
		donkeyTrack = loadTrack()
		donkeyTrack.scaleToWindowSize(WINDOW_SIZE, 50)
		donkeyTrack.shift(Point(150,0))
		self.racecar = Car()
		self.world = World(False, WINDOW_SIZE, donkeyTrack, self.racecar)
		# pygame.display.flip()
		# self.clock.tick(30)


		# 					#Throttle           #Steer
		# self.low = np.array([self.min_throttle, self.min_steer], dtype=np.float32)
		# self.high = np.array([self.max_throttle, self.max_steer], dtype=np.float32)

		# self.action_space = spaces.Box(self.low, self.high, dtype=np.float32)
		# Example for using image as input:
		# self.observation_space = spaces.Box(low=0, high=255, shape=(HEIGHT, WIDTH, N_CHANNELS), dtype=np.uint8)

		#action space[0]: 0= decrease throttle, 1=maintain throttle, 2= increase throttle
		#action space[1]: 0= decrease steer, 1=maintain steer, 2=increase steer
		self.action_space = spaces.MultiDiscrete([ 3, 3 ])

	def step(self, action, episode):
		assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))
		throttle_change, steer_change = action

		self.racecar.drive(throttle_change-1, steer_change-1)

		done = self.world.update()
		self.world.DisplayWindow.Draw(episode)
		reward = self.world.getReward()
		state = self.world.getState()
		# state = self.world.DisplayWindow.Draw(episode)
		# pygame.event.wait()
		# if state != None: assert self.observation_space.contains(state), "%r (%s) invalid" % (state, type(state))
		#return observation space, reward, done info
		return state, reward, done, {}

	def reset(self, episode):
		self.racecar = Car()
		donkeyTrack = loadTrack()
		donkeyTrack.scaleToWindowSize(WINDOW_SIZE, 50)
		donkeyTrack.shift(Point(150,0))
		self.world = World(True, WINDOW_SIZE, donkeyTrack, self.racecar)
		self.world.DisplayWindow.Draw(episode)
		return (int(self.racecar.X/35), int(self.racecar.Y/35), int(self.racecar.Theta/36))

		# return self.world.DisplayWindow.Draw(episode)

	def sample_action(self):
		action = np.random.randint(3, size=2)
		# action = np.multiply((np.subtract(np.random.rand(2), np.array([0,.5]))),(np.array([8,16])))
		return action

	def getStateSpaceSize(self):
		return (int(WINDOW_SIZE[0]/35), int(WINDOW_SIZE[1]/35), int(360/36))

	def getActionSpaceSize(self):
		return (self.action_space.nvec[0], self.action_space.nvec[1])