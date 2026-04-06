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

    return {
        "observation": {
            "lanes": env.lanes
        },
        "reward": 0.0,
        "done": False,
        "info": {}
    }
    
from fastapi import Body
@app.post("/openenv/step")
def step(action: Action = Body(...)):
    env.step(action)

    return {
        "observation": {
            "lanes": env.lanes
        },
        "reward": 1.0,  # or your logic
        "done": False,
        "info": {}
    }
