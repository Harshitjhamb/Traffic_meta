# 🚦 Smart Traffic Signal Optimization Environment (OpenEnv)

## 🌍 Overview

This project presents a **Reinforcement Learning (RL) environment** for optimizing traffic signal control in multi-lane intersections under **dynamic and uncertain traffic conditions**.

Inspired by the patented concept:
**“Non-Internet Traffic Signal Timing Broadcast System Using Wired-Backbone RSUs and DSRC for Lane-Specific Vehicle Alerts”**,
this environment emphasizes **lane-specific intelligence, decentralized decision-making, and real-time optimization**.

---

## 🎯 Problem Statement

Urban intersections suffer from:

* 🚗 Excessive vehicle idling
* ⛽ Fuel wastage and emissions
* ❌ Lack of lane-specific signal control

The goal is to:

> Learn an optimal signaling policy that **minimizes congestion and total waiting time**.

---

## 🧠 RL Formulation

### 🔹 State Space (S)

```python
S = [l₁, l₂, l₃, l₄]
```

Where each `lᵢ` represents the number of vehicles in lane *i*.

---

### 🔹 Action Space (A)

```python
A ∈ {0, 1, 2, 3}
```

Selecting which lane receives the green signal.

---

### 🔹 Transition Function (P)

The environment evolves as:

* Vehicles in selected lane are cleared
* New vehicles arrive randomly

```python
lᵢ(t+1) = lᵢ(t) - μ·I(i = a) + εᵢ
```

Where:

* μ = vehicles cleared per step
* εᵢ ~ Uniform(0, k) (random arrivals)
* I = indicator function

---

## 🧮 Reward Function (Advanced Explanation)

### 🔹 Current Reward:

```python
R = - Σ lᵢ
```

👉 This represents **total congestion penalty**

---

### 🔥 Why this works:

* Encourages minimizing **global traffic load**
* Penalizes accumulation across all lanes
* Simple but effective baseline

---

### ⚠️ Limitation:

This reward does NOT:

* Penalize uneven congestion
* Capture worst-case lane buildup

---

### 🚀 Improved Reward (Advanced)

```python
R = - (Σ lᵢ + α · max(lᵢ))
```

Where:

* `Σ lᵢ` → total congestion
* `max(lᵢ)` → worst lane congestion
* `α` → weighting factor

👉 This ensures:

* Balanced traffic distribution
* Avoids extreme bottlenecks

---

### 🧠 RL Insight:

> This transforms the problem into a **multi-objective optimization**:

* Minimize total congestion
* Minimize peak congestion

---

## 🔁 Simulation Dynamics

At each timestep:

1. 🚦 Agent selects a lane
2. 🚗 Vehicles move through green signal
3. 🚙 New vehicles arrive (stochastic)
4. 📊 State updates
5. 🧮 Reward computed

---

## 📊 Example Simulation Step

```text
State: [10, 14, 17, 13]
Action: 2  (select lane with 17 vehicles)
```

### Step Execution:

* Clearance:

```text
17 → 15
```

* Random arrivals:

```text
[10, 14, 15, 13] → [11, 16, 17, 15]
```

* Reward:

```text
Total = 59 → Reward = -59
```

👉 Demonstrates **stochasticity + delayed optimization challenge**

---

## 🎬 Visualization

### 🔹 Traffic Evolution (Example)

![Traffic Simulation](assets/traffic_simulation.gif)

👉 Each frame shows:

* Vehicle density per lane
* Effect of signal decisions over time

---

## 🧪 Tasks

| Task   | Lanes | Complexity |
| ------ | ----- | ---------- |
| Easy   | 2     | Low        |
| Medium | 3     | Moderate   |
| Hard   | 4     | High       |

Each task returns a normalized score ∈ [0,1].

---

## 🤖 Baseline Policies

### 🔹 Heuristic Agent

```python
action = argmax(lanes)
```

Select lane with highest congestion.

---

### 🔹 Random Agent

```python
action = random.choice([0,1,2,3])
```

Used for baseline comparison.

---

## 🏗️ Architecture

```text
Traffic Controller (Agent)
        ↓
TrafficEnv (Simulation Engine)
        ↓
State → Action → Reward Loop
```

---

## 🚀 Key Innovations

* ✅ Lane-specific decision modeling (aligned with patent)
* ✅ Stochastic traffic dynamics
* ✅ Scalable RL environment
* ✅ Real-world applicability

---

## 📁 Project Structure

```bash
traffic-env/
│
├── env.py
├── models.py
├── tasks.py
├── grader.py
├── inference.py
├── openenv.yaml
├── Dockerfile
└── assets/
    └── traffic_simulation.gif
```

---

## 🐳 Running Locally

```bash
pip install -r requirements.txt
python test.py
```

---

## 🌐 Deployment

Compatible with:

* Docker
* Hugging Face Spaces
* OpenEnv validation framework

---

## 🔮 Future Work

* Multi-agent coordination
* Adaptive signal duration
* Integration with real traffic datasets
* Vehicle-to-Infrastructure (V2I) extension

---

## 🧠 Research Relevance

This environment models a **Markov Decision Process (MDP)** under uncertainty and can be extended to:

* Smart cities
* Autonomous traffic systems
* Sustainable urban planning

---

## 🏁 Conclusion

This project demonstrates how RL can address real-world infrastructure challenges by combining:

* Simulation
* Decision-making
* Optimization

---

## 👨‍💻 Author

Harshit Jhamb
NIT Delhi
