import numpy as np

class EpGrNonStatAgent:
    def __init__(self, n_arms, epsilon, alpha):
        self.n_arms = n_arms
        self.epsilon = epsilon
        self.alpha = alpha
        self.q_values = np.zeros(n_arms)  

    def select_action(self):
        if np.random.rand() < self.epsilon:  
            return np.random.randint(self.n_arms)
        else: 
            return np.argmax(self.q_values)

    def update_q_value(self, action, reward):
        self.q_values[action] += self.alpha * (reward - self.q_values[action])

def band_nonstat(action, true_rewards):
    reward = np.random.randn() + true_rewards[action]
    return reward
n_arms = 10
n_steps = 10000
epsilon = 0.1
alpha = 0.1
true_rewards = np.zeros(n_arms)  
agent = EpGrNonStatAgent(n_arms, epsilon, alpha)

for step in range(n_steps):
    action = agent.select_action()
    reward = band_nonstat(action, true_rewards)
    agent.update_q_value(action, reward)
    true_rewards += np.random.normal(0, 0.01, n_arms) 
