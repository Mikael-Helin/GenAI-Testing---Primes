#!/usr/bin/env python3
"""
Sum all primes from sequence X(1) to X(10^8) where:
    X(0) = 1
    X(n+1) = (2147483647 * X(n) + 137438953471) mod 1400 + 1

Key insight: X values are in [1, 1400], so sequence must cycle within 1400 steps.
We detect the cycle and use math to avoid iterating 10^8 times.
"""

def solve():
    MULT = 2147483647
    ADD = 137438953471
    MOD = 1400
    N = 100_000_000
    
    # Sieve of Eratosthenes for primes up to 1400
    is_prime = [True] * 1401
    is_prime[0] = is_prime[1] = False
    for i in range(2, 38):  # sqrt(1400) < 38
        if is_prime[i]:
            for j in range(i * i, 1401, i):
                is_prime[j] = False
    
    # Generate sequence and detect cycle (guaranteed within 1401 steps)
    x = 1  # X(0)
    seq = []
    first_seen = {}
    
    cycle_start = None
    for i in range(1, 1402):
        x = (MULT * x + ADD) % MOD + 1
        if x in first_seen:
            cycle_start = first_seen[x]
            cycle_len = i - cycle_start
            break
        first_seen[x] = i
        seq.append(x)
    
    if cycle_start is None:
        raise RuntimeError("No cycle found - shouldn't happen!")
    
    # seq contains X(1), X(2), ..., X(i-1) where cycle was detected at i
    # Pre-cycle: X(1) to X(cycle_start - 1) -> seq[0 : cycle_start-1]
    # Cycle: X(cycle_start) to X(cycle_start + cycle_len - 1) -> seq[cycle_start-1 :]
    
    pre_cycle = seq[:cycle_start - 1]
    cycle = seq[cycle_start - 1:]
    
    sum_pre = sum(v for v in pre_cycle if is_prime[v])
    sum_cycle = sum(v for v in cycle if is_prime[v])
    
    num_pre = len(pre_cycle)
    
    # Edge case: N smaller than pre-cycle
    if N <= num_pre:
        return sum(v for v in pre_cycle[:N] if is_prime[v])
    
    # Calculate using cycle structure
    remaining = N - num_pre
    full_cycles = remaining // cycle_len
    leftover = remaining % cycle_len
    
    total = sum_pre + full_cycles * sum_cycle + sum(v for v in cycle[:leftover] if is_prime[v])
    
    return total


if __name__ == "__main__":
    result = solve()
    print(f"Sum of primes: {result}")