def compute_score(total_waiting):
    score = max(0, 1 - total_waiting / 100)
    return min(score, 1.0)