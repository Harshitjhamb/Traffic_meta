from pydantic import BaseModel
from typing import List
class Observation(BaseModel):
    lanes: List[int]
    current_signal: int
class Action(BaseModel):
    signal: int  
class StepResult(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: dict = {}