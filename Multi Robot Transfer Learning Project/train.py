import random
import numpy as np
from learning import makeMove
from learning import getReward
from IPython.display import clear_output
import sensor

def training(model):
    epochs = 3000 #number of trials
    gamma = 0.975 #make gamma high as it may take several moves to get to the goal
    epsilon = 1
    batchSize = 40 
    buffer = 80  #replay memory frame size
    replay = []   #replay empry array
    #stores tuples of (State : S, Action : A, Reward : R, new State : S')
    h = 0
    
    
    #goal position is reinitialized for each epoch
    for i in range(epochs): 
        status = 1
        #while game still in progress
        while(status == 1):
            #We are in state S
            #get feature mop, car position, car orientation, sensor_collision_distances goal position for the current state
            state = sensor.getCurrentState()
            
            #Let's run our Q function on S to get Q values for all possible actions
            qval = model.predict(state.reshape(1,64), batch_size=1)
            
            if (random.random() < epsilon): #choose random action
                action = np.random.randint(0,4)
            else: #choose best action from Q(s,a) values
                action = (np.argmax(qval))
            
            #Take action, observe new state S'
            new_state = makeMove(state, action)
            
            #Observe reward
            reward = getReward(new_state)
    
            #Experience replay storage
            if (len(replay) < buffer): #if buffer not filled, add to it
                replay.append((state, action, reward, new_state))
            else: #if buffer full, overwrite old values
                if (h < (buffer-1)):
                    h += 1
                else:
                    h = 0
                replay[h] = (state, action, reward, new_state)
                #randomly sample our experience replay memory
                minibatch = random.sample(replay, batchSize)
                X_train = []
                y_train = []
                for memory in minibatch:
                    #Get max_Q(S',a)
                    old_state, action, reward, new_state = memory
                    old_qval = model.predict(old_state.reshape(1,64), batch_size=1)
                    newQ = model.predict(new_state.reshape(1,64), batch_size=1)
                    maxQ = np.max(newQ)
                    y = np.zeros((1,4))
                    y[:] = old_qval[:]
                    if reward == -1: #non-terminal state
                        update = (reward + (gamma * maxQ))
                    else: #terminal state
                        update = reward
                    y[0][action] = update
                    X_train.append(old_state.reshape(64,))
                    y_train.append(y.reshape(4,))
    
                X_train = np.array(X_train)
                y_train = np.array(y_train)
                print("Game #: %s" % (i,))
                model.fit(X_train, y_train, batch_size=batchSize, nb_epoch=1, verbose=1)
                state = new_state
            if reward != -1: #if reached terminal state, update game status
                status = 0
            clear_output(wait=True)
        if epsilon > 0.1:    #decrement epsilon over time
            epsilon -= (1/epochs)