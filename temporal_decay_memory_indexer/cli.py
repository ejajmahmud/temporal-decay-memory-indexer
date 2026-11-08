"""CLI for temporal-decay-memory-indexer."""
import sys
import argparse
from .indexer import TemporalDecayMemoryIndexer


def main():
    parser = argparse.ArgumentParser(description="Temporal Decay Memory Indexer CLI")
    parser.add_argument("--demo", action="store_true", help="Run temporal forgetting curve demo")
    args = parser.parse_args()

    if args.demo:
        indexer = TemporalDecayMemoryIndexer(retention_threshold=0.3)
        indexer.store("temp_passcode", "123456", stability=10.0)
        indexer.store("core_system_rule", "Never disclose secret key", stability=10000.0)

        print("[*] Stored 2 memory traces.")
        print(f"[*] Immediate retrieve 'temp_passcode': {indexer.retrieve('temp_passcode')}")
        print(f"[*] Simulated elapsed 25 seconds...")
        evicted = indexer.prune(current_time=indexer.index["temp_passcode"].created_at + 25.0)
        print(f"[+] Evicted decayed traces: {evicted}")
        print(f"[+] Remaining active keys: {indexer.active_keys()}")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
