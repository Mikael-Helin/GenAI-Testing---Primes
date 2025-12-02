#!/usr/bin/env python3
"""
Create performance comparison visualization.
Tries matplotlib first, falls back to ASCII art if not available.
"""

import json
import os
import math

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load results
with open(os.path.join(SCRIPT_DIR, "test_results.json"), "r") as f:
    results = json.load(f)

# Sort by average time
sorted_results = sorted(results.items(), key=lambda x: x[1]['average'] if x[1]['average'] else float('inf'))

algorithms = [name for name, _ in sorted_results]
avg_times = [data['average'] for _, data in sorted_results]

# Try matplotlib first
try:
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
    import numpy as np

    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    colors = ['#2ecc71', '#27ae60', '#3498db', '#e74c3c', '#9b59b6', '#f39c12']

    # Plot 1: All algorithms (log scale)
    bars1 = ax1.bar(algorithms, avg_times, color=colors)
    ax1.set_yscale('log')
    ax1.set_ylabel('Average Time (seconds) - Log Scale')
    ax1.set_xlabel('Algorithm')
    ax1.set_title('Problem 1 Round 1 - All Algorithms\n(Log Scale)')
    ax1.tick_params(axis='x', rotation=45)

    for bar, time in zip(bars1, avg_times):
        height = bar.get_height()
        ax1.annotate(f'{time:.4f}s',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)

    # Plot 2: Only fast algorithms
    fast_algos = [(name, data['average']) for name, data in sorted_results if data['average'] < 1.0]
    if fast_algos:
        fast_names = [name for name, _ in fast_algos]
        fast_times = [time for _, time in fast_algos]
        bars2 = ax2.bar(fast_names, fast_times, color=colors[:len(fast_algos)])
        ax2.set_ylabel('Average Time (seconds)')
        ax2.set_xlabel('Algorithm')
        ax2.set_title('Problem 1 Round 1 - Fast Algorithms Only\n(Linear Scale)')
        ax2.tick_params(axis='x', rotation=45)

        for bar, time in zip(bars2, fast_times):
            height = bar.get_height()
            ax2.annotate(f'{time*1000:.2f}ms',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.savefig(os.path.join(SCRIPT_DIR, 'performance_comparison.png'), dpi=150, bbox_inches='tight')
    print(f"Diagram saved to: {os.path.join(SCRIPT_DIR, 'performance_comparison.png')}")

except ImportError:
    print("Matplotlib not available, creating ASCII diagram...")

# Always create ASCII diagram
def create_ascii_bar(value, max_value, width=50):
    """Create an ASCII bar."""
    if max_value == 0:
        return ""
    # Use log scale for better visualization
    log_val = math.log10(value + 0.001)
    log_max = math.log10(max_value + 0.001)
    log_min = math.log10(min(avg_times) + 0.001)

    normalized = (log_val - log_min) / (log_max - log_min) if log_max != log_min else 1
    bar_length = int(normalized * width)
    return '█' * max(1, bar_length)

print("\n" + "=" * 80)
print("PROBLEM 1 - ROUND 1: ALGORITHM PERFORMANCE COMPARISON")
print("=" * 80)
print("(5 runs per algorithm, sorted by average execution time)")
print()

max_time = max(avg_times)
max_name_len = max(len(name) for name in algorithms)

for name, time in zip(algorithms, avg_times):
    bar = create_ascii_bar(time, max_time)
    time_str = f"{time:.4f}s" if time < 1 else f"{time:.2f}s"
    print(f"{name:<{max_name_len}} │ {bar} {time_str}")

print()
print("=" * 80)
print("SPEEDUP COMPARISON (relative to slowest)")
print("=" * 80)
slowest = max(avg_times)
for name, time in zip(algorithms, avg_times):
    speedup = slowest / time
    print(f"{name:<{max_name_len}} │ {speedup:>8.1f}x faster than slowest")

print()
print("=" * 80)
print("KEY FINDINGS")
print("=" * 80)
print(f"Fastest: {algorithms[0]} ({avg_times[0]*1000:.2f} ms)")
print(f"Slowest: {algorithms[-1]} ({avg_times[-1]:.2f} s)")
print(f"Speed difference: {avg_times[-1]/avg_times[0]:.0f}x")
print()

# Categorize algorithms
fast_algos = [(n, t) for n, t in zip(algorithms, avg_times) if t < 0.1]
medium_algos = [(n, t) for n, t in zip(algorithms, avg_times) if 0.1 <= t < 10]
slow_algos = [(n, t) for n, t in zip(algorithms, avg_times) if t >= 10]

if fast_algos:
    print("FAST (<100ms) - Used cycle detection optimization:")
    for name, time in fast_algos:
        print(f"  • {name}: {time*1000:.2f}ms")

if medium_algos:
    print("\nMEDIUM (100ms - 10s):")
    for name, time in medium_algos:
        print(f"  • {name}: {time:.2f}s")

if slow_algos:
    print("\nSLOW (>10s) - Brute force iteration:")
    for name, time in slow_algos:
        print(f"  • {name}: {time:.2f}s")

# Save ASCII diagram to file
output_file = os.path.join(SCRIPT_DIR, "performance_diagram.txt")
with open(output_file, "w") as f:
    f.write("=" * 80 + "\n")
    f.write("PROBLEM 1 - ROUND 1: ALGORITHM PERFORMANCE COMPARISON\n")
    f.write("=" * 80 + "\n")
    f.write("(5 runs per algorithm, sorted by average execution time)\n\n")

    for name, time in zip(algorithms, avg_times):
        bar = create_ascii_bar(time, max_time)
        time_str = f"{time:.4f}s" if time < 1 else f"{time:.2f}s"
        f.write(f"{name:<{max_name_len}} | {bar} {time_str}\n")

    f.write("\n" + "=" * 80 + "\n")
    f.write("SUMMARY TABLE\n")
    f.write("=" * 80 + "\n")
    f.write(f"{'Algorithm':<20} {'Avg Time':<15} {'Min':<12} {'Max':<12} {'Runs':<8}\n")
    f.write("-" * 80 + "\n")

    for name, data in sorted_results:
        if data['average']:
            f.write(f"{name:<20} {data['average']:<15.4f} {data['min']:<12.4f} {data['max']:<12.4f} {data['successful_runs']:<8}\n")

    f.write("\n" + "=" * 80 + "\n")
    f.write("KEY FINDINGS\n")
    f.write("=" * 80 + "\n")
    f.write(f"Fastest: {algorithms[0]} ({avg_times[0]*1000:.2f} ms)\n")
    f.write(f"Slowest: {algorithms[-1]} ({avg_times[-1]:.2f} s)\n")
    f.write(f"Speed difference: {avg_times[-1]/avg_times[0]:.0f}x\n")

print(f"\nASCII diagram saved to: {output_file}")
