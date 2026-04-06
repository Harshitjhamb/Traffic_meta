from env import TrafficEnv
from models import Action
env = TrafficEnv()
obs = env.reset()
print("Initial:", obs)
for i in range(10):
    action = Action(signal=i % 4)  # switch lanes
    result = env.step(action)
    print(f"\nStep {i+1}")
    print("Lanes:", result.observation.lanes)
    print("Signal:", result.observation.current_signal)
    print("Reward:", result.reward)