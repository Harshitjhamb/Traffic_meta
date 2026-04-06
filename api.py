from fastapi import FastAPI
from env import TrafficEnv
from models import Action

app = FastAPI()
env = TrafficEnv()

@app.post("/reset")
def reset():
    global env
    env = TrafficEnv()
    return {"lanes": env.lanes}

@app.post("/step")
def step():
    env.step(Action(signal=0))
    return {
        "lanes": env.lanes,
        "total_cars": sum(env.lanes)
    }
