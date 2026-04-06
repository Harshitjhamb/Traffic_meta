from fastapi import FastAPI, Body
from env import TrafficEnv
from models import Action

app = FastAPI()
env = TrafficEnv()

@app.get("/")
def home():
    return {"message": "Traffic OpenEnv API running"}

@app.post("/openenv/reset")
def reset():
    global env
    env = TrafficEnv()
    obs = env.reset()
    return {
        "observation": obs.dict(),
        "reward": 0.0,
        "done": False,
        "info": {}
    }

@app.post("/openenv/step")
def step(action: Action = Body(...)):
    result = env.step(action)
    return {
        "observation": result.observation.dict(),
        "reward": result.reward,
        "done": result.done,
        "info": result.info
    }

@app.get("/openenv/validate")
def validate():
    return {
        "name": "traffic-env",
        "tasks": ["easy", "medium", "hard"],
        "status": "ok"
    }
