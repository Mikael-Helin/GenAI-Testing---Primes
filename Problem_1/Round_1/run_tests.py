#!/usr/bin/env python3
"""
Test runner for Problem 1 Round 1 algorithms.
Runs each algorithm 5 times and records execution times.
"""

import subprocess
import time
import json
import os

ALGORITHMS = [
    ("chatgpt_4.py", "ChatGPT 4"),
    ("chatgpt_5.1.py", "ChatGPT 5.1"),
    ("claude_opus_4.5.py", "Claude Opus 4.5"),
    ("gemini_1.5.py", "Gemini 1.5"),
    ("gemini_3_pro.py", "Gemini 3 Pro"),
    ("mikael.py", "Mikael"),
]

NUM_RUNS = 5
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def run_algorithm(filename):
    """Run an algorithm and return (execution_time, output, success)."""
    filepath = os.path.join(SCRIPT_DIR, filename)
    start_time = time.perf_counter()
    try:
        result = subprocess.run(
            ["python3", filepath],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        return execution_time, result.stdout.strip(), result.returncode == 0
    except subprocess.TimeoutExpired:
        return None, "TIMEOUT", False
    except Exception as e:
        return None, str(e), False

def main():
    results = {}

    for filename, name in ALGORITHMS:
        print(f"\n{'='*50}")
        print(f"Testing: {name} ({filename})")
        print('='*50)

        times = []
        outputs = []

        for run in range(1, NUM_RUNS + 1):
            print(f"  Run {run}/{NUM_RUNS}...", end=" ", flush=True)
            exec_time, output, success = run_algorithm(filename)

            if success and exec_time is not None:
                times.append(exec_time)
                outputs.append(output)
                print(f"{exec_time:.4f}s - Output: {output[:50]}...")
            else:
                print(f"FAILED - {output}")

        if times:
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            results[name] = {
                "filename": filename,
                "times": times,
                "average": avg_time,
                "min": min_time,
                "max": max_time,
                "output": outputs[0] if outputs else None,
                "successful_runs": len(times)
            }
            print(f"  Average: {avg_time:.4f}s | Min: {min_time:.4f}s | Max: {max_time:.4f}s")
        else:
            results[name] = {
                "filename": filename,
                "times": [],
                "average": None,
                "min": None,
                "max": None,
                "output": None,
                "successful_runs": 0
            }

    # Save results to JSON
    output_file = os.path.join(SCRIPT_DIR, "test_results.json")
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n\nResults saved to: {output_file}")

    # Print summary table
    print("\n" + "="*80)
    print("SUMMARY TABLE")
    print("="*80)
    print(f"{'Algorithm':<20} {'Avg Time (s)':<15} {'Min (s)':<12} {'Max (s)':<12} {'Runs':<8}")
    print("-"*80)

    sorted_results = sorted(results.items(), key=lambda x: x[1]['average'] if x[1]['average'] else float('inf'))

    for name, data in sorted_results:
        if data['average']:
            print(f"{name:<20} {data['average']:<15.4f} {data['min']:<12.4f} {data['max']:<12.4f} {data['successful_runs']:<8}")
        else:
            print(f"{name:<20} {'FAILED':<15} {'-':<12} {'-':<12} {0:<8}")

if __name__ == "__main__":
    main()
