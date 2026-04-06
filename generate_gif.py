import matplotlib.pyplot as plt
import imageio
from env import TrafficEnv
from models import Action

env = TrafficEnv()
env.reset()

frames = []

for _ in range(10):
    # choose best lane (IMPORTANT improvement)
    best_lane = env.lanes.index(max(env.lanes))
    env.step(Action(signal=best_lane))

    plt.bar(range(len(env.lanes)), env.lanes)
    plt.title("Traffic Simulation")
    plt.xlabel("Lane")
    plt.ylabel("Vehicles")

    plt.savefig("frame.png")
    plt.close()

    frames.append(imageio.imread("frame.png"))

imageio.mimsave("traffic_simulation.gif", frames, duration=0.5)

print("✅ GIF generated: traffic_simulation.gif")