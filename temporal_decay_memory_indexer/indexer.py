"""Core Temporal Decay Memory Indexer implementation."""
import time
import math
from typing import Dict, List, Optional, Any


class MemoryTrace:
    def __init__(self, key: str, value: Any, stability: float = 3600.0, salience: float = 1.0):
        self.key = key
        self.value = value
        self.stability = stability  # Half-life in seconds
        self.salience = salience
        self.created_at = time.time()
        self.last_accessed = self.created_at
        self.reinforcement_count = 0

    def compute_retention(self, current_time: Optional[float] = None) -> float:
        now = current_time if current_time is not None else time.time()
        elapsed = max(0.0, now - self.last_accessed)
        # Ebbinghaus exponential decay: R = salience * exp(-t / stability)
        return self.salience * math.exp(-elapsed / max(1.0, self.stability))

    def reinforce(self, factor: float = 1.6):
        self.reinforcement_count += 1
        self.last_accessed = time.time()
        # Spaced repetition increases stability
        self.stability = min(86400.0 * 30.0, self.stability * factor)


class TemporalDecayMemoryIndexer:
    def __init__(self, retention_threshold: float = 0.25, max_items: int = 1000):
        self.retention_threshold = retention_threshold
        self.max_items = max_items
        self.index: Dict[str, MemoryTrace] = {}

    def store(self, key: str, value: Any, stability: float = 3600.0, salience: float = 1.0) -> MemoryTrace:
        trace = MemoryTrace(key, value, stability, salience)
        self.index[key] = trace
        if len(self.index) > self.max_items:
            self.prune()
        return trace

    def retrieve(self, key: str) -> Optional[Any]:
        if key not in self.index:
            return None
        trace = self.index[key]
        retention = trace.compute_retention()
        if retention < self.retention_threshold:
            del self.index[key]
            return None
        trace.reinforce()
        return trace.value

    def prune(self, current_time: Optional[float] = None) -> List[str]:
        now = current_time if current_time is not None else time.time()
        evicted = []
        for key, trace in list(self.index.items()):
            if trace.compute_retention(now) < self.retention_threshold:
                evicted.append(key)
                del self.index[key]
        return evicted

    def active_keys(self) -> List[str]:
        return list(self.index.keys())
