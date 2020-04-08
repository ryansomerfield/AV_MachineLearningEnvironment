import gym
import envs
import numpy as np
import random
startnum = 0
FILENAME = './QTables/QTable_ep65000_reward_-3.399999999999835.npy'

env= gym.make('DIYRobocarEnv-v0')

action_space_size = env.getActionSpaceSize()
state_space_size = env.getStateSpaceSize()

a,b,c = state_space_size
d,e = action_space_size

if FILENAME != None:
	q_table = np.load(FILENAME)
else:
	q_table = np.random.rand(a,b,c,d,e)*-1

num_episodes = 1000000
max_steps_per_episode = 100000
save_every = 5000

learning_rate = 0.25
discount_rate = 0.60

exploration_rate = [1]*13
max_exploration_rate = 1
min_exploration_rate = 0.01
exploration_decay_rate = 0.00001



rewards_all_episodes = []
# Q-learning algorithm
for episode in range(startnum, num_episodes):
	
    # initialize new episode params
	state = env.reset(episode)
	done = False
	total_reward = 0
	objective = 0
	for step in range(max_steps_per_episode): 
        # Exploration-exploitation trade-off
		exploration_rate_threshold = random.uniform(0, 1)
		if exploration_rate_threshold > exploration_rate[objective]:
			action = np.array(np.unravel_index(np.argmax(q_table[state[0],state[1], state[2],:], axis=None), q_table[state[0],state[1], state[2],:].shape))
		else:
			action = env.sample_action()

		#Take the Decided action
		observation, reward, done, info = env.step(action, episode)
		discrete_observation = (int(observation[0]/35)-1, int(observation[1]/35)-1, int(observation[2]/10)-1)

		discrete_action = (int(action[0]), int(action[1]))
        # Update Q-table
		q_table[state[0], state[1], state[2], discrete_action[0], discrete_action[1]] = q_table[state[0], state[1], state[2], discrete_action[0], discrete_action[1]] * (1 - learning_rate) + \
		learning_rate * (reward + discount_rate * np.max(q_table[discrete_observation[0], discrete_observation[1], discrete_observation[2], :]))
        # Set new state
		state = discrete_observation
        # Add new reward        
		total_reward += reward

		if(reward == (200-.1)):
			#move on to next objective
			objective +=1



		if(total_reward<-1000):
			done=True
        #Check Done
		if done == True: 
			break
    # Exploration rate decay  
	exploration_rate[objective] = min_exploration_rate + \
	(max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate*episode)

	# Add current episode reward to total rewards list
	rewards_all_episodes.append(total_reward)
	print(episode, total_reward, objective, exploration_rate[objective])
	if not episode % save_every:
		np.save(f"./QTables2/QTable_ep{episode}_reward_{total_reward}",q_table)
# print(rewards_all_episodes)
np.save('QTable',q_table)
save = np.array(rewards_all_episodes)
np.savetxt('QRewards.txt', save)