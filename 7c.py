import numpy as np

class EpGrAgent:
    def __init__(self, n_arms, epsilon):
        self.n_arms = n_arms
        self.epsilon = epsilon
        self.q_values = np.zeros(n_arms)  
        self.action_counts = np.zeros(n_arms)  

    def sel_act(self):
        if np.random.rand() < self.epsilon:  
            return np.random.randint(self.n_arms)
        else:  
            return np.argmax(self.q_values)

    def update_qval(self, action, reward):
        self.action_counts[action] += 1
        self.q_values[action] += (reward - self.q_values[action]) / self.action_counts[action]

binband = [0.1, 0.2] 
agent = EpGrAgent(n_arms=2, epsilon=0.1)

for _ in range(1000):  
    action = agent.sel_act()
    reward = np.random.rand() < binband[action] 
    agent.update_qval(action, reward)

print("Estimated Q values:", agent.q_values)
