import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install", "openai", "-q"])

import asyncio
import os
import textwrap
import requests
from typing import List, Optional
from openai import OpenAI

API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY") or "dummy"
API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"
ENV_URL = os.getenv("ENV_URL") or "https://harshitjhamb-meta-hackathon.hf.space"
TASK_NAME = os.getenv("TASK_NAME") or "easy"
BENCHMARK = "traffic-env"
MAX_STEPS = 8
TEMPERATURE = 0.7
MAX_TOKENS = 150
SUCCESS_SCORE_THRESHOLD = 0.1
MAX_TOTAL_REWARD = MAX_STEPS * 10.0

SYSTEM_PROMPT = textwrap.dedent("""
    You are an AI agent controlling traffic signals.
    You will receive the current lane vehicle counts and must choose which lane (0-3) to give the green signal.
    Respond with only a single integer: 0, 1, 2, or 3.
""").strip()

def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}", flush=True)

def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)

def get_action(client: OpenAI, lanes: List[int], step: int, history: List[str]) -> int:
    history_block = "\n".join(history[-4:]) if history else "None"
    user_prompt = textwrap.dedent(f"""
        Step: {step}
        Current lane vehicle counts: {lanes}
        Previous steps:
        {history_block}
        Which lane (0-3) should get the green signal? Reply with only a single integer.
    """).strip()
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )
        text = (completion.choices[0].message.content or "").strip()
        return int(text[0]) % 4
    except Exception as exc:
        print(f"[DEBUG] Model request failed: {exc}", flush=True)
        return 0

def main() -> None:
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    history: List[str] = []
    rewards: List[float] = []
    steps_taken = 0
    score = 0.0
    success = False

    log_start(task=TASK_NAME, env=BENCHMARK, model=MODEL_NAME)

    try:
        # Reset environment
        res = requests.post(f"{ENV_URL}/reset", timeout=30)
        obs = res.json()["observation"]
        lanes = obs["lanes"]

        for step in range(1, MAX_STEPS + 1):
            action = get_action(client, lanes, step, history)

            res = requests.post(f"{ENV_URL}/step", json={"signal": action}, timeout=30)
            result = res.json()
            obs = result["observation"]
            lanes = obs["lanes"]
            reward = float(result.get("reward", 0.0))
            done = result.get("done", False)

            rewards.append(reward)
            steps_taken = step
            log_step(step=step, action=str(action), reward=reward, done=done, error=None)
            history.append(f"Step {step}: signal={action} lanes={lanes} reward={reward:+.2f}")

            if done:
                break

        score = sum(rewards) / MAX_TOTAL_REWARD if MAX_TOTAL_REWARD > 0 else 0.0
        score = min(max(score, 0.0), 1.0)
        success = score >= SUCCESS_SCORE_THRESHOLD

    except Exception as e:
        print(f"[DEBUG] Exception: {e}", flush=True)

    log_end(success=success, steps=steps_taken, score=score, rewards=rewards)

if __name__ == "__main__":
    main()
