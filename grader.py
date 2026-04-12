from env import TrafficEnv

def grade(task: str) -> float:
    env = TrafficEnv()
    env.reset()
    
    total_reward = 0.0
    
    if task == "easy":
        steps = 5
    elif task == "medium":
        steps = 10
    else:  # hard
        steps = 20

    from models import Action
    for _ in range(steps):
        # Greedy: pick lane with most cars
        action = Action(signal=env.lanes.index(max(env.lanes)))
        result = env.step(action)
        total_reward += result.reward

    # Normalize to strictly (0, 1)
    # reward is negative (penalty), so we convert to positive score
    max_possible = steps * 20  # worst case ~20 cars per step
    raw = abs(total_reward) / max_possible
    # Clamp strictly between 0.01 and 0.99
    score = max(0.01, min(0.99, 1.0 - raw))
    return round(score, 4)


if __name__ == "__main__":
    for task in ["easy", "medium", "hard"]:
        score = grade(task)
        print(f"task={task} score={score}")
