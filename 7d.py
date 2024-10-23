import numpy as np
import random

class Bandit:
    def __init__(self, p):
        self.p = p
        self.q = [0.0, 0.0]
        self.n = [0, 0]
    
    def reward(self, a):
        return 1 if random.random() < self.p[a] else 0
    
    def select(self, e):
        return random.randint(0, 1) if random.random() < e else np.argmax(self.q)
    
    def update(self, a, r):
        self.n[a] += 1
        self.q[a] += (r - self.q[a]) / self.n[a]

def run(b, e, steps):
    total_r = 0
    rewards = []
    
    for _ in range(steps):
        a = b.select(e)
        r = b.reward(a)
        b.update(a, r)
        total_r += r
        rewards.append(total_r)
    
    return rewards

p_true = [0.8, 0.6]
b = Bandit(p_true)
eps = 0.1
steps = 1000

rewards = run(b, eps, steps)

print(f"Action counts: {b.n}")
print(f"Estimated action values: {b.q}")
print(f"Total reward after {steps} steps: {rewards[-1]}")
