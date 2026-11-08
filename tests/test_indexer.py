"""Unit tests for temporal-decay-memory-indexer."""
import unittest
import time
from temporal_decay_memory_indexer.indexer import TemporalDecayMemoryIndexer, MemoryTrace


class TestTemporalDecayMemoryIndexer(unittest.TestCase):
    def test_store_and_retrieve(self):
        indexer = TemporalDecayMemoryIndexer()
        indexer.store("key1", "data1", stability=100.0)
        self.assertEqual(indexer.retrieve("key1"), "data1")

    def test_decay_and_prune(self):
        indexer = TemporalDecayMemoryIndexer(retention_threshold=0.3)
        trace = indexer.store("temp", "volatile", stability=5.0)
        # Advance virtual time by 20 seconds
        future_time = trace.created_at + 20.0
        evicted = indexer.prune(current_time=future_time)
        self.assertIn("temp", evicted)
        self.assertNotIn("temp", indexer.active_keys())

    def test_reinforcement_increases_stability(self):
        trace = MemoryTrace("k", "v", stability=10.0)
        orig_stability = trace.stability
        trace.reinforce()
        self.assertGreater(trace.stability, orig_stability)
        self.assertEqual(trace.reinforcement_count, 1)
