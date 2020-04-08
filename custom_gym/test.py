import gym
import envs
import numpy as np
import random
import time
from PIL import Image

FILENAME = "./QTables/QTable_ep55000_reward_984.4000000000004.npy"

env= gym.make('DIYRobocarEnv-v0')



q_table = np.load(FILENAME)

num_episodes = 10000
max_steps_per_episode = 1000
save_every = 50

learning_rate = 0.1
discount_rate = 0.99
total_reward =0
state = env.reset(0)

done = False
for step in range(max_steps_per_episode): 
	start = time.time()
	action = np.array(np.unravel_index(np.argmax(q_table[state[0],state[1], state[2],:], axis=None), q_table[state[0],state[1], state[2],:].shape))
	#Take the Decided action
	observation, reward, done, info = env.step(action, 0)
	discrete_observation = (int(observation[0]/35)-1, int(observation[1]/35)-1, int(observation[2]/10)-1)
    # Set new state
	state = discrete_observation
    # Add new reward 
	total_reward += reward
	if done == True: 
		break
	end = time.time()
	print(end-start)
print(total_reward)


