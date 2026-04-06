import random
from models import Observation, Action, StepResult
class TrafficEnv:
    def __init__(self):
        self.lanes = [5, 3, 7, 2]
        self.signal = 0
        self.steps = 0
    def reset(self):
        self.lanes = [5, 3, 7, 2]
        self.signal = 0
        self.steps = 0
        return Observation(lanes=self.lanes, current_signal=self.signal)
    def state(self):
        return Observation(lanes=self.lanes, current_signal=self.signal)
    def step(self, action: Action):
        self.signal = action.signal
        self.lanes[self.signal] = max(0, self.lanes[self.signal] - 2)
        self.lanes = [x + random.randint(0, 3) for x in self.lanes]
        reward = -sum(self.lanes)
        self.steps += 1
        done = self.steps > 20
        return StepResult(
            observation=Observation(lanes=self.lanes, current_signal=self.signal),
            reward=reward,
            done=done,
        )