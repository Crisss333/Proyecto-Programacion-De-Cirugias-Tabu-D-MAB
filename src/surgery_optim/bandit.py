"""UCB1 operator selection with optional Page–Hinkley restart."""

from __future__ import annotations

import math


MOVES = ("swap", "insert", "room_1", "room_2", "room_pair")


class DynamicMultiArmedBandit:
    """Non-contextual D-MAB adapted from Da Costa et al. (GECCO 2008).

    Page–Hinkley resets only the reward estimates, never the Tabu search.
    Each arm starts with one observation before UCB1 scores are compared.
    """

    def __init__(self, *, delta: float = 0.01, threshold: float = 0.35,
                 dynamic: bool = True) -> None:
        if delta < 0 or threshold <= 0:
            raise ValueError("invalid Page–Hinkley parameters")
        self.delta = delta
        self.threshold = threshold
        self.dynamic = dynamic
        self.counts = {action: 0 for action in MOVES}
        self.means = {action: 0.0 for action in MOVES}
        self.cumulative = {action: 0.0 for action in MOVES}
        self.maximum = {action: 0.0 for action in MOVES}
        self.total_choices = {action: 0 for action in MOVES}
        self.restarts = 0

    def select(self) -> str:
        for action in MOVES:
            if self.counts[action] == 0:
                return action
        total = sum(self.counts.values())
        return max(
            MOVES,
            key=lambda action: (
                self.means[action]
                + math.sqrt(2.0 * math.log(total) / self.counts[action]),
                -MOVES.index(action),
            ),
        )

    def update(self, action: str, reward: float) -> bool:
        if action not in MOVES or not 0.0 <= reward <= 1.0:
            raise ValueError("unknown action or reward outside [0,1]")
        previous_count = self.counts[action]
        self.counts[action] = previous_count + 1
        self.total_choices[action] += 1
        self.means[action] = (
            previous_count * self.means[action] + reward
        ) / self.counts[action]
        self.cumulative[action] += reward - self.means[action] + self.delta
        self.maximum[action] = max(self.maximum[action], self.cumulative[action])
        if not self.dynamic or self.maximum[action] - self.cumulative[action] <= self.threshold:
            return False
        self.restarts += 1
        for arm in MOVES:
            self.counts[arm] = 0
            self.means[arm] = 0.0
            self.cumulative[arm] = 0.0
            self.maximum[arm] = 0.0
        return True
