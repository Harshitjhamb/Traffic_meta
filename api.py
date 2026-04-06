from fastapi import FastAPI
from env import TrafficEnv
from models import Action

app = FastAPI()
env = TrafficEnv()

@app.get("/")
def home():
    return {"message": "Traffic API running"}

@app.post("/openenv/reset")
def reset():
    global env
    env = TrafficEnv()
    return {"lanes": env.lanes}

@app.post("/openenv/step")
def step():
    env.step(Action(signal=0))
    return {
        "lanes": env.lanes,
        "total_cars": sum(env.lanes)
    }
