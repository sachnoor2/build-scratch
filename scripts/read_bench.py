#!/usr/bin/env python3
"""Print the benchmark as a GITHUB_OUTPUT line."""
import json
print(f"spf={json.load(open('bench.json'))['secondsPerFrame']}")
